"""Scenario model behind the report's figures and tables.

Everything in this directory is CONSTRUCTED for an idealised teaching report (see the
disclaimer on the report's first page and in ../../README.md). Nothing here is a measurement
of any dataset, model or platform.

The model: a feed over four groups of videos
    A  issue videos carrying the target narrative (gender group label)
    B  other issue videos
    C  issue videos that explicitly rebut the narrative (a small part of the retained set)
    O  everything else
The recommender keeps an exponentially weighted profile of what the user finished and responds
through two saturating channels, one for the topic and one for the narrative within it.
"""
from __future__ import annotations

import numpy as np

# ------------------------------------------------------------------ constants of the study
P_SUP = 0.041      # share of A among distinct issue videos (supply)
P_BAR = 0.062      # share of A among issue impressions, platform average
C_BAR = 0.015      # share of C among issue impressions, platform average
M0 = 0.024         # share of issue videos among all impressions, platform average
HIST = 200         # history length used when probing the recommender (finished videos)
K_PROBE = 10       # injected videos at the calibration point
TOPIC_RESP = 1.02  # response of topic log-odds to 10 injected issue videos
NARR_RESP = 0.70   # response of within-issue log-odds to 10 injected A videos
S_T, S_A = 2.8, 1.5  # saturation levels of the two channels (log-odds)
NI_WEIGHT = 0.38   # weight of a "not interested" video relative to a finished one (same sign)
BASE_COMPLETE = 0.38
LAMBDA = BASE_COMPLETE / HIST  # forgetting per shown video: effective history of 200 finished videos
VIDEOS_PER_DAY = 180

A, B, C, O = 0, 1, 2, 3
ISSUE = np.array([1.0, 1.0, 1.0, 0.0])
ATTR = np.array([1.0, 0.0, -1.0, 0.0])
PI0 = np.array([M0 * P_BAR, M0 * (1 - P_BAR - C_BAR), M0 * C_BAR, 1 - M0])
KAPPA = P_BAR - C_BAR  # centring of the narrative feature within the issue


def logit(p):
    p = np.asarray(p, dtype=float)
    return np.log(p / (1 - p))


def expit(x):
    return 1 / (1 + np.exp(-np.asarray(x, dtype=float)))


PLATFORM_LAYER = float(logit(P_BAR) - logit(P_SUP))


def _solve_gain(target, sat, delta):
    return sat * np.arctanh(target / sat) / delta


G_T = float(_solve_gain(TOPIC_RESP, S_T, K_PROBE / HIST))
G_A = float(_solve_gain(NARR_RESP, S_A, K_PROBE / HIST * (1 - KAPPA)))


def response(f_t, f_a, gain_scale=1.0):
    d_t = S_T * np.tanh(G_T * f_t / S_T)
    d_a = S_A * np.tanh(gain_scale * G_A * f_a / S_A)
    return d_t, d_a


def probs_from_features(f_t, f_a, gain_scale=1.0, topic_offset=0.0):
    d_t, d_a = response(f_t, f_a, gain_scale)
    lg = np.log(PI0)[None, :] + (d_t + topic_offset)[:, None] * ISSUE[None, :] + d_a[:, None] * ATTR[None, :]
    lg -= lg.max(axis=1, keepdims=True)
    p = np.exp(lg)
    return p / p.sum(axis=1, keepdims=True)


def features(h, w):
    q = h / np.maximum(w, 1e-9)[:, None]
    q_issue = q[:, A] + q[:, B] + q[:, C]
    f_t = q_issue - M0
    f_a = q[:, A] - q[:, C] - KAPPA * q_issue
    return f_t, f_a


def completion_probs(phi, theta):
    """Probability of finishing a video of each group for a user with topic interest phi
    and narrative preference theta."""
    b0 = logit(BASE_COMPLETE)
    return np.array([
        expit(b0 + phi + theta),
        expit(b0 + phi),
        expit(b0 + phi - 0.5 * theta),
        expit(b0),
    ])


def probe(k, kind="narrative", field="watched"):
    """Model response when k videos are injected into a neutral 200-video history."""
    w = 1.0 if field == "watched" else NI_WEIGHT
    q = PI0.copy() * (HIST - k) / HIST
    tot = (HIST - k) / HIST + w * k / HIST
    if kind == "narrative":
        q[A] += w * k / HIST
    elif kind == "issue":
        q[B] += w * k / HIST
    q = q / tot
    f_t = np.array([q[A] + q[B] + q[C] - M0])
    f_a = np.array([q[A] - q[C] - KAPPA * (q[A] + q[B] + q[C])])
    p = probs_from_features(f_t, f_a)[0]
    topic = logit(p[A] + p[B] + p[C]) - logit(M0)
    narr = logit(p[A] / (p[A] + p[B] + p[C])) - logit(P_BAR)
    return float(topic), float(narr)


# ------------------------------------------------------------------ strategies
STRATEGIES = {
    "S0": dict(name="Continue as before", family="none"),
    "S1": dict(name="Scroll past the narrative", family="implicit"),
    "S2": dict(name="``Not interested'' (as implemented)", family="explicit"),
    "S3": dict(name="``Not interested'' (true negative)", family="explicit"),
    "S4": dict(name="Finish more of the other issue videos", family="implicit"),
    "S5": dict(name="Seek out rebuttal videos", family="implicit"),
    "S6": dict(name="Delete the narrative from history, then S1", family="history"),
    "S7": dict(name="Clear the whole history", family="history"),
    "S8": dict(name="Switch personalisation off", family="platform"),
    "S9": dict(name="``Show less of this topic''", family="platform"),
    "S10": dict(name="Keyword and creator blocklist", family="filter"),
    "S11": dict(name="Classifier-based filter", family="filter"),
}
FILTERS = {"S10": (0.45, 0.01), "S11": (0.79, 0.01)}  # (recall, false-positive rate)
SEARCH_RATE = 0.03   # S5: rebuttal videos found by search, per feed video
TOPIC_LESS = -1.5    # S9: log-odds offset applied to the whole issue


