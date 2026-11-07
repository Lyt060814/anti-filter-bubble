"""Add portable text hashing to genuine screenshot provenance."""
from pathlib import Path
import json,hashlib
folder=Path(__file__).parents[2]/'report/screenshots'
p=folder/'ruicong_calibrated_run.meta.json'
m=json.loads(p.read_text());m['source_log_hash_format']='raw original plus UTF-8 normalized LF for cross-platform verification'
m['source_log_sha256_normalized_lf']=hashlib.sha256((folder/'calibrated_run_output.txt').read_text(encoding='utf8').encode()).hexdigest()
p.write_text(json.dumps(m,indent=2),encoding='utf8')
