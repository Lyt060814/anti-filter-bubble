"""Supplementary OneRec-like NI response calibration, independent of assigned +.5 arm.

Fit an NI pulse coefficient so the topic injection response is .78 of neutral
mention, then compare its dynamics to matched natural and negative-feedback arms.
Probe targets .39/.78/1.17. Caps can make the upper target unattainable; retain
the achieved response and residual rather than claim a successful fit.
"""
from calibrated_model import Model
from calibrated_run import update,randoms,THETA,SEED,FORM,ACTIVE,FOLLOW
from revised_common import *


def topic_response(m,coef):
    context=Model(m.supply,.15,m.topic_target,m.attribute_target,m.ratio,m.decay)
    topic=np.zeros(6);topic[0]=10*m.t*coef
    outside=np.zeros(6);outside[2:]=m.t*coef*np.array([3,3,2,2])
    # Actual capped pulse, not the uncapped fitted score.
    return np.log(context.state(context.pi(context.clip(topic)))[0]/context.state(context.pi(context.clip(outside)))[0])


def fit(m,target):
    lo,hi=0.,4.
    for _ in range(80):
        mid=(lo+hi)/2
        if topic_response(m,mid)<target:lo=mid
        else:hi=mid
    coef=(lo+hi)/2
    return coef,topic_response(m,coef)


def run():
    rows=[];cal=[]
    for family,attribute in [('group',1.13),('conflict',.65)]:
        for ni_ratio in (.39,.78,1.17):
            m=Model(.02,.15,.7,attribute)
            coefficient,achieved=fit(m,.7*ni_ratio)
            cal.append(dict(family=family,relative_response_target=ni_ratio,topic_response_target=.7*ni_ratio,
                            coefficient=coefficient,achieved_topic_response=achieved,
                            residual=achieved-.7*ni_ratio,attainable=abs(achieved-.7*ni_ratio)<1e-9))
            u=np.zeros((80,6));ledger=np.zeros_like(u)
            draws=np.stack([r.random((FORM,2)) for r in randoms()],axis=1)
            for step in range(FORM):u,ledger=update(m,u,ledger,draws[step])
            bm,bv=m.state(m.pi(u));u=np.tile(u,(3,1,1))
            draws=np.stack([r.random((ACTIVE+FOLLOW,2)) for r in randoms(10000)],axis=1)
            for step in range(ACTIVE+FOLLOW+1):
                pi=m.pi(u);mass,v=m.state(pi)
                if step in (0,ACTIVE,ACTIVE+FOLLOW):
                    for arm,name in enumerate(('S0','S1a','S1b_calibrated')):
                        for i in range(80):
                            rows.append(dict(family=family,relative_response_target=ni_ratio,theta=THETA[i],seed=int(SEED[i]),
                                strategy=name,step=step,m=mass[arm,i],delta_V=v[arm,i]-bv[i],
                                delta_log_m=np.log(mass[arm,i]/bm[i]),delta_vs_control=v[arm,i]-v[0,i]))
                if step==ACTIVE+FOLLOW:break
                draw=draws[step];j=(np.cumsum(pi,axis=-1)<draw[None,:,0,None]).sum(axis=-1)
                prob=1/(1+np.exp(-(-1+(j<2)+THETA[None,:]*(j==0))))
                coef=(draw[None,:,1]<prob).astype(float)
                if step<ACTIVE:
                    coef[1,j[1]==0]=-1
                    coef[2,j[2]==0]=coefficient
                u=m.clip((1-m.decay)*u+coef[:,:,None]*m.v[j])
    save('ni_response_calibration',cal);save('ni_calibrated_sensitivity',rows)
    meta('ni_response_calibration',dict(evidence_type='scenario calibration to repository-reported positive response ~78% of neutral mention',
         source='docs/context-recovery/plan_v5_feasibility.md section 3.2',targets=[.39,.78,1.17],
         context_prior=.15,topic_target=.7,raw_results='ni_calibrated_sensitivity.csv',seeds=list(range(20)),
         warning='Upper response may be unattainable under coordinate caps; all residuals and attainable flags retained.'),
         ['ni_calibration.py','calibrated_model.py','calibrated_run.py','revised_common.py'])
    for r in cal:print(r)


if __name__=='__main__':run()
