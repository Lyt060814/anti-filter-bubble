"""D6 mock-up of a user-side "viewpoint exposure report" (Zhao Dingcheng).

Usage: python -I -X utf8 design_mockup.py
Writes figures/exposure_report_mockup.{png,pdf} and results/exposure_report_mockup.csv / .meta.json.

Every number on the mock-up is one of three kinds, recorded in the CSV column `kind`:
  - illustrative: the example user's own feed (invented; no real user is shown);
  - formula: evidence needed for a verdict, from Proposition 6 (section 3.5) with the classifier and
    reference rates stated in the CSV; the group-label case reproduces section 5.3's 6,475 videos per arm;
  - simulation: expected effect of each action relative to doing nothing, from Xu Ruicong's calibrated
    main case (analysis/v6_simulation/results/calibrated_escape_summary.csv.gz; group family, supply .02,
    prior .15, fitted ratio, theta 2, end of the 1,000-exposure active phase). These are synthetic results,
    not measured effects on Kuaishou.
"""
import json
import math
import os
import subprocess
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
ESCAPE = os.path.join(ROOT, "analysis", "v6_simulation", "results", "calibrated_escape_summary.csv.gz")

# Example user (illustrative, invented)
USER = {"days": 30, "videos": 2200, "topic_videos": 46, "topic_share": 46 / 2200, "typical_topic_share": 0.016}

# Proposition 6 settings (section 3.5 / 5.3): one-sided a=.05, power .8, classifier alpha=.8, beta=.02, 2x odds
Z = 1.6449 + 0.8416
ALPHA, BETA, ODDS = 0.8, 0.02, 2.0
REFS = [("Any opposing narrative", 11 / 54, "Table 4.1: gender and relationships, 11/54 (DeepSeek)"),
        ("Group labels", 5 / 500, "Table 4.2: v2 reference, 5/500 (DeepSeek)")]

# Section 5.2: v2-classifier rerun of filtering in the main case, delta log m = -.1453 -> exp = .865 topic kept
FILTER_V2_TOPIC_KEPT = math.exp(-0.1453)

# Actions shown on the card: (label, strategy code, how it works / caveat)
ACTIONS = [("Delete these videos from my history", "S5", "lasts after you stop; needs accurate labels"),
           ("Hide these videos (filter)", "S6", "works only while on; keeps 86% with a weaker classifier"),
           ("\"Not interested\", if it acts as negative feedback", "S1a", "depends on how the platform uses it"),
           ("\"Not interested\", if it behaves as in our OneRec test", "S1b", "may not help at all"),
           ("Turn off personalisation", "S8", "removes only the personal layer"),
           ("Skip these videos quickly", "S2", ""),
           ("Watch other videos on the topic to the end", "S3", "ordinary videos barely offset it")]


def needed_n(p0, odds=ODDS):
    pu = odds * p0 / (1 - p0) / (1 + odds * p0 / (1 - p0))
    q0, qu = BETA + (ALPHA - BETA) * p0, BETA + (ALPHA - BETA) * pu
    return Z ** 2 * (q0 * (1 - q0) + qu * (1 - qu)) / ((ALPHA - BETA) ** 2 * (pu - p0) ** 2)


def action_effects():
    s = pd.read_csv(ESCAPE)
    m = s[(s.family == "group") & (s.scan == "main_grid") & (s.supply == 0.02) & (s.prior == 0.15) & (s.theta == 2.0)
          & (s.step == 1000) & (s.ratio.round(2) == 1.28)]
    assert m.strategy.nunique() == len(m) and len(m) >= 10, len(m)
    out = {}
    for _, r in m.iterrows():
        out[r.strategy] = {"delta_vs_control": r.delta_vs_control, "ci": r.delta_vs_control_ci,
                           "odds_factor": math.exp(r.delta_vs_control), "topic_change": math.expm1(r.delta_log_m)}
    return out


def strength(f):
    return "large" if f <= 0.35 else "medium" if f <= 0.55 else "small" if f <= 0.8 else "little or none"


