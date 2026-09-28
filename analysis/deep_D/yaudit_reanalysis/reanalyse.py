import pandas as pd, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
D='/home/user/kinit-sk/yaudit-recsys-2021/Data/'; OUT='yaudit_reanalysis/'
r=pd.read_csv(D+'raw_data/recommendations.csv',index_col=0)
top=r[(r.position<=10)]
lab=top[top.normalized_annotation.notna()]
# per list (bot, watched video) mean normalized score = paper's "normalized score"
lists=lab.groupby(['topic','bot_id','seed_sequence']).agg(score=('normalized_annotation','mean'),
      prom=('normalized_annotation',lambda x:(x==1).mean()),deb=('normalized_annotation',lambda x:(x==-1).mean()),n=('normalized_annotation','size')).reset_index()
cov=top.groupby(['topic','seed_sequence']).normalized_annotation.apply(lambda x:x.notna().mean()).rename('coverage')
curve=lists.groupby(['topic','seed_sequence']).agg(score=('score','mean'),prom=('prom','mean'),deb=('deb','mean'),nlists=('score','size')).join(cov).reset_index()
curve.to_csv(OUT+'rec_top10_curve_manual_labels.csv',index=False)
# S1/E1/E2 : paper uses first 2 seed videos, last 2 of each phase -> seq {1,2},{39,40},{79,80}
ph={'S1':[1,2],'E1':[39,40],'E2':[79,80]}
rows=[]
for t,g in lists.groupby('topic'):
    d={k:g[g.seed_sequence.isin(v)].score for k,v in ph.items()}
    row={'topic':t,**{k:round(v.mean(),2) for k,v in d.items()}}
    for a,b in [('S1','E1'),('E1','E2'),('S1','E2')]:
        row[f'p_{a}{b}']=float('%.2g'%mannwhitneyu(d[a],d[b]).pvalue)
    row.update({f'prom%_{k}':round(100*g[g.seed_sequence.isin(v)].prom.mean(),1) for k,v in ph.items()})
    rows.append(row)
tab=pd.DataFrame(rows); print(tab.to_string(index=False)); tab.to_csv(OUT+'S1_E1_E2_table.csv',index=False)
# summary numbers: slope in phase 1 vs mean jump at 40->41
for t,g in curve.groupby('topic'):
    g=g.set_index('seed_sequence')
    p1=g.loc[1:40,'score'].dropna(); p2=g.loc[41:80,'score'].dropna()
    s1=np.polyfit(p1.index,p1.values,1)[0] if len(p1)>3 else np.nan
    pre=g.loc[36:40,'score'].mean(); post=g.loc[41:45,'score'].mean()
    print(f"{t:12s} phase1 slope/video={s1:+.4f}  mean(36-40)={pre:+.2f} mean(41-45)={post:+.2f} jump={post-pre:+.2f}  mean coverage={g.coverage.mean():.2f}")
# predicted grouped (authors' manual+ML labels) for comparison
p=pd.read_csv(D+'predicted_data/recommendations_with_predicted_grouped.csv',index_col=0)
hp=pd.read_csv(D+'predicted_data/home_page_with_predicted_grouped.csv',index_col=0)
topics=['911','chemtrails','flatearth','moonlanding','vaccines']
fig,axes=plt.subplots(1,5,figsize=(17,3.6),sharey=True)
for ax,t in zip(axes,topics):
    c=curve[curve.topic==t]; pp=p[p.topic==t]
    ax.axvspan(40.5,80.5,color='#eeeeea',lw=0); ax.axhline(0,color='#bbbbbb',lw=0.8)
    ax.plot(c.seed_sequence,c.score.rolling(3,center=True,min_periods=1).mean(),color='#2a78d6',lw=2,label='top-10 recs, manual labels only (3-pt avg)')
    ax.plot(pp.seed_sequence,pp.score,color='#eb6834',lw=2,label="top-10 recs, authors' manual+ML file")
    ax.set_title(t,fontsize=11); ax.set_xlabel('watched video # (1-40 promoting, 41-80 debunking)',fontsize=8)
    for s in ['top','right']: ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=8)
axes[0].set_ylabel('mean normalized score\n(+1 promoting, -1 debunking)',fontsize=9)
axes[0].legend(fontsize=7,loc='lower left',frameon=False)
fig.suptitle('YouTube misinformation bubble: fall-in (videos 1-40) and bursting (41-80). Re-plot of Srba et al. 2023 data',fontsize=11)
fig.tight_layout(); fig.savefig(OUT+'bubble_curves.png',dpi=130)
print('saved')
