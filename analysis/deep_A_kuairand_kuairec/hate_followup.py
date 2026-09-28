# Exploratory: after a user hates a video with tag T, does the share of tag-T videos in that user's later
# *standard* (non-random) exposures drop? Compare to a control event: non-hated, not-clicked exposures.
import pandas as pd, numpy as np
D='/home/user/data/kuairand/KuaiRand-Pure/KuaiRand-Pure/data/'
r=pd.read_csv(D+'log_random_4_22_to_5_08_pure.csv'); s1=pd.read_csv(D+'log_standard_4_08_to_4_21_pure.csv'); s2=pd.read_csv(D+'log_standard_4_22_to_5_08_pure.csv')
v=pd.read_csv(D+'video_features_basic_pure.csv')[['video_id','tag']]
v['tag1']=v.tag.astype(str).str.split(',').str[0]
a=pd.concat([s1,s2,r]).merge(v[['video_id','tag1']],on='video_id',how='left').sort_values(['user_id','time_ms'])
std=a[a.is_rand==0]
def shares(events, label, rng=np.random.default_rng(0)):
    pre,post,npre,npost=[],[],[],[]
    g=dict(tuple(std.groupby('user_id')))
    for _,e in events.iterrows():
        h=g.get(e.user_id)
        if h is None: continue
        b=h[h.time_ms<e.time_ms]; f=h[h.time_ms>e.time_ms]
        if len(b)<5 or len(f)<5: continue
        pre.append((b.tag1==e.tag1).mean()); post.append((f.tag1==e.tag1).mean()); npre.append(len(b)); npost.append(len(f))
    pre,post=np.array(pre),np.array(post)
    d=post-pre
    print(f'{label}: n={len(d)} mean pre={pre.mean():.4f} post={post.mean():.4f} diff={d.mean():+.4f} (se {d.std(ddof=1)/np.sqrt(len(d)):.4f}); median #std before {np.median(npre)}, after {np.median(npost)}')
    return d
hate=a[a.is_hate==1]
dh=shares(hate,'HATE events (all)')
shares(hate[hate.is_rand==1],'HATE on random-exposed video')
shares(hate[hate.is_rand==0],'HATE on standard video')
ctrl=a[(a.is_hate==0)&(a.is_click==0)].sample(5000,random_state=0)
dc=shares(ctrl,'CONTROL: not clicked, not hated (5000 sampled)')
ctrl2=a[(a.is_hate==0)&(a.long_view==1)].sample(5000,random_state=0)
shares(ctrl2,'CONTROL2: long_view (5000 sampled)')
