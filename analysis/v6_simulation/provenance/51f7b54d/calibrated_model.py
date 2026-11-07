"""Moment-calibrated synthetic model. Calibration is not external validation.

Only eta*t^2/tau and eta*c^2/tau are identified. eta=tau=1 fixes units.
Coordinate caps preserve an attribute memory independently of topic saturation.
Caps, forgetting, heavy-user priors and homogeneous groups remain assumptions.
"""
from dataclasses import dataclass
import numpy as np


@dataclass
class Model:
    supply: float=.02
    topic_prior: float=.15
    topic_target: float=.70
    attribute_target: float=1.13
    ratio: float|None=None
    decay: float=.0002

    def __post_init__(self):
        # Calibration context is fixed at 15% prior, supply-centred topic mean.
        # Ten outside exposures split 3,3,2,2 among four outside directions.
        def response(x):
            p=.15
            mt=p*np.exp(x)/(1-p+p*np.exp(x))
            outside=(np.exp(.3*x)+np.exp(.3*x)+np.exp(.2*x)+np.exp(.2*x))/4
            mo=p/(p+(1-p)*outside)
            return np.log(mt/mo)
        lo,hi=0.,10.
        for _ in range(80):
            mid=(lo+hi)/2
            if response(mid)<self.topic_target:lo=mid
            else:hi=mid
        self.x=(lo+hi)/2
        self.t=np.sqrt(self.x/10)
        self.calibrated_ratio=np.sqrt(self.attribute_target/self.x)
        self.ratio=self.calibrated_ratio if self.ratio is None else self.ratio
        self.c=self.ratio*self.t
        self.v=np.zeros((6,6));self.v[:2,0]=self.t
        self.v[0,1]=self.c*(1-self.supply);self.v[1,1]=-self.c*self.supply
        self.v[2:,2:]=self.t*np.eye(4)
        self.prior=np.array([self.topic_prior*self.supply,self.topic_prior*(1-self.supply)]+[(1-self.topic_prior)/4]*4)
        # 10 positive injection updates remain strictly interior to the caps.
        self.cap=11*np.max(abs(self.v),axis=0)

    def pi(self,u):
        z=u@self.v.T+np.log(self.prior)
        z-=z.max(axis=-1,keepdims=True)
        p=np.exp(z);return p/p.sum(axis=-1,keepdims=True)

    def state(self,p):
        m=p[...,0]+p[...,1]
        with np.errstate(divide='ignore',invalid='ignore'):
            v=np.log(p[...,0]/p[...,1])-np.log(self.supply/(1-self.supply))
        return m,v

    def clip(self,u): return np.clip(u,-self.cap,self.cap)

    def calibration_check(self):
        # Use a separate calibration context, not the heavy user's prior.
        context=Model(self.supply,.15,self.topic_target,self.attribute_target,self.ratio,self.decay)
        topic=np.zeros(6);topic[0]=10*self.t
        outside=np.zeros(6);outside[2:]=self.t*np.array([3,3,2,2])
        topic_logratio=np.log(context.state(context.pi(topic))[0]/context.state(context.pi(outside))[0])
        va=context.state(context.pi(10*self.v[0]))[1]
        vb=context.state(context.pi(10*self.v[1]))[1]
        assert abs(topic_logratio-self.topic_target)<1e-12
        assert abs((va-vb)-10*self.c*self.c)<1e-12
        if abs(self.ratio-self.calibrated_ratio)<1e-12:
            assert abs((va-vb)-self.attribute_target)<1e-12
        return topic_logratio,va-vb
