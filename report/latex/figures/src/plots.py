"""Charts for the report, drawn from results.json (constructed data; see ../../README.md).

Run:  python3 plots.py            # writes ../fig_*.pdf
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("pdf")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.ticker import FuncFormatter, PercentFormatter

import model as M

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
R = json.loads((SRC / "results.json").read_text())

import sys
sys.path.insert(0, str(SRC / "fonts"))
from pagella import FAMILY, ensure  # noqa: E402  TrueType copies of the report's body font

for f in ensure().values():
    font_manager.fontManager.addfont(str(f))

INK, TICK, GRID, MUTE = "#1A1A1A", "#5F6670", "#ECECEC", "#9AA1AB"
C_A, C_B, C_O = "#D1603D", "#2B5C8A", "#C9CED6"        # target narrative, other issue videos, everything else
C_TOPIC, C_NARR = "#2B5C8A", "#D1603D"
USER_COL = dict(fan_strong="#B5473F", fan_mild="#E39A6B", fan_none="#8A8F98", fan_averse="#3C7A89", casual_strong="#8B7BB8")
FAM_COL = dict(none="#8A8F98", implicit="#2E8B8B", explicit="#D1603D", history="#7B6BB0", platform="#5F7A99", filter="#C9952C")
FAM_LAB = dict(implicit="Viewing behaviour", explicit="Explicit feedback", history="History editing",
               platform="Platform setting", filter="External filter")
TYPE_COL = ["#2B5C8A", "#6F9CC6", "#E39A6B", "#B5473F"]
W = 6.3  # text width, inches

plt.rcParams.update({
    "font.family": FAMILY, "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8.6, "axes.titleweight": "bold",
    "axes.titlelocation": "left", "axes.titlepad": 5, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "legend.fontsize": 7.2, "axes.edgecolor": TICK, "axes.labelcolor": INK, "xtick.color": TICK, "ytick.color": TICK,
    "text.color": INK, "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 2.5, "ytick.major.size": 2.5, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True, "legend.frameon": False,
    "lines.linewidth": 1.3, "pdf.fonttype": 42, "mathtext.fontset": "custom", "mathtext.rm": FAMILY,
    "mathtext.it": f"{FAMILY}:italic", "mathtext.bf": f"{FAMILY}:bold", "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
})


def panel(ax, letter, title):
    ax.set_title(f"{letter}   {title}", loc="left")


def signed(x, nd=2):
    return f"{'+' if x >= 0 else '−'}{abs(x):.{nd}f}"


def save(fig, name, target=W):
    # widen or narrow the canvas until the cropped figure is exactly `target` inches wide,
    # so that every figure is included at scale 1 and all text has the same size on the page
    for _ in range(4):
        bb = fig.get_tightbbox(fig._get_renderer())
        if abs(bb.width + 0.04 - target) < 0.005:
            break
        fw, fh = fig.get_size_inches()
        fig.set_size_inches(fw + (target - 0.04 - bb.width), fh)
    fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)
    print("wrote", name)


# ===================================================================================== framework
# ===================================================================================== landscape
def fig_landscape():
    L = R["landscape"]
    rows = L["rows"]
    fig, axs = plt.subplots(1, 3, figsize=(W, 2.15), gridspec_kw=dict(width_ratios=[1.0, 1.0, 1.35], wspace=0.2))
    ax, bx, cx = axs
    y = np.arange(len(rows))[::-1]
    panel(ax, "a", "Share of the feed")
    tot = np.array([100 * r["share_all"] for r in rows])
    opp = np.array([100 * r["share_all"] * r["opp_share"] for r in rows])
    ax.barh(y, tot, color="#C8D7E6", height=0.62)
    ax.barh(y, opp, color=C_A, height=0.62)
    for yi, t, r in zip(y, tot, rows):
        ax.text(t + 0.06, yi, f"{t:.1f}%", va="center", fontsize=7.1, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels([r["domain"] for r in rows], fontsize=7.6, color=INK)
    ax.set_xlim(0, 3.1)
    ax.set_xticks([0, 1, 2, 3])
    ax.xaxis.set_major_formatter(PercentFormatter(decimals=0))
    ax.grid(axis="y", visible=False)
    ha_ = [Rectangle((0, 0), 1, 1, color=C_A), Rectangle((0, 0), 1, 1, color="#C8D7E6")]
    la_ = ["opposing narrative", "other issue videos"]

    panel(bx, "b", "Opposing, by type")
    left = np.zeros(len(rows))
    for i, tname in enumerate(L["types"]):
        vals = np.array([100 * r["types"][i] / r["n"] for r in rows])
        bx.barh(y, vals, left=left, color=TYPE_COL[i], height=0.62, label=tname)
        left += vals
    for yi, r in zip(y, rows):
        bx.text(100 * r["opp_share"] + 0.6, yi, f"{100*r['opp_share']:.0f}%", va="center", fontsize=7.1, color=INK)
    bx.set_yticks(y)
    bx.set_yticklabels([])
    bx.tick_params(axis="y", length=0)
    bx.set_xlim(0, 29.5)
    bx.set_xticks([0, 10, 20])
    bx.xaxis.set_major_formatter(PercentFormatter(decimals=0))
    bx.grid(axis="y", visible=False)

    panel(cx, "c", "Engagement vs. other issue videos")
    E = R["engagement"]["by"]
    names = list(E.keys())
    yy = np.arange(len(names))[::-1]
    outs = [("finish", "finished", "#8A8F98", "o"), ("like", "liked", C_B, "s"), ("share", "shared", "#C9952C", "D"),
            ("comment", "commented", C_A, "^")]
    off = np.linspace(0.24, -0.24, len(outs))
    for (k, lab, col, mk), o in zip(outs, off):
        xs = [E[n][k]["or_"] for n in names]
        lo = [E[n][k]["lo"] for n in names]
        hi = [E[n][k]["hi"] for n in names]
        cx.hlines(yy + o, lo, hi, color=col, lw=1.0)
        cx.scatter(xs, yy + o, s=13, color=col, marker=mk, zorder=4, label=lab, edgecolor="white", linewidth=0.4)
    cx.axvline(1, color=INK, lw=0.7)
    cx.axhline(3.5, color=GRID, lw=0.8)
    cx.set_xscale("log")
    cx.set_xticks([1, 1.5, 2, 2.5])
    cx.set_xticklabels(["1×", "1.5×", "2×", "2.5×"])
    cx.minorticks_off()
    cx.set_xlim(0.93, 3.0)
    cx.set_yticks(yy)
    cx.set_yticklabels(names, fontsize=7.6, color=INK)
    cx.yaxis.tick_right()
    cx.tick_params(axis="y", length=0)
    cx.spines["left"].set_visible(False)
    cx.grid(axis="y", visible=False)
    cx.set_xlabel("Adjusted odds ratio (95% CI)", labelpad=2)
    # one legend for panels b and c, below the figure: first row narrative types, second row engagement
    hb, lb = bx.get_legend_handles_labels()
    hc, lc = cx.get_legend_handles_labels()
    # columns: panel a, then one column per narrative type (top) and engagement outcome (bottom)
    hs = ha_ + [h for pair in zip(hb, hc) for h in pair]
    ls = la_ + [l for pair in zip(lb, lc) for l in pair]
    fig.legend(hs, ls, loc="upper center", bbox_to_anchor=(0.5, -0.07), ncol=5, handlelength=0.9, handleheight=0.7,
               handletextpad=0.35, columnspacing=1.3, labelspacing=0.35, borderaxespad=0.0)
    ax.set_xlabel("% of impressions")
    bx.set_xlabel("% of the domain")
    save(fig, "fig_landscape")


# ===================================================================================== logs
def fig_logs():
    F = R["funnel"]
    m, V = 100 * np.array(F["m"]), np.array(F["V"])
    fig = plt.figure(figsize=(W, 2.3))
    gs = fig.add_gridspec(1, 4, width_ratios=[1.35, 0.22, 0.22, 1.25], wspace=0.05)
    ax = fig.add_subplot(gs[0])
    hx = fig.add_subplot(gs[1], sharey=ax)
    bx = fig.add_subplot(gs[3])
    panel(ax, "a", "Skew varies widely, whatever the topic share")
    ax.scatter(m, V, s=1.6, color=C_B, alpha=0.16, linewidth=0, rasterized=True)
    ln2 = np.log(2)
    for yv, lab in ((ln2, "odds ×2"), (-ln2, "odds ×½")):
        ax.axhline(yv, color=C_A, lw=0.7, ls=(0, (3, 2)))
        ax.text(44.3, yv + (0.05 if yv < 0 else -0.16), lab, color=C_A, fontsize=6.7, ha="right")
    ax.axhline(0, color=INK, lw=0.6)
    bins = np.array([3.5, 6, 10, 15, 21, 28, 45])
    mid, q10, q90 = [], [], []
    for a, b in zip(bins[:-1], bins[1:]):
        sel = (m >= a) & (m < b)
        mid.append(m[sel].mean())
        q10.append(np.quantile(V[sel], 0.1))
        q90.append(np.quantile(V[sel], 0.9))
    ax.plot(mid, q90, color=INK, lw=0.9, marker="o", ms=2.2)
    ax.plot(mid, q10, color=INK, lw=0.9, marker="o", ms=2.2)
    ax.text(mid[-1] + 1.2, q90[-1] + 0.08, "90th pct.", fontsize=6.4, ha="right")
    ax.text(mid[-1] + 1.2, q10[-1] - 0.14, "10th pct.", fontsize=6.4, ha="right")
    ax.set_xlim(2.5, 45)
    ax.set_ylim(-1.3, 1.9)
    ax.set_xlabel("Topic share  $m$  (% of the user's impressions)")
    ax.set_ylabel("Personal skew  $V_u$  (log-odds)")
    ax.text(3.6, -0.80, f"$\\rho(m, V)$ = {F['rho_m']:.2f}\n$\\rho$(category entropy, $V$) = {F['rho_ent']:.2f}".replace("-", "−"),
            fontsize=6.9, va="top", linespacing=1.4)
    hx.hist(V, bins=np.linspace(-1.3, 1.9, 44), orientation="horizontal", color="#C8D7E6", lw=0)
    hx.hist(V[V > ln2], bins=np.linspace(-1.3, 1.9, 44), orientation="horizontal", color=C_A, lw=0)
    hx.axis("off")
    ax.text(44.3, 1.72, f"{100*F['frac_hi']:.0f}% of heavy viewers above", color=C_A, fontsize=6.7, ha="right", va="top")

    panel(bx, "b", "Skew grows with the narrative in recent history")
    O = R["obs_dose"]
    ks = np.arange(len(O))
    bx.plot(ks, [M.probe(o["k"], "narrative")[1] for o in O], color=C_A, lw=1.2, marker="s", ms=3.2, mfc="white", mew=1.0,
            label="recommender probe at the same $k$ (Sec. 5.2)")
    bx.errorbar(ks, [o["V"] for o in O], yerr=[[o["V"] - o["lo"] for o in O], [o["hi"] - o["V"] for o in O]], fmt="o", ms=3.4,
                color=INK, elinewidth=0.9, capsize=1.8, label="logs (observed, 95% CI)", zorder=5)
    bx.axhline(0, color=INK, lw=0.6)
    bx.set_xlabel("Narrative videos finished among the last 200")
    bx.set_ylabel("Skew of the next issue impressions")
    bx.set_xticks(ks)
    bx.set_xticklabels([o["bin"] for o in O])
    bx.set_ylim(-0.15, 1.5)
    bx.set_xlim(-0.4, 5.4)
    bx.legend(loc="upper left")
    save(fig, "fig_logs")


# ===================================================================================== probe
def fig_probe():
    P = R["probe"]
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(W, 2.2), gridspec_kw=dict(width_ratios=[1.15, 1], wspace=0.27))
    panel(ax, "a", "Response to videos injected into the history")
    ks = np.array(P["k"])
    kk = np.linspace(0, 42, 80)
    series = [("topic", "topic share, after issue videos", C_TOPIC, "o", "issue", 0),
              ("narr", "within-issue mix, after narrative videos", C_NARR, "s", "narrative", 1)]
    for key, lab, col, mk, kind, idx in series:
        ax.plot(kk, [M.probe(k, kind)[idx] for k in kk], color=col, lw=1.0, alpha=0.55)
        mu = np.array([p["mean"] for p in P[key]])
        lo = np.array([p["lo"] for p in P[key]])
        hi = np.array([p["hi"] for p in P[key]])
        ax.errorbar(ks, mu, yerr=[mu - lo, hi - mu], fmt=mk, ms=3.6, color=col, elinewidth=0.9, capsize=1.8, label=lab, zorder=5)
    mu = np.array([p["mean"] for p in P["narr_from_other"]])
    lo = np.array([p["lo"] for p in P["narr_from_other"]])
    hi = np.array([p["hi"] for p in P["narr_from_other"]])
    ax.errorbar(ks, mu, yerr=[mu - lo, hi - mu], fmt="D", ms=2.8, color=MUTE, elinewidth=0.8, capsize=1.5,
                label="within-issue mix, after other issue videos", zorder=4)
    q = P["null"]["q975"]
    ax.axhspan(-q, q, color="#E6E8EB", lw=0, zorder=0)
    ax.text(41.5, q + 0.05, "random-split null (95%)", fontsize=6.4, color=TICK, ha="right")
    ax.axhline(0, color=INK, lw=0.6)
    ax.set_xlabel("Injected videos  $k$  (history of 200)")
    ax.set_ylabel("Change in log-odds")
    ax.set_xticks([0, 2, 5, 10, 20, 40])
    ax.set_xlim(-1, 43)
    ax.set_ylim(-0.45, 3.2)
    ax.legend(loc="upper left", handletextpad=0.3)

    panel(bx, "b", "The same ten videos in different fields")
    Fd = P["fields"]
    x = np.arange(len(Fd))
    wdt = 0.36
    for i, (key, col, lab) in enumerate((("topic", C_TOPIC, "topic share"), ("narr", C_NARR, "within-issue mix"))):
        mu = np.array([f[key]["mean"] for f in Fd])
        lo = np.array([f[key]["lo"] for f in Fd])
        hi = np.array([f[key]["hi"] for f in Fd])
        cols = [col] * len(Fd)
        bars = bx.bar(x + (i - 0.5) * wdt, mu, wdt * 0.92, color=cols, label=lab)
        bx.errorbar(x + (i - 0.5) * wdt, mu, yerr=[mu - lo, hi - mu], fmt="none", ecolor=INK, elinewidth=0.7, capsize=1.5)
        for xi, v in zip(x + (i - 0.5) * wdt, hi):
            pass
    for xi, f in zip(x, Fd):
        bx.text(xi - 0.5 * wdt - 0.03, f["topic"]["hi"] + 0.035, signed(f["topic"]["mean"]), ha="center", fontsize=6.2)
        bx.text(xi + 0.5 * wdt + 0.05, f["narr"]["hi"] + 0.035, signed(f["narr"]["mean"]), ha="center", fontsize=6.2)
    bx.axhline(0, color=INK, lw=0.6)
    bx.set_xticks(x)
    bx.set_xticklabels(["watched\nto the end", "liked", "“not\ninterested”", "unlabelled\nextra field"], fontsize=7.2, color=INK)
    bx.set_ylabel("Change in log-odds")
    bx.set_ylim(-0.6, 1.55)
    bx.grid(axis="x", visible=False)
    bx.annotate("what a negative signal\nwould look like", xy=(2, -0.32), xytext=(2.0, -0.5), fontsize=6.4, color=TICK, ha="center", va="center")
    bx.add_patch(FancyArrowPatch((2.0, -0.05), (2.0, -0.36), arrowstyle="-|>", mutation_scale=6, lw=0.8, color=MUTE, ls=(0, (2, 2))))
    bx.legend(loc="upper right", handlelength=0.9, handleheight=0.7)
    save(fig, "fig_probe")


# ===================================================================================== formation
def fig_formation():
    Fm = R["formation"]["users"]
    fig, axs = plt.subplots(1, 3, figsize=(W, 2.25), gridspec_kw=dict(width_ratios=[1.25, 1, 1.05], wspace=0.36))
    ax, bx, cx = axs
    order = ["fan_strong", "fan_mild", "fan_none", "fan_averse", "casual_strong"]
    lab_short = dict(fan_strong="strong pref.", fan_mild="mild pref.", fan_none="no pref.",
                     fan_averse="averse", casual_strong="casual viewer")
    panel(ax, "a", "Personal viewpoint skew")
    for k in order:
        u = Fm[k]
        d = np.array(u["t"]) / M.VIDEOS_PER_DAY
        ls = (0, (4, 2)) if k == "casual_strong" else "-"
        if k in ("fan_strong", "fan_averse"):
            ax.fill_between(d, u["V_lo"], u["V_hi"], color=USER_COL[k], alpha=0.13, lw=0)
        ax.plot(d, u["V"], color=USER_COL[k], ls=ls)
        yv = u["V_end"] + {"casual_strong": 0.13, "fan_none": -0.10, "fan_averse": -0.04}.get(k, 0)
        ax.text(d[-1] + 1.5, yv, lab_short[k], color=USER_COL[k], fontsize=6.8, va="center")
    ax.axhline(0, color=INK, lw=0.5)
    ax.set_xlim(0, 132)
    ax.set_xticks([0, 30, 60, 90])
    ax.set_ylim(-0.75, 1.35)
    ax.set_xlabel("Days of use (180 videos a day)")
    ax.set_ylabel("$V$  (log-odds)")
    ax.spines["bottom"].set_bounds(0, 90)

    panel(bx, "b", "Topic share")
    for k in order:
        u = Fm[k]
        d = np.array(u["t"]) / M.VIDEOS_PER_DAY
        bx.plot(d, 100 * np.array(u["m"]), color=USER_COL[k], ls=(0, (4, 2)) if k == "casual_strong" else "-")
    bx.set_xticks([0, 30, 60, 90])
    bx.set_xlabel("Days of use")
    bx.set_ylabel("$m$  (% of feed)")
    bx.set_ylim(0, 36)
    bx.text(88, 32.3, "the four topic fans", fontsize=6.8, ha="right", color=TICK)
    bx.text(88, 7.3, "casual viewer", fontsize=6.8, ha="right", color=USER_COL["casual_strong"])

    panel(cx, "c", "What the recommender must separate")
    S = R["sweep"]
    cx.plot(S["ratio"], S["strong"], color=USER_COL["fan_strong"], marker="o", ms=2.6, label="strong")
    cx.plot(S["ratio"], S["mild"], color=USER_COL["fan_mild"], marker="o", ms=2.6, label="mild")
    cx.axvline(S["measured"], color=INK, lw=0.7, ls=(0, (3, 2)))
    cx.text(S["measured"] - 0.03, 1.74, "fitted\n(Sec. 5.2)", fontsize=6.4, ha="right", va="top", color=INK)
    cx.set_xlabel("Narrative response ÷ topic response  ($c/t$)")
    cx.set_ylabel("$V$ after 89 days")
    cx.set_ylim(-0.05, 1.8)
    cx.set_xlim(-0.03, 1.23)
    cx.legend(loc="upper left", bbox_to_anchor=(0.0, 0.84), handlelength=1.4, title="preference", title_fontsize=6.9, alignment="left")
    save(fig, "fig_formation")


# ===================================================================================== detection
def fig_detection():
    D = R["detection"]
    V = np.array(D["V"])
    a_, b_ = D["clfs"]["Validated classifier"]
    fig, (ax, bx, cx) = plt.subplots(1, 3, figsize=(W, 2.2), gridspec_kw=dict(width_ratios=[1, 1.35, 1], wspace=0.42))
    C_KNOWN = "#2E8B7A"
    n_known = np.array([M.detection_n(v, alpha=a_, beta=b_, known_reference=True) for v in V])

    panel(ax, "a", "Issue videos needed")
    cols = {"Perfect labels": MUTE, "Validated classifier": C_B, "Keyword list": "#C9952C"}
    for k, c in cols.items():
        ax.plot(V, D["curves"][k], color=c, label=k.lower() if k != "Perfect labels" else "perfect labels")
    ax.plot(V, n_known, color=C_KNOWN, ls=(0, (4, 2)), label="published reference")
    ax.set_yscale("log")
    ax.set_ylim(40, 12000)
    ax.set_xlim(0.2, 2.0)
    n2 = M.detection_n(np.log(2), alpha=a_, beta=b_)
    ax.scatter([np.log(2)], [n2], s=18, color=C_B, zorder=5, edgecolor="white", linewidth=0.5)
    ax.annotate(f"odds ×2: {int(round(n2, -1))}", xy=(np.log(2), n2), xytext=(0.25, 60), fontsize=6.8,
                arrowprops=dict(arrowstyle="-", color=TICK, lw=0.6), color=INK)
    ax.set_xlabel("Personal skew  $V$")
    ax.set_ylabel("Issue videos per sample")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.legend(loc="upper right", fontsize=6.2, handlelength=1.6, labelspacing=0.25, borderaxespad=0.2)

    # (b) what one topic fan with a doubled odds would see, day by day
    panel(bx, "b", "One user counting, day by day")
    pu = float(M.expit(M.logit(M.P_BAR) + np.log(2)))
    p0 = M.P_BAR
    days = np.arange(1, 131)
    rng = np.random.default_rng(7)

    def est(p, per_day):
        q = b_ + (a_ - b_) * p
        n = days * per_day
        k = np.cumsum(rng.binomial(np.round(np.full(days.size, per_day)).astype(int), q))
        qh = k / np.maximum(n, 1)
        se = np.sqrt(q * (1 - q) / n) / (a_ - b_)
        return 100 * (qh - b_) / (a_ - b_), 100 * (p - 1.96 * se), 100 * (p + 1.96 * se)

    own, own_lo, own_hi = est(pu, D["per_day_fan"])
    ref, ref_lo, ref_hi = est(p0, D["per_day_avg"])
    bx.fill_between(days, ref_lo, ref_hi, color=MUTE, alpha=0.16, lw=0)
    bx.fill_between(days, own_lo, own_hi, color=C_B, alpha=0.16, lw=0)
    bx.plot(days, ref, color=MUTE, lw=1.0, label="reference the user collects")
    bx.plot(days, own, color=C_B, lw=1.2, label="own feed")
    bx.axhline(100 * p0, color=C_KNOWN, lw=1.0, ls=(0, (4, 2)), label="published reference")
    d_known = M.detection_n(np.log(2), alpha=a_, beta=b_, known_reference=True) / D["per_day_fan"]
    d_ref = n2 / D["per_day_avg"]
    for d, lab, c, y, ha, dx in ((d_known, f"day {d_known:.0f}: enough against\nthe published reference", C_KNOWN, 17.2, "left", 2),
                                 (d_ref, f"day {d_ref:.0f}: enough against\na collected reference", "#5F6670", 15.4, "right", -2)):
        bx.axvline(d, color=c, lw=0.8, ls=(0, (1, 1.6)))
        bx.text(d + dx, y, lab, fontsize=6.0, color=c, va="top", ha=ha, linespacing=1.15)
    bx.set_xlim(0, 130)
    bx.set_ylim(0, 18)
    bx.set_xlabel("Days of viewing")
    bx.set_ylabel("Estimated group-label share (%)")
    bx.legend(loc="lower right", fontsize=6.2, handlelength=1.6, labelspacing=0.25, borderaxespad=0.2)

    panel(cx, "c", "Days needed")
    n = np.array(D["curves"]["Validated classifier"])
    cx.plot(V, n / D["per_day_avg"], color=MUTE, label="collected reference")
    cx.plot(V, n / D["per_day_fan"], color=C_B, label="own feed")
    cx.plot(V, n_known / D["per_day_fan"], color=C_KNOWN, ls=(0, (4, 2)), label="published reference")
    cx.set_yscale("log")
    cx.set_ylim(0.3, 1500)
    cx.set_xlim(0.2, 2.0)
    for d, lab in ((7, "week"), (30.4, "month"), (365, "year")):
        cx.axhline(d, color=TICK, lw=0.5, ls=(0, (1, 2)))
        cx.text(1.62, d * 0.86, lab, fontsize=6.2, color=TICK, ha="left", va="top")
    cx.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    cx.set_xlabel("Personal skew  $V$")
    cx.set_ylabel("Days of viewing")
    cx.legend(loc="lower left", fontsize=6.2, handlelength=1.6, labelspacing=0.25, borderaxespad=0.2, frameon=True, facecolor="white", edgecolor="none", framealpha=0.92)
    save(fig, "fig_detection")


# ===================================================================================== escape
def fig_escape():
    E = R["escape"]["strategies"]
    n_act = R["escape"]["n_act"]
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(W, 2.75), gridspec_kw=dict(width_ratios=[1, 1.12], wspace=0.26))
    panel(ax, "a", "Effect on the skew against topic kept")
    V0 = E["S0"]["V0"]
    ax.plot([-4, 104], [0, 0], color=INK, lw=0.6)
    ax.plot([-4, 104], [-V0, -V0], color=C_B, lw=0.8, ls=(0, (3, 2)))
    ax.text(14, -V0 - 0.05, "$V$ = 0: personal layer removed", color=C_B, fontsize=6.6, ha="left", va="top")
    ax.plot([-4, 104], [-V0 - M.PLATFORM_LAYER] * 2, color=MUTE, lw=0.8, ls=(0, (3, 2)))
    ax.text(14, -V0 - M.PLATFORM_LAYER - 0.05, "supply level", color=TICK, fontsize=6.6, ha="left", va="top")
    col_y = dict(S0=0.14, S4=-0.44, S2=-0.68, S1=-0.92, S6=-1.12, S10=-1.33, S3=-1.54, S5=-2.06, S11=-2.56)
    side = dict(S7=(0, 0.16), S8=(2.5, 0.16), S9=(-1.5, 0.16))
    for s, e in E.items():
        x, y = 100 * e["topic_kept"], e["dV_late"]
        col = FAM_COL[e["family"]]
        ax.scatter([x], [y], s=46 if s == "S6" else 26, color="white" if s == "S6" else col, zorder=4 if s == "S6" else 5,
                   edgecolor=col if s == "S6" else "white", linewidth=1.0 if s == "S6" else 0.6)
        if s in col_y:
            ax.plot([x + 1.6, 106.5], [y, col_y[s]], color=col, lw=0.5, alpha=0.7, zorder=3)
            ax.text(108, col_y[s], s, fontsize=7.1, fontweight="bold", color=col, ha="left", va="center")
        else:
            dx, dy = side[s]
            ax.text(x + dx, y + dy, s, fontsize=7.1, fontweight="bold", color=col, ha="center", va="center")
    ax.set_xlim(-4, 122)
    ax.set_ylim(-2.85, 0.4)
    ax.set_xlabel("Topic kept (% of the share before acting)")
    ax.set_ylabel("Change in skew after 17 days (log-odds)")
    ax.set_xticks([0, 25, 50, 75, 100])
    hs = [Line2D([], [], marker="o", ls="", ms=4.2, color=FAM_COL[k], label=v) for k, v in FAM_LAB.items()]
    ax.legend(handles=hs, loc="lower left", bbox_to_anchor=(0.0, 0.0), handletextpad=0.1, labelspacing=0.25, borderaxespad=0.2)

    panel(bx, "b", "During the action and after it stops")
    bx.axvspan(0, n_act / M.VIDEOS_PER_DAY, color="#F3F1EC", lw=0)
    bx.text(n_act / M.VIDEOS_PER_DAY / 2, 1.27, "acting", ha="center", fontsize=6.9, color=TICK)
    bx.text(n_act / M.VIDEOS_PER_DAY + 11, 1.27, "stopped: old habits return", ha="center", fontsize=6.9, color=TICK)
    show = [("S0", "S0 continue"), ("S2", "S2 button (as built)"), ("S1", "S1 scroll past"), ("S3", "S3 button (true negative)"),
            ("S7", "S7 clear history"), ("S11", "S11 classifier filter")]
    for s, lab in show:
        e = E[s]
        d = np.array(e["t"]) / M.VIDEOS_PER_DAY
        v = np.array(e["V"])   # mean of 400 simulated users, unsmoothed
        bx.plot(d, v, color=FAM_COL[e["family"]], lw=1.2, ls=(0, (4, 1.5)) if s in ("S2", "S7") else "-",
                alpha=1.0, label=lab)
    bx.axhline(0, color=INK, lw=0.5)
    bx.set_xlim(-6, 39)
    bx.set_ylim(-2.2, 1.45)
    bx.set_xlabel("Days since the user started acting")
    bx.set_ylabel("Personal skew  $V$")
    lab_pos = dict(S0=(38.5, 0.93, "S0"), S2=(8.2, 0.33, "S2"), S1=(12.6, -0.48, "S1"), S3=(11.3, -0.95, "S3"), S7=(2.4, -0.22, "S7"),
                   S11=(8.3, -1.93, "S11"))
    for s, (x, y, t) in lab_pos.items():
        bx.text(x, y, t, fontsize=7.1, fontweight="bold", color=FAM_COL[E[s]["family"]], ha="right" if s == "S0" else "left")
    save(fig, "fig_escape")


# ===================================================================================== teaser (right panel)
if __name__ == "__main__":
    fig_landscape()
    fig_logs()
    fig_probe()
    fig_formation()
    fig_detection()
    fig_escape()
