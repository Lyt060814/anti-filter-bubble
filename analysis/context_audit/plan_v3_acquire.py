"""Acquire bounded primary-source snapshots for v3; never download model weights.

Usage: python3 analysis/context_audit/plan_v3_acquire.py SOURCE_ROOT
Existing checkouts are inspected, never pulled or reset. Large datasets are
checked separately. Acquisition is not a claim of reading or reproduction.
"""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone
import requests

REPOS = {
    "KuaiSim": "Applied-Machine-Learning-Lab/KuaiSim",
    "LLM_User_Simulator": "Applied-Machine-Learning-Lab/LLM_User_Simulator",
    "YuLan-Rec": "RUC-GSAI/YuLan-Rec",
    "Qwen3-VL": "QwenLM/Qwen3-VL",
    "Qwen3-Omni": "QwenLM/Qwen3-Omni",
    "SenseVoice": "FunAudioLLM/SenseVoice",
    "FlagEmbedding": "FlagOpen/FlagEmbedding",
    "Qwen-Agent": "QwenLM/Qwen-Agent",
    "OpenOneRec": "Kuaishou-OneRec/OpenOneRec",
    "zr-obp": "st-tech/zr-obp",
    "RecAI": "microsoft/RecAI",
    "Qwen3-Embedding": "QwenLM/Qwen3-Embedding",
    "Qwen3-VL-Embedding": "QwenLM/Qwen3-VL-Embedding",
    "naacl24-user-sim": "granelle/naacl24-user-sim",
}
PAPERS = {
    "llm_user_simulator": "https://arxiv.org/pdf/2412.16984",
    "user_simulator_evaluation": "https://aclanthology.org/2024.naacl-long.83.pdf",
    "kuaisim": "https://arxiv.org/pdf/2309.12645",
    "qwen3_omni": "https://arxiv.org/pdf/2509.17765",
    "bge_m3": "https://arxiv.org/pdf/2402.03216",
    "open_bandit": "https://arxiv.org/pdf/2008.07146",
}

def acquire_repo(root, name, slug):
    path = root / "code" / name
    url = f"https://github.com/{slug}.git"
    row = {"kind": "code", "name": name, "url": url, "path": str(path)}
    try:
        if not path.exists():
            subprocess.run(["git", "clone", "--depth", "1", "--filter=blob:none", url, str(path)],
                           check=True, capture_output=True, timeout=180,
                           env={**os.environ, "GIT_LFS_SKIP_SMUDGE": "1", "GIT_TERMINAL_PROMPT": "0"})
        row["commit"] = subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()
        row["license_files"] = [str(p.relative_to(path)) for p in path.glob("*LICENSE*")]
        row["status"] = "downloaded_not_reproduced"
    except Exception as e:
        row["status"] = "failed"
        row["error"] = str(e)
    return row

def acquire_paper(root, name, url):
    path = root / "papers" / "v3" / f"{name}.pdf"
    row = {"kind": "paper", "name": name, "url": url, "path": str(path)}
    try:
        if not path.exists():
            r = requests.get(url, timeout=90)
            r.raise_for_status()
            if not r.content.startswith(b"%PDF"):
                raise ValueError("Response is not a PDF")
            path.write_bytes(r.content)
        row.update(bytes=path.stat().st_size, sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        subprocess.run(["pdftotext", "-layout", str(path), str(path.with_suffix(".txt"))], check=True, timeout=30)
        row["status"] = "downloaded_text_extracted"
    except Exception as e:
        row.update(status="failed", error=str(e))
    return row

def main():
    root = Path(sys.argv[1]).resolve()
    (root / "code").mkdir(parents=True, exist_ok=True)
    (root / "papers" / "v3").mkdir(parents=True, exist_ok=True)
    output = Path(__file__).resolve().parents[2] / "docs/context-recovery/plan_v3_acquisition.json"
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [pool.submit(acquire_repo, root, n, u) for n, u in REPOS.items()]
        jobs += [pool.submit(acquire_paper, root, n, u) for n, u in PAPERS.items()]
        rows = []
        for job in concurrent.futures.as_completed(jobs):
            row = job.result()
            rows.append(row)
            print(row["name"], row["status"], flush=True)
    output.write_text(json.dumps({"created_at": datetime.now(timezone.utc).isoformat(),
                                 "scope": "Acquisition only; reading and smoke checks documented separately",
                                 "resources": sorted(rows, key=lambda x: x["name"])}, indent=2) + "\n")

if __name__ == "__main__":
    main()
