"""Do KuaiRec, KuaiRand and ShortVideo share one category space?

All three come from Kuaishou. We check (a) the KuaiRand supplementary files (Zenodo 18159199)
really join on KuaiRand-1K video_id, (b) level-1 ids and names across the three datasets,
(c) a name-free test for KuaiRand's own `tag` field (median duration per id vs ShortVideo),
and write category_map_l1.csv.
"""
import numpy as np, pandas as pd
from scipy.stats import spearmanr
from common import KR_DIR, KR_SUPP, KREC_DIR, SV_VIDEOS, SV_CATS, OUT

# (a) join check: caption-file duration vs KuaiRand-1K video_duration
cap = pd.read_csv(KR_SUPP / 'kuairand_1k_video_captions.csv', usecols=['final_video_id', 'duration', 'caption'])
basic = pd.read_csv(KR_DIR / 'video_features_basic_1k.csv', usecols=['video_id', 'video_duration', 'tag'])
cap['duration'] = pd.to_numeric(cap.duration, errors='coerce')
basic['video_duration'] = pd.to_numeric(basic.video_duration, errors='coerce')
j = basic.merge(cap, left_on='video_id', right_on='final_video_id')
ok = j.dropna(subset=['duration', 'video_duration'])
print(f'(a) KuaiRand supplement: {len(j):,} of {len(basic):,} 1K videos joined; '
      f'duration identical for {np.isclose(ok.duration, ok.video_duration).mean():.3f} of {len(ok):,} with both')
print(f'    caption non-empty: {(j.caption.fillna("").str.strip() != "").mean():.3f}')

krc = pd.read_csv(KR_SUPP / 'kuairand_1k_video_categories.csv',
                  usecols=['final_video_id', 'first_level_category_id', 'first_level_category_name', 'first_level_category_prob',
                           'second_level_category_id', 'third_level_category_id'])
print(f'    categories: {len(krc):,} videos; L1 known {(krc.first_level_category_id >= 0).mean():.3f}; '
      f'L2 known {(krc.second_level_category_id >= 0).mean():.3f}; L3 known {(krc.third_level_category_id >= 0).mean():.3f}; '
      f'median L1 prob {krc.first_level_category_prob.median():.3f}  (categories are model-predicted)')
t = basic.merge(krc, left_on='video_id', right_on='final_video_id')
t = t[t.tag.notna() & ~t.tag.astype(str).str.contains(',')]
t['tag'] = t.tag.astype(int)
print(f'    KuaiRand `tag` == supplement L1 id for {(t.tag == t.first_level_category_id).mean():.3f} of single-tag videos')

# (b) level-1 table
sv_names = pd.read_csv(SV_CATS).query('category_level == 1').set_index('category_id')[['category_name_cn', 'category_name_en']]
sv_vid = pd.read_parquet(SV_VIDEOS)
kc = pd.read_csv(KREC_DIR / 'kuairec_caption_category.csv', engine='python', on_bad_lines='skip')
kc['video_id'] = pd.to_numeric(kc.video_id, errors='coerce')
krec_names = kc[kc.first_level_category_id >= 0].groupby('first_level_category_id').first_level_category_name.agg(lambda s: s.mode()[0])
kr_names = krc[krc.first_level_category_id >= 0].groupby('first_level_category_id').first_level_category_name.agg(lambda s: s.mode()[0])
m = pd.DataFrame({'sv_name': sv_names.category_name_cn, 'sv_name_en': sv_names.category_name_en.str.strip(),
                  'kuairand_name': kr_names, 'kuairec_name': krec_names})
m['sv_videos'] = sv_vid.root_id.value_counts()
m['kuairand_videos'] = krc.first_level_category_id.value_counts()
m['kuairec_videos'] = kc.first_level_category_id.value_counts()
m.index = m.index.astype(int); m.index.name = 'l1_id'
m = m.sort_index()
names = m[['sv_name', 'kuairand_name', 'kuairec_name']]
m['status'] = np.where(names.notna().all(axis=1) & (names.nunique(axis=1) == 1), 'same',
              np.where(names.notna().sum(axis=1) >= 2, 'renamed/partial', 'one-dataset-only'))
