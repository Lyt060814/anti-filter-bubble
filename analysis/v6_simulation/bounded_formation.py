"""R2 review revision. All defaults are explicitly synthetic assumptions.

Six groups compress a catalogue of identical-within-group item vectors exactly.
The prior topic mass is .04; user norm is capped at .75 after every update.
Reference is SUPPLY (reviewer's permitted alternative), NOT platform mean.
"""
from pathlib import Path
import csv
import hashlib
import json
import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
RATIOS = sorted(set(np.round(np.linspace(0,1,11),2).tolist()+[.15,.59]))
THETAS = np.repeat([0.,.5,1.,2.],20)
SEEDS = np.tile(np.arange(20),4)
T = 1200
CAP = .75
ETA = .05
DECAY = .002
TAU = 1.


def vectors(ratio,supply=.02):
    v = np.zeros((6,6))
    v[:2,0] = 1
    v[0,1],v[1,1] = ratio*(1-supply),-ratio*supply
    v[2:,2:] = np.eye(4)
    return v


def probabilities(u,v,supply):
    prior = np.array([.04*supply,.04*(1-supply)]+[.96/4]*4)
    scores = u@v.T/TAU+np.log(prior)
    scores -= scores.max(axis=-1,keepdims=True)
    p = np.exp(scores)
    return p/p.sum(axis=-1,keepdims=True)


def project(u):
    return u*np.minimum(1,CAP/np.maximum(np.linalg.norm(u,axis=-1,keepdims=True),1e-300))


def metrics(pi,supply):
    m = pi[:,0]+pi[:,1]
    total_skew = np.log(pi[:,0]/pi[:,1])-np.log(supply/(1-supply))
    return m,total_skew


def checks():
    for ratio in RATIOS:
        v = vectors(ratio)
        # With natural positive updates all coordinates stay nonnegative.
        # Hence outside scores >=0, and max topic score <= cap*sqrt(1+c^2).
        bound = .04*np.exp(CAP*np.sqrt(1+ratio**2))
        bound = bound/(.96+bound)
        assert bound<.2
    v = vectors(0)
    rng = np.random.default_rng(1)
    m,z = metrics(probabilities(project(rng.random((80,6))),v,.02),.02)
    assert np.max(abs(z))<1e-12
    # General signed local feedback check tests the smooth update BEFORE norm
    # projection; Proposition 2 does not describe a clipped finite update.
    v = vectors(.59)+rng.normal(0,.1,(6,6))
    u = rng.normal(0,.1,(1,6))
    pi = probabilities(u,v,.02)
    _,before = metrics(pi,.02)
    contrast = v[0]@(v[0]-v[1])
    for eta in (-1e-5,1e-5):
        _,after = metrics(probabilities(u+eta*v[0],v,.02),.02)
        assert abs((after-before)[0]-eta*contrast/TAU)<1e-10
    print('PASS: c=0; signed first-order feedback before projection; analytic m upper bound <20%.')


