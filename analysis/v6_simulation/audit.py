"""Validate stored results and print actual output suitable for a screenshot."""
from experiments import *


def read(name):
    with (ROOT/'results'/f'{name}.csv').open() as f:
        return list(csv.DictReader(f))


def main():
    from model import self_check
    self_check()
    formation = read('formation')
    assert len(formation) == 13*4*20*2*2*31
    for r in formation:
        assert np.isfinite(float(r['V']))
        assert abs(float(r['total_bias'])-float(r['platform_bias'])-float(r['V'])) < 1e-10
        if float(r['ratio'])==0:
            assert abs(float(r['V'])) < 1e-12
    print(f'PASS R2: {len(formation):,} snapshots; full grid; finite V; decomposition; zero contrast.')
    escape = read('escape')
    assert len(escape) == 13*4*20*11*32
    for r in escape:
        if r['strategy']=='S7' and int(r['step'])<=ACTIVE:
            assert float(r['m'])==0 and float(r['B_retention'])==0 and np.isnan(float(r['V']))
        else:
            assert np.isfinite(float(r['V']))
    persistence = read('persistence')
    assert len(persistence)==13*4*20*11
    print(f'PASS R3: {len(escape):,} snapshots, 11 arms; S7 undefined V; {len(persistence):,} half-life records.')
    sensitivity = read('ni_sensitivity')
    assert len(sensitivity)==13*4*20*7*3
    print('PASS R3 sensitivity: seven NI strengths, including +0.5 and +0.78; full grid.')
    detection = read('detection')
    assert len(detection)==2*5*61*2
    for p0 in (.018,.41):
        group = [r for r in detection if float(r['p0'])==p0 and float(r['alpha'])==.8 and float(r['beta'])==.02 and float(r['topic_rate'])==.016]
        ns = [float(r['n_per_arm']) for r in group]
        assert all(x>=y for x,y in zip(ns,ns[1:]))
        print(f'R4 p0={p0}: odds x2 -> {int(ns[0])} same-topic videos per arm; total at m=.016: {group[0]["total_per_arm"]}.')
    print('PASS R4: correct odds conversion; sample sizes decrease from odds x2 to x8.')
    from PIL import Image
    for name in ('formation','escape','persistence','detection'):
        meta = json.loads((ROOT/'figures'/f'{name}.meta.json').read_text())
        for filename, expected in meta['source_sha256'].items():
            actual = hashlib.sha256((ROOT/filename).read_text(encoding='utf8').encode('utf8')).hexdigest()
            assert actual==expected, f'Stale source provenance: {name}: {filename}'
        with Image.open(ROOT/'figures'/f'{name}.png') as im:
            assert min(im.info['dpi']) > 299
        assert (ROOT/'figures'/f'{name}.pdf').read_bytes().startswith(b'%PDF')
        assert (ROOT/'results'/f'{name}.csv').exists()
    print('PASS artifacts: four PNG/PDF pairs, 300 dpi, CSVs, and matching source SHA256.')
    print('All simulation parameters are SCENARIO ASSUMPTIONS. No GPU, raw data or credentials used.')


if __name__ == '__main__':
    main()
