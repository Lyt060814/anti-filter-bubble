"""D2/D3 annotation prompt v2 for marriage-and-family narratives (Zhao Dingcheng, 2026-11-07; issue #10).

Same interface as prompt_v1.py and analysis/v6/dual_model_check.py:
    from prompt_v2 import PROMPT_VERSION, SYSTEM, TEMPLATE, FIELDS, parse
Changes from v1 (why: analysis/v6_annotation/agreement.md section 5):
  - the four group-label questions are separate fields answered before the label; `reason` comes last;
    parse() rejects outputs whose label contradicts the answers; no "对象：..." prefix;
  - the target defaults to an individual; role words (婆婆, 丈夫, 继母, 前任) are individuals;
  - generalisation no longer needs "都": a derogatory summary of a loosely named group counts;
    text the video itself says (title, subtitles, voice-over, the creator's own words) counts as endorsed
    unless the video rebuts it;
  - people defined by a specific wrongdoing (家暴者, 出轨者) are not a gender group;
  - explicit advice or verdicts count as a stance for narrative_type.
`python -I -X utf8 prompt_v2.py` runs a self-check (no model needed).
"""
import json
import re

PROMPT_VERSION = "v2"
SYSTEM = "你是严谨的内容分析标注员。只根据给出的视频描述判断，不猜测描述中没有的信息。只输出一个 JSON 对象。"
TEMPLATE = """以下是一条短视频的文字描述（由模型根据视频生成）：
「{cap}」

请按顺序回答下面的问题，最后只输出一个 JSON 对象。

【第 1 步 issue】视频主要内容是否涉及婚恋、夫妻、婆媳、两性关系或家庭中的性别角色。取值："是"/"否"。

【第 2 步 群体标签的四个问题】每个问题单独作答，不要先想结论。
q1_target：视频批评或贬低的对象是谁？
  - 默认是"个人"。婆婆、丈夫、妻子、继母、前任、相亲对象、剧中某个角色，都是具体人物，选"个人"。
  - 只有描述里出现明确指称一类人的说法，才选群体：如"女人""男人""女生们""现在的女孩""某地人"，或"捞女""凤凰男""妈宝男""扶弟魔""普信男"这类称号。指称性别的选"性别群体"，指称地域、年龄、职业等的选"其他群体"。
  - 按具体恶行定义的人（家暴者、出轨的人、骗子），选"个人"，除非视频把这种恶行说成某一性别的普遍特征（如"男人都会家暴"）。
  - 视频没有批评或贬低任何人（温馨、搞笑、记录日常），选"无对象"。
  取值："个人"/"性别群体"/"其他群体"/"无对象"。
q2_generalize：视频是否把负面特征说成这类人共有的？全称说法（"都""没一个"）算；泛指一类人的贬义总结（"现在的女生就是……""有些男人就是……"）也算；用称号解释人物（"一看就是捞女"）也算。q1 不是群体时选"否"。取值："是"/"否"。
q3_negative：归给这类人的是不是人品、能力或动机上的负面特征（如物质、靠不住、心机重、懒）？只说"很难""很累"是诉苦，选"否"。开玩笑的语气不影响判断。取值："是"/"否"。
q4_endorse：视频是否认同这个说法？视频自己的标题、字幕、旁白或博主原话说出来的，默认认同，除非视频明确反驳或嘲讽它；剧中角色的台词，看整条视频是印证它还是纠正它；看不出来选"无法判断"。取值："是"/"否"/"无法判断"。

【第 3 步 group_label】
  - q1 为"性别群体"，且 q2、q3、q4 都是"是"：按被贴标签的性别填"针对女性"或"针对男性"。
  - q1 为"性别群体"，q2、q3 为"是"，q4 为"无法判断"：填"无法判断"。
  - 其他情况：填"无"（q4 为"无法判断"时也可以填"无法判断"）。
  取值："针对女性"/"针对男性"/"无"/"无法判断"。

【第 4 步 narrative_type】只选一类，按顺序取第一个符合的：
  "群体标签"：q1 为"性别群体"或"其他群体"，且 q2、q3、q4 都是"是"时必须选；其他情况不能选。
  "唯一正确"：把一种选择说成唯一正道，同时贬低或否定其他选择。
  "二元对立"：把问题说成只有两个对立的阵营或选项，非此即彼。
  "焦虑渲染"：用恐惧、紧迫感或羞耻感推动一个观点或选择（如年龄倒计时、夸大风险）。
  "无"：以上都不符合。
  博主直接给出劝告、评判或结论（"女生一定要……""千万别……"）时，就是在表达立场，按上面几类判断。只讲冲突、不表态的故事选"无"。商品、课程、婚恋中介等的推销内容选"无"。

【第 5 步 genre】"剧情/段子"（虚构表演、短剧、搞笑段子）/"观点/评论"（博主直接表达看法）/"个人经历"（真人记录自己的生活）/"新闻/普法"/"其他"。

【第 6 步 reason】最后写，不超过 40 字，用自己的话概括依据，不要引用描述原文。

issue 为"否"时，q1_target 填"无对象"，q2–q3 填"否"，q4 填"否"，group_label 和 narrative_type 都填"无"。

【示例】（示例是编写的，不来自真实视频）
- 描述大意：短剧中一名妻子为骗保险金谋害丈夫，最后被警方抓获。
  {{"issue":"是","q1_target":"个人","q2_generalize":"否","q3_negative":"是","q4_endorse":"否","group_label":"无","narrative_type":"无","genre":"剧情/段子","reason":"单个反派，没有说到女性整体"}}
- 描述大意：丈夫偷吃妻子藏的零食被发现，两人互相打趣，配着搞笑音效。
  {{"issue":"是","q1_target":"无对象","q2_generalize":"否","q3_negative":"否","q4_endorse":"否","group_label":"无","narrative_type":"无","genre":"剧情/段子","reason":"夫妻搞笑互动，没有贬低谁"}}
- 描述大意：博主讲述一起家暴案件，批评施暴的丈夫，呼吁受害者及时报警。
  {{"issue":"是","q1_target":"个人","q2_generalize":"否","q3_negative":"是","q4_endorse":"是","group_label":"无","narrative_type":"无","genre":"观点/评论","reason":"批评具体施暴者，没有说男性都会家暴"}}
- 描述大意：婆婆干涉小夫妻生活，字幕总结"嫁给凤凰男就是嫁给他全家"。
  {{"issue":"是","q1_target":"性别群体","q2_generalize":"是","q3_negative":"是","q4_endorse":"是","group_label":"针对男性","narrative_type":"群体标签","genre":"剧情/段子","reason":"字幕用贬义称号概括农村出身的男性"}}
- 描述大意：视频字幕写着"现在的女生谈恋爱，看的只是你兜里有多少钱"，配着男生叹气的画面。
  {{"issue":"是","q1_target":"性别群体","q2_generalize":"是","q3_negative":"是","q4_endorse":"是","group_label":"针对女性","narrative_type":"群体标签","genre":"观点/评论","reason":"字幕把只看钱说成当下女生的共性"}}
- 描述大意：博主列出"男人都靠不住"等网络说法，并逐条反驳。
  {{"issue":"是","q1_target":"性别群体","q2_generalize":"是","q3_negative":"是","q4_endorse":"否","group_label":"无","narrative_type":"无","genre":"观点/评论","reason":"转述标签但立场是反驳"}}

按 issue、q1_target、q2_generalize、q3_negative、q4_endorse、group_label、narrative_type、genre、reason 的顺序输出 JSON，不要输出其他内容。"""
FIELDS = {"issue": ["是", "否"], "q1_target": ["个人", "性别群体", "其他群体", "无对象"],
          "q2_generalize": ["是", "否"], "q3_negative": ["是", "否"], "q4_endorse": ["是", "否", "无法判断"],
          "group_label": ["针对女性", "针对男性", "无", "无法判断"],
          "narrative_type": ["唯一正确", "二元对立", "焦虑渲染", "群体标签", "无"],
          "genre": ["剧情/段子", "观点/评论", "个人经历", "新闻/普法", "其他"]}
