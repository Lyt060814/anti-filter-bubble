"""Issue #27: gender group labels in the enriched (cue-word + random) sample, prompt v0 vs v2 (Zhao Dingcheng).

Usage: python -I -X utf8 enrich_v2.py
Inputs (analysis/v6/results): enrich_ds_labels.csv (v0), enrich_v2_labels.csv (v2), dual_v2_labels.csv (500-video check).
Writes results/enrich_v2.json and results/enrich_v2.meta.json.

Design: the cue-word stratum is a census of candidate videos whose description contains a label word; the random
stratum is an exposure-weighted sample of the other candidates. The exposure-weighted share over all candidates is
    p = w_cue * p_cue + (1 - w_cue) * p_rand,
where w_cue is the cue-word videos' share of candidate exposures and p_cue their exposure-weighted positive share.
Neither is in the repository yet (issue #27 asks for exposures). Until then this script:
  - estimates w_cue from the 500-video check, which is itself an exposure-weighted sample of the same pool;
  - bounds p_cue between 0 and 1 and also reports the unweighted (per-video) cue share as a central value;
  - pools the non-cue videos of the 500-video check and the random stratum (both exposure-weighted, same model and
    prompt; duplicated pids counted once) for p_rand.
When exposures arrive, use agreement.py --stratified for the exact estimate.
"""
import json
import math
import os
import subprocess
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(HERE), "v6", "results")
POS = ("针对女性", "针对男性")
QS = ["q1_target", "q2_generalize", "q3_negative", "q4_endorse"]


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]


def share(k, n):
    return {"k": int(k), "n": int(n), "share": round(k / n, 4), "ci": wilson(k, n)}


def first_no(r):
    """First of the four v2 answers that rules out a gender group label."""
    if r.q1_target != "性别群体":
        return f"q1_target: {r.q1_target}"
    for q in QS[1:]:
        if r[q] != "是":
            return f"{q}: {r[q]}"
    return f"all yes, label {r.group_label_2}"


