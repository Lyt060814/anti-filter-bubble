"""Exposure counts and draw multiplicities for the enriched gender sample (deepseek_label.py enrich mode).

Usage: python -I enrich_exposures.py RECIF_DIR LABELS_CSV OUT_PREFIX
The enrich mode drew the random stratum with replacement, weighted by exposure, then kept the first occurrence of
each video. This script reproduces that draw (same seed and order), checks that it yields exactly the random-stratum
pids in the labels file, and records for each video how often it was drawn before the cut-off. Weighting random-stratum
videos by this multiplicity restores an exposure-weighted sample of non-cue-word exposures.
Writes OUT_PREFIX_exposures.csv (pid, stratum, exposures, draws) and OUT_PREFIX_exposures_meta.json (pool totals).
"""
import csv
import json
import os
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deepseek_label as dl  # noqa: E402

recif_dir, labels, prefix = sys.argv[1:4]
rows = list(csv.DictReader(open(labels, encoding="utf-8")))
want_rand = [int(r["pid"]) for r in rows if r["stratum"] == "random_exposure_weighted"]
n_random = 2000
caps = dl.issue_captions(recif_dir)
cue = [p for p, c in caps.items() if any(k in c for k in dl.CUES)]
cue_set = set(cue)
cnt = dl.item_counts(recif_dir, set(caps))
seen = [p for p in cnt if cnt[p][0] > 0]
w = np.array([cnt[p][0] for p in seen], float)
rng = np.random.default_rng(29)
draws = np.array(seen)[rng.choice(len(seen), size=n_random * 3, p=w / w.sum())].tolist()
uniq, got, cut = [], set(), len(draws)
for i, p in enumerate(draws):
    if p not in got:
        got.add(p)
        uniq.append(p)
        if len(uniq) == n_random:
            cut = i + 1
            break
rand = [p for p in uniq if p not in cue_set]
assert rand == want_rand, "reproduced random stratum differs from the labels file"
mult = Counter(draws[:cut])
exp = lambda p: int(cnt[p][0]) if p in cnt else 0  # noqa: E731
with open(prefix + "_exposures.csv", "w", newline="", encoding="utf-8") as f:
    wr = csv.writer(f)
    wr.writerow(["pid", "stratum", "exposures", "draws"])
    for r in rows:
        p = int(r["pid"])
        wr.writerow([p, r["stratum"], exp(p), mult.get(p, 0) if r["stratum"] == "random_exposure_weighted" else ""])
tot = sum(int(cnt[p][0]) for p in caps if p in cnt)
cue_tot = sum(exp(p) for p in cue)
meta = {"candidate_pool": len(caps), "candidate_pool_exposures": tot, "cue_word_videos": len(cue),
        "cue_word_exposures": cue_tot, "non_cue_exposures": tot - cue_tot,
        "random_draws_until_cutoff": cut, "random_draws_on_cue_videos": sum(v for p, v in mult.items() if p in cue_set),
        "random_draws_on_non_cue_videos": sum(v for p, v in mult.items() if p not in cue_set),
        "reproduction_check": "passed: reproduced random stratum equals labels file (same pids, same order)",
        "weighting": "cue stratum: census, weight each video by its exposures; random stratum: each draw represents "
                     "non_cue_exposures / random_draws_on_non_cue_videos exposures (weight a video by its draws)"}
json.dump(meta, open(prefix + "_exposures_meta.json", "w"), indent=2)
print(json.dumps(meta))
