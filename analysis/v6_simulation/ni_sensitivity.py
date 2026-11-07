"""Additional assumed NI strengths, including +0.78 (not a calibration)."""
from experiments import *


def run():
    multipliers = [-2., -1., -.5, .25, .5, .78, 1.]
    rows = []
    for ratio in RATIOS:
        for seed in SEEDS:
            model, endpoints, _, ref, _ = population(ratio, seed)
            for q, theta in enumerate(THETAS):
                rng = np.random.default_rng(10000+100*seed+q)
                u = np.tile(endpoints[q], (len(multipliers),1))
                pi0 = model.probabilities(endpoints[q])
                bm, _, bv = model.metrics(pi0, ref)
                for step in range(ACTIVE+FOLLOW+1):
                    logits = u@model.v.T/model.cfg.tau
                    logits -= logits.max(axis=1,keepdims=True)
                    pi = np.exp(logits)
                    pi /= pi.sum(axis=1,keepdims=True)
                    if step in (0,ACTIVE,ACTIVE+FOLLOW):
                        for a, multiplier in enumerate(multipliers):
                            m,p,v = model.metrics(pi[a],ref)
                            rows.append(dict(ratio=ratio,theta=theta,seed=seed,multiplier=multiplier,
                                             step=step,m=m,V=v,delta_V=v-bv,delta_log_m=np.log(m/bm)))
                    if step == ACTIVE+FOLLOW:
                        break
                    uniform, completed, _ = rng.random(3)
                    j = (np.cumsum(pi,axis=1)<uniform).sum(axis=1)
                    prob = 1/(1+np.exp(-(-1+model.I[j]+theta*model.A[j])))
                    coefficient = (completed<prob).astype(float)
                    if step < ACTIVE:
                        coefficient = np.where(model.A[j],multipliers,coefficient)
                    u = (1-model.cfg.decay)*u+model.cfg.eta*coefficient[:,None]*model.v[j]
        print(f'R3 NI sensitivity c/t={ratio}: 20 seeds complete',flush=True)
    save_csv('ni_sensitivity',rows)
    metadata('ni_sensitivity',dict(script='analysis/v6_simulation/ni_sensitivity.py',multipliers=multipliers,
               caution='0.78 is a scenario update coefficient, not the measured OneRec response ratio itself.'))


if __name__ == '__main__':
    run()
