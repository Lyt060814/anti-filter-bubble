"""Benchmark for 'can an LLM user agent predict real short-video behaviour better than our parametric model?'

ShortVideo is the only dataset with real demographics + readable titles + exposed-but-skipped records
(click=False ~ swiped away within ~3 s). Task: for users with enough history, predict click (did not skip)
on their last-2-day exposures from earlier days. Here we build the split and the non-LLM baselines that
an LLM agent would have to beat. No LLM is called in this script.
"""
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from common import SV_INTER, SV_VIDEOS, SV_DIR, OUT

it = pd.read_parquet(SV_INTER).sort_values('exposed_time')
vid = pd.read_parquet(SV_VIDEOS)
E = np.load(SV_DIR / 'sv_title_emb_bge_small.npy').astype(np.float32)
row = pd.Series(np.arange(len(vid)), index=vid.index)
it['y'] = it.click.astype(int)
test_days = [20220921, 20220922]
tr, te = it[~it.p_date.isin(test_days)], it[it.p_date.isin(test_days)]
ntr = tr.groupby('user_id').size(); nte = te.groupby('user_id').size()
users = ntr[ntr >= 20].index.intersection(nte[nte >= 5].index)
tr, te = tr[tr.user_id.isin(users)], te[te.user_id.isin(users)].copy()
print(f'benchmark: {len(users):,} users with >=20 train and >=5 test exposures; train {len(tr):,}, test {len(te):,}, '
      f'test positive rate {te.y.mean():.3f}; test videos unseen in train {(~te.pid.isin(tr.pid)).mean():.2f}')
te[['user_id', 'pid', 'exposed_time', 'y']].to_csv(SV_DIR / 'llm_benchmark_test_keys.csv', index=False)   # derived data stays outside the repo

def gauc(df, s):
    a = [roc_auc_score(g.y, g[s]) for _, g in df.groupby('user_id') if g.y.nunique() == 2]
    return np.mean(a), len(a)

full_tr = it[~it.p_date.isin(test_days)]
g_root = full_tr.groupby('root_id').y.mean()
u_rate = tr.groupby('user_id').y.mean()
u_root = tr.groupby(['user_id', 'root_id']).y.agg(['sum', 'size'])
def feats(df):
    f = pd.DataFrame(index=df.index)
    f['u_rate'] = df.user_id.map(u_rate)
    k = pd.MultiIndex.from_frame(df[['user_id', 'root_id']])
    s = u_root.reindex(k)
    f['u_root'] = ((s['sum'].fillna(0) + 5 * f.u_rate.values) / (s['size'].fillna(0) + 5)).values   # smoothed
    f['u_root_n'] = np.log1p(s['size'].fillna(0).values)
    f['g_root'] = df.root_id.map(g_root).fillna(g_root.mean())
    f['log_dur'] = np.log1p(df.duration); f['log_fans'] = np.log1p(df.author_fans_count)
    f['hour'] = np.sin(df.p_hour / 24 * 2 * np.pi)
    # content similarity: mean emb of user's clicked minus skipped train items
    return f
Ftr, Fte = feats(tr), feats(te)
U = {}
for u, g in tr.groupby('user_id'):
    e = E[row[g.pid].values]; U[u] = e[g.y.values == 1].mean(0) if g.y.sum() else 0 * e[0]
    U[u] = U[u] - (e[g.y.values == 0].mean(0) if (g.y == 0).any() else 0)
for F, df in ((Ftr, tr), (Fte, te)):
    F['emb_sim'] = [float(E[row[p]] @ U[u]) for u, p in zip(df.user_id, df.pid)]

res = {}
for name, cols in {'B0 user click-rate only': ['u_rate'], 'B1 + user x category pref': ['u_rate', 'u_root', 'u_root_n', 'g_root'],
                   'B2 + video meta (duration, fans, hour)': ['u_rate', 'u_root', 'u_root_n', 'g_root', 'log_dur', 'log_fans', 'hour'],
                   'B3 + title-embedding similarity': ['u_rate', 'u_root', 'u_root_n', 'g_root', 'log_dur', 'log_fans', 'hour', 'emb_sim']}.items():
    lr = LogisticRegression(max_iter=1000).fit(Ftr[cols], tr.y)
    te[name] = lr.predict_proba(Fte[cols])[:, 1]
    ga, n = gauc(te, name)
    res[name] = (roc_auc_score(te.y, te[name]), ga, n)
    print(f'{name:40s} AUC {res[name][0]:.3f} | per-user GAUC {ga:.3f} (users with both labels: {n})')
print('\nAn LLM agent counts as "better than parametric" only if it beats B2/B3 on GAUC on the same test keys.')

# single-feature GAUCs and a non-linear model, so the bar is not artificially low
from sklearn.ensemble import HistGradientBoostingClassifier
print()
for c in ['u_root', 'g_root', 'log_dur', 'log_fans', 'emb_sim']:
    te['_f'] = Fte[c].values; print(f'single feature {c:9s} GAUC {gauc(te, "_f")[0]:.3f}')
allc = ['u_rate', 'u_root', 'u_root_n', 'g_root', 'log_dur', 'log_fans', 'hour', 'emb_sim']
hgb = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, random_state=0).fit(Ftr[allc], tr.y)
te['B4 gradient boosting, all features'] = hgb.predict_proba(Fte[allc])[:, 1]
print(f'B4 gradient boosting, all features       AUC {roc_auc_score(te.y, te["B4 gradient boosting, all features"]):.3f} | '
      f'per-user GAUC {gauc(te, "B4 gradient boosting, all features")[0]:.3f}')

# keep test predictions so the LLM pilot (07) is scored on exactly the same rows
te.drop(columns=['_f']).to_parquet(SV_DIR / 'llm_benchmark_test_with_baselines.parquet')
tr.to_parquet(SV_DIR / 'llm_benchmark_train.parquet')
