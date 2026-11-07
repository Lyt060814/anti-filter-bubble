"""Label videos with DeepSeek V4 Pro through the official API (no GPU, no human annotation).

Usage (keys from `source ~/.fb_api_env`):
  python -I deepseek_label.py bottomup RECIF_DIR BOTTOM_UP_LABELS_CSV OUT_PREFIX
      re-label the 3,000 bottom-up impressions with an all-domain prompt (common rules from D1)
  python -I deepseek_label.py stratified RECIF_DIR N_SCREEN PER_DOMAIN OUT_PREFIX
      screen N_SCREEN exposure-weighted impressions with deepseek-flash (cross-domain prompt), then relabel up to
      PER_DOMAIN impressions in each studied domain (by the flash domain) with V4 Pro; strata sizes go to meta
  python -I deepseek_label.py enrich RECIF_DIR N_RANDOM OUT_PREFIX
      marriage-and-family candidates: all with explicit label/generalisation cue words, plus N_RANDOM
      exposure-weighted random candidates; labelled with the v0 dual-check prompt (stratum recorded)
Outputs OUT_PREFIX_labels.csv (pid, stratum, labels, one-line reason; no caption text) and OUT_PREFIX_meta.json.
"""
import concurrent.futures as cf
import csv
import json
import os
import re
import sys
import time

import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dual_model_check as dmc  # noqa: E402
from label_pilot import issue_captions, item_counts  # noqa: E402

MODEL = "deepseek-v4-pro"
DOMAINS = ["性别与婚恋", "身体与外貌", "家庭与代际", "人生选择与出路", "消费与经济", "资源与公平", "学术与思想",
           "文化与价值观", "公共秩序与自由", "其他社会议题", "非议题内容"]
TYPES = ["唯一正确", "二元对立", "焦虑渲染", "群体标签", "无"]
BU_TEMPLATE = """以下是一条短视频的文字描述（由模型根据视频生成）：
「{cap}」

请判断：
1. "domain"：视频主要涉及的社会议题大类，取值之一：{domains}。娱乐、美食、游戏、风景、商品展示、技能教学等不涉及社会观点争议的内容选"非议题内容"。
2. "issue"：若不是"非议题内容"，用不超过8个字写出具体议题；否则写"无"。
3. "opposing"：视频本身是否认同并表达了某种有争议的立场或叙事。注意：只转述、反驳或嘲讽某种说法不算；讲冲突或纠纷但不表态不算；商品、课程、"赚钱游戏"等营销推销不算；中性记录、介绍、娱乐不算。取值："是"/"否"。
4. "narrative_type"：若 opposing 为"是"，选一类（按此顺序取第一个符合的）："群体标签"（给某类人整体贴负面标签或把个案说成群体特征）、"唯一正确"（把一种选择说成唯一正道并贬低其他）、"二元对立"（非此即彼的两个阵营）、"焦虑渲染"（用恐惧、紧迫感、羞耻感推动观点或选择）；否则为"无"。
5. "reason"：不超过30字，用自己的话概括依据，不要引用描述原文。

只输出 JSON，例如：{{"domain":"性别与婚恋","issue":"彩礼","opposing":"否","narrative_type":"无","reason":"……"}}"""
CUES = ["捞女", "凤凰男", "扶弟魔", "妈宝男", "普信男", "小仙女", "女拳", "田园女权", "女人都", "男人都", "女的都", "男的都",
        "现在的女人", "现在的男人", "现在的女孩", "女人就是", "男人就是", "物质女", "拜金", "渣男", "绿茶"]


def bu_parse(text):
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if d.get("domain") not in DOMAINS or d.get("opposing") not in ("是", "否") or d.get("narrative_type") not in TYPES:
        return None
    if d["opposing"] == "否" and d["narrative_type"] != "无":
        return None
    d["reason"] = str(d.get("reason", ""))[:60]
    return d


def call(prompts, parse, system, model=None, workers=16):
    key = os.environ["DEEPSEEK_API_KEY"]
    model = model or MODEL

    def one(p):
        body = {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": p}],
                "max_tokens": 4000, "response_format": {"type": "json_object"}}
        for attempt in range(5):
            try:
                r = requests.post("https://api.deepseek.com/chat/completions", headers={"Authorization": f"Bearer {key}"}, json=body, timeout=180)
                if r.status_code == 200:
                    out = parse(r.json()["choices"][0]["message"]["content"])
                    if out is not None:
                        return out
            except Exception:
                pass
            time.sleep(2 * (attempt + 1))
        return None
    with cf.ThreadPoolExecutor(workers) as ex:
        return list(ex.map(one, prompts))


def captions(recif_dir, pids):
    want = pa.array(list(pids), type=pa.int64())
    out = {}
    f = pq.ParquetFile(f"{recif_dir}/pid2caption.parquet")
    for rg in range(f.num_row_groups):
        t = f.read_row_group(rg, columns=["pid", "dense_caption"])
        t = t.filter(pc.is_in(t.column("pid"), value_set=want.cast(t.column("pid").type)))
        out.update(zip(t.column("pid").to_pylist(), t.column("dense_caption").to_pylist()))
    return out


