"""Download RecIF files (gated; requires the user's accepted access and local HF token)."""
import os
import sys
os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "1")
from huggingface_hub import hf_hub_download

target = sys.argv[1]
for name in sys.argv[2:]:
    path = hf_hub_download("OpenOneRec/OpenOneRec-RecIF", name, repo_type="dataset", local_dir=target)
    print(name, os.path.getsize(path), flush=True)
