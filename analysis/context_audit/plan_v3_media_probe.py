"""Download paired ShortVideo media for feasibility, not a representative audit.

Uses publisher-provided public access credentials from its local README; never
logs them. Selects up to two keyword hits for each of three broad issues and
two non-issue controls. Sequential downloads respect the host concurrency rule.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import pandas as pd
import requests

root = Path(sys.argv[1]).resolve()
readme = (root / 'code/ShortVideo_dataset/README.md').read_text()
auth = (re.search(r'\*\*Username:\*\* (\S+)', readme).group(1),
        re.search(r'\*\*Password:\*\* ([^)]+)', readme).group(1))
data = pd.read_csv(root / 'data/shortvideo/interaction_sampled.csv', usecols=['pid', 'title', 'tag_name'])
data = data.drop_duplicates('pid').sort_values('pid')
text = data.title.fillna('') + ' ' + data.tag_name.fillna('')
groups = {'relationships': '婚姻|彩礼|夫妻|结婚', 'parenting': '育儿|教育|孩子|家长', 'career': '工作|职业|辞职|打工'}
selected = {}
for group, pattern in groups.items():
    hits = data[text.str.contains(pattern, regex=True)].head(2)
    for pid in hits.pid:
        selected.setdefault(int(pid), []).append(group)
for pid in data[~text.str.contains('|'.join(groups.values()), regex=True)].head(2).pid:
    selected.setdefault(int(pid), []).append('control')
folder = root / 'data/audit/plan_v3/media'
folder.mkdir(parents=True, exist_ok=True)
base = 'https://fi.ee.tsinghua.edu.cn/datasets/short-video-dataset/'
rows = []
for pid, labels in selected.items():
    row = {'pid': pid, 'selection_groups': labels, 'files': []}
    for remote, ext in [('raw_file', 'mp4'), ('asr_zn', 'txt')]:
        target = folder / f'{pid}.{ext}'
        f = {'url': f'{base}{remote}/{pid}.{ext}', 'path': str(target)}
        try:
            if not target.exists():
                response = requests.get(f['url'], auth=auth, timeout=60)
                response.raise_for_status()
                target.write_bytes(response.content)
            f.update(bytes=target.stat().st_size, sha256=hashlib.sha256(target.read_bytes()).hexdigest())
            if ext == 'mp4':
                p = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name,width,height','-of','json', str(target)], capture_output=True, text=True, check=True)
                f['probe'] = json.loads(p.stdout)
                subprocess.run(['ffmpeg','-v','error','-y','-i',str(target),'-frames:v','1',str(folder/f'{pid}.jpg')],check=True)
                subprocess.run(['ffmpeg','-v','error','-y','-i',str(target),'-vn','-ac','1','-ar','16000',str(folder/f'{pid}.wav')],check=True)
                f['decode'] = 'frame_and_16khz_audio_pass'
            else:
                f['characters'] = len(target.read_text())
            f['status'] = 'pass'
        except Exception as e:
            f.update(status='failed', error=str(e))
        row['files'].append(f)
    rows.append(row)
    print(pid, [f['status'] for f in row['files']], flush=True)
out = Path(__file__).resolve().parents[2] / 'docs/context-recovery/plan_v3_media_probe.json'
out.write_text(json.dumps({'selection': 'first two unique IDs per keyword group and two controls; convenience feasibility sample, not semantic labels', 'rows': rows}, indent=2) + '\n')
