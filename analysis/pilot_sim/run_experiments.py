"""
run_experiments.py -- runs all pilot experiments and writes figures + results.txt / results.json.
Usage:  python3 run_experiments.py            (~5-8 min on a laptop CPU)
"""
import json, time
from dataclasses import replace
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sim

OUT = {}
LINES = []
T_START = time.time()
U = 200


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LINES.append(s)


def ci(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    if len(x) == 0:
        return np.nan, np.nan
    return x.mean(), 1.96 * x.std(ddof=1) / np.sqrt(len(x)) if len(x) > 1 else 0.0


def summarise(m, log):
    """Escape/relapse statistics over users whose feed the binge really moved (cocooned)."""
    c = m["cocooned"]
    r = dict(n=int(len(c)), cocooned=float(c.mean()), base=float(m["base_s"].mean()),
             peak=float(m["peak"].mean()), ttc=float(m["ttc"].mean()),
             reach50=float((m["ttc"] < log["cfg"].T1).mean()),
             st0=float(m["st0"].mean()), st1=float(m["st1"].mean()), st2=float(m["st2"].mean()),
             st3=float(m["st3"].mean()))
    for k in ["esc", "esc_H", "esc_act", "total_actions", "end2", "end3", "relapse", "rel_time", "util_ratio"]:
        r[k], r[k + "_ci"] = (float(v) for v in ci(m[k][c]))
    r["escaped"] = float(m["escaped"][c].mean())
    r["relapsed"] = float((m["rel_time"][c] < log["cfg"].T3).mean())
    return r


def run(cfg):
    log = sim.run(cfg)
    return log, sim.metrics(log)


# ============================================================ 1. calibration against KuaiRand
say("=== 1. Calibration (Phase 0 only, 20-exposure blocks) ===")
say("KuaiRand target: algorithmic top-tag share 0.312 vs random 0.215 (ratio 1.45); distinct 9.49 vs 11.87 (ratio 0.80)")
cal0 = sim.Config(n_users=U, T1=0, T2=0, T3=0, T0=30)
t = time.time()
rnd = sim.calibration_blocks(sim.run(replace(cal0, recommender="random")), 30)
say(f"random recommender: top share {rnd[0]:.3f}, distinct {rnd[1]:.2f}   ({time.time()-t:.1f}s)")
cal = []
for lam in [0.25, 0.4, 0.5, 0.75, 1.0]:
    x = sim.calibration_blocks(sim.run(replace(cal0, lam=lam)), 30)
    loss = abs(x[0] / rnd[0] - 1.45) / 1.45 + abs(x[1] / rnd[1] - 0.80) / 0.80
    cal.append(dict(lam=lam, top=x[0], distinct=x[1], r_top=x[0] / rnd[0], r_dist=x[1] / rnd[1], loss=loss))
    say(f"X-like lam={lam}: top {x[0]:.3f} (ratio {x[0]/rnd[0]:.2f}), distinct {x[1]:.2f} (ratio {x[1]/rnd[1]:.2f}), loss {loss:.3f}")
for name, kw in [("greedy", dict(recommender="greedy")), ("X no DPP", dict(dpp=False))]:
    x = sim.calibration_blocks(sim.run(replace(cal0, **kw)), 30)
    say(f"{name} (lam=0.5): top {x[0]:.3f} (ratio {x[0]/rnd[0]:.2f}), distinct {x[1]:.2f} (ratio {x[1]/rnd[1]:.2f})")
LAM = min(cal, key=lambda d: d["loss"])["lam"]
say(f"-> chosen lam = {LAM}")
OUT["calibration"] = dict(random=rnd, grid=cal, chosen=LAM)
BASE = sim.Config(n_users=U, lam=LAM)

# ============================================================ 2. main experiment: strategies x NI variant x history variant
say("\n=== 2. Escape strategies (X-like full pipeline) ===")
STRATS = ["S0", "S1", "S2", "S3", "S4", "S5"]
NAMES = dict(S0="S0 passive", S1="S1 not-interested", S2="S2 search 2/step", S3="S3 follow 10 new",
             S4="S4 personalisation off", S5="S5 combo S1+S2+S3")
main, curves = {}, {}
for hist in ["H1", "H2"]:
    for s in STRATS:
        for v in (["A", "B", "C"] if s in ("S1", "S5") else ["B"]):
            t = time.time()
            cfg = replace(BASE, strategy=s, ni_variant=v, log_skips=(hist == "H2"))
            log, m = run(cfg)
            key = f"{hist}|{s}|{v}"
            main[key] = summarise(m, log)
            curves[key] = dict(seed=m["seed_share"].mean(0), st=m["s_tilde"].mean(0))
            r = main[key]
            say(f"{key:10s} cocooned {r['cocooned']:.2f} peak {r['peak']:.2f} | escape steps {r['esc']:.1f}±{r['esc_ci']:.1f} "
                f"(escaped {r['escaped']:.0%}) actions {r['esc_act']:.1f}±{r['esc_act_ci']:.1f} "
                f"| end2 {r['end2']:.2f} end3 {r['end3']:.2f} relapse R {r['relapse']:.2f} relapsed {r['relapsed']:.0%} "
                f"| util {r['util_ratio']:.2f} | s~ {r['st0']:.2f}/{r['st1']:.2f}/{r['st2']:.2f}/{r['st3']:.2f} ({time.time()-t:.1f}s)")
OUT["main"] = main

# replication with two more RNG seeds (H1, NI variant B)
say("\n--- replication, seeds 1-2 (H1, variant B): escape steps / relapse R")
for s in STRATS:
    vals = []
    for sd in [1, 2]:
        log, m = run(replace(BASE, strategy=s, seed=sd))
        vals.append(summarise(m, log))
    say(f"{s}: esc " + ", ".join(f"{v['esc']:.1f}" for v in vals) + f" (seed0 {main['H1|'+s+'|B']['esc']:.1f}); "
        "R " + ", ".join(f"{v['relapse']:.2f}" for v in vals) + f" (seed0 {main['H1|'+s+'|B']['relapse']:.2f})")
    OUT.setdefault("replication", {})[s] = vals

# ============================================================ 3. ablation / sensitivity
say("\n=== 3. Ablation & sensitivity (H1; escape via S1-B and S2) ===")
ABL = [("X full", {}), ("no author-div", dict(author_div=False)), ("no OON 0.75", dict(oon=False)),
       ("no DPP", dict(dpp=False)), ("no DPP/AD/OON", dict(dpp=False, author_div=False, oon=False)),
       ("DPP theta 0.5", dict(theta=0.5)), ("DPP theta 0.8", dict(theta=0.8)),
       ("greedy p_eng", dict(recommender="greedy")), ("M = 50", dict(M=50)), ("M = 400", dict(M=400)),
       ("lam 0.25", dict(lam=0.25)), ("lam 1.0", dict(lam=1.0)),
       ("emb noise .15 (cos .87)", dict(emb_noise=0.15)), ("emb noise .8 (cos .57)", dict(emb_noise=0.8)),
       ("relapse h = 0", dict(relapse_h=0.0))]
abl = {}
for name, kw in ABL:
    t = time.time()
    row = {}
    for s in ["S1", "S2"]:
        log, m = run(replace(BASE, strategy=s, **kw))
        row[s] = summarise(m, log)
    abl[name] = row
    a, b = row["S1"], row["S2"]
    say(f"{name:24s} peak {a['peak']:.2f} reach>.5 {a['reach50']:.0%} ttc {a['ttc']:.1f} s~1 {a['st1']:.2f} | "
        f"S1 esc {a['esc']:.1f} ({a['escaped']:.0%}) R {a['relapse']:.2f} | S2 esc {b['esc']:.1f} ({b['escaped']:.0%}) R {b['relapse']:.2f} "
        f"({time.time()-t:.1f}s)")
OUT["ablation"] = abl

# ============================================================ figures
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e6e5e0"
SER = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#4a3aa7"]   # fixed categorical order
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "figure.dpi": 130})
c = BASE
bounds = np.cumsum([c.T0, c.T1, c.T2])
PH = ["P0 normal", "P1 binge", "P2 escape", "P3 relapse"]


