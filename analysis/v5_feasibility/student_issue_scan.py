"""Keyword scan of university-student issues in RecIF (candidates, not labels). Vectorised for speed.

Usage: python -I student_issue_scan.py RECIF_DIR OUT_JSON
"""
import json
import sys

import numpy as np
import pyarrow.compute as pc
import pyarrow.parquet as pq

ISSUES = {
    "kaoyan": ["考研", "读研", "保研", "研究生"],
    "civil_service": ["考公", "考编", "公务员", "事业编", "铁饭碗", "体制内"],
    "study_abroad": ["留学", "雅思", "托福", "出国读"],
    "job_internship": ["实习", "秋招", "春招", "校招", "找工作", "简历"],
    "grades": ["绩点", "GPA", "挂科", "奖学金", "期末考"],
    "lying_flat": ["躺平", "内卷", "摆烂", "卷王"],
    "consumption": ["超前消费", "花呗", "消费主义", "极简", "月光族", "存钱"],
    "employment_anxiety": ["35岁", "裁员", "就业难", "失业"],
    "college_life": ["大学生", "宿舍", "毕业"],
}


def main():
    recif_dir, out_path = sys.argv[1:3]
    f = pq.ParquetFile(f"{recif_dir}/pid2caption.parquet")
    pids_by = {k: [] for k in ISSUES}
    for rg in range(f.num_row_groups):
        t = f.read_row_group(rg, columns=["pid", "dense_caption"])
        caps, pids = t.column("dense_caption"), t.column("pid").to_numpy()
        for k, kws in ISSUES.items():
            m = None
            for w in kws:
                x = pc.match_substring(caps, w)
                m = x if m is None else pc.or_(m, x)
            pids_by[k].append(pids[np.asarray(pc.fill_null(m, False).to_numpy(zero_copy_only=False))])
    item_sets = {k: np.unique(np.concatenate(v)) for k, v in pids_by.items()}
    union = np.unique(np.concatenate(list(item_sets.values())))
    out = {k: {"items": int(len(v)), "exposures": 0, "users": 0} for k, v in item_sets.items()}
    out["any_student_issue"] = {"items": int(len(union)), "exposures": 0, "users": 0}
    total = 0
    fb = pq.ParquetFile(f"{recif_dir}/onerec_bench_release.parquet")
    for rg in range(fb.num_row_groups):
        t = fb.read_row_group(rg, columns=["hist_video_pid"])
        col = t.column("hist_video_pid").combine_chunks()
        flat = pc.list_flatten(col).to_numpy()
        owner = pc.list_parent_indices(col).to_numpy()
        total += len(flat)
        for k, s in list(item_sets.items()) + [("any_student_issue", union)]:
            hit = np.isin(flat, s)
            out[k]["exposures"] += int(hit.sum())
            out[k]["users"] += int(len(np.unique(owner[hit])))
    for v in out.values():
        v["share_of_exposures"] = v["exposures"] / total
    out["_total_exposures_hist"] = total
    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
