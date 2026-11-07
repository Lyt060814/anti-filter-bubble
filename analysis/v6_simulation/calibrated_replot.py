"""Redraw reviewed figures from stored numeric results, preserving run provenance."""
from calibrated_run import plots
from calibrated_audit import rows,BASE
import json


def numeric(filename):
    records=list(rows(filename))
    for r in records:
        for key,value in r.items():
            try:r[key]=float(value)
            except ValueError:pass
    return records


if __name__=='__main__':
    details=json.loads((BASE/'figures/formation_calibrated.meta.json').read_text())
    details['simulation_code_commit']=details.get('simulation_code_commit',details['git_commit'])
    details['simulation_source_sha256']=details.get('simulation_source_sha256',details['source_sha256'])
    for key in ('git_commit','python','numpy','source_sha256','source_hash_format'):details.pop(key,None)
    plots(numeric('calibrated_formation_summary.csv'),numeric('calibrated_escape_summary.csv'),details)
