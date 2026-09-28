"""Step 5: early-warning evaluation.
For each at-risk user-day t (post-baseline, not currently in cocoon state), predict
y = "cocoon event on any of the next H days" from signals available at t.
User-level 70/30 train/test split. Usage: python 05_evaluate.py kuairec
"""
import json
import sys
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import roc_auc_score, average_precision_score, precision_score, recall_score, f1_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

name = sys.argv[1] if len(sys.argv) > 1 else "kuairec"
ud = pd.read_parquet(f"{name}_userday.parquet")
info = json.load(open(f"{name}_info.json"))
first_pred_seg = info.get("first_pred_seg", 1)   # segments before this are baseline

SCREEN = ["D20", "S20", "A20", "NOV20", "rD20", "rS20", "dD20", "dS20"]
PLATFORM = ["H_day", "RW", "relRW", "dH_day"]
REF = ["n"]                                          # activity only (naive benchmark)
ud["logn"] = np.log(ud.n)

rng = np.random.default_rng(42)
users = ud.u.unique()
test_users = set(rng.choice(users, size=int(0.3 * len(users)), replace=False))
ud["test"] = ud.u.isin(test_users)


def best_threshold(score, y):
    """threshold on 'score' (higher = more alarming) maximising F1 on training data"""
    qs = np.unique(np.quantile(score, np.linspace(0.5, 0.995, 100)))
    f1s = [f1_score(y, score >= q, zero_division=0) for q in qs]
    return qs[int(np.argmax(f1s))]


