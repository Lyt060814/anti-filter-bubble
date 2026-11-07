"""Instantaneous filter sensitivity at saved formation endpoints, NOT a dynamic rerun."""
from pathlib import Path
import argparse,csv,gzip,json,hashlib,subprocess
import numpy as np
BASE=Path(__file__).parent


def run(results,v2json):
    rates=json.loads(v2json.read_text())
    output=BASE/'results/filter_v2_instant.csv.gz'
    output.parent.mkdir(exist_ok=True)
    selected=[];count=0;input_hashes={}
    with gzip.open(output,'wt',encoding='utf8',newline='') as f:
        fields=['case','family','supply','prior','theta','seed','classifier','recall','false_positive_rate','delta_V_direct','delta_log_m_direct','B_retention_direct']
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        for family in ('group','conflict'):
            source=results/f'calibrated_formation_{family}.csv.gz'
            input_hashes[source.name]=hashlib.sha256(source.read_bytes()).hexdigest()
            with gzip.open(source,'rt',encoding='utf8',newline='') as sourcefile:
                for r in csv.DictReader(sourcefile):
                    if int(r['step'])!=6000:continue
                    s=float(r['supply']);m=float(r['m']);v=float(r['V_supply'])
                    odds=s/(1-s)*np.exp(v);p=odds/(1+odds)
                    for name,alpha,beta in (('assumed',.8,.02),('Qwen_vs_DeepSeek_v2',rates['recall'],rates['false_positive_rate'])):
                        loss=m*(p*alpha+(1-p)*beta)
                        after_m=(m-loss)/(1-loss)
                        row={key:r[key] for key in ('case','family','supply','prior','theta','seed')}
                        row.update(classifier=name,recall=alpha,false_positive_rate=beta,
                                   delta_V_direct=np.log((1-alpha)/(1-beta)),delta_log_m_direct=np.log(after_m/m),
                                   B_retention_direct=(1-beta)/(1-loss))
                        writer.writerow(row);count+=1
                        if int(r['case'])==27 and float(r['theta'])==2:selected.append(row)
    assert count==41920
    meta=dict(evidence_type='analytic one-step output filtering on synthetic formation states; measured cross-model rates are plug-in inputs',
              script='analysis/v6_simulation/filter_v2_instant.py',git_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
              source_sha256=hashlib.sha256(Path(__file__).read_text(encoding='utf8').encode()).hexdigest(),
              source_files=input_hashes,v2_input_sha256=hashlib.sha256(v2json.read_bytes()).hexdigest(),
              model_reference='supply total skew',seeds=list(range(20)),rows=count,
              compression='gzip CSV',caveat='Instantaneous renormalized thinning, not the 1000-exposure S6 endpoint; classifier uncertainty not propagated.',
              rates=rates)
    output.with_name('filter_v2_instant.meta.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
    for classifier in ('assumed','Qwen_vs_DeepSeek_v2'):
        group=[r for r in selected if r['classifier']==classifier]
        print(classifier,'direct dV=',group[0]['delta_V_direct'],'mean direct dlogm=',np.mean([r['delta_log_m_direct'] for r in group]))
    print('PASS filter sensitivity: all 262 x 4 theta x 20 seed endpoints x 2 classifier cases = 41920 records.')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--results',type=Path,default=BASE/'results')
    parser.add_argument('--v2-json',type=Path,default=BASE/'results/v2_detection_inputs.json')
    args=parser.parse_args();run(args.results,args.v2_json)
