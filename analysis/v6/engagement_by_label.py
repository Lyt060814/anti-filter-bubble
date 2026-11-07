"""L5: engagement rates in RecIF logs by DeepSeek label (Section 4.4).

Usage: python -I engagement_by_label.py RECIF_DIR ENRICH_CSV BOTTOMUP_CSV OUT_PREFIX
For each video in the label files, counts impressions, long views, likes and "not interested" over all
users' histories and targets. Rates are pooled over impressions; 95% intervals come from a bootstrap over
videos (2,000 resamples), because impressions of the same video are not independent.
Outputs OUT_PREFIX.json (rates and intervals) and OUT_PREFIX_items.csv (pid, group, counts).
"""
import csv
import json
import sys
from collections import defaultdict

import numpy as np
import pyarrow.compute as pc
import pyarrow.parquet as pq

recif_dir, enrich_csv, bu_csv, prefix = sys.argv[1:5]
groups = {}
for r in csv.DictReader(open(enrich_csv, encoding="utf-8")):
    if r["issue"] == "是" and r["group_label"]:
        g = "group_label" if r["group_label"] in ("针对女性", "针对男性") else ("other_issue" if r["group_label"] == "无" else None)
        if g:
            groups[int(r["pid"])] = ("marriage_" + g, r["stratum"])
for r in csv.DictReader(open(bu_csv, encoding="utf-8")):
    if r["domain"] and r["domain"] != "非议题内容":
        p = int(r["pid"])
        groups.setdefault(p, ("issue_opposing" if r["opposing"] == "是" else "issue_not_opposing", "bottom_up"))
pids = np.array(sorted(groups), dtype=np.int64)
cnt = np.zeros((len(pids), 4), dtype=np.int64)
cols = [("hist_video_pid", "hist_video_longview", "hist_video_like", "hist_video_not_interested"),
        ("target_video_pid", "target_video_longview", "target_video_like", "target_video_not_interested")]
f = pq.ParquetFile(f"{recif_dir}/onerec_bench_release.parquet")
for rg in range(f.num_row_groups):
    t = f.read_row_group(rg, columns=[c for cs in cols for c in cs])
    for cs in cols:
        seq = pc.list_flatten(t.column(cs[0]).combine_chunks()).to_numpy()
        flags = [pc.list_flatten(t.column(c).combine_chunks()).to_numpy() for c in cs[1:]]
        if not all(len(x) == len(seq) for x in flags):
            continue
        idx = np.searchsorted(pids, seq)
        idx[idx >= len(pids)] = 0
        hit = pids[idx] == seq
        np.add.at(cnt[:, 0], idx[hit], 1)
        for k, fl in enumerate(flags, 1):
            np.add.at(cnt[:, k], idx[hit], fl[hit].astype(np.int64))
rng = np.random.default_rng(5)
by = defaultdict(list)
for i, p in enumerate(pids):
    by[groups[int(p)][0]].append(i)
out = {}
for g, ix in by.items():
    ix = np.array(ix)
    ix = ix[cnt[ix, 0] > 0]
    c = cnt[ix]
    res = {"videos": int(len(ix)), "impressions": int(c[:, 0].sum())}
    for k, name in enumerate(["long_view", "like", "not_interested"], 1):
        rate = c[:, k].sum() / max(c[:, 0].sum(), 1)
        boots = []
        for _ in range(2000):
            b = c[rng.integers(0, len(c), len(c))]
            boots.append(b[:, k].sum() / max(b[:, 0].sum(), 1))
        res[name] = {"rate": float(rate), "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]}
    out[g] = res
json.dump({"groups": out, "note": "pooled over impressions; bootstrap over videos; labels from DeepSeek V4 Pro (enrichment v0 prompt for marriage videos, cross-domain prompt for bottom-up)"},
          open(prefix + ".json", "w"), ensure_ascii=False, indent=2)
with open(prefix + "_items.csv", "w", newline="") as fo:
    w = csv.writer(fo)
    w.writerow(["pid", "group", "stratum", "impressions", "long_views", "likes", "not_interested"])
    for i, p in enumerate(pids):
        w.writerow([int(p), groups[int(p)][0], groups[int(p)][1]] + cnt[i].tolist())
print(json.dumps(out, ensure_ascii=False, indent=1))
