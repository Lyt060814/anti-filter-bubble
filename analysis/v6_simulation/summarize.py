"""Seed-level means and pointwise 95% Monte Carlo intervals for every setting."""
from collections import defaultdict
from audit import read
from experiments import *


def summarize():
    parameters = [dict(parameter=k, value=str(v), evidence_type='scenario assumption',source='model.Config') for k,v in vars(Config()).items()]
    for k,v in dict(ratios=RATIOS,theta_scan=THETAS,seeds=SEEDS,T=T,active=ACTIVE,followup=FOLLOW,
                    catalogue='40 A / 40 B / 320 outside', nuisance='paired A/B; Gaussian 2 coordinates',
                    p0=[.018,.41],topic_rate=[.016,.036],recall=.8,false_positive_rate=.02).items():
        evidence = 'repository-reported pilot anchor' if k in ('p0','topic_rate') else 'scenario assumption'
        parameters.append(dict(parameter=k,value=str(v),evidence_type=evidence,source='Xu task R4 / v5 sections 4,7' if k in ('p0','topic_rate') else 'experiments.py'))
    save_csv('parameters',parameters)
    metadata('parameters',dict(script='analysis/v6_simulation/summarize.py',table='report/sections/5_case_study.md parameter table'))
    for source, keys, fields, end in [
        ('formation',['ratio','theta','decay','outside_topics'],['m','V','total_bias','platform_bias'],T),
        ('escape',['ratio','theta','strategy'],['delta_V','delta_log_m','B_retention','effort','delta_V_vs_control'],ACTIVE)]:
        groups = defaultdict(list)
        for row in read(source):
            if int(row['step'])==end:
                groups[tuple(row[k] for k in keys)].append(row)
        output = []
        for key, group in groups.items():
            row = dict(zip(keys,key))
            row['n_seeds'] = len(group)
            assert len(group)==20
            for field in fields:
                vals = np.array([float(r[field]) for r in group])
                if np.isfinite(vals).all():
                    mean, half = ci(vals)
                    row[field+'_mean'], row[field+'_lower'], row[field+'_upper'] = mean,mean-half,mean+half
                else:
                    row[field+'_mean'], row[field+'_lower'], row[field+'_upper'] = np.nan,np.nan,np.nan
            output.append(row)
        save_csv(source+'_summary',output)
        print(source)
        for r in output:
            if float(r['ratio']) in (.15,.59) and float(r['theta'])==2:
                if source=='formation' and (float(r['decay'])!=.002 or r['outside_topics']!='4'):
                    continue
                print(r)


if __name__ == '__main__':
    summarize()
