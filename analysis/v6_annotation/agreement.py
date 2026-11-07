"""D3 dual-model agreement analysis for marriage-family narrative labels (Zhao Dingcheng).

Usage:
  python -I agreement.py LABELS_CSV [PREV_LABELS_CSV]     e.g. ../v6/results/dual_v1_labels.csv ../v6/results/dual_v0_labels.csv
  python -I agreement.py --stratified LABELS_CSV META_JSON  enriched sample from analysis/v6/deepseek_label.py enrich;
      needs CSV columns pid, stratum (cue_word / random_exposure_weighted), exposures, a reference label column
      (deepseek_group_label or group_label) and optionally qwen_group_label; META_JSON needs total_exposures
      (exposures of the whole candidate pool). Writes exposure-weighted shares, precision and recall.
  python -I agreement.py --enrich V0_LABELS V2_LABELS EXPOSURES META [DUAL_V2_LABELS]
      exact exposure-weighted group-label share in the enriched sample (cue words by exposures, random draws by
      draw counts; issue #27); with the 500-video check added to the random stratum as a pooled estimate.
  python -I agreement.py --selftest

Input: the CSV written by analysis/v6/dual_model_check.py (pid, exposures, {qwen,deepseek,gpt}_{issue,group_label,
narrative_type,genre,reason}); an empty cell means the model's output was missing or rejected by the parser.
Reference: DeepSeek V4 Pro (all rows); GPT-6.1 Sol is a second reference on the rows it labelled.
The sample was drawn with probability proportional to exposures, so unweighted shares over sampled videos
estimate shares of issue exposures; no further weighting is applied.

Writes to results/ next to this script (numbers, pids and categories only, no caption or reason text):
  agreement_<ver>.json            metrics with 95% intervals, missing counts, corrected prevalence, v0->v1 change
  agreement_<ver>_confusion.csv   group_label confusion matrices (incl. missing) for each model pair
  agreement_<ver>_disagreements.csv  pid, both labels, keyword-based disagreement category
  agreement_<ver>.meta.json       inputs, settings, commit, evidence type
"""
import json
import os
import re
import subprocess
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = ("qwen", "deepseek", "gpt")
POS = ("针对女性", "针对男性")
GL = ["针对女性", "针对男性", "无", "无法判断", "缺失"]
NT = ["群体标签", "唯一正确", "二元对立", "焦虑渲染", "无", "缺失"]
PAIRS = [("qwen", "deepseek"), ("qwen", "gpt"), ("deepseek", "gpt")]  # (rated, reference)
B = 2000
SEED = 0

# Keyword rules for sorting disagreements; applied in order to both models' reasons. A sorting aid, not a judgment.
CATEGORIES = [
    ("家庭角色被当作性别群体", r"婆婆|婆媳|后妈|继母|岳母|丈母娘|公公|父亲|母亲"),
    ("调侃或幽默被当作贬低", r"幽默|调侃|搞笑|玩笑|动物|狮子|怕老婆|可爱|称呼"),
    ("个案被说成推广", r"个别|个案|具体|个人|仅|单个|某个|角色"),
]


def wilson(k, n, z=1.96):
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]


def kappa(a, b):
    a, b = np.asarray(a), np.asarray(b)
    if len(a) == 0:
        return None
    cats = np.union1d(a, b)
    po = np.mean(a == b)
    pe = sum(np.mean(a == c) * np.mean(b == c) for c in cats)
    return 1.0 if pe == 1 else float((po - pe) / (1 - pe))


def boot(fn, n, rng):
    """Percentile 95% interval of fn(idx) over B bootstrap resamples of row indices."""
    vals = [fn(rng.integers(0, n, n)) for _ in range(B)]
    vals = [v for v in vals if v is not None and np.isfinite(v)]
    if len(vals) < B / 2:
        return [None, None]
    return [round(float(np.percentile(vals, 2.5)), 4), round(float(np.percentile(vals, 97.5)), 4)]


def rogan_gladen(q, tpr, fpr):
    if tpr is None or fpr is None or tpr - fpr <= 0:
        return None
    return float(min(1.0, max(0.0, (q - fpr) / (tpr - fpr))))


