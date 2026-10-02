"""LLM pilot 2 on KuaiRand-1K random exposures (stronger signal than ShortVideo's sampled log).

For each sampled user: history = last 50 recommended exposures before 04-22 (caption, L1 category, outcome);
candidates = the user's randomly-exposed videos 04-22..05-08 (no recommender selection, up to 30).
Label = long_view. The LLM gives P(long view) per candidate.
We compare per-user GAUC with parametric scores AND check whether the LLM reproduces the aggregate
'acceptance by category rank' curve from 05, which is what the simulator actually needs.
No demographics exist in KuaiRand, so the LLM sees behaviour only.
Usage: python3 08_llm_pilot_kuairand.py [n_users] [budget_cny]
"""
import json, os, sys, time, concurrent.futures as cf
import numpy as np, pandas as pd, requests
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold
from common import KR_DIR, KR_SUPP, OUT, DATA

N_USERS = int(sys.argv[1]) if len(sys.argv) > 1 else 150
BUDGET = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
MODEL, URL = 'deepseek-flash', 'https://api.deepseek.com/chat/completions'
PRICE = {'in_miss': 1.0, 'in_hit': 0.02, 'out': 4.0}        # CNY / 1M tokens, off-peak, checked 2026-10-02
CACHE = DATA / 'kuairand' / 'llm_pilot_kuairand_cache.jsonl'
N_HIST, N_CAND, MAX_TITLE = 50, 30, 50

cmap = pd.read_csv(OUT / 'category_map_l1.csv', index_col='l1_id')
names = cmap.kuairand_name.dropna().to_dict()
cat = pd.read_csv(KR_SUPP / 'kuairand_1k_video_categories.csv', usecols=['final_video_id', 'first_level_category_id']).set_index('final_video_id').first_level_category_id
grp = cat.map(cmap.h_kuairand.dropna().astype(int).to_dict())

cols = ['user_id', 'video_id', 'time_ms', 'is_click', 'long_view', 'is_like', 'play_time_ms', 'duration_ms']
hist = pd.read_csv(KR_DIR / 'log_standard_4_08_to_4_21_1k.csv', usecols=cols)
rnd = pd.read_csv(KR_DIR / 'log_random_4_22_to_5_08_1k.csv', usecols=cols)
for d in (hist, rnd):
    d['g'] = d.video_id.map(grp)

# --- parametric scores for ALL random rows (profile from the full 14-day history)
prof = hist.dropna(subset=['g']).groupby(['user_id', 'g']).agg(n=('long_view', 'size'), lv=('long_view', 'sum'))
prof['share'] = prof.n / prof.groupby('user_id').n.transform('sum')
u_lv = hist.groupby('user_id').long_view.mean()
prof['lv_s'] = (prof.lv + 10 * u_lv.reindex(prof.index.get_level_values(0)).values) / (prof.n + 10)
r = rnd[rnd.user_id.isin(u_lv.index) & rnd.duration_ms.notna()].join(prof[['share', 'lv_s']], on=['user_id', 'g'])
r['share'] = r.share.fillna(0); r['lv_s'] = r.lv_s.fillna(r.user_id.map(u_lv))
r['u_lv'] = r.user_id.map(u_lv); r['log_dur'] = np.log1p(r.duration_ms)
r['rank'] = r.join(prof.groupby('user_id').n.rank(ascending=False, method='first').rename('rank'), on=['user_id', 'g'])['rank'].fillna(99)
F = ['share', 'lv_s', 'u_lv', 'log_dur']
r['P_lr'] = 0.0
for tri, tei in GroupKFold(5).split(r, groups=r.user_id):         # fitted on other users only
    r.loc[r.index[tei], 'P_lr'] = LogisticRegression(max_iter=1000).fit(r.iloc[tri][F], r.iloc[tri].long_view).predict_proba(r.iloc[tei][F])[:, 1]

ok = r.groupby('user_id').long_view.agg(['nunique', 'size'])
elig = ok[(ok['nunique'] == 2) & (ok['size'] >= 10)].index
users = np.random.default_rng(0).choice(np.array(sorted(elig)), size=min(N_USERS, len(elig)), replace=False)
print(f'eligible users {len(elig)} (both labels, >=10 random exposures); sampled {len(users)}')

need = set(hist[hist.user_id.isin(users)].video_id) | set(rnd[rnd.user_id.isin(users)].video_id)
cap = pd.concat(c[c.final_video_id.isin(need)] for c in pd.read_csv(KR_SUPP / 'kuairand_1k_video_captions.csv', chunksize=1_000_000,
                usecols=['final_video_id', 'caption', 'show_cover_text'])).set_index('final_video_id')

def vtext(v, dur_ms):
    c = cap.caption.get(v); c = c if isinstance(c, str) and c.strip() else cap.show_cover_text.get(v)
    c = c.strip()[:MAX_TITLE] if isinstance(c, str) and c.strip() else '（无标题）'
    return f'[{names.get(cat.get(v), "未知")}] {c}（时长{dur_ms / 1000:.0f}秒）'

def history(u):
    h = hist[hist.user_id == u].sort_values('time_ms').tail(N_HIST)
    out = []
    for x in h.itertuples():
        o = '看了很久' if x.long_view else ('看了一会' if x.play_time_ms > 3000 else '很快划走')
        out.append(f'- {vtext(x.video_id, x.duration_ms)} → {o}（{x.play_time_ms / 1000:.0f}秒）{"，点赞" if x.is_like else ""}')
    return '\n'.join(out)

