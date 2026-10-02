"""Small LLM pilot: does an LLM 'user' predict real skip/watch decisions better than our parametric baselines?

Same test rows as 06 (ShortVideo, predict click = did not swipe away on 09-21/22). Two LLM conditions:
  persona  - demographics only (what SimTok-style agents get)
  history  - demographics + the user's last 50 earlier exposures with outcomes
The LLM returns a 0-100 probability per test video; we score per-user GAUC on the same users as the baselines.

Model: DeepSeek deepseek-flash (DeepSeek-V4.1-Flash), thinking disabled, via DEEPSEEK_API_KEY.
Only anonymised fields are sent (no user id, no city name). Responses are cached outside the repo.
Usage: python3 07_llm_pilot.py [n_users] [budget_cny]
"""
import json, os, sys, time, concurrent.futures as cf
import numpy as np, pandas as pd, requests
from sklearn.metrics import roc_auc_score
from common import SV_DIR, SV_VIDEOS, SV_CATS, OUT

N_USERS = int(sys.argv[1]) if len(sys.argv) > 1 else 150
BUDGET = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0          # CNY, hard stop
MODEL, URL = 'deepseek-flash', 'https://api.deepseek.com/chat/completions'
# CNY per 1M tokens, off-peak (weekends/holidays/evenings Beijing time); peak is 2x. Checked 2026-10-02.
PRICE = {'in_miss': 1.0, 'in_hit': 0.02, 'out': 4.0}
CACHE = SV_DIR / 'llm_pilot_cache.jsonl'
N_HIST, MAX_TITLE = 50, 50

te = pd.read_parquet(SV_DIR / 'llm_benchmark_test_with_baselines.parquet')
tr = pd.read_parquet(SV_DIR / 'llm_benchmark_train.parquet')
vid = pd.read_parquet(SV_VIDEOS)
cat = pd.read_csv(SV_CATS).query('category_level == 1').set_index('category_id').category_name_cn
both = te.groupby('user_id').y.nunique().pipe(lambda s: s[s == 2].index)
users = np.random.default_rng(0).choice(np.array(sorted(both)), size=min(N_USERS, len(both)), replace=False)

def vtext(pid):
    v = vid.loc[pid]
    tags = ' '.join('#' + t for t in list(v.tags)[:3])
    return f'[{cat.get(v.root_id, "其他")}] {str(v.title)[:MAX_TITLE]} {tags}（时长{v.duration:.0f}秒）'

def persona(u):
    r = tr[tr.user_id == u].iloc[0]
    g = {'M': '男', 'F': '女'}.get(r.gender, '未知性别')
    comm = {'urban': '城镇', 'country': '农村', 'unknown': ''}.get(r.fre_community_type, '')
    return f'{g}，{r.age}岁，常住{r.fre_city_level}{("（" + comm + "）") if comm else ""}，手机价格约{r.mod_price}元'

def history(u):
    h = tr[tr.user_id == u].sort_values('exposed_time').tail(N_HIST)
    lines = []
    for r in h.itertuples():
        out = f'看了{r.watch_time}秒' if r.click else f'很快划走（{r.watch_time}秒）'
        extra = ''.join(s for s, f in (('，点赞', r.cvm_like), ('，收藏', r.collect), ('，评论', r.comment), ('，关注作者', r.follow)) if f)
        lines.append(f'- {vtext(r.pid)} → {out}{extra}')
    return '\n'.join(lines)

SYSTEM = ('你在模拟一位真实的快手短视频用户。给定这位用户的基本情况（以及这位用户过去刷到视频时的真实反应），'
          '请预测这位用户接下来刷到每个视频时，会点开观看（看超过约3秒）而不是很快划走的概率。'
          '要贴近这位具体用户的真实习惯，而不是一般人的喜好。只输出 JSON：{"p": [每个视频的概率, 0-100 的整数，按编号顺序]}。')

def prompt(u, cond, items):
    s = f'用户情况：{persona(u)}\n'
    if cond == 'history':
        s += f'\n这位用户最近刷到的视频和真实反应（按时间顺序）：\n{history(u)}\n'
    s += '\n接下来这位用户会刷到这些视频：\n' + '\n'.join(f'{i + 1}. {vtext(p)}' for i, p in enumerate(items))
    s += f'\n\n请输出 {len(items)} 个概率。'
    return s

def call(u, cond, items):
    body = {'model': MODEL, 'messages': [{'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': prompt(u, cond, items)}],
            'thinking': {'type': 'disabled'}, 'response_format': {'type': 'json_object'}, 'temperature': 0.0, 'max_tokens': 800}
    for attempt in range(4):
        try:
            r = requests.post(URL, json=body, timeout=120, headers={'Authorization': f'Bearer {os.environ["DEEPSEEK_API_KEY"]}'})
            r.raise_for_status(); d = r.json()
            p = json.loads(d['choices'][0]['message']['content'])['p']
            if len(p) != len(items): raise ValueError(f'got {len(p)} probs for {len(items)} items')
            return {'user_id': int(u), 'cond': cond, 'pids': [int(x) for x in items], 'p': [float(x) for x in p], 'usage': d['usage']}
        except Exception as e:
            err = e; time.sleep(2 ** attempt)
    return {'user_id': int(u), 'cond': cond, 'error': repr(err)}

