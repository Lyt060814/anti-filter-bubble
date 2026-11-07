"""Dual-model check of narrative labels on marriage-and-family videos (no human annotation).

Usage: python -I dual_model_check.py LLM_DIR RECIF_DIR OUT_PREFIX [N] [N_GPT] [PROMPT_VERSION]
  - samples N issue-candidate videos by exposure (same keyword set as v5),
  - labels them with Qwen3-30B (local vLLM, GPUs given by CUDA_VISIBLE_DEVICES, TP=2),
    DeepSeek V4 Pro (API, reference) and, on the first N_GPT, GPT-6.1 Sol (relay API, second reference).
Keys are read from the environment (source ~/.fb_api_env); nothing secret is written out.
Outputs: OUT_PREFIX_labels.csv (pid + each model's labels and one-line reason) and OUT_PREFIX_meta.json.
"""
import concurrent.futures as cf
import csv
import json
import os
import re
import sys
import time

import numpy as np
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from label_pilot import issue_captions, item_counts  # noqa: E402

PROMPT_VERSION = "v0"
SYSTEM = "你是严谨的内容分析标注员。只根据给出的视频描述判断，不猜测描述中没有的信息。只输出一个 JSON 对象。"
TEMPLATE = """以下是一条短视频的文字描述（由模型根据视频生成）：
「{cap}」

请按定义判断：
1. "issue"：视频主要内容是否涉及婚恋、夫妻、婆媳、两性关系或家庭中的性别角色。取值："是"/"否"。
2. "group_label"：视频是否给某一性别**群体整体**贴负面标签，或把个案说成该性别的普遍特征（如"女人都物质""男人没一个靠得住""这就是典型的凤凰男/捞女"）。
   - 只刻画某个具体人物的行为（包括剧情里的单个反派、个人经历中的某个人），没有推广到群体的，选"无"。
   - 判断看内容是否推广到群体，不看体裁；剧情、段子、评论都可能含群体标签。
   取值："针对女性"/"针对男性"/"无"/"无法判断"。
3. "narrative_type"：视频是否表达有争议的立场或叙事，属于哪一类："唯一正确"（把一种选择说成唯一正道并贬低其他）、"二元对立"（非此即彼）、"焦虑渲染"（用恐惧、紧迫感推动观点；不包括商品促销）、"群体标签"（同第2项）、"无"（中性记录、介绍或娱乐）。若第2项不是"无"，这里应为"群体标签"。
4. "genre"："剧情/段子"/"观点/评论"/"个人经历"/"新闻/普法"/"其他"。
5. "reason"：不超过30字的判断依据，用自己的话概括，不要引用描述原文。

只输出 JSON，例如：{{"issue":"是","group_label":"无","narrative_type":"二元对立","genre":"观点/评论","reason":"……"}}"""
FIELDS = {"issue": ["是", "否"], "group_label": ["针对女性", "针对男性", "无", "无法判断"],
          "narrative_type": ["唯一正确", "二元对立", "焦虑渲染", "群体标签", "无"],
          "genre": ["剧情/段子", "观点/评论", "个人经历", "新闻/普法", "其他"]}


def parse(text):
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if not all(d.get(k) in v for k, v in FIELDS.items()):
        return None
    d["reason"] = str(d.get("reason", ""))[:60]
    return d


def api_label(url, key, model, prompts, workers, extra):
    def one(p):
        body = {"model": model, "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": p}], **extra}
        for attempt in range(5):
            try:
                r = requests.post(url, headers={"Authorization": f"Bearer {key}"}, json=body, timeout=180)
                if r.status_code == 200:
                    return parse(r.json()["choices"][0]["message"]["content"])
            except Exception:
                pass
            time.sleep(2 * (attempt + 1))
        return None
    with cf.ThreadPoolExecutor(workers) as ex:
        return list(ex.map(one, prompts))


def main():
    llm_dir, recif_dir, prefix = sys.argv[1:4]
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 500
    n_gpt = int(sys.argv[5]) if len(sys.argv) > 5 else 150
    caps = issue_captions(recif_dir)
    cnt = item_counts(recif_dir, set(caps))
    seen = [p for p in cnt if cnt[p][0] > 0]
    w = np.array([cnt[p][0] for p in seen], float)
    rng = np.random.default_rng(23)
    pids = list(dict.fromkeys(np.array(seen)[rng.choice(len(seen), size=n * 3, p=w / w.sum())].tolist()))[:n]
    prompts = [TEMPLATE.format(cap=caps[p][:1200]) for p in pids]
    print("sampled", len(pids), flush=True)
    t0 = time.time()
    ds = api_label("https://api.deepseek.com/chat/completions", os.environ["DEEPSEEK_API_KEY"], "deepseek-v4-pro",
                   prompts, 16, {"max_tokens": 4000, "response_format": {"type": "json_object"}})
    print("deepseek done", sum(x is not None for x in ds), round(time.time() - t0), flush=True)
    gpt = api_label(os.environ["RELAY_OPENAI_BASE_URL"] + "/chat/completions", os.environ["RELAY_OPENAI_API_KEY"], "gpt-6.1-sol",
                    prompts[:n_gpt], 6, {}) + [None] * (len(prompts) - n_gpt)
    print("gpt done", sum(x is not None for x in gpt), round(time.time() - t0), flush=True)
    from vllm import LLM, SamplingParams
    llm = LLM(model=llm_dir, dtype="bfloat16", tensor_parallel_size=2, max_model_len=4096, gpu_memory_utilization=0.88, seed=0)
    tok = llm.get_tokenizer()
    qp = [tok.apply_chat_template([{"role": "system", "content": SYSTEM}, {"role": "user", "content": p}], tokenize=False, add_generation_prompt=True) for p in prompts]
    qw = [parse(o.outputs[0].text) for o in llm.generate(qp, SamplingParams(temperature=0.0, max_tokens=250), use_tqdm=False)]
    cols = ["issue", "group_label", "narrative_type", "genre", "reason"]
    with open(prefix + "_labels.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["pid", "exposures"] + [f"{m}_{c}" for m in ("qwen", "deepseek", "gpt") for c in cols])
        for p, a, b, c in zip(pids, qw, ds, gpt):
            wr.writerow([p, int(cnt[p][0])] + [((x or {}).get(k, "") if x else "") for x in (a, b, c) for k in cols])
    meta = {"prompt_version": PROMPT_VERSION, "n": len(pids), "n_gpt": n_gpt, "sampling": "exposure-weighted, seed 23, v5 marriage-family keywords",
            "models": {"qwen": "Qwen3-30B-A3B-Instruct-2507 (vLLM, temperature 0)", "deepseek": "deepseek-v4-pro (official API, json mode)",
                       "gpt": "gpt-6.1-sol (relay chat/completions)"},
            "parsed": {"qwen": sum(x is not None for x in qw), "deepseek": sum(x is not None for x in ds), "gpt": sum(x is not None for x in gpt)},
            "system_prompt": SYSTEM, "template": TEMPLATE, "date": time.strftime("%Y-%m-%d")}
    json.dump(meta, open(prefix + "_meta.json", "w"), ensure_ascii=False, indent=2)
    print(json.dumps(meta["parsed"]), flush=True)


if __name__ == "__main__":
    main()