def phase_shade(ax, ymax):
    for i, (a, b) in enumerate(zip(np.r_[0, bounds], np.r_[bounds, bounds[-1] + c.T3])):
        if i % 2 == 1:
            ax.axvspan(a, b, color="#f3f2ee", zorder=0)
        ax.text((a + b) / 2, ymax * 0.97, PH[i], ha="center", va="top", fontsize=8, color=INK2)


# Fig 1: seed share curves per strategy, H1 vs H2
fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
for ax, hist, title in zip(axes, ["H1", "H2"], ["H1: history = actions only (default)",
                                                  "H2: skipped impressions also enter FIFO"]):
    phase_shade(ax, 1.0)
    for i, s in enumerate(STRATS):
        y = curves[f"{hist}|{s}|B"]["seed"]
        ax.plot(y, color=SER[i], lw=2, label=NAMES[s])
        ax.text(len(y) + 1, y[-1], s, color=INK, fontsize=7, va="center")
    ax.set_title(title, fontsize=10, color=INK, loc="left")
    ax.set_xlabel("step (1 step = one refresh of 10 posts)")
    ax.set_ylim(0, 1)
axes[0].set_ylabel("seed-topic share of feed (rolling 30 posts)")
axes[1].legend(loc="center right", fontsize=7, frameon=False, bbox_to_anchor=(1.0, 0.62))
fig.suptitle("Seed-topic share over the four phases, by escape strategy (NI variant B, mean of 200 users)",
             fontsize=10, color=INK, x=0.01, ha="left")
fig.tight_layout()
fig.savefig("fig1_seed_share_curves.png")

# Fig 1b: NI variants for S1 and S5 (H1)
fig, ax = plt.subplots(figsize=(7, 3.6))
phase_shade(ax, 1.0)
for i, v in enumerate(["A", "B", "C"]):
    for s, ls in [("S1", "-"), ("S5", ":")]:
        ax.plot(curves[f"H1|{s}|{v}"]["seed"], color=SER[i], lw=2, ls=ls, label=f"{s}, NI variant {v}")
