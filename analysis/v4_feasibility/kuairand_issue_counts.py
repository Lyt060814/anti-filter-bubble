"""KuaiRand-1K: keyword candidate videos per issue, their impressions and is_hate events. Usage: python -I kuairand_issue_counts.py CAPTIONS_CSV LOG_DIR"""
import sys, random, collections
import pandas as pd
cap_path, log_dir = sys.argv[1], sys.argv[2]
claims = {
 "marriage_gender": ["离婚","婆媳","婆婆","女方","男方","家暴","出轨","AA制","彩礼"],
 "parenting_any": ["孩子","育儿","家长","宝宝"],
 "strict_only(her kw)": ["管教","棍棒","严父","不打不成器"],
 "must_jiwa(her kw)": ["鸡娃","补习","起跑线","双减"],
 "bride_price(her kw)": ["彩礼","天价彩礼","嫁妆","返还彩礼"],
 "discipline(broad)": ["管教","棍棒","严父","不打不成器","打孩子","惩罚孩子","教育孩子","虎妈","狼爸","管孩子"],
}
logs = [f"{log_dir}/log_standard_4_08_to_4_21_1k.csv", f"{log_dir}/log_standard_4_22_to_5_08_1k.csv"]
vid_in_logs = collections.Counter(); hate = collections.Counter(); users = collections.defaultdict(set)
for lp in logs:
    for ch in pd.read_csv(lp, usecols=["user_id","video_id","is_hate"], chunksize=2_000_000):
        vc = ch["video_id"].value_counts()
        vid_in_logs.update(vc.to_dict())
        h = ch[ch["is_hate"]==1]["video_id"].value_counts(); hate.update(h.to_dict())
print("log videos", len(vid_in_logs), "log rows", sum(vid_in_logs.values()))
matches = {c: {} for c in claims}
for ch in pd.read_csv(cap_path, usecols=["final_video_id","caption","show_cover_text"], chunksize=500_000, dtype=str):
    ch = ch.fillna("")
    ch["vid"] = pd.to_numeric(ch["final_video_id"], errors="coerce")
    ch = ch[ch["vid"].isin(vid_in_logs.keys())]
    text = ch["caption"] + " " + ch["show_cover_text"]
    for c, kws in claims.items():
        m = text.str.contains("|".join(kws), regex=True)
        for v, t in zip(ch.loc[m, "vid"], text[m]):
            matches[c][int(v)] = t
random.seed(0)
for c, d in matches.items():
    ev = [vid_in_logs[v] for v in d]
    print(f"\n== {c}: videos={len(d)} impressions={sum(ev)} hate={sum(hate[v] for v in d)}")
    print("   videos with >=10 / >=50 / >=200 impressions:", sum(e>=10 for e in ev), sum(e>=50 for e in ev), sum(e>=200 for e in ev))
    for v in random.sample(sorted(d), min(10, len(d))):
        print("   -", vid_in_logs[v], d[v][:70].replace("\n"," "))
