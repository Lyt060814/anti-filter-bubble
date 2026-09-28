"""Minimal CPU run of CIRS's original KuaiEnv (copied verbatim from cirs-codes) with trivial policies.
Only changes: torch is stubbed (unused by step()), distance matrix skipped, data rebuilt from KuaiRec 2.0 CSVs."""
import sys, os, time, collections, numpy as np, pandas as pd, random
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path[:0]=[HERE, os.path.join(HERE,'shim')]
import kuaishouEnv_orig as ke
ke.DATAPATH=os.path.join(HERE,'data')
t0=time.time(); env=ke.KuaishouEnv(num_leave_compute=1, leave_threshold=0, max_turn=100)
print('env loaded in %.1fs; mat shape'%(time.time()-t0), env.mat.shape)
mat=env.mat; feats=env.list_feat_small; nU,nI=mat.shape
# dominant categories (DORL-style MCD): categories of 'positive' big-matrix interactions (watch_ratio >= 80th pct), top covering 80%
S="/home/user/data/kuairec/KuaiRec 2.0/data/"
big=pd.read_csv(S+"big_matrix.csv",usecols=["video_id","watch_ratio"])
thr=np.percentile(big.watch_ratio,80); pos=big[big.watch_ratio>=thr]
cat=pd.read_csv(S+"item_categories.csv"); cat['feat']=cat.feat.apply(eval); cmap=dict(zip(cat.video_id,cat.feat))
cnt=collections.Counter(c for v in pos.video_id for c in cmap[v]); tot=sum(cnt.values())
dom=[];cum=0
for c,n in cnt.most_common():
    if cum/tot>0.8: break
    dom.append(c); cum+=n
dom=set(dom); print('big-matrix positive threshold watch_ratio>=%.3f; %d dominant categories of %d:'%(thr,len(dom),len(cnt)),sorted(dom))
pop=mat.mean(0)  # item mean watch_ratio in small matrix (uses TEST data -> leaky)
bm=big.groupby('video_id').watch_ratio.mean().clip(upper=5); pop_big=np.array([bm.get(v,0.0) for v in env.lbe_photo.classes_])  # TRAIN-only (big matrix) item mean
def policy_factory(name, eps=0.1, N=1):
    def act(u, hist):
        seen=set(hist)
        if name=='random': return random.randrange(nI)
        if name in('oracle_greedy','eps_greedy','oracle_div'): scores=mat[u]
        elif name.endswith('_big'): scores=pop_big
        else: scores=pop
        order=np.argsort(-scores)
        if name=='eps_greedy' and random.random()<eps: return random.randrange(nI)
        if name in('oracle_div','pop_div','pop_div_big'):
            recent=set(c for a in hist[-N:] for c in feats[a])
            for a in order:
                if a not in seen and not (set(feats[a])&recent): return int(a)
        for a in order:
            if a not in seen: return int(a)
    return act
def run(pname, N, thr_leave, max_turn, n_traj=100, seed=0):
    random.seed(seed); np.random.seed(seed)
    e=ke.KuaishouEnv(mat=env.mat,lbe_user=env.lbe_user,lbe_photo=env.lbe_photo,list_feat=env.list_feat,df_photo_env=env.df_photo_env,df_dist_small=None,num_leave_compute=N,leave_threshold=thr_leave,max_turn=max_turn)
    pol=policy_factory(pname,N=N); R=[];L=[];single=[];mcd=[];ncat=[]
    for _ in range(n_traj):
        e.reset(); u=e.cur_user; hist=[]; done=False
        while not done:
            a=pol(u,hist); _,r,done,info=e.step(a); hist.append(a)
        R.append(info['cum_reward']); L.append(len(hist)); single.append(info['cum_reward']/len(hist))
        mcd.append(np.mean([bool(set(feats[a])&dom) for a in hist])); ncat.append(len(set(c for a in hist for c in feats[a])))
    return dict(policy=pname,N=N,max_turn=max_turn,cum_reward=np.mean(R),length=np.mean(L),single_round=np.mean(single),MCD=np.mean(mcd),n_categories=np.mean(ncat))
rows=[]
for (N,thr_l,mt,label) in [(1,0,100,'CIRS setting (N=1,thr=0,max=100)'),(4,0,30,'DORL setting (N=4,M=0,max=30)')]:
    for p in ['random','pop_greedy','oracle_greedy','eps_greedy','pop_greedy_big','pop_div_big','pop_div','oracle_div']:
        d=run(p,N,thr_l,mt); d['setting']=label; rows.append(d)
df=pd.DataFrame(rows)[['setting','policy','cum_reward','length','single_round','MCD','n_categories']]
pd.set_option('display.width',200); print(df.round(3).to_string(index=False))
df.to_csv(os.path.join(HERE,'kuaienv_trivial_results.csv'),index=False)
