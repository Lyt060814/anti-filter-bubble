"""Prepare bounded inputs for execution_plan_v2; no stance labels or effect estimates.

Usage: python3 analysis/context_audit/plan_v2_preflight.py /absolute/resource/root
Raw candidate texts and anonymous event IDs remain outside Git. The small summary
is written to docs/context-recovery/plan_v2_preflight.json.
"""
import argparse
import hashlib
import json
import resource
import time
from pathlib import Path

import numpy as np
import pandas as pd


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("resource_root", type=Path)
    root = parser.parse_args().resource_root.resolve()
    start = time.perf_counter()
    data = root / "data"
    out = data / "audit/plan_v2"
    out.mkdir(parents=True, exist_ok=True)
    basic = pd.read_csv(data / "KuaiRand-1K/data/video_features_basic_1k.csv",
                        usecols=["video_id", "author_id"])
    assert basic.video_id.is_unique
    size = int(basic.video_id.max()) + 1
    used = np.zeros(size, dtype=bool)
    used[basic.video_id.to_numpy()] = True
    author = np.full(size, -1, dtype=np.int32)
    author[basic.video_id.to_numpy()] = basic.author_id.fillna(-1).to_numpy(dtype=np.int32)
    parts = []
    raw_rows = 0
    for p in sorted((data / "KuaiRand-1K/data").glob("log_standard*.csv")):
        frame = pd.read_csv(p, usecols=["user_id", "video_id", "time_ms", "is_hate", "tab"],
                            dtype={"user_id": "int32", "video_id": "int32", "is_hate": "uint8", "tab": "uint8"})
        raw_rows += len(frame)
        parts.append(frame[frame.tab.eq(1)].copy())
    logs = pd.concat(parts, ignore_index=True)
    del frame, parts
    logs = logs.sort_values(["user_id", "time_ms", "video_id"], kind="stable")
    logs["author_id"] = author[logs.video_id.to_numpy()]
    assert logs.author_id.ge(0).all()
    full_events = 0
    full_users = 0
    isolated_events = 0
    selected = []
    for uid, group in logs.groupby("user_id", sort=True):
        flags = group.is_hate.to_numpy()
        events = np.flatnonzero(flags)
        full = events[(events >= 200) & (events + 100 < len(group))]
        full_events += len(full)
        full_users += bool(len(full))
        prefix = np.r_[0, np.cumsum(flags)]
        previous_selected = -301
        count = 0
        for i in full:
            nearby = int(prefix[i + 101] - prefix[i - 100] - 1)
            isolated_events += nearby == 0
            if count == 5 or i - previous_selected <= 300:
                continue
            row = group.iloc[i]
            selected.append({"user_id": int(uid), "position_in_tab1": int(i),
                "video_id": int(row.video_id), "author_id": int(row.author_id),
                "time_ms": int(row.time_ms), "other_hate_within_100": nearby,
                "pre200_elapsed_hours": float((row.time_ms - group.iloc[i - 200].time_ms) / 3600000),
                "post100_elapsed_hours": float((group.iloc[i + 100].time_ms - row.time_ms) / 3600000)})
            previous_selected = i
            count += 1
    chosen = pd.DataFrame(selected)
    event_path = out / "event_anchors.csv"
    chosen.to_csv(event_path, index=False)
    summary = {"scope": "Input feasibility only; no manual labels, model accuracy or button effect estimated.",
        "resource_root": str(root), "seed": 1110,
        "events": {"standard_rows": raw_rows, "tab1_rows": len(logs),
            "tab1_users": int(logs.user_id.nunique()), "tab1_hate": int(logs.is_hate.sum()),
            "author_join_coverage": float(logs.author_id.ge(0).mean()),
            "pre200_post100_complete_events": int(full_events),
            "users_with_complete_events": int(full_users),
            "complete_events_without_other_hate_within_100": int(isolated_events),
            "selection": "Per user, chronological first up to 5 complete events, positions >300 apart; other hate is flagged, not excluded.",
            "selected_events": len(chosen), "selected_users": int(chosen.user_id.nunique()),
            "selected_without_other_hate_within_100": int(chosen.other_hate_within_100.eq(0).sum()),
            "pre200_elapsed_hours_quantiles": chosen.pre200_elapsed_hours.quantile([0.5, 0.9, 1]).to_dict(),
            "post100_elapsed_hours_quantiles": chosen.post100_elapsed_hours.quantile([0.5, 0.9, 1]).to_dict(),
            "file": str(event_path.relative_to(root)), "sha256": digest(event_path)}}
    del logs, basic, author
    print("Event input bounds checked", flush=True)
    candidate_parts = []
    for chunk in pd.read_csv(data / "kuairand_video_captions.csv", chunksize=200000,
                             usecols=["final_video_id", "caption", "show_cover_text"]):
        chunk = chunk[chunk.final_video_id.lt(size)]
        chunk = chunk[used[chunk.final_video_id.to_numpy()]]
        text = chunk.caption.fillna("") + " " + chunk.show_cover_text.fillna("")
        candidate_parts.append(chunk[text.str.contains("彩礼", regex=False)])
    pool = pd.concat(candidate_parts, ignore_index=True).sort_values("final_video_id")
    assert pool.final_video_id.is_unique and len(pool) >= 200
    pool_path = out / "bride_price_candidates.csv"
    pool.to_csv(pool_path, index=False)
    selected_indices = np.random.default_rng(1110).permutation(len(pool))[:200]
    sample = pool.iloc[selected_indices].copy()
    sample.insert(0, "sample_order", np.arange(1, 201))
    sample.insert(1, "phase", ["pilot"] * 40 + ["audit"] * 160)
    sample_path = out / "annotation_sample_200.csv"
    sample.to_csv(sample_path, index=False)
    summary["content"] = {"query": "literal 彩礼 in caption or show_cover_text",
        "population": "Unique videos in the KuaiRand-1K basic feature table, including logged random-pool videos",
        "candidate_videos": len(pool), "sample_videos": len(sample), "pilot_videos": 40,
        "audit_videos": 160, "selection": "Uniform sample without replacement over sorted candidate IDs; seed 1110; no stance or popularity filtering",
        "pool_file": str(pool_path.relative_to(root)), "pool_sha256": digest(pool_path),
        "sample_file": str(sample_path.relative_to(root)), "sample_sha256": digest(sample_path),
        "annotated": False}
    summary["runtime_seconds"] = round(time.perf_counter() - start, 2)
    summary["peak_rss_mib_linux"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 1)
    target = Path(__file__).resolve().parents[2] / "docs/context-recovery/plan_v2_preflight.json"
    target.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
