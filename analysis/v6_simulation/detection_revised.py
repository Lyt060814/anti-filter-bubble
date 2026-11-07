"""R4: deterministic two-arm analytic scenario, with task-specific provenance."""
import csv,json,hashlib,subprocess,sys
from pathlib import Path
from statistics import NormalDist
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from v2_detection_inputs import load as load_v2
BASE=Path(__file__).parent


def run():
    rows=[]
    v2=load_v2()
    sources=[('DeepSeek v2',v2['p0'],'dual_v2_labels.csv; main reference'),('DeepSeek v0',.014,'agreement.md section 2'),
             ('DeepSeek v1',.006,'agreement.md section 5; unstable definition'),('Qwen v5',.018,'research_plan_v5.md section 4'),
             ('Conflict v5',.41,'research_plan_v5.md section 4')]
    classifiers=[('assumed',.8,.02),('recall_0.7',.7,.02),('recall_0.9',.9,.02),('fpr_0',.8,0),('fpr_0.05',.8,.05),
                 ('Qwen_vs_DeepSeek_v2',v2['recall'],v2['false_positive_rate'])]
    z=NormalDist().inv_cdf(.95)+NormalDist().inv_cdf(.8)
    for version,p0,source in sources:
        for classifier,alpha,beta in classifiers:
            last=np.inf
            for odds in np.linspace(2,8,61):
                p=odds*p0/(1-p0+odds*p0)
                q=beta+(alpha-beta)*p;q0=beta+(alpha-beta)*p0
                exact=z*z*(q*(1-q)+q0*(1-q0))/((alpha-beta)**2*(p-p0)**2)
                assert exact<=last+1e-10
                last=exact;n=int(np.ceil(exact))
                for rate in (.016,.036):
                    rows.append(dict(version=version,p0=p0,source=source,classifier=classifier,odds=odds,alpha=alpha,beta=beta,
                         topic_rate=rate,n_per_arm=n,total_per_arm=int(np.ceil(n/rate)),
                         both_arms_total=2*int(np.ceil(n/rate))))
    (BASE/'results').mkdir(exist_ok=True);(BASE/'figures').mkdir(exist_ok=True)
    with (BASE/'results/detection_revised.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    for version,p0,_ in sources:
        group=[r for r in rows if r['version']==version and r['classifier']=='assumed' and r['topic_rate']==.016]
        axes[0].plot([r['odds'] for r in group],[r['n_per_arm'] for r in group],label=f'{version}: {p0:.1%}',lw=2 if version=='DeepSeek v2' else 1)
    for classifier in ('assumed','Qwen_vs_DeepSeek_v2'):
        for rate in (.016,.036):
            group=[r for r in rows if r['version']=='DeepSeek v2' and r['classifier']==classifier and r['topic_rate']==rate]
            axes[1].plot([r['odds'] for r in group],[r['total_per_arm'] for r in group],label=f'{classifier}; m={rate:.1%}',linestyle='--' if classifier!='assumed' else '-')
    for ax,y in zip(axes,('Same-topic videos PER ARM','Total exposures PER ARM')):
        ax.set(xlabel='Odds multiplier',ylabel=y,yscale='log');ax.legend(fontsize=6)
    fig.text(.5,.006,'Analytic approximation; v2 main reference; assumed and Qwen-vs-DeepSeek classifier cases. Model cross-check is not gold-standard accuracy.',ha='center',fontsize=7)
    fig.tight_layout(rect=(0,.04,1,1))
    for ext in ('png','pdf'): fig.savefig(BASE/f'figures/detection_revised.{ext}',dpi=300)
    meta=dict(script='analysis/v6_simulation/detection_revised.py',git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
              source_sha256=hashlib.sha256(Path(__file__).read_text(encoding='utf8').encode()).hexdigest(),
              source_hash_format='UTF-8 normalized LF',evidence_type='analytic approximation with scenario classifier; repository-reported pilot anchors',
              python=sys.version,numpy=np.__version__,matplotlib=matplotlib.__version__,
              p0_sources=[dict(version=version,p0=p0,source=source) for version,p0,source in sources],main_reference='DeepSeek v2',
              topic_rate_sources='RecIF median 1.6%, p90 3.6%; Xu task R4 / v5 section 4',
              classifier_cases=classifiers,classifier_status='five assumed cases plus measured Qwen-vs-DeepSeek v2 cross-check; not gold-standard accuracy',
              v2_cross_check=v2,input_script='analysis/v6_simulation/v2_detection_inputs.py',
              input_script_sha256=hashlib.sha256((BASE/'v2_detection_inputs.py').read_text(encoding='utf8').encode()).hexdigest(),
              odds_range=[2,8],points=61,significance=.05,power=.8,n0_equals_n=True,
              seeds=[],interval='none: deterministic calculation',count_unit='n per arm; both_arms_total explicitly doubles total_per_arm',
              limitations=['independent observations','normal approximation','known classifier rates','no sequential testing','no elapsed-time claim',
                           'pilot prevalence is not supply','not all four pilot prevalences have identical narrative definitions'])
    for folder in ('results','figures'):
        (BASE/folder/'detection_revised.meta.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
    assert len(rows)==5*6*61*2
    for version,p0,_ in sources:
        r=next(r for r in rows if r['version']==version and r['odds']==2 and r['classifier']=='assumed' and r['topic_rate']==.016)
        print(f'R4 {version} p0={p0:.1%}: n={r["n_per_arm"]} per arm; exposures={r["total_per_arm"]} per arm')
    r=next(r for r in rows if r['version']=='DeepSeek v2' and r['classifier']=='Qwen_vs_DeepSeek_v2' and r['odds']==2 and r['topic_rate']==.016)
    print(f'R4 v2 Qwen-classifier plug-in: n={r["n_per_arm"]}; exposures={r["total_per_arm"]} per arm.')
    print('PASS R4: 3660 analytic settings; decreasing sample requirements; odds conversion; task-specific provenance.')


if __name__=='__main__': run()