def load(path):
    d = pd.read_csv(path, dtype=str, keep_default_na=False)
    for m in MODELS:
        for f in ("issue", "group_label", "narrative_type", "genre") + tuple(QS):
            if f"{m}_{f}" in d.columns:
                d[f"{m}_{f}"] = d[f"{m}_{f}"].replace("", "缺失")
    return d


def version_of(path):
    m = re.search(r"dual_(v\d+)", os.path.basename(path))
    return m.group(1) if m else "x"


def pair_metrics(d, a, ref, rng):
    """Binary group label (either direction) of model a against reference ref, on rows both parsed."""
    rows = d[d[f"{ref}_issue"] != "缺失"]
    missing_a = int((rows[f"{a}_issue"] == "缺失").sum())
    both = rows[rows[f"{a}_issue"] != "缺失"]
    x = both[f"{a}_group_label"].isin(POS).to_numpy()
    y = both[f"{ref}_group_label"].isin(POS).to_numpy()
    same_dir = (both[f"{a}_group_label"].to_numpy() == both[f"{ref}_group_label"].to_numpy())
    tp, fp = int((x & y).sum()), int((x & ~y).sum())
    fn, tn = int((~x & y).sum()), int((~x & ~y).sum())
    n = len(both)
    out = {
        "rows_with_reference": int(len(rows)), "rows_both_parsed": n, f"missing_{a}": missing_a,
        "binary_counts": {"tp": tp, "fp": fp, "fn": fn, "tn": tn},
        "tp_same_direction": int((x & y & same_dir).sum()),
        f"{a}_positive_share": round(x.mean(), 4) if n else None,
        f"{ref}_positive_share": round(y.mean(), 4) if n else None,
        f"{ref}_positive_share_ci": wilson(int(y.sum()), n),
        "precision": round(tp / (tp + fp), 4) if tp + fp else None, "precision_ci": wilson(tp, tp + fp),
        "recall": round(tp / (tp + fn), 4) if tp + fn else None, "recall_ci": wilson(tp, tp + fn),
        "false_positive_rate": round(fp / (fp + tn), 4) if fp + tn else None, "false_positive_rate_ci": wilson(fp, fp + tn),
        "raw_agreement": round(float(np.mean(x == y)), 4) if n else None,
    }
    xa, ya = both[f"{a}_group_label"].to_numpy(), both[f"{ref}_group_label"].to_numpy()
    out["kappa_binary"] = kappa(x, y)
    out["kappa_binary_ci"] = boot(lambda i: kappa(x[i], y[i]), n, rng) if n else [None, None]
    out["kappa_group_label_4class"] = kappa(xa, ya)
    na, nb = both[f"{a}_narrative_type"].to_numpy(), both[f"{ref}_narrative_type"].to_numpy()
    out["kappa_narrative_type"] = kappa(na, nb)
    out["kappa_narrative_type_ci"] = boot(lambda i: kappa(na[i], nb[i]), n, rng) if n else [None, None]
    ia, ib = both[f"{a}_issue"].to_numpy(), both[f"{ref}_issue"].to_numpy()
    out["kappa_issue"] = kappa(ia, ib)
    for k in ("kappa_binary", "kappa_group_label_4class", "kappa_narrative_type", "kappa_issue"):
        out[k] = None if out[k] is None else round(out[k], 4)
    if a == "qwen":
        # Corrected share of group-label videos if Qwen labels a larger set with this error profile.
        def corr(i):
            xi, yi = x[i], y[i]
            if yi.sum() == 0 or (~yi).sum() == 0:
                return None
            return rogan_gladen(xi.mean(), (xi & yi).sum() / yi.sum(), (xi & ~yi).sum() / (~yi).sum())
        out["corrected_share_rogan_gladen"] = None if corr(np.arange(n)) is None else round(corr(np.arange(n)), 4)
        out["corrected_share_ci"] = boot(corr, n, rng)
    return out, both


