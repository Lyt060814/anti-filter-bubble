"""Attribute contrast vs topic contrast in the content representation behind OneRec's semantic IDs.

Usage: CUDA_VISIBLE_DEVICES=5 python -I embedding_contrast_probe.py EMB_MODEL_DIR RECIF_DIR LABELS_JSONL OUT_JSON

Embeds generated captions with Qwen3-Embedding-8B (the model OneRec's semantic IDs are built from) and
reports, for each attribute (pilot LLM labels, feasibility only):
  attribute contrast  c = mean cos(A, A') - mean cos(A, B)        (within the issue)
  topic contrast      t = mean cos(I, I') - mean cos(I, Off)      (issue vs off-issue)
  linear-probe AUC (5-fold logistic regression) for A vs B and for issue vs off-issue
  semantic-ID sharing: P(same first-level code) for A-A, A-B, I-I, I-Off pairs
A null attribute (random genre-matched subset of B) gives the noise floor for c and the probe AUC.
"""
import json
import random
import sys
from collections import Counter

import numpy as np
import pyarrow.compute as pc
import pyarrow.parquet as pq

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from onerec_manipulation_probe import Maps  # noqa: E402
from onerec_viewpoint_probe import ATTRS  # noqa: E402


def captions_for(recif_dir, pids):
    want = set(pids)
    f = pq.ParquetFile(f"{recif_dir}/pid2caption.parquet")
    out = {}
    for rg in range(f.num_row_groups):
        t = f.read_row_group(rg, columns=["pid", "dense_caption"])
        mask = pc.is_in(t.column("pid"), value_set=__import__("pyarrow").array(list(want), type=t.column("pid").type))
        tt = t.filter(mask)
        for p, c in zip(tt.column("pid").to_pylist(), tt.column("dense_caption").to_pylist()):
            out[p] = c
    return out


def mean_cos(X, Y, same=False):
    S = X @ Y.T
    if same:
        n = len(X)
        return float((S.sum() - np.trace(S)) / (n * (n - 1)))
    return float(S.mean())


def probe_auc(X, y, seed=0):
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_predict, StratifiedKFold
    from sklearn.metrics import roc_auc_score
    cv = StratifiedKFold(5, shuffle=True, random_state=seed)
    p = cross_val_predict(LogisticRegression(max_iter=2000, C=1.0, class_weight="balanced"), X, y, cv=cv, method="predict_proba")[:, 1]
    return float(roc_auc_score(y, p))


def main():
    emb_dir, recif_dir, labels_path, out_path = sys.argv[1:5]
    rng = random.Random(5)
    maps = Maps(recif_dir)
    rows = [json.loads(l) for l in open(labels_path, encoding="utf-8")]
    rel = [r for r in rows if r["issue"] == "是"]
    off = [int(p) for p in rng.sample(list(maps.pid[~maps.pid_issue]), 1500)]
    caps = captions_for(recif_dir, off)
    off = [p for p in off if p in caps][:1200]
    from vllm import LLM
    llm = LLM(model=emb_dir, task="embed", dtype="bfloat16", max_model_len=2048, gpu_memory_utilization=0.85)
    texts = [r["caption"][:1500] for r in rel] + [caps[p][:1500] for p in off]
    E = np.array([o.outputs.embedding for o in llm.embed(texts, use_tqdm=False)], dtype=np.float32)
    E /= np.linalg.norm(E, axis=1, keepdims=True)
    E_rel, E_off = E[:len(rel)], E[len(rel):]
    idx = {r["pid"]: i for i, r in enumerate(rel)}
    out = {"n_relevant": len(rel), "n_off": len(off)}
    t = mean_cos(E_rel, E_rel, True) - mean_cos(E_rel, E_off)
    X = np.vstack([E_rel, E_off]); y = np.r_[np.ones(len(rel)), np.zeros(len(off))]
    sid1 = lambda p: maps.sid_of(p)[0] if maps.has(p) else None
    def share_code(P, Q, same=False):
        a = [sid1(p) for p in P]; b = [sid1(q) for q in Q]
        hits = tot = 0
        for i, x in enumerate(a):
            for j, z in enumerate(b):
                if same and i == j:
                    continue
                if x is None or z is None:
                    continue
                hits += x == z; tot += 1
        return hits / max(tot, 1)
    rel_p = [r["pid"] for r in rel]
    out["topic"] = {"t": t, "cos_within": mean_cos(E_rel, E_rel, True), "cos_issue_off": mean_cos(E_rel, E_off),
                    "probe_auc": probe_auc(X, y), "P_same_code_II": share_code(rel_p[:400], rel_p[:400], True),
                    "P_same_code_IOff": share_code(rel_p[:400], off[:400])}
    attrs = dict(ATTRS)
    a_true = [r for r in rel if ATTRS["gender_generalization"][0](r)]
    pool_b = [r for r in rel if ATTRS["gender_generalization"][1](r)]
    fake = set()
    for g, c in Counter(r["genre"] for r in a_true).items():
        cand = [r["pid"] for r in pool_b if r["genre"] == g]
        fake.update(rng.sample(cand, min(c, len(cand))))
    attrs["null_random_subset"] = (lambda r: r["pid"] in fake, lambda r: ATTRS["gender_generalization"][1](r) and r["pid"] not in fake)
    for name, (is_a, is_b) in attrs.items():
        A = [r for r in rel if is_a(r)]
        B = [r for r in rel if is_b(r)]
        # genre-matched B, as in the OneRec probe
        byg = {}
        for r in B:
            byg.setdefault(r["genre"], []).append(r)
        Bm = []
        for g, c in Counter(r["genre"] for r in A).items():
            Bm += rng.sample(byg.get(g, []), min(len(byg.get(g, [])), 3 * c))
        EA = E_rel[[idx[r["pid"]] for r in A]]; EB = E_rel[[idx[r["pid"]] for r in Bm]]
        c = mean_cos(EA, EA, True) - mean_cos(EA, EB)
        Xa = np.vstack([EA, EB]); ya = np.r_[np.ones(len(EA)), np.zeros(len(EB))]
        out[name] = {"n_A": len(A), "n_B_matched": len(Bm), "c": c, "c_over_t": c / t,
                     "probe_auc": probe_auc(Xa, ya) if min(len(EA), len(EB)) >= 10 else None,
                     "P_same_code_AA": share_code([r["pid"] for r in A], [r["pid"] for r in A], True),
                     "P_same_code_AB": share_code([r["pid"] for r in A], [r["pid"] for r in Bm])}
        print(name, json.dumps(out[name], ensure_ascii=False), flush=True)
    print("topic", json.dumps(out["topic"]), flush=True)
    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
