"""LLM labelling pilot on RecIF marriage-and-family captions (v5 feasibility).

Usage: python -I label_pilot.py MODEL_DIR RECIF_DIR OUT_PREFIX [N_EXPOSURE_WEIGHTED] [N_UNIFORM] [TP]

Samples issue-candidate items (keyword retrieval) by exposure and uniformly, labels several candidate
viewpoint attributes with an open-weight LLM, and reports prevalence (item-level and exposure-weighted)
and pooled engagement rates by label. Labels are model outputs for feasibility only, not gold labels.
"""
import collections
import json
import random
import re
import sys

import numpy as np
import pyarrow.compute as pc
import pyarrow.parquet as pq

ISSUE = ["离婚", "婆媳", "婆婆", "女方", "男方", "家暴", "出轨", "AA制", "彩礼", "结婚", "婚姻", "相亲", "夫妻", "老公", "老婆"]
SYSTEM = "你是严谨的内容分析标注员。只根据给出的视频描述判断，不要猜测描述中没有的信息。只输出一个 JSON 对象。"
TEMPLATE = """以下是一条短视频的文字描述（由模型根据视频生成）：
「{cap}」

请按定义判断：
1. "issue"：视频主要内容是否涉及婚恋、夫妻、婆媳、两性关系或家庭中的性别角色。取值："是"/"否"。
2. "genre"：视频形式。取值："剧情/段子"（虚构表演、短剧、搞笑段子）、"观点/评论"（博主直接表达看法）、"个人经历"（真人记录自己的生活）、"新闻/普法"、"其他"。
3. "gender_generalization"：视频是否把某一性别群体整体描绘为负面，或把个案归结为该性别的普遍特征（例如"女人都物质""男人都靠不住"，或使用"捞女""凤凰男""妈宝男"等标签贬低群体）。只描述某个具体人物的行为、没有推广到群体的，选"无"。取值："针对女性"/"针对男性"/"无"/"无法判断"。
4. "marriage_attitude"：视频对进入或维持婚姻传达的态度。取值："积极"（婚姻值得、用心经营）/"消极"（婚姻不值得、恐婚、劝人别结婚）/"中性或混合"/"不涉及"。
5. "conflict"：视频是否以婚恋或家庭冲突为核心（出轨、家暴、离婚纠纷、婆媳矛盾、彩礼纠纷等）。取值："是"/"否"。
6. "bride_price"：视频对彩礼的态度。取值："支持"/"反对或批评高额彩礼"/"中性"/"不涉及"。
7. "evidence"：不超过30字，概括判断依据。

只输出 JSON，例如：{{"issue":"是","genre":"剧情/段子","gender_generalization":"无","marriage_attitude":"不涉及","conflict":"是","bride_price":"不涉及","evidence":"……"}}"""
FIELDS = {"issue": ["是", "否"], "genre": ["剧情/段子", "观点/评论", "个人经历", "新闻/普法", "其他"],
          "gender_generalization": ["针对女性", "针对男性", "无", "无法判断"],
          "marriage_attitude": ["积极", "消极", "中性或混合", "不涉及"], "conflict": ["是", "否"],
          "bride_price": ["支持", "反对或批评高额彩礼", "中性", "不涉及"]}


def issue_captions(recif_dir):
    f = pq.ParquetFile(f"{recif_dir}/pid2caption.parquet")
    caps = {}
    for rg in range(f.num_row_groups):
        t = f.read_row_group(rg, columns=["pid", "dense_caption"])
        c = t.column("dense_caption")
        m = None
        for k in ISSUE:
            x = pc.match_substring(c, k)
            m = x if m is None else pc.or_(m, x)
        idx = np.flatnonzero(pc.fill_null(m, False).to_numpy(zero_copy_only=False))
        pids = t.column("pid").to_numpy()
        for i in idx:
            caps[int(pids[i])] = c[int(i)].as_py()
    return caps


def item_counts(recif_dir, items):
    cols = ["hist_video_pid", "hist_video_longview", "hist_video_like", "hist_video_not_interested",
            "target_video_pid", "target_video_longview", "target_video_like", "target_video_not_interested"]
    cnt = collections.defaultdict(lambda: np.zeros(4, np.int64))
    f = pq.ParquetFile(f"{recif_dir}/onerec_bench_release.parquet")
    for rg in range(f.num_row_groups):
        for r in f.read_row_group(rg, columns=cols).to_pylist():
            seq = (r["hist_video_pid"] or []) + (r["target_video_pid"] or [])
            lv = (r["hist_video_longview"] or []) + (r["target_video_longview"] or [])
            lk = (r["hist_video_like"] or []) + (r["target_video_like"] or [])
            ni = (r["hist_video_not_interested"] or []) + (r["target_video_not_interested"] or [])
            if not (len(seq) == len(lv) == len(lk) == len(ni)):
                continue
            for p, a, b, c in zip(seq, lv, lk, ni):
                if p in items:
                    cnt[p] += (1, a, b, c)
    return cnt


