"""Transparent softmax model. All numerical defaults are scenario assumptions.

Paired A/B nuisance vectors ensure c=0 means zero attribute contrast, rather
than merely zero *expected* contrast. c/t below is a generating coefficient
ratio, NOT the exposure-weighted geometric contrast ratio in Proposition 2.
"""
from dataclasses import dataclass
import numpy as np


def logit(p):
    return np.log(p) - np.log1p(-p)


@dataclass
class Config:
    ratio: float = 0.15
    theta: float = 2.0
    t: float = 1.0
    tau: float = 1.0
    eta: float = 0.05
    decay: float = 0.002
    a: float = -1.0
    gamma: float = 1.0
    noise: float = 0.05


class Model:
    def __init__(self, cfg, seed):
        self.cfg = cfg
        rng = np.random.default_rng(seed)
        # 40 A, 40 B, 320 outside items; balanced supply is an assumption.
        nuisance = rng.normal(0, cfg.noise, (40, 4))
        self.v = np.zeros((400, 8))
        self.v[:80, 0] = cfg.t
        self.v[:40, 1] = cfg.ratio * cfg.t
        self.v[40:80, 1] = -cfg.ratio * cfg.t
        self.v[:40, 4:] = nuisance
        self.v[40:80, 4:] = nuisance
        self.v[80:, 2] = cfg.t
        self.v[80:, 3] = np.tile([-0.5, 0.5], 160)
        self.v[80:, 4:] = rng.normal(0, cfg.noise, (320, 4))
        self.A = np.arange(400) < 40
        self.B = (np.arange(400) >= 40) & (np.arange(400) < 80)
        self.I = self.A | self.B

    def probabilities(self, u):
        z = self.v @ u / self.cfg.tau
        z -= z.max()
        w = np.exp(z)
        return w / w.sum()

    def metrics(self, pi, reference):
        m = pi[self.I].sum()
        p = pi[self.A].sum() / m if m > 0 else np.nan
        # Use group log masses to avoid rounding p to 1 at extreme logits.
        va, vb = pi[self.A].sum(), pi[self.B].sum()
        v = np.log(va / vb) - logit(reference) if va > 0 and vb > 0 else np.nan
        return m, p, v

    def contrast(self, u, j):
        pi = self.probabilities(u)
        s = self.v @ self.v[j]
        mean = lambda mask: np.sum(pi[mask] * s[mask]) / pi[mask].sum()
        return mean(self.A) - mean(self.B), mean(self.I) - pi @ s

    def natural(self, u, rng):
        j = rng.choice(len(self.v), p=self.probabilities(u))
        cfg = self.cfg
        prob = 1 / (1 + np.exp(-(cfg.a + cfg.gamma*self.I[j] + cfg.theta*self.A[j])))
        delta = cfg.eta * self.v[j] if rng.random() < prob else np.zeros(8)
        return (1-cfg.decay)*u + delta


def self_check():
    import csv
    from pathlib import Path
    rows = []
    for theta in (0, 0.5, 1, 2):
        for seed in range(20):
            model = Model(Config(ratio=0, theta=theta), seed)
            rng = np.random.default_rng(seed)
            u = np.zeros(8)
            for _ in range(500):
                u = model.natural(u, rng)
            v = model.metrics(model.probabilities(u), 0.5)[2]
            assert abs(v) < 1e-12, (theta, seed, v)
            rows.append(dict(check='zero_contrast', theta=theta, seed=seed,
                             eta=0, observed=v, predicted=0, error=abs(v)))
    # Non-paired random item vectors: general, nontrivial first-order test.
    for seed in range(20):
        rng = np.random.default_rng(seed)
        model = Model(Config(), seed)
        model.v += rng.normal(0, 0.2, model.v.shape)
        u = rng.normal(0, 0.2, 8)
        c, _ = model.contrast(u, 0)
        before = model.metrics(model.probabilities(u), 0.5)[2]
        for sign in (-1, 1):
            errors = []
            for h in (0.01, 0.005, 0.0025):
                eta = sign*h
                observed = model.metrics(model.probabilities(u+eta*model.v[0]), 0.5)[2]-before
                predicted = eta/model.cfg.tau*c
                error = abs(observed-predicted)
                errors.append(error)
                rows.append(dict(check='first_order', theta=2, seed=seed,
                                 eta=eta, observed=observed, predicted=predicted, error=error))
            # A small quadratic coefficient can cancel the cubic term at the
            # largest h. Require reduction and an explicit O(h^2) bound.
            assert errors[-1] < errors[0]*0.3 + 1e-13, errors
            assert max(e/h**2 for e, h in zip(errors, (0.01, 0.005, 0.0025))) < 0.1
    path = Path(__file__).parent/'results'
    path.mkdir(exist_ok=True)
    with (path/'r1_checks.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    print('PASS R1: c=0 (4 theta x 20 seeds x 500 steps); first-order +/- eta, 20 seeds, quadratic error.')


if __name__ == '__main__':
    self_check()
