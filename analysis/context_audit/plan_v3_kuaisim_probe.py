"""Run unmodified KuaiSim response network on synthetic tensors on CPU.

This is an interface/numerical smoke check, NOT trained user simulation.
Also documents the probability contract in one inspected environment path.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import torch

root = Path(sys.argv[1]).resolve()
source = root/'code/KuaiSim'
sys.path.insert(0, str(source/'code'))
from model.simulator.KRMBUserResponse import KRMBUserResponse

torch.manual_seed(1110)
torch.set_num_threads(2)
args = KRMBUserResponse.parse_model_args(argparse.ArgumentParser()).parse_args([])
stats = {'n_user': 3, 'n_item': 8, 'max_seq_len': 4,
         'user_feature_dims': {}, 'item_feature_dims': {},
         'feedback_type': ['is_like','is_hate'], 'feedback_size': 2}
model = KRMBUserResponse(args, stats, torch.device('cpu')).to(torch.device('cpu')).eval()
batch = {'user_id':torch.tensor([1,2]),'item_id':torch.tensor([3,4]),
         'history':torch.tensor([[1,2,3,4],[2,4,6,8]]),
         'history_is_like':torch.tensor([[0.,1,0,1],[1.,0,1,0]]),
         'history_is_hate':torch.zeros(2,4)}
out = model(batch)
loss = torch.nn.functional.binary_cross_entropy_with_logits(out['preds'],torch.zeros_like(out['preds']))
loss.backward()
base = (source/'code/model/general.py').read_text()
env = (source/'code/env/KREnvironment_WholeSession_GPU.py').read_text()
result = {
    'scope':'Untrained network; synthetic input; no simulator fidelity or policy-effect result',
    'commit':subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip(),
    'torch':torch.__version__, 'device':'cpu',
    'prediction_shape':list(out['preds'].shape), 'state_shape':list(out['state'].shape),
    'finite_forward':bool(torch.isfinite(out['preds']).all()),
    'finite_backward':all(bool(torch.isfinite(p.grad).all()) for p in model.parameters() if p.grad is not None),
    'base_probability_is_sigmoid_logits':bool(torch.allclose(out['probs'],out['preds'].sigmoid())),
    'source_contract_checks':{
        'base_adds_sigmoid':'out_dict["probs"] = nn.Sigmoid()(out_dict["preds"])' in base,
        'env_reads_probs':"behavior_scores = out_dict['probs']" in env,
        'env_applies_sigmoid_again':'point_scores = torch.sigmoid(behavior_scores)' in env},
    'probability_contract_example':{'logit':0.,'base_probability':0.5,'env_before_diversity_penalty':float(torch.tensor(0.5).sigmoid())},
    'interpretation':'For this BaseModel + environment path probabilities are sigmoid-transformed twice before diversity penalty. Audit/adapt before reuse; do not generalize to every KuaiSim environment or original reported experiment.'
}
Path('docs/context-recovery/plan_v3_kuaisim_probe.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
