"""Real pretrained retrieval smoke check; no accuracy claim or stance labels.

Run with the isolated v3-check Python and SOURCE_ROOT. Uses a fixed model
revision resolved on acquisition, records it and dependency versions.
"""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import resource
import sys
import time
import pandas as pd
import torch
from huggingface_hub import snapshot_download
from transformers import AutoModel, AutoTokenizer

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('source_root', type=Path)
parser.add_argument('--revision', default='97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3')
args = parser.parse_args()
root = args.source_root.resolve()
model_id = 'Qwen/Qwen3-Embedding-0.6B'
revision = args.revision
folder = root / 'models' / 'Qwen3-Embedding-0.6B' / revision
snapshot_download(model_id, revision=revision, local_dir=folder,
                  allow_patterns=['*.json', '*.safetensors', '*.txt', '*.model', 'README.md'], max_workers=3)
torch.set_num_threads(4)
t0 = time.perf_counter()
tokenizer = AutoTokenizer.from_pretrained(folder, padding_side='left')
model = AutoModel.from_pretrained(folder).eval()
manifest = json.loads(Path('docs/context-recovery/plan_v3_media_probe.json').read_text())
ids = [r['pid'] for r in manifest['rows']]
data = pd.read_csv(root/'data/shortvideo/interaction_sampled.csv', usecols=['pid','title']).drop_duplicates('pid').set_index('pid')
documents = [str(data.loc[i, 'title']) + '\n' + (root/f'data/audit/plan_v3/media/{i}.txt').read_text() for i in ids]
queries = ['孩子使用手机应该怎样引导？', '夫妻相处中的冲突与解释', '学生假期兼职与经济独立']
texts = [f'Instruct: Retrieve short-video passages relevant to the issue, regardless of stance.\nQuery: {q}' for q in queries] + documents
vectors = []
for start in range(0, len(texts), 2):
    batch = tokenizer(texts[start:start+2], padding=True, truncation=True, max_length=512, return_tensors='pt')
    with torch.inference_mode():
        v = model(**batch).last_hidden_state[:, -1]
        vectors.append(torch.nn.functional.normalize(v, p=2, dim=1))
embedding = torch.cat(vectors)
scores = embedding[:len(queries)] @ embedding[len(queries):].T
result = {
    'scope': 'Pretrained CPU inference and finite retrieval only; convenience samples, no gold labels; not accuracy evaluation',
    'model': model_id, 'revision': revision, 'device': 'cpu',
    'load_and_inference_seconds': time.perf_counter()-t0,
    'max_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    'max_tokens': 512, 'document_ids': ids, 'embedding_shape': list(embedding.shape),
    'finite_outputs': bool(torch.isfinite(embedding).all()),
    'queries': [{'query':q, 'ranked_pids':[ids[i] for i in scores[n].argsort(descending=True).tolist()],
                 'scores':scores[n].tolist()} for n,q in enumerate(queries)],
    'versions': {p:importlib.metadata.version(p) for p in ['torch','transformers','huggingface-hub','pandas']},
    'weights': [{'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in folder.glob('*.safetensors')],
}
Path('docs/context-recovery/plan_v3_embedding_probe.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['model','revision','embedding_shape','finite_outputs','load_and_inference_seconds','max_rss_kib']},indent=2))
