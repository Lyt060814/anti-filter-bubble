"""Shared helpers: build the user-day table of screen-visible signals, platform entropy and
cocoon outcomes. Used for both KuaiRec (02_kuairec.py) and KuaiRand (04_kuairand.py).

Input: exposure DataFrame with columns user_id, day (int calendar-day index), ts, cat
(0..K-1 known category, -1 unknown), author. Rows must be one exposure each.
"""
import numpy as np
import pandas as pd

N_SCREEN = 20  # "first N exposures of the day" = what a user sees in a couple of screens


def norm_entropy(counts, K):
    """Normalised Shannon entropy (0..1) of category counts along the last axis,
    with the Miller-Madow small-sample correction (+ (m-1)/(2n)) so that windows with fewer
    exposures are not automatically 'narrower'. NaN where n == 0."""
    counts = np.asarray(counts, dtype=float)
    n = counts.sum(-1)
    with np.errstate(divide="ignore", invalid="ignore"):
        p = counts / n[..., None]
        h = -np.where(p > 0, p * np.log(p), 0).sum(-1)
        m = (counts > 0).sum(-1)
        h = h + (m - 1) / (2 * n)
        h = h / np.log(K)
    return np.where(n > 0, h, np.nan)


def build_userday(e, K, segments, baseline_days, W=3, H=3, min_win=30, min_base=100,
                  prev_active=7, rng_seed=0):
    """Return (userday DataFrame, info dict).

    segments: list of (first_day, last_day) contiguous observed periods.
    baseline_days: calendar days forming the user's baseline period.
    W: rolling window (days) for the 'platform' entropy R_W. H: prediction horizon (days).
    """
    e = e.sort_values(["user_id", "ts"]).reset_index(drop=True)
    uids, u = np.unique(e.user_id.values, return_inverse=True)
    U, D = len(uids), int(e.day.max()) + 1
    d = e.day.values.astype(int)
    k = np.where(e.cat.values < 0, K, e.cat.values).astype(int)  # slot K = unknown

    # dense count tensor C[user, day, category]
    C = np.zeros((U, D, K + 1), dtype=np.int32)
    np.add.at(C, (u, d, k), 1)
    Ck = C[:, :, :K]                       # known categories only (used for entropy)
    n_all = C.sum(-1)                      # all exposures per user-day
    n_k = Ck.sum(-1)

    seg_of = np.full(D, -1)
    for i, (s, t) in enumerate(segments):
        seg_of[s:t + 1] = i

    # ---- platform-side signals -------------------------------------------------------
    H_day = np.where(n_k >= N_SCREEN, norm_entropy(Ck, K), np.nan)
    RW = np.full((U, D), np.nan)           # rolling W-day entropy inside one segment
    for t in range(D):
        if t - W + 1 < 0 or seg_of[t] < 0 or seg_of[t - W + 1] != seg_of[t]:
            continue
        cw = Ck[:, t - W + 1:t + 1].sum(1)
        RW[:, t] = np.where(cw.sum(-1) >= min_win, norm_entropy(cw, K), np.nan)

    # ---- baseline (user's own) --------------------------------------------------------
    bd = list(baseline_days)
    base_c = Ck[:, bd].sum(1)
    base_active = (n_all[:, bd] > 0).sum(1)
    B = np.where((base_c.sum(-1) >= min_base) & (base_active >= 4), norm_entropy(base_c, K), np.nan)

    # ---- screen-visible signals from the first N exposures of each day ----------------
    e["u"], e["k"] = u, k
    e["rank"] = e.groupby(["u", "day"]).cumcount()
    f = e[e["rank"] < N_SCREEN].copy()
    # categories seen in the user's previous `prev_active` active days (strictly before t)
    seen_prev = np.zeros((U, D, K), dtype=bool)
    act = n_all > 0
    for i in range(U):
        days = np.flatnonzero(act[i])
        pres = Ck[i, days] > 0
        for j in range(1, len(days)):
            seen_prev[i, days[j]] = pres[max(0, j - prev_active):j].any(0)
    fk = f[f.k < K]
    fk = fk.assign(novel=~seen_prev[fk.u.values, fk.day.values, fk.k.values])
    g = f.groupby(["u", "day"])
    gk = fk.groupby(["u", "day"])
    scr = pd.DataFrame({
        "n20": g.size(),
        "D20": gk.k.nunique(),
        "S20": fk.groupby(["u", "day", "k"]).size().groupby(level=[0, 1]).max() / gk.size(),
        "A20": 1 - g.author.nunique() / g.size(),
        "NOV20": gk.novel.mean(),
    })
    # (first active day of a user has no history -> NOV20 = 1 by construction; set NaN)
    first_day = np.array([np.flatnonzero(act[i])[0] for i in range(U)])
    scr.loc[scr.index.get_level_values("day") == first_day[scr.index.get_level_values("u")], "NOV20"] = np.nan

    # ---- assemble long table ------------------------------------------------------------
    uu, dd = np.nonzero(act)
    ud = pd.DataFrame({"u": uu, "day": dd, "user_id": uids[uu], "seg": seg_of[dd],
                       "n": n_all[uu, dd], "H_day": H_day[uu, dd], "RW": RW[uu, dd],
                       "B": B[uu]})
    ud = ud.merge(scr.reset_index(), on=["u", "day"], how="left")
    ud = ud.sort_values(["u", "day"]).reset_index(drop=True)

    # user's own baseline of the screen signals (mean over baseline days with >= N exposures)
    bmask = ud.day.isin(bd) & (ud.n20 >= N_SCREEN)
    sb = ud[bmask].groupby("u")[["D20", "S20", "A20"]].mean().add_prefix("base_")
    ud = ud.merge(sb, left_on="u", right_index=True, how="left")
    ud["rD20"] = ud.D20 - ud.base_D20
    ud["rS20"] = ud.S20 - ud.base_S20
    ud["relRW"] = ud.RW / ud.B

    # 3-day trends: today's value minus mean of the previous 2 calendar days in same segment
    full = {}
    for col in ["D20", "S20", "H_day"]:
        M = np.full((U, D), np.nan)
        M[ud.u.values, ud.day.values] = ud[col].values
        prev = np.full((U, D), np.nan)
        for t in range(2, D):
            if seg_of[t] >= 0 and seg_of[t - 2] == seg_of[t]:
                with np.errstate(all="ignore"):
                    prev[:, t] = np.nanmean(M[:, t - 2:t], axis=1)
        full[col] = M - prev
    ud["dD20"] = full["D20"][ud.u.values, ud.day.values]
    ud["dS20"] = full["S20"][ud.u.values, ud.day.values]
    ud["dH_day"] = full["H_day"][ud.u.values, ud.day.values]

    # ---- outcomes ----------------------------------------------------------------------
    # future non-overlapping window change (continuous outcome)
    RWf = np.full((U, D), np.nan)
    RWf[:, :D - W] = RW[:, W:]
    ud["dRW_next"] = RWf[ud.u.values, ud.day.values] - ud.RW.values
    for X in (0.15, 0.25):
        tag = int(X * 100)
        ev = RW <= (1 - X) * B[:, None]              # event state per user-day (NaN -> False)
        defined = ~np.isnan(RW)
        ud[f"ev{tag}"] = ev[ud.u.values, ud.day.values]
        # label: event on any of days t+1..t+H, all inside t's segment and all R_W defined
        lab = np.full((U, D), np.nan)
        for t in range(D):
            if t + H >= D or seg_of[t] < 0 or seg_of[t + H] != seg_of[t]:
                continue
            fut_def = defined[:, t + 1:t + H + 1].all(1)
            lab[:, t] = np.where(fut_def, ev[:, t + 1:t + H + 1].any(1), np.nan)
        ud[f"y{tag}"] = lab[ud.u.values, ud.day.values]

    # ---- sampling-noise null: same n per window, but categories drawn from baseline mix ---
    rng = np.random.default_rng(rng_seed)
    # parametric bootstrap: redraw BOTH the baseline and the window from the user's baseline mix
    pB = base_c / np.maximum(base_c.sum(-1, keepdims=True), 1)
    Bnull = np.array([norm_entropy(rng.multinomial(nb, p), K) if nb > 0 else np.nan
                      for nb, p in zip(base_c.sum(-1), pB)])
    null_ev = {15: [], 25: []}
    for t in range(D):
        if np.all(np.isnan(RW[:, t])) or t in bd:
            continue
        nw = Ck[:, t - W + 1:t + 1].sum((1, 2))
        ok = ~np.isnan(RW[:, t]) & ~np.isnan(B)
        for i in np.flatnonzero(ok):
            cnt = rng.multinomial(nw[i], pB[i])
            h = norm_entropy(cnt, K)
            null_ev[15].append(h <= 0.85 * Bnull[i])
            null_ev[25].append(h <= 0.75 * Bnull[i])
    info = {"U": U, "null_event_rate15": float(np.mean(null_ev[15])),
            "null_event_rate25": float(np.mean(null_ev[25])), "segments": segments,
            "W": W, "H": H}
    return ud, info
