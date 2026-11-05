"""Viewpoint-level pilot on OneRec-1.7B: does the model separate a narrative attribute within an issue?

Usage: CUDA_VISIBLE_DEVICES=0 python -I onerec_viewpoint_probe.py MODEL_DIR RECIF_DIR LABELS_JSONL OUT_JSON [N_USERS] [THINKING 0/1]

Uses the LLM pilot labels (feasibility only). For each attribute, labelled issue items are split into an
"inject" half and an "evaluation" half. For each seed user and condition we compute the exact model
probability of every evaluation item (three semantic-ID tokens, teacher forcing on a shared prompt cache):
  label_cond: base; lv_A / lv_B (long-view section replaced by 10 injected A or B items);
              ni_A / ni_B (10 injected A or B items in the not-interested section)
  video_rec : base; add_A / add_B (20 injected items appended to the exposure history)
Outputs log pi(A_eval), log pi(B_eval), log pi(Off) per condition, hence
  dV   = change of log pi(A_eval) - log pi(B_eval)      (viewpoint skew within the labelled sample)
  dlm  = change of log pi(A_eval + B_eval)              (issue mass within the labelled sample)
Off is a random set of non-issue items used as a check that mass moves between topics.
"""
import json
import random
import sys
from collections import Counter

import numpy as np
import pyarrow.parquet as pq
import torch

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from onerec_manipulation_probe import ASK, HEAD, SYS, Maps, sid_str  # noqa: E402

ATTRS = {
    "gender_generalization": (lambda r: r["gender_generalization"] in ("针对女性", "针对男性"), lambda r: r["gender_generalization"] == "无"),
    "marriage_negative": (lambda r: r["marriage_attitude"] == "消极", lambda r: r["marriage_attitude"] in ("积极", "中性或混合", "不涉及")),
    "conflict": (lambda r: r["conflict"] == "是", lambda r: r["conflict"] == "否"),
}


def label_cond_messages(hist):
    lines = ["以下是用户的历史互动行为："]
    for k in ["longview", "like", "follow", "forward", "not_interested"]:
        if hist.get(k):
            lines.append(HEAD[k] + "".join(sid_str(s) for s in hist[k]))
    lines.append(ASK)
    return [{"role": "system", "content": SYS}, {"role": "user", "content": "\n".join(lines)}]


def video_messages(sids):
    return [{"role": "system", "content": "你是一位视频推荐系统专家，擅长捕捉用户的兴趣演变。请根据历史序列推荐后续视频。"},
            {"role": "user", "content": "".join(sid_str(s) for s in sids) + "\n推荐后续视频："}]


