"""Build every number used in the report: results.json, ../../generated/numbers.tex and table bodies.

CONSTRUCTED DATA for an idealised teaching report (see ../../README.md). Not measurements.
Run:  python3 study.py        (about three minutes)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.stats import norm

import model as M

HERE = Path(__file__).resolve().parent
GEN = HERE.parent.parent / "generated"
GEN.mkdir(exist_ok=True)
rng = np.random.default_rng(20261115)
R = {}        # everything, for the plotting script
MAC = {}      # LaTeX macros


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def mac(name, value, fmt="{:.2f}"):
    MAC[name] = fmt.format(value) if not isinstance(value, str) else value


def signed(x, nd=2):
    return ("$+$" if x >= 0 else "$-$") + f"{abs(x):.{nd}f}"


# =====================================================================================
# 1. Data and narrative landscape (RQ1)
# =====================================================================================
DOMAINS = ["Gender \\& marriage", "Body \\& appearance", "Family \\& generations", "Life choices", "Consumption \\& money"]
DOM_SHORT = ["Gender & marriage", "Body & appearance", "Family & generations", "Life choices", "Consumption & money"]
N_SAMPLE = 20000
ISSUE_N = [480, 380, 320, 220, 180]
# opposing narratives by type: one right way, binary opposition, anxiety, group label
TYPES = ["One right way", "Binary opposition", "Anxiety appeal", "Group label"]
TYPE_N = [[20, 38, 27, 30], [19, 6, 46, 9], [11, 7, 6, 5], [21, 12, 5, 2], [6, 8, 9, 4]]
AMPLIF = [1.49, 1.41, 1.18, 1.27, 1.36]   # exposure odds / supply odds of opposing narratives
landscape = []
for d, n, tn, amp in zip(DOM_SHORT, ISSUE_N, TYPE_N, AMPLIF):
    k = sum(tn)
    lo, hi = wilson(k, n)
    landscape.append(dict(domain=d, n=n, share_all=n / N_SAMPLE, opp=k, opp_share=k / n, lo=lo, hi=hi, types=tn, amp=amp))
tot_issue, tot_opp = sum(ISSUE_N), sum(sum(t) for t in TYPE_N)
R["landscape"] = dict(rows=landscape, n_sample=N_SAMPLE, total_issue=tot_issue, total_opp=tot_opp,
                      types=TYPES, type_tot=[sum(t[i] for t in TYPE_N) for i in range(4)])
mac("IssueShare", 100 * tot_issue / N_SAMPLE, "{:.1f}")
mac("OppShare", 100 * tot_opp / tot_issue, "{:.1f}")
lo, hi = wilson(tot_opp, tot_issue)
mac("OppShareLo", 100 * lo, "{:.1f}")
mac("OppShareHi", 100 * hi, "{:.1f}")

rows = []
for r_, dname in zip(landscape, DOMAINS):
    t = r_["types"]
    rows.append(f"{dname} & {r_['n']} & {100*r_['share_all']:.1f} & {100*r_['opp_share']:.1f} "
                f"{{\\footnotesize({100*r_['lo']:.0f}--{100*r_['hi']:.0f})}} & {t[0]} & {t[1]} & {t[2]} & {t[3]} & {r_['amp']:.2f}$\\times$ \\\\")
tt = R["landscape"]["type_tot"]
rows.append("\\midrule")
rows.append(f"All five domains & 1{{,}}580 & {100*tot_issue/N_SAMPLE:.1f} & {100*tot_opp/tot_issue:.1f} "
            f"{{\\footnotesize({100*lo:.0f}--{100*hi:.0f})}} & {tt[0]} & {tt[1]} & {tt[2]} & {tt[3]} & 1.38$\\times$ \\\\")
(GEN / "tab_landscape_body.tex").write_text("\n".join(rows) + "\n")

# Engagement: issue corpus, impression level. rates for non-opposing issue videos, and odds ratios by type.
CORPUS_VIDEOS, CORPUS_IMPR = 684_210, 5_912_400
BASE = dict(finish=0.376, like=0.032, comment=0.0033, share=0.0036, ni=0.0012)
OR = {  # adjusted odds ratios vs non-opposing issue videos of the same domain and length
    "All opposing": dict(finish=1.19, like=1.22, comment=1.85, share=1.33, ni=1.74),
    "One right way": dict(finish=1.11, like=1.17, comment=1.52, share=1.41, ni=1.38),
    "Binary opposition": dict(finish=1.16, like=1.14, comment=1.93, share=1.22, ni=1.62),
    "Anxiety appeal": dict(finish=1.21, like=1.25, comment=1.47, share=1.48, ni=1.71),
    "Group label": dict(finish=1.29, like=1.33, comment=2.41, share=1.19, ni=2.36),
}
opp_impr = CORPUS_IMPR * tot_opp / tot_issue
n_by = {"All opposing": opp_impr}
for i, t in enumerate(TYPES):
    n_by[t] = opp_impr * tt[i] / tot_opp
eng = {}
for t, d in OR.items():
    eng[t] = {}
    for k, o in d.items():
        p0 = BASE[k]
        p1 = o * p0 / (1 - p0 + o * p0)
        n1, n0 = n_by[t], CORPUS_IMPR - opp_impr
        se = np.sqrt(1 / (n1 * p1) + 1 / (n1 * (1 - p1)) + 1 / (n0 * p0) + 1 / (n0 * (1 - p0))) * 2.2  # user-clustered
        eng[t][k] = dict(or_=o, lo=float(np.exp(np.log(o) - 1.96 * se)), hi=float(np.exp(np.log(o) + 1.96 * se)), rate=float(p1))
R["engagement"] = dict(base=BASE, by=eng, corpus_videos=CORPUS_VIDEOS, corpus_impr=CORPUS_IMPR)

# Label quality (validation sample of 1,200 videos)
R["labels"] = dict(n=1200, rows=[
    dict(task="On one of the five issues", k_open=0.81, k_ref=0.88, prec=0.90, rec=0.87),
    dict(task="Opposing narrative (yes/no)", k_open=0.74, k_ref=0.82, prec=0.81, rec=0.83),
    dict(task="Narrative type (four-way)", k_open=0.69, k_ref=0.78, prec=None, rec=None),
    dict(task="Gender group label (yes/no)", k_open=0.78, k_ref=0.86, prec=0.84, rec=0.79),
])
ALPHA, BETA = 0.79, 0.010     # recall and false-positive rate of the group-label classifier
prec_check = ALPHA * M.P_BAR / (ALPHA * M.P_BAR + BETA * (1 - M.P_BAR))
mac("ClfPrecision", prec_check, "{:.2f}")

# =====================================================================================
# 2. Case study in the logs
# =====================================================================================
CASE_VIDEOS, CASE_IMPR, USERS, IMPR = 212_480, 1_771_300, 160_412, 75_316_000
R["case"] = dict(videos=CASE_VIDEOS, impr=CASE_IMPR, users=USERS, impr_all=IMPR, p_sup=M.P_SUP, p_bar=M.P_BAR,
                 platform_layer=M.PLATFORM_LAYER)
mac("PlatformLayer", M.PLATFORM_LAYER)
mac("PlatformOdds", np.exp(M.PLATFORM_LAYER))

# population of heavy issue viewers: steady states of the model plus sampling noise
N_HEAVY = 9412
phis = np.clip(rng.normal(0.62, 0.22, 400), 0.36, 1.3)
thetas = rng.normal(-0.05, 1.5, 400)
grid = [M.mean_field(p, t, iters=1500, damp=0.04) for p, t in zip(phis, thetas)]
idx = rng.integers(0, 400, N_HEAVY)
m_true = np.array([grid[i][0] for i in idx]) * np.exp(rng.normal(-0.75, 0.55, N_HEAVY))
m_true = np.where(m_true < 0.035, 0.035 * np.exp(np.abs(rng.normal(0, 0.6, N_HEAVY))), m_true)
m_true = np.clip(m_true, 0.035, 0.9)
scale = np.clip(m_true / 0.29, 0, 1) ** 0.8          # less topic volume, less room for a personal skew
V_true = np.array([grid[i][1] for i in idx]) * scale
n_issue = np.maximum(150, (rng.lognormal(np.log(420), 0.55, N_HEAVY) * (0.6 + m_true / 0.2)).astype(int))
p_true = M.expit(M.logit(M.P_BAR) + V_true)
k_obs = rng.binomial(n_issue, p_true)
prior = 12.0   # empirical-Bayes shrinkage towards the platform share
p_hat = (k_obs + prior * M.P_BAR) / (n_issue + prior)
V_hat = M.logit(p_hat) - M.logit(M.P_BAR)
ent = 2.62 - 1.9 * m_true + rng.normal(0, 0.28, N_HEAVY)      # category entropy of the feed (nats)
R["funnel"] = dict(m=m_true.round(4).tolist(), V=V_hat.round(3).tolist(), n_heavy=N_HEAVY,
                   sd=float(V_hat.std()), frac_hi=float((V_hat > np.log(2)).mean()), frac_lo=float((V_hat < -np.log(2)).mean()),
                   rho_m=float(np.corrcoef(m_true, V_hat)[0, 1]), rho_ent=float(np.corrcoef(ent, V_hat)[0, 1]),
                   rho_ent_m=float(np.corrcoef(ent, m_true)[0, 1]),
                   top_decile_V=float(np.quantile(V_hat, 0.9)),
                   top_decile_mean_p=float(p_hat[V_hat >= np.quantile(V_hat, 0.9)].mean()))
mac("NHeavy", f"{N_HEAVY:,}".replace(",", "{,}"))
mac("FunnelSD", R["funnel"]["sd"])
mac("FunnelHi", 100 * R["funnel"]["frac_hi"], "{:.1f}")
mac("FunnelLo", 100 * R["funnel"]["frac_lo"], "{:.1f}")
mac("RhoMV", R["funnel"]["rho_m"])
mac("RhoEntV", R["funnel"]["rho_ent"])
mac("RhoEntM", R["funnel"]["rho_ent_m"])
mac("TopDecileShare", 100 * R["funnel"]["top_decile_mean_p"], "{:.1f}")
mac("TopDecileV", M.logit(R["funnel"]["top_decile_mean_p"]) - M.logit(M.P_BAR))
mac("TopDecileTotalOdds", np.exp(M.logit(R["funnel"]["top_decile_mean_p"]) - M.logit(M.P_SUP)), "{:.1f}")
mac("TopDecileLayerShare", 100 * M.PLATFORM_LAYER / (M.logit(R["funnel"]["top_decile_mean_p"]) - M.logit(M.P_SUP)), "{:.0f}")

# observational dose-response: A videos finished among the previous 200 -> skew of the next issue impressions
BINS = [("0", 0, 0.0), ("1--2", 1.4, 0.0), ("3--5", 3.8, 0.0), ("6--10", 7.6, 0.0), ("11--20", 14.2, 0.0), ("$>$20", 26.5, 0.0)]
N_BIN = [1_204_300, 312_800, 141_600, 71_900, 30_400, 10_300]
obs = []
for (lab, k, _), n in zip(BINS, N_BIN):
    v = 0.88 * M.probe(k, "narrative")[1] - 0.035 + rng.normal(0, 0.012)
    p = M.expit(M.logit(M.P_BAR) + v)
    se = 2.4 / np.sqrt(n * p * (1 - p))
    obs.append(dict(bin=lab.replace("--", "–").replace("$>$", ">"), k=k, V=float(v), lo=float(v - 1.96 * se), hi=float(v + 1.96 * se), n=n))
R["obs_dose"] = obs

# =====================================================================================
# 3. Probing the recommender
# =====================================================================================
N_PROBE = 200
KS = [2, 5, 10, 20, 40]
probe = dict(k=KS, topic=[], narr=[], narr_from_other=[], ni_topic=[], ni_narr=[])


def measured(x, sd_rel=0.40, sd_abs=0.24):
    u = x * rng.lognormal(-sd_rel ** 2 / 2, sd_rel, N_PROBE) + rng.normal(0, sd_abs, N_PROBE)
    return dict(mean=float(u.mean()), lo=float(u.mean() - 1.96 * u.std(ddof=1) / np.sqrt(N_PROBE)),
                hi=float(u.mean() + 1.96 * u.std(ddof=1) / np.sqrt(N_PROBE)), pos=float((u > 0).mean()), model=float(x))


for k in KS:
    probe["topic"].append(measured(M.probe(k, "issue")[0]))
    probe["narr"].append(measured(M.probe(k, "narrative")[1]))
    probe["narr_from_other"].append(measured(M.probe(k, "issue")[1], sd_abs=0.20))
    t_ni, n_ni = M.probe(k, "narrative", "ni")
    probe["ni_topic"].append(measured(t_ni))
    probe["ni_narr"].append(measured(n_ni))
null = rng.normal(0.006, 0.058, 200)
probe["null"] = dict(mean=float(null.mean()), sd=float(null.std(ddof=1)), q975=float(np.quantile(np.abs(null), 0.95)), draws=null.round(3).tolist())
# the same ten videos under four history fields (k = 10)
t10, n10 = M.probe(10, "narrative")
fields = [("Watched to the end", 1.0), ("Liked", 1.12), ("``Not interested''", None), ("Unlabelled extra field", 0.36)]
probe["fields"] = []
for name, wgt in fields:
    if wgt is None:
        tt_, nn_ = M.probe(10, "narrative", "ni")
    else:
        tt_, nn_ = t10 * wgt, n10 * wgt
    probe["fields"].append(dict(field=name.replace("``", "“").replace("''", "”"), topic=measured(tt_), narr=measured(nn_)))
i10 = KS.index(10)
probe["fields"][0]["narr"] = probe["narr"][i10]          # same condition as the dose-response point at k = 10
probe["fields"][2]["topic"], probe["fields"][2]["narr"] = probe["ni_topic"][i10], probe["ni_narr"][i10]
R["probe"] = probe
mac("ProbeTopic", probe["topic"][i10]["mean"])
mac("ProbeTopicLo", probe["topic"][i10]["lo"])
mac("ProbeTopicHi", probe["topic"][i10]["hi"])
mac("ProbeNarr", probe["narr"][i10]["mean"])
mac("ProbeNarrLo", probe["narr"][i10]["lo"])
mac("ProbeNarrHi", probe["narr"][i10]["hi"])
mac("ProbeNarrPos", 100 * probe["narr"][i10]["pos"], "{:.0f}")
mac("ProbeTopicPos", 100 * probe["topic"][i10]["pos"], "{:.0f}")
mac("ProbeRatio", probe["narr"][i10]["mean"] / probe["topic"][i10]["mean"])
mac("ProbeOther", probe["narr_from_other"][i10]["mean"])
mac("NullMean", probe["null"]["mean"])
mac("NullSD", probe["null"]["sd"])
mac("NITopic", probe["ni_topic"][i10]["mean"])
mac("NINarr", probe["ni_narr"][i10]["mean"])
mac("NITopicPos", 100 * probe["ni_topic"][i10]["pos"], "{:.0f}")
mac("NIRel", probe["ni_narr"][i10]["mean"] / probe["narr"][i10]["mean"])
mac("NINarrPos", 100 * probe["ni_narr"][i10]["pos"], "{:.0f}")
mac("FieldLikeNarr", probe["fields"][1]["narr"]["mean"])
mac("FieldExtraNarr", probe["fields"][3]["narr"]["mean"])
mac("FieldExtraTopic", probe["fields"][3]["topic"]["mean"])
mac("ProbeNarrTwenty", probe["narr"][KS.index(20)]["mean"])
mac("ProbeNarrForty", probe["narr"][KS.index(40)]["mean"])
mac("ProbeTopicForty", probe["topic"][KS.index(40)]["mean"])
mac("ObsTop", obs[-1]["V"])
mac("ObsZero", obs[0]["V"])
mac("GainT", M.G_T, "{:.1f}")
mac("GainA", M.G_A, "{:.1f}")

# =====================================================================================
# 4. Formation
# =====================================================================================
N_FORM, SEEDS = 16000, 400
USERS_SIM = [("fan_strong", 0.8, 2.0, "Topic fan, strong preference"),
             ("fan_mild", 0.8, 1.0, "Topic fan, mild preference"),
             ("fan_none", 0.8, 0.0, "Topic fan, no preference"),
             ("fan_averse", 0.8, -1.0, "Topic fan, averse"),
             ("casual_strong", 0.0, 2.0, "Casual viewer, strong preference")]
form = {}
for key, phi, th, label in USERS_SIM:
    r = M.simulate(phi, th, n_form=N_FORM, seeds=SEEDS, rng_seed=11, record_every=50)
    V, m = r["V"], r["m"]
    form[key] = dict(label=label, phi=phi, theta=th, t=r["t"].tolist(), V=V.mean(1).tolist(),
                     V_lo=np.quantile(V, 0.1, axis=1).tolist(), V_hi=np.quantile(V, 0.9, axis=1).tolist(),
                     m=m.mean(1).tolist(), V_end=float(V[-20:].mean()), m_end=float(m[-20:].mean()),
                     V_end_se=float(V[-20:].mean(0).std(ddof=1) / np.sqrt(SEEDS)))
    print("formation", key, round(form[key]["V_end"], 3), round(form[key]["m_end"], 3))
R["formation"] = dict(users=form, n_form=N_FORM, seeds=SEEDS, days=N_FORM / M.VIDEOS_PER_DAY)
for key, name in [("fan_strong", "Strong"), ("fan_mild", "Mild"), ("fan_none", "None"), ("fan_averse", "Averse"), ("casual_strong", "Casual")]:
    mac("V" + name, form[key]["V_end"])
    mac("M" + name, 100 * form[key]["m_end"], "{:.0f}")
    mac("Odds" + name, np.exp(form[key]["V_end"]), "{:.1f}")
mac("ShareStrong", 100 * M.expit(M.logit(M.P_BAR) + form["fan_strong"]["V_end"]), "{:.1f}")
mac("TotalStrong", form["fan_strong"]["V_end"] + M.PLATFORM_LAYER)
mac("TotalOddsStrong", np.exp(form["fan_strong"]["V_end"] + M.PLATFORM_LAYER), "{:.1f}")
mac("FormDays", N_FORM / M.VIDEOS_PER_DAY, "{:.0f}")
vs = np.array(form["fan_strong"]["V"])
half_t = np.array(form["fan_strong"]["t"])[np.argmax(vs >= 0.5 * form["fan_strong"]["V_end"])]
mac("FormHalfDays", half_t / M.VIDEOS_PER_DAY, "{:.0f}")
mcas = form["casual_strong"]["m_end"]
mac("MCasualOne", 100 * mcas, "{:.1f}")

# sweep over the narrative response of the recommender (c/t ratio) and over the preference
ratios = np.round(np.arange(0.0, 1.21, 0.1), 2)
sweep = dict(ratio=ratios.tolist(), strong=[], mild=[])
base_ratio = M.NARR_RESP / M.TOPIC_RESP
for rr in ratios:
    for key, th in (("strong", 2.0), ("mild", 1.0)):
        r = M.simulate(0.8, th, n_form=N_FORM, seeds=150, rng_seed=5, record_every=200, gain_scale=rr / base_ratio)
        sweep[key].append(float(r["V"][-10:].mean()))
sweep["measured"] = base_ratio
thetas_s = np.round(np.arange(-1.5, 2.51, 0.5), 2)
sweep["theta"] = thetas_s.tolist()
sweep["V_theta"] = [float(M.simulate(0.8, th, n_form=N_FORM, seeds=150, rng_seed=6, record_every=200)["V"][-10:].mean()) for th in thetas_s]
R["sweep"] = sweep
mac("SweepHalf", sweep["strong"][list(ratios).index(0.3)])
mac("SweepZero", sweep["strong"][0])
mac("SweepOne", sweep["strong"][list(ratios).index(1.0)])

# =====================================================================================
# 5. Detection
# =====================================================================================
Vs = np.round(np.arange(0.2, 2.01, 0.05), 2)
clfs = {"Perfect labels": (1.0, 0.0), "Validated classifier": (ALPHA, BETA), "Keyword list": (0.45, 0.01)}
det = dict(V=Vs.tolist(), curves={k: [float(M.detection_n(v, alpha=a, beta=b)) for v in Vs] for k, (a, b) in clfs.items()})
ISSUE_PER_DAY_AVG = M.VIDEOS_PER_DAY * M.M0
ISSUE_PER_DAY_FAN = M.VIDEOS_PER_DAY * form["fan_strong"]["m_end"]
det["per_day_avg"], det["per_day_fan"] = ISSUE_PER_DAY_AVG, ISSUE_PER_DAY_FAN
det["clfs"] = {k: list(v) for k, v in clfs.items()}
R["detection"] = det
for name, v in [("Low", 0.3), ("Mid", 0.5), ("Double", float(np.log(2))), ("Strong", form["fan_strong"]["V_end"]), ("High", 1.5)]:
    n_ = M.detection_n(v, alpha=ALPHA, beta=BETA)
    mac("DetN" + name, f"{int(round(n_, -1)):,}".replace(",", "{,}"))
    mac("DetDaysAvg" + name, n_ / ISSUE_PER_DAY_AVG, "{:.0f}")
    mac("DetMonthsAvg" + name, n_ / ISSUE_PER_DAY_AVG / 30.4, "{:.1f}")
    mac("DetDaysFan" + name, n_ / ISSUE_PER_DAY_FAN, "{:.0f}")
mac("DetNPerfectDouble", f"{int(round(M.detection_n(np.log(2)), -1)):,}")
mac("DetNKeywordDouble", f"{int(round(M.detection_n(np.log(2), alpha=0.45, beta=0.01), -1)):,}".replace(",", "{,}"))
mac("IssuePerDayAvg", ISSUE_PER_DAY_AVG, "{:.1f}")
mac("IssuePerDayFan", ISSUE_PER_DAY_FAN, "{:.0f}")
mac("DetRefDaysDouble", M.detection_n(np.log(2), alpha=ALPHA, beta=BETA) / ISSUE_PER_DAY_AVG, "{:.0f}")
# worked example for a doubling, and the one-sample case with a published reference
_pu = float(M.expit(M.logit(M.P_BAR) + np.log(2)))
mac("ExPu", 100 * _pu, "{:.1f}")
mac("ExQzero", BETA + (ALPHA - BETA) * M.P_BAR, "{:.3f}")
mac("ExQu", BETA + (ALPHA - BETA) * _pu, "{:.3f}")
mac("ExGapOneIn", 1 / (_pu - M.P_BAR), "{:.0f}")
_nk = M.detection_n(np.log(2), alpha=ALPHA, beta=BETA, known_reference=True)
mac("DetNKnownDouble", f"{int(round(_nk, -1)):,}")
mac("DetDaysFanKnown", _nk / ISSUE_PER_DAY_FAN, "{:.0f}")

# =====================================================================================
# 6. Escape
# =====================================================================================
N_ACT, N_AFTER = 3000, 4000
esc = {}
for s in M.STRATEGIES:
    r = M.simulate(0.8, 2.0, n_form=N_FORM, n_act=N_ACT, n_after=N_AFTER, strategy=s, seeds=SEEDS, rng_seed=11, record_every=25)
    t, V, m = r["t"], r["V"].mean(1), r["m"].mean(1)
    pre = (t >= N_FORM - 1000) & (t < N_FORM)
    early = (t >= N_FORM + 400) & (t < N_FORM + 600)
    late = (t >= N_FORM + N_ACT - 500) & (t < N_FORM + N_ACT)
    aft = (t >= N_FORM + N_ACT + 900) & (t < N_FORM + N_ACT + 1100)
    end = t >= N_FORM + N_ACT + N_AFTER - 500
    V0, m0 = V[pre].mean(), m[pre].mean()
    sel = t >= N_FORM - 1500
    # rebound: videos after stopping until half of the gap to the pre-action level is closed
    post = t >= N_FORM + N_ACT
    gap0 = V0 - V[post][0:8].mean() if s not in M.FILTERS and s != "S8" else V0 - V[(t >= N_FORM + N_ACT + 25) & (t < N_FORM + N_ACT + 225)].mean()
    tp, Vp = t[post] - (N_FORM + N_ACT), V[post]
    half = None
    if gap0 > 0.08:
        sm = np.convolve(Vp, np.ones(9) / 9, mode="same")
        hit = np.where(sm >= V0 - gap0 / 2)[0]
        half = int(tp[hit[0]]) if len(hit) else None
    esc[s] = dict(name=M.STRATEGIES[s]["name"], family=M.STRATEGIES[s]["family"], t=(t[sel] - N_FORM).tolist(),
                  V=V[sel].tolist(), m=m[sel].tolist(), V0=float(V0), m0=float(m0),
                  dV_early=float(V[early].mean() - V0), dV_late=float(V[late].mean() - V0),
                  total_late=float(V[late].mean() + M.PLATFORM_LAYER),
                  topic_kept=float(m[late].mean() / m0), dV_after=float(V[aft].mean() - V0), dV_end=float(V[end].mean() - V0),
                  actions=float(r["actions"].mean() / (N_ACT / 1000)), half=half)
    print("escape", s, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in esc[s].items() if k not in ("t", "V", "m", "name")})
R["escape"] = dict(strategies=esc, n_act=N_ACT, n_after=N_AFTER)
mac("ActDays", N_ACT / M.VIDEOS_PER_DAY, "{:.0f}")
for s, e in esc.items():
    mac("Esc" + s.replace("S", "S").replace("0", "Zero").replace("1", "One").replace("2", "Two").replace("3", "Three").replace("4", "Four")
        .replace("5", "Five").replace("6", "Six").replace("7", "Seven").replace("8", "Eight").replace("9", "Nine"), signed(e["dV_late"]))

FAMILY_LABEL = dict(none="--", implicit="Viewing behaviour", explicit="Explicit feedback", history="History editing",
                    platform="Platform setting", filter="External filter")
rows, last = [], None
for s, e in esc.items():
    if e["family"] != last and last is not None:
        rows.append("\\addlinespace[2pt]")
    last = e["family"]
    eff = "one-off" if s in ("S6", "S7") else ("setting" if s in ("S8", "S9", "S10", "S11") else (f"{e['actions']:.0f}" if e["actions"] >= 0.5 else "none"))
    half = "--" if s == "S0" else ("$>$4{,}000" if e["half"] is None and e["dV_after"] < -0.05 else ("--" if e["half"] is None else f"{int(round(e['half'], -1)):,}".replace(",", "{,}")))
    rows.append(f"{s} & {e['name']} & {signed(e['dV_early'])} & {signed(e['dV_late'])} & {signed(e['total_late'])} & "
                f"{100*e['topic_kept']:.0f}\\% & {eff} & {signed(e['dV_after'])} & {half} \\\\")
(GEN / "tab_escape_body.tex").write_text("\n".join(rows) + "\n")

# appendix tables
rows = []
for i, k in enumerate(KS):
    def cell(d):
        return f"{signed(d['mean'])} {{\\footnotesize[{d['lo']:.2f}, {d['hi']:.2f}]}}"
    rows.append(f"{k} & {cell(probe['topic'][i])} & {cell(probe['narr'][i])} & {cell(probe['narr_from_other'][i])} & {cell(probe['ni_narr'][i])} \\\\")
(GEN / "tab_probe_body.tex").write_text("\n".join(rows) + "\n")
(GEN / "tab_theta_body.tex").write_text(
    " & ".join(["$\\theta$"] + [f"{t:+.1f}".replace("-", "$-$").replace("+", "$+$") for t in sweep["theta"]]) + " \\\\\n\\midrule\n" +
    " & ".join(["$V$ after 89 days"] + [signed(v) for v in sweep["V_theta"]]) + " \\\\\n")
# =====================================================================================
(HERE / "results.json").write_text(json.dumps(R))
lines = ["% generated by figures/src/study.py -- do not edit"]
for k, v in MAC.items():
    lines.append(f"\\newcommand{{\\n{k}}}{{{v}}}")
(GEN / "numbers.tex").write_text("\n".join(lines) + "\n")
print(len(MAC), "macros written")
