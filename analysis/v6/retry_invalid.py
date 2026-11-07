"""Diagnose and retry rows whose DeepSeek V4 Pro output was invalid (empty domain) in a stratified label file.

Usage: python -I retry_invalid.py RECIF_DIR LABELS_CSV OUT_PREFIX
For each invalid row, sends the same prompt up to 3 times and records why it failed (HTTP status, API error type,
finish_reason, unparseable JSON, or a valid reply whose fields fail the checks). Writes OUT_PREFIX_retry.csv
(pid, stratum, outcome, fields if now valid) and OUT_PREFIX_retry_meta.json with counts by stratum and outcome.
No caption text or model reasoning beyond the short `reason` field is written.
"""
import csv
import json
import os
import sys
import time
from collections import Counter

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deepseek_label as dl  # noqa: E402
import dual_model_check as dmc  # noqa: E402

recif_dir, labels, prefix = sys.argv[1:4]
rows = [r for r in csv.DictReader(open(labels, encoding="utf-8")) if r["domain"] == ""]
caps = dl.captions(recif_dir, {int(r["pid"]) for r in rows})
key = os.environ["DEEPSEEK_API_KEY"]
doms = "、".join(f'"{d}"' for d in dl.DOMAINS)
out = []
for r in rows:
    p = dl.BU_TEMPLATE.format(cap=(caps.get(int(r["pid"])) or "")[:1200], domains=doms)
    body = {"model": dl.MODEL, "messages": [{"role": "system", "content": dmc.SYSTEM}, {"role": "user", "content": p}],
            "max_tokens": 4000, "response_format": {"type": "json_object"}}
    outcome, fields = None, None
    for attempt in range(3):
        try:
            resp = requests.post("https://api.deepseek.com/chat/completions", headers={"Authorization": f"Bearer {key}"},
                                 json=body, timeout=180)
        except Exception as e:
            outcome = f"exception:{type(e).__name__}"
            time.sleep(3); continue
        if resp.status_code != 200:
            try:
                err = resp.json().get("error", {})
                outcome = f"http{resp.status_code}:{str(err.get('type') or err.get('code') or '')[:40]}:{str(err.get('message', ''))[:60]}"
            except Exception:
                outcome = f"http{resp.status_code}"
            time.sleep(3); continue
        ch = resp.json()["choices"][0]
        text = ch["message"].get("content") or ""
        fr = ch.get("finish_reason")
        d = dl.bu_parse(text)
        if d is not None:
            outcome, fields = "valid_on_retry", d
            break
        if fr != "stop":
            outcome = f"finish_reason:{fr}"
        elif not text.strip():
            outcome = "empty_content"
        else:
            try:
                j = json.loads(text[text.find("{"): text.rfind("}") + 1])
                bad = [k for k in ("domain", "opposing", "narrative_type") if k in j and
                       j[k] not in {"domain": dl.DOMAINS, "opposing": ("是", "否"), "narrative_type": dl.TYPES}[k]]
                outcome = "field_check_failed:" + ",".join(bad or ["opposing_type_mismatch"])
                if "domain" in bad:
                    outcome += ":" + str(j.get("domain"))[:12]
            except Exception:
                outcome = "unparseable_json"
    out.append({"pid": r["pid"], "stratum": r["stratum"], "outcome": outcome, **(fields or {})})
    print(r["stratum"], outcome, flush=True)
cols = ["pid", "stratum", "outcome", "domain", "issue", "opposing", "narrative_type", "reason"]
with open(prefix + "_retry.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, cols, extrasaction="ignore"); w.writeheader(); w.writerows(out)
meta = {"input": os.path.basename(labels), "n_invalid": len(rows), "model": dl.MODEL,
        "by_stratum_outcome": {f"{s}|{o.split(':')[0] if o else None}": n for (s, o), n in Counter((x["stratum"], x["outcome"]) for x in out).items()},
        "outcomes_detail": dict(Counter(x["outcome"] for x in out))}
json.dump(meta, open(prefix + "_retry_meta.json", "w"), ensure_ascii=False, indent=2)
print(json.dumps(meta, ensure_ascii=False))
