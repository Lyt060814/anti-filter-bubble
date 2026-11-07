"""Bottom-up issue discovery: label an exposure-weighted random sample of RecIF videos with an open LLM.

Usage: CUDA_VISIBLE_DEVICES=1,2 python -I bottom_up_sample.py LLM_DIR RECIF_DIR OUT_PREFIX [N]
Samples N impressions uniformly from user histories (so videos are weighted by how often they are shown),
asks the LLM for domain, issue, whether the video carries an opposing narrative, and its type.
Writes per-video labels (pid + labels, no caption text) and a summary JSON.
"""
import collections
import json
import re
import sys

import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

DOMAINS = ["性别与婚恋", "身体与外貌", "家庭与代际", "人生选择与出路", "消费与经济", "资源与公平", "学术与思想",
           "文化与价值观", "公共秩序与自由", "其他社会议题", "非议题内容"]
TYPES = ["唯一正确", "二元对立", "焦虑渲染", "群体标签", "无"]
SYSTEM = "你是严谨的内容分析标注员。只根据给出的视频描述判断，不猜测描述中没有的信息。只输出一个 JSON 对象。"
TEMPLATE = """以下是一条短视频的文字描述（由模型根据视频生成）：
「{cap}」

请判断：
1. "domain"：视频主要涉及的社会议题大类，取值之一：{domains}。娱乐、美食、游戏、风景、商品展示、技能教学等不涉及社会观点争议的内容选"非议题内容"。
2. "issue"：若不是"非议题内容"，用不超过8个字写出具体议题（如"彩礼""考研考公""容貌焦虑"）；否则写"无"。
3. "opposing"：视频是否表达或强化了某种有争议的立场或叙事（而不只是中性记录或介绍）。取值："是"/"否"。
4. "narrative_type"：若 opposing 为"是"，叙事属于哪一类：
   "唯一正确"（把一种选择或做法说成唯一正道，贬低其他选择）；
   "二元对立"（把问题说成只有两边，非此即彼）；
   "焦虑渲染"（用恐惧、紧迫感推动观点或选择）；
   "群体标签"（给某类人整体贴负面标签或以偏概全）；
   否则为"无"。
5. "stance"：若 opposing 为"是"，用不超过20字概括视频的立场；否则写"无"。

只输出 JSON，例如：{{"domain":"性别与婚恋","issue":"彩礼","opposing":"是","narrative_type":"群体标签","stance":"……"}}"""


def parse(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if d.get("domain") not in DOMAINS or d.get("opposing") not in ("是", "否") or d.get("narrative_type") not in TYPES:
        return None
    return d


def main():
    llm_dir, recif_dir, prefix = sys.argv[1:4]
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 3000
    rng = np.random.default_rng(11)
    fb = pq.ParquetFile(f"{recif_dir}/onerec_bench_release.parquet")
    lens = [fb.metadata.row_group(i).num_rows for i in range(fb.num_row_groups)]
    picks = []
    for rg in range(fb.num_row_groups):
        flat = pc.list_flatten(fb.read_row_group(rg, columns=["hist_video_pid"]).column(0).combine_chunks()).to_numpy()
        k = rng.binomial(n * 2, len(flat) / (sum(lens) * 500))
        picks.append(rng.choice(flat, size=min(k, len(flat)), replace=False))
    sample = list(dict.fromkeys(np.concatenate(picks).tolist()))
    rng.shuffle(sample)
    want = pa.array(sample[: int(n * 1.3)], type=pa.int64())
    caps = {}
    f = pq.ParquetFile(f"{recif_dir}/pid2caption.parquet")
    for rg in range(f.num_row_groups):
        t = f.read_row_group(rg, columns=["pid", "dense_caption"])
        t = t.filter(pc.is_in(t.column("pid"), value_set=want.cast(t.column("pid").type)))
        caps.update(zip(t.column("pid").to_pylist(), t.column("dense_caption").to_pylist()))
    pids = [p for p in sample if caps.get(p)][:n]
    print("sampled", len(pids), flush=True)
    from vllm import LLM, SamplingParams
    llm = LLM(model=llm_dir, dtype="bfloat16", tensor_parallel_size=2, max_model_len=4096, gpu_memory_utilization=0.88, seed=0)
    tok = llm.get_tokenizer()
    prompts = [tok.apply_chat_template([{"role": "system", "content": SYSTEM},
                                        {"role": "user", "content": TEMPLATE.format(cap=caps[p][:1200], domains="、".join(f'"{d}"' for d in DOMAINS))}],
                                       tokenize=False, add_generation_prompt=True) for p in pids]
    res = llm.generate(prompts, SamplingParams(temperature=0.0, max_tokens=200), use_tqdm=False)
    rows, bad = [], 0
    for p, o in zip(pids, res):
        d = parse(o.outputs[0].text)
        if d is None:
            bad += 1
            continue
        rows.append({"pid": p, **d})
    with open(prefix + "_labels.jsonl", "w", encoding="utf-8") as fo:
        for r in rows:
            fo.write(json.dumps(r, ensure_ascii=False) + "\n")
    N = len(rows)
    out = {"labelled": N, "parse_failures": bad, "domains": {}}
    for dom in DOMAINS:
        R = [r for r in rows if r["domain"] == dom]
        opp = [r for r in R if r["opposing"] == "是"]
        out["domains"][dom] = {
            "share_of_sample": round(len(R) / max(N, 1), 4), "n": len(R),
            "opposing_share_within": round(len(opp) / max(len(R), 1), 3),
            "types": dict(collections.Counter(r["narrative_type"] for r in opp).most_common()),
            "top_issues": collections.Counter(r["issue"] for r in R).most_common(12),
        }
    json.dump(out, open(prefix + "_summary.json", "w"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
