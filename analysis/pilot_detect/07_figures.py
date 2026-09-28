"""Step 7: figures (PNG)."""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SCREEN_C, PLAT_C, REF_C, INK, MUTED = "#2a78d6", "#eb6834", "#8a8984", "#0b0b0b", "#52514e"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED})

res = pd.read_csv("kuairec_eval_results.csv")
summ = json.load(open("kuairec_eval_summary.json"))

# ---- Fig 1: AUC comparison ------------------------------------------------------------
show = [("S20 (high = alarm)", "S20 top-category share (single)"), ("D20 (low = alarm)", "D20 distinct categories (single)"),
        ("LR screen", "LR screen signals"), ("LR screen + log n", "LR screen + activity"),
        ("LR activity only (log n)", "Activity only (log n)"),
        ("H_day (low = alarm)", "Today's full entropy (single)"), ("LR platform", "LR platform signals")]
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
for ax, s in zip(axes, summ):
    r = res[res.tag == s["tag"]].set_index("model")
    vals = [r.AUC[m] for m, _ in show]
    cols = [SCREEN_C if r.group[m] == "screen" else PLAT_C if r.group[m] == "platform" else REF_C for m, _ in show]
    y = np.arange(len(show))[::-1]
    ax.barh(y, np.array(vals) - 0.5, left=0.5, color=cols, height=0.6)
    ci_end = {k: s["CI95"][k][1] for k in ("LR screen", "LR platform")}
    for (m, _), yi, v in zip(show, y, vals):
        ax.text(max(v, ci_end.get(m, 0)) + 0.006, yi, f"{v:.2f}", va="center", color=INK, fontsize=9)
    for m, ci_key in [("LR screen", "LR screen"), ("LR platform", "LR platform")]:
        yi = y[[k for k, _ in show].index(m)]
        lo, hi = s["CI95"][ci_key]
        ax.plot([lo, hi], [yi, yi], color=INK, lw=1.2)
    ax.set_yticks(y, [lab for _, lab in show])
    ax.set_xlim(0.5, 1.0)
    ax.axvline(0.5, color=MUTED, lw=0.8)
    ax.set_title(f"Event = 3-day entropy ≥{s['tag']}% below own baseline\n(test positives {s['positives_test']}, base rate {s['base_rate']:.1%})",
                 fontsize=9.5, color=INK)
    ax.set_xlabel("Test AUC (predict event in next 3 days)")
    ax.grid(axis="x", color="#e5e4df", lw=0.6)
    ax.set_axisbelow(True)
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (SCREEN_C, PLAT_C, REF_C)]
fig.legend(handles, ["Screen-visible (first 20 items)", "Platform-side (all exposures)", "Reference"],
           loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.55, -0.02))
fig.suptitle("KuaiRec: screen-visible vs platform-side early warning (black line = 95% CI)", fontsize=11, color=INK)
fig.tight_layout(rect=(0, 0.06, 1, 1))
fig.savefig("fig1_auc_comparison.png", dpi=160, bbox_inches="tight")

# ---- Fig 2: lead time distribution (X=15%) ----------------------------------------------
s = summ[0]
fig, ax = plt.subplots(figsize=(6.5, 3.4))
labs = [("al_single", f"Single rule S20 ≥ {s['rule_best_single']['threshold']:.2f}", SCREEN_C),
        ("al_LR screen", "LR screen", "#1baf7a"), ("al_LR platform", "LR platform", PLAT_C)]
w = 0.26
for i, (k, lab, c) in enumerate(labs):
    h = {int(a): b for a, b in s["lead"][k]["lead_hist"].items()}
    xs = np.arange(1, 8)
    ax.bar(xs + (i - 1) * w, [h.get(x, 0) for x in xs], width=w - 0.03, color=c,
           label=f"{lab}: detects {s['lead'][k]['detected_share']:.0%} of events, "
                 f"false-alarm {s['lead'][k]['false_alarm_segments']:.0%} of no-event user-segments")