def confusion(d, a, ref):
    rows = d if ref != "gpt" else d[d["gpt_issue"] != "缺失"]
    t = pd.crosstab(rows[f"{a}_group_label"], rows[f"{ref}_group_label"]).reindex(index=GL, columns=GL, fill_value=0)
    t.index.name, t.columns.name = a, ref
    long = t.stack().reset_index()
    long.columns = ["rated_label", "reference_label", "count"]
    long.insert(0, "reference", ref)
    long.insert(0, "rated", a)
    return long


def categorise(r, a, ref):
    pa, pr = r[f"{a}_group_label"] in POS, r[f"{ref}_group_label"] in POS
    if pa and pr:
        return "方向不同" if r[f"{a}_group_label"] != r[f"{ref}_group_label"] else "一致"
    if r[f"{a}_group_label"] in ("无法判断", "缺失") or r[f"{ref}_group_label"] in ("无法判断", "缺失"):
        return "无法判断或缺失"
    if not pa:
        return "漏判（参照判为群体标签）"
    if r[f"{ref}_narrative_type"] not in ("无", "群体标签", "缺失"):
        return "参照判为其他叙事类型"
    text = f"{r[f'{a}_reason']} {r[f'{ref}_reason']}"
    for name, pat in CATEGORIES:
        if re.search(pat, text):
            return name
    return "其他"


def disagreements(both, a, ref):
    x = both[f"{a}_group_label"].isin(POS)
    y = both[f"{ref}_group_label"].isin(POS)
    sel = both[(x != y) | (x & y & (both[f"{a}_group_label"] != both[f"{ref}_group_label"]))]
    out = pd.DataFrame({"rated": a, "reference": ref, "pid": sel["pid"], "exposures": sel["exposures"],
                        "rated_group_label": sel[f"{a}_group_label"], "reference_group_label": sel[f"{ref}_group_label"],
                        "rated_narrative_type": sel[f"{a}_narrative_type"], "reference_narrative_type": sel[f"{ref}_narrative_type"],
                        "rated_genre": sel[f"{a}_genre"],
                        "category": [categorise(r, a, ref) for _, r in sel.iterrows()]})
    return out


QS = ["q1_target", "q2_generalize", "q3_negative", "q4_endorse"]


def question_divergence(d, a, ref):
    """Where two models part ways on the four group-label questions (prompt v2 onwards).

    For rows both models labelled: agreement and kappa per question, and, for rows where the binary group label
    differs, the first question (in order) on which their answers differ.
    """
    if not all(f"{m}_{q}" in d.columns for m in (a, ref) for q in QS):
        return None
    rows = d[(d[f"{a}_issue"] != "缺失") & (d[f"{ref}_issue"] != "缺失")]
    out = {"rows": int(len(rows)), "per_question": {}}
    for q in QS:
        x, y = rows[f"{a}_{q}"].to_numpy(), rows[f"{ref}_{q}"].to_numpy()
        out["per_question"][q] = {"agreement": round(float(np.mean(x == y)), 4), "kappa": None if kappa(x, y) is None else round(kappa(x, y), 4),
                                  "crosstab": pd.crosstab(rows[f"{a}_{q}"], rows[f"{ref}_{q}"]).to_dict()}
    dis = rows[rows[f"{a}_group_label"].isin(POS) != rows[f"{ref}_group_label"].isin(POS)]

    def first(r):
        for q in QS:
            if r[f"{a}_{q}"] != r[f"{ref}_{q}"]:
                return f"{q}: {r[f'{a}_{q}']} vs {r[f'{ref}_{q}']}"
        return "same answers, different label"
    out["label_disagreements"] = int(len(dis))
    out["first_divergence"] = pd.Series([first(r) for _, r in dis.iterrows()], dtype=object).value_counts().to_dict()
    return out


def compare_versions(cur, prev):
    """Change from the previous prompt version on the same pids."""
    m = cur.merge(prev, on="pid", suffixes=("", "_prev"))
    out = {"common_pids": int(len(m))}
    for mod in MODELS:
        c, p = m[f"{mod}_group_label"], m[f"{mod}_group_label_prev"]
        ok = (c != "缺失") & (p != "缺失")
        out[mod] = {"positives_prev": int(p[ok].isin(POS).sum()), "positives_now": int(c[ok].isin(POS).sum()),
                    "pos_to_neg": int((p[ok].isin(POS) & ~c[ok].isin(POS)).sum()),
                    "neg_to_pos": int((~p[ok].isin(POS) & c[ok].isin(POS)).sum()), "rows": int(ok.sum()),
                    "missing_prev": int((p == "缺失").sum()), "missing_now": int((c == "缺失").sum())}
    return out


