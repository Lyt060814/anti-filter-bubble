"""D3 dual-model agreement analysis for marriage-family narrative labels (Zhao Dingcheng).

Usage:
  python -I agreement.py LABELS_CSV [PREV_LABELS_CSV]     e.g. ../v6/results/dual_v1_labels.csv ../v6/results/dual_v0_labels.csv
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
        for f in ("issue", "group_label", "narrative_type", "genre"):
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


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    else:
        r = analyse(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
        print(json.dumps({k: r["pairs"][k] for k in r["pairs"]}, ensure_ascii=False, indent=1))
