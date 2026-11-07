# Appendix A. Narrative Definitions and the Annotation Prompt

<!-- Zhao Dingcheng, 2026-11-07. English version of analysis/v6_annotation/narrative_types.md (definitions, v2) and prompt_v2.py (prompt text, copied verbatim in A.5); A.6 is BU_TEMPLATE from analysis/v6/deepseek_label.py, copied verbatim with the domain list inserted. -->

All labels in this report were produced by large language models from the text description of each video; no video was labelled by hand. This appendix gives the definitions the models were asked to apply, how the prompt changed between versions, and the exact prompt used for the final labels. All examples below were written by us to illustrate the rules; none is taken from a video description.

## A.1 Common rules

1. **Label what the video endorses, not what it mentions.** A video that reports, rebuts or mocks a claim does not hold that claim. A video's own title, subtitles, voice-over or the creator's own words count as endorsed unless the video clearly rebuts them. For a line spoken by a character in a drama, ask whether the video as a whole confirms or corrects it; if this cannot be told, answer "cannot judge".
2. **Judge the content, not the genre.** Dramas, sketches, personal stories, commentary and news can all carry an opposing narrative, and all can lack one.
3. **Judge from the description only.** The model sees a machine-written description of the video, not the video. A summary sentence added by the describer (for example, "this reflects a social phenomenon") is not a claim made by the video; subtitles, dialogue and narration reported in the description are.
4. **One type per video.** If several types apply, take the first in the order group label → only-right-way → binary opposition → anxiety-raising.
5. **Conflict is not a stance.** A story about an affair or a quarrel with in-laws that takes no position is labelled "none". Conversely, explicit advice, a verdict or a conclusion ("girls must…", "never…") is a stance and is judged by type.
6. **Marketing is excluded.** Sales talk for products, courses, money-making games or matchmaking services is labelled "none", even when it uses fear or urgency.

## A.2 The four narrative types

| Type | Definition | Example (invented) | Not this type (invented) |
|---|---|---|---|
| Group label | A whole social group (by gender, region, age, occupation, origin) is portrayed negatively, or one case is presented as typical of the group | Subtitles over a sighing young man: "Girls these days only look at how much money you have" | A drama in which one wife plots against her husband for insurance money and is arrested |
| Only-right-way | One choice is presented as the only proper path, and the alternatives are belittled | "A woman who doesn't marry will have no one to look after her when she is old; marriage and children are the only right way" | A creator says married life suits them, without criticising other choices |
| Binary opposition | A question is framed as having exactly two opposed camps or options, with no middle ground | "In a marriage there are only two kinds of people: those who control and those who are controlled" | A couple on a show explain their different views on housework |
| Anxiety-raising | Fear, urgency or shame is used to push a view or a choice | "Girls who are still single at 30 can only pick from what others left behind" | A lawyer calmly explains how property is divided in a divorce |

## A.3 Deciding whether a video carries a gender group label

The case study (Section 5) uses only gender group labels, so this type has an explicit procedure. The model answers four questions in order; the label is "against women" or "against men" only if all four are "yes".

1. **Who is the target?** By default, an individual. Role words such as mother-in-law, husband, wife, stepmother, ex-partner or a blind-date partner refer to specific people. A group is the target only when the description names one explicitly ("women", "girls these days", "people from a certain place") or uses a derogatory group nickname (for example *fenghuang nan*, a man from a poor rural family who is said to bring his whole family into the marriage, or *lao nü*, a woman said to date for money). People defined by a specific wrongdoing (abusers, cheaters, swindlers) are individuals, unless the video presents the wrongdoing as typical of a gender ("all men hit their wives"). The slang terms *zha nan* and *zha nü* ("scumbag" man or woman) are treated the same way: calling one person a scumbag is not a group label; "there isn't a man who isn't a scumbag" is.
2. **Is a negative trait generalised to the group?** Universal claims ("all", "not one of them") count; so does a derogatory summary of a loosely named group ("girls these days are just…"), and using a group nickname to explain a person's behaviour.
3. **Is the trait negative in character, ability or motive?** For example materialistic, unreliable, scheming or lazy. Saying a group has it hard is a complaint, not a label. A joking tone does not change the answer.
4. **Does the video endorse it?** Rule A.1.1 applies.

Labels aimed at non-gender groups (region, age and so on) are recorded as the group-label narrative type but not as a gender label, and are reported only in the distribution in Section 4.2.

## A.4 How the prompt changed

We checked each version by having the open model (Qwen3-30B-A3B-Instruct-2507) and a stronger reference model (DeepSeek V4 Pro) label the same 500 marriage-and-family videos (Section 4.3).

