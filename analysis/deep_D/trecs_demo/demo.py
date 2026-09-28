import time, numpy as np, trecs
from trecs.models import ContentFiltering, PopularityRecommender, RandomRecommender, ImplicitMF
from trecs.components import Users, Items
from trecs.metrics import InteractionSimilarity, InteractionSpread, MSEMeasurement, InteractionMeasurement, RecSimilarity, AverageFeatureScoreRange
print("trecs", trecs.__version__ if hasattr(trecs,'__version__') else '0.2.1')
rng=np.random.default_rng(0)
U,I,K=100,500,20
# uneven user prefs (Chaney-like), sparse item attrs
mu_u=10*rng.dirichlet(np.ones(K)); user_prof=rng.dirichlet(mu_u,size=U)
item_attr=rng.dirichlet(0.1*np.ones(K)*1.0+0.0,size=I).T  # K x I
pairs=[(u,(u+1)%U) for u in range(U)]
def cos_user_mean(P):
    P=P/np.linalg.norm(P,axis=1,keepdims=True); S=P@P.T; return (S.sum()-U)/(U*(U-1))
res={}
for name,cls in [("content",ContentFiltering),("popularity",PopularityRecommender),("random",RandomRecommender),("mf",ImplicitMF)]:
    users=Users(actual_user_profiles=user_prof.copy(),drift=0.05,attention_exp=-0.8,repeat_interactions=False,seed=1)
    kw=dict(actual_user_representation=users,actual_item_representation=item_attr.copy(),num_items_per_iter=10,seed=1)
    if name=="content": kw["item_representation"]=item_attr.copy()
    if name=="mf": kw["num_latent_factors"]=K
    rs=cls(num_users=U,num_items=I,**kw) if name!="content" else cls(**kw)
    rs.add_metrics(InteractionSimilarity(pairs),InteractionSpread(),MSEMeasurement(),RecSimilarity(pairs))
    t=time.time()
    before=cos_user_mean(rs.users.actual_user_profiles.value)
    rs.startup_and_train(timesteps=10)
    rs.run(timesteps=50,train_between_steps=True,repeated_items=False)
    dt=time.time()-t
    m=rs.get_measurements()
    after=cos_user_mean(rs.users.actual_user_profiles.value)
    js=[x for x in m["interaction_similarity"] if x is not None]
    print(f"{name:10s} time={dt:5.2f}s steps={len(m['timesteps'])} Jaccard(last)={js[-1]:.4f} RecSim(last)={m['rec_similarity'][-1]:.3f} MSE(last)={m['mse'][-1]:.4f} usercos before={before:.3f} after={after:.3f}")
print(list(m.keys()))
