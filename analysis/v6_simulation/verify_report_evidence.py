"""Focused checks for the R5 additions, preserving the already-audited main run."""
from pathlib import Path
import csv,gzip,json,hashlib,re
import numpy as np
BASE=Path(__file__).parent


def read(name):
    with gzip.open(BASE/'results'/name,'rt',encoding='utf8') as f:yield from csv.DictReader(f)


def run():
    reference={}
    for family,case in (('group',27),('conflict',157)):
        for r in read(f'calibrated_escape_{family}_s0.02.csv.gz'):
            if int(r['case'])==case and r['strategy'] in ('S0','S6'):
                reference[(family,r['theta'],r['seed'],r['strategy'],r['step'])]=r
    n=0;matched=0
    for r in read('filter_v2_dynamic.csv.gz'):
        n+=1
        if r['strategy'] in ('S0','S6_assumed'):
            key=(r['family'],r['theta'],r['seed'],'S6' if r['strategy']=='S6_assumed' else 'S0',r['step'])
            if key in reference:
                expected=reference[key]
                assert np.allclose([float(r[k]) for k in ('m','V_supply','delta_V','delta_log_m','B_retention')],
                                   [float(expected[k]) for k in ('m','V_supply','delta_V','delta_log_m','B_retention')],atol=1e-12)
                matched+=1
    assert n==15360 and matched>0
    assert sum(1 for r in read('filter_v2_instant.csv.gz'))==41920
    screenshot=BASE.parents[1]/'report/screenshots/ruicong_calibrated_run.png'
    evidence=json.loads(screenshot.with_suffix('.meta.json').read_text())
    assert hashlib.sha256(screenshot.read_bytes()).hexdigest()==evidence['screenshot_sha256']
    log=screenshot.with_name('calibrated_run_output.txt').read_text(encoding='utf8').encode('utf8')
    assert hashlib.sha256(log).hexdigest()==evidence['source_log_sha256_normalized_lf']
    report=BASE.parents[1]/'report/sections/5_case_study.md'
    text=report.read_text(encoding='utf8')
    for relative in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text):assert (report.parent/relative).resolve().exists(),relative
    assert text.count('<!-- BEGIN XU RUICONG SIMULATION')==1 and text.count('<!-- END XU RUICONG SIMULATION -->')==1
    size=sum(p.stat().st_size for p in BASE.rglob('*') if p.is_file())
    assert size<60_000_000
    print(f'PASS R5: {n:,} dynamic and 41,920 static v2 sensitivity records; {matched:,} baseline values match merged R3.')
    print(f'PASS R5: four figure links, real screenshot/log hashes, simulation scope markers; analysis directory {size/1e6:.2f} MB.')


if __name__=='__main__':run()
