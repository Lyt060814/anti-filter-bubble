---
title: "COMP1110 小组汇报方案 v2（10 分钟 · 5 人）"
subtitle: "Keeping the Topic, Widening the View · 按新分工重排"
---

# 0 先看这一页：总览与本次改动

**依据**：Presentation Guideline（2026-11-05 版）、Project Plan、GitHub 仓库（已重新核对，最新状态不变）、期末报告（整合版）。

**这次的改动**

- 第 1–5 页分工不变：Fu Yitong 第 1–3 页，Wang Junbo 第 4–5 页。
- 原来的第 6–9 页合并成一个部分，全部交给 **Li Yitong**（真实原型 + 数据地图 + OneRec 实验 + 各操作能动到什么）。
- Xu Ruicong 仍讲第 10–12 页（模拟、可察觉性、报告与决策规则）。
- 新增最后一个部分第 13–15 页：**婚恋与家庭案例研究 + 总结**，由 **Zhao Dingcheng** 讲（他定义了群体标签的规则、做了标注可靠性分析）。
- 全场从 12 页变成 **15 页**，仍是 **10:00**。

> **关于"生育"**：我重新读了仓库。最终案例研究是"**性别与婚恋（婚恋与家庭）**"，选视频的 15 个关键词是：离婚、婆媳、婆婆、女方、男方、家暴、出轨、AA制、彩礼、结婚、婚姻、相亲、夫妻、老公、老婆，**没有生育类关键词**。"生孩子、催生、二胎"等词只出现在早期可行性扫描脚本里，最终报告和结果中没有生育的单独分析。所以本方案把案例写成"婚恋与家庭"，**不会**讲生育方面的发现；如果你们想提到，只能说"早期扫描过，最终没有纳入"。

**Guideline 里直接决定打分的几条**

| 要求 | 我们怎么落实 |
|---|---|
| 10 分钟，**没有 Q&A**，5 人都要讲（时间可以不等） | 5 个连续板块，不插队；最后一页自己把话讲完 |
| 假设听众不了解项目；先讲问题和研究空白，再讲做了什么和主要贡献 | 前 3 页只讲问题、例子、gap，不出现术语 |
| 选能体现实质的内容，解释陌生概念，用一个例子或图；**不要讲完报告所有细节** | 全场只讲少数核心数字、一个主例子（育儿）、一个案例（婚恋）、一张主图 |
| 不要照读稿，只用 cue notes | 每人一张 cue card（≤ 8 个关键词） |
| **每页显示当前讲者全名** | 右下角固定 `Presenting: 全名`，多人页标相关姓名 |
| 11-16 交 Moodle（.pptx 或 PDF）；汇报必须基于已交幻灯片，仅允许格式/动画等小差异 | 提交后只改格式，不改内容 |
| 评分：内容清晰 30%、结构与时间 20%、幻灯片 20%（按**现场使用**的幻灯片评）、个人 Delivery 30% | 见各人"踩坑"和 §5 |

**一句话主线（全组统一）**

> 信息茧房不只是"话题窄"，更是**同一话题里被一直推同一种说法**。我们把它拆成"兴趣"和"观点偏斜"两个量，让用户说清想**减少什么、保留什么、探索什么**，再按**效果、损失、成本**选操作；并在真实快手日志上、以婚恋与家庭为案例测试：哪些成立，哪些不成立。

**统一的证据标签**（口头也要说出来）：**Measured（实测）· Derived（推导）· Scenario（模拟情境）· Proposed（设计提议，未测试）**

# 1 幻灯片框架与顺序（共 15 页）

