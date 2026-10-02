"""Can we get content embeddings (for DPP similarity / 'similar content') on a CPU?

Encodes ShortVideo titles+tags with a small Chinese sentence model and checks that the
embeddings carry category structure (same-root pairs more similar than cross-root pairs).
Also times throughput to extrapolate to the KuaiRand-1K caption set.
"""
import time, numpy as np, pandas as pd, torch
from sentence_transformers import SentenceTransformer
from common import SV_VIDEOS, SV_DIR

torch.set_num_threads(4)
MODEL = 'BAAI/bge-small-zh-v1.5'   # 24M params, 512-d, MIT licence
vid = pd.read_parquet(SV_VIDEOS)
text = (vid.title.fillna('') + ' ' + vid.tags.apply(' '.join)).str.slice(0, 128).tolist()

m = SentenceTransformer(MODEL, device='cpu')
t0 = time.time(); E = m.encode(text, batch_size=128, normalize_embeddings=True, show_progress_bar=False); dt = time.time() - t0
print(f'{MODEL}: {len(text):,} texts in {dt:.0f}s on 4 CPU threads -> {len(text)/dt:.0f} texts/s')
print(f'  extrapolated: KuaiRand-1K logged videos (4.37M) ~ {4.37e6/(len(text)/dt)/3600:.1f} h; KuaiRec (10.7k) ~ {10_728/(len(text)/dt):.0f} s')
np.save(SV_DIR / 'sv_title_emb_bge_small.npy', E.astype(np.float16))

rng = np.random.default_rng(0)
root = vid.root_id.values
i, j = rng.integers(0, len(E), 200_000), rng.integers(0, len(E), 200_000)
cos = (E[i] * E[j]).sum(1); same = root[i] == root[j]
print(f'cosine same-root {cos[same].mean():.3f} vs cross-root {cos[~same].mean():.3f}')
# nearest-neighbour category agreement
idx = rng.choice(len(E), 3000, replace=False)
S = E[idx] @ E.T; S[np.arange(len(idx)), idx] = -1
nn = S.argmax(1)
base = (pd.Series(root).value_counts(normalize=True) ** 2).sum()
print(f'1-NN shares root category: {(root[idx] == root[nn]).mean():.3f} (chance {base:.3f})')
