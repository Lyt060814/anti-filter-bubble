"""Estimate how often candidate everyday issues appear in ShortVideo ASR, and print random snippets.

Usage: python -I issue_prevalence.py ASR_DIR INDEX_FILE [GROUP SAMPLE_N SEED]
Counts are keyword hits (not relevance or stance); snippets support manual pilot judgement.
"""
import math
import os
import random
import sys

GROUPS = {
    "bride_price": ["彩礼"],
    "discipline": ["打孩子", "管教", "棍棒", "严厉", "正面管教", "惩罚孩子", "骂孩子"],
    "childbearing": ["生孩子", "丁克", "不生", "二胎", "三胎", "催生", "生育"],
    "marriage_pressure": ["催婚", "不结婚", "剩女", "大龄单身"],
    "housework_roles": ["全职太太", "全职妈妈", "家庭主妇", "做家务", "AA制"],
    "in_laws": ["婆媳", "婆婆"],
    "career_choice": ["考公", "公务员", "铁饭碗", "躺平", "读书无用", "学历"],
    "education_anxiety": ["鸡娃", "补习", "内卷", "起跑线", "双减", "辅导作业"],
}

def load(asr_dir):
    texts = {}
    for name in os.listdir(asr_dir):
        if not name.endswith(".txt"):
            continue
        with open(os.path.join(asr_dir, name), encoding="utf-8", errors="ignore") as f:
            text = f.read()
        if text.lstrip().startswith("<"):
            continue
        texts[name[:-4]] = text
    return texts

def main():
    asr_dir, index_file = sys.argv[1], sys.argv[2]
    total = sum(1 for _ in open(index_file))
    texts = load(asr_dir)
    n = len(texts)
    print(f"ASR files read: {n} of {total} listed")
    for group, keywords in GROUPS.items():
        hits = [pid for pid, t in texts.items() if any(k in t for k in keywords)]
        p = len(hits) / n
        se = math.sqrt(p * (1 - p) / n)
        print(f"{group:18s} {len(hits):5d}  {p:6.2%}  est. {p*total:7,.0f}  (95% CI {max(0,p-1.96*se)*total:,.0f}-{(p+1.96*se)*total:,.0f})")
    if len(sys.argv) > 3:
        group, k, seed = sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
        keywords = GROUPS[group]
        hits = sorted(pid for pid, t in texts.items() if any(kw in t for kw in keywords))
        random.Random(seed).shuffle(hits)
        for pid in hits[:k]:
            t = texts[pid].replace("\n", " ")
            kw = next(x for x in keywords if x in t)
            i = t.find(kw)
            print(f"\n[{pid}] len={len(t)} | {t[max(0, i-110): i+110]}")

if __name__ == "__main__":
    main()
