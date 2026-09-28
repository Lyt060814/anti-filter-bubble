"""Step 2: build KuaiRec user-day table.
Usage: python 02_kuairec_userday.py [min_win]   (min known exposures in a 3-day window; default 30)
"""
import json
import sys
import pandas as pd
from detect_lib import build_userday

min_win = int(sys.argv[1]) if len(sys.argv) > 1 else 30
out = "kuairec" if min_win == 30 else f"kuairec_mw{min_win}"
e = pd.read_parquet("kuairec_exposures.parquet", columns=["user_id", "ts", "day", "cat", "author"])
K = int(e.cat.max()) + 1
# observed days are 0-7, 27-36, 53-62 (see 01 output): three contiguous segments
SEG = [(0, 7), (27, 36), (53, 62)]
ud, info = build_userday(e, K, SEG, baseline_days=range(0, 7), W=3, H=3, min_win=min_win)
ud.to_parquet(f"{out}_userday.parquet")
info.update(K=K, min_win=min_win, baseline_days=list(range(0, 7)), first_pred_seg=1)
json.dump(info, open(f"{out}_info.json", "w"), indent=1)
print(out, info)
