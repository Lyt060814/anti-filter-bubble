"""Reproduce resource-feasibility counts; no stance labels or causal estimates.

python3 analysis/context_audit/probe_resources.py /absolute/resource/root
Large inputs and generated samples stay outside Git, under resource_root/data/audit.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


PATTERNS = {
    "marriage_broad": "彩礼|结婚|婚姻|婚恋|夫妻|婆媳|离婚",
    "parenting_broad": "鸡娃|育儿|教育|早教|孩子|严管|快乐教育",
    "health_broad": "养生|食疗|中医|偏方|减肥|糖尿病|辟谣",
    "bride_price": "彩礼",
    "parenting_control": "鸡娃|快乐教育|严管|棍棒|打骂孩子",
    "diabetes": "糖尿病|降血糖",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("resource_root", type=Path)
    args = parser.parse_args()
    base = args.resource_root / "data"
    out = base / "audit"
    out.mkdir(exist_ok=True)
    paths = sorted((base / "KuaiRand-1K/data").glob("log_*.csv"))
    parts = []
    for p in paths:
        part = pd.read_csv(p, usecols=["user_id", "video_id", "time_ms", "is_hate", "is_follow", "tab"],
                           dtype={"user_id": "int32", "video_id": "int32", "is_hate": "uint8", "is_follow": "uint8", "tab": "uint8"})
        part["random"] = "random" in p.name
        parts.append(part)
    logs = pd.concat(parts, ignore_index=True)
    del parts
    size = int(logs.video_id.max()) + 1
    used = np.zeros(size, dtype=bool)
    used[logs.video_id.to_numpy()] = True
    title_present = np.zeros(size, dtype=bool)
    caption_present = np.zeros(size, dtype=bool)
    caption_matched = np.zeros(size, dtype=bool)
    keyword = np.zeros(size, dtype=np.uint8)
    samples = []
    seen = {name: 0 for name in PATTERNS}
    caption_path = base / "kuairand_video_captions.csv"
    for chunk in pd.read_csv(caption_path, chunksize=200000):
        chunk = chunk[chunk.final_video_id.lt(size)]
        chunk = chunk[used[chunk.final_video_id.to_numpy()]]
        ids = chunk.final_video_id.to_numpy()
        caption_matched[ids] = True
        caption = chunk.caption.fillna("").str.strip()
        cover = chunk.show_cover_text.fillna("").str.strip()
        text = caption + " " + cover
        caption_present[ids] = caption.ne("")
        title_present[ids] = caption.ne("") | cover.ne("")
        for i, (name, pattern) in enumerate(PATTERNS.items()):
            hit = text.str.contains(pattern, regex=True).to_numpy()
            keyword[ids[hit]] |= 1 << i
            sample = chunk[hit].head(max(0, 12 - seen[name]))
            for row in sample.itertuples():
                samples.append({"query": name, "video_id": row.final_video_id,
                                "caption": str(row.caption), "cover": str(row.show_cover_text)})
                seen[name] += 1
    print("captions scanned", flush=True)
    category = np.full(size, -999, dtype=np.int16)
    category_matched = np.zeros(size, dtype=bool)
    for chunk in pd.read_csv(base / "kuairand_video_categories.csv", chunksize=200000,
                             usecols=["final_video_id", "first_level_category_id"]):
        chunk = chunk[chunk.final_video_id.lt(size)]
        ids = chunk.final_video_id.to_numpy()
        category_matched[ids] = True
        category[ids] = chunk.first_level_category_id.fillna(-999).to_numpy(dtype=np.int16)
    mapping = pd.read_csv(Path(__file__).resolve().parents[1] / "data_check/category_map_l1.csv")
    mapped_categories = mapping.loc[mapping.h_kuairand.notna(), "l1_id"].astype(int).to_numpy()
    category_valid = np.isin(category, mapped_categories)
    result = {"patterns": PATTERNS, "window": "non-overlapping 200 standard exposures per user, chronological; discard incomplete windows", "keyword_warning": "candidate counts only, not same-target stance-valid counts", "raw_rows": len(logs), "unique_videos": int(used.sum()),
              "unique_video_caption_join": int((caption_matched & used).sum()),
              "unique_video_nonempty_caption": int((caption_present & used).sum()),
              "unique_video_caption_or_cover": int((title_present & used).sum()),
              "unique_video_category_join": int((category_matched & used).sum())}
    for name, mask in [("all", np.ones(len(logs), dtype=bool)), ("standard", ~logs.random), ("random", logs.random)]:
        frame = logs[mask]
        valid = category_valid[frame.video_id.to_numpy()]
        result[name] = {"rows": len(frame), "hate": int(frame.is_hate.sum()), "follow": int(frame.is_follow.sum()),
                        "mapped_rows": int(valid.sum()), "mapped_hate": int(frame.loc[valid, "is_hate"].sum()), "mapped_follow": int(frame.loc[valid, "is_follow"].sum()),
                        "caption_exposures": int(caption_present[frame.video_id.to_numpy()].sum())}
    std = logs[~logs.random].sort_values(["user_id", "time_ms", "video_id"]).copy()
    del logs
    std["window"] = std.groupby("user_id").cumcount() // 200
    groups = std.groupby(["user_id", "window"])
    n = groups.size()
    complete = n.eq(200)
    result["full_windows"] = int(complete.sum())
    result["keyword_candidates"] = {}
    for i, name in enumerate(PATTERNS):
        std["hit"] = (keyword[std.video_id.to_numpy()] & (1 << i)) != 0
        counts = std.groupby(["user_id", "window"]).hit.sum()[complete]
        enough = counts.ge(20)
        result["keyword_candidates"][name] = {
            "unique_videos": int(((keyword & (1 << i)) != 0).sum()),
            "standard_exposures": int(std.hit.sum()),
            "windows_with_any": int(counts.gt(0).sum()),
            "windows_at_least_20": int(enough.sum()),
            "users_with_window_at_least_20": int(counts[enough].index.get_level_values(0).nunique()),
            "max_candidates_in_full_window": int(counts.max()),
        }
    (out / "kuairand_metadata_probe.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
    (out / "keyword_examples.json").write_text(json.dumps(samples, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
