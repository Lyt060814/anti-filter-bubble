"""Does OneRec read the meaning of the "not interested" section, or only the items in it?

Usage: CUDA_VISIBLE_DEVICES=0 python -I onerec_ni_header_probe.py MODEL_DIR RECIF_DIR OUT_JSON [N_USERS]
Same 10 issue items are placed under different section headers; the issue share of the next
recommendation is computed exactly from model probabilities over a fixed candidate set
(issue and non-issue items), so no sampling noise.
"""
import json
import random
import sys

import numpy as np
import pyarrow.parquet as pq

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from onerec_manipulation_probe import ASK, HEAD, SYS, Maps, sid_str  # noqa: E402
from onerec_viewpoint_probe import Scorer, lse  # noqa: E402

HEADERS = {
    "ni_standard": "用户表示不感兴趣的内容：",
    "ni_variant": "用户不喜欢的内容：",
    "ni_block": "用户屏蔽的内容类型：",
    "neutral": "以下是一些内容：",
    "like": "用户喜欢的内容：",
}


def messages(hist, extra_header=None, extra=None):
    lines = ["以下是用户的历史互动行为："]
    for k in ["longview", "like", "follow", "forward", "not_interested"]:
        if hist.get(k):
            lines.append(HEAD[k] + "".join(sid_str(s) for s in hist[k]))
    if extra:
        lines.append(extra_header + "".join(sid_str(s) for s in extra))
    lines.append(ASK)
    return [{"role": "system", "content": SYS}, {"role": "user", "content": "\n".join(lines)}]


def main():
    model_dir, recif_dir, out_path = sys.argv[1:4]
    n_users = int(sys.argv[4]) if len(sys.argv) > 4 else 30
    rng = random.Random(11)
    maps = Maps(recif_dir)
    sc = Scorer(model_dir)
    lc = pq.read_table(f"{recif_dir}/benchmark_data/label_cond/label_cond_test.parquet").to_pylist()
    seen = {}
    for r in lc:
        for p in r["hist_longview"] + r["hist_like"]:
            seen[p] = seen.get(p, 0) + 1
    pool = [p for p, _ in sorted(seen.items(), key=lambda x: -x[1]) if maps.has(p)]
    issue_pool = [p for p in pool if maps.is_issue(p)][:400]
    ctrl_pool = [p for p in pool if not maps.is_issue(p)][:400]
    # Fixed candidate set: issue and non-issue items not used for injection.
    cand_issue = [int(p) for p in rng.sample(list(maps.pid[maps.pid_issue]), 1500)]
    cand_off = [int(p) for p in rng.sample(list(maps.pid[~maps.pid_issue]), 1500)]
    cands = [maps.sid_of(p) for p in cand_issue + cand_off]
    res = {k: [] for k in ["none", *HEADERS, "ctrl_ni_standard"]}
    seeds = [r for r in rng.sample(lc, 300) if len(r["hist_longview"]) >= 5 and not r["hist_not_interested"]][:n_users]
    for r in seeds:
        h0 = {k[5:]: [maps.sid_of(p) for p in r[k] if maps.has(p)] for k in r if k.startswith("hist_")}
        h0.pop("not_interested", None)
        iss = [maps.sid_of(p) for p in rng.sample(issue_pool, 10)]
        ctl = [maps.sid_of(p) for p in rng.sample(ctrl_pool, 10)]
        variants = {"none": messages(h0), **{k: messages(h0, v, iss) for k, v in HEADERS.items()},
                    "ctrl_ni_standard": messages(h0, HEADERS["ni_standard"], ctl)}
        for k, m in variants.items():
            lp = sc.logprobs(m, cands)
            res[k].append(lse(lp[:1500]) - np.logaddexp(lse(lp[:1500]), lse(lp[1500:])))
    out = {}
    base = np.array(res["none"])
    for k, v in res.items():
        v = np.array(v)
        d = v - base
        out[k] = {"logit_issue_share_mean": float(v.mean()), "diff_vs_none": float(d.mean()),
                  "se": float(d.std(ddof=1) / np.sqrt(len(d))), "share_users_up": float((d > 0).mean())}
    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