# Harmonised level-1 groups. Kuaishou revised its taxonomy between KuaiRec/KuaiRand (2020/2022-04)
# and ShortVideo (2022-09): some ids were split, merged or reused. Rules (checked by reading captions):
#   29 科学与法律 -> SV split into 29 科学 + 30 法律          => group 29
#   32 短剧 merged into SV 39 影视和短剧                       => group 39
#   23 is REUSED: 时政资讯 (KuaiRand/KuaiRec: 国际/国内时政) vs 宗教 (SV: 菩萨, 佛法)
#        -> KuaiRand/KuaiRec 23 joins 28 资讯 (SV has no politics id); SV 23 stays its own group 'religion'
#   33 自拍 (no L2; absent in SV) joins 34 其他/随手拍; 31 健身 (absent in SV) joins 7 运动
#   KuaiRec stray ids 418/667 (1 video each) are dropped.
HARM = {'kuairand': {29: 29, 32: 39, 23: 28, 33: 34, 31: 7},
        'kuairec':  {29: 29, 32: 39, 23: 28, 33: 34, 31: 7, 418: None, 667: None},
        'shortvideo': {30: 29, 23: 1023}}
def harm(ds, i):
    return HARM[ds].get(i, i)
for ds, col in [('shortvideo', 'sv_name'), ('kuairand', 'kuairand_name'), ('kuairec', 'kuairec_name')]:
    m['h_' + ds] = [harm(ds, i) if pd.notna(n) else None for i, n in zip(m.index, m[col])]
m.to_csv(OUT / 'category_map_l1.csv', encoding='utf-8-sig')
print(f'\n(b) level-1 ids: ShortVideo {m.sv_name.notna().sum()}, KuaiRand {m.kuairand_name.notna().sum()}, KuaiRec {m.kuairec_name.notna().sum()}; '
      f'present in all three {names.notna().all(axis=1).sum()}')
print(m.status.value_counts().to_string())
groups = {ds: set(m['h_' + ds].dropna()) for ds in ('shortvideo', 'kuairand', 'kuairec')}
print(f'harmonised groups: SV {len(groups["shortvideo"])}, KuaiRand {len(groups["kuairand"])}, KuaiRec {len(groups["kuairec"])}; '
      f'shared by all three {len(set.intersection(*groups.values()))}; SV-only {sorted(groups["shortvideo"] - groups["kuairand"])}')
print(m[m.status != 'same'][['sv_name', 'kuairand_name', 'kuairec_name', 'sv_videos', 'kuairand_videos', 'kuairec_videos']].to_string())

# (c) name-free check on the original KuaiRand `tag`
svd = sv_vid.groupby('root_id').duration.agg(['median', 'size'])
krd = t.groupby('tag').video_duration.agg(['median', 'size'])
jj = svd.join(krd, lsuffix='_sv', rsuffix='_kr', how='inner').query('size_sv >= 30 and size_kr >= 30')
rho = spearmanr(jj.median_sv, jj.median_kr).correlation
null = [spearmanr(jj.median_sv, np.random.default_rng(i).permutation(jj.median_kr.values)).correlation for i in range(2000)]
print(f'\n(c) median duration per L1 id, ShortVideo vs KuaiRand tag: Spearman {rho:.2f} over {len(jj)} ids, permutation p < {max(np.mean(np.array(null) >= rho), 1/2000):.4f}')

# (d) finer levels: ids shared between datasets
def ids(df, col): return set(df[col].dropna().astype(int)) - {-124}
sv_l2, sv_l3 = set().union(*map(set, sv_vid.l2)), set().union(*map(set, sv_vid.l3))
print(f'\n(d) L2 ids  SV {len(sv_l2)} | KuaiRand {len(ids(krc, "second_level_category_id"))} | KuaiRec {len(ids(kc, "second_level_category_id"))} | '
      f'SV&KuaiRand {len(sv_l2 & ids(krc, "second_level_category_id"))} | SV&KuaiRec {len(sv_l2 & ids(kc, "second_level_category_id"))}')
print(f'    L3 ids  SV {len(sv_l3)} | KuaiRand {len(ids(krc, "third_level_category_id"))} | KuaiRec {len(ids(kc, "third_level_category_id"))} | '
      f'SV&KuaiRand {len(sv_l3 & ids(krc, "third_level_category_id"))} | SV&KuaiRec {len(sv_l3 & ids(kc, "third_level_category_id"))}')