class Scorer:
    def __init__(self, model_dir, thinking=False, chunk=256):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.tok = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForCausalLM.from_pretrained(model_dir, dtype=torch.bfloat16).to("cuda").eval()
        self.thinking, self.chunk = thinking, chunk
        ids = self.tok.convert_tokens_to_ids
        self.begin = ids("<|sid_begin|>")
        self.tid = lambda lvl, x: ids(f"<s_{lvl}_{x}>")

    @torch.no_grad()
    def logprobs(self, messages, sids):
        """Exact log P(item) for each semantic ID triple (the constant log P(<|sid_begin|>) is dropped)."""
        text = self.tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=self.thinking)
        prompt = torch.tensor([self.tok(text, add_special_tokens=False)["input_ids"]], device="cuda")
        out = self.model(input_ids=prompt, use_cache=True)
        cache, L = out.past_key_values, prompt.shape[1]
        cfg = self.model.config
        kv_bytes = 2 * 2 * cfg.num_hidden_layers * cfg.num_key_value_heads * cfg.head_dim * (L + 4)
        chunk = int(max(8, min(self.chunk, 16e9 // kv_bytes)))
        cache.batch_repeat_interleave(chunk)
        toks = torch.tensor([[self.begin, self.tid("a", a), self.tid("b", b), self.tid("c", c)] for a, b, c in sids], device="cuda")
        res = []
        for s in range(0, len(toks), chunk):
            x = toks[s:s + chunk]
            n = len(x)
            if n < chunk:
                x = torch.cat([x, x[:1].repeat(chunk - n, 1)])
            pos = torch.arange(L, L + 4, device="cuda").unsqueeze(0).expand(chunk, -1)
            lg = self.model(input_ids=x, past_key_values=cache, position_ids=pos, use_cache=True).logits.float()
            cache.crop(L)
            lp = torch.log_softmax(lg[:, :3], dim=-1)
            tgt = x[:, 1:4]
            res.append(lp.gather(2, tgt.unsqueeze(-1)).squeeze(-1).sum(1)[:n].cpu())
        return torch.cat(res).numpy()


def lse(x):
    m = x.max()
    return float(m + np.log(np.exp(x - m).sum()))


def main():
    model_dir, recif_dir, labels_path, out_path = sys.argv[1:5]
    n_users = int(sys.argv[5]) if len(sys.argv) > 5 else 30
    thinking = len(sys.argv) > 6 and sys.argv[6] == "1"
    controls = len(sys.argv) > 7 and sys.argv[7] == "controls"
    rng = random.Random(3)
    maps = Maps(recif_dir)
    rows = [json.loads(l) for l in open(labels_path, encoding="utf-8")]
    rows = [r for r in rows if r["issue"] == "是" and maps.has(r["pid"])]
    sc = Scorer(model_dir, thinking=thinking)
    lc = pq.read_table(f"{recif_dir}/benchmark_data/label_cond/label_cond_test.parquet").to_pylist()
    vt = pq.read_table(f"{recif_dir}/benchmark_data/video/video_test.parquet", columns=["hist_pid"]).to_pylist()
    off = [int(p) for p in rng.sample(list(maps.pid[~maps.pid_issue]), 600)]
    off_sids = [maps.sid_of(p) for p in off]
    out = {}
    attrs = dict(ATTRS)
    if controls:
        # Null attribute: a random subset of "no generalisation" items with the same size and genre mix as A.
        pool_b = [r for r in rows if ATTRS["gender_generalization"][1](r)]
        a_true = [r for r in rows if ATTRS["gender_generalization"][0](r)]
        fake = set()
        for g, c in Counter(r["genre"] for r in a_true).items():
            cand = [r["pid"] for r in pool_b if r["genre"] == g]
            fake.update(rng.sample(cand, min(c, len(cand))))
        attrs = {"null_random_subset": (lambda r, f=fake: r["pid"] in f, lambda r, f=fake: ATTRS["gender_generalization"][1](r) and r["pid"] not in f),
                 "gender_generalization_sidsplit": ATTRS["gender_generalization"],
                 "conflict_sidsplit": ATTRS["conflict"]}
    for attr, (is_a, is_b) in attrs.items():
        A_rows = [r for r in rows if is_a(r)]
        B_rows = [r for r in rows if is_b(r)]
        if len(A_rows) < 30:
            out[attr] = {"skipped": f"only {len(A_rows)} A items"}
            continue
        # Genre-matched B: same genre mix as A, so that A-vs-B contrasts are not genre contrasts.
        by_genre = {}
        for r in B_rows:
            by_genre.setdefault(r["genre"], []).append(r["pid"])
        for v in by_genre.values():
            rng.shuffle(v)
        ratio = min(3.0, min(len(by_genre.get(g, [])) / c for g, c in Counter(r["genre"] for r in A_rows).items()) or 1.0)
        B = []
        for g, c in Counter(r["genre"] for r in A_rows).items():
            B += by_genre.get(g, [])[:max(1, int(round(c * max(ratio, 1.0))))]
        A = [r["pid"] for r in A_rows]
        rng.shuffle(A); rng.shuffle(B)
        if attr.endswith("_sidsplit"):
            # Items sharing a first-level semantic code go to the same side, so near-duplicate stories
            # cannot appear in both the injected and the evaluated half.
            def split(items):
                codes = sorted({maps.sid_of(p)[0] for p in items}); rng.shuffle(codes)
                half = set(codes[:len(codes) // 2])
                return [p for p in items if maps.sid_of(p)[0] in half], [p for p in items if maps.sid_of(p)[0] not in half]
            A_inj, A_ev = split(A)
            B_inj, B_ev = split(B)
        else:
            A_inj, A_ev = A[:len(A) // 2], A[len(A) // 2:]
            B_inj, B_ev = B[:len(B) // 2], B[len(B) // 2:]
        ev = [maps.sid_of(p) for p in A_ev + B_ev] + off_sids
        nA, nB = len(A_ev), len(B_ev)

        def masses(lp):
            return lse(lp[:nA]), lse(lp[nA:nA + nB]), lse(lp[nA + nB:])

        recs = {"label_cond": [], "video_rec": []}
        seeds = [r for r in rng.sample(lc, 300) if len(r["hist_longview"]) >= 5][:n_users]
        for r in seeds:
            h0 = {k[5:]: [maps.sid_of(p) for p in r[k] if maps.has(p)] for k in r if k.startswith("hist_")}
            ia = [maps.sid_of(p) for p in rng.sample(A_inj, min(10, len(A_inj)))]
            ib = [maps.sid_of(p) for p in rng.sample(B_inj, 10)]
            conds = {"base": h0, "lv_A": {**h0, "longview": ia}, "lv_B": {**h0, "longview": ib},
                     "ni_A": {**h0, "not_interested": ia}, "ni_B": {**h0, "not_interested": ib}}
            recs["label_cond"].append({c: masses(sc.logprobs(label_cond_messages(h), ev)) for c, h in conds.items()})
        for r in rng.sample(vt, n_users):
            hs = [maps.sid_of(p) for p in r["hist_pid"] if maps.has(p)][-480:]
            ia = [maps.sid_of(p) for p in rng.sample(A_inj, min(20, len(A_inj)))]
            ib = [maps.sid_of(p) for p in rng.sample(B_inj, 20)]
            conds = {"base": hs, "add_A": hs + ia, "add_B": hs + ib}
            recs["video_rec"].append({c: masses(sc.logprobs(video_messages(h), ev)) for c, h in conds.items()})

        def summarise(lst, cond, ref="base"):
            dV = np.array([(x[cond][0] - x[cond][1]) - (x[ref][0] - x[ref][1]) for x in lst])
            dlm = np.array([np.logaddexp(x[cond][0], x[cond][1]) - np.logaddexp(x[ref][0], x[ref][1]) for x in lst])
            doff = np.array([x[cond][2] - x[ref][2] for x in lst])
            se = lambda v: float(v.std(ddof=1) / np.sqrt(len(v)))
            return {"dV": float(dV.mean()), "dV_se": se(dV), "dlogm": float(dlm.mean()), "dlogm_se": se(dlm),
                    "dlog_off": float(doff.mean()), "share_users_dV_pos": float((dV > 0).mean())}

        res = {"n_A_eval": nA, "n_B_eval": nB, "n_A_inject": len(A_inj), "genre_mix_A": dict(Counter(r["genre"] for r in A_rows))}
        for c in ("lv_A", "lv_B", "ni_A", "ni_B"):
            res[f"label_cond:{c}"] = summarise(recs["label_cond"], c)
        res["label_cond:lv_A-vs-lv_B"] = summarise(recs["label_cond"], "lv_A", "lv_B")
        res["label_cond:ni_A-vs-ni_B"] = summarise(recs["label_cond"], "ni_A", "ni_B")
        for c in ("add_A", "add_B"):
            res[f"video_rec:{c}"] = summarise(recs["video_rec"], c)
        res["video_rec:add_A-vs-add_B"] = summarise(recs["video_rec"], "add_A", "add_B")
        out[attr] = res
        print(attr, json.dumps(res, ensure_ascii=False), flush=True)
    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