| 页 | 标题（屏幕上的短句） | 讲者 | 时长 | 主视觉 |
|---|---|---|---|---|
| 1 | Keeping the Topic, Widening the View | Fu Yitong | 0:20 | 手机 feed 示意 + 全员姓名 |
| 2 | A feed can look diverse and still be one-sided | Fu Yitong | 0:45 | 左：话题饼图；右：放大"育儿"10 条视频，7 条同一说法（*Illustrative*） |
| 3 | What is missing, and our question | Fu Yitong | 0:45 | 三列（测量 / 审计 / 控制）各自看不到什么；底部研究问题 |
| 4 | Interest is not skew | Wang Junbo | 0:55 | m 与 V 两个量；"1.0% → 1.4% → 2.8%"例子（*Illustrative*） |
| 5 | From a goal to an action | Wang Junbo | 1:05 | 四阶段框架图 + 目标"减少 / 保留 / 探索" + 一行规则 |
| 6 | What we actually built | Li Yitong | 0:20 | 真实原型流水线 + 已做 / 仅提议清单 |
| 7 | Where one-sided narratives appear | Li Yitong | 0:35 | 大数字 **1 in 7**；五个议题域的小条形图（7%–20%） |
| 8 | Does the recommender amplify a narrative? | Li Yitong | 0:55 | 三个结果：话题强响应；"不感兴趣"反向；叙事对比≈0 |
| 9 | What each action can reach | Li Yitong | 0:30 | 动作表：作用在推荐器状态还是展示结果；平台层 vs 个人层 |
| 10 | Simulating the escape | Xu Ruicong | 0:40 | 各策略对偏斜的影响 + 保留的话题量（报告图 4 简化） |
| 11 | Can a user even notice? | Xu Ruicong | 0:35 | 6,475 条议题视频 ≈ 405,000 次观看 vs 用户历史中位数 493 |
| 12 | What a user-side report should do | Xu Ruicong | 0:35 | 报告原型截图（"Not enough evidence yet"）+ 决策规则的三条教训（*Proposed*） |
| 13 | Case study: marriage and family | Zhao Dingcheng | 0:35 | 选择理由 + 15 个关键词的数据规模 + "群体标签"四问判断 |
| 14 | What we found in the case study | Zhao Dingcheng | 0:55 | 三个发现：很稀有；标注很脆弱；没有被"奖励" |
| 15 | Takeaway | Zhao Dingcheng | 0:30 | 三句话总结 + 四色证据图例 |

**时间分配**：Fu 1:50（0:00–1:50）· Wang 2:00（1:50–3:50）· Li 2:20（3:50–6:10）· Xu 1:50（6:10–8:00）· Zhao 2:00（8:00–10:00）。合计 **10:00**；彩排目标 **9:30–9:50**。

**幻灯片设计规则（全组一致）**

1. 每页**一个信息**、一个主视觉，文字 ≤ ~25 个英文词（不含图内标签）。
2. 右下角 `Presenting: Fu Yitong`（全名，不缩写）。
3. 每个数字旁小字标证据类型和来源（如 *Measured · RecIF, 162,074 users*）；示意例子标 *Illustrative*。
4. 字号 ≥ 18pt，图内标签 ≥ 14pt；不放整页表格。
5. "实测 / 推导 / 模拟 / 提议"四种标签的颜色全场固定。
6. 提交 PDF 前检查字体和图片是否丢失。

# 2 五人分工总表

| 讲者 | 板块 | 页 | 时长 | 理由 |
|---|---|---|---|---|
| **Fu Yitong** | ① 问题与研究空白 | 1–3 | 1:50 | 计划中负责问题定义与文献 |
| **Wang Junbo** | ② 我们的核心想法（整合后的理想化构想） | 4–5 | 2:00 | 计划中负责用户目标、曝光报告和控制设计 |
| **Li Yitong** | ③ 真实原型 + 数据地图 + 推荐器实验与理论 | 6–9 | 2:20 | 技术整合者；推导命题，跑了全部 OneRec 实验和 LLM 标注流水线 |
| **Xu Ruicong** | ④ 模拟、可察觉性、报告与决策 | 10–12 | 1:50 | 实现模拟与策略比较，计算检测样本量 |
| **Zhao Dingcheng** | ⑤ 婚恋与家庭案例研究 + 总结 | 13–15 | 2:00 | 定义了群体标签规则，做了标注可靠性分析 |

> 第 ③ 部分页数最多（4 页），所以内容必须**狠狠删**：只讲结论，不讲方法细节。方法细节留给第 ⑤ 部分的案例页。

# 3 每个人的详细方案

## ① Fu Yitong：问题与研究空白（第 1–3 页，约 1:50）