def evaluate(tag):
    y = f"y{tag}"
    r = ud[(ud.seg >= first_pred_seg) & ud[y].notna() & ud.RW.notna() & ud.B.notna()
           & ~ud[f"ev{tag}"] & (ud.n20 >= 20)].dropna(subset=SCREEN + PLATFORM)
    tr, te = r[~r.test], r[r.test]
    ytr, yte = tr[y].astype(int).values, te[y].astype(int).values
    out = {"tag": tag, "rows": len(r), "rows_test": len(te), "users": r.u.nunique(),
           "base_rate": float(r[y].mean()), "positives_test": int(yte.sum())}
    rows = []
    rules = {}
    preds = {}
    # (a) single-signal threshold rules
    for f in SCREEN + PLATFORM + REF:
        sign = 1 if roc_auc_score(ytr, tr[f]) >= 0.5 else -1   # orientation learned on train
        s_tr, s_te = sign * tr[f].values, sign * te[f].values
        th = best_threshold(s_tr, ytr)
        a = s_te >= th
        grp = "screen" if f in SCREEN else "platform" if f in PLATFORM else "reference"
        rows.append(dict(model=f"{f} ({'high' if sign > 0 else 'low'} = alarm)", group=grp, kind="single",
                         AUC=roc_auc_score(yte, s_te), AP=average_precision_score(yte, s_te),
                         precision=precision_score(yte, a, zero_division=0), recall=recall_score(yte, a),
                         alarm_rate=a.mean()))
        rules[f] = (sign, th)
    # (b)/(c) logistic regressions
    for label, feats, grp in [("LR screen", SCREEN, "screen"), ("LR platform", PLATFORM, "platform"),
                              ("LR screen+platform", SCREEN + PLATFORM, "platform"),
                              ("LR activity only (log n)", ["logn"], "reference"),
                              ("LR screen + log n", SCREEN + ["logn"], "screen"),
                              ("LR platform + log n", PLATFORM + ["logn"], "platform")]:
        m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)).fit(tr[feats], ytr)
        p_tr, p_te = m.predict_proba(tr[feats])[:, 1], m.predict_proba(te[feats])[:, 1]
        th = best_threshold(p_tr, ytr)
        a = p_te >= th
        rows.append(dict(model=label, group=grp, kind="LR", AUC=roc_auc_score(yte, p_te),
                         AP=average_precision_score(yte, p_te), precision=precision_score(yte, a, zero_division=0),
                         recall=recall_score(yte, a), alarm_rate=a.mean()))
        rules[label] = (m, th, feats)
        preds[label] = p_te
        hv = te.n.values >= 50                      # heavy user-days only (less sampling noise)
        rows[-1]["AUC_n>=50"] = roc_auc_score(yte[hv], p_te[hv]) if yte[hv].sum() > 5 else np.nan
        if label == "LR screen":
            coefs = dict(zip(feats, m[-1].coef_[0].round(3)))
    res = pd.DataFrame(rows)
    res["tag"] = tag
    out["coef_LR_screen"] = coefs
    best_single = res[(res.group == "screen") & (res.kind == "single")].sort_values("AUC").iloc[-1]
    out["best_single_screen"] = best_single.model
    out["gap_LR"] = float(res.set_index("model").AUC["LR platform"] - res.set_index("model").AUC["LR screen"])
    out["gap_single"] = float(res[(res.group == "platform") & (res.kind == "single")].AUC.max() - best_single.AUC)

    # 95% CI by bootstrapping TEST USERS (clusters), 300 resamples
    uids = te.u.values
    uniq = np.unique(uids)
    idx_by_u = pd.Series(np.arange(len(te))).groupby(uids).apply(np.array)
    bs = {"LR screen": [], "LR platform": [], "gap": []}
    brng = np.random.default_rng(0)
    for _ in range(300):
        idx = np.concatenate(idx_by_u.loc[brng.choice(uniq, len(uniq))].values)
        if yte[idx].sum() == 0:
            continue
        a1 = roc_auc_score(yte[idx], preds["LR screen"][idx]); a2 = roc_auc_score(yte[idx], preds["LR platform"][idx])
        bs["LR screen"].append(a1); bs["LR platform"].append(a2); bs["gap"].append(a2 - a1)
    out["CI95"] = {k_: [round(float(np.percentile(v, 2.5)), 3), round(float(np.percentile(v, 97.5)), 3)] for k_, v in bs.items()}

    # continuous outcome: change of R_W over the next non-overlapping window
    c = te.dropna(subset=["dRW_next"])
    ctr = tr.dropna(subset=["dRW_next"])
    out["spearman_dRW_next"] = {f: round(spearmanr(c[f], c.dRW_next)[0], 3) for f in SCREEN + PLATFORM + REF}
    for label, feats in [("screen", SCREEN), ("platform", PLATFORM)]:
        lr = LinearRegression().fit(ctr[feats], ctr.dRW_next)
        out[f"R2_dRW_next_{label}"] = round(lr.score(c[feats], c.dRW_next), 3)

    # lead time + false alarms on test users (best single screen rule, LR screen, LR platform)
    feat = best_single.model.split(" ")[0]
    lead = {}
    T = ud[ud.test & (ud.seg >= first_pred_seg) & ud.B.notna()].copy()
    ok = T[SCREEN + PLATFORM].notna().all(axis=1) & (T.n20 >= 20)
    sign, th = rules[feat]
    T["al_single"] = ok & (sign * T[feat] >= th)
    for lab in ["LR screen", "LR platform"]:
        m, th2, feats = rules[lab]
        pr = np.zeros(len(T)); pr[ok.values] = m.predict_proba(T.loc[ok, feats])[:, 1]
        T[f"al_{lab}"] = ok & (pr >= th2)
    segstart = {i: s for i, (s, _) in enumerate(info["segments"])}
    for col in ["al_single", "al_LR screen", "al_LR platform"]:
        leads, n_ev, n_fa_seg, n_noev_seg = [], 0, 0, 0
        for (uu, sg), g in T.groupby(["u", "seg"]):
            evd = g.loc[g[f"ev{tag}"], "day"]
            s0 = segstart[sg] + 2           # first day a W=3 window exists
            if len(evd):
                e0 = evd.min()
                if e0 <= s0:                # event already on the first observable day
                    continue
                n_ev += 1
                pre = g[(g.day >= s0) & (g.day < e0) & g[col]]
                if len(pre):
                    leads.append(e0 - pre.day.min())
            else:
                n_noev_seg += 1
                n_fa_seg += g[col].any()
        lead[col] = dict(events=n_ev, detected_share=round(len(leads) / max(n_ev, 1), 3),
                         lead_median=float(np.median(leads)) if leads else None,
                         lead_mean=round(float(np.mean(leads)), 2) if leads else None,
                         lead_hist=pd.Series(leads).value_counts().sort_index().to_dict(),
                         false_alarm_segments=round(n_fa_seg / max(n_noev_seg, 1), 3),
                         alarm_rate_userdays=round(float(T[col].mean()), 3))
    out["lead"] = lead
    out["rule_best_single"] = {"feature": feat, "sign": int(sign), "threshold": float(th)}
    return res, out


allres, outs = [], []
for tag in (15, 25):
    res, out = evaluate(tag)
    allres.append(res); outs.append(out)
    print(f"\n===== {name}: X={tag}%  rows={out['rows']} users={out['users']} base_rate={out['base_rate']:.4f} "
          f"test positives={out['positives_test']}")
    print(res.drop(columns="tag").round(3).to_string(index=False))
    for k_, v in out.items():
        if k_ not in ("tag",):
            print(k_, ":", v)
pd.concat(allres).to_csv(f"{name}_eval_results.csv", index=False)
json.dump(outs, open(f"{name}_eval_summary.json", "w"), indent=1, default=str)
