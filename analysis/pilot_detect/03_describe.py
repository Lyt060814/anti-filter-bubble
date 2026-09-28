"""Step 3: descriptive facts on the user-day table (works for kuairec / kuairand)."""
import json
import sys
import numpy as np
import pandas as pd

name = sys.argv[1] if len(sys.argv) > 1 else "kuairec"
ud = pd.read_parquet(f"{name}_userday.parquet")
info = json.load(open(f"{name}_info.json"))
base_days = set(info["baseline_days"])
print(f"== {name}: users {ud.u.nunique()}, user-days {len(ud)}")
print("exposures per user-day quantiles:", ud.n.quantile([.1, .25, .5, .75, .9]).to_dict())
print("share user-days with n>=20:", round((ud.n >= 20).mean(), 3),
      "| n>=10:", round((ud.n >= 10).mean(), 3))
print("screen signals (user-days with n>=20) mean/median:")
s = ud[ud.n >= 20]
print(s[["D20", "S20", "A20", "NOV20"]].describe().loc[["mean", "25%", "50%", "75%"]].round(3).to_string())
print("baseline entropy B: valid users", ud.drop_duplicates("u").B.notna().sum(),
      ud.drop_duplicates("u").B.describe().round(3).to_dict())
print("mean R_W by day (population trend):")
print(ud.groupby("day").RW.mean().dropna().round(3).to_string())

post = ud[(~ud.day.isin(base_days)) & ud.RW.notna() & ud.B.notna()]
users = post.groupby("u").agg(ev15=("ev15", "any"), ev25=("ev25", "any"), ndays=("day", "size"))
print("\nEvent state share of post-baseline user-days: X=15%:", round(post.ev15.mean(), 4),
      "X=25%:", round(post.ev25.mean(), 4))
print("Sampling-noise null event rate (same n, baseline mix): X=15%:", round(info["null_event_rate15"], 4),
      "X=25%:", round(info["null_event_rate25"], 4))
print("Share of users with >=1 event day: X=15%:", round(users.ev15.mean(), 4), "X=25%:", round(users.ev25.mean(), 4),
      "(n users", len(users), ")")
for tag in (15, 25):
    first = post[post[f"ev{tag}"]].groupby("u").day.min()
    seg = post.drop_duplicates("u").set_index("u")
    print(f"X={tag}%: first event day distribution (days since baseline start):",
          first.describe().round(1).to_dict())
    print("   first event in which segment:", post[post[f"ev{tag}"]].groupby("u").seg.min().value_counts().to_dict())
    # persistence: of event user-days, share where event also next day
    nxt = post.groupby("u")[f"ev{tag}"].shift(-1)
    m = post[f"ev{tag}"] & nxt.notna()
    print(f"   persistence P(event at t+1 | event at t) = {nxt[m].astype(bool).mean():.3f}")

# heavy users: quartile of mean daily exposures in baseline
act = ud[ud.day.isin(base_days)].groupby("u").n.mean()
users["q_act"] = pd.qcut(act.reindex(users.index), 4, labels=["Q1 light", "Q2", "Q3", "Q4 heavy"])
tab = users.groupby("q_act", observed=True)[["ev15", "ev25"]].mean().round(3)
tab["mean_daily_exposures"] = act.groupby(users.q_act).mean().round(1)
print("\nEvent-ever share by baseline activity quartile:\n", tab.to_string())
print("share of all X=15% event user-days from Q4 heavy users:",
      round(post[post.ev15].u.map(users.q_act).eq("Q4 heavy").mean(), 3))
