"""Aggregate v2 model cross-check, matching agreement.py's complete-case rule.

No descriptions/reasons or per-video outputs are copied to this directory.
"""
from pathlib import Path
import csv,json,hashlib
BASE=Path(__file__).parent


def load():
    source=BASE.parent/'v6/results/dual_v2_labels.csv'
    with source.open(encoding='utf8',newline='') as f:data=list(csv.DictReader(f))
    pos={'针对女性','针对男性'}
    parsed=lambda r,m:r.get(m+'_issue','') not in ('','缺失')
    reference=[r for r in data if parsed(r,'deepseek')]
    both=[r for r in reference if parsed(r,'qwen')]
    tp=sum(r['qwen_group_label'] in pos and r['deepseek_group_label'] in pos for r in both)
    fp=sum(r['qwen_group_label'] in pos and r['deepseek_group_label'] not in pos for r in both)
    fn=sum(r['qwen_group_label'] not in pos and r['deepseek_group_label'] in pos for r in both)
    tn=sum(r['qwen_group_label'] not in pos and r['deepseek_group_label'] not in pos for r in both)
    positive=sum(r['deepseek_group_label'] in pos for r in reference)
    out=dict(source='analysis/v6/results/dual_v2_labels.csv',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             reference='DeepSeek v2, not human gold standard',total_rows=len(data),reference_parsed=len(reference),
             reference_positive=positive,p0=positive/len(reference),paired_parsed=len(both),
             qwen_missing=len(reference)-len(both),tp=tp,fp=fp,fn=fn,tn=tn,
             recall=tp/(tp+fn),false_positive_rate=fp/(fp+tn),
             caveat='Small reference-positive count; model agreement rates, not gold-standard accuracy; plug-in uncertainty not propagated.')
    return out


if __name__=='__main__':
    out=load();(BASE/'results').mkdir(exist_ok=True)
    (BASE/'results/v2_detection_inputs.json').write_text(json.dumps(out,indent=2),encoding='utf8')
    print(json.dumps(out,indent=2))