ax.set_ylim(0, 1)
ax.set_ylabel("seed-topic share (rolling 30 posts)")
ax.set_xlabel("step")
ax.legend(fontsize=7, frameon=False, loc="upper right", bbox_to_anchor=(1, 0.9))
ax.set_title("How far does one 'not interested' click generalise? A=author, B=topic, C=embedding",
             fontsize=10, color=INK, loc="left")
fig.tight_layout()
fig.savefig("fig1b_ni_variants.png")

# Fig 2: escape cost bars (steps and actions), H1 vs H2
labels, keys = [], []
for s in STRATS:
    for v in (["A", "B", "C"] if s in ("S1", "S5") else ["B"]):
        labels.append(s if s not in ("S1", "S5") else f"{s}-{v}")
        keys.append(f"{s}|{v}")
x = np.arange(len(labels))
fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))
for j, (metric, ylab) in enumerate([("esc", f"steps to escape (censored at {c.T2})"),
                                     ("esc_act", "explicit user actions until escape")]):
    ax = axes[j]
    for i, hist in enumerate(["H1", "H2"]):
        vals = [main[f"{hist}|{k}"][metric] for k in keys]
        errs = [main[f"{hist}|{k}"][metric + "_ci"] for k in keys]
        ax.bar(x + (i - 0.5) * 0.4, vals, 0.38, yerr=errs, color=SER[i], label=hist,
               error_kw=dict(ecolor=INK2, lw=0.8, capsize=2), edgecolor="white", linewidth=1)
        if metric == "esc":
            for xi, k in zip(x, keys):
                r = main[f"{hist}|{k}"]["escaped"]
                ax.text(xi + (i - 0.5) * 0.4, main[f"{hist}|{k}"]["esc"] + 2, f"{r:.0%}", ha="center",
                        fontsize=6, color=INK2, rotation=90)
    ax.set_xticks(x, labels, rotation=45, fontsize=8)
    ax.set_ylabel(ylab)
    ax.grid(axis="x", visible=False)
axes[0].set_title("Escape time (label = % of cocooned users escaped)", fontsize=10, color=INK, loc="left")
axes[1].set_title("Escape cost in user actions", fontsize=10, color=INK, loc="left")
axes[0].legend(frameon=False, fontsize=8, title="history variant", title_fontsize=7)
fig.tight_layout()
fig.savefig("fig2_escape_cost.png")

# Fig 3: ablation
names = [n for n, _ in ABL]
y = np.arange(len(names))[::-1]
fig, axes = plt.subplots(1, 3, figsize=(12, 4.6), sharey=True)
panels = [("peak seed share after binge", lambda r: r["S1"]["peak"], None),
          ("S1 (NI-B) steps to escape", lambda r: r["S1"]["esc"], lambda r: r["S1"]["esc_ci"]),
          ("S2 (search) steps to escape", lambda r: r["S2"]["esc"], lambda r: r["S2"]["esc_ci"])]
for ax, (title, f, fe) in zip(axes, panels):
    vals = [f(abl[n]) for n in names]
    errs = [fe(abl[n]) for n in names] if fe else None
    ax.barh(y, vals, 0.65, xerr=errs, color=[SER[0] if n != "X full" else SER[1] for n in names],
            error_kw=dict(ecolor=INK2, lw=0.8, capsize=2))
    ax.axvline(f(abl["X full"]), color=INK2, lw=0.8, ls="--")
    ax.set_title(title, fontsize=10, color=INK, loc="left")
    ax.grid(axis="y", visible=False)
    for yi, v in zip(y, vals):
        ax.text(v, yi, f" {v:.2f}" if v < 1.5 else f" {v:.0f}", va="center", fontsize=7, color=INK)
axes[0].set_yticks(y, names, fontsize=8)
fig.suptitle("Ablation / sensitivity (orange = X-like default; dashed line = default value)", fontsize=10,
             color=INK, x=0.01, ha="left")
fig.tight_layout()
fig.savefig("fig3_ablation.png")

# Fig 4: calibration
fig, axes = plt.subplots(1, 2, figsize=(8, 3))
lams = [d["lam"] for d in cal]
for ax, k, tgt, lab in [(axes[0], "r_top", 1.45, "top-topic share ratio (X-like / random)"),
                        (axes[1], "r_dist", 0.80, "distinct-topic ratio (X-like / random)")]:
    ax.plot(lams, [d[k] for d in cal], color=SER[0], lw=2, marker="o", ms=5)
    ax.axhline(tgt, color=SER[1], lw=1.5, ls="--")
    ax.text(lams[-1], tgt, " KuaiRand", color=INK2, fontsize=7, va="bottom", ha="right")
    ax.set_xlabel("learning sensitivity lambda")
    ax.set_title(lab, fontsize=9, color=INK, loc="left")
fig.tight_layout()
fig.savefig("fig4_calibration.png")

say(f"\nTotal runtime {time.time()-T_START:.0f}s")
json.dump(OUT, open("results.json", "w"), indent=1, default=float)
open("results.txt", "w").write("\n".join(LINES) + "\n")
