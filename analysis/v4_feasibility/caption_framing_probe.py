"""Check whether RecIF generated captions retain antagonistic narrative cues.

Usage: python -I caption_framing_probe.py PID2CAPTION_PARQUET OUT_TXT
Counts captions containing explicit gender-antagonism or generalisation cues and
writes random samples for manual reading. Cue hits are candidates, not labels.
"""
import random
import sys

import numpy as np
import pyarrow.compute as pc
import pyarrow.parquet as pq

CUES = {
    "slang": ["捞女", "凤凰男", "扶弟魔", "妈宝男", "普信男", "小仙女", "女拳", "田园女权", "彩礼贷"],
    "generalisation": ["女人都", "男人都", "女的都", "男的都", "现在的女孩", "现在的女人", "现在的男人", "女人就是", "男人就是"],
    "antagonism_frame": ["性别对立", "物质女", "拜金", "不劳而获", "骗婚", "吸血"],
    "neutral_marriage": ["离婚", "彩礼", "婆媳"],
}


def main():
    path, out_path = sys.argv[1], sys.argv[2]
    f = pq.ParquetFile(path)
    hits = {g: [] for g in CUES}
    for rg in range(f.num_row_groups):
        t = f.read_row_group(rg, columns=["pid", "dense_caption"])
        pids = t.column("pid").to_numpy()
        caps = t.column("dense_caption")
        for g, kws in CUES.items():
            mask = None
            for k in kws:
                m = pc.match_substring(caps, k)
                mask = m if mask is None else pc.or_(mask, m)
            idx = np.flatnonzero(pc.fill_null(mask, False).to_numpy(zero_copy_only=False))
            hits[g].extend((int(pids[i]), caps[int(i)].as_py()) for i in idx[:5000])
    rng = random.Random(5)
    with open(out_path, "w", encoding="utf-8") as out:
        for g, rows in hits.items():
            out.write(f"== {g}: {len(rows)} captions (capped at 5000 per row group)\n")
            for pid, cap in rng.sample(rows, min(12, len(rows))):
                out.write(f"[{pid}] {cap[:420]}\n")
            out.write("\n")
    print(open(out_path, encoding="utf-8").read())


if __name__ == "__main__":
    main()
