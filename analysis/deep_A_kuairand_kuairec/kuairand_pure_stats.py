import pandas as pd, numpy as np
D='/home/user/data/kuairand/KuaiRand-Pure/KuaiRand-Pure/data/'
r=pd.read_csv(D+'log_random_4_22_to_5_08_pure.csv')
s1=pd.read_csv(D+'log_standard_4_08_to_4_21_pure.csv')
s2=pd.read_csv(D+'log_standard_4_22_to_5_08_pure.csv')
for n,d in [('random',r),('std_0408_0421',s1),('std_0422_0508',s2)]:
    print(n, 'rows',len(d),'users',d.user_id.nunique(),'videos',d.video_id.nunique(),'dates',d.date.min(),d.date.max(),
          'is_rand==1',int(d.is_rand.sum()),'is_hate',int(d.is_hate.sum()),'hate_rate %.5f'%d.is_hate.mean(),
          'click %.4f like %.5f long_view %.4f'%(d.is_click.mean(),d.is_like.mean(),d.long_view.mean()))
    print('   tab dist', d.tab.value_counts().sort_index().to_dict())
a=pd.concat([s1,s2,r])
print('ALL rows',len(a),'users',a.user_id.nunique(),'videos',a.video_id.nunique(),'share is_rand %.4f'%a.is_rand.mean(),'hate',int(a.is_hate.sum()))
print('hate in rand',int(a[a.is_rand==1].is_hate.sum()),'hate in non-rand',int(a[a.is_rand==0].is_hate.sum()))
print('users with >=1 hate',a[a.is_hate==1].user_id.nunique())
v=pd.read_csv(D+'video_features_basic_pure.csv')
print('videos in basic',len(v),'tag null',v.tag.isna().sum())
tags=v.tag.dropna().astype(str).str.split(',')
print('n tags per video',tags.str.len().value_counts().to_dict())
from collections import Counter
c=Counter(t for l in tags for t in l); print('distinct tags',len(c),'top',c.most_common(10))
print(v.video_type.value_counts().to_dict())
u=pd.read_csv(D+'user_features_pure.csv'); print('user feat rows',len(u), u.user_active_degree.value_counts().to_dict())
# per-user counts
cnt=a.groupby('user_id').size(); print('interactions per user: median',cnt.median(),'mean %.1f'%cnt.mean())
rc=r.groupby('user_id').size(); print('random per user: median',rc.median(),'min',rc.min(),'max',rc.max())
