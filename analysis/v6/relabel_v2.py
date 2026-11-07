"""Relabel a CSV of marriage-and-family pids with DeepSeek V4 Pro and an external prompt module (e.g. prompt_v2.py).

Usage: python -I relabel_v2.py RECIF_DIR IN_CSV PROMPT_MODULE OUT_PREFIX
Keeps the IN_CSV `stratum` column; writes OUT_PREFIX_labels.csv (pid, stratum, all prompt fields, reason) and meta.
"""
import csv
import importlib.util
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deepseek_label import call, captions  # noqa: E402

recif_dir, in_csv, mod_path, prefix = sys.argv[1:5]
spec = importlib.util.spec_from_file_location("prompt_mod", mod_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
rows = list(csv.DictReader(open(in_csv, encoding="utf-8")))
pids = [int(r["pid"]) for r in rows]
caps = captions(recif_dir, pids)
t0 = time.time()
res = call([mod.TEMPLATE.format(cap=caps[p][:1200]) for p in pids], mod.parse, mod.SYSTEM)
cols = list(mod.FIELDS) + ["reason"]
with open(prefix + "_labels.csv", "w", newline="", encoding="utf-8") as f:
    wr = csv.writer(f)
    wr.writerow(["pid", "stratum"] + cols)
    for r, d in zip(rows, res):
        wr.writerow([r["pid"], r.get("stratum", "")] + [(d or {}).get(c, "") for c in cols])
meta = {"source": in_csv, "prompt_version": mod.PROMPT_VERSION, "model": "deepseek-v4-pro", "n": len(pids),
        "parsed": sum(d is not None for d in res), "seconds": round(time.time() - t0), "date": time.strftime("%Y-%m-%d")}
json.dump(meta, open(prefix + "_meta.json", "w"), ensure_ascii=False, indent=2)
print(json.dumps(meta))