ax.set_xlabel("Lead time: days between first alarm and event")
ax.set_ylabel("# test events")
ax.set_title(f"KuaiRec, X=15%: lead time of first alarm ({s['lead']['al_single']['events']} test events)", fontsize=10)
ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.2))
fig.tight_layout()
fig.savefig("fig2_lead_time.png", dpi=160, bbox_inches="tight")

# ---- Fig 3: event share by day vs noise null; + example user timeline -------------------
ud = pd.read_parquet("kuairec_userday.parquet")
info = json.load(open("kuairec_info.json"))
post = ud[(ud.day >= 7) & ud.RW.notna() & ud.B.notna()]
by = post.groupby("day").ev15.mean()
fig, axes = plt.subplots(1, 2, figsize=(11, 3.4), gridspec_kw={"width_ratios": [1, 1.2]})
ax = axes[0]
for seg in [(7, 7), (29, 36), (55, 62)]:
    b = by.loc[seg[0]:seg[1]]
    ax.plot(b.index, b.values * 100, color=SCREEN_C, lw=2, marker="o", ms=4)
ax.axhline(info["null_event_rate15"] * 100, color=MUTED, lw=1, ls="--")
ax.text(8, info["null_event_rate15"] * 100 + 0.15, "sampling-noise null", color=MUTED, fontsize=8)
ax.set_xlabel("Day index (0 = 2020-07-05; gaps = no data)")
ax.set_ylabel("% user-days in cocoon state (X=15%)")
ax.set_title("Share of users 'in cocoon' per day", fontsize=10)
# example: test user with a first event in segment C preceded by an alarm of the S20 rule
th = s["rule_best_single"]["threshold"]
cand = post[post.ev15 & (post.seg == 2)].groupby("u").day.min()
pick = None
for uu, e0 in cand.items():
    g = ud[(ud.u == uu) & (ud.seg == 2)]
    if ((g.day < e0) & (g.day >= 55) & (g.S20 >= th) & (g.n20 >= 20)).any() and e0 >= 58 and g.n.min() >= 25:
        pick = (uu, e0); break
ax = axes[1]
if pick:
    uu, e0 = pick
    g = ud[ud.u == uu].set_index("day")
    B = g.B.iloc[0]
    days = [d for d in range(53, 63) if d in g.index]
    ax.plot(days, g.loc[days, "RW"], color=PLAT_C, lw=2, marker="o", ms=4, label="3-day entropy R3 (platform)")
    ax.plot(days, g.loc[days, "S20"], color=SCREEN_C, lw=2, marker="s", ms=4, label="S20 top-category share (screen)")
    ax.axhline(0.85 * B, color=PLAT_C, lw=1, ls="--")
    ax.text(53, 0.85 * B + 0.01, "event threshold 0.85 × baseline", color=MUTED, fontsize=8)
    ax.axhline(th, color=SCREEN_C, lw=1, ls=":")
    ax.text(53, th + 0.01, f"alarm threshold S20 ≥ {th:.2f}", color=MUTED, fontsize=8)
    al = [d for d in days if g.loc[d, "S20"] >= th and d < e0]
    ax.scatter(al, g.loc[al, "S20"], s=90, facecolors="none", edgecolors=INK, zorder=5, label="alarm")
    ax.axvline(e0, color=MUTED, lw=0.8)
    ax.text(e0 + 0.1, 0.05, "first event", color=MUTED, fontsize=8)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Day index (segment C)")
    ax.set_title(f"Example test user (user_id {int(g.user_id.iloc[0])}), days 53–62", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=3)
fig.tight_layout()
fig.savefig("fig3_events_by_day_and_example.png", dpi=160, bbox_inches="tight")
print("example user", pick)
print("share of X=15% event user-days on days 58-60:", round(post[post.ev15].day.between(58, 60).mean(), 3))
