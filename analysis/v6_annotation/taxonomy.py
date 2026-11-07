"""D4 taxonomy table from the bottom-up sample (Zhao Dingcheng).

Usage: python -I -X utf8 taxonomy.py LABELS_CSV SOURCE_NAME [COMPARE_CSV COMPARE_NAME]
  e.g. python -I -X utf8 taxonomy.py ../v6/results/bottomup_ds_labels.csv deepseek_bu ../v6/results/bottom_up_labels.csv qwen_v0
Rows with an empty domain (invalid model output) are counted as missing and left out of every share.
With COMPARE_CSV, the table adds the other model's share and opposing share for each domain (same impressions).
Sub-issues are listed only for domains with at least MIN_SUB impressions.
Input columns: pid, domain, issue, opposing, narrative_type (as written by analysis/v6/bottom_up_sample.py).
The sample is impressions drawn uniformly from user histories, so shares are shares of exposures.

The LLM writes `issue` as free text (most strings occur once), so sub-issues are formed by the keyword
rules in SUBISSUES below, applied in order; strings matching none go to "other". This only groups the
LLM's own issue labels; no video is labelled by hand.

Writes to results/: taxonomy_<src>.csv (per domain), taxonomy_<src>_subissues.csv, taxonomy_<src>_table.md,
taxonomy_<src>.meta.json.
"""
import json
import os
import re
import subprocess
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TYPES = ["唯一正确", "二元对立", "焦虑渲染", "群体标签"]
TYPE_EN = {"唯一正确": "only-right-way", "二元对立": "binary opposition", "焦虑渲染": "anxiety-raising", "群体标签": "group label"}
DOMAIN_EN = {"性别与婚恋": "Gender and relationships", "身体与外貌": "Body and appearance", "家庭与代际": "Family and generations",
             "人生选择与出路": "Life choices and paths", "消费与经济": "Consumption and money", "文化与价值观": "Culture and values",
             "学术与思想": "Study and ideas", "公共秩序与自由": "Public order and freedom", "资源与公平": "Resources and fairness",
             "其他社会议题": "Other social issues", "非议题内容": "Non-issue content"}
IN_SCOPE = ["性别与婚恋", "身体与外貌", "家庭与代际", "人生选择与出路", "消费与经济"]
# (English name, regex over the LLM's issue string), first match wins within a domain.
SUBISSUES = {
    "性别与婚恋": [("money and bride price", r"经济|金钱|彩礼"), ("pregnancy and childbearing", r"怀孕|生育|代孕|月经"),
               ("gender roles and expectations", r"男女|女性|男性|女强|性别|第六感|大叔"),
               ("marriage and spouses", r"婚|夫妻|伴娘|忠诚"), ("dating, break-ups and feelings", r"情|恋|爱|分手|表白|情侣|追求|失联|闺蜜")],
    "身体与外貌": [("appearance anxiety", r"容貌|审美|身高|脱发|痘|外貌|颜|美丽|身材|形象|穿衣")],
    "家庭与代际": [("in-laws and marrying into a family", r"婆媳|远嫁|媳妇|婚事|继母|重组|复婚|护嫂"),
               ("elder care", r"养老|老人|代际|三代"),
               ("family conflict and violence", r"暴力|纠纷|抚养权|房屋|财务|经济|冲突|矛盾"),
               ("parenting and parent-child relations", r"亲子|父|母|育儿|子女|儿童|管教|厌学|教育|孝|兄|姐|妹")],
    "人生选择与出路": [("exams and study paths", r"考研|考公|学业|退学|留级|住校"),
                 ("jobs and careers", r"职业|职场|求职|工作|暑假工|退伍|练习生"),
                 ("striving, lying flat and life direction", r"奋斗|躺平|人生|选择|独立|迷茫|梦想|成长|底层")],
    "消费与经济": [("promotions and marketing", r"优惠|促销|赚钱游戏|游戏赚钱|抽奖|红包|营销|带货|福利|新人|新用户|0元|免费|推荐|赚取"),
               ("spending values and personal finance", r"消费|性价比|平价|穿搭|理财|财务|借贷|债务|收入|诱惑"),
               ("prices and housing", r"房|价")],
    "文化与价值观": [("history and national memory", r"历史|抗日|国耻|革命|爱国|民族|英雄|军人|国家|战争|红歌"),
                ("images of women and men", r"女性|男性|婚|爱情|恋|同性"), ("appearance and aesthetics", r"容貌|审美|着装|美学"),
                ("tradition and heritage", r"传统|非遗|节气|方言|习俗")],
    "学术与思想": [("exam and study pressure", r"学业|考|压力|分数|学习")],
    "公共秩序与自由": [("policing and law enforcement", r"执法|警察|酒驾|卧底|防卫|监管"),
                 ("safety and surveillance", r"安全|偷拍|避险|救援|人贩子|监控")],
    "其他社会议题": [("history and war", r"历史|731|战争"), ("crime and public safety", r"案|欺凌|安全|骗|调查|黑帮|求助"),
               ("health", r"健康|医|病|器官|心理|骨肉瘤")],
}
MARKETING = "promotions and marketing"
MIN_SUB = 30


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(max(0.0, c - h), 4), round(min(1.0, c + h), 4))


