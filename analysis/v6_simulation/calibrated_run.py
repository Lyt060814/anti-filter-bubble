"""R3 calibration, formation and escape. All raw values are synthetic."""
from calibrated_model import Model
from bounded_formation import RATIOS
from revised_common import *
THETA=np.repeat([0.,.5,1.,2.],20)
SEED=np.tile(np.arange(20),4)
ARMS=['S0','S1a','S1b','S2','S3','S4','S5','S6','S7','S8','S9']
FORM=6000;ACTIVE=1000;FOLLOW=2000
SCRIPTS=['calibrated_model.py','calibrated_run.py','revised_common.py']


def cases():
    for family,attr in [('group',1.13),('conflict',.65)]:
        anchor=Model(attribute_target=attr).calibrated_ratio
        for supply in (.02,.1,.5):
            for prior in (.1,.15,.2):
                for ratio in sorted(set(RATIOS+[anchor])):
                    yield dict(family=family,supply=supply,prior=prior,topic_target=.7,attribute_target=attr,ratio=ratio,decay=.0002,scan='main_grid')
        for target,level in [('topic',.5),('topic',1.5),('attribute',.5),('attribute',1.5)]:
            topic=.7*level if target=='topic' else .7
            attribute=attr*level if target=='attribute' else attr
            yield dict(family=family,supply=.02,prior=.15,topic_target=topic,attribute_target=attribute,ratio=None,decay=.0002,scan=f'{target}_x{level}')
        yield dict(family=family,supply=.02,prior=.15,topic_target=.7,attribute_target=attr,ratio=None,decay=.002,scan='forgetting_x10')


def randoms(seedoffset=0): return [np.random.default_rng(seedoffset+int(s)) for s in SEED]


def update(model,u,ledger,draw,theta=THETA):
    p=model.pi(u)
    j=(np.cumsum(p,axis=-1)<draw[:,0,None]).sum(axis=-1)
    finish=draw[:,1]<1/(1+np.exp(-(-1+(j<2)+theta*(j==0))))
    delta=finish[:,None]*model.v[j]
    raw=(1-model.decay)*u+delta
    factor=np.minimum(1,np.divide(model.cap,abs(raw),out=np.ones_like(raw),where=raw!=0))
    return raw*factor,((1-model.decay)*ledger+delta*(j==0)[:,None])*factor


