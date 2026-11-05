"""RecIF feasibility statistics for the v5 simulation plan.

Usage: python -I recif_user_item_stats.py RECIF_DIR OUT_JSON

Answers, for keyword-defined issue candidates (not labels):
  1. How many issue exposures does each user have (detection and user-level estimation)?
  2. How many exposures and engaged users does each issue item have (ID-based models, co-engagement)?
  3. Long-view, like and not-interested rates on issue items, and on a crude framing-cue proxy.
  4. A pilot overdispersion test: do users differ in the proxy share of their issue exposures more
     than a label permutation (same per-user counts) would produce? Also the same test for topic share.
The framing proxy is a keyword cue in generated captions; it is only a feasibility signal.
"""
import collections
import json
import sys

import numpy as np
import pyarrow.compute as pc
import pyarrow.parquet as pq

ISSUE = ["离婚", "婆媳", "婆婆", "女方", "男方", "家暴", "出轨", "AA制", "彩礼", "结婚", "婚姻", "相亲", "夫妻", "老公", "老婆"]
PROXY_A = ["捞女", "凤凰男", "扶弟魔", "妈宝男", "普信男", "女拳", "田园女权", "女人都", "男人都", "女的都", "男的都",
           "现在的女人", "现在的男人", "现在的女孩", "女人就是", "男人就是", "物质女", "拜金"]


def mask_any(caps, kws):
    m = None
    for k in kws:
        x = pc.match_substring(caps, k)
        m = x if m is None else pc.or_(m, x)
    return np.asarray(pc.fill_null(m, False).to_numpy(zero_copy_only=False))


def load_items(recif_dir):
    f = pq.ParquetFile(f"{recif_dir}/pid2caption.parquet")
    issue, proxy = set(), set()
    for rg in range(f.num_row_groups):
        t = f.read_row_group(rg, columns=["pid", "dense_caption"])
        pids = t.column("pid").to_numpy()
        caps = t.column("dense_caption")
        mi = mask_any(caps, ISSUE)
        ma = mask_any(caps, PROXY_A) & mi
        issue.update(pids[mi].tolist())
        proxy.update(pids[ma].tolist())
    return issue, proxy


def beta_binomial_rho(k, n):
    """Method-of-moments intra-class correlation for counts k out of n (Kleinman 1973 style)."""
    k = np.asarray(k, float); n = np.asarray(n, float)
    p = k.sum() / n.sum()
    if p <= 0 or p >= 1:
        return float("nan")
    s = np.sum((k - n * p) ** 2 / (n * p * (1 - p)))
    df = len(n) - 1
    n_bar = n.sum()
    denom = np.sum(n * (n - 1)) / n_bar
    return float((s / df - 1) / (denom - 1)) if denom > 1 else float("nan")