POS = ("针对女性", "针对男性")


def consistent(d):
    """True if group_label and narrative_type follow from the four answers (rules in TEMPLATE step 3-4)."""
    if d["issue"] == "否":
        return d["group_label"] == "无" and d["narrative_type"] == "无"
    group = d["q1_target"] in ("性别群体", "其他群体")
    core = group and d["q2_generalize"] == "是" and d["q3_negative"] == "是"
    all_yes = core and d["q4_endorse"] == "是"
    gender = d["q1_target"] == "性别群体"
    if d["group_label"] in POS:
        if not (gender and all_yes):
            return False
    elif gender and all_yes:
        return False
    if d["group_label"] == "无法判断" and d["q4_endorse"] != "无法判断":
        return False
    if gender and core and d["q4_endorse"] == "无法判断" and d["group_label"] != "无法判断":
        return False
    return (d["narrative_type"] == "群体标签") == all_yes


def parse(text):
    """Return the label dict, or None if the JSON is invalid, a value is out of range, or labels contradict answers."""
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if not all(d.get(k) in v for k, v in FIELDS.items()):
        return None
    if not consistent(d):
        return None
    d["reason"] = str(d.get("reason", ""))[:60]
    return d


if __name__ == "__main__":
    TEMPLATE.format(cap="测试")
    examples = re.findall(r"^  (\{\{.*\}\})$", TEMPLATE, re.M)
    assert len(examples) == 6, len(examples)
    for e in examples:
        assert parse(e.replace("{{", "{").replace("}}", "}")) is not None, e
    base = {"issue": "是", "q1_target": "性别群体", "q2_generalize": "是", "q3_negative": "是", "q4_endorse": "是",
            "group_label": "针对女性", "narrative_type": "群体标签", "genre": "其他", "reason": "x"}
    j = lambda **kw: json.dumps({**base, **kw}, ensure_ascii=False)
    assert parse(j()) is not None
    assert parse(j(q1_target="个人")) is None                      # label without a group
    assert parse(j(group_label="无")) is None                       # all yes but no label
    assert parse(j(narrative_type="焦虑渲染")) is None             # gender label must be 群体标签
    assert parse(j(q1_target="其他群体", group_label="无")) is not None
    assert parse(j(q1_target="其他群体", group_label="无", narrative_type="无")) is None
    assert parse(j(q4_endorse="无法判断", group_label="无法判断", narrative_type="无")) is not None
    assert parse(j(q4_endorse="无法判断", group_label="无", narrative_type="无")) is None
    assert parse(j(q4_endorse="否", group_label="无法判断", narrative_type="无")) is None
    assert parse(j(issue="否")) is None
    assert parse(j(issue="否", q1_target="无对象", group_label="无", narrative_type="无")) is not None
    assert parse(j(q1_target="男")) is None and parse("not json") is None
    print("prompt", PROMPT_VERSION, "ok;", len(TEMPLATE), "chars;", len(examples), "examples parse")