| Version | Main change | Open model: gender group label | Reference model: gender group label |
|---|---|---:|---:|
| v0 | One-paragraph definition with a note that single characters do not count | 4.0% (20/498) | 1.4% (7/500) |
| v1 | Four questions in prose; the model writes its reason first, starting with "target: individual / group" | 51% (252/494) | 0.6% (3/500) |
| v2 | The four questions become separate output fields answered before the label, and the reason comes last; the target defaults to an individual; looser tests for generalisation and endorsement; wrongdoing-defined groups excluded | 13% (66/500) | 1.0% (5/500) |

The same edit moved the two models in opposite directions. Under v1, the open model began almost every reason with "target: group", including reasons for videos it then labelled "none", and then looked for a generalisation to fit; the reference model read the stricter wording as requiring a universal claim, and withdrew five of its seven earlier positives. In v2 the answer to each question is a separate field, and outputs whose label does not follow from the four answers are rejected and, for the API model, re-requested. Under v2 the reference model's five flags were all among its seven under v0, and every disagreement between the two models began at the first question, who the target is (Section 4.3). Section 4.2 uses the cross-domain prompt in A.6; Sections 4.3 and 5 use prompt v2.

## A.5 The v2 prompt (verbatim)

The prompt is in Chinese, as are the descriptions. `{cap}` is replaced by the video description, truncated to 1,200 characters. Doubled braces become single braces once the description is inserted. The output fields are: `issue` (whether the video concerns marriage, couples, in-laws, gender relations or gender roles in the family), `q1_target` to `q4_endorse` (the four questions in A.3), `group_label` (against women / against men / none / cannot judge), `narrative_type` (the four types or none), `genre` (drama or sketch / opinion / personal story / news or legal explainer / other) and `reason` (at most 40 characters, in the model's own words).

**System prompt**

```text
你是严谨的内容分析标注员。只根据给出的视频描述判断，不猜测描述中没有的信息。只输出一个 JSON 对象。
```

**User prompt**

```text
以下是一条短视频的文字描述（由模型根据视频生成）：
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

按 issue、q1_target、q2_generalize、q3_negative、q4_endorse、group_label、narrative_type、genre、reason 的顺序输出 JSON，不要输出其他内容。
```

## A.6 The cross-domain prompt for the bottom-up sample (verbatim)

Section 4.2 labels a random sample of all impressions, most of which are not about marriage, so it uses a shorter prompt that covers every domain. It was run with DeepSeek V4 Pro and applies the common rules in A.1 in condensed form. The system prompt is the same as in A.5. `{cap}` is replaced by the video description, truncated to 1,200 characters; the list of eleven domains, shown here already inserted, is the one in Table 4.1, and doubled braces become single braces. The output fields are `domain`, `issue` (at most eight characters, or "none"), `opposing` (whether the video itself endorses a contested position), `narrative_type` and `reason` (at most 30 characters). Outputs with an invalid domain or type, or with a narrative type but no opposing position, were rejected and re-requested.

**System prompt**

```text
你是严谨的内容分析标注员。只根据给出的视频描述判断，不猜测描述中没有的信息。只输出一个 JSON 对象。
```

**User prompt**

```text
以下是一条短视频的文字描述（由模型根据视频生成）：
「{cap}」

请判断：
1. "domain"：视频主要涉及的社会议题大类，取值之一："性别与婚恋"、"身体与外貌"、"家庭与代际"、"人生选择与出路"、"消费与经济"、"资源与公平"、"学术与思想"、"文化与价值观"、"公共秩序与自由"、"其他社会议题"、"非议题内容"。娱乐、美食、游戏、风景、商品展示、技能教学等不涉及社会观点争议的内容选"非议题内容"。
2. "issue"：若不是"非议题内容"，用不超过8个字写出具体议题；否则写"无"。
3. "opposing"：视频本身是否认同并表达了某种有争议的立场或叙事。注意：只转述、反驳或嘲讽某种说法不算；讲冲突或纠纷但不表态不算；商品、课程、"赚钱游戏"等营销推销不算；中性记录、介绍、娱乐不算。取值："是"/"否"。
4. "narrative_type"：若 opposing 为"是"，选一类（按此顺序取第一个符合的）："群体标签"（给某类人整体贴负面标签或把个案说成群体特征）、"唯一正确"（把一种选择说成唯一正道并贬低其他）、"二元对立"（非此即彼的两个阵营）、"焦虑渲染"（用恐惧、紧迫感、羞耻感推动观点或选择）；否则为"无"。
5. "reason"：不超过30字，用自己的话概括依据，不要引用描述原文。

只输出 JSON，例如：{{"domain":"性别与婚恋","issue":"彩礼","opposing":"否","narrative_type":"无","reason":"……"}}
```
