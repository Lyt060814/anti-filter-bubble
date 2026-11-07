"""Check issue21 outputs and preserve other authors' report material."""
from pathlib import Path
import csv,gzip,json,hashlib,subprocess
import numpy as np
from PIL import Image
BASE=Path(__file__).parent;ROOT=BASE.parents[1]


def read(name):
    with gzip.open(BASE/'results'/name,'rt',encoding='utf8') as f:return list(csv.DictReader(f))


def outside(text):
    a=text.index('<!-- BEGIN XU RUICONG SIMULATION:');end='<!-- END XU RUICONG SIMULATION -->';b=text.index(end,a)+len(end)
    return text[:a]+text[b:]


def run():
    original=subprocess.check_output(['git','show','55e3047:report/sections/5_case_study.md'],encoding='utf8')
    current=(ROOT/'report/sections/5_case_study.md').read_text(encoding='utf8')
    assert outside(original)==outside(current)
    print('PASS scope: Li Yitong 5.1 and all material outside Xu markers unchanged.')
    formation=read('l4_main_formation.csv.gz');endpoints=read('l4_main_endpoints.csv.gz')
    assert len(formation)==9760 and len(endpoints)==3840
    for r in formation:
        assert np.isfinite(float(r['V_supply'])) and 0<float(r['m'])<1
        if r['scenario']=='zero_lower':assert abs(float(r['V_supply']))<1e-12
    for r in endpoints:
        assert np.isfinite(float(r['V_supply']))
        if r['scenario']=='zero_lower' and r['strategy']!='S6':assert abs(float(r['delta_V']))<1e-12
    old={}
    with gzip.open(BASE/'results/calibrated_escape_group_s0.02.csv.gz','rt',encoding='utf8') as f:
        for r in csv.DictReader(f):
            if int(r['case'])==14:old[(r['theta'],r['seed'],r['strategy'],r['step'])]=r
    for r in endpoints:
        if r['scenario']=='zero_lower':
            ref=old[(r['theta'],r['seed'],r['strategy'],r['step'])]
            assert np.allclose([float(r[k]) for k in ('m','V_supply','delta_V','delta_log_m')],
                               [float(ref[k]) for k in ('m','V_supply','delta_V','delta_log_m')],atol=1e-12)
    print('PASS data: all seed records complete; zero limit matches preserved c/t=0 scan; S6 remains a separate output mechanism.')
    meta=json.loads((BASE/'figures/l4_main.meta.json').read_text())
    for name,sha in meta['source_sha256'].items():assert hashlib.sha256((BASE/name).read_text(encoding='utf8').encode()).hexdigest()==sha
    with Image.open(BASE/'figures/l4_main.png') as im:assert min(im.info['dpi'])>299
    assert (BASE/'figures/l4_main.pdf').read_bytes().startswith(b'%PDF')
    changed=subprocess.check_output(['git','diff','--name-only','55e3047','--','analysis/v6_simulation/results/calibrated_*','analysis/v6_simulation/figures/*calibrated*'],encoding='utf8')
    assert not changed.strip(),changed
    size=sum(p.stat().st_size for p in BASE.rglob('*') if p.is_file());assert size<60_000_000
    print(f'PASS provenance: source hashes, PNG 300 dpi/PDF, old upper files unchanged; directory {size/1e6:.2f} MB.')


if __name__=='__main__':run()