**板块核心目标**：让没听过项目的同学在不到 2 分钟里明白：**现象是什么；现有办法为什么看不到；我们问什么**。不出现公式、模型名。

**屏幕上**
- 第 1 页：标题 + 钩子 "Your feed looks diverse. Is it?" + 五人姓名（讲者加粗）。
- 第 2 页：左话题饼图（food / music / travel / parenting）"Looks diverse"；右把 parenting 放大成 10 个方块，7 个同色 "strict discipline is the only way"，标 *Illustrative*。
- 第 3 页：三列卡片：*Category checks*（只数话题）、*Audits*（多在政治话题、从平台外部看）、*"Not interested"*（只能对整个话题说不）；底部研究问题；强调 **Interest ≠ Skew**。

**演讲提示（English cue lines，用自己的话说）**
- *Slide 1（20s）*："Imagine you watch parenting videos. Over a week, one claim keeps appearing: strict discipline is the only way. Could your feed do that without you noticing?"
- *Slide 2（45s）*："Count topics and this feed is diverse. Zoom into parenting and most videos say the same thing. You may want less of that claim but still want parenting advice. The button you have, 'not interested', can only say no to the whole thing."
- *Slide 3（45s）*："Platforms and researchers mostly measure cocoons by counting topics. Audits look at politics, from outside the app. Controls ask how much unwanted content disappears, not how much *wanted* content you lose. Our question: how can users see limits in the viewpoints within an issue, and adjust exposure without losing what they still want? Our real data are about marriage and family, which you'll see later. Wang Junbo will show how we make this measurable."

**技巧**：先例子后抽象；只教一个新概念（interest ≠ skew）；"信息茧房"口头解释成 *a feed that keeps showing you one side*；gap 用"三个看不见"收束（数话题不数说法、在外部看、只量删除不量保留）。

**容易踩的坑**：背景讲太久；把例子数字当真实发现；说"我们证明算法有害"（只主张**曝光**，不主张信念变化或平台意图）；照念标题；研究问题念太快。

**时长**：1:50（20 + 45 + 45）。**超时就砍**：第 3 页 "Audits" 一列。

## ② Wang Junbo：我们的核心想法（第 4–5 页，约 2:00）

**板块核心目标**：讲清**整合后的理想化构想**（评分重点）：**两个量（兴趣 m、偏斜 V）+ 用户确认的目标（减少/保留/探索）+ 按效果·损失·成本选操作的规则**，且该规则**可以回答"无需操作"或"没有可行方案"**。

**屏幕上**
- 第 4 页：两张并列卡片：*Interest = how much of my feed is this topic*；*Skew = inside the topic, how much more one narrative shows up than it should*。下方例子条：`available 1.0% → platform shows 1.4% → this user sees 2.8%`，标出 *platform layer 0.34 + personal layer 0.71*，标 *Illustrative*（用婚恋视频里"对某一性别的整体负面标签"来举例，与后面案例呼应）。
- 第 5 页：四阶段图（Observe → Diagnose → Decide → Verify）+ 左侧三个目标图标 + 一行规则：*Meet the goal, keep wanted content and effort within limits — or say "no feasible option".*

**演讲提示**
- *Slide 4（55s）*："Two numbers describe a feed. Interest is how much of it is about the topic. Skew is what you see once you're inside the topic. A topic lover has high interest and normal skew. Someone in a cocoon has high skew, whatever their interest. A made-up example: a narrative is 1% of what's available, the platform shows it 1.4% of the time on average, and this user sees it 2.8%. The first jump is shared by everyone; the second is personalisation, and that is the part a user can act on."
- *Slide 5（65s）*："Our idea has four steps: observe, diagnose, decide, verify. In 'decide', *you* confirm a goal: reduce some claims, retain other content, explore reasons you haven't met. We compare actions by three things: how close to the goal, how much wanted content you keep, how much effort. It can answer 'no action needed' or 'no feasible option'. This is our ideal design; Li Yitong will now show what we actually built and tested."

**技巧**：第 4 页用手势把两个量分左右；"platform layer / personal layer"一句话："the first is shared by everyone, the second is yours"；第 5 页顺着箭头讲；明确说"这是设计，后面讲哪些测过"；强调目标由**用户确认**。

