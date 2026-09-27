"""Quick look: does users' category diversity narrow over time in KuaiRec's big_matrix?

Exploratory only. Data: KuaiRec 2.0 (Gao et al., CIKM 2022), CC BY 4.0,
https://zenodo.org/records/18164998 -- unzip KuaiRec.zip and set DATA_DIR below.

Compares, per user-week, the normalised Shannon entropy of first-level categories of
(a) all videos EXPOSED to the user and (b) videos the user ENGAGED with (watch_ratio >= 2).
Caveats: entropy depends on the number of items per week; weeks 2 and 6 have no data;
"engaged" is a crude proxy.
"""
import numpy as np
import pandas as pd

DATA_DIR = "KuaiRec 2.0/data"
N_CATEGORIES = 41

bm = pd.read_csv(f"{DATA_DIR}/big_matrix.csv", usecols=["user_id", "video_id", "date", "watch_ratio"])
cats = pd.read_csv(f"{DATA_DIR}/kuairec_caption_category.csv", engine="python", on_bad_lines="skip",
                   usecols=["video_id", "first_level_category_name"])
cats["video_id"] = pd.to_numeric(cats.video_id, errors="coerce")
bm = bm.merge(cats.dropna(), on="video_id", how="left").dropna(subset=["date"])
bm = bm[bm.first_level_category_name.notna() & (bm.first_level_category_name != "UNKNOWN")]
day = pd.to_datetime(bm.date.astype(int).astype(str))
bm["week"] = (day - day.min()).dt.days // 7


def norm_entropy(s):
    p = s.value_counts(normalize=True).values
    return -(p * np.log(p)).sum() / np.log(N_CATEGORIES)


keys = ["user_id", "week"]
table = pd.concat([
    bm.groupby(keys).first_level_category_name.agg(norm_entropy).rename("H_exposed"),
    bm[bm.watch_ratio >= 2].groupby(keys).first_level_category_name.agg(norm_entropy).rename("H_engaged"),
    bm.groupby(keys).size().rename("n"),
], axis=1).reset_index()
table = table[table.n >= 30]
print(table.groupby("week")[["H_exposed", "H_engaged", "n"]].agg(["mean", "count"]).round(3))
