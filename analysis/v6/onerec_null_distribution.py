"""Null distribution for the OneRec attribute contrast (L4 control).

Usage: CUDA_VISIBLE_DEVICES=3 python -I onerec_null_distribution.py MODEL_DIR RECIF_DIR LABELS_JSONL OUT_JSON [K] [N_USERS]
Draws K random "pseudo-attributes" from videos labelled as not carrying a gender group label, each with the
same size and genre mix as the real group-label set, and runs the label-conditional injection test
(long-view and not-interested sections) used for the real attribute. Reports the contrast for each draw.
"""
import json
import random
import sys
from collections import Counter

import numpy as np
import pyarrow.parquet as pq

sys.path.insert(0, "analysis")
from onerec_manipulation_probe import Maps  # noqa: E402
from onerec_viewpoint_probe import Scorer, label_cond_messages, lse  # noqa: E402

model_dir, recif_dir, labels, out_path = sys.argv[1:5]
K = int(sys.argv[5]) if len(sys.argv) > 5 else 10
n_users = int(sys.argv[6]) if len(sys.argv) > 6 else 30
rng = random.Random(41)
maps = Maps(recif_dir)
rows = [json.loads(l) for l in open(labels, encoding="utf-8")]
rows = [r for r in rows if r["issue"] == "是" and maps.has(r["pid"])]
A = [r for r in rows if r["gender_generalization"] in ("针对女性", "针对男性")]
pool = [r for r in rows if r["gender_generalization"] == "无"]
mix = Counter(r["genre"] for r in A)
sc = Scorer(model_dir)
lc = pq.read_table(f"{recif_dir}/benchmark_data/label_cond/label_cond_test.parquet").to_pylist()
seeds = [r for r in rng.sample(lc, 300) if len(r["hist_longview"]) >= 5][:n_users]
off = [int(p) for p in rng.sample(list(maps.pid[~maps.pid_issue]), 400)]
results = []
for k in range(K):
    fake = []
    for g, c in mix.items():
        cand = [r["pid"] for r in pool if r["genre"] == g]
        fake += rng.sample(cand, min(c, len(cand)))
    fs = set(fake)
    rest = [r["pid"] for r in pool if r["pid"] not in fs]
    rng.shuffle(fake); rng.shuffle(rest)
    a_inj, a_ev = fake[: len(fake) // 2], fake[len(fake) // 2:]
    b_inj, b_ev = rest[:200], rest[200:400]
    ev = [maps.sid_of(p) for p in a_ev + b_ev] + [maps.sid_of(p) for p in off]
    nA, nB = len(a_ev), len(b_ev)
    diffs = {"lv": [], "ni": []}
    for r in seeds:
        h0 = {kk[5:]: [maps.sid_of(p) for p in r[kk] if maps.has(p)] for kk in r if kk.startswith("hist_")}
        ia = [maps.sid_of(p) for p in rng.sample(a_inj, 10)]
        ib = [maps.sid_of(p) for p in rng.sample(b_inj, 10)]
        m = {}
        for name, h in {"lv_A": {**h0, "longview": ia}, "lv_B": {**h0, "longview": ib},
                        "ni_A": {**h0, "not_interested": ia}, "ni_B": {**h0, "not_interested": ib}}.items():
            lp = sc.logprobs(label_cond_messages(h), ev)
            m[name] = lse(lp[:nA]) - lse(lp[nA:nA + nB])
        diffs["lv"].append(m["lv_A"] - m["lv_B"])
        diffs["ni"].append(m["ni_A"] - m["ni_B"])
    res = {"draw": k, "lv_A_vs_B": float(np.mean(diffs["lv"])), "ni_A_vs_B": float(np.mean(diffs["ni"])),
           "per_user_lv": diffs["lv"], "per_user_ni": diffs["ni"]}
    results.append(res)
    print(json.dumps({kk: v for kk, v in res.items() if not kk.startswith("per_user")}), flush=True)
lv = [r["lv_A_vs_B"] for r in results]; ni = [r["ni_A_vs_B"] for r in results]
summary = {"K": K, "n_users": n_users, "set_size": len(A), "genre_mix": dict(mix),
           "lv_null_mean": float(np.mean(lv)), "lv_null_sd": float(np.std(lv, ddof=1)), "lv_null_range": [min(lv), max(lv)],
           "ni_null_mean": float(np.mean(ni)), "ni_null_sd": float(np.std(ni, ddof=1)), "ni_null_range": [min(ni), max(ni)],
           "draws": results}
json.dump(summary, open(out_path, "w"), indent=2)
print(json.dumps({k: v for k, v in summary.items() if k != "draws"}))
