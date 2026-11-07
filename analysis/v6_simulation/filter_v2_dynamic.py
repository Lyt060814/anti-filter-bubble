"""Main fitted cases only: dynamic measured-classifier sensitivity, not full-grid rerun."""
from calibrated_model import Model
from calibrated_run import update,randoms,THETA,SEED,FORM,ACTIVE,FOLLOW
from pathlib import Path
import csv,gzip,json,hashlib,subprocess
import numpy as np
BASE=Path(__file__).parent


def run():
    rates=json.loads((BASE/'results/v2_detection_inputs.json').read_text())
    output=BASE/'results/filter_v2_dynamic.csv.gz';n=0
    with gzip.open(output,'wt',encoding='utf8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['family','theta','seed','strategy','step','m','V_supply','delta_V','delta_log_m','B_retention','delta_vs_control']);writer.writeheader()
        for family,attribute in [('group',1.13),('conflict',.65)]:
            model=Model(.02,.15,.7,attribute)
            u=np.zeros((80,6));ledger=np.zeros_like(u)
            draws=np.stack([r.random((FORM,2)) for r in randoms()],axis=1)
            for step in range(FORM):u,ledger=update(model,u,ledger,draws[step])
            bp=model.pi(u);bm,bv=model.state(bp);u=np.tile(u,(3,1,1))
            draws=np.stack([r.random((ACTIVE+FOLLOW,2)) for r in randoms(10000)],axis=1)
            for step in range(ACTIVE+FOLLOW+1):
                raw=model.pi(u);pi=raw.copy()
                if step<=ACTIVE:
                    for arm,alpha,beta in ((1,.8,.02),(2,rates['recall'],rates['false_positive_rate'])):
                        pi[arm,:,0]*=1-alpha;pi[arm,:,1]*=1-beta;pi[arm]/=pi[arm].sum(axis=-1,keepdims=True)
                m,v=model.state(pi)
                if step%100==0 or step==ACTIVE+1:
                    for arm,name in enumerate(('S0','S6_assumed','S6_v2_crosscheck')):
                        for i in range(80):
                            writer.writerow(dict(family=family,theta=THETA[i],seed=int(SEED[i]),strategy=name,step=step,m=m[arm,i],V_supply=v[arm,i],
                                delta_V=v[arm,i]-bv[i],delta_log_m=np.log(m[arm,i]/bm[i]),B_retention=pi[arm,i,1]/bp[i,1],delta_vs_control=v[arm,i]-v[0,i]));n+=1
                    if family=='group' and step==ACTIVE:
                        for arm,name in enumerate(('S0','S6_assumed','S6_v2_crosscheck')):
                            print(name,'mean dV=',(v[arm,60:]-bv[60:]).mean(),'mean dlogm=',np.log(m[arm,60:]/bm[60:]).mean())
                if step==ACTIVE+FOLLOW:break
                if step==ACTIVE:pi=raw
                draw=draws[step];j=(np.cumsum(pi,axis=-1)<draw[None,:,0,None]).sum(axis=-1)
                prob=1/(1+np.exp(-(-1+(j<2)+THETA[None,:]*(j==0))))
                delta=(draw[None,:,1]<prob)[:,:,None]*model.v[j]
                u=model.clip((1-model.decay)*u+delta)
    assert n==15360
    meta=dict(script='analysis/v6_simulation/filter_v2_dynamic.py',git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        evidence_type='main-case synthetic dynamic sensitivity using measured cross-model classifier rates; not gold-standard accuracy',
        source_sha256={name:hashlib.sha256((BASE/name).read_text(encoding='utf8').encode()).hexdigest() for name in ('filter_v2_dynamic.py','calibrated_model.py','calibrated_run.py')},
        v2_input_sha256=hashlib.sha256((BASE/'results/v2_detection_inputs.json').read_bytes()).hexdigest(),
        rates=rates,supply=.02,prior=.15,theta=[0,.5,1,2],seeds=list(range(20)),families=['group','conflict'],
        formation=FORM,active=ACTIVE,followup=FOLLOW,interval=100,rows=n,compression='gzip CSV',
        caveat='Only main fitted cases rerun; does not replace the full-grid assumed-classifier benchmark. Rate uncertainty not propagated.')
    output.with_name('filter_v2_dynamic.meta.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
    print('PASS v2 dynamic filtering sensitivity: 15,360 per-seed records, benchmark and cross-check arms.')


if __name__=='__main__':run()
