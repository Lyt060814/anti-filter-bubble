"""Why can a recommender learned from logs treat "not interested" as interest? A selection check.

Usage: python -I ni_confounding_check.py RECIF_DIR CACHE_NPZ
Users are split by interest measured in the first half of their history (long-view rate on issue items).
In the second half we compare, between interested (Z=1) and other users (Z=0):
  e = share of impressions that are issue items (how strongly the logging policy targets the topic)
  d = not-interested rate on shown issue items (how much more the uninterested dislike it)
An observed NI on an issue item raises the odds of Z=1 by (e1*d1)/(e0*d0); if e1/e0 > d0/d1, a model
fitted to logs learns that NI on topic k predicts more topic-k exposure.
"""
import sys

import numpy as np
import pyarrow.parquet as pq

recif_dir, cache = sys.argv[1], sys.argv[2]
z = np.load(cache)
pid_sorted, pid_issue = z["pid"], z["pid_issue"]
cols = ["hist_video_pid", "hist_video_longview", "hist_video_not_interested", "target_video_pid", "target_video_longview", "target_video_not_interested"]
f = pq.ParquetFile(f"{recif_dir}/onerec_bench_release.parquet")
rows = []
for rg in range(f.num_row_groups):
    t = f.read_row_group(rg, columns=cols).to_pylist()
    for r in t:
        seq = np.array((r["hist_video_pid"] or []) + (r["target_video_pid"] or []), dtype=np.int64)
        lv = np.array((r["hist_video_longview"] or []) + (r["target_video_longview"] or []))
        ni = np.array((r["hist_video_not_interested"] or []) + (r["target_video_not_interested"] or []))
        if len(seq) < 100 or not (len(seq) == len(lv) == len(ni)):
            continue
        idx = np.clip(np.searchsorted(pid_sorted, seq), 0, len(pid_sorted) - 1)
        iss = (pid_sorted[idx] == seq) & pid_issue[idx]
        h = len(seq) // 2
        a, b = slice(0, h), slice(h, None)
        if iss[a].sum() < 3:
            continue
        rows.append((lv[a][iss[a]].mean(), iss[b].mean(), iss[b].sum(), (ni[b] * iss[b]).sum(), len(seq) - h))
R = np.array(rows)
med = np.median(R[:, 0])
for name, cut in (("median split", med), ("top quartile vs rest", np.quantile(R[:, 0], 0.75))):
    z1 = R[:, 0] > cut
    e1, e0 = R[z1, 2].sum() / R[z1, 4].sum(), R[~z1, 2].sum() / R[~z1, 4].sum()
    d1, d0 = R[z1, 3].sum() / R[z1, 2].sum(), R[~z1, 3].sum() / R[~z1, 2].sum()
    print(f"{name}: users Z=1 {int(z1.sum())}, Z=0 {int((~z1).sum())}")
    print(f"  issue exposure share e1={e1:.4f} e0={e0:.4f}  ratio e1/e0={e1/e0:.3f}")
    print(f"  NI rate on issue items d1={d1:.5f} d0={d0:.5f}  ratio d0/d1={d0/max(d1,1e-9):.3f}  (NI events Z=1 {int(R[z1,3].sum())}, Z=0 {int(R[~z1,3].sum())})")
    print(f"  likelihood ratio of an NI for Z=1: {(e1*d1)/(e0*d0):.3f}")