def run():
    checks()
    rows=[]
    for supply in (.02,.10,.50):
        for ratio in RATIOS:
            v=vectors(ratio,supply)
            u=np.zeros((80,6))
            # Every setting uses the same 20 independent random streams.
            rngs=[np.random.default_rng(int(s)) for s in SEEDS]
            for step in range(T+1):
                pi=probabilities(u,v,supply)
                m,skew=metrics(pi,supply)
                assert np.all((m>=.02)&(m<=.20)), (supply,ratio,step)
                assert np.max(np.linalg.norm(u,axis=1))<=CAP+1e-12
                if ratio==0:
                    assert np.max(abs(skew))<1e-12
                if step%20==0:
                    for i in range(80):
                        rows.append(dict(supply=supply,ratio=ratio,theta=THETAS[i],seed=int(SEEDS[i]),step=step,
                                         m=m[i],V_supply=skew[i],norm=np.linalg.norm(u[i])))
                if step==T: break
                draws=np.array([rng.random(2) for rng in rngs])
                j=(np.cumsum(pi,axis=1)<draws[:,0,None]).sum(axis=1)
                prob=1/(1+np.exp(-(-1+(j<2)+THETAS*(j==0))))
                delta=ETA*(draws[:,1]<prob)[:,None]*v[j]
                u=project((1-DECAY)*u+delta)
            print(f'R2 revision supply={supply} c/t={ratio}: 4 theta x20 seeds complete',flush=True)
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'figures').mkdir(exist_ok=True)
    with (ROOT/'results/formation_bounded.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    summaries=[]
    for supply in (.02,.10,.50):
        for ratio in RATIOS:
            for theta in (0,.5,1,2):
                subset=[r for r in rows if r['supply']==supply and r['ratio']==ratio and r['theta']==theta and r['step']==T]
                summary=dict(supply=supply,ratio=ratio,theta=theta,n=20)
                for key in ('m','V_supply'):
                    x=np.array([r[key] for r in subset]);mean=x.mean();half=2.093*x.std(ddof=1)/np.sqrt(20)
                    summary.update({key+'_mean':mean,key+'_lower':mean-half,key+'_upper':mean+half})
                summaries.append(summary)
    with (ROOT/'results/formation_bounded_summary.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=summaries[0]);w.writeheader();w.writerows(summaries)
    diagnostics=[]
    for s in (.02,.1,.5):
        for r in RATIOS:
            x=[q for q in summaries if q['supply']==s and q['ratio']==r]
            neutral=x[0]
            diagnostics.append(dict(check='neutral_95CI_contains_zero',supply=s,ratio=r,theta=0,
                                    passed=neutral['V_supply_lower']<=0<=neutral['V_supply_upper'],
                                    value=neutral['V_supply_mean']))
            for left,right in zip(x,x[1:]):
                diagnostics.append(dict(check='sample_mean_nondecreasing_theta',supply=s,ratio=r,theta=right['theta'],
                                        passed=right['V_supply_mean']>=left['V_supply_mean']-1e-12,
                                        value=right['V_supply_mean']-left['V_supply_mean']))
        for theta in (.5,1,2):
            x=[q for q in summaries if q['supply']==s and q['theta']==theta]
            for left,right in zip(x,x[1:]):
                diagnostics.append(dict(check='sample_mean_nondecreasing_ratio',supply=s,ratio=right['ratio'],theta=theta,
                                        passed=right['V_supply_mean']>=left['V_supply_mean']-1e-12,
                                        value=right['V_supply_mean']-left['V_supply_mean']))
    with (ROOT/'results/formation_diagnostics.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=diagnostics[0]);w.writeheader();w.writerows(diagnostics)
    print(f'Review diagnostics: {sum(q["passed"] for q in diagnostics)}/{len(diagnostics)} pass; all failures retained, not tuned away.',flush=True)
    fig,axes=plt.subplots(3,4,figsize=(13,8))
    for q,theta in enumerate((0,.5,1,2)):
        for ratio in RATIOS:
            group=[r for r in rows if r['supply']==.02 and r['ratio']==ratio and r['theta']==theta]
            a=np.array([r['m'] for r in group]).reshape(-1,20)
            b=np.array([r['V_supply'] for r in group]).reshape(-1,20)
            steps=np.arange(0,T+1,20)
            colour=plt.cm.viridis(ratio)
            label=f'c/t={ratio}' if ratio in (0,.15,.59,1) else '_nolegend_'
            for ax,x in ((axes[0,q],a),(axes[1,q],b)):
                mean=x.mean(axis=1);half=2.093*x.std(axis=1,ddof=1)/np.sqrt(20)
                ax.plot(steps,mean,color=colour,label=label)
                ax.fill_between(steps,mean-half,mean+half,color=colour,alpha=.07)
            axes[2,q].plot(a.mean(axis=1),b.mean(axis=1),color=colour)
        axes[0,q].set(title=f'theta={theta}; supply A=2%',xlabel='Step',ylabel='Topic exposure m',ylim=(.02,.20))
        axes[1,q].set(xlabel='Step',ylabel='Total skew vs supply')
        axes[2,q].set(xlabel='Mean topic exposure m',ylabel='Mean total skew vs supply')
    axes[0,0].legend(fontsize=7)
    fig.text(.5,.005,'SCENARIO ASSUMPTIONS: norm cap .75; topic prior 4%; A supply 2%. Bands: pointwise 95% MC CI, 20 seeds.',ha='center',fontsize=8)
    fig.tight_layout(rect=(0,.035,1,1))
    for ext in ('png','pdf'): fig.savefig(ROOT/f'figures/formation_bounded.{ext}',dpi=300)
    meta=dict(evidence_type='synthetic scenario assumptions',script='analysis/v6_simulation/bounded_formation.py',
              git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),seeds=list(range(20)),
              ratios=RATIOS,theta=[0,.5,1,2],supply_scan=[.02,.10,.50],main_supply=.02,
              topic_prior=.04,norm_cap=CAP,eta=ETA,decay=DECAY,tau=TAU,steps=T,
              reference='supply p_sup; V_supply is TOTAL skew, not personal V relative to platform average',
              catalogue='six homogeneous vector groups; exact aggregation of arbitrary item multiplicities',
              noise=0,interval='pointwise mean +/- t19(.975)*SD/sqrt(20)',
              attribute_coordinates='A=c*(1-s); B=-c*s; supply-weighted mean zero; A-B contrast c',
              sources=['PR #4 review 2026-11-07','analysis/v6_annotation/agreement.md: DeepSeek v0 1.4%; not supply estimate',
                       'docs/context-recovery/plan_v5_feasibility.md: topic exposure median 1.6%, p90 3.6%'],
              caveat='Exposure proportions are not supply estimates. Both synthetic prior and supply are assumptions. Projection changes Proposition 2 at the boundary.')
    for directory in ('results','figures'):
        (ROOT/directory/'formation_bounded.meta.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
    print(f'PASS: {len(rows)} snapshots, all natural m within 2%-20%; bounded states; zero-contrast invariant.')


if __name__=='__main__': run()
