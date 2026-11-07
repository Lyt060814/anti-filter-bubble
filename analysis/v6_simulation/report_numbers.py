"""Print selected actual results for report writing; all full grids remain in CSV."""
from calibrated_audit import rows
import numpy as np


def main():
    print('Formation: family group, prior=.15, supply=.02, step=6000')
    for r in rows('calibrated_formation_summary.csv'):
        if r['family']=='group' and r['scan']=='main_grid' and float(r['prior'])==.15 and float(r['supply'])==.02 and int(r['step'])==6000:
            if float(r['theta'])==2 or (float(r['theta'])==0 and float(r['ratio'])>1):
                print({k:r[k] for k in ('ratio','theta','m','m_ci','V','V_ci')})
    print('Strategies: fitted group ratio, prior=.15, supply=.02, theta=2, active endpoint')
    for r in rows('calibrated_escape_summary.csv'):
        if int(r['case'])==27 and float(r['theta'])==2 and int(r['step'])==1000:
            print({k:r[k] for k in ('strategy','delta_V','delta_V_ci','delta_log_m','delta_log_m_ci','B_retention','effort')})
    print('Supplementary NI calibration target .78, group, theta=2, active endpoint')
    for arm in ('S0','S1a','S1b_calibrated'):
        group=[r for r in rows('ni_calibrated_sensitivity.csv') if r['family']=='group' and float(r['relative_response_target'])==.78 and float(r['theta'])==2 and int(r['step'])==1000 and r['strategy']==arm]
        a=np.array([float(r['delta_V']) for r in group]);half=2.093*a.std(ddof=1)/np.sqrt(20)
        print(arm,a.mean(),half)


if __name__=='__main__': main()