SYSTEM = ('你在模拟一位真实的快手短视频用户。给定这位用户最近刷到的视频和真实反应，请预测这位用户接下来刷到每个视频时，'
          '会"看很久"（长播放）的概率。要贴近这位具体用户的真实习惯。只输出 JSON：{"p": [每个视频的概率, 0-100 的整数，按编号顺序]}。')

def call(u, items):
    rows = r.loc[items]
    msg = (f'这位用户最近刷到的视频和真实反应（按时间顺序）：\n{history(u)}\n\n接下来这位用户会刷到这些视频：\n'
           + '\n'.join(f'{i + 1}. {vtext(x.video_id, x.duration_ms)}' for i, x in enumerate(rows.itertuples()))
           + f'\n\n请输出 {len(rows)} 个概率。')
    body = {'model': MODEL, 'messages': [{'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': msg}],
            'thinking': {'type': 'disabled'}, 'response_format': {'type': 'json_object'}, 'temperature': 0.0, 'max_tokens': 800}
    for attempt in range(4):
        try:
            resp = requests.post(URL, json=body, timeout=120, headers={'Authorization': f'Bearer {os.environ["DEEPSEEK_API_KEY"]}'})
            resp.raise_for_status(); d = resp.json()
            p = json.loads(d['choices'][0]['message']['content'])['p']
            if len(p) != len(rows): raise ValueError(f'{len(p)} != {len(rows)}')
            return {'user_id': int(u), 'rows': [int(i) for i in items], 'p': [float(x) for x in p], 'usage': d['usage']}
        except Exception as e:
            err = e; time.sleep(2 ** attempt)
    return {'user_id': int(u), 'error': repr(err)}

def cost(us):
    hit = us.get('prompt_cache_hit_tokens', 0); miss = us.get('prompt_cache_miss_tokens', us['prompt_tokens'] - hit)
    return (miss * PRICE['in_miss'] + hit * PRICE['in_hit'] + us['completion_tokens'] * PRICE['out']) / 1e6

done = {}
if CACHE.exists():
    for line in open(CACHE):
        d = json.loads(line)
        if 'p' in d: done[d['user_id']] = d
spent = sum(cost(d['usage']) for d in done.values())
rng = np.random.default_rng(1)
items_of = {u: list(rng.permutation(r.index[r.user_id == u].values)[:N_CAND]) for u in users}
jobs = [u for u in users if int(u) not in done]
print(f'{len(jobs)} calls to make; already spent {spent:.3f} CNY (budget {BUDGET})')
with open(CACHE, 'a') as f, cf.ThreadPoolExecutor(8) as ex:
    for i in range(0, len(jobs), 16):
        if spent > BUDGET: print('budget reached, stopping'); break
        for d in ex.map(lambda u: call(u, items_of[u]), jobs[i:i + 16]):
            f.write(json.dumps(d, ensure_ascii=False) + '\n'); f.flush()
            if 'p' in d: done[d['user_id']] = d; spent += cost(d['usage'])
            else: print('ERROR', d)
tok = pd.DataFrame([d['usage'] for d in done.values()])
print(f'calls ok {len(done)}; tokens in {tok.prompt_tokens.sum():,}, out {tok.completion_tokens.sum():,}; cost {spent:.3f} CNY')

sel = set(int(u) for u in users)   # score only this run's sample (the cache may hold extra smoke-test users)
llm = pd.Series({i: p for d in done.values() if d['user_id'] in sel for i, p in zip(d['rows'], d['p'])}, name='P_llm')
ev = r.loc[llm.index].assign(P_llm=llm)
models = {'share of category in history': 'share', 'user x category long-view rate': 'lv_s', 'logistic (other users)': 'P_lr', 'LLM (history)': 'P_llm'}
def per_user(c):
    return pd.Series({u: roc_auc_score(g.long_view, g[c]) for u, g in ev.groupby('user_id') if g.long_view.nunique() == 2})
pu = pd.DataFrame({k: per_user(v) for k, v in models.items()})
boot = np.random.default_rng(2).integers(0, len(pu), (2000, len(pu)))
print(f'\n== {len(pu)} users, {len(ev):,} random exposures, long-view rate {ev.long_view.mean():.3f}')
for k, v in models.items():
    b = pu[k].values[boot].mean(1)
    print(f'{k:32s} GAUC {pu[k].mean():.3f} [{np.percentile(b, 2.5):.3f}, {np.percentile(b, 97.5):.3f}] | global AUC {roc_auc_score(ev.long_view, ev[v]):.3f}')
for a, b in (('LLM (history)', 'user x category long-view rate'), ('LLM (history)', 'logistic (other users)')):
    d = (pu[a] - pu[b]).values; ci = np.percentile(d[boot].mean(1), [2.5, 97.5])
    print(f'diff {a} - {b}: {d.mean():+.3f} 95% CI [{ci[0]:+.3f}, {ci[1]:+.3f}]')

# aggregate fidelity: does the LLM reproduce the acceptance-by-rank curve?
ev['bucket'] = pd.cut(ev['rank'], [0, 3, 10, 98, 100], labels=['rank 1-3', 'rank 4-10', 'rank >10', 'never seen'])
t = ev.groupby('bucket', observed=True).agg(n=('long_view', 'size'), real=('long_view', 'mean'), llm=('P_llm', 'mean'), logistic=('P_lr', 'mean'))
t['llm'] /= 100
for c in ('real', 'llm', 'logistic'):
    t[c + '_rel'] = t[c] / t[c].iloc[0]
print('\nacceptance by category rank (relative columns = divided by rank 1-3):'); print(t.round(3).to_string())
pu.to_csv(OUT / '08_llm_pilot_kuairand_per_user_gauc.csv')
