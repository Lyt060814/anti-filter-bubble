"""Manipulation checks for OneRec-1.7B as a simulated recommender (v5 feasibility).

Usage: CUDA_VISIBLE_DEVICES=0 python -I onerec_manipulation_probe.py MODEL_DIR RECIF_DIR OUT_JSON [N_USERS] [N_SAMPLES]

Steps
  0. Template check: which chat template (thinking on/off) yields valid semantic IDs, and a rough
     sampled recall against benchmark answers (sanity only; the paper reports beam-search Recall@32).
  1. Label-conditional prompts (sectioned history with a "not interested" section), per seed user:
       base      : the user's own history
       lv_issue  : long-view section replaced by 10 issue items        (topic responsiveness)
       lv_ctrl   : long-view section replaced by 10 random non-issue items
       ni_issue  : 10 issue items placed in the not-interested section  (negative feedback)
       ni_ctrl   : 10 random non-issue items placed in the not-interested section
     Recommendations are sampled at temperature 1 (the model's own distribution); the issue share m is
     the share of sampled semantic IDs that belong to issue items.
  2. Video-rec prompts (long exposure history, no feedback types): append 20 issue vs 20 random items.
  3. Item level: exact log-probability of the not-interested items and of their semantic-ID siblings.
Issue membership is keyword-based (candidates, not labels).
"""
import json
import random
import re
import sys
from collections import defaultdict

import numpy as np
import pyarrow.compute as pc
import pyarrow.parquet as pq

ISSUE = ["离婚", "婆媳", "婆婆", "女方", "男方", "家暴", "出轨", "AA制", "彩礼", "结婚", "婚姻", "相亲", "夫妻", "老公", "老婆"]
SYS = "你是一个内容推荐引擎，通过学习用户的互动历史，预测用户对新内容的反应。"
HEAD = {"longview": "用户长时观看过以下内容：", "like": "用户喜欢的内容：", "follow": "用户关注了这些内容的创作者：",
        "forward": "用户转发过以下内容：", "not_interested": "用户表示不感兴趣的内容："}
ASK = "请推荐能够吸引用户长时间观看的内容。"
SID_RE = re.compile(r"<\|sid_begin\|><s_a_(\d+)><s_b_(\d+)><s_c_(\d+)><\|sid_end\|>")


def sid_str(s):
    return f"<|sid_begin|><s_a_{s[0]}><s_b_{s[1]}><s_c_{s[2]}><|sid_end|>"


def key(a, b, c):
    return (int(a) << 26) | (int(b) << 13) | int(c)


class Maps:
    """Sorted-array lookups: pid -> semantic ID, semantic ID -> share of its items that are issue candidates."""

    def __init__(self, recif_dir):
        import os
        cache = f"{recif_dir}/cache_v5_maps.npz"
        if os.path.exists(cache):
            z = np.load(cache)
            self.pid, self.sid, self.pid_issue, self.ukey, self.ufrac = (z[k] for k in ("pid", "sid", "pid_issue", "ukey", "ufrac"))
            return
        t = pq.read_table(f"{recif_dir}/video_ad_pid2sid.parquet")
        pids = t.column("pid").to_numpy().astype(np.int64)
        flat = pc.list_flatten(t.column("sid")).to_numpy().astype(np.int64)
        sids = flat.reshape(-1, 3)
        f = pq.ParquetFile(f"{recif_dir}/pid2caption.parquet")
        issue = []
        for rg in range(f.num_row_groups):
            tt = f.read_row_group(rg, columns=["pid", "dense_caption"])
            caps = tt.column("dense_caption")
            m = None
            for k in ISSUE:
                x = pc.match_substring(caps, k)
                m = x if m is None else pc.or_(m, x)
            issue.append(tt.column("pid").to_numpy()[np.asarray(pc.fill_null(m, False).to_numpy(zero_copy_only=False))])
        issue = np.unique(np.concatenate(issue)).astype(np.int64)
        o = np.argsort(pids)
        self.pid, self.sid = pids[o], sids[o]
        self.pid_issue = np.isin(self.pid, issue)
        keys = (self.sid[:, 0] << 26) | (self.sid[:, 1] << 13) | self.sid[:, 2]
        o2 = np.argsort(keys, kind="stable")
        ks, iss = keys[o2], self.pid_issue[o2]
        self.ukey, start, counts = np.unique(ks, return_index=True, return_counts=True)
        self.ufrac = np.add.reduceat(iss.astype(float), start) / counts
        np.savez(cache, pid=self.pid, sid=self.sid, pid_issue=self.pid_issue, ukey=self.ukey, ufrac=self.ufrac)

    def has(self, p):
        i = np.searchsorted(self.pid, p)
        return i < len(self.pid) and self.pid[i] == p

    def sid_of(self, p):
        return tuple(int(x) for x in self.sid[np.searchsorted(self.pid, p)])

    def is_issue(self, p):
        return bool(self.pid_issue[np.searchsorted(self.pid, p)])

    def issue_frac(self, k):
        i = np.searchsorted(self.ukey, k)
        return float(self.ufrac[i]) if i < len(self.ukey) and self.ukey[i] == k else None


