"""Profile the public (sampled) ShortVideo dataset (Shang et al., WWW'25 Companion).

The CSV has one row per (interaction x tag x category-path node): a video with 3 tags and a
level-1/2/3 path appears 9+ times. We collapse to one row per interaction and one row per video.
"""
import pandas as pd
from common import SV_RAW, SV_INTER, SV_VIDEOS

df = pd.read_csv(SV_RAW)
KEY = ['user_id', 'pid', 'exposed_time']
print(f'raw rows {len(df):,}; columns {list(df.columns)}')

# --- videos: category path + tags
vid = df.groupby('pid').agg(
    root_id=('root_id', 'first'),
    n_root=('root_id', 'nunique'),
    l2=('category_id', lambda s: sorted(set(s[df.loc[s.index, 'category_level'] == 2]))),
    l3=('category_id', lambda s: sorted(set(s[df.loc[s.index, 'category_level'] == 3]))),
    tags=('tag_name', lambda s: sorted(set(s.dropna().astype(str)))),
    title=('title', 'first'), duration=('duration', 'first'),
    author_id=('author_id', 'first'), author_fans_count=('author_fans_count', 'max'))
vid.to_parquet(SV_VIDEOS)

# --- interactions
inter = df.drop(columns=['tag_name', 'category_id', 'category_level', 'parent_id']).drop_duplicates(KEY)
for c in ['watch_time', 'cvm_like', 'click', 'hate']:
    assert df.groupby(KEY)[c].nunique().max() == 1, c
inter.to_parquet(SV_INTER)

print(f'\ninteractions {len(inter):,} | users {inter.user_id.nunique():,} | videos {inter.pid.nunique():,} | authors {inter.author_id.nunique():,}')
print('paper (full, not public): 10,000 users | 153,561 videos | 1,019,568 interactions')
print('dates', sorted(inter.p_date.unique()))
pu = inter.groupby('user_id').size()
print('\ninteractions per user:', pu.describe(percentiles=[.25, .5, .75, .9, .99]).round(1).to_dict())
for k in (20, 30, 50, 100):
    print(f'  users with >= {k}: {(pu >= k).sum():,}')
print('per user-day median', inter.groupby(['user_id', 'p_date']).size().median())
s = inter.sort_values(['user_id', 'exposed_time'])
gap = s.groupby('user_id').exposed_time.diff().dropna()
print(f'gap between consecutive records of a user: median {gap.median():.0f}s, share <=60s {(gap <= 60).mean():.2f}'
      '  -> records are sampled, NOT contiguous feed sessions')

print('\naction rates (%, count):')
for c in ['click', 'cvm_like', 'comment', 'follow', 'collect', 'forward', 'hate']:
    print(f'  {c:9s} {inter[c].mean()*100:7.3f}%  {int(inter[c].sum()):,}')
print('  hate: distinct users', inter[inter.hate].user_id.nunique())
print('click semantics (undocumented field): watch_time by click')
print(inter.groupby('click').watch_time.describe(percentiles=[.5, .9]).round(1).to_string())
print('share watch_time>3s by click', inter.groupby('click').watch_time.apply(lambda w: (w > 3).mean()).round(3).to_dict())

print('\nvideos: roots per video max', vid.n_root.max(), '| share with L2', (vid.l2.str.len() > 0).mean().round(3),
      '| share with L3', (vid.l3.str.len() > 0).mean().round(3))
print('distinct roots', vid.root_id.nunique(), '| L2', len(set(sum(vid.l2, []))), '| L3', len(set(sum(vid.l3, []))))
print('tags per video median', vid.tags.str.len().median(), '| title missing', vid.title.isna().mean())
print('author_fans_count quantiles', vid.author_fans_count.quantile([.25, .5, .75, .9]).round(0).to_dict())
print('share of videos whose author has <= 50k fans (X cold-start eligibility):', round((vid.author_fans_count <= 50_000).mean(), 3))
u = inter.drop_duplicates('user_id')
print('\nusers: age', u.age.describe().round(1)[['mean', '25%', '50%', '75%']].to_dict(), '| gender', u.gender.value_counts().to_dict())
print('city level', u.fre_city_level.value_counts().to_dict())
