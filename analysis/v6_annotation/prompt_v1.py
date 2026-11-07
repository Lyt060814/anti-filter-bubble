"""D2 annotation prompt v1 for marriage-and-family narratives (Zhao Dingcheng, 2026-11-07).

Drop-in replacement for SYSTEM / TEMPLATE / FIELDS in analysis/v6/dual_model_check.py:
    from prompt_v1 import PROMPT_VERSION, SYSTEM, TEMPLATE, FIELDS, parse
Definitions: narrative_types.md. Human-readable copy and rationale: prompt.md.
`python -I prompt_v1.py` runs a self-check of the parser and template (no model needed).
"""
import json
import re

PROMPT_VERSION = "v1"
SYSTEM = "你是严谨的内容分析标注员。只根据给出的视频描述判断，不猜测描述中没有的信息。拿不准时按规则输出\"无法判断\"，不要猜。只输出一个 JSON 对象。"
TEMPLATE = """以下是一条短视频的文字描述（由模型根据视频生成）：
「{cap}」

请按下面的顺序判断，最后只输出一个 JSON 对象。

【共同规则】
- 标的是视频本身认同的说法。视频转述、反驳或嘲讽某种说法，不算视频持有它。剧情里某个角色说了偏激的话，要看整条视频是在肯定它，还是把它当作被纠正的错误。
- 看内容，不看体裁。剧情、段子、个人经历、评论都可能含对立叙事，也都可能不含。
- 描述者自己加的概括（如"反映了当代婚恋现象"）不算视频在推广，要看视频本身说了什么、演了什么。
- 有冲突不等于有立场。讲出轨、婆媳矛盾、离婚纠纷的视频，如果没有表达立场，叙事类型是"无"。
- 商品、课程、婚恋中介等的推销内容，叙事类型一律为"无"，依据写"营销"。

【第 1 步 issue】视频主要内容是否涉及婚恋、夫妻、婆媳、两性关系或家庭中的性别角色。取值："是"/"否"。为"否"时，group_label 填"无"，narrative_type 填"无"。

【第 2 步 group_label：群体标签】依次回答下面四个问题，任何一个答"否"，就填"无"：
  (1) 批评的对象是一类人（"女人""男生""某地的人"），而不只是一个具体人物？剧中的单个反派、博主的某个前任，都只是具体人物。
  (2) 有没有推广到群体？算推广的情况：全称说法（"都""没一个""十个有九个"）；用贬义的群体称号解释人物（"典型的凤凰男""一看就是捞女"，以及妈宝男、扶弟魔、普信男等）；由个案得出群体结论（"所以娶某地姑娘要小心"）。
  (3) 归给这个群体的是负面特征（人品、能力、动机，如物质、靠不住、心机重）？只说某个群体"很难""很累"是诉苦，不算。开玩笑的语气不影响判断。
  (4) 视频认同这个说法（见共同规则第一条）？
  四个都答"是"：按被贴标签的性别填"针对女性"或"针对男性"；两个性别都被贴了标签时，选更突出的一方。被贴标签的不是性别群体（如地域、年龄）时，这里填"无"，在第 3 步填"群体标签"。
  描述太短、太乱，或者看不出视频是否认同时，填"无法判断"。
  取值："针对女性"/"针对男性"/"无"/"无法判断"。

【第 3 步 narrative_type：叙事类型】只选一类。按下面的顺序，取第一个符合的：
  "群体标签"：第 2 步为"针对女性"或"针对男性"时必须选这一项；给非性别群体整体贴负面标签时也选这一项。
  "唯一正确"：把一种选择说成唯一正道，同时贬低或否定其他选择。只推荐、不贬低别的，不算。
  "二元对立"：把问题说成只有两个对立的阵营或选项，非此即彼。只是呈现两种意见、征集观点，不算。
  "焦虑渲染"：用恐惧、紧迫感或羞耻感推动一个观点或选择（如年龄倒计时、夸大风险）。平静地讲风险信息不算；营销不算。
  "无"：以上都不符合，包括中性记录、介绍、娱乐，以及没有立场的冲突故事。
  第 2 步为"无法判断"时，这里按其余几类判断；都不符合就选"无"。

【第 4 步 genre：形式】"剧情/段子"（虚构表演、短剧、搞笑段子）/"观点/评论"（博主直接表达看法）/"个人经历"（真人记录自己的生活）/"新闻/普法"/"其他"。

【reason：依据】不超过 40 字，用自己的话概括，不要引用描述原文。先写批评对象是"个人"还是"群体（哪个群体）"，再写理由。

【示例】（示例是编写的，不来自真实视频）
- 描述大意：短剧中一名妻子为骗保险金谋害丈夫，最后被警方抓获。
  输出：{{"reason":"对象：个人。单个反派，未推广到女性","issue":"是","group_label":"无","narrative_type":"无","genre":"剧情/段子"}}
- 描述大意：婆婆干涉小夫妻生活，字幕总结"嫁给凤凰男就是嫁给他全家"。
  输出：{{"reason":"对象：群体（农村出身男性）。用贬义称号推广","issue":"是","group_label":"针对男性","narrative_type":"群体标签","genre":"剧情/段子"}}
- 描述大意：博主列出"男人都靠不住"等网络说法，并逐条反驳。
  输出：{{"reason":"对象：群体。转述标签但立场是反驳","issue":"是","group_label":"无","narrative_type":"无","genre":"观点/评论"}}
- 描述大意：博主说过了三十岁的女生只能挑别人剩下的，劝女生尽早结婚。
  输出：{{"reason":"对象：群体（大龄女性）。用年龄恐惧推动早婚","issue":"是","group_label":"无","narrative_type":"焦虑渲染","genre":"观点/评论"}}

按 reason、issue、group_label、narrative_type、genre 的顺序输出 JSON，不要输出其他内容。"""
FIELDS = {"issue": ["是", "否"], "group_label": ["针对女性", "针对男性", "无", "无法判断"],
          "narrative_type": ["唯一正确", "二元对立", "焦虑渲染", "群体标签", "无"],
          "genre": ["剧情/段子", "观点/评论", "个人经历", "新闻/普法", "其他"]}


def parse(text):
    """Return the label dict, or None if the output is not valid JSON or a value is out of range.

    Also enforces two consistency rules from narrative_types.md: a gendered group label implies
    narrative_type 群体标签, and issue 否 implies no label.
    """
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if not all(d.get(k) in v for k, v in FIELDS.items()):
        return None
    if d["group_label"] in ("针对女性", "针对男性") and d["narrative_type"] != "群体标签":
        return None
    if d["issue"] == "否" and (d["group_label"] != "无" or d["narrative_type"] != "无"):
        return None
    d["reason"] = str(d.get("reason", ""))[:60]
    return d


if __name__ == "__main__":
    TEMPLATE.format(cap="测试")  # braces in the examples must be escaped
    ok = '{"reason":"对象：个人。","issue":"是","group_label":"无","narrative_type":"无","genre":"剧情/段子"}'
    bad_rule = '{"reason":"x","issue":"是","group_label":"针对女性","narrative_type":"焦虑渲染","genre":"其他"}'
    bad_value = '{"reason":"x","issue":"是","group_label":"女性","narrative_type":"无","genre":"其他"}'
    assert parse("好的：" + ok)["group_label"] == "无"
    assert parse(bad_rule) is None and parse(bad_value) is None and parse("not json") is None
    print("prompt", PROMPT_VERSION, "ok;", len(TEMPLATE), "chars")
