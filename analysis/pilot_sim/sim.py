"""
sim.py -- a small, readable "X-like" For You feed simulator (feasibility pilot).

Question: how cheaply can a user ESCAPE an information cocoon, and how fast do they relapse?

One call to `run(cfg)` simulates cfg.n_users users IN PARALLEL (NumPy arrays have a user axis U)
through four phases:
    Phase 0 normal use -> Phase 1 binge on a seed category -> Phase 2 escape strategy -> Phase 3 relapse check
One time step = one feed refresh that shows a slate of cfg.slate (=10) posts.

Every modelling assumption is tagged in comments:
  [X file:line]  value/formula copied from xai-org/x-algorithm (snapshot 2026-09-25)
  [ASSUMPTION]   our own simplification (X's learned model internals are not public)
  [LIT]          taken from a paper (Chaney+ 2018, Piao+ 2023, phoenix/reference/world.py)
"""
from dataclasses import dataclass
import numpy as np

# ---------------------------------------------------------------- X constants
# Action weights [X home-mixer/params/param.rs:295-407]
W_FAV, W_REPLY, W_RETWEET, W_QUOTE, W_SHARE, W_DWELL = 0.5, 5.0, 1.0, 5.0, 2.0, 0.05
W_FOLLOW, W_NOT_INTERESTED, W_NOT_DWELLED = 4.0, -43.2, -0.02
# [ASSUMPTION] Phoenix predicts ~25 heads; we collapse the positive ones into ONE predicted
# engagement probability p_eng and assume the other heads are proportional to it, using the base
# rates of phoenix/reference/world.py:54-63 (fav .14, reply .035, repost .045, quote .015, share .012).
W_POS = (W_FAV + W_REPLY * .035 / .14 + W_RETWEET * .045 / .14 + W_QUOTE * .015 / .14
         + W_SHARE * .012 / .14 + W_DWELL)          # = 2.83 per unit of p_eng
FOLLOW_RATE = 0.02                                  # [ASSUMPTION] P(follow) = 0.02 * p_eng for OON posts
# Negative-score squashing [X xai-value-model/scoring.rs:121-130, weights.rs:4,45-72]
OFFSET, POS_SUM, NEG_SUM = 0.001, 43.34, 367.22

ENG, NI, SKIP = 1, 2, 3                             # event types stored in the action history


@dataclass
class Config:
    # world
    K: int = 20                 # topic categories (Chaney+ 2018 and Piao+ 2023 both use ~20)
    authors_per_cat: int = 20   # A = K * 20 = 400 authors, each with one primary category
    D: int = 32                 # embedding dim (must be >> slate size, else DPP is rank-limited)
    emb_noise: float = 0.5      # [ASSUMPTION] post-specific noise; 0.5 -> same-topic cos ~0.73 (world.py 0.15 -> ~0.87)
    n_groups: int = 5           # [ASSUMPTION] categories come in 5 groups of related topics
    glob_conc: float = 3.0      # global category popularity g ~ Dir(3)  (tuned so random feed ~ KuaiRand random)
    user_conc: float = 10.0     # user taste p_u ~ Dir(10 * g)  [LIT Chaney+ 2018: Dir(10*mu)]
    n_users: int = 200
    seed: int = 0
    # candidate sources per request (X: Thunder <=1200, Phoenix <=1000, SimClusters <=800; scaled down)
    n_in: int = 30              # in-network: posts from followed authors  [X thunder]
    n_ret: int = 70             # OON retrieval: categories ~ history affinity  [X phoenix_source / simclusters]
    n_glob: int = 50            # [ASSUMPTION] OON "global" posts ~ popularity g (fresh inventory)
    n_follow0: int = 15         # initial follows, categories ~ p_u
    slate: int = 10
    q_sigma: float = 0.7        # [ASSUMPTION] post quality q ~ LogNormal(0, .7), mean 1  [LIT world.py:302-305]
    # recommender ("Phoenix stand-in", all [ASSUMPTION])
    recommender: str = "x"      # "x" (X-like pipeline) | "greedy" (top p_eng) | "random"
    M: int = 200                # FIFO action history length  [X param.rs:770-781 uses 1024]
    log_skips: bool = False     # H2: skipped impressions also enter the FIFO (only as filler, no signal)
    lam: float = 0.4            # learning sensitivity (calibrated to KuaiRand, see run_experiments.py): p_eng ~ (K * affinity)^lam
    b_eng: float = 0.1          # base engagement rate for an "average" category
    pred_noise: float = 0.1     # log-normal noise on predictions (random tie-breaking)
    b_ni: float = 0.002         # base P(not_interested)
    ni_smooth: float = 10.0     # pseudo-count when estimating P(NI) from history
    ni_variant: str = "B"       # A: per author, B: per category, C: embedding similarity
    ni_tau: float = 0.2         # variant C: cosine threshold for "similar"
    author_div: bool = True     # [X vm-ranker/params.rs:139-156] enable, decay .5, floor .25
    decay: float = 0.5
    floor: float = 0.25
    oon: bool = True            # [X vm-ranker/params.rs:175-180] OON factor 0.75
    oon_factor: float = 0.75
    dpp: bool = True            # [X vm-ranker/params.rs:199-211] DPP enabled, theta .65, pool 150
    theta: float = 0.65
    dpp_k: int = 14             # DPP picks 14, top 10 by score are served (X: DPP top_k 50 -> serve 35)
    # user behaviour
    e0: float = 0.35            # P(engage) = w(rank) * min(1, e0 * K * p_u[c])
    pos_bias: float = 0.8       # w(rank) = rank^-0.8  [LIT Chaney+ 2018]
    binge_eng: float = 0.9      # Phase 1: P(engage | seed post) before position bias
    binge_follow: float = 0.2   # Phase 1: prob./step of following an engaged seed author
    binge_search: int = 5       # Phase 1: seed searches per step (active seeking)
    strategy: str = "S0"        # escape strategy S0..S5 (see run())
    n_search: int = 2           # S2: searches per step
    follow_steps: int = 10      # S3: follow 1 new author/step for the first 10 escape steps
    relapse_h: float = 0.2      # Phase 3: residual seed interest p' ~ p + h*onehot(seed)
    T0: int = 30
    T1: int = 40
    T2: int = 60
    T3: int = 60