def subissue(domain, issue):
    for name, pat in SUBISSUES.get(domain, []):
        if re.search(pat, issue):
            return name
    return "other"


def load(path):
    d = pd.read_csv(path, dtype=str, keep_default_na=False)
    missing = int((d.domain == "").sum())
    return d[d.domain != ""].reset_index(drop=True), missing


def main(path, src, cmp_path=None, cmp_name=None):
    d, n_missing = load(path)
    n = len(d)
    cmp = None
    if cmp_path:
        c, c_missing = load(cmp_path)
        c = c[c.pid.isin(set(d.pid))]
        cmp = {"n": len(c), "missing": c_missing,
               "by_domain": {dom: (len(g), int(g.opposing.eq("是").sum())) for dom, g in c.groupby("domain")}}
    d["sub"] = [subissue(a, b) for a, b in zip(d.domain, d.issue)]
    d["opp"] = d.opposing.eq("是")
    rows, subs = [], []
    for dom, g in d.groupby("domain"):
        k = int(g.opp.sum())
        types = g[g.opp].narrative_type.value_counts()
        rows.append({"domain": dom, "domain_en": DOMAIN_EN.get(dom, dom), "in_scope": dom in IN_SCOPE, "n": len(g),
                     "share": round(len(g) / n, 4), "share_ci": wilson(len(g), n), "opposing_n": k,
                     "opposing_share": round(k / len(g), 4), "opposing_ci": wilson(k, len(g)),
                     **{f"type_{TYPE_EN[t].replace(' ', '_').replace('-', '_')}": int(types.get(t, 0)) for t in TYPES},
                     "type_none_but_opposing": int(types.get("无", 0))})
        if cmp:
            cn, ck = cmp["by_domain"].get(dom, (0, 0))
            rows[-1].update({f"{cmp_name}_n": cn, f"{cmp_name}_share": round(cn / cmp["n"], 4),
                             f"{cmp_name}_opposing_share": round(ck / cn, 4) if cn else None})
        if dom == "非议题内容":
            continue
        for s, h in g.groupby("sub"):
            subs.append({"domain": dom, "subissue": s, "n": len(h), "opposing_n": int(h.opp.sum()),
                         "anxiety_raising_n": int((h.opp & h.narrative_type.eq("焦虑渲染")).sum()),
                         "top_issue_strings": "、".join(h.issue.value_counts().index[:5])})
    tab = pd.DataFrame(rows).sort_values("n", ascending=False)
    sub = pd.DataFrame(subs).sort_values(["domain", "n"], ascending=[True, False])
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    stem = os.path.join(HERE, "results", f"taxonomy_{src}")
    tab.to_csv(stem + ".csv", index=False, encoding="utf-8")
    sub.to_csv(stem + "_subissues.csv", index=False, encoding="utf-8")
    head = "| Domain | Share of exposures | Opposing narrative (within domain) | Narrative types (count) | Largest sub-issues (n) |"
    rule = "|---|---:|---:|---|---|"
    if cmp:
        head += f" {cmp_name.split('_')[0].capitalize()} on the same impressions: share; opposing |"
        rule += "---:|"
    md = [head, rule]
    for _, r in tab.iterrows():
        if r.domain == "非议题内容":
            line = f"| {r.domain_en} | {r.share:.1%} | — | — | — |"
            if cmp:
                line += f" {r[f'{cmp_name}_share']:.1%}; — |"
            md.append(line)
            continue
        tc = sorted(((r[f"type_{TYPE_EN[t].replace(' ', '_').replace('-', '_')}"], TYPE_EN[t]) for t in TYPES), reverse=True)
        tcs = ", ".join(f"{name} ({c})" for c, name in tc if c > 0)
        ss = sub[(sub.domain == r.domain) & (sub.subissue != "other")].head(3)
        sss = ("; ".join(f"{a} ({b})" for a, b in zip(ss.subissue, ss.n)) or "—") if r.n >= MIN_SUB else "(too few to split)"
        star = " *" if r.in_scope else ""
        line = f"| {r.domain_en}{star} | {r.share:.1%} | {r.opposing_n}/{r.n} ({r.opposing_ci[0]:.0%}–{r.opposing_ci[1]:.0%}) | {tcs or '—'} | {sss} |"
        if cmp:
            cs, co = r[f"{cmp_name}_share"], r[f"{cmp_name}_opposing_share"]
            line += f" {cs:.1%}; {'—' if co is None else format(co, '.0%')} |"
        md.append(line)
    open(stem + "_table.md", "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n")
    cons = sub[sub.domain == "消费与经济"]
    mk = cons[cons.subissue == MARKETING]
    issue_k = int((d.domain != "非议题内容").sum())
    scope_k = int(d.domain.isin(IN_SCOPE).sum())
    summary = {"n": n, "missing": n_missing, "issue_share": round(issue_k / n, 4), "issue_share_ci": wilson(issue_k, n),
               "in_scope_share": round(scope_k / n, 4), "in_scope_share_ci": wilson(scope_k, n),
               "in_scope_opposing_share": round(float(d[d.domain.isin(IN_SCOPE)].opposing.eq("是").mean()), 4),
               "in_scope_opposing_ci": wilson(int(d[d.domain.isin(IN_SCOPE)].opposing.eq("是").sum()), scope_k),
               "consumption_anxiety_raising_total": int(cons.anxiety_raising_n.sum()),
               "consumption_anxiety_raising_in_marketing": int(mk.anxiety_raising_n.sum()) if len(mk) else 0,
               "subissue_other_share_in_scope": round(float((d[d.domain.isin(IN_SCOPE)]["sub"] == "other").mean()), 4)}
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=HERE).stdout.strip()
    except OSError:
        commit = None
    meta = {"script": "analysis/v6_annotation/taxonomy.py", "commit": commit, "date": time.strftime("%Y-%m-%d"),
            "input": os.path.relpath(path, HERE).replace("\\", "/"), "label_source": src, "summary": summary,
            "compare": None if not cmp else {"input": os.path.relpath(cmp_path, HERE).replace("\\", "/"), "label_source": cmp_name,
                                             "n_on_same_pids": cmp["n"], "missing": cmp["missing"]},
            "intervals": "Wilson 95%", "weighting": "none (impressions sampled uniformly from user histories)",
            "subissues": "keyword rules over the LLM's free-text issue labels; see SUBISSUES in the script",
            "evidence": "measured: LLM labels on a random sample; no human check"}
    json.dump(meta, open(stem + ".meta.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n".join(md))
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main(*sys.argv[1:5])
