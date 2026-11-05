"""Check what the OneRec video-rec history contains: all impressions, or only long-viewed ones?

Usage: python -I video_history_check.py RECIF_DIR [N_USERS]
Compares benchmark video_test hist_pid with the raw per-user sequence and its long-view flags.
"""
import json
import sys

import numpy as np
import pyarrow.parquet as pq

recif_dir = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 200
vt = pq.read_table(f"{recif_dir}/benchmark_data/video/video_test.parquet", columns=["hist_pid", "metadata"]).to_pylist()[:n]
want = {json.loads(r["metadata"])["uid"]: r["hist_pid"] for r in vt}
cols = ["uid", "hist_video_pid", "hist_video_longview", "target_video_pid"]
f = pq.ParquetFile(f"{recif_dir}/onerec_bench_release.parquet")
stats = []
for rg in range(f.num_row_groups):
    for r in f.read_row_group(rg, columns=cols).to_pylist():
        if r["uid"] not in want:
            continue
        h = want[r["uid"]]
        seq, lv = r["hist_video_pid"] or [], r["hist_video_longview"] or []
        lv_seq = [p for p, x in zip(seq, lv) if x]
        stats.append({
            "bench_len": len(h), "raw_len": len(seq), "raw_lv_len": len(lv_seq),
            "suffix_of_raw": seq[-len(h):] == h if h else None,
            "suffix_of_lv": lv_seq[-len(h):] == h if h else None,
            "share_in_lv": float(np.mean([p in set(lv_seq) for p in h])) if h else None,
        })
print(len(stats), "users matched")
for k in ("suffix_of_raw", "suffix_of_lv"):
    print(k, float(np.mean([s[k] for s in stats if s[k] is not None])))
print("share of bench history items that were long-viewed:", float(np.mean([s["share_in_lv"] for s in stats])))
print("median lengths bench/raw/raw_lv:", np.median([s["bench_len"] for s in stats]), np.median([s["raw_len"] for s in stats]), np.median([s["raw_lv_len"] for s in stats]))
