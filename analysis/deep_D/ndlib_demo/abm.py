import time, numpy as np, networkx as nx, random
import ndlib.models.ModelConfig as mc
import ndlib.models.opinions as op
def eff_clusters(x, tol=0.02):
    x=np.sort(np.array(x)); groups=[[x[0]]]
    for v in x[1:]:
        (groups[-1].append(v) if v-groups[-1][-1]<tol else groups.append([v]))
    s=np.array([len(g) for g in groups])/len(x); return 1/np.sum(s**2)
N=200; g=nx.complete_graph(N)
for eps in [0.32]:
  for gamma in [0.0,1.0,1.6]:
    Cs=[];t=time.time()
    for seed in range(3):
        np.random.seed(seed); random.seed(seed)
        m=op.AlgorithmicBiasModel(g,seed=seed); c=mc.Configuration()
        c.add_model_parameter("epsilon",eps); c.add_model_parameter("gamma",gamma); m.set_initial_status(c)
        its=m.iteration_bunch(200,node_status=True,progress_bar=False)
        Cs.append(eff_clusters(list(m.status.values())))
    print(f"eps={eps} gamma={gamma} effective clusters after 200 iters (mean of 3 seeds)={np.mean(Cs):.2f} {np.round(Cs,2)} time={time.time()-t:.1f}s")