# ---------------------------------------------------------------- helpers
def unit(x):
    return x / np.linalg.norm(x, axis=-1, keepdims=True)


def sample_rows(P, k, rng):
    """For each row of probability matrix P (U,n) draw k indices -> (U,k)."""
    cdf = np.cumsum(P / P.sum(1, keepdims=True), axis=1)
    r = rng.random((P.shape[0], k))
    return np.minimum((cdf[:, None, :] < r[:, :, None]).sum(-1), P.shape[1] - 1)


def row_counts(idx, mask, n):
    """Per-row histogram: counts[u, j] = #{m : idx[u,m]==j and mask[u,m]}."""
    U = idx.shape[0]
    flat = (np.arange(U)[:, None] * n + idx)[mask]
    return np.bincount(flat, minlength=U * n).reshape(U, n).astype(float)


def norm_entropy(counts):
    """Shannon entropy of each row of counts, divided by ln(K)."""
    p = counts / np.maximum(counts.sum(-1, keepdims=True), 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        h = -np.nansum(np.where(p > 0, p * np.log(p), 0.0), axis=-1)
    return h / np.log(counts.shape[-1])


class World:
    """Categories, authors, users.  Posts are generated fresh every step (X serves posts < 48 h old)."""

    def __init__(self, cfg, rng):
        K, D, U = cfg.K, cfg.D, cfg.n_users
        self.A = K * cfg.authors_per_cat
        self.noise = cfg.emb_noise
        group = unit(rng.normal(size=(cfg.n_groups, D)))[np.arange(K) % cfg.n_groups]
        self.cent = unit(0.6 * group + 0.8 * unit(rng.normal(size=(K, D))))   # related cats: cos ~ .36
        self.style = unit(rng.normal(size=(self.A, D)))
        self.auth_cat = np.repeat(np.arange(K), cfg.authors_per_cat)
        self.g = rng.dirichlet(np.full(K, cfg.glob_conc))                   # global popularity
        self.p = rng.dirichlet(cfg.user_conc * self.g, size=U)             # true taste (U,K)
        # seed category: random among the user's categories ranked 4..K (a "rabbit hole", not a main interest)
        rank = np.argsort(-self.p, axis=1)
        self.seed = rank[np.arange(U), rng.integers(3, K, U)]

    def emb(self, cat, auth, rng):
        """Post embedding = category centroid + 0.35 author style + noise  [LIT world.py:417-429 uses 0.15]."""
        noise = unit(rng.normal(size=cat.shape + (self.cent.shape[1],)))
        return unit(self.cent[cat] + 0.35 * self.style[auth] + self.noise * noise).astype(np.float32)

    def rand_author(self, cat, rng, cfg):
        return cat * cfg.authors_per_cat + rng.integers(0, cfg.authors_per_cat, cat.shape)


class History:
    """FIFO buffer of the last M user actions [X: user action sequence, param.rs:770-781]."""

    def __init__(self, U, M, D):
        self.typ = np.zeros((U, M), np.int8)
        self.cat = np.zeros((U, M), int)
        self.auth = np.zeros((U, M), int)
        self.emb = np.zeros((U, M, D), np.float32)
        self.ptr = np.zeros(U, int)
        self.M = M

    def add(self, mask, typ, cat, auth, emb):
        u = np.nonzero(mask)[0]
        j = self.ptr[u] % self.M
        self.typ[u, j], self.cat[u, j], self.auth[u, j], self.emb[u, j] = typ, cat[u], auth[u], emb[u]
        self.ptr[u] += 1


# ---------------------------------------------------------------- recommender
def affinity(cfg, H):
    """Category affinity learned from the ENG events in the history; rel = (K*aff)^lam."""
    cat_eng = row_counts(H.cat, H.typ == ENG, cfg.K)
    aff = (cat_eng + 1.0) / (cat_eng.sum(1, keepdims=True) + cfg.K)     # Laplace-smoothed share
    return cat_eng, (cfg.K * aff) ** cfg.lam                            # lam = learning sensitivity


def predict(cfg, w, H, cc, ca, ce, cq, rng):
    """Phoenix stand-in [ASSUMPTION]: predicted P(engage) and P(not_interested) from history counts."""
    U, K, A = cc.shape[0], cfg.K, w.A
    eng, ni = H.typ == ENG, H.typ == NI
    cat_eng, rel = affinity(cfg, H)
    auth_eng = row_counts(H.auth, eng, A)
    u = np.arange(U)[:, None]
    boost = 1 + 0.5 * np.minimum(auth_eng[u, ca], 3) / 3                 # liked this author before
    x = cfg.b_eng * rel[u, cc] * boost * cq * np.exp(cfg.pred_noise * rng.standard_normal(cc.shape))
    p_eng = 1 - np.exp(-x)                                               # smooth saturation in [0,1)
    # P(NI) = smoothed share of NI among the user's past reactions to the "same thing" (variant-dependent)
    if cfg.ni_variant == "A":                                            # "show fewer from @author"
        n_ni, n_e = row_counts(H.auth, ni, A)[u, ca], auth_eng[u, ca]
    elif cfg.ni_variant == "B":                                          # "not interested in this topic"
        n_ni, n_e = row_counts(H.cat, ni, K)[u, cc], cat_eng[u, cc]
    else:                                                                # C: generalises by embedding
        sim = np.clip((np.einsum("und,umd->unm", ce, H.emb) - cfg.ni_tau) / (1 - cfg.ni_tau), 0, 1)
        n_ni, n_e = (sim * ni[:, None, :]).sum(-1), (sim * eng[:, None, :]).sum(-1)
    p_ni = (n_ni + cfg.b_ni * cfg.ni_smooth) / (n_ni + n_e + cfg.ni_smooth)
    return p_eng, p_ni


def author_rank(S, ca):
    """k_i = # candidates by the same author with a higher score [X scoring.rs:147-164]."""
    U, N = S.shape
    order = np.argsort(-S, axis=1)
    a_sorted = np.take_along_axis(ca, order, 1)
    key = (np.arange(U)[:, None] * 10**6 + a_sorted).ravel()
    idx = np.argsort(key, kind="stable")                  # groups by (user, author), keeps score order
    pos = np.arange(U * N)
    new_group = np.r_[True, key[idx][1:] != key[idx][:-1]]
    start = np.maximum.accumulate(np.where(new_group, pos, 0))
    k_sorted = np.empty(U * N, int)
    k_sorted[idx] = pos - start
    k = np.empty((U, N), int)
    np.put_along_axis(k, order, k_sorted.reshape(U, N), 1)
    return k


def dpp_select(S, E, theta, k):
    """Greedy DPP MAP (Chen+ 2018), batched over users  [X vm-ranker/dpp.rs:92-314].
    q = exp(alpha * s / s_max), alpha = theta / (2(1-theta)); L_ij = q_i q_j cos(e_i, e_j)."""
    U, N = S.shape
    alpha = theta / (2 * (1 - theta))
    q = np.exp(alpha * S / np.maximum(S.max(1, keepdims=True), 1e-6))
    d2 = q ** 2                                            # L_ii (embeddings are unit vectors)
    C = np.zeros((U, k, N))
    sel = np.zeros((U, k), int)
    u = np.arange(U)
    for t in range(k):
        j = np.argmax(d2, axis=1)
        sel[:, t] = j
        Lj = q[u, j][:, None] * q * np.einsum("ud,und->un", E[u, j], E)
        e = (Lj - np.einsum("uk,ukn->un", C[u, :t, j], C[:, :t, :])) / np.sqrt(np.maximum(d2[u, j], 1e-12))[:, None]
        C[:, t, :] = e
        d2 = d2 - e ** 2
        d2[u[:, None], sel[:, :t + 1]] = -np.inf           # never pick twice
    # X's DPP is a FILTER: winners keep their original score order [X dpp.rs:154-171]
    return np.take_along_axis(sel, np.argsort(-np.take_along_axis(S, sel, 1), 1), 1)


def recommend(cfg, w, H, followed, rng, personalised=True):
    """One For You request: candidates -> scores -> multipliers -> DPP -> slate indices."""
    U, K = followed.shape[0], cfg.K
    # --- candidate sources
    a_in = sample_rows(followed.astype(float), cfg.n_in, rng)
    c_in = np.where(rng.random(a_in.shape) < 0.8, w.auth_cat[a_in],   # 80% primary topic [LIT world.py]
                    sample_rows(np.tile(w.g, (U, 1)), cfg.n_in, rng))
    c_ret = sample_rows(affinity(cfg, H)[1], cfg.n_ret, rng)                             # retrieval ~ history affinity
    c_gl = sample_rows(np.tile(w.g, (U, 1)), cfg.n_glob, rng)            # fresh global inventory
    cc = np.concatenate([c_in, c_ret, c_gl], 1)
    ca = np.concatenate([a_in, w.rand_author(c_ret, rng, cfg), w.rand_author(c_gl, rng, cfg)], 1)
    ce = w.emb(cc, ca, rng)
    cq = np.exp(cfg.q_sigma * rng.standard_normal(cc.shape) - cfg.q_sigma ** 2 / 2)   # post quality
    innet = followed[np.arange(U)[:, None], ca]
    if not personalised or cfg.recommender == "random":                  # random slate from global inventory
        sel = cfg.n_in + cfg.n_ret + np.argsort(rng.random((U, cfg.n_glob)), 1)[:, :cfg.slate]
        return cc, ca, ce, cq, innet, sel
    p_eng, p_ni = predict(cfg, w, H, cc, ca, ce, cq, rng)
    if cfg.recommender == "greedy":                                      # pure engagement-greedy baseline
        return cc, ca, ce, cq, innet, np.argsort(-p_eng, 1)[:, :cfg.slate]
    # --- X value model [X scoring.rs:65-130]
    S = (W_POS * p_eng + W_FOLLOW * FOLLOW_RATE * p_eng * ~innet
         + W_NOT_INTERESTED * p_ni + W_NOT_DWELLED * (1 - p_eng))
    S = np.where(S >= 0, S + OFFSET, (S + NEG_SUM) / (POS_SUM + NEG_SUM) * OFFSET)
    if cfg.author_div:                                                   # [X scoring.rs:143-145]
        S = S * ((1 - cfg.floor) * cfg.decay ** author_rank(S, ca) + cfg.floor)
    if cfg.oon:                                                          # [X scoring.rs:166-175]
        S = S * np.where(innet, 1.0, cfg.oon_factor)
    if cfg.dpp:                                                          # pool = all 150 = max_selected_rank
        sel = dpp_select(S, ce, cfg.theta, cfg.dpp_k)[:, :cfg.slate]   # winners sorted by score
    else:
        sel = np.argsort(-S, 1)[:, :cfg.slate]
    return cc, ca, ce, cq, innet, sel


# ---------------------------------------------------------------- simulation
def run(cfg):
    """Simulate all users through the 4 phases. Returns a dict of per-step logs (arrays U x T ...)."""
    rng = np.random.default_rng(cfg.seed)
    w = World(cfg, rng)
    U, K, u = cfg.n_users, cfg.K, np.arange(cfg.n_users)
    T = cfg.T0 + cfg.T1 + cfg.T2 + cfg.T3
    seed_1h = np.eye(K)[w.seed].astype(bool)
    # initial follows and a warm history of M engagements drawn from true taste ("existing user")
    followed = np.zeros((U, w.A), bool)
    fc = sample_rows(w.p, cfg.n_follow0, rng)
    followed[u[:, None], w.rand_author(fc, rng, cfg)] = True
    H = History(U, cfg.M, cfg.D)
    hc = sample_rows(w.p, cfg.M, rng)
    ha = w.rand_author(hc, rng, cfg)
    he = w.emb(hc, ha, rng)
    for m in range(cfg.M):
        H.add(np.ones(U, bool), ENG, hc[:, m], ha[:, m], he[:, m])
    pw = np.arange(1, cfg.slate + 1) ** -cfg.pos_bias                    # position bias w(rank)
    no_seed = w.p * ~seed_1h                                             # taste without the seed topic
    log = dict(cats=np.zeros((U, T, cfg.slate), int), util=np.zeros((U, T)),
               actions=np.zeros((U, T)), innet=np.zeros((U, T)))
    S = cfg.strategy
    for t in range(T):
        phase = int(t >= cfg.T0) + int(t >= cfg.T0 + cfg.T1) + int(t >= cfg.T0 + cfg.T1 + cfg.T2)
        t2 = t - cfg.T0 - cfg.T1                                         # step index inside Phase 2
        personalised = not (phase == 2 and S == "S4")                    # S4: personalisation OFF
        cc, ca, ce, cq, innet, sel = recommend(cfg, w, H, followed, rng, personalised)
        c, a, q = (np.take_along_axis(x, sel, 1) for x in (cc, ca, cq))
        e = ce[u[:, None], sel]
        is_seed = c == w.seed[:, None]
        # --- user response (true model, hidden from the recommender; post quality q is visible to both)
        pref = w.p if phase < 3 else (w.p + cfg.relapse_h * seed_1h) / (1 + cfg.relapse_h)
        p_true = np.minimum(1, cfg.e0 * K * pref[u[:, None], c] * q)
        if phase == 1:
            p_true = cfg.binge_eng * is_seed                             # binge: only the seed topic
        if phase == 2:
            p_true = p_true * ~is_seed                                   # escape: stop engaging the seed
        eng = rng.random(c.shape) < pw * p_true
        for r in range(cfg.slate):
            H.add(eng[:, r], ENG, c[:, r], a[:, r], e[:, r])
        n_act, ni_mask = np.zeros(U), np.zeros_like(eng)
        # --- phase-specific extra actions
        if phase == 1:                                                   # binge: search the seed topic,
            for _ in range(cfg.binge_search):                            # sometimes follow a seed author
                sc = w.seed.copy(); sa = w.rand_author(sc, rng, cfg)
                H.add(np.ones(U, bool), ENG, sc, sa, w.emb(sc, sa, rng))
            hit = eng & is_seed                                          # follow the first engaged seed author
            f = hit.any(1) & (rng.random(U) < cfg.binge_follow)
            followed[u[f], a[u, hit.argmax(1)][f]] = True
        if phase == 2 and S in ("S1", "S5"):                             # NI on every seed post shown
            ni_mask = is_seed
            for r in range(cfg.slate):
                H.add(ni_mask[:, r], NI, c[:, r], a[:, r], e[:, r])
            n_act += ni_mask.sum(1)
        if phase == 2 and S in ("S2", "S5"):                             # search & engage other topics
            for _ in range(cfg.n_search):
                sc = sample_rows(no_seed, 1, rng)[:, 0]; sa = w.rand_author(sc, rng, cfg)
                H.add(np.ones(U, bool), ENG, sc, sa, w.emb(sc, sa, rng))
            n_act += cfg.n_search
        if phase == 2 and S in ("S3", "S5") and t2 < cfg.follow_steps:   # follow a new non-seed author
            fc = sample_rows(no_seed, 1, rng)[:, 0]; fa = w.rand_author(fc, rng, cfg)
            followed[u, fa] = True
            H.add(np.ones(U, bool), ENG, fc, fa, w.emb(fc, fa, rng))    # a follow is an engagement event
            n_act += 1
        if cfg.log_skips:                                                # H2: impressions refresh the memory
            for r in range(cfg.slate):
                H.add(~eng[:, r] & ~ni_mask[:, r], SKIP, c[:, r], a[:, r], e[:, r])
        if phase == 2 and S == "S4" and t2 == 0:
            n_act += 1                                                   # one toggle in settings
        log["cats"][:, t] = c
        log["util"][:, t] = (pw * np.minimum(1, cfg.e0 * K * w.p[u[:, None], c] * q)).sum(1)
        log["actions"][:, t] = n_act
        log["innet"][:, t] = np.take_along_axis(innet, sel, 1).mean(1)
    log.update(seed=w.seed, p=w.p, g=w.g, cfg=cfg)
    return log


# ---------------------------------------------------------------- metrics
def metrics(log, win=3):
    """Rolling (win steps = 30 posts) seed share, entropy, s-tilde; derived escape/relapse numbers."""
    cfg, cats, seed, p = log["cfg"], log["cats"], log["seed"], log["p"]
    U, T, n = cats.shape
    K = cfg.K
    per_step = np.stack([(cats == k).sum(-1) for k in range(K)], -1).astype(float)   # (U,T,K)
    cs = np.cumsum(np.concatenate([np.zeros((U, 1, K)), per_step], 1), 1)
    roll = cs[:, win:] - cs[:, :-win]                                   # window ending at t (t>=win-1)
    roll = np.concatenate([np.repeat(roll[:, :1], win - 1, 1), roll], 1)
    seed_share = roll[np.arange(U), :, seed] / (win * n)
    H = norm_entropy(roll)
    rng = np.random.default_rng(1)                                      # s* = entropy of win*n draws
    draws = np.stack([rng.multinomial(win * n, pi, size=200) for pi in p])   # from the true taste
    s_star = norm_entropy(draws).mean(1)
    s_tilde = H / s_star[:, None]
    b0, b1, b2 = cfg.T0, cfg.T0 + cfg.T1, cfg.T0 + cfg.T1 + cfg.T2
    base_s, base_H = seed_share[:, b0 - 10:b0].mean(1), H[:, b0 - 10:b0].mean(1)
    peak = seed_share[:, b1 - 5:b1].mean(1)

    def first(cond, T):                                                 # first True index, else T (censored)
        return np.where(cond.any(1), cond.argmax(1), T)
    ttc = first(seed_share[:, b0:b1] > 0.5, cfg.T1)
    esc = first(seed_share[:, b1:b2] < base_s[:, None] + 0.1, cfg.T2)
    esc_H = first(H[:, b1:b2] >= 0.9 * base_H[:, None], cfg.T2)
    acts = np.cumsum(log["actions"][:, b1:b2], 1)
    esc_act = acts[np.arange(U), np.minimum(esc, cfg.T2 - 1)]
    end3 = seed_share[:, -10:].mean(1)
    half = base_s + 0.5 * (peak - base_s)                               # relapse time: steps in Phase 3 until
    rel_time = first(seed_share[:, b2:] > half[:, None], cfg.T3)        # seed share is half-way back to peak
    cocooned = peak - base_s > 0.2                                      # binge really moved the feed
    relapse = np.where(cocooned, (end3 - base_s) / np.maximum(peak - base_s, 1e-6), np.nan)
    return dict(seed_share=seed_share, H=H, s_tilde=s_tilde, base_s=base_s, base_H=base_H, peak=peak,
                ttc=ttc, cocooned=cocooned, esc=esc, escaped=esc < cfg.T2, esc_H=esc_H, esc_act=esc_act,
                end2=seed_share[:, b2 - 10:b2].mean(1), end3=end3, relapse=relapse, rel_time=rel_time,
                st0=s_tilde[:, b0 - 10:b0].mean(1), st1=s_tilde[:, b1 - 5:b1].mean(1),
                st2=s_tilde[:, b2 - 10:b2].mean(1), st3=s_tilde[:, -10:].mean(1),
                util_ratio=log["util"][:, b1:b2].mean(1) / log["util"][:, b0 - 10:b0].mean(1),
                total_actions=acts[:, -1])


def calibration_blocks(log, T_end, block=2):
    """KuaiRand-style concentration over blocks of 20 exposures (2 slates) during Phase 0."""
    cats = log["cats"][:, :T_end]
    U, T, n = cats.shape
    b = cats[:, :T - T % block].reshape(U, -1, block * n)
    cnt = np.stack([(b == k).sum(-1) for k in range(log["cfg"].K)], -1)
    return cnt.max(-1).mean() / (block * n), (cnt > 0).sum(-1).mean()