def main():
    mode, recif_dir = sys.argv[1:3]
    t0 = time.time()
    if mode == "bottomup":
        src, prefix = sys.argv[3:5]
        pids = [int(r["pid"]) for r in csv.DictReader(open(src, encoding="utf-8"))]
        caps = captions(recif_dir, pids)
        pids = [p for p in pids if caps.get(p)]
        prompts = [BU_TEMPLATE.format(cap=caps[p][:1200], domains="、".join(f'"{d}"' for d in DOMAINS)) for p in pids]
        res = call(prompts, bu_parse, dmc.SYSTEM)
        cols = ["domain", "issue", "opposing", "narrative_type", "reason"]
        strata = ["bottom_up"] * len(pids)
        meta = {"mode": mode, "template": BU_TEMPLATE, "source": src}
    elif mode == "stratified":
        n_screen, per_domain, prefix = int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
        studied = ["性别与婚恋", "身体与外貌", "家庭与代际", "人生选择与出路", "消费与经济"]
        rng = np.random.default_rng(31)
        fb = pq.ParquetFile(f"{recif_dir}/onerec_bench_release.parquet")
        total = fb.metadata.num_rows * 470
        picks = []
        for rg in range(fb.num_row_groups):
            flat = pc.list_flatten(fb.read_row_group(rg, columns=["hist_video_pid"]).column(0).combine_chunks()).to_numpy()
            k = rng.binomial(int(n_screen * 1.4), min(1.0, len(flat) / total))
            picks.append(rng.choice(flat, size=min(k, len(flat)), replace=False))
        sample = np.concatenate(picks).tolist()
        rng.shuffle(sample)
        caps = captions(recif_dir, set(sample))
        screen = [p for p in sample if caps.get(p)][:n_screen]
        fl = call([BU_TEMPLATE.format(cap=caps[p][:1200], domains="、".join(f'"{d}"' for d in DOMAINS)) for p in screen],
                  bu_parse, dmc.SYSTEM, model="deepseek-flash", workers=32)
        with open(prefix + "_screen.csv", "w", newline="", encoding="utf-8") as f:
            wr = csv.writer(f)
            wr.writerow(["pid", "flash_domain", "flash_opposing", "flash_narrative_type"])
            for p, d in zip(screen, fl):
                wr.writerow([p, (d or {}).get("domain", ""), (d or {}).get("opposing", ""), (d or {}).get("narrative_type", "")])
        strata_sizes = {dom: sum(1 for d in fl if d and d["domain"] == dom) for dom in DOMAINS}
        pids, strata = [], []
        for dom in studied:
            members = [p for p, d in zip(screen, fl) if d and d["domain"] == dom]
            chosen = members if len(members) <= per_domain else [members[i] for i in sorted(rng.choice(len(members), per_domain, replace=False))]
            pids += chosen
            strata += [dom] * len(chosen)
        prompts = [BU_TEMPLATE.format(cap=caps[p][:1200], domains="、".join(f'"{d}"' for d in DOMAINS)) for p in pids]
        res = call(prompts, bu_parse, dmc.SYSTEM)
        cols = ["domain", "issue", "opposing", "narrative_type", "reason"]
        meta = {"mode": mode, "template": BU_TEMPLATE, "screen_model": "deepseek-flash", "n_screen": len(screen),
                "screen_parsed": sum(d is not None for d in fl), "flash_domain_counts": strata_sizes, "per_domain": per_domain,
                "sampled_per_stratum": {dom: strata.count(dom) for dom in studied}, "random_seed": 31,
                "weighting": "stratum = flash domain; within-stratum weight = flash_domain_counts[d] / sampled_per_stratum[d]; screen is exposure-weighted"}
    else:
        n_random, prefix = int(sys.argv[3]), sys.argv[4]
        caps = issue_captions(recif_dir)
        cue = [p for p, c in caps.items() if any(k in c for k in CUES)]
        cnt = item_counts(recif_dir, set(caps))
        seen = [p for p in cnt if cnt[p][0] > 0]
        w = np.array([cnt[p][0] for p in seen], float)
        rng = np.random.default_rng(29)
        rand = list(dict.fromkeys(np.array(seen)[rng.choice(len(seen), size=n_random * 3, p=w / w.sum())].tolist()))[:n_random]
        cue_set = set(cue)
        pids = [p for p in cue] + [p for p in rand if p not in cue_set]
        strata = ["cue_word"] * len(cue) + ["random_exposure_weighted"] * (len(pids) - len(cue))
        prompts = [dmc.TEMPLATE.format(cap=caps[p][:1200]) for p in pids]
        res = call(prompts, dmc.parse, dmc.SYSTEM)
        cols = ["issue", "group_label", "narrative_type", "genre", "reason"]
        meta = {"mode": mode, "prompt": "v0 (analysis/v6/dual_model_check.py)", "cue_words": CUES, "n_cue_candidates": len(cue),
                "n_random": len(pids) - len(cue), "candidate_pool": len(caps), "random_seed": 29,
                "note": "stratified sample: cue-word stratum is a census of candidates containing any cue word; random stratum is exposure-weighted from all candidates (cue-word videos excluded from it)"}
    with open(prefix + "_labels.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["pid", "stratum"] + cols)
        for p, s, d in zip(pids, strata, res):
            wr.writerow([p, s] + [(d or {}).get(c, "") for c in cols])
    meta.update({"model": MODEL, "n": len(pids), "parsed": sum(d is not None for d in res), "seconds": round(time.time() - t0),
                 "date": time.strftime("%Y-%m-%d")})
    json.dump(meta, open(prefix + "_meta.json", "w"), ensure_ascii=False, indent=2)
    print(json.dumps({k: v for k, v in meta.items() if k not in ("template", "cue_words")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
