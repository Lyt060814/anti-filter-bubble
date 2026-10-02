"""Compare LLM variants from 08 (model x thinking) on the same KuaiRand users and rows.

Reads the per-row predictions 08 saves for each variant, keeps variants run on >= 100 users,
and reports per-user GAUC, paired differences vs the logistic baseline, calibration, and the
acceptance-by-category-rank curve (relative to rank 1-3).
"""
import glob, json, numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score
from common import DATA, OUT

preds = {}
for f in sorted(glob.glob(str(DATA / 'kuairand' / 'llm_pilot_kuairand_preds_*.parquet'))):
    tag = f.split('preds_')[1].removesuffix('.parquet')
    preds[tag] = pd.read_parquet(f)
big = {t: p for t, p in preds.items() if p.user_id.nunique() >= 100}
common = set.intersection(*(set(p.index) for p in big.values()))
base = next(iter(big.values())).loc[sorted(common)].drop(columns='P_llm')
for t, p in big.items():
    base['LLM ' + t] = p.loc[base.index, 'P_llm'] / 100
users = [u for u, g in base.groupby('user_id') if g.long_view.nunique() == 2]
ev = base[base.user_id.isin(users)]
print(f'variants with >=100 users: {list(big)}; common rows {len(ev):,}, users {len(users)}')

cost = {}
for t in preds:
    rows = [json.loads(l) for l in open(DATA / 'kuairand' / f'llm_pilot_kuairand_{t}.jsonl')]
    ok = [r for r in rows if 'usage' in r]
    cost[t] = (len(ok), np.mean([r['usage']['completion_tokens'] for r in ok]), sum('error' in r for r in rows))
print('\ncalls / mean output tokens / errors per variant:', {t: (n, round(o), e) for t, (n, o, e) in cost.items()})

cols = {'history share': 'share', 'user x category rate': 'lv_s', 'logistic': 'P_lr', **{'LLM ' + t: 'LLM ' + t for t in big}}
pu = pd.DataFrame({k: pd.Series({u: roc_auc_score(g.long_view, g[c]) for u, g in ev.groupby('user_id')}) for k, c in cols.items()})
boot = np.random.default_rng(2).integers(0, len(pu), (4000, len(pu)))
print(f'\n{"model":28s} GAUC  [95% CI]        global AUC  mean pred (actual {ev.long_view.mean():.3f})')
for k, c in cols.items():
    b = pu[k].values[boot].mean(1)
    print(f'{k:28s} {pu[k].mean():.3f} [{np.percentile(b, 2.5):.3f}, {np.percentile(b, 97.5):.3f}]   {roc_auc_score(ev.long_view, ev[c]):.3f}'
          + (f'       {ev[c].mean():.3f}' if c != 'share' else ''))
print()
for t in big:
    for ref in ('logistic', 'LLM flash'):
        if 'LLM ' + t == ref: continue
        d = (pu['LLM ' + t] - pu[ref]).values; ci = np.percentile(d[boot].mean(1), [2.5, 97.5])
        print(f'diff LLM {t:16s} - {ref:10s}: {d.mean():+.3f}  95% CI [{ci[0]:+.3f}, {ci[1]:+.3f}]')

ev = ev.assign(bucket=pd.cut(ev['rank'], [0, 3, 10, 98, 100], labels=['rank 1-3', 'rank 4-10', 'rank >10', 'never seen']))
t = ev.groupby('bucket', observed=True)[['long_view', 'P_lr'] + ['LLM ' + x for x in big]].mean()
print('\nacceptance by category rank, relative to rank 1-3 (n per bucket:', ev.bucket.value_counts().sort_index().to_dict(), ')')
print((t / t.iloc[0]).round(2).rename(columns={'long_view': 'REAL', 'P_lr': 'logistic'}).to_string())
pu.to_csv(OUT / '09_llm_variants_per_user_gauc.csv')