def simulate(phi, theta, n_form, n_act=0, n_after=0, strategy="S0", seeds=300, gain_scale=1.0,
             rng_seed=0, record_every=10):
    """Simulate `seeds` users. Returns dict of trajectories (mean and quantiles over users)."""
    rng = np.random.default_rng(rng_seed)
    comp0 = completion_probs(phi, theta)
    h = np.tile(PI0 * BASE_COMPLETE, (seeds, 1))
    w = np.full(seeds, BASE_COMPLETE)
    total = n_form + n_act + n_after
    ts, V, M, TOT, actions = [], [], [], [], np.zeros(seeds)
    tpr, fpr = FILTERS.get(strategy, (0.0, 0.0))
    for t in range(total):
        acting = n_form <= t < n_form + n_act
        if acting and t == n_form:
            if strategy == "S6":
                w = w - h[:, A]
                h[:, A] = 0.0
                actions += 1
            elif strategy == "S7":
                h = np.tile(PI0 * BASE_COMPLETE, (seeds, 1))
                w = np.full(seeds, BASE_COMPLETE)
                actions += 1
        f_t, f_a = features(h, w)
        if acting and strategy == "S8":
            p = np.tile(PI0, (seeds, 1))
        else:
            off = TOPIC_LESS if (acting and strategy == "S9") else 0.0
            p = probs_from_features(f_t, f_a, gain_scale, off)
        # what reaches the screen
        keep = np.ones(4)
        if acting and strategy in FILTERS:
            keep = np.array([1 - tpr, 1 - fpr, 1 - fpr, 1.0])
        shown = p * keep[None, :]
        if t % record_every == 0:
            issue = shown[:, A] + shown[:, B] + shown[:, C]
            share = shown[:, A] / issue
            ts.append(t)
            V.append(logit(share) - logit(P_BAR))
            M.append(issue / shown.sum(axis=1))
        # sample the next video and the user's reaction
        g = (rng.random(seeds)[:, None] > np.cumsum(p, axis=1)).sum(axis=1).clip(0, 3)
        seen = rng.random(seeds) < keep[g]
        comp = comp0.copy()
        sig_on_a = None
        if acting:
            if strategy in ("S1", "S5", "S6"):
                comp[A] = 0.0
            if strategy == "S2":
                comp[A] = 0.0
                sig_on_a = NI_WEIGHT
            if strategy == "S3":
                comp[A] = 0.0
                sig_on_a = -1.0
            if strategy == "S4":
                comp[B] = 1.0
            if strategy == "S5":
                comp[C] = 1.0
        sig = (rng.random(seeds) < comp[g]).astype(float) * seen
        if sig_on_a is not None:
            press = (g == A) & seen
            sig = np.where(press, sig_on_a, sig)
            actions += press
        h *= (1 - LAMBDA)
        w *= (1 - LAMBDA)
        h[np.arange(seeds), g] += LAMBDA * sig
        w += LAMBDA * np.abs(sig)
        if acting and strategy == "S5":
            found = rng.random(seeds) < SEARCH_RATE
            h[:, C] += LAMBDA * found
            w += LAMBDA * found
            actions += found
    V, M = np.array(V), np.array(M)
    return dict(t=np.array(ts), V=V, m=M, actions=actions)


def mean_field(phi, theta, gain_scale=1.0, iters=4000, damp=0.02):
    """Deterministic steady state (m, V) for a user type, by damped iteration."""
    comp = completion_probs(phi, theta)
    h = (PI0 * BASE_COMPLETE)[None, :].copy()
    w = np.array([BASE_COMPLETE])
    for _ in range(iters):
        f_t, f_a = features(h, w)
        p = probs_from_features(f_t, f_a, gain_scale)
        h = (1 - damp) * h + damp * p * comp[None, :]
        w = (1 - damp) * w + damp * (p * comp[None, :]).sum(axis=1)
    f_t, f_a = features(h, w)
    p = probs_from_features(f_t, f_a, gain_scale)[0]
    m = p[A] + p[B] + p[C]
    return float(m), float(logit(p[A] / m) - logit(P_BAR))


def detection_n(V, p0=P_BAR, alpha=1.0, beta=0.0, level=0.05, power=0.8):
    """Issue videos needed in each sample to detect a personal skew V (Proposition on detection)."""
    from scipy.stats import norm
    pu = expit(logit(p0) + V)
    q0 = beta + (alpha - beta) * p0
    qu = beta + (alpha - beta) * pu
    z = norm.ppf(1 - level) + norm.ppf(power)
    return z ** 2 * (qu * (1 - qu) + q0 * (1 - q0)) / (qu - q0) ** 2


if __name__ == "__main__":
    print("platform layer", round(PLATFORM_LAYER, 3), "G_T", round(G_T, 2), "G_A", round(G_A, 2))
    for k in (2, 5, 10, 20, 40):
        print(k, "issue->topic %.3f" % probe(k, "issue")[0], "A->topic %.3f narr %.3f" % probe(k, "narrative"),
              "NI A: %.3f %.3f" % probe(k, "narrative", "ni"))
    for phi, th in [(0.8, 0), (0.8, 0.75), (0.8, 1.5), (0.8, -1.0), (0.0, 1.5), (0.4, 1.5), (0.3, 0)]:
        print(phi, th, "mean-field m=%.3f V=%.3f" % mean_field(phi, th))
