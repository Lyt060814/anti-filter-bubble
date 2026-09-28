# Is exposure under the standard (algorithmic) policy more concentrated in categories than under random exposure?
import pandas as pd, numpy as np
D='/home/user/data/kuairand/KuaiRand-Pure/KuaiRand-Pure/data/'
r=pd.read_csv(D+'log_random_4_22_to_5_08_pure.csv'); s=pd.concat([pd.read_csv(D+'log_standard_4_08_to_4_21_pure.csv'),pd.read_csv(D+'log_standard_4_22_to_5_08_pure.csv')])
v=pd.read_csv(D+'video_features_basic_pure.csv'); v['tag1']=v.tag.astype(str).str.split(',').str[0]
t=dict(zip(v.video_id,v.tag1))
for n,d in [('standard',s),('random',r)]:
    d=d.assign(tag1=d.video_id.map(t))
    p=d.tag1.value_counts(normalize=True)
    H=-(p*np.log2(p)).sum()
    print(f'{n}: global top-1 tag share {p.iloc[0]:.3f}, top-5 {p.iloc[:5].sum():.3f}, entropy {H:.2f} bits, distinct {len(p)}')
# per-user: sample 20 exposures from each log for users with >=20 in both
rng=np.random.default_rng(0); a=[];b=[];ea=[];eb=[]
sg=s.assign(tag1=s.video_id.map(t)).groupby('user_id'); rg=r.assign(tag1=r.video_id.map(t)).groupby('user_id')
for u,gs in sg:
    if len(gs)<20 or u not in rg.groups: continue
    gr=rg.get_group(u)
    if len(gr)<20: continue
    xs=gs.tag1.sample(20,random_state=0); xr=gr.tag1.sample(20,random_state=0)
    a.append(xs.nunique()); b.append(xr.nunique()); ea.append(xs.value_counts().iloc[0]/20); eb.append(xr.value_counts().iloc[0]/20)
a,b,ea,eb=map(np.array,(a,b,ea,eb))
print(f'users compared: {len(a)}; distinct tags in 20 exposures: standard {a.mean():.2f} vs random {b.mean():.2f}; top-tag share: standard {ea.mean():.3f} vs random {eb.mean():.3f}; share users with standard more concentrated: {(ea>eb).mean():.3f}')
for n,d in [('standard',s),('random',r)]:
    print(n,'click %.3f long_view %.3f like %.4f hate %.5f'%(d.is_click.mean(),d.long_view.mean(),d.is_like.mean(),d.is_hate.mean()))