**坑**：把 1.0/1.4/2.8 说成真实数据；术语（entropy、log-odds）；讲成一堆框；忘了"可以说无需操作/无可行方案"；把目标说成"我们判断用户想要什么"。

**时长**：2:00（55 + 65）。**超时就砍**：第 5 页四阶段的逐步解释，保留"目标 + 三个比较量 + 可以说无可行方案"。

## ③ Li Yitong：真实原型 + 数据地图 + 推荐器实验与理论（第 6–9 页，约 2:20）

**板块核心目标**：（1）**单独、清楚地介绍 GitHub 上真实落地的原型**；（2）给出一张"对立叙事在哪里"的数据地图；（3）回答"推荐器会放大吗？按钮管用吗？"；（4）用一句核心洞察串起来：**让推荐器能形成茧房的量，也正是让用户能解开茧房的量**。这是全场信息量最大的部分，**只讲结论**。

**屏幕上**
- 第 6 页：横向流水线 *RecIF log (162,074 users) → LLM labels on video descriptions → OneRec probes → transparent simulation*；下方两排：✔ *Built and run*（标注与可靠性检查、OneRec 实验、模拟、检测计算）；○ *Proposed, not built*（用户端报告、人工标注、用户测试）。
- 第 7 页：大数字 **1 in 7**（*five everyday-issue domains, 13%, 95% interval 10–17%*）；小条形图：家庭与代际 7% 到 消费与金钱 20%；小字 *About 7% of impressions touch a social issue · Measured*。
- 第 8 页：三个并排小图：①话题强响应（2.6% → 5.7%）；②"Not interested" 反而升到 4.0%；③叙事对比 +0.12，落在随机伪叙事范围（−0.18 到 +0.24）内。标 *Measured · OneRec-1.7B, 30–50 held-out users*。
- 第 9 页：精简三行表（推荐器状态：不感兴趣 / 看别的 / 删历史 → 个人层；展示结果：过滤 → 个人层 + 平台层；关闭个性化 → 去掉个人层）+ 一句 *Same quantity builds the cocoon and takes it apart.* 标 *Derived*。

**演讲提示**
- *Slide 6（20s）*："What did we actually build? A prototype in our repository: a public Kuaishou log of about 160,000 users; language models that label each video's description; probes of a recommender trained on that log; and a small simulator. We did *not* build a user-facing tool or run a user test."
- *Slide 7（35s）*："First, a map. About 7% of what users are shown touches a social issue. In five everyday-issue domains, about one video in seven carries a one-sided narrative, from 7% in family topics to 20% in money topics. Dingcheng will zoom into one domain at the end."
- *Slide 8（55s）*："Then we tested whether a recommender amplifies a narrative. We took OneRec, trained by Kuaishou on this log, edited a user's history in one controlled way, and measured how the recommendations changed. One narrative here is a negative label on a whole gender. Result one: the *topic* responds strongly; ten issue videos double the issue share. Result two: 'not interested' goes the *wrong way*, and raises similar recommendations. Result three: the narrative is barely separated from other videos on the issue; the effect is inside the range of random sets. That is a negative result for our own hypothesis, and we report it as it is."
- *Slide 9（30s）*："Our maths gives one rule: how a feedback action changes your skew is proportional to how well the recommender tells the narrative apart. If it can't, your clicks can't build a cocoon, and your feedback can't remove one. Actions on your history reach your personal layer, not the platform's shared layer; only filters do. Xu Ruicong will show how this plays out over thousands of videos."

**技巧**
1. 每页只说**一个结论**，数字不超过 2 个；表格不逐行念。
2. 第 8 页逐个结果用同一句式 *We did X → the model did Y*；先讲"怎么测"（改一次历史，量一次变化）。
3. **主动讲负面结果**（≈0、按钮反向）：这是诚实和思考的加分点。
4. 命题只讲一句话版本；公式留在报告。
5. 明确"这是开源模型，不是快手 App 里的推荐器"。
6. 彩排时**计时每页**，第 6 页和第 9 页必须守住 20s/30s，否则会拖垮后面的人。

