"""Feasibility probe for RecIF (OpenOneRec): captions, issue prevalence, exposure and not-interested events.

Usage: python -I recif_probe.py RECIF_DIR OUT_JSON
Reads parquet files row group by row group to keep memory bounded.
Counts are keyword-based candidate counts, not relevance or stance labels.
"""
import collections
import json
import random
import sys

import numpy as np
import pyarrow.compute as pc
import pyarrow.parquet as pq

GROUPS = {
    "bride_price": ["彩礼"],
    "marriage_gender": ["离婚", "婆媳", "婆婆", "女方", "男方", "家暴", "出轨", "AA制"],
    "discipline": ["打孩子", "管教", "棍棒", "严厉", "正面管教", "惩罚孩子", "骂孩子"],
    "childbearing": ["生孩子", "丁克", "二胎", "三胎", "催生", "生育"],
    "marriage_pressure": ["催婚", "不结婚", "剩女", "大龄单身"],
    "career_choice": ["考公", "公务员", "铁饭碗", "躺平", "读书无用"],
    "education_anxiety": ["鸡娃", "补习", "内卷", "起跑线", "双减", "辅导作业"],
}


def captions(recif_dir, out):
    f = pq.ParquetFile(f"{recif_dir}/pid2caption.parquet")
    print("pid2caption schema:", f.schema_arrow, "rows:", f.metadata.num_rows, flush=True)
    matched = {g: set() for g in GROUPS}
    lengths, samples, rng = [], [], random.Random(0)
    for rg in range(f.num_row_groups):
        t = f.read_row_group(rg, columns=["pid", "dense_caption"])
        pids = t.column("pid").to_numpy()
        caps = t.column("dense_caption")
        lengths.extend(pc.utf8_length(caps).to_numpy(zero_copy_only=False).tolist()[:2000])
        for g, kws in GROUPS.items():
            mask = None
            for k in kws:
                m = pc.match_substring(caps, k)
                mask = m if mask is None else pc.or_(mask, m)
            idx = np.flatnonzero(pc.fill_null(mask, False).to_numpy(zero_copy_only=False))
            matched[g].update(pids[idx].tolist())
            if g in ("bride_price", "marriage_gender", "discipline") and len(idx):
                for i in rng.sample(list(idx), min(2, len(idx))):
                    if len(samples) < 40:
                        samples.append((g, int(pids[i]), caps[i].as_py()[:300]))
    out["captions"] = {
        "rows": f.metadata.num_rows,
        "length_sample_quantiles": dict(zip(["p10", "p50", "p90"], np.percentile(lengths, [10, 50, 90]).tolist())),
        "issue_candidates": {g: len(s) for g, s in matched.items()},
        "samples": samples,
    }
    return matched


def histories(recif_dir, matched, out):
    f = pq.ParquetFile(f"{recif_dir}/onerec_bench_release.parquet")
    cols = ["uid", "hist_video_pid", "hist_video_not_interested", "target_video_pid", "target_video_not_interested"]
    print("bench schema:", f.schema_arrow, "rows:", f.metadata.num_rows, flush=True)
    issue_of = collections.defaultdict(set)
    for g, s in matched.items():
        for p in s:
            issue_of[p].add(g)
    stats = collections.Counter()
    hist_len = []
    per_issue = {g: collections.Counter() for g in GROUPS}
    window_after = {g: [] for g in GROUPS}
    for rg in range(f.num_row_groups):
        t = f.read_row_group(rg, columns=cols).to_pylist()
        for row in t:
            hp = row["hist_video_pid"] or []
            hn = row["hist_video_not_interested"] or []
            tp = row["target_video_pid"] or []
            tn = row["target_video_not_interested"] or []
            seq = list(hp) + list(tp)
            ni = list(hn) + list(tn)
            if len(ni) != len(seq):
                stats["length_mismatch_users"] += 1
                continue
            stats["users"] += 1
            hist_len.append(len(seq))
            stats["impressions"] += len(seq)
            stats["ni_flags"] += sum(ni)
            seen_issue = set()
            for i, (p, flag) in enumerate(zip(seq, ni)):
                for g in issue_of.get(p, ()):
                    per_issue[g]["exposures"] += 1
                    seen_issue.add(g)
                    if flag:
                        per_issue[g]["ni_events"] += 1
                        after = sum(1 for q in seq[i + 1:] if g in issue_of.get(q, ()))
                        before = sum(1 for q in seq[:i] if g in issue_of.get(q, ()))
                        window_after[g].append((before, after))
            for g in seen_issue:
                per_issue[g]["users_exposed"] += 1
    out["histories"] = {
        "users": stats["users"],
        "length_mismatch_users": stats["length_mismatch_users"],
        "impressions": stats["impressions"],
        "ni_rate": stats["ni_flags"] / max(stats["impressions"], 1),
        "seq_len_quantiles": dict(zip(["p10", "p50", "p90", "max"], np.percentile(hist_len, [10, 50, 90, 100]).tolist())),
        "per_issue": {g: dict(c) for g, c in per_issue.items()},
        "ni_events_with_issue_exposure_before_and_after": {
            g: {
                "events": len(w),
                "with_>=3_before_and_>=3_after": sum(1 for b, a in w if b >= 3 and a >= 3),
                "median_after": float(np.median([a for _, a in w])) if w else None,
            }
            for g, w in window_after.items()
        },
    }


def main():
    recif_dir, out_path = sys.argv[1], sys.argv[2]
    out = {}
    matched = captions(recif_dir, out)
    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=2)
    histories(recif_dir, matched, out)
    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=2)
    print(json.dumps({k: v for k, v in out.items()}, ensure_ascii=False, indent=2)[:6000])


if __name__ == "__main__":
    main()