def parse(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if not all(d.get(k) in v for k, v in FIELDS.items()):
        return None
    return d


def main():
    model_dir, recif_dir, prefix = sys.argv[1:4]
    n_w = int(sys.argv[4]) if len(sys.argv) > 4 else 1200
    n_u = int(sys.argv[5]) if len(sys.argv) > 5 else 600
    tp = int(sys.argv[6]) if len(sys.argv) > 6 else 2
    rng = random.Random(7)
    caps = issue_captions(recif_dir)
    cnt = item_counts(recif_dir, set(caps))
    seen = [p for p in cnt if cnt[p][0] > 0]
    w = np.array([cnt[p][0] for p in seen], float)
    npr = np.random.default_rng(7)
    weighted = list(dict.fromkeys(np.array(seen)[npr.choice(len(seen), size=n_w * 2, p=w / w.sum())].tolist()))[:n_w]
    uniform = rng.sample([p for p in seen if p not in set(weighted)], n_u)
    sample = [(p, "exposure_weighted") for p in weighted] + [(p, "uniform") for p in uniform]
    print("captions", len(caps), "seen", len(seen), "sample", len(sample), flush=True)
    from vllm import LLM, SamplingParams
    llm = LLM(model=model_dir, dtype="bfloat16", tensor_parallel_size=tp, max_model_len=4096, gpu_memory_utilization=0.88, seed=0)
    tok = llm.get_tokenizer()
    prompts = [tok.apply_chat_template([{"role": "system", "content": SYSTEM},
                                        {"role": "user", "content": TEMPLATE.format(cap=caps[p][:1200])}],
                                       tokenize=False, add_generation_prompt=True) for p, _ in sample]
    res = llm.generate(prompts, SamplingParams(temperature=0.0, max_tokens=220), use_tqdm=False)
    rows, bad = [], 0
    for (p, how), o in zip(sample, res):
        d = parse(o.outputs[0].text)
        if d is None:
            bad += 1
            continue
        c = cnt[p]
        rows.append({"pid": p, "sample": how, "exp": int(c[0]), "longview": int(c[1]), "like": int(c[2]), "ni": int(c[3]),
                     "caption": caps[p], **d})
    with open(prefix + "_labels.jsonl", "w", encoding="utf-8") as fo:
        for r in rows:
            fo.write(json.dumps(r, ensure_ascii=False) + "\n")
    out = {"labelled": len(rows), "parse_failures": bad}
    for how in ("uniform", "exposure_weighted"):
        R = [r for r in rows if r["sample"] == how]
        rel = [r for r in R if r["issue"] == "是"]
        out[how] = {"n": len(R), "issue_yes": len(rel) / max(len(R), 1)}
        for fld in ("genre", "gender_generalization", "marriage_attitude", "conflict", "bride_price"):
            c = collections.Counter(r[fld] for r in rel)
            out[how][fld] = {k: round(v / max(len(rel), 1), 4) for k, v in c.most_common()}
    # Pooled engagement by label among relevant items (all sampled rows; exposures pooled).
    rel = [r for r in rows if r["issue"] == "是"]
    eng = {}
    for fld in ("gender_generalization", "marriage_attitude", "conflict", "genre"):
        g = collections.defaultdict(lambda: np.zeros(4))
        for r in rel:
            g[r[fld]] += (r["exp"], r["longview"], r["like"], r["ni"])
        eng[fld] = {k: {"items": sum(1 for r in rel if r[fld] == k), "exposures": int(v[0]),
                        "longview": v[1] / max(v[0], 1), "like": v[2] / max(v[0], 1), "ni": v[3] / max(v[0], 1)} for k, v in g.items()}
    out["engagement_by_label"] = eng
    ex = collections.defaultdict(list)
    for r in rel:
        if r["gender_generalization"] in ("针对女性", "针对男性") and len(ex[r["gender_generalization"]]) < 8:
            ex[r["gender_generalization"]].append({"evidence": r["evidence"], "caption": r["caption"][:200]})
        if r["marriage_attitude"] == "消极" and len(ex["婚姻消极"]) < 6:
            ex["婚姻消极"].append({"evidence": r["evidence"], "caption": r["caption"][:200]})
    out["examples"] = ex
    json.dump(out, open(prefix + "_summary.json", "w"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
