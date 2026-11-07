"""R2--R4 runners: synthetic scenario assumptions, no real user data."""
import argparse
import csv
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from statistics import NormalDist
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model import Config, Model, logit, reference_logit

ROOT = Path(__file__).parent
RATIOS = sorted(set([round(x, 2) for x in np.linspace(0, 1, 11)] + [0.15, 0.59]))
THETAS = [0, 0.5, 1, 2]
SEEDS = list(range(20))
T = 600
ACTIVE = 200
FOLLOW = 400


def save_csv(name, rows):
    (ROOT/'results').mkdir(exist_ok=True)
    with (ROOT/'results'/f'{name}.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=rows[0])
        w.writeheader()
        w.writerows(rows)


def metadata(name, extra):
    meta = dict(evidence_type='scenario assumption / synthetic simulation',
                seeds=SEEDS, independent_unit='seed: four-user population, one user per theta',
                theta=THETAS, coefficient_ratios=RATIOS,
                defaults=vars(Config()), formation_steps=T, intervention_steps=ACTIVE,
                followup_steps=FOLLOW, script='analysis/v6_simulation/experiments.py',
                git_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                utc=datetime.now(timezone.utc).isoformat(),
                interval='mean +/- t(19,0.975)=2.093 * sample SD / sqrt(20); pointwise Monte Carlo CI',
                sources=['docs/tasks/xu_ruicong.md', 'docs/project-plan/research_plan_v5.md section 4',
                         'docs/context-recovery/plan_v5_feasibility.md section 3.4'])
    meta.update(extra)
    (ROOT/'results'/f'{name}.meta.json').write_text(json.dumps(meta, indent=2), encoding='utf8')
    (ROOT/'figures'/f'{name}.meta.json').write_text(json.dumps(meta, indent=2), encoding='utf8')


def figure(name, extra=None):
    (ROOT/'figures').mkdir(exist_ok=True)
    plt.gcf().text(0.5, 0.005, 'Synthetic scenarios; parameters assumed. Bands/bars: pointwise 95% Monte Carlo CI (20 seeds).',
                  ha='center', fontsize=7)
    plt.tight_layout(rect=(0, 0.035, 1, 1))
    plt.savefig(ROOT/'figures'/f'{name}.png', dpi=300)
    plt.savefig(ROOT/'figures'/f'{name}.pdf')
    plt.close()
    metadata(name, extra or {})


def ci(x):
    x = np.asarray(x, dtype=float)
    return np.mean(x, axis=0), 2.093*np.std(x, axis=0, ddof=1)/np.sqrt(len(x))


def population(ratio, seed, decay=0.002):
    """Each seed is an independent four-user world; shared item catalogue.

    Platform reference is ratio of *mean masses*, never mean conditional p.
    Record exact metrics every step internally; CSV snapshots every 20 steps.
    Keep decayed A contributions so S5 reverses only their surviving weights.
    """
    model = Model(Config(ratio=ratio, decay=decay), seed)
    rngs = [np.random.default_rng(seed*100+q) for q in range(4)]
    users = np.zeros((4, 8))
    ahist = np.zeros_like(users)
    rows = []
    for step in range(T+1):
        pis = np.array([model.probabilities(u) for u in users])
        mean_pi = pis.mean(axis=0)
        ref = (mean_pi[model.A].sum(), mean_pi[model.B].sum())
        if step % 20 == 0:
            for q, theta in enumerate(THETAS):
                m, p, v = model.metrics(pis[q], ref)
                c, topic = model.contrast(users[q], 0)
                rows.append(dict(ratio=ratio, theta=theta, seed=seed, decay=decay, step=step,
                                 m=m, p=p, V=v, reference=ref[0]/sum(ref),
                                 total_bias=np.log(pis[q,model.A].sum()/pis[q,model.B].sum()),
                                 platform_bias=reference_logit(ref), contrast_A=c, topic_contrast_A=topic))
        if step == T:
            return model, users, ahist, ref, rows
        for q, theta in enumerate(THETAS):
            rng = rngs[q]
            j = rng.choice(400, p=pis[q])
            prob = 1/(1+np.exp(-(-1+model.I[j]+theta*model.A[j])))
            completed = rng.random() < prob
            users[q] *= 1-decay
            ahist[q] *= 1-decay
            if completed:
                users[q] += model.cfg.eta*model.v[j]
                if model.A[j]:
                    ahist[q] += model.cfg.eta*model.v[j]


def formation():
    rows = []
    for decay in (0, 0.002):
        for ratio in RATIOS:
            for seed in SEEDS:
                rows.extend(population(ratio, seed, decay)[-1])
            print(f'R2 decay={decay} c/t={ratio}: 20 seeds complete', flush=True)
    save_csv('formation', rows)
    fig, axes = plt.subplots(2, 4, figsize=(13, 6))
    for d, decay in enumerate((0, 0.002)):
        for q, theta in enumerate(THETAS):
            ax = axes[d, q]
            for ratio in (0, 0.15, 0.59, 1):
                group = [r for r in rows if r['ratio']==ratio and r['theta']==theta and r['decay']==decay]
                m = np.array([r['m'] for r in group]).reshape(20, -1)
                v = np.array([r['V'] for r in group]).reshape(20, -1)
                mm, em = ci(m)
                vv, ev = ci(v)
                line, = ax.plot(mm, vv, label=f'c/t={ratio}')
                ax.fill_between(mm, vv-ev, vv+ev, alpha=.12, color=line.get_color())
                ax.errorbar(mm[-1], vv[-1], xerr=em[-1], yerr=ev[-1], color=line.get_color())
            ax.set(title=f'theta={theta}; decay={decay}', xlabel='Topic exposure m', ylabel='Personal skew V')
    axes[0,0].legend(fontsize=7)
    figure('formation', dict(csv_snapshot_interval=20, decay_scan=[0, .002],
                             plotted_ratios=[0,.15,.59,1], all_ratios_available_in_csv=True))


def detection():
    zsum = NormalDist().inv_cdf(.95)+NormalDist().inv_cdf(.8)
    rows = []
    # Deterministic formula: no artificial random seeds / confidence intervals.
    for p0 in (.018, .41):
        for alpha, beta in ((.8,.02), (.7,.02), (.9,.02), (.8,0), (.8,.05)):
            for odds in np.linspace(2,8,61):
                p = odds*p0/(1-p0+odds*p0)
                q, q0 = beta+(alpha-beta)*p, beta+(alpha-beta)*p0
                n = zsum**2*(q*(1-q)+q0*(1-q0))/((alpha-beta)**2*(p-p0)**2)
                for rate in (.016,.036):
                    rows.append(dict(p0=p0, odds=odds, alpha=alpha, beta=beta,
                                     topic_rate=rate, n_per_arm=np.ceil(n),
                                     total_per_arm=np.ceil(np.ceil(n)/rate),
                                     combined_two_arm_exposures=2*np.ceil(np.ceil(n)/rate)))
    save_csv('detection', rows)
    fig, axes = plt.subplots(1,2,figsize=(10,4))
    for p0 in (.018,.41):
        for rate in (.016,.036):
            group = [r for r in rows if r['p0']==p0 and r['alpha']==.8 and r['beta']==.02 and r['topic_rate']==rate]
            axes[1].plot([r['odds'] for r in group], [r['total_per_arm'] for r in group], label=f'p0={p0}, m={rate}')
        group = [r for r in rows if r['p0']==p0 and r['alpha']==.8 and r['beta']==.02 and r['topic_rate']==.016]
        axes[0].plot([r['odds'] for r in group], [r['n_per_arm'] for r in group], label=f'p0={p0}')
    for ax, label in zip(axes, ('Same-topic videos per arm', 'Total exposures per arm')):
        ax.set(xlabel='Odds multiplier (not probability multiplier)', ylabel=label, yscale='log')
        ax.legend(fontsize=8)
    figure('detection', dict(evidence_type='analytic approximation; assumed classifier; repository-reported pilot anchors',
                             seeds=[], interval='none: deterministic formula', alpha=.8, beta=.02,
                             significance=.05, power=.8, n0_equals_n=True,
                             warning='Independent observations, known classifier rates; no D3 calibration yet. Each arm needs n.'))
    print('PASS R4: odds conversion and two-arm sample sizes saved.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('task', choices=['formation','detection'])
    args = parser.parse_args()
    globals()[args.task]()