**坑**
- 时间失控（4 页 2:20 很紧）；多讲了标注方法（留给最后一个部分）。
- 说"证明快手的'不感兴趣'失效"——只能说"在这个开源模型里反向"。
- 把早期试点值 +1.13 当主结果（它是标注较差时的**上限情境**）。
- 把"≈0"说成"证明没有效应"——应说"和零无法区分（只有 30–50 个用户）"。
- 把 "1 in 7"（13%，参考模型）和"群体标签 <1%"（更窄的一类）混为一谈。

**时长**：2:20（20 + 35 + 55 + 30）。**超时就砍**：第 7 页只留 "1 in 7"；第 9 页只留 "same quantity" 一句。

## ④ Xu Ruicong：模拟、可察觉性、报告与决策（第 10–12 页，约 1:50）

**板块核心目标**：展示"如果有这些操作，长期会怎样、有什么代价"，"用户自己能不能发现"，并把结果变成**用户端报告的设计**（含决策规则的教训）。

**屏幕上**
- 第 10 页：报告图 4 的简化版：横轴"保留的话题量"、纵轴"偏斜的变化"，标 *Filter / Delete from history / "Not interested" (negative) / "Not interested" (as OneRec) / Watch other videos*；一句 *A filter stops when switched off; deletion persists.* 标 *Scenario*。
- 第 11 页：大数字 **6,475 issue videos → ≈ 405,000 watched**（*to notice a doubling of a rare narrative*）对比 *median user history: 493 videos*；标 *Derived*。
- 第 12 页：报告原型截图（突出 **"Not enough evidence yet"**）+ 三条教训：*① The permitted actions decide the outcome · ② Over-correction is a failure · ③ Sometimes do nothing*，标 *Proposed*。

**演讲提示**
- *Slide 10（40s）*："We can't experiment on the live app, so we built a transparent simulator whose scale is set by the measurements you just saw. At the response we measured there is hardly any skew to correct, so history-based actions change little. A filter changes the most, but only while it's on. Deleting the narrative from your history changes less but lasts. In a stronger scenario the ordering is the same. These are scenario results, not observations of a platform."
- *Slide 11（35s）*："Could a user simply notice? To see that a rare narrative has doubled, you would need about 6,500 issue videos, roughly 400,000 videos watched, about 800 times the median user's whole history. So an honest user-side tool should say 'not enough evidence yet' instead of a score, and the platform, which knows what it shows, can compute it directly."
- *Slide 12（35s）*："So what should a report do? Three lessons from our decision rule. One: which action wins depends on which actions the platform really offers; 'not interested' helps only if built as negative feedback. Two: pushing too hard overshoots, leaving you with *less* of a narrative than exists, which is its own distortion. Three: sometimes the right answer is 'no action needed'. Dingcheng will now show all of this on one real case, marriage and family."

**技巧**：先说为什么模拟（不能在 App 上做实验），再看图，只指 3 个点；第 11 页用对比让数字有感觉（405,000 vs 493）；"过度纠正"讲成直觉："you can end up with less of it than there should be"；第 12 页三条教训各一句。

**坑**：把模拟说成"实验证明过滤最好"；6,475（议题视频数）与 405,000（观看总数）混淆；说"用户永远无法察觉"（应说"对这个稀有叙事需要远超一般用户历史的样本"）；把报告原型说成已实现（它是 mock-up，数字里用户部分是编的）。

**时长**：1:50（40 + 35 + 35）。**超时就砍**：第 10 页保留"过滤只在开着时有效 / 删除会持续"；第 12 页保留教训 ②③。

## ⑤ Zhao Dingcheng：婚恋与家庭案例研究 + 总结（第 13–15 页，约 2:00）

**板块核心目标**：把前面所有抽象想法**落到我们仓库里真实做过的一个案例上**（婚恋与家庭），并用三句话收束全场。这是"从想法到数据"的闭环，也是全场结尾，必须干脆。