def rel(path):
    try:
        return os.path.relpath(path, HERE).replace("\\", "/")
    except ValueError:
        return os.path.abspath(path)


def git_commit():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=HERE).stdout.strip()
    except OSError:
        return None


def analyse(path, prev_path=None, out_dir=None, write=True):
    rng = np.random.default_rng(SEED)
    d = load(path)
    ver = version_of(path)
    res = {"input": rel(path), "prompt_version": ver, "n": int(len(d)),
           "missing": {m: int((d[f"{m}_issue"] == "缺失").sum()) for m in MODELS},
           "gpt_rows": int((d["gpt_issue"] != "缺失").sum()),
           "label_counts": {m: d.loc[d[f"{m}_issue"] != "缺失", f"{m}_group_label"].value_counts().to_dict() for m in MODELS},
           "pairs": {}}
    res["missing"]["gpt_note"] = "gpt labels only the first n_gpt rows; missing counts include unlabelled rows"
    conf, dis = [], []
    for a, ref in PAIRS:
        if res["gpt_rows"] == 0 and "gpt" in (a, ref):
            continue
        met, both = pair_metrics(d, a, ref, rng)
        res["pairs"][f"{a}_vs_{ref}"] = met
        conf.append(confusion(d, a, ref))
        dis.append(disagreements(both, a, ref))
    dis = pd.concat(dis, ignore_index=True)
    res["disagreement_categories"] = {f"{a}_vs_{ref}": dis[(dis.rated == a) & (dis.reference == ref)].category.value_counts().to_dict()
                                      for a, ref in PAIRS if f"{a}_vs_{ref}" in res["pairs"]}
    qd = {f"{a}_vs_{ref}": question_divergence(d, a, ref) for a, ref in PAIRS if f"{a}_vs_{ref}" in res["pairs"]}
    if any(qd.values()):
        res["question_divergence"] = qd
    if prev_path:
        res["change_from_" + version_of(prev_path)] = compare_versions(d, load(prev_path))
    if write:
        out_dir = out_dir or os.path.join(HERE, "results")
        os.makedirs(out_dir, exist_ok=True)
        stem = os.path.join(out_dir, f"agreement_{ver}")
        json.dump(res, open(stem + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        pd.concat(conf).to_csv(stem + "_confusion.csv", index=False, encoding="utf-8")
        dis.to_csv(stem + "_disagreements.csv", index=False, encoding="utf-8")
        meta = {"script": "analysis/v6_annotation/agreement.py", "commit": git_commit(), "date": time.strftime("%Y-%m-%d"),
                "inputs": [res["input"]] + ([rel(prev_path)] if prev_path else []),
                "reference_model": "deepseek-v4-pro; gpt-6.1-sol as second reference on its subset",
                "positive": "group_label in {针对女性, 针对男性}; 无法判断 counts as negative in binary metrics",
                "intervals": f"Wilson 95% for proportions; percentile bootstrap ({B} resamples, seed {SEED}) for kappa and corrected share",
                "weighting": "none (sample drawn proportional to exposures)",
                "evidence": "measured: LLM labels compared with a stronger LLM; not a human gold standard",
                "disagreement_categories": "keyword rules on both models' reasons (see CATEGORIES in script); sorting aid only"}
        json.dump(meta, open(stem + ".meta.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return res


CUE, RAND = "cue_word", "random_exposure_weighted"


def stratum_weights(d, total_exposures):
    """Row weights so that weighted sums estimate exposure-weighted shares of the whole candidate pool.

    Design (analysis/v6/deepseek_label.py enrich): the cue-word stratum is a census of candidates whose
    description contains a cue word, so each row counts with its own exposures; the random stratum is an
    exposure-weighted sample of the other candidates, so each row stands for an equal share of their exposures.
    """
    e = d["exposures"].astype(float).to_numpy()
    cue = (d["stratum"] == CUE).to_numpy()
    rnd = (d["stratum"] == RAND).to_numpy()
    e_cue = e[cue].sum()
    if not 0 < e_cue < total_exposures or rnd.sum() == 0:
        raise ValueError("need exposures > 0 in the cue stratum, total_exposures above that, and a random stratum")
    w = np.zeros(len(d))
    w[cue] = e[cue] / total_exposures
    w[rnd] = (total_exposures - e_cue) / total_exposures / rnd.sum()
    return w


def weighted_metrics(x, y, w):
    """Exposure-weighted reference share and rated-model precision, recall and false-positive rate."""
    out = {"reference_share": float((w * y).sum() / w.sum())}
    if x is not None:
        out["rated_share"] = float((w * x).sum() / w.sum())
        out["precision"] = float((w * x * y).sum() / (w * x).sum()) if (w * x).sum() > 0 else None
        out["recall"] = float((w * x * y).sum() / (w * y).sum()) if (w * y).sum() > 0 else None
        out["false_positive_rate"] = float((w * x * ~y).sum() / (w * ~y).sum()) if (w * ~y).sum() > 0 else None
    return out


def stratified(path, meta_path, rated="qwen", ref="deepseek", write=True):
    """Exposure-weighted estimates from the enriched (stratified) sample, with a within-stratum bootstrap."""
    d = pd.read_csv(path, dtype=str, keep_default_na=False)
    meta = json.load(open(meta_path, encoding="utf-8"))
    need = [c for c in ("pid", "stratum", "exposures") if c not in d.columns]
    if need or "total_exposures" not in meta:
        raise SystemExit(f"stratified input needs CSV columns pid, stratum, exposures and meta field total_exposures; missing: {need + ([] if 'total_exposures' in meta else ['total_exposures'])}")
    ref_col = f"{ref}_group_label" if f"{ref}_group_label" in d.columns else "group_label"
    rated_col = f"{rated}_group_label" if f"{rated}_group_label" in d.columns else None
    ok = d[ref_col] != ""
    if rated_col:
        ok &= d[rated_col] != ""
    res = {"input": rel(path), "meta": rel(meta_path), "rows": int(len(d)), "rows_used": int(ok.sum()),
           "missing": int((~ok).sum()), "rows_by_stratum": d.stratum.value_counts().to_dict(),
           "total_exposures": meta["total_exposures"], "reference": ref, "rated": rated if rated_col else None}
    d = d[ok].reset_index(drop=True)
    w = stratum_weights(d, float(meta["total_exposures"]))
    y = d[ref_col].isin(POS).to_numpy()
    x = d[rated_col].isin(POS).to_numpy() if rated_col else None
    res["reference_positives_by_stratum"] = {s: int(y[(d.stratum == s).to_numpy()].sum()) for s in (CUE, RAND)}
    res["estimates"] = {k: (None if v is None else round(v, 4)) for k, v in weighted_metrics(x, y, w).items()}
    rng = np.random.default_rng(SEED)
    groups = [np.flatnonzero((d.stratum == s).to_numpy()) for s in (CUE, RAND)]
    draws = []
    for _ in range(B):
        i = np.concatenate([rng.choice(g, len(g)) for g in groups])
        sub = d.iloc[i].reset_index(drop=True)
        draws.append(weighted_metrics(None if x is None else x[i], y[i], stratum_weights(sub, float(meta["total_exposures"]))))
    res["estimates_ci"] = {}
    for k in res["estimates"]:
        v = [r[k] for r in draws if r.get(k) is not None]
        res["estimates_ci"][k] = [round(float(np.percentile(v, 2.5)), 4), round(float(np.percentile(v, 97.5)), 4)] if len(v) > B / 2 else [None, None]
    if write:
        stem = os.path.join(HERE, "results", "agreement_" + os.path.splitext(os.path.basename(path))[0].replace("_labels", ""))
        os.makedirs(os.path.dirname(stem), exist_ok=True)
        json.dump(res, open(stem + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        json.dump({"script": "analysis/v6_annotation/agreement.py --stratified", "commit": git_commit(), "date": time.strftime("%Y-%m-%d"),
                   "weights": "cue stratum: own exposures / total; random stratum: (total - cue exposures) / total / n_random",
                   "intervals": f"percentile bootstrap within strata ({B} resamples, seed {SEED})",
                   "evidence": "measured: LLM labels; reference is a stronger LLM, not a human gold standard"},
                  open(stem + ".meta.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return res


def selftest_stratified(tmp):
    # Pool: 10 cue videos (exposures 10 each, 5 positive) and non-cue exposures 900 with 2% positives.
    rows = [{"pid": i, "stratum": CUE, "exposures": 10, "deepseek_group_label": "针对女性" if i < 5 else "无",
             "qwen_group_label": "针对女性" if i < 4 else "无"} for i in range(10)]
    rows += [{"pid": 100 + i, "stratum": RAND, "exposures": 1, "deepseek_group_label": "针对男性" if i < 2 else "无",
              "qwen_group_label": "针对男性" if i in (0, 50) else "无"} for i in range(100)]
    p, mp = os.path.join(tmp, "enrich_test_labels.csv"), os.path.join(tmp, "enrich_test_meta.json")
    pd.DataFrame(rows).to_csv(p, index=False)
    json.dump({"total_exposures": 1000}, open(mp, "w"))
    r = stratified(p, mp, write=False)["estimates"]
    # reference share = (5*10 + 900*0.02) / 1000 = 0.068; recall = (4*10 + 900*0.01) / 68
    assert abs(r["reference_share"] - 0.068) < 1e-4, r
    assert abs(r["recall"] - round(49 / 68, 4)) < 1e-4, r
    return r


def enrich_units(labels_path, exposures_path, meta, extra_noncue=None):
    """Weighted units for the enriched sample (analysis/v6/enrich_exposures.py design).

    Cue-word stratum: a census of videos, each weighted by its exposures. Random stratum: exposure-weighted draws
    with replacement, de-duplicated; each video is expanded to its number of draws, and each draw stands for
    non_cue_exposures / (valid draws). extra_noncue (optional): another exposure-weighted sample of non-cue videos
    from the same pool (pid, group_label), each row counted as one draw; videos already in the random stratum are
    not counted twice. Returns a frame with columns stratum, y (positive) and w (weight summing to 1).
    """
    lab = pd.read_csv(labels_path, dtype=str, keep_default_na=False)
    exp = pd.read_csv(exposures_path, dtype=str, keep_default_na=False)
    assert (lab.pid.values == exp.pid.values).all() and (lab.stratum.values == exp.stratum.values).all()
    d = lab.assign(exposures=exp.exposures.astype(float), draws=pd.to_numeric(exp.draws, errors="coerce").fillna(0))
    d = d[d.group_label != ""]
    total, e_cue, e_non = meta["candidate_pool_exposures"], meta["cue_word_exposures"], meta["non_cue_exposures"]
    cue = d[d.stratum == CUE]
    cue_units = pd.DataFrame({"stratum": CUE, "pid": cue.pid, "y": cue.group_label.isin(POS), "units": cue.exposures})
    rnd = d[d.stratum == RAND]
    rnd_units = pd.DataFrame({"stratum": RAND, "pid": rnd.pid, "y": rnd.group_label.isin(POS), "units": rnd.draws})
    if extra_noncue is not None:
        x = extra_noncue[~extra_noncue.pid.isin(set(d.pid))]
        rnd_units = pd.concat([rnd_units, pd.DataFrame({"stratum": RAND, "pid": x.pid, "y": x.group_label.isin(POS), "units": 1.0})])
    cue_units["w"] = cue_units.units / cue_units.units.sum() * e_cue / total
    rnd_units["w"] = rnd_units.units / rnd_units.units.sum() * e_non / total
    return pd.concat([cue_units, rnd_units], ignore_index=True)


def enrich_estimate(units, rng):
    """Exposure-weighted positive share with a bootstrap that resamples cue videos and random draws."""
    point = float((units.w * units.y).sum())
    by = {s: units[units.stratum == s] for s in (CUE, RAND)}
    share_cue = float((by[CUE].w * by[CUE].y).sum() / by[CUE].w.sum())
    share_rnd = float((by[RAND].w * by[RAND].y).sum() / by[RAND].w.sum())
    w_cue = float(by[CUE].w.sum())
    cue_y, cue_u = by[CUE].y.to_numpy(), by[CUE].units.to_numpy()
    draws_y = np.repeat(by[RAND].y.to_numpy(), by[RAND].units.round().astype(int).to_numpy())
    vals = []
    for _ in range(B):
        i = rng.integers(0, len(cue_y), len(cue_y))
        j = rng.integers(0, len(draws_y), len(draws_y))
        pc = (cue_u[i] * cue_y[i]).sum() / cue_u[i].sum()
        vals.append(w_cue * pc + (1 - w_cue) * draws_y[j].mean())
    ci = [round(float(np.percentile(vals, 2.5)), 4), round(float(np.percentile(vals, 97.5)), 4)]
    return {"share": round(point, 4), "ci": ci, "cue_share_exposure_weighted": round(share_cue, 4),
            "random_share_draw_weighted": round(share_rnd, 4), "w_cue": round(w_cue, 4),
            "cue_videos": int(len(by[CUE])), "random_units": int(len(by[RAND])), "random_draws": int(len(draws_y)),
            "positives": {"cue": int(by[CUE].y.sum()), "random": int(by[RAND].y.sum())}}


def enrich(labels_by_version, exposures_path, meta_path, dual_path=None, write=True):
    """Exact exposure-weighted gender group-label share in the enriched sample (issue #27)."""
    meta = json.load(open(meta_path, encoding="utf-8"))
    rng = np.random.default_rng(SEED)
    res = {"meta": rel(meta_path), "exposures": rel(exposures_path), "pool_exposures": meta["candidate_pool_exposures"],
           "cue_word_exposures": meta["cue_word_exposures"], "estimates": {}}
    extra = None
    if dual_path:
        dual = pd.read_csv(dual_path, dtype=str, keep_default_na=False)
        lab = pd.read_csv(labels_by_version["v2"], dtype=str, keep_default_na=False)
        cue_pids = set(lab[lab.stratum == CUE].pid)
        dn = dual[~dual.pid.isin(cue_pids) & (dual.deepseek_group_label != "")]
        extra = pd.DataFrame({"pid": dn.pid, "group_label": dn.deepseek_group_label})
        res["dual_noncue_rows"] = int(len(extra))
        res["dual_note"] = ("the 500-video check also kept the first unique videos of an exposure-weighted draw with replacement, "
                            "and its draw counts are not recorded, so each of its rows counts as one draw")
    for ver, path in labels_by_version.items():
        res["estimates"][f"{ver}_enriched_only"] = enrich_estimate(enrich_units(path, exposures_path, meta), rng)
        if extra is not None and ver == "v2":
            res["estimates"]["v2_pooled_with_500_check"] = enrich_estimate(enrich_units(path, exposures_path, meta, extra), rng)
    if write:
        stem = os.path.join(HERE, "results", "agreement_enrich")
        json.dump(res, open(stem + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        json.dump({"script": "analysis/v6_annotation/agreement.py --enrich", "commit": git_commit(), "date": time.strftime("%Y-%m-%d"),
                   "inputs": [rel(p) for p in labels_by_version.values()] + [rel(exposures_path), rel(meta_path)] + ([rel(dual_path)] if dual_path else []),
                   "weights": "cue stratum: each video by its exposures, scaled to the cue-word share of pool exposures; random stratum: each video by its number of draws, scaled to the non-cue share",
                   "intervals": f"percentile bootstrap ({B} resamples, seed {SEED}) over cue videos and random draws",
                   "evidence": "measured: DeepSeek V4 Pro labels; no human check"},
                  open(stem + ".meta.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return res


def selftest_enrich(tmp):
    # Pool exposures 1000: cue 100 (videos with 60 and 40 exposures; the 60 one positive),
    # non-cue 900 (draws: positive video drawn twice, negative video drawn 8 times) -> share = .06 + .9 * .2 = .24
    lab = pd.DataFrame({"pid": ["1", "2", "3", "4"], "stratum": [CUE, CUE, RAND, RAND],
                        "group_label": ["针对女性", "无", "针对男性", "无"]})
    exp = pd.DataFrame({"pid": ["1", "2", "3", "4"], "stratum": [CUE, CUE, RAND, RAND], "exposures": [60, 40, 5, 3], "draws": ["", "", 2, 8]})
    lp, ep = os.path.join(tmp, "enrich_lab.csv"), os.path.join(tmp, "enrich_exp.csv")
    lab.to_csv(lp, index=False)
    exp.to_csv(ep, index=False)
    meta = {"candidate_pool_exposures": 1000, "cue_word_exposures": 100, "non_cue_exposures": 900}
    r = enrich_estimate(enrich_units(lp, ep, meta), np.random.default_rng(0))
    assert abs(r["share"] - 0.24) < 1e-9, r
    return r


def selftest():
    assert abs(kappa([1, 1, 0, 0], [1, 1, 0, 0]) - 1) < 1e-9
    assert abs(kappa([1, 0, 1, 0], [1, 1, 0, 0]) - 0) < 1e-9
    lo, hi = wilson(5, 10)
    assert abs(lo - 0.2366) < 1e-3 and abs(hi - 0.7634) < 1e-3
    assert abs(rogan_gladen(0.2, 0.8, 0.0) - 0.25) < 1e-9
    rows = []
    gl = ["针对女性", "无", "无", "针对男性", "无", "无法判断", "", "无"]
    ref = ["针对女性", "无", "针对女性", "针对男性", "无", "无", "无", "针对男性"]
    for i, (a, b) in enumerate(zip(gl, ref)):
        rows.append({"pid": i, "exposures": 1, "qwen_issue": "是" if a else "", "qwen_group_label": a,
                     "qwen_narrative_type": ("群体标签" if a in POS else ("无" if a else "")), "qwen_genre": "其他" if a else "",
                     "qwen_reason": "对象：个人。剧情反派" if a else "", "deepseek_issue": "是", "deepseek_group_label": b,
                     "deepseek_narrative_type": "群体标签" if b in POS else "无", "deepseek_genre": "其他", "deepseek_reason": "x",
                     **{f"gpt_{f}": "" for f in ("issue", "group_label", "narrative_type", "genre", "reason")}})
    import tempfile
    tmp = tempfile.mkdtemp()
    p = os.path.join(tmp, "dual_v9_labels.csv")
    pd.DataFrame(rows).to_csv(p, index=False)
    r = analyse(p, prev_path=p, out_dir=tmp)
    m = r["pairs"]["qwen_vs_deepseek"]
    assert r["missing"]["qwen"] == 1 and m["rows_both_parsed"] == 7 and m["missing_qwen"] == 1
    assert m["binary_counts"] == {"tp": 2, "fp": 0, "fn": 2, "tn": 3}, m["binary_counts"]
    assert m["precision"] == 1.0 and m["recall"] == 0.5
    assert r["change_from_v9"]["qwen"]["pos_to_neg"] == 0
    print("selftest ok:", json.dumps(m["binary_counts"]), "kappa", m["kappa_binary"])
    print("stratified selftest ok:", json.dumps(selftest_stratified(tmp)))
    print("enrich selftest ok:", json.dumps(selftest_enrich(tmp)))


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif sys.argv[1:2] == ["--enrich"]:
        # --enrich V0_LABELS V2_LABELS EXPOSURES META [DUAL_V2_LABELS]
        a = sys.argv[2:]
        print(json.dumps(enrich({"v0": a[0], "v2": a[1]}, a[2], a[3], a[4] if len(a) > 4 else None), ensure_ascii=False, indent=1))
    elif sys.argv[1:2] == ["--stratified"]:
        print(json.dumps(stratified(sys.argv[2], sys.argv[3]), ensure_ascii=False, indent=1))
    else:
        r = analyse(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
        print(json.dumps({k: r["pairs"][k] for k in r["pairs"]}, ensure_ascii=False, indent=1))