def card(ax, x, y, w, h, color="#ffffff", edge="#d0d4da"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.012", fc=color, ec=edge, lw=1))


def draw(eff, rows, path_png, path_pdf):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    fig = plt.figure(figsize=(6.2, 11.2))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.patch.set_facecolor("#f3f4f6")
    ink, grey, accent, warn = "#1f2933", "#616e7c", "#2b6cb0", "#b7791f"

    ax.text(0.06, 0.965, "Your viewpoint exposure report", fontsize=14, weight="bold", color=ink)
    ax.text(0.06, 0.945, f"Topic: gender and relationships  ·  last {USER['days']} days  ·  MOCK-UP, example user",
            fontsize=8, color=grey)

    # 1. Interest
    card(ax, 0.05, 0.855, 0.90, 0.075)
    ax.text(0.08, 0.910, "1  How much of your feed is this topic", fontsize=10, weight="bold", color=ink)
    ax.text(0.08, 0.888, f"{USER['topic_videos']} of {USER['videos']:,} videos ({USER['topic_share']:.1%}).  "
            f"Typical user: {USER['typical_topic_share']:.1%}.", color=ink)
    ax.text(0.08, 0.867, "Watching a lot of one topic is interest, not a cocoon. Part 2 is about what you see within it.",
            fontsize=7.5, color=grey)

    # 2. Within-topic narratives
    card(ax, 0.05, 0.597, 0.90, 0.243)
    ax.text(0.08, 0.818, "2  Within the topic: are you seeing one side more?", fontsize=10, weight="bold", color=ink)
    ax.text(0.08, 0.798, "Compared with the same topic in the non-personalised feed.", fontsize=7.5, color=grey)
    yy = 0.765
    for r in rows:
        ax.text(0.08, yy, r["narrative"], weight="bold", color=ink)
        ax.add_patch(FancyBboxPatch((0.62, yy - 0.010), 0.30, 0.026, boxstyle="round,pad=0.003,rounding_size=0.01",
                                    fc="#fdf3e1", ec=warn, lw=0.8))
        ax.text(0.77, yy + 0.003, "Not enough evidence yet", ha="center", va="center", fontsize=8, color=warn, weight="bold")
        ax.text(0.08, yy - 0.022, f"To tell a 2x difference from chance needs about {r['needed']:,.0f} videos on this topic;",
                fontsize=7.5, color=ink)
        frac = min(1.0, USER["topic_videos"] / r["needed"])
        ax.barh(yy - 0.044, 0.84, left=0.08, height=0.008, color="#e4e7eb")
        ax.barh(yy - 0.044, max(0.004, 0.84 * frac), left=0.08, height=0.008, color=accent)
        ax.text(0.08, yy - 0.062, f"you have seen {USER['topic_videos']} ({frac:.1%} of what is needed).", fontsize=7.5, color=ink)
        yy -= 0.083
    ax.text(0.08, 0.607, "We show a verdict only when the evidence is sufficient. For most users and rare narratives it never is.",
            fontsize=7.5, color=grey)

    # 3. Actions
    card(ax, 0.05, 0.200, 0.90, 0.385)
    ax.text(0.08, 0.563, "3  What you can do, and what it may cost", fontsize=10, weight="bold", color=ink)
    ax.text(0.08, 0.543, "Expected change in this narrative's share vs doing nothing (simulation, not measured on the app).",
            fontsize=7.5, color=grey)
    ax.text(0.62, 0.520, "effect", fontsize=7.5, color=grey, weight="bold")
    ax.text(0.80, 0.520, "topic kept", fontsize=7.5, color=grey, weight="bold")
    yy = 0.497
    for label, code, note in ACTIONS:
        e = eff[code]
        ax.text(0.08, yy, label, fontsize=8, color=ink)
        if note:
            ax.text(0.08, yy - 0.016, note, fontsize=7, color=grey, style="italic")
        bar = max(0.0, 1 - e["odds_factor"])
        ax.barh(yy - 0.004, 0.15, left=0.62, height=0.010, color="#e4e7eb")
        ax.barh(yy - 0.004, 0.15 * bar, left=0.62, height=0.010, color=accent)
        ax.text(0.62, yy - 0.020, strength(e["odds_factor"]), fontsize=7, color=ink)
        ax.text(0.80, yy - 0.004, f"{1 + e['topic_change']:.0%}", fontsize=8, color=ink, va="center")
        yy -= 0.040
    ax.text(0.08, yy - 0.002, "Leave the topic entirely: the narrative disappears, and so does everything else on the topic.",
            fontsize=7.5, color=ink)

    # 4. Limits
    card(ax, 0.05, 0.040, 0.90, 0.148, color="#fafbfc")
    ax.text(0.08, 0.168, "4  What this report does not say", fontsize=10, weight="bold", color=ink)
    lines = ["It does not judge which view is right, or label any view as harmful.",
             "It does not infer what you believe; it describes only what you were shown.",
             "It does not claim the platform intends any pattern.",
             "Comparing with the non-personalised feed shows only your personal layer;",
             "    a skew built into the platform's overall ranking would not appear here.",
             "Labels come from a language model and can be wrong."]
    for i, t in enumerate(lines):
        ax.text(0.08, 0.146 - i * 0.018, ("• " if not t.startswith("    ") else "  ") + t.strip(), fontsize=7.5, color=ink)

    fig.savefig(path_png, dpi=300, facecolor=fig.get_facecolor())
    fig.savefig(path_pdf, facecolor=fig.get_facecolor())
    plt.close(fig)


def main():
    eff = action_effects()
    rows = [{"narrative": name, "reference_share": p0, "needed": needed_n(p0), "source": src} for name, p0, src in REFS]
    os.makedirs(os.path.join(HERE, "figures"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    draw(eff, rows, os.path.join(HERE, "figures", "exposure_report_mockup.png"), os.path.join(HERE, "figures", "exposure_report_mockup.pdf"))
    recs = [{"item": k, "value": v, "kind": "illustrative", "source": "invented example user"} for k, v in USER.items()]
    for r in rows:
        recs.append({"item": f"needed_videos_per_arm: {r['narrative']}", "value": round(r["needed"]), "kind": "formula",
                     "source": f"Proposition 6, alpha {ALPHA}, beta {BETA}, odds x{ODDS}, a .05, power .8; reference {r['source']}"})
    for label, code, _ in ACTIONS:
        e = eff[code]
        recs.append({"item": f"{code} odds factor vs S0: {label}", "value": round(e["odds_factor"], 4), "kind": "simulation",
                     "source": f"delta_vs_control {e['delta_vs_control']:.4f} (95% half-width {e['ci']:.4f})"})
        recs.append({"item": f"{code} topic exposure kept", "value": round(1 + e["topic_change"], 4), "kind": "simulation",
                     "source": "exp(delta_log_m), main case"})
    recs.append({"item": "S6 topic exposure kept with the v2 open-model classifier", "value": round(FILTER_V2_TOPIC_KEPT, 4),
                 "kind": "simulation", "source": "section 5.2: v2-classifier main-case rerun, delta log m -.1453"})
    pd.DataFrame(recs).to_csv(os.path.join(HERE, "results", "exposure_report_mockup.csv"), index=False, encoding="utf-8")
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=HERE).stdout.strip()
    except OSError:
        commit = None
    meta = {"script": "analysis/v6_annotation/design_mockup.py", "commit": commit, "date": time.strftime("%Y-%m-%d"),
            "inputs": ["analysis/v6_simulation/results/calibrated_escape_summary.csv.gz"],
            "simulation_case": "group family, supply .02, prior .15, topic target .70, attribute target 1.13, fitted ratio 1.28, decay .0002, main_grid, theta 2, step 1000",
            "evidence": "mock-up: example-user numbers are invented; evidence thresholds are formula results; action effects are synthetic simulation results",
            "check_group_label_needed_vs_section_5_3": {"this_script": round(rows[1]["needed"]), "section_5_3": 6475}}
    json.dump(meta, open(os.path.join(HERE, "results", "exposure_report_mockup.meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(pd.DataFrame(recs).to_string())


if __name__ == "__main__":
    main()
