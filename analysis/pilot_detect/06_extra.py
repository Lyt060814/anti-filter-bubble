"""Step 6: extra checks.
(a) KuaiRec 'nowcasting': do first-20 screen signals track today's full-information entropy?
(b) KuaiRec long-horizon narrowing: pooled entropy per observed segment vs own baseline (+ noise null).
(c) KuaiRand-Pure replication (is_rand==0, first tag as category): reachability of N=20,
    static screen-vs-platform agreement, and week-0 vs later narrowing (+ noise null).
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from detect_lib import norm_entropy

rng = np.random.default_rng(0)


def drop_table(base_counts, later_counts, K, label):
    """share of users whose pooled entropy in 'later' is >=X% below baseline, vs. multinomial null"""
    B = norm_entropy(base_counts, K)
    L = norm_entropy(later_counts, K)
    pB = base_counts / base_counts.sum(1, keepdims=True)
    Lnull = np.array([norm_entropy(rng.multinomial(n, p), K) for n, p in zip(later_counts.sum(axis=1), pB)])
    # parametric bootstrap null: redraw BOTH periods from the user's baseline mix (same sizes)
    Bnull = np.array([norm_entropy(rng.multinomial(n, p), K) for n, p in zip(base_counts.sum(axis=1), pB)])
    rel, reln = L / B - 1, Lnull / Bnull - 1
    print(f"{label}: users {len(B)}, median relative change {np.median(rel):+.3f} (null {np.median(reln):+.3f})")
    for X in (0.05, 0.10, 0.15, 0.25):
        print(f"   drop >= {int(X*100)}%: observed {np.mean(rel <= -X):.4f}  null {np.mean(reln <= -X):.4f}")
    print(f"   rise >= 10%: observed {np.mean(rel >= 0.10):.4f}")
    return rel


# ---------------- (a) KuaiRec nowcasting ----------------
ud = pd.read_parquet("kuairec_userday.parquet")
print("== (a) KuaiRec: Spearman correlation of screen signals with full-information entropy (same day)")
for nmin in (20, 60, 100):
    s = ud[ud.n >= nmin].dropna(subset=["D20", "S20", "H_day"])
    print(f"   user-days n>={nmin} ({len(s)}): D20~H_day {spearmanr(s.D20, s.H_day)[0]:.3f}, "
          f"S20~H_day {spearmanr(s.S20, s.H_day)[0]:.3f}, D20~R3 {spearmanr(s.D20, s.RW, nan_policy='omit')[0]:.3f}")

# ---------------- (b) KuaiRec long-horizon ----------------
print("\n== (b) KuaiRec pooled segment entropy vs baseline (days 0-6)")
e = pd.read_parquet("kuairec_exposures.parquet", columns=["user_id", "day", "cat"])
e = e[e.cat >= 0]
K = 38
seg = pd.cut(e.day, [-1, 6, 7, 36, 62], labels=["A_base", "A_day7", "B", "C"])
cnt = e.groupby(["user_id", seg, "cat"], observed=True).size().unstack(fill_value=0).reindex(columns=range(K), fill_value=0)
base = cnt.xs("A_base", level=1)
for sname in ("B", "C"):
    later = cnt.xs(sname, level=1)
    common = base.index[(base.sum(axis=1) >= 100)].intersection(later.index[later.sum(axis=1) >= 100])
    drop_table(base.loc[common].values, later.loc[common].values, K, f"segment {sname} (days {'27-36' if sname=='B' else '53-62'})")

# ---------------- (c) KuaiRand-Pure ----------------
print("\n== (c) KuaiRand-Pure standard (non-random) logs")
D = "/home/user/data/kuairand/KuaiRand-Pure/KuaiRand-Pure/data/"
cols = ["user_id", "video_id", "date", "time_ms", "is_rand"]
r = pd.concat([pd.read_csv(D + f, usecols=cols) for f in
               ["log_standard_4_08_to_4_21_pure.csv", "log_standard_4_22_to_5_08_pure.csv"]])
r = r[r.is_rand == 0].drop_duplicates(["user_id", "video_id", "time_ms"])
vf = pd.read_csv(D + "video_features_basic_pure.csv", usecols=["video_id", "tag"])
vf["tag1"] = pd.to_numeric(vf.tag.astype(str).str.split(",").str[0], errors="coerce")
r = r.merge(vf[["video_id", "tag1"]], on="video_id", how="left").dropna(subset=["tag1"])
tags = np.sort(r.tag1.unique()); KR = len(tags)
r["k"] = np.searchsorted(tags, r.tag1)
r = r.sort_values(["user_id", "time_ms"])
print(f"   rows {len(r)}, users {r.user_id.nunique()}, distinct first-tags {KR}")
udn = r.groupby(["user_id", "date"]).size()
print(f"   exposures per user-day: median {udn.median():.0f}, p90 {udn.quantile(.9):.0f}; share user-days n>=20: {(udn>=20).mean():.3f}")
# static agreement: per user in 04-08..04-21, first 20 exposures vs all exposures
p1 = r[r.date <= 20220421]
n_u = p1.groupby("user_id").size()
keep = n_u[n_u >= 60].index
p1 = p1[p1.user_id.isin(keep)]
first20 = p1.groupby("user_id").head(20)
D20 = first20.groupby("user_id").k.nunique()
S20 = first20.groupby("user_id").k.agg(lambda s: s.value_counts().iloc[0] / len(s))
Hall = p1.groupby("user_id").k.apply(lambda s: norm_entropy(np.bincount(s, minlength=KR), KR))
print(f"   users with >=60 exposures in 04-08..04-21: {len(keep)}; Spearman D20~H_all {spearmanr(D20, Hall[D20.index])[0]:.3f}, "
      f"S20~H_all {spearmanr(S20, Hall[S20.index])[0]:.3f}")
# week 0 (04-08..04-14) baseline vs later (04-15..05-08) pooled
r["late"] = r.date >= 20220415
c = r.groupby(["user_id", "late", "k"]).size().unstack(fill_value=0).reindex(columns=range(KR), fill_value=0)
b, l = c.xs(False, level=1), c.xs(True, level=1)
common = b.index[b.sum(axis=1) >= 50].intersection(l.index[l.sum(axis=1) >= 50])
drop_table(b.loc[common].values, l.loc[common].values, KR, "KuaiRand later (04-15..05-08) vs week0")