def cost(usage):
    hit = usage.get('prompt_cache_hit_tokens', 0); miss = usage.get('prompt_cache_miss_tokens', usage['prompt_tokens'] - hit)
    return (miss * PRICE['in_miss'] + hit * PRICE['in_hit'] + usage['completion_tokens'] * PRICE['out']) / 1e6

done = {}
if CACHE.exists():
    for line in open(CACHE):
        d = json.loads(line)
        if 'p' in d: done[(d['user_id'], d['cond'])] = d
spent = sum(cost(d['usage']) for d in done.values())
jobs = [(u, c) for u in users for c in ('persona', 'history') if (int(u), c) not in done]
print(f'{len(users)} users, {len(jobs)} calls to make; already spent {spent:.3f} CNY (budget {BUDGET})')
rng = np.random.default_rng(1)
items_of = {u: list(rng.permutation(te[te.user_id == u].pid.values)) for u in users}   # same shuffled order for both conditions
with open(CACHE, 'a') as f, cf.ThreadPoolExecutor(8) as ex:
    for i in range(0, len(jobs), 16):
        if spent > BUDGET: print('budget reached, stopping'); break
        for d in ex.map(lambda j: call(j[0], j[1], items_of[j[0]]), jobs[i:i + 16]):
            f.write(json.dumps(d, ensure_ascii=False) + '\n'); f.flush()
            if 'p' in d: done[(d['user_id'], d['cond'])] = d; spent += cost(d['usage'])
            else: print('ERROR', d)
tok = pd.DataFrame([{**d['usage'], 'cond': d['cond']} for d in done.values()])
print(f'calls ok {len(done)}; tokens in {tok.prompt_tokens.sum():,} (cache hit {tok.get("prompt_cache_hit_tokens", pd.Series([0])).sum():,}), '
      f'out {tok.completion_tokens.sum():,}; cost {spent:.3f} CNY')
print(tok.groupby('cond')[['prompt_tokens', 'completion_tokens']].mean().round(0).to_string())

# ---- score on the same rows as the baselines
pred = pd.DataFrame([{'user_id': d['user_id'], 'pid': p, d['cond']: q} for d in done.values() for p, q in zip(d['pids'], d['p'])])
pred = pred.groupby(['user_id', 'pid']).first().reset_index()
ev = te[te.user_id.isin([u for u in users if (int(u), 'persona') in done and (int(u), 'history') in done])]
ev = ev.merge(pred, on=['user_id', 'pid'], how='left')
assert ev[['persona', 'history']].notna().all().all(), 'missing LLM predictions'
models = {'B1 user x category pref': 'B1 + user x category pref', 'B3 + title embedding': 'B3 + title-embedding similarity',
          'B4 gradient boosting': 'B4 gradient boosting, all features', 'LLM persona only': 'persona', 'LLM persona + history': 'history'}
def per_user(col):
    return pd.Series({u: roc_auc_score(g.y, g[col]) if g[col].nunique() > 1 else 0.5
                      for u, g in ev.groupby('user_id')})
pu = pd.DataFrame({k: per_user(v) for k, v in models.items()})
print(f'\n== {len(pu)} users, {len(ev):,} test exposures, positive rate {ev.y.mean():.3f}')
boot = np.random.default_rng(2).integers(0, len(pu), (2000, len(pu)))
for k, v in models.items():
    print(f'{k:26s} GAUC {pu[k].mean():.3f}  [{np.percentile(pu[k].values[boot].mean(1), 2.5):.3f}, {np.percentile(pu[k].values[boot].mean(1), 97.5):.3f}]'
          f'  | global AUC {roc_auc_score(ev.y, ev[v]):.3f}')
for a, b in (('LLM persona + history', 'B4 gradient boosting'), ('LLM persona + history', 'LLM persona only'), ('LLM persona only', 'B1 user x category pref')):
    d = (pu[a] - pu[b]).values; ci = np.percentile(d[boot].mean(1), [2.5, 97.5])
    print(f'diff {a} - {b}: {d.mean():+.3f}  95% CI [{ci[0]:+.3f}, {ci[1]:+.3f}]')
print(f'\nmean predicted P(watch): persona {ev.persona.mean():.1f}, history {ev.history.mean():.1f}  vs actual {ev.y.mean()*100:.1f}')
print(f'share of identical probabilities within a user (no ranking signal): persona '
      f'{ev.groupby("user_id").persona.apply(lambda s: 1 - s.nunique() / len(s)).mean():.2f}, history '
      f'{ev.groupby("user_id").history.apply(lambda s: 1 - s.nunique() / len(s)).mean():.2f}')
pu.to_csv(OUT / '07_llm_pilot_per_user_gauc.csv')