def main():
    recif_dir, out_path = sys.argv[1], sys.argv[2]
    rng = np.random.default_rng(0)
    issue, proxy = load_items(recif_dir)
    print("issue candidates", len(issue), "proxy", len(proxy), flush=True)
    cols = ["uid", "hist_video_pid", "hist_video_longview", "hist_video_like", "hist_video_not_interested",
            "target_video_pid", "target_video_longview", "target_video_like", "target_video_not_interested"]
    f = pq.ParquetFile(f"{recif_dir}/onerec_bench_release.parquet")
    item_exp = collections.Counter(); item_lv = collections.Counter(); item_like = collections.Counter()
    user_rows = []  # (n_total, n_issue, n_proxy)
    resp = {g: collections.Counter() for g in ["all", "issue", "proxy", "issue_nonproxy"]}
    all_exp = collections.Counter()
    for rg in range(f.num_row_groups):
        for row in f.read_row_group(rg, columns=cols).to_pylist():
            seq = (row["hist_video_pid"] or []) + (row["target_video_pid"] or [])
            lv = (row["hist_video_longview"] or []) + (row["target_video_longview"] or [])
            lk = (row["hist_video_like"] or []) + (row["target_video_like"] or [])
            ni = (row["hist_video_not_interested"] or []) + (row["target_video_not_interested"] or [])
            if not (len(seq) == len(lv) == len(lk) == len(ni)) or not seq:
                continue
            n_i = n_a = 0
            for p, a, b, c in zip(seq, lv, lk, ni):
                all_exp[p] += 1
                groups = ["all"]
                if p in issue:
                    n_i += 1; groups.append("issue")
                    item_exp[p] += 1; item_lv[p] += a; item_like[p] += b
                    if p in proxy:
                        n_a += 1; groups.append("proxy")
                    else:
                        groups.append("issue_nonproxy")
                for g in groups:
                    r = resp[g]; r["n"] += 1; r["longview"] += a; r["like"] += b; r["ni"] += c
            user_rows.append((len(seq), n_i, n_a))
    U = np.array(user_rows)
    n_tot, n_iss, n_prx = U[:, 0], U[:, 1], U[:, 2]
    q = lambda x, ps=(10, 25, 50, 75, 90, 99): {f"p{p}": float(np.percentile(x, p)) for p in ps}
    out = {"issue_candidates": len(issue), "proxy_candidates": len(proxy), "users": int(len(U))}
    out["user_issue_exposures"] = {"quantiles": q(n_iss), **{f">={k}": int((n_iss >= k).sum()) for k in (1, 5, 10, 20, 50, 100)}}
    out["user_issue_share_quantiles"] = q(n_iss / n_tot)
    ie = np.array(list(item_exp.values())); il = np.array([item_lv[p] for p in item_exp]); ik = np.array([item_like[p] for p in item_exp])
    out["issue_item_exposures"] = {"items_seen": int(len(ie)), "quantiles": q(ie), **{f">={k}": int((ie >= k).sum()) for k in (5, 10, 20, 50, 100, 500)}}
    out["issue_item_longviews>="] = {str(k): int((il >= k).sum()) for k in (5, 10, 20, 50)}
    out["issue_item_likes>="] = {str(k): int((ik >= k).sum()) for k in (1, 5, 10, 20)}
    allc = np.array(list(all_exp.values()))
    out["all_items"] = {"items_seen": int(len(allc)), **{f">={k}": int((allc >= k).sum()) for k in (5, 10, 20, 50)}}
    out["response_rates"] = {g: {"n": r["n"], **{k: r[k] / max(r["n"], 1) for k in ("longview", "like", "ni")}} for g, r in resp.items()}
    # Overdispersion pilot (users with >=10 issue exposures): proxy share within issue, and issue share overall.
    sel = n_iss >= 10
    k, n = n_prx[sel], n_iss[sel]
    rho_obs = beta_binomial_rho(k, n)
    p0 = k.sum() / n.sum()
    rho_null = [beta_binomial_rho(rng.binomial(n, p0), n) for _ in range(200)]
    # Permutation null that keeps the item mix: reshuffle which issue exposures are proxy across users.
    labels = np.concatenate([np.r_[np.ones(a), np.zeros(b - a)] for a, b in zip(k, n)])
    cuts = np.cumsum(n)[:-1]
    rho_perm = []
    for _ in range(200):
        rng.shuffle(labels)
        rho_perm.append(beta_binomial_rho([s.sum() for s in np.split(labels, cuts)], n))
    sel2 = n_tot >= 50
    rho_topic = beta_binomial_rho(n_iss[sel2], n_tot[sel2])
    p1 = n_iss[sel2].sum() / n_tot[sel2].sum()
    rho_topic_null = [beta_binomial_rho(rng.binomial(n_tot[sel2], p1), n_tot[sel2]) for _ in range(100)]
    out["overdispersion_pilot"] = {
        "proxy_within_issue": {"users": int(sel.sum()), "pooled_share": float(p0), "rho": rho_obs,
                                "binomial_null_p95": float(np.percentile(rho_null, 95)),
                                "permutation_null_p95": float(np.percentile(rho_perm, 95))},
        "issue_share_overall": {"users": int(sel2.sum()), "pooled_share": float(p1), "rho": rho_topic,
                                 "binomial_null_p95": float(np.percentile(rho_topic_null, 95))},
    }
    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
