"""Keyword scan of candidate everyday issues in RecIF: items, exposures, users (candidates, not labels).

Usage: python -I issue_candidates_scan.py RECIF_DIR OUT_JSON
"""
import json
import sys
from collections import defaultdict

import numpy as np
import pyarrow.compute as pc
import pyarrow.parquet as pq

ISSUES = {
    "marriage_family": ["离婚", "婆媳", "婆婆", "女方", "男方", "家暴", "出轨", "AA制", "彩礼", "结婚", "婚姻", "相亲", "夫妻", "老公", "老婆"],
    "parenting_education": ["鸡娃", "补习", "辅导作业", "打孩子", "管教", "学区房", "高考", "中考", "家长群", "起跑线", "双减"],
    "work_career": ["躺平", "内卷", "996", "打工人", "裁员", "考公", "公务员", "铁饭碗", "加班", "失业", "35岁"],
    "body_appearance": ["减肥", "瘦身", "身材焦虑", "容貌焦虑", "整容", "医美", "颜值", "白幼瘦"],
    "health_wellness": ["养生", "致癌", "偏方", "保健品", "中医", "长寿", "排毒", "体检"],
    "money_housing": ["理财", "炒股", "基金", "买房", "房价", "房贷", "存款", "退休金"],
    "region": ["地域黑", "地域歧视", "河南人", "东北人", "上海人", "北京人", "广东人", "外地人"],
    "elderly_care": ["养老", "老人", "啃老", "赡养", "养儿防老", "退休"],
}


def main():
    recif_dir, out_path = sys.argv[1:3]
    f = pq.ParquetFile(f"{recif_dir}/pid2caption.parquet")
    sets = {k: [] for k in ISSUES}
    for rg in range(f.num_row_groups):
        t = f.read_row_group(rg, columns=["pid", "dense_caption"])
        caps, pids = t.column("dense_caption"), t.column("pid").to_numpy()
        for k, kws in ISSUES.items():
            m = None
            for w in kws:
                x = pc.match_substring(caps, w)
                m = x if m is None else pc.or_(m, x)
            sets[k].append(pids[np.asarray(pc.fill_null(m, False).to_numpy(zero_copy_only=False))])
    member = defaultdict(set)
    for k, v in sets.items():
        for p in np.concatenate(v).tolist():
            member[p].add(k)
    stats = {k: {"items": int(len(np.unique(np.concatenate(v)))), "exposures": 0, "users": 0, "user_counts": []} for k, v in sets.items()}
    total = 0
    fb = pq.ParquetFile(f"{recif_dir}/onerec_bench_release.parquet")
    for rg in range(fb.num_row_groups):
        for r in fb.read_row_group(rg, columns=["hist_video_pid", "target_video_pid"]).to_pylist():
            seq = (r["hist_video_pid"] or []) + (r["target_video_pid"] or [])
            total += len(seq)
            c = defaultdict(int)
            for p in seq:
                for k in member.get(p, ()):
                    c[k] += 1
            for k, n in c.items():
                stats[k]["exposures"] += n
                stats[k]["users"] += 1
                stats[k]["user_counts"].append(n)
    out = {}
    for k, s in stats.items():
        uc = np.array(s.pop("user_counts") or [0])
        out[k] = {**s, "share_of_exposures": s["exposures"] / total, "user_median": float(np.median(uc)),
                  "users_ge20": int((uc >= 20).sum())}
    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