**屏幕上**
- 第 13 页 "Case study: marriage and family"：左：为什么选它（*the largest everyday-issue domain: 1.8% of exposure; 17% carry an opposing narrative*，*Measured*）；中：数据规模（15 个婚恋家庭关键词，260,566 个视频，占曝光 2.0%；中位用户一生只看到 8 条）；右：判断"群体标签"的**四个问题**（Who is the target? Generalised? Negative? Endorsed?）+ 一个**自编例子**（*Invented*）。
- 第 14 页 "What we found"：三个并排卡片：
  ① **Rare**：整体负面标签在婚恋视频中约 **0.2%–1%**；
  ② **Fragile labelling**：同一次提示词修改让两个模型**反向变化**（开源 4% → 51% → 13%；参考模型 1.4% → 0.6% → 1.0%），63 处分歧全部来自"对象是谁"；
  ③ **Not rewarded**：被标"群体标签"的视频点赞率 4.7% vs 其他 4.6%，看完率 27% vs 40%（*Measured*）。
- 第 15 页 "Takeaway"：三句话 + 四色图例：
  1. *Interest ≠ skew: measure both.*
  2. *What a button does depends on how it is built; the strongest lever is on the platform's side.*
  3. *A user-side report should show examples, say when evidence is thin, and let users set goals.*

**演讲提示**
- *Slide 13（35s）*："Now one real case. We chose marriage and family, the largest everyday issue in the data: about 1.8% of what users are shown, and about one in six of those videos carry a one-sided narrative. We selected videos by 15 keywords like divorce, mother-in-law, bride price: about 260,000 videos, 2% of all impressions. A typical user sees only 8 of them in their whole history. The narrative we study most closely is a negative label on a whole gender. To decide, a model answers four questions: Who is the target? Is a negative trait generalised to the group? Is it a flaw in character or motive? Does the video itself endorse it? A drama villain is not a label; 'girls these days only care about money', endorsed by the video, is."
- *Slide 14（55s）*："Three findings. One: it is rare, between 0.2% and 1% of marriage videos, depending on the sample. Two: labelling is fragile. We had a strong model and an open model label the same 500 videos. One edit to the prompt moved them in *opposite* directions: the open model went from 4% to 51% flagged, the strong one from 1.4% down to 0.6%. In the final version, the open model flagged 13% against 1%, and 94% of its flags were not confirmed. Every disagreement started at question one: it read a *topic*, 'women and money', as a *target*, 'women'. Three: the logs show no reward for this narrative. These videos are liked as often as other marriage videos, and watched to the end less. So any tilt would not come simply from users rewarding it."
- *Slide 15（30s）*："To take away three things. One, interest and skew are different, so measure both. Two, what a button does depends on how it is built, so the strongest lever is on the platform's side. Three, a user-side report should show examples, admit when evidence is thin, and let people set their goals. Everything we measured is offline and partly simulated; the rest is a design we propose. Thank you."

**技巧**
1. 第 13 页只教"四个问题"，用**一个例子**；别念关键词列表（只说 3 个）。
2. 第 14 页每个发现一句"结论 + 一个数字"；"反向变化"这个故事用**手势**（一个向上、一个向下）。
3. 94% = 1 − 6% 的精确度；也可以只说 "only 6% of its flags were confirmed"，更稳。
4. 结尾三句话**背熟**，放慢，抬头，说完 "Thank you" 就停。
5. 一句话伦理声明（可在第 13 页或第 14 页带过）："our definition counts a negative label on *any* gender and judges no position on marriage."

**坑**
- 把参考模型说成"人工金标准"（它也是模型）。
- 把"0.2%–1%"说成"确定的发生率"（它依赖样本与提示词）。
- 把"没有被奖励"说成"算法没有放大"——这里只说**用户没有用互动奖励它**；放大要看 OneRec 的结果。
- 把案例讲成"婚恋现象评论"：我们不评价任何婚恋立场。
- 结尾发散，加新观点；或在最后一页没有区分"已测"和"提议"。

**时长**：2:00（35 + 55 + 30）。**超时就砍**：第 13 页的关键词和例子之一；第 14 页卡片 ③ 只说一句。第 15 页三句话**不可砍**。

# 4 全场时间与交接表

