"""How do real users react to content OUTSIDE their usual categories? (escape calibration)

Escape depends on whether a user engages with out-of-cocoon items when they appear. KuaiRand-1K
has a randomly-exposed log (no recommender selection), so we can measure it without the usual
exposure bias. Interest profile = harmonised L1 shares in the user's standard log 04-08..04-21;
outcomes = random-exposure log 04-22..05-08 (and the standard log of the same period, for contrast).
"""
import numpy as np, pandas as pd
from common import KR_DIR, KR_SUPP, OUT

cmap = pd.read_csv(OUT / 'category_map_l1.csv', index_col='l1_id')
h = cmap.h_kuairand.dropna().astype(int).to_dict()
cat = pd.read_csv(KR_SUPP / 'kuairand_1k_video_categories.csv', usecols=['final_video_id', 'first_level_category_id'])
cat['g'] = cat.first_level_category_id.map(h)
vg = cat.set_index('final_video_id').g

cols = ['user_id', 'video_id', 'is_click', 'long_view', 'is_like', 'is_hate', 'play_time_ms', 'duration_ms']
hist = pd.read_csv(KR_DIR / 'log_standard_4_08_to_4_21_1k.csv', usecols=['user_id', 'video_id'])
hist['g'] = hist.video_id.map(vg)
prof = hist.dropna(subset=['g']).groupby(['user_id', 'g']).size()
share = (prof / prof.groupby('user_id').transform('sum')).rename('share')
rank = prof.groupby('user_id').rank(ascending=False, method='first').rename('rank')
print(f'profiles: {share.index.get_level_values(0).nunique()} users, median {hist.groupby("user_id").size().median():.0f} history items')

def outcome(log, name):
    log['g'] = log.video_id.map(vg)
    log = log.dropna(subset=['g']).join(share, on=['user_id', 'g']).join(rank, on=['user_id', 'g'])
    log['share'] = log.share.fillna(0)
    log['bucket'] = pd.cut(log['rank'].fillna(99), [0, 1, 3, 10, 98, 100], labels=['top-1', 'rank 2-3', 'rank 4-10', 'rank >10', 'never seen'])
    log['ratio'] = (log.play_time_ms / log.duration_ms).clip(0, 3)
    t = log.groupby('bucket', observed=True).agg(n=('user_id', 'size'), click=('is_click', 'mean'), long_view=('long_view', 'mean'),
                                                 like=('is_like', 'mean'), hate=('is_hate', 'mean'), watch_ratio=('ratio', 'median'))
    t['share_of_exposures'] = t.n / t.n.sum()
    print(f'\n== {name} ({len(log):,} exposures)'); print(t.round(4).to_string())
    return log, t

rnd, tr = outcome(pd.read_csv(KR_DIR / 'log_random_4_22_to_5_08_1k.csv', usecols=cols), 'RANDOM exposure log')
std, ts = outcome(pd.read_csv(KR_DIR / 'log_standard_4_22_to_5_08_1k.csv', usecols=cols), 'STANDARD (recommended) log, same period')

top = tr.loc['top-1', 'long_view']
print('\nrandom log, long_view relative to top-1 category:', (tr.long_view / top).round(2).to_dict())
# per-user slope: does acceptance of unfamiliar content differ a lot between users? (heterogeneity for the user model)
rnd['in_top3'] = rnd['rank'].fillna(99) <= 3
pu = rnd.groupby(['user_id', 'in_top3']).long_view.agg(['mean', 'size']).unstack()
pu = pu[(pu['size'] >= 5).all(axis=1)]
r = (pu['mean'][False] + 0.01) / (pu['mean'][True] + 0.01)
print(f'per-user ratio long_view(outside top-3)/long_view(top-3), users with >=5 of each: n={len(r)}, '
      f'quartiles {r.quantile([.25, .5, .75]).round(2).to_dict()}')
print(f'hate events in random log: {int(rnd.is_hate.sum())} (too few for per-user NI modelling; standard log: {int(std.is_hate.sum())})')
