"""Audit calibrated outputs independently of saved means; no real data used."""
from pathlib import Path
import csv,json,hashlib,gzip
from collections import defaultdict
import numpy as np
from PIL import Image
BASE=Path(__file__).parent


def rows(name):
    path=BASE/'results'/name
    if path.exists():
        with path.open() as f:yield from csv.DictReader(f)
    else:
        with gzip.open(str(path)+'.gz','rt') as f:yield from csv.DictReader(f)


def run():
    from calibrated_model import Model
    model=Model();u=np.zeros(6);_,before=model.state(model.pi(u))
    contrast=model.v[0]@(model.v[0]-model.v[1])
    for h in (-1e-5,1e-5):
        _,after=model.state(model.pi(u+h*model.v[0]))
        assert abs(after-before-h*contrast)<1e-10
    print('PASS signed local-feedback formula in calibrated model before coordinate clipping.')
    calibrations=list(rows('calibration_targets.csv'))
    assert len(calibrations)==262
    cases={int(r['case']):r for r in calibrations}
    for r in calibrations:
        assert abs(float(r['achieved_topic'])-float(r['topic_target']))<1e-10
        if r['attribute_target_matched']=='True':assert abs(float(r['achieved_attribute'])-float(r['attribute_target']))<1e-10
    print('PASS injection calibration: 262 cases; topic matches target; fitted attribute anchors match target.')
    endpoints={};n=0;observedm=[]
    for family in ('group','conflict'):
        for r in rows(f'calibrated_formation_{family}.csv'):
            n+=1;m=float(r['m']);v=float(r['V_supply'])
            assert 0<m<1 and np.isfinite(v)
            if float(r['ratio'])==0:assert abs(v)<1e-12
            if int(r['step'])==6000:endpoints[(int(r['case']),float(r['theta']),int(r['seed']))]=(m,v)
            if int(r['step'])==6000 and r['family']=='group' and r['scan']=='main_grid' and float(r['supply'])==.02 and float(r['prior'])==.15:
                observedm.append(m)
    compact=(BASE/'results/packaging_manifest.json').exists()
    assert n==(65520 if compact else 1278560)
    print(f'PASS formation: {n:,} per-seed snapshots; zero contrast; bounded probabilities.')
    print(f'Main group final topic-share range across seeds/ratios: {min(observedm):.4f}--{max(observedm):.4f}.')
    count=0;comparisons=defaultdict(dict)
    for family in ('group','conflict'):
        for s in (.02,.1,.5):
            for r in rows(f'calibrated_escape_{family}_s{s}.csv'):
                count+=1;key=(int(r['case']),float(r['theta']),int(r['seed']))
                step=int(r['step']);v=float(r['V_supply'])
                if r['strategy']=='S0' and step==0:
                    assert np.allclose([float(r['m']),v],endpoints[key],atol=1e-12)
                if r['strategy']=='S7' and step<=1000:
                    assert float(r['m'])==0 and np.isnan(v) and float(r['B_retention'])==0
                else:assert np.isfinite(v)
                if float(r['ratio'])==0 and not(r['strategy'] in ('S6','S7') and step<=1000):assert abs(v)<1e-12
                if key[0]==27 and key[1]==2 and step==1000 and r['strategy'] in ('S1a','S1b'):
                    comparisons[key][r['strategy']]=float(r['delta_V'])
    assert count==(971520 if compact else 1168640)
    print(f'PASS escape: {count:,} seed snapshots; all S0 starts match formation; S7 undefined skew handled.')
    vals=np.array([r['S1b']-r['S1a'] for r in comparisons.values()])
    assert len(vals)==20
    half=2.093*vals.std(ddof=1)/np.sqrt(20)
    print(f'Main fitted group S1b minus S1a, paired 20 seeds: mean {vals.mean():.6f}, 95% CI [{vals.mean()-half:.6f}, {vals.mean()+half:.6f}].')
    counts=defaultdict(lambda:[0,0,0])
    n=0
    for r in rows('calibrated_persistence.csv'):
        n+=1
        if r['right_censored']=='True' or r['reduction_present']=='False':assert np.isnan(float(r['half_life']))
        else:assert 1<=float(r['half_life'])<=2000
        if int(r['case'])==27 and float(r['theta'])==2 and r['reference']=='matched_S0':
            cc=counts[r['strategy']];cc[0]+=1;cc[1]+=r['reduction_present']=='True';cc[2]+=r['right_censored']=='True'
    assert n==461120
    print('PASS persistence: 461,120 records; undefined and right-censored times distinguished.')
    for k,v in counts.items():print(f'Persistence {k}: n={v[0]}, initial reductions={v[1]}, right-censored={v[2]} (matched S0).')
    for name in ('formation_calibrated','escape_calibrated','persistence_calibrated'):
        meta=json.loads((BASE/'figures'/f'{name}.meta.json').read_text())
        for source,expected in meta['source_sha256'].items():assert hashlib.sha256((BASE/source).read_text(encoding='utf8').encode()).hexdigest()==expected
        with Image.open(BASE/'figures'/f'{name}.png') as im:assert min(im.info['dpi'])>299
        assert (BASE/'figures'/f'{name}.pdf').read_bytes().startswith(b'%PDF')
    assert all(p.stat().st_size<100_000_000 for p in (BASE/'results').glob('calibrated_*.csv'))
    print('PASS artifacts: PNG 300 dpi/PDF, matching code hashes; every CSV under 100 MB.')
    ni=list(rows('ni_response_calibration.csv'))
    assert len(ni)==6 and all(r['attainable']=='True' and abs(float(r['residual']))<1e-9 for r in ni)
    assert sum(1 for r in rows('ni_calibrated_sensitivity.csv'))==4320
    print('PASS NI calibration: targets .39/.78/1.17 reproduced, 4,320 per-seed endpoint records.')
    print('Evidence: synthetic scenarios fitted to uncertain pilot anchors; no online-platform or belief claim.')


if __name__=='__main__':run()