def run():
    (BASE/'results').mkdir(exist_ok=True)
    keys=['case','family','scan','supply','prior','topic_target','attribute_target','ratio','decay','theta','seed','step']
    # Raw endpoints for every configuration; dense traces only in nominated main cases.
    forms=[];form_summary=[];summaries=[];lives=[];calibrations=[]
    handles={};writers={}
    for family in ('group','conflict'):
        for supply in (.02,.1,.5):
            key=(family,supply)
            path=BASE/'results'/f'calibrated_escape_{family}_s{supply}.csv'
            handles[key]=path.open('w',newline='')
            writers[key]=csv.DictWriter(handles[key],fieldnames=keys+['strategy','m','V_supply','delta_V','delta_log_m','B_retention','effort','delta_vs_control'])
            writers[key].writeheader()
    for caseid,case in enumerate(cases()):
        model=Model(case['supply'],case['prior'],case['topic_target'],case['attribute_target'],case['ratio'],case['decay'])
        case['ratio']=model.ratio
        topic,attribute=model.calibration_check()
        calibrations.append(dict(case=caseid,**case,t=model.t,c=model.c,achieved_topic=topic,
            achieved_attribute=attribute,attribute_target_matched=abs(model.ratio-model.calibrated_ratio)<1e-12,
            eta=1,tau=1,cap_topic=model.cap[0],cap_attribute=model.cap[1]))
        base=dict(case=caseid,**case)
        primary=(case['scan']=='main_grid' and case['supply']==.02 and case['prior']==.15)
        dense=primary and any(abs(model.ratio-r)<1e-12 for r in (0,.15,.59,1,model.calibrated_ratio))
        u=np.zeros((80,6));ledger=np.zeros_like(u)
        formdraw=np.stack([r.random((FORM,2)) for r in randoms()],axis=1)
        for step in range(FORM+1):
            if step%100==0:
                m,v=model.state(model.pi(u))
                for i in range(80):forms.append(dict(**base,theta=THETA[i],seed=int(SEED[i]),step=step,m=m[i],V_supply=v[i]))
                for q,theta in enumerate((0,.5,1,2)):
                    sl=slice(q*20,(q+1)*20);mm,em=ci(m[sl]);vv,ev=ci(v[sl])
                    form_summary.append(dict(**base,theta=theta,step=step,m=mm,m_ci=em,V=vv,V_ci=ev))
            if step<FORM:u,ledger=update(model,u,ledger,formdraw[step])
        original=u.copy();bp=model.pi(original);bm,bv=model.state(bp)
        u=np.tile(original,(11,1,1));u[6]=model.clip(u[6]-ledger);u[10]=0
        effort=np.zeros((11,80));effort[[6,10]]=1
        escapedraw=np.stack([r.random((ACTIVE+FOLLOW,2)) for r in randoms(10000)],axis=1)
        trajectory=[]
        for step in range(ACTIVE+FOLLOW+1):
            rawpi=model.pi(u);p=rawpi.copy()
            if step<=ACTIVE:
                p[9]=model.pi(np.tile(original.mean(axis=0),(80,1)))
                p[7,:,0]*=.2;p[7,:,1]*=.98;p[7]/=p[7].sum(axis=-1,keepdims=True)
                p[8,:,:2]=0;p[8]/=p[8].sum(axis=-1,keepdims=True)
            m,v=model.state(p);trajectory.append(v.copy())
            if step in (0,ACTIVE,ACTIVE+1,ACTIVE+FOLLOW) or (dense and step%100==0):
                with np.errstate(divide='ignore'): logm=np.log(m/bm)
                vals=dict(delta_V=v-bv,delta_log_m=logm,B_retention=p[:,:,1]/bp[:,1],effort=effort,delta_vs_control=v-v[0])
                for arm,name in enumerate(ARMS):
                    for i in range(80):
                        writers[(case['family'],case['supply'])].writerow(dict(**base,theta=THETA[i],seed=int(SEED[i]),step=step,strategy=name,m=m[arm,i],V_supply=v[arm,i],**{k:x[arm,i] for k,x in vals.items()}))
                    for q,theta in enumerate((0,.5,1,2)):
                        item=dict(**base,theta=theta,step=step,strategy=name)
                        for key,x in vals.items():
                            xx=x[arm,q*20:(q+1)*20]
                            if np.isfinite(xx).all(): mean,err=ci(xx)
                            else:mean,err=np.nan,np.nan
                            item.update({key:mean,key+'_ci':err})
                        summaries.append(item)
            if step==ACTIVE+FOLLOW:break
            if step==ACTIVE:p=rawpi
            draw=escapedraw[step]
            j=(np.cumsum(p,axis=-1)<draw[None,:,0,None]).sum(axis=-1)
            finish=draw[None,:,1]<1/(1+np.exp(-(-1+(j<2)+THETA[None,:]*(j==0))))
            coeff=finish.astype(float)
            if step<ACTIVE:
                for arm,value in ((1,-1.),(2,.5),(3,0.)):
                    take=j[arm]==0;coeff[arm,take]=value;effort[arm]+=take
                take=j[4]==1;coeff[4,take]=1;effort[4]+=take
                if step==0:effort[7:10]+=1
            u=model.clip((1-model.decay)*u+coeff[:,:,None]*model.v[j])
            if step<ACTIVE and step%10==0:u[5]=model.clip(u[5]+model.v[1]);effort[5]+=1
            assert np.all(abs(u)<=model.cap+1e-12)
        trajectory=np.array(trajectory)
        for arm,name in enumerate(ARMS):
            for i in range(80):
                for reference in ('pre_intervention','matched_S0'):
                    ref=bv[i] if reference=='pre_intervention' else trajectory[ACTIVE:,0,i]
                    gain=ref-trajectory[ACTIVE:,arm,i];reduction=gain[0]
                    hit=np.flatnonzero(gain[1:]<=reduction/2) if reduction>0 else []
                    lives.append(dict(**base,theta=THETA[i],seed=int(SEED[i]),strategy=name,reference=reference,
                        initial_reduction=reduction,reduction_present=bool(np.isfinite(reduction) and reduction>0),
                        half_life=int(hit[0])+1 if len(hit) else np.nan,
                        right_censored=bool(np.isfinite(reduction) and reduction>0 and not len(hit)),horizon=FOLLOW))
        print(f'R3 calibrated {caseid}: {case["family"]} prior={case["prior"]} supply={case["supply"]} r={model.ratio:.3f} {case["scan"]}',flush=True)
    for f in handles.values():f.close()
    # Family split keeps individual CSV files below GitHub's 100 MB limit.
    for family in ('group','conflict'):save(f'calibrated_formation_{family}',[r for r in forms if r['family']==family])
    save('calibration_targets',calibrations);save('calibrated_formation_summary',form_summary)
    save('calibrated_escape_summary',summaries);save('calibrated_persistence',lives)
    details=dict(evidence_type='synthetic simulation moment-matched to repository-reported v5 pilot anchors; not external validation',
        seeds=list(range(20)),theta=[0,.5,1,2],ratio_scan=RATIOS,additional_ratio='fitted sqrt(attribute_target / topic_scale)',
        prior_scan=[.1,.15,.2],supply_scan=[.02,.1,.5],calibration_context_prior=.15,
        topic_target=.7,attribute_targets=[1.13,.65],target_sensitivity='one at a time x0.5/x1.5 at prior=.15,supply=.02,fitted ratio; not joint uncertainty',
        eta_tau='eta=tau=1 unit convention; only eta*t^2/tau and eta*c^2/tau identified',
        cap='coordinatewise 11*max(abs(item coordinate)); assumed; 10-step injection remains interior',
        forgetting=[.0002,.002],formation=FORM,active=ACTIVE,followup=FOLLOW,
        reference='SUPPLY: total skew, not personal platform-referenced skew',classifier='assumed TPR=.8 FPR=.02 pending validated v2',
        OneRec_NI='positive response ~78% of neutral mention; S1b uses assigned +0.5 update, not an estimate of eta',
        source='docs/context-recovery/plan_v5_feasibility.md sections 3.1-3.3; PR #4 approval review',
        raw_trace_policy='formation every100 for all cases; escape all seed endpoints plus every100 in nominated main cases',
        deletion='remove surviving A ledger with coordinate clipping factors; not counterfactual replay',
        censoring='explicit reduction_present/right_censored; no reduction and unobserved half-lives are NaN')
    plots(form_summary,summaries,details)
    print(f'PASS calibrated run: {len(calibrations)} cases; matched injection targets checked; every state bounded.')


