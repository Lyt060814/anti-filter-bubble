"""Artifact helpers for reviewed, scenario-only simulations."""
from pathlib import Path
import csv,json,hashlib,subprocess,sys
import numpy as np
import matplotlib.pyplot as plt
BASE=Path(__file__).parent


def save(name,rows):
    (BASE/'results').mkdir(exist_ok=True)
    with (BASE/'results'/f'{name}.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)


def ci(x):
    return np.mean(x,axis=-1),2.093*np.std(x,axis=-1,ddof=1)/np.sqrt(20)


def meta(name,details,scripts):
    data=dict(git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
              python=sys.version,numpy=np.__version__,
              source_sha256={s:hashlib.sha256((BASE/s).read_text(encoding='utf8').encode()).hexdigest() for s in scripts},
              source_hash_format='UTF-8 normalized LF',**details)
    for folder in ('results','figures'):
        (BASE/folder).mkdir(exist_ok=True)
        (BASE/folder/f'{name}.meta.json').write_text(json.dumps(data,indent=2),encoding='utf8')


def fig(name,details,scripts,note='Synthetic scenarios; pilot-matched scales; remaining parameters assumed. Pointwise 95% Monte Carlo intervals, 20 seeds.'):
    plt.gcf().text(.5,.006,note,ha='center',fontsize=7)
    plt.tight_layout(rect=(0,.035,1,1))
    (BASE/'figures').mkdir(exist_ok=True)
    for ext in ('png','pdf'): plt.savefig(BASE/'figures'/f'{name}.{ext}',dpi=300)
    plt.close()
    meta(name,details,scripts)