def build_prompt(tok, hist, thinking):
    lines = ["以下是用户的历史互动行为："]
    for k in ["longview", "like", "follow", "forward", "not_interested"]:
        if hist.get(k):
            lines.append(HEAD[k] + "".join(sid_str(s) for s in hist[k]))
    lines.append(ASK)
    msgs = [{"role": "system", "content": SYS}, {"role": "user", "content": "\n".join(lines)}]
    return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=thinking)


def video_prompt(tok, sids, thinking):
    msgs = [{"role": "system", "content": "你是一位视频推荐系统专家，擅长捕捉用户的兴趣演变。请根据历史序列推荐后续视频。"},
            {"role": "user", "content": "".join(sid_str(s) for s in sids) + "\n推荐后续视频："}]
    return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=thinking)


def parse(texts):
    return [tuple(map(int, m)) for t in texts for m in SID_RE.findall(t)]


def issue_share(outs, maps):
    found = [maps.issue_frac(key(*s)) for s in parse(o.text for o in outs)]
    valid = [x for x in found if x is not None]
    return {"n": len(outs), "valid": len(valid), "m": float(np.mean(valid)) if valid else float("nan")}


def main():
    model_dir, recif_dir, out_path = sys.argv[1:4]
    n_users = int(sys.argv[4]) if len(sys.argv) > 4 else 40
    n_samples = int(sys.argv[5]) if len(sys.argv) > 5 else 2000
    rng = random.Random(0)
    from vllm import LLM, SamplingParams
    maps = Maps(recif_dir)
    print("maps loaded", len(maps.pid), len(maps.ukey), int(maps.pid_issue.sum()), flush=True)
    llm = LLM(model=model_dir, dtype="bfloat16", enable_prefix_caching=True, gpu_memory_utilization=0.85,
              max_model_len=8192, seed=0)
    tok = llm.get_tokenizer()
    out = {}
    # Popular issue / non-issue pools from the benchmark histories (items users actually saw).
    lc = pq.read_table(f"{recif_dir}/benchmark_data/label_cond/label_cond_test.parquet").to_pylist()
    seen = defaultdict(int)
    for r in lc:
        for k in ("hist_longview", "hist_like"):
            for p in r[k]:
                seen[p] += 1
    pool = [p for p, c in sorted(seen.items(), key=lambda x: -x[1]) if maps.has(p)]
    issue_pool = [p for p in pool if maps.is_issue(p)][:400]
    ctrl_pool = [p for p in pool if not maps.is_issue(p)][:400]
    out["pools"] = {"issue": len(issue_pool), "ctrl": len(ctrl_pool)}
    # 0. Template check on benchmark rows.
    sp32 = SamplingParams(n=64, temperature=1.0, top_p=1.0, top_k=-1, max_tokens=8, seed=1)
    rows = rng.sample(lc, 60)
    for thinking in (False, True):
        prompts, answers = [], []
        for r in rows:
            m = json.loads(r["messages"])
            msgs = [{"role": x["role"], "content": x["content"][0]["text"]} for x in m]
            prompts.append(tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=thinking))
            answers.append(set(json.loads(r["metadata"])["answer_pid"]))
        res = llm.generate(prompts, sp32, use_tqdm=False)
        valid = hits = total = 0
        for o, ans in zip(res, answers):
            sids = parse(c.text for c in o.outputs)
            valid += len(sids)
            total += len(o.outputs)
            rec = {key(*s) for s in sids}
            hits += len([p for p in ans if maps.has(p) and key(*maps.sid_of(p)) in rec]) / max(len(ans), 1)
        out[f"template_thinking_{thinking}"] = {"valid_sid_rate": valid / total, "sampled_recall@64": hits / len(rows),
                                                 "example": res[0].outputs[0].text[:120]}
        print(out[f"template_thinking_{thinking}"], flush=True)
    thinking = out["template_thinking_True"]["valid_sid_rate"] > out["template_thinking_False"]["valid_sid_rate"] + 0.2
    out["thinking_used"] = thinking
    # 1. Label-conditional manipulations.
    sp = SamplingParams(n=n_samples, temperature=1.0, top_p=1.0, top_k=-1, max_tokens=8, seed=2)
    seeds = [r for r in rng.sample(lc, 400) if len(r["hist_longview"]) >= 5][:n_users]
    conds = ["base", "lv_issue", "lv_ctrl", "ni_issue", "ni_ctrl"]
    per = {c: [] for c in conds}
    ni_items = {}
    for ui, r in enumerate(seeds):
        h0 = {k[5:]: [maps.sid_of(p) for p in r[k] if maps.has(p)] for k in r if k.startswith("hist_")}
        iss = rng.sample(issue_pool, 10)
        ctl = rng.sample(ctrl_pool, 10)
        variants = {"base": h0,
                    "lv_issue": {**h0, "longview": [maps.sid_of(p) for p in iss]},
                    "lv_ctrl": {**h0, "longview": [maps.sid_of(p) for p in ctl]},
                    "ni_issue": {**h0, "not_interested": [maps.sid_of(p) for p in iss]},
                    "ni_ctrl": {**h0, "not_interested": [maps.sid_of(p) for p in ctl]}}
        ni_items[ui] = iss
        res = llm.generate([build_prompt(tok, variants[c], thinking) for c in conds], sp, use_tqdm=False)
        for c, o in zip(conds, res):
            s = issue_share(o.outputs, maps)
            # Item-level: how often are the 10 manipulated issue items themselves (or SID twins) sampled?
            target = {key(*maps.sid_of(p)) for p in iss}
            s["target_rate"] = sum(key(*x) in target for x in parse(z.text for z in o.outputs)) / max(s["valid"], 1)
            per[c].append(s)
        print(ui, {c: round(per[c][-1]["m"], 4) for c in conds}, flush=True)
    def summ(c):
        m = np.array([x["m"] for x in per[c]]); t = np.array([x["target_rate"] for x in per[c]])
        v = np.array([x["valid"] / x["n"] for x in per[c]])
        return {"m_mean": float(np.nanmean(m)), "m_median": float(np.nanmedian(m)), "target_rate_mean": float(t.mean()),
                "valid_rate": float(v.mean())}
    out["label_cond"] = {c: summ(c) for c in conds}
    diffs = {}
    for a, b in [("lv_issue", "lv_ctrl"), ("ni_issue", "ni_ctrl"), ("ni_issue", "base"), ("lv_issue", "base")]:
        d = np.array([x["m"] - y["m"] for x, y in zip(per[a], per[b])])
        lr = np.array([np.log((x["m"] + 1e-4) / (y["m"] + 1e-4)) for x, y in zip(per[a], per[b])])
        tr = np.array([x["target_rate"] - y["target_rate"] for x, y in zip(per[a], per[b])])
        diffs[f"{a}-{b}"] = {"mean_diff_m": float(d.mean()), "se": float(d.std(ddof=1) / np.sqrt(len(d))),
                             "share_users_lower": float((d < 0).mean()), "mean_log_ratio_m": float(lr.mean()),
                             "mean_diff_target_rate": float(tr.mean()), "se_target": float(tr.std(ddof=1) / np.sqrt(len(tr)))}
    out["label_cond_diffs"] = diffs
    # 2. Video-rec prompts with long histories.
    vt = pq.read_table(f"{recif_dir}/benchmark_data/video/video_test.parquet", columns=["hist_pid"]).to_pylist()
    vseeds = rng.sample(vt, n_users)
    vres = {"base": [], "add_issue": [], "add_ctrl": []}
    for r in vseeds:
        hs = [maps.sid_of(p) for p in r["hist_pid"] if maps.has(p)][-480:]
        iss = [maps.sid_of(p) for p in rng.sample(issue_pool, 20)]
        ctl = [maps.sid_of(p) for p in rng.sample(ctrl_pool, 20)]
        res = llm.generate([video_prompt(tok, hs, thinking), video_prompt(tok, hs + iss, thinking), video_prompt(tok, hs + ctl, thinking)], sp, use_tqdm=False)
        for c, o in zip(vres, res):
            vres[c].append(issue_share(o.outputs, maps))
    out["video_rec"] = {c: {"m_mean": float(np.nanmean([x["m"] for x in v])), "valid_rate": float(np.mean([x["valid"] / x["n"] for x in v]))} for c, v in vres.items()}
    d = np.array([x["m"] - y["m"] for x, y in zip(vres["add_issue"], vres["add_ctrl"])])
    out["video_rec"]["add_issue-add_ctrl"] = {"mean_diff_m": float(d.mean()), "se": float(d.std(ddof=1) / np.sqrt(len(d)))}
    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
