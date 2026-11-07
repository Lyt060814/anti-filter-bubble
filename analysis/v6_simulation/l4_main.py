"""Issue #21: revised L4-aligned main and zero-contrast lower scenario.

Keep all earlier +1.13 outputs unchanged as an upper scenario. New experiments
reuse the same model, seeds and horizons; only the attribute target changes.
"""
from calibrated_model import Model
from calibrated_run import update,randoms,THETA,SEED,FORM,ACTIVE,FOLLOW
from revised_common import *
import gzip
ARMS=['S0','S1a','S1b','S3','S5','S6']


def run():
    formation=[];endpoints=[];summary=[];cal=[]
    for scenario,target in [('L4_main',.12),('zero_lower',0.)]:
        model=Model(.02,.15,.7,target)
        achieved=model.calibration_check()
        cal.append(dict(scenario=scenario,topic_target=.7,attribute_target=target,
                        t=model.t,c=model.c,ratio=model.ratio,achieved_topic=achieved[0],achieved_attribute=achieved[1]))
        u=np.zeros((80,6));ledger=np.zeros_like(u)
        draws=np.stack([r.random((FORM,2)) for r in randoms()],axis=1)
        for step in range(FORM+1):
            if step%100==0:
                mass,skew=model.state(model.pi(u))
                for i in range(80):formation.append(dict(scenario=scenario,theta=THETA[i],seed=int(SEED[i]),step=step,m=mass[i],V_supply=skew[i]))
                if target==0:assert np.max(abs(skew))<1e-12
            if step<FORM:u,ledger=update(model,u,ledger,draws[step])
        bp=model.pi(u);bm,bv=model.state(bp)
        for q,theta in enumerate((0,.5,1,2)):
            sl=slice(q*20,(q+1)*20)
            mean,err=ci(bv[sl]);summary.append(dict(scenario=scenario,theta=theta,strategy='formation',step=FORM,V_or_delta_V=mean,ci_half=err,delta_log_m=0))
        u=np.tile(u,(6,1,1));u[4]=model.clip(u[4]-ledger)
        draws=np.stack([r.random((ACTIVE+FOLLOW,2)) for r in randoms(10000)],axis=1)
        for step in range(ACTIVE+FOLLOW+1):
            raw=model.pi(u);pi=raw.copy()
            if step<=ACTIVE:
                pi[5,:,0]*=.2;pi[5,:,1]*=.98;pi[5]/=pi[5].sum(axis=-1,keepdims=True)
            mass,skew=model.state(pi)
            if step in (0,ACTIVE,ACTIVE+1,ACTIVE+FOLLOW):
                for a,name in enumerate(ARMS):
                    for i in range(80):endpoints.append(dict(scenario=scenario,theta=THETA[i],seed=int(SEED[i]),strategy=name,step=step,
                         m=mass[a,i],V_supply=skew[a,i],delta_V=skew[a,i]-bv[i],delta_log_m=np.log(mass[a,i]/bm[i]),B_retention=pi[a,i,1]/bp[i,1]))
                    for q,theta in enumerate((0,.5,1,2)):
                        sl=slice(q*20,(q+1)*20);mean,err=ci(skew[a,sl]-bv[sl])
                        summary.append(dict(scenario=scenario,theta=theta,strategy=name,step=step,V_or_delta_V=mean,ci_half=err,
                                            delta_log_m=np.log(mass[a,sl]/bm[sl]).mean()))
            if step==ACTIVE+FOLLOW:break
            if step==ACTIVE:pi=raw
            draw=draws[step];j=(np.cumsum(pi,axis=-1)<draw[None,:,0,None]).sum(axis=-1)
            prob=1/(1+np.exp(-(-1+(j<2)+THETA[None,:]*(j==0))))
            coef=(draw[None,:,1]<prob).astype(float)
            if step<ACTIVE:
                coef[1,j[1]==0]=-1;coef[2,j[2]==0]=.5;coef[3,j[3]==1]=1
            u=model.clip((1-model.decay)*u+coef[:,:,None]*model.v[j])
            assert np.all(abs(u)<=model.cap+1e-12)
    for name,records in [('l4_main_formation',formation),('l4_main_endpoints',endpoints)]:
        with gzip.open(BASE/'results'/f'{name}.csv.gz','wt',encoding='utf8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=records[0]);w.writeheader();w.writerows(records)
    save('l4_main_summary',summary);save('l4_main_calibration',cal)
    assert len(formation)==9760 and len(endpoints)==3840
    source=BASE.parent/'v6/results'
    null=json.loads((source/'l4_null.json').read_text())
    details=dict(evidence_type='synthetic scenarios calibrated to L4 measurement; not independent validation',
        issue=21,main_attribute_target=.12,topic_target=.7,upper_attribute_target=1.13,lower_attribute_target=0,
        lower_rationale='null mean .0923 and SD .1266 do not identify a positive contrast; zero corresponds to existing c/t=0 scan',
        null_mean=null['lv_null_mean'],null_sd=null['lv_null_sd'],
        descriptive_null_subtraction=.12-null['lv_null_mean'],near_null_existing_case=17,near_null_ratio=.2,
        near_null_achieved_target=Model(ratio=.2).calibration_check()[1],
        measured_sources={name:hashlib.sha256((source/name).read_bytes()).hexdigest() for name in ('l4_onerec_v0.json','l4_null.json')},
        seeds=list(range(20)),theta=[0,.5,1,2],supply=.02,prior=.15,formation=FORM,active=ACTIVE,followup=FOLLOW,
        TPR=.8,FPR=.02,S1b=.5,NI_note='~40% of watched response differs in denominator from 78% of neutral mention; prior .39 sensitivity numerically covers ~.40',
        raw_formation='l4_main_formation.csv.gz',raw_endpoints='l4_main_endpoints.csv.gz',compression='gzip CSV',
        limitations='Supply-reference total skew; no platform/personal decomposition. Classifier filtering acts independently of embedding contrast.')
    f,axes=plt.subplots(1,3,figsize=(13,4))
    for theta in (0,.5,1,2):
        group=[r for r in formation if r['scenario']=='L4_main' and r['theta']==theta]
        values=np.array([r['V_supply'] for r in group]).reshape(-1,20)
        mean,err=ci(values);x=np.arange(0,FORM+1,100)
        line,=axes[0].plot(x,mean,label=f'theta={theta}')
        axes[0].fill_between(x,mean-err,mean+err,color=line.get_color(),alpha=.1)
    axes[0].axhline(0,color='grey',linestyle='--',label='zero-contrast lower')
    axes[0].set(xlabel='Formation exposures',ylabel='Total skew vs supply',title='L4 main attribute target +0.12');axes[0].legend(fontsize=7)
    group=[r for r in summary if r['scenario']=='L4_main' and r['theta']==2 and r['step']==ACTIVE]
    for i,r in enumerate(group):
        ax=axes[2] if r['strategy']=='S6' else axes[1]
        ax.errorbar(0 if r['strategy']=='S6' else i,r['V_or_delta_V'],yerr=r['ci_half'],fmt='o',color=plt.cm.tab10(i/10))
    axes[1].set(xticks=range(5),xticklabels=ARMS[:5],ylabel='Endpoint change in total skew',title='Feedback/history controls, theta=2')
    axes[1].axhline(0,color='grey',lw=.5)
    axes[2].set(xticks=[0],xticklabels=['S6'],ylabel='Endpoint change in total skew',title='Output filtering: separate mechanism',ylim=(-1.7,.05))
    axes[2].axhline(0,color='grey',lw=.5)
    fig('l4_main',details,['l4_main.py','calibrated_model.py','calibrated_run.py','revised_common.py'],
        note='Synthetic scenarios; attribute scale matched to the L4 OneRec measurement (+0.12), topic scale to the pilot (+0.70); remaining parameters assumed. Pointwise 95% Monte Carlo intervals, 20 seeds.')
    for r in cal:print(r)
    for r in summary:
        if r['theta']==2 and ((r['scenario']=='L4_main' and r['step'] in (FORM,ACTIVE)) or (r['scenario']=='zero_lower' and r['strategy']=='formation')):print(r)
    print('PASS issue21: 20 seeds per theta, 9760 formation snapshots, 3840 strategy endpoints; zero-contrast invariant and injection targets checked.')


if __name__=='__main__':run()