def main():
    v0 = pd.read_csv(os.path.join(RES, "enrich_ds_labels.csv"), dtype=str, keep_default_na=False)
    v2 = pd.read_csv(os.path.join(RES, "enrich_v2_labels.csv"), dtype=str, keep_default_na=False)
    dual = pd.read_csv(os.path.join(RES, "dual_v2_labels.csv"), dtype=str, keep_default_na=False)
    assert (v0.pid == v2.pid).all() and (v0.stratum == v2.stratum).all()
    res = {"rows": len(v2), "missing": {"v0": int((v0.group_label == "").sum()), "v2": int((v2.group_label == "").sum())}}

    # 1. per-stratum shares, each version on its own valid rows
    res["by_stratum"] = {}
    for name, d in (("v0", v0), ("v2", v2)):
        ok = d[d.group_label != ""]
        res["by_stratum"][name] = {st: share(g.group_label.isin(POS).sum(), len(g)) for st, g in ok.groupby("stratum")}

    # 2. v0 -> v2 transitions on rows valid in both, and where v2 rules out the v0 positives
    m = v0.join(v2, lsuffix="_0", rsuffix="_2")
    m = m[(m.group_label_0 != "") & (m.group_label_2 != "")]
    trans = {}
    for st, g in m.groupby("stratum_0"):
        a, b = g.group_label_0.isin(POS), g.group_label_2.isin(POS)
        trans[st] = {"rows": len(g), "v0_pos": int(a.sum()), "v2_pos": int(b.sum()), "both": int((a & b).sum()),
                     "v0_only": int((a & ~b).sum()), "v2_only": int((~a & b).sum())}
    res["v0_to_v2"] = trans
    cue = m[m.stratum_0 == "cue_word"].rename(columns={q: q for q in QS})
    lost = cue[cue.group_label_0.isin(POS) & ~cue.group_label_2.isin(POS)]
    gained = cue[~cue.group_label_0.isin(POS) & cue.group_label_2.isin(POS)]
    res["cue_v0_only_first_no_in_v2"] = lost.apply(first_no, axis=1).value_counts().to_dict()
    res["cue_v0_only_genre_v2"] = lost.genre_2.value_counts().to_dict()
    res["cue_v2_only_q_answers"] = gained[QS].astype(str).agg(" / ".join, axis=1).value_counts().to_dict()

    # 3. run-to-run consistency of DeepSeek v2 on videos in both the 500-video check and the enriched sample
    ov = dual.merge(v2[v2.group_label != ""], on="pid")
    res["repeat_consistency"] = {"videos": len(ov),
                                 "same_group_label": round(float((ov.deepseek_group_label == ov.group_label).mean()), 4),
                                 "same_q1": round(float((ov.deepseek_q1_target == ov.q1_target).mean()), 4)}

    # 4. exposure-weighted share, bounded until exposures are available
    cue_pids = set(v2[v2.stratum == "cue_word"].pid)
    dual["cue"] = dual.pid.isin(cue_pids)
    w = share(dual.cue.sum(), len(dual))
    rnd = v2[(v2.stratum != "cue_word") & (v2.group_label != "")][["pid", "group_label"]]
    dnc = dual[~dual.cue][["pid", "deepseek_group_label"]].rename(columns={"deepseek_group_label": "group_label"})
    pooled = pd.concat([rnd, dnc[~dnc.pid.isin(set(rnd.pid))]])
    p_rand = share(pooled.group_label.isin(POS).sum(), len(pooled))
    p_cue_videos = res["by_stratum"]["v2"]["cue_word"]["share"]
    lo = (1 - w["ci"][1]) * p_rand["ci"][0]
    hi = w["ci"][1] * 1.0 + (1 - w["ci"][0]) * p_rand["ci"][1]
    central = w["share"] * p_cue_videos + (1 - w["share"]) * p_rand["share"]
    res["exposure_weighted"] = {
        "w_cue_from_500_check": w,
        "p_rand_random_stratum_only": res["by_stratum"]["v2"]["random_exposure_weighted"],
        "p_rand_500_check_noncue_only": share(dnc.group_label.isin(POS).sum(), len(dnc)),
        "p_rand_pooled": p_rand,
        "central": round(central, 4),
        "bounds_any_p_cue": [round(lo, 4), round(hi, 4)],
        "bounds_p_cue_in_per_video_ci": [round((1 - w["ci"][1]) * p_rand["ci"][0] + w["ci"][0] * res["by_stratum"]["v2"]["cue_word"]["ci"][0], 4),
                                         round(w["ci"][1] * res["by_stratum"]["v2"]["cue_word"]["ci"][1] + (1 - w["ci"][0]) * p_rand["ci"][1], 4)],
        "note": "central uses the w_cue point estimate and the per-video cue share; both bounds take the Wilson ends of w_cue and p_rand; bounds_any_p_cue lets p_cue range over [0, 1], bounds_p_cue_in_per_video_ci over the per-video cue share's Wilson interval",
        "compare_500_check_v2": share(dual.deepseek_group_label.isin(POS).sum(), len(dual)),
    }
    out = os.path.join(HERE, "results", "enrich_v2")
    json.dump(res, open(out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=HERE).stdout.strip()
    except OSError:
        commit = None
    json.dump({"script": "analysis/v6_annotation/enrich_v2.py", "commit": commit, "date": time.strftime("%Y-%m-%d"),
               "inputs": ["analysis/v6/results/enrich_ds_labels.csv", "analysis/v6/results/enrich_v2_labels.csv",
                          "analysis/v6/results/dual_v2_labels.csv"],
               "intervals": "Wilson 95%", "status": "provisional: exposures per cue-word video and pool exposure totals not yet available (issue #27)",
               "evidence": "measured: DeepSeek V4 Pro labels; no human check"},
              open(out + ".meta.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