def plots(forms,escapes,details):
    f,axes=plt.subplots(3,4,figsize=(13,8))
    for q,theta in enumerate((0,.5,1,2)):
        selection=[r for r in forms if r['family']=='group' and r['scan']=='main_grid' and r['supply']==.02 and r['prior']==.15 and r['theta']==theta]
        anchor=Model().calibrated_ratio
        for ratio in (0,.15,.59,1,anchor):
            g=[r for r in selection if abs(r['ratio']-ratio)<1e-12]
            for ax,key in ((axes[0,q],'m'),(axes[1,q],'V')):
                x=np.array([r['step'] for r in g]);y=np.array([r[key] for r in g]);e=np.array([r[key+'_ci'] for r in g])
                line,=ax.plot(x,y,label=f'r={ratio:.2f}');ax.fill_between(x,y-e,y+e,color=line.get_color(),alpha=.1)
        axes[0,q].set(title=f'theta={theta}; prior=.15; supply=.02',xlabel='Formation exposure',ylabel='Topic share m')
        axes[1,q].set(xlabel='Formation exposure',ylabel='Total skew vs supply')
        terminal=[r for r in selection if r['step']==FORM]
        x=np.array([r['ratio'] for r in terminal]);y=np.array([r['V'] for r in terminal]);e=np.array([r['V_ci'] for r in terminal])
        axes[2,q].plot(x,y,color='black');axes[2,q].fill_between(x,y-e,y+e,alpha=.15,color='black')
        axes[2,q].set(xlabel='Generating c/t: full sweep + fitted point',ylabel='Terminal total skew vs supply')
    axes[0,0].legend(fontsize=6)
    fig('formation_calibrated',details,SCRIPTS)
    for name,persistent in [('escape_calibrated',False),('persistence_calibrated',True)]:
        f,axes=plt.subplots(1,2,figsize=(11,4.5))
        for ax,ratio in zip(axes,(.59,anchor)):
            for a,arm in enumerate(ARMS):
                g=[r for r in escapes if r['family']=='group' and r['scan']=='main_grid' and r['supply']==.02 and r['prior']==.15 and r['theta']==2 and r['strategy']==arm and abs(r['ratio']-ratio)<1e-12]
                color=plt.cm.tab20(a/20)
                if persistent:
                    g=[r for r in g if r['step']>=ACTIVE]
                    x=np.array([r['step']-ACTIVE for r in g]);y=np.array([r['delta_vs_control'] for r in g]);e=np.array([r['delta_vs_control_ci'] for r in g])
                    ax.plot(x,y,label=arm,color=color);ax.fill_between(x,y-e,y+e,alpha=.1,color=color)
                elif arm!='S7':
                    r=next(r for r in g if r['step']==ACTIVE)
                    ax.errorbar(r['delta_log_m'],r['delta_V'],xerr=r['delta_log_m_ci'],yerr=r['delta_V_ci'],fmt='o',color=color,label=arm)
            ax.set(title=f'r={ratio:.2f}; supply=.02; prior=.15; theta=2',xlabel='Follow-up exposures' if persistent else 'Change log topic share',ylabel='Skew difference from S0' if persistent else 'Change total skew vs supply')
            ax.legend(fontsize=6,ncol=2);ax.axhline(0,color='grey',lw=.5)
        fig(name,details,SCRIPTS)


if __name__=='__main__':run()
