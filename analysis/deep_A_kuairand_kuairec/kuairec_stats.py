import pandas as pd, numpy as np, ast
S="/home/user/data/kuairec/KuaiRec 2.0/data/"
for name in ['small_matrix.csv','big_matrix.csv']:
    d=pd.read_csv(S+name,usecols=['user_id','video_id','play_duration','video_duration','timestamp','date','watch_ratio'])
    nu,ni=d.user_id.nunique(),d.video_id.nunique()
    print(name,'rows',len(d),'users',nu,'videos',ni,'density %.4f'%(len(d)/nu/ni),'dup pairs',int(d.duplicated(['user_id','video_id']).sum()))
    w=d.watch_ratio; print('  watch_ratio: mean %.3f median %.3f p90 %.3f p99 %.2f max %.1f; share>=2: %.3f; share>=1: %.3f; share>5: %.4f'%(w.mean(),w.median(),w.quantile(.9),w.quantile(.99),w.max(),(w>=2).mean(),(w>=1).mean(),(w>5).mean()))
    print('  NaN timestamp rows',int(d.timestamp.isna().sum()),'date range',d.date.min(),d.date.max(),'video_duration==0',int((d.video_duration==0).sum()))
c=pd.read_csv(S+'item_categories.csv'); c['f']=c.feat.apply(ast.literal_eval)
print('item_categories: videos',len(c),'distinct cats',len(set(x for l in c.f for x in l)),'tags/video',c.f.str.len().value_counts().to_dict())
cc=pd.read_csv(S+'kuairec_caption_category.csv',nrows=3, engine='python', on_bad_lines='skip'); print('caption_category cols',list(cc.columns))
