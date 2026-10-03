"""Verify KuaiSAR v2 archive and inspect bounded CSV prefixes, not full data.

python3 analysis/context_audit/plan_v3_kuaisar_probe.py SOURCE_ROOT
"""
import hashlib
import json
from pathlib import Path
import sys
import zipfile
import pandas as pd
import requests

root = Path(sys.argv[1]).resolve() / 'data/kuaisar'
root.mkdir(parents=True, exist_ok=True)
record = requests.get('https://zenodo.org/api/records/8181109', timeout=30).json()
(root/'record.json').write_text(json.dumps(record))
remote = next(f for f in record['files'] if f['key'] == 'KuaiSAR_v2.zip')
path = root / remote['key']
if not path.exists():
    partial = path.with_suffix('.zip.partial')
    with requests.get(remote['links']['self'], stream=True, timeout=60) as response:
        response.raise_for_status()
        with partial.open('wb') as out:
            for chunk in response.iter_content(4*1024*1024):
                out.write(chunk)
    partial.rename(path)
md5, sha = hashlib.md5(), hashlib.sha256()
with path.open('rb') as f:
    while chunk := f.read(4*1024*1024):
        md5.update(chunk)
        sha.update(chunk)
assert remote['checksum'] == 'md5:' + md5.hexdigest(), 'Publisher checksum mismatch'
rows = []
with zipfile.ZipFile(path) as archive:
    for info in archive.infolist():
        with archive.open(info) as f:
            frame = pd.read_csv(f, nrows=5000)
        row = {'member': info.filename, 'uncompressed_bytes': info.file_size,
               'inspected_prefix_rows': len(frame), 'columns': frame.columns.tolist(),
               'non_null_in_prefix': {c:int(v) for c,v in frame.notna().sum().items()}}
        # playing_time is a duration, not the event timestamp.
        time_columns = [c for c in ['timestamp', 'search_session_timestamp', 'time'] if c in frame]
        user_columns = [c for c in frame if c.lower() in ['user_id','uid']]
        if time_columns and user_columns:
            keys = [user_columns[0], time_columns[0]]
            row['duplicate_user_time_keys'] = keys
            row['duplicate_user_time_prefix_rows'] = int(frame.duplicated(keys, keep=False).sum())
        rows.append(row)
result = {'source': remote['links']['self'], 'bytes': path.stat().st_size,
          'sha256': sha.hexdigest(), 'publisher_md5_matches': True,
          'scope': 'First 5000 rows per CSV only; not population counts, causal effects, or semantic labels',
          'files': rows}
Path('docs/context-recovery/plan_v3_kuaisar_probe.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