| 时间 | 谁 | 内容 | 交接句 |
|---|---|---|---|
| 0:00–1:50 | Fu Yitong | 问题、例子、gap、研究问题 | "…Wang Junbo will show how we make this measurable." |
| 1:50–3:50 | Wang Junbo | 兴趣 vs 偏斜；目标→行动 | "…Li Yitong will now show what we actually built and tested." |
| 3:50–6:10 | Li Yitong | 真实原型；1/7；OneRec；动作能动什么 | "…Xu Ruicong will show how this plays out over thousands of videos." |
| 6:10–8:00 | Xu Ruicong | 模拟；可察觉性；报告与决策 | "…Dingcheng will now show all of this on one real case." |
| 8:00–10:00 | Zhao Dingcheng | 婚恋与家庭案例；总结 | "Thank you." |

**换人动作**：下一位在上一位说最后一句时已走到站位；交接句说完点头让位，不多说"好的"；翻页由当前讲者负责（或彩排时固定一人）。

# 5 彩排与提交安排（11-14 → 11-17）

1. **11-14（今天）**：确认分工与页码；每人读完自己对应的期末报告章节（Fu：§1–2；Wang：§3、§7；Li：§4、§5.2、§6.1；Xu：§6.2–6.4、§7；Zhao：§5.2–5.4、附录 A.3–A.4、§10）；把 cue lines 改成自己的话。
2. **11-15**：期末报告提交；完成幻灯片初版；**每人独立计时**自己的板块（±10 秒）。
3. **11-16**：全组连续彩排 2 次（手机计时、带交接），目标 9:30–9:50；检查每页姓名；**当天提交 Moodle**（.pptx 或 PDF），之后只改格式。
4. **11-17 17:30 前**：到场测试投影、字体、翻页；每人带一张 cue card，不带逐字稿。

**Delivery 通用要点（个人 30%）**：语速比平时慢，数字后停半秒；抬头看老师和后排；每页以"看图 → 一句结论"开头；手势只用来指图和比较；不用 "um / so basically / 就是说"；卡壳就回到本页的一句结论。

# 6 没有 Q&A，所以要提前回答的问题

| 听众会想 | 在哪一页回答 |
|---|---|
| 这和普通"话题多样性"有什么区别？ | 第 2、4 页 |
| 你们用了真数据吗？ | 第 6 页 |
| 标注靠 AI，可靠吗？ | 第 7 页预告，第 14 页详述 |
| 推荐器真的会放大吗？ | 第 8 页（含负面结果） |
| 按钮能解决吗？ | 第 8–10 页 |
| 用户自己能发现吗？ | 第 11 页 |
| 哪些做了，哪些只是设想？ | 第 6、12、15 页 |
| 这个案例是不是在评价婚恋观？ | 第 13–14 页的一句话声明 |

# 7 超时时的统一砍法（彩排时练）

| 优先级 | 砍什么 | 省 |
|---|---|---|
| 1 | 第 3 页 "Audits"；第 7 页五域小条形图 | ~15s |
| 2 | 第 9 页表格，只留一句；第 13 页例子之一 | ~15s |
| 3 | 第 10 页缩到两点；第 12 页只留教训 ②③ | ~20s |
| **不可砍** | 第 2 页例子；第 5 页"目标 + 可说无可行方案"；第 8 页"按钮反向"；第 14 页"标注脆弱"故事；第 15 页三句话 | – |

# 附：幻灯片与期末报告的对应

| 汇报页 | 报告章节 | 证据类型 |
|---|---|---|
| 2–3 | §1、§2 | – |
| 4 | §3.1–3.2 | 推导 + 示意例子 |
| 5 | §3.3–3.6、图 1 | 设计 + 推导 |
| 6 | §5.1、§8.1 | – |
| 7 | §5.2、表 1 | 实测 |
| 8 | §6.1、表 3 | 实测 |
| 9 | §4 命题 1–5 | 推导 |
| 10 | §6.2、图 2、图 4 | 模拟情境 |
| 11 | §4.5、§6.3、图 3 | 推导 |
| 12 | §6.4、§7、图 5 | 设计提议 + 模拟 |
| 13 | §5.1–5.2、附录 A.3 | 实测 + 定义 |
| 14 | §5.3–5.4、表 2、附录 A.4 | 实测 |
| 15 | §10、§8 | – |
