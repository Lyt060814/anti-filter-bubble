"""Step 1: KuaiRec big_matrix -> clean exposure table (parquet).

Each row of big_matrix = one video played (at least started) by a user = one "exposure".
Output columns: user_id, ts (unix seconds), day (int index from 2020-07-05), cat (first-level
category code, -1 = UNKNOWN/missing), author (author_id, -1 missing).
"""
import numpy as np
import pandas as pd

D = "/home/user/data/kuairec/KuaiRec 2.0/data"
bm = pd.read_csv(f"{D}/big_matrix.csv",
                 usecols=["user_id", "video_id", "date", "timestamp", "watch_ratio"],
                 dtype={"user_id": "int32", "video_id": "int32", "date": "float64",
                        "timestamp": "float64", "watch_ratio": "float32"})
print("raw rows", len(bm))
bm = bm.dropna(subset=["timestamp", "date"])
print("rows with timestamp+date", len(bm))

# duplicates
n_pair_dup = bm.duplicated(["user_id", "video_id"]).sum()
n_exact = bm.duplicated(["user_id", "video_id", "timestamp"]).sum()
print("dup user-video pairs", n_pair_dup, "| exact dup (user,video,timestamp)", n_exact)
# how far apart are repeated plays of the same pair?
bm = bm.sort_values(["user_id", "timestamp"])
g = bm.groupby(["user_id", "video_id"]).timestamp
gap = g.diff().dropna()
print("gap between repeated plays of same pair (hours): quantiles",
      (gap / 3600).quantile([.1, .25, .5, .75, .9]).round(2).to_dict())
# Choice (see report): exact duplicates are log duplicates -> drop. Most remaining repeats of a
# pair happen within seconds (looping replay), so we keep only the FIRST play of a video per
# user per calendar day. Repeats on different days (median gap ~3 weeks) are kept: the feed
# really showed the item again.
bm = bm.drop_duplicates(["user_id", "video_id", "timestamp"])
n0 = len(bm)
bm = bm.drop_duplicates(["user_id", "video_id", "date"])  # already sorted by timestamp -> keeps first
print("after exact dedupe", n0, "| after same-day dedupe", len(bm))

# category
cats = pd.read_csv(f"{D}/kuairec_caption_category.csv", engine="python", on_bad_lines="skip",
                   usecols=["video_id", "first_level_category_name"])
cats["video_id"] = pd.to_numeric(cats.video_id, errors="coerce")
cats = cats.dropna().drop_duplicates("video_id")
cats["video_id"] = cats.video_id.astype("int32")
names = sorted(n for n in cats.first_level_category_name.unique() if n != "UNKNOWN")
code = {n: i for i, n in enumerate(names)}
cats["cat"] = cats.first_level_category_name.map(code).fillna(-1).astype("int16")
print("known categories", len(names))
pd.Series(names).to_csv("cat_names.csv", header=["name"])

# author (constant per video; take the most frequent)
auth = pd.read_csv(f"{D}/item_daily_features.csv", usecols=["video_id", "author_id"])
auth = auth.groupby("video_id").author_id.agg(lambda s: s.mode().iloc[0]).rename("author").reset_index()

bm = bm.merge(cats[["video_id", "cat"]], on="video_id", how="left").merge(auth, on="video_id", how="left")
bm["cat"] = bm.cat.fillna(-1).astype("int16")
bm["author"] = bm.author.fillna(-1).astype("int64")
d = pd.to_datetime(bm.date.astype(int).astype(str))
bm["day"] = (d - pd.Timestamp("2020-07-05")).dt.days.astype("int16")
bm = bm.rename(columns={"timestamp": "ts"})[["user_id", "video_id", "ts", "day", "cat", "author", "watch_ratio"]]
bm = bm.sort_values(["user_id", "ts"]).reset_index(drop=True)
print("final exposures", len(bm), "| UNKNOWN/missing cat share", round((bm.cat < 0).mean(), 4),
      "| missing author share", round((bm.author < 0).mean(), 4))
print("exposures per day index:\n", bm.groupby("day").size().to_string())
bm.to_parquet("kuairec_exposures.parquet")
