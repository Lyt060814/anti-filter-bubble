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
| 4 | Interest is not skew | Wang Junbo | 0:55 | m 与 V 两个量；实测三层分解 4.1% → 6.2% → 12.7%（*Measured* · 报告 §5.1） |
| 5 | What each action can move | Wang Junbo | 1:05 | 命题 1–4 三卡（ΔV = η·c / ΔV = 0 / 过滤器）+ 底部一句"平台层 Λ 用户操作够不到" |
| 6 | How common are one-sided narratives? | Li Yitong | 0:20 | 三个点阵数字：7.9% / 1 in 5（18.4%）/ 6.2%（*Measured*） |
| 7 | Split the lean in two | Li Yitong | 0:35 | 平台层 Λ 与个人层 V<sub>u</sub> 示意（论文风） |
| 8 | Does a recommender amplify a narrative? | Li Yitong | 0:55 | OneRec 三个结果：话题 +1.01、叙事 +0.67、"not interested" 反向 |
| 9 | Same topic share. Twice the odds. | Li Yitong | 0:30 | 三层分解 + 探针条形 + 90 天形成曲线（*Measured / Scenario*） |
| 10 | How much of the topic survives? | Xu Ruicong | 0:40 | 逃离策略表：personalisation off −0.78 / scroll −1.11 / delete −1.12 / filter −2.56；保留话题 8%/93%/93%/90%（*Scenario · Table 5*） |
| 11 | The reference is the bottleneck | Xu Ruicong | 0:35 | 两条曲线（自己 feed 9 天 vs 参照 114 天）+ ≈490 条/样本（*Derived · Eq. 6*） |
| 12 | What should an exposure report show? | Xu Ruicong | 0:35 | 报告内容：29.8% 话题、12.7% vs 6.2%、证据是否足够、选项表（*Proposed · Fig. 10*） |
| 13 | Same topic, narrower view | Zhao Dingcheng | 0:35 | 两个用户各 100 格：话题都是 30%，群体标签 6% vs 13% |
| 14 | 490 videos to notice. A button that feeds it. | Zhao Dingcheng | 0:55 | 490 + 17 天尝试的逃离表（报告 Table 5）+ 三条结论 |
| 15 | What is solid, what is not | Zhao Dingcheng | 0:30 | Measured / Scenario / Not shown 三卡 + 收束句 |

> ⚠️ **待定（需要 Zhao 确认）**：Xu 的新第 10–11 页已经讲了逃离策略表和 490 条门槛，而 Zhao 现在的第 14 页 "490 videos to notice. A button that feeds it." 是同一批数字（逃离表 + 9 天/114 天），会重复。建议把第 14 页换成案例的三个发现：①群体标签带来最多互动（评论 1.85×）但同时被点"不感兴趣"最多（2.4×）；②曝光超供给（6.2% vs 4.1%，平台层）；③无人工标注，靠双强模型参照验证（κ 0.74–0.81）。

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

**板块核心目标**：讲清两个量——**兴趣 m（话题占比）与观点偏斜 V（话题内部一种说法多出现的程度）**——并用**实测的三层分解**（supply → 平台层 Λ → 个人层）说明"同一个话题、更窄的视角"；再用**命题 1–4** 回答"每类操作能动到什么、够不到什么"：反馈能造也能拆、话题级控制动不了话题内部的配比、过滤器不依赖推荐器、**平台层 Λ 任何用户操作都够不到**。

> 注：旧方案的"用户确认目标（减少/保留/探索）+ 按效果·损失·成本选操作 + 可回答'无需操作 / 没有可行方案'"框架**最终报告里没有**，已从幻灯片和本方案中删除（见 `presentation/README.md` 的对应说明）。

**屏幕上**
- 第 4 页：两张并列卡片：*Interest = how much of my feed is this topic*；*Skew = inside the topic, how much more one narrative shows up than it should*。下方案例条（*Measured* · 报告 §3.3 / §4.1）：`supply 4.1% → platform layer +0.44, 6.2%（1.55× supply，shared by everyone）→ personal layer +0.79, 12.7%（most skewed tenth of heavy viewers, 2.2× platform odds）`；底部一句 *together 3.4× supply*。
- 第 5 页：三张命题卡（*01 · Feedback · Prop. 1: ΔV = η·c*，可口头带一句 OneRec 实测：叙事响应约为话题响应的 2/3（§4.2）；*02 · Topic controls · Prop. 2: ΔV = 0*；*03 · Filters · Prop. 3: ΔV = log((1−TPR)/(1−FPR))*）+ 底部整宽一句：*No user action reaches the platform layer Λ — it is added for everyone, before any personalisation (Prop. 4)*。

**演讲提示**（与 `slides.html` 的 NOTES 一致，以 NOTES 为准）
- *Slide 4（55s）*："Two numbers describe a feed. Interest is how much of it is about the topic. Skew is what you see once you're inside the topic — how much more often one narrative shows up than it should. A topic lover has high interest and ordinary skew; a cocoon is high skew, whatever the interest. Our case study, measured in the logs: a gender group label is 4.1% of the marriage videos on offer. Ranking alone lifts it to 6.2% — the platform layer, 1.55 times supply, shared by everyone. The most skewed tenth of heavy viewers see 12.7% — personalisation adds 2.2 times the odds again. Together, 3.4 times supply. The platform layer belongs to everyone; the personal layer is yours — and that is the part a user can act on."
- *Slide 5（65s）*："So what can each action actually move? Four propositions. One: any feedback moves your skew in proportion to one quantity — how sharply the recommender separates the narrative from the rest of the topic. The same quantity builds a cocoon and takes it apart. In OneRec it is measured, not assumed: the model separates the narrative about two-thirds as sharply as it separates the topic. And the sign of 'not interested' is the platform's choice: in a recommender trained on logged behaviour, the button is read as interest. Two: topic-level controls — 'show less of this topic', every category-based cocoon check — hit all videos in the topic equally, so they cannot change the mix inside it; the skew only falls because the topic does. Three: a filter acts on what reaches the screen, so it is the one action that needs no cooperation from the recommender. Four: no user action reaches the platform layer — it is added for everyone, before any personalisation. Li Yitong will now show what we actually built."

**技巧**：第 4 页用手势把两个量分左右；"platform layer / personal layer"一句话："the first is shared by everyone, the second is yours"；第 5 页按 01→02→03 讲，最后用底部那句收束（这是第 4–5 页唯一要背下来的结论）；提到 "not interested" 时强调"**它的符号是平台决定的**——在这个模型里被当成兴趣"；数字都按报告口径讲（整份报告是理想化项目、数据是构造的，如被问到如实说明）。

**坑**：把 4.1/6.2/12.7 讲成"我们真实跑快手 App 的结果"（是公开日志 + 开源模型的理想化情景）；术语（log-odds、entropy）；把命题讲成一堆公式框（每张卡只留一句白话）；忘了收束句"平台层够不到"；交接对象说成 Zhao Dingcheng（**第 6 页是 Li Yitong**）。

**时长**：2:00（55 + 65）。**超时就砍**：第 5 页命题 2、3 的展开，保留 Prop 1 的"同一个量"和 Prop 4 的"平台层够不到"。

## ③ Li Yitong：真实原型 + 数据地图 + 推荐器实验与理论（第 6–9 页，约 2:20）

**板块核心目标**：（1）**单独、清楚地介绍 GitHub 上真实落地的原型**；（2）给出一张"对立叙事在哪里"的数据地图；（3）回答"推荐器会放大吗？按钮管用吗？"；（4）用一句核心洞察串起来：**让推荐器能形成茧房的量，也正是让用户能解开茧房的量**。这是全场信息量最大的部分，**只讲结论**。

**屏幕上**
- 第 6 页：三个点阵数字——`7.9%` of impressions touch a social issue；`1 in 5`（18.4%，16.6–20.4）issue impressions carry an opposing narrative；`6.2%` of gender-&-marriage impressions carry a negative label on a whole gender（supply 4.1%）。标 *Measured*。
- 第 7 页：论文风一页：平台层 *what exists and how it is ranked*；个人层 *what your history adds*；底部 `total skew = Λ + V_u · ΔV = η·c`，以及"你的按钮只够到内层"。
- 第 8 页：OneRec 三行结果：话题 **+1.01**（每 10 条议题视频）；叙事 **+0.67**（≈话题的 2/3）；"not interested" 反向（叙事 **+0.29**、话题 +0.39）。标 *Measured · OneRec-1.7B*。
- 第 9 页：三层分解 4.1% → 6.2%（+0.44，×1.55）→ 12.7%（+0.79，×2.2，合计 ×3.4）+ 探针条形（+1.01 / +0.67 / −0.05）+ 90 天形成曲线（她 +0.78 vs 随意观众 +0.09）。标 *Measured / Scenario*。

**演讲提示**
- *Slide 6（20s）*："First, what is out there? About 8% of what users are shown touches a social issue; within those areas about one impression in five carries an opposing narrative — 18.4%. Our case study is the sharpest form: a negative label on a whole gender, 4.1% of the supply on marriage and 6.2% of what is shown."
- *Slide 7（35s）*："Where does the lean come from? It splits in two: a platform layer — what exists and how it is ranked — the same for everyone, and a personal layer built by your history. Your buttons only reach the inner one."
- *Slide 8（55s）*："We tested whether a real recommender amplifies. We used OneRec, trained by Kuaishou on this log, changed one user's history in one controlled way, and measured what it recommends next. Topics respond strongly: ten issue videos add about one log-odds. The narrative responds too — two-thirds as much, far outside the random range, so this model does tell the narrative apart. And 'not interested' goes the wrong way: it raises the narrative instead of lowering it."
- *Slide 9（30s）*："One probe is one step; weeks of use need a simulation, with its scale set by that probe. A heavy viewer of one narrative ends at twice the odds while her topic share never moves — same topic, narrower view, built in weeks. Xu Ruicong will show what it takes to get out, and whether she could notice."

**技巧**
1. 每页只说**一个结论**，数字不超过 2 个；表格不逐行念。
2. 第 8 页逐个结果用同一句式 *We did X → the model did Y*；先讲"怎么测"（改一次历史，量一次变化）。
3. **主动讲"按钮反向"**：这是诚实和思考的加分点；但别再讲"叙事≈0"，最终报告里叙事响应是话题的 2/3。
4. 命题只讲一句话版本；公式留在报告。
5. 明确"这是开源模型，不是快手 App 里的推荐器"。
6. 彩排时**计时每页**，第 6 页和第 9 页必须守住 20s/30s，否则会拖垮后面的人。

**坑**
- 时间失控（4 页 2:20 很紧）；多讲了标注方法（留给第 6 页一句带过）。
- 说"证明快手的'不感兴趣'失效"——只能说"在这个开源模型里反向"。
- 把 4.1/6.2/12.7 讲成"我们真实跑快手 App 的结果"（公开日志 + 开源模型的理想化情景）。
- 把 18.4%（叙事在议题曝光中的占比）和 6.2%（群体标签在婚恋曝光中的占比）混为一谈。
- 把形成曲线（+0.78）说成实测——它是模拟情境，尺度来自探针。

**时长**：2:20（20 + 35 + 55 + 30）。**超时就砍**：第 6 页只留 1 in 5；第 9 页只留"同话题、更窄视角"一句。

## ④ Xu Ruicong：模拟、可察觉性、报告与决策（第 10–12 页，约 1:50）

**板块核心目标**：展示"如果有这些操作，长期会怎样、有什么代价"，"用户自己能不能发现"，并把结果变成**用户端报告的设计**（含决策规则的教训）。

**屏幕上**
- 第 10 页 "How much of the topic survives?"：START V = +0.78，3,000 条视频 / 约 17 天后，四行策略表（personalisation off −0.78 / scroll past −1.11 / delete then scroll −1.12 / classifier filter −2.56）+ 保留话题条形（8% / 93% / 93% / 90%）；底部 *Deleting first reaches about the same reduction in 3 days versus 2 weeks of scrolling alone. Old habits bring the skew back.* 标 *Scenario · Table 5 / Figure 9*。
- 第 11 页 "The reference is the bottleneck"：两条曲线（viewing days log scale vs narrative odds to detect）；右栏 ≈490 条/feed、≈114 天（参照 · 关个性化）、≈9 天（自己 feed · 话题粉）；脚注 6.2% baseline · 79% recall · 1% FP · 5% sig · 80% power。标 *Derived · Eq. 6 / Figure 8*。
- 第 12 页 "What should an exposure report show?"：左 29.8% 话题、your feed 12.7% vs personalisation off 6.2%、证据是否足够（1,610 条）、"Not enough evidence yet"；右 options 表（scroll past / filter，ΔV 与保留话题）；底部 *The reference reveals personal skew. A catalogue comparison is needed to see the skew shared across the platform.* 标 *Proposed · Fig. 10*。

**演讲提示**
- *Slide 10（40s）*："So what actually gets her out? We ran the measured tilt forward 3,000 videos, about 17 days, and tried the actions a user really has. Personalisation off removes the whole personal layer −0.78 but costs the topic: 8% of it survives. Scrolling past the narrative works −1.11 and keeps 93%, but only while she keeps it up. Deleting first then scrolling reaches the same in three days instead of two weeks. A classifier filter is strongest, −2.56, while it is on. And old habits bring the skew back: about half the reduction disappears within a week."
- *Slide 11（35s）*："Could she notice on her own? To detect double the odds she needs about 490 labelled issue videos in each of two feeds. Her own feed reaches that in nine days; a feed with personalisation off needs about 114 days. The reference is the bottleneck, not her attention. A shared reference from the platform or a research panel would make the comparison practical."
- *Slide 12（35s）*："So what should a report show? Topic interest and the label share inside it, her own feed against a non-personalised reference, and whether the evidence is enough — if either sample is too small, it must say so. The options table shows what each action buys and what it costs. This is a proposal: the numbers in the example are simulated. Dingcheng will now explain how we defined and identified group labels."

**技巧**：先说为什么模拟（不能在 App 上做实验），再看图，只指 3 个点；第 11 页用对比让数字有感觉（自己 9 天 vs 参照 4 个月；平台公布后 6 天）；第 12 页三条原则各一句。

**坑**：把模拟说成"实验证明过滤最好"；把 490（每样本条数）与 9 天/114 天（攒够所需时间）混淆；说"用户永远无法察觉"（应说"要靠平台公布参照才现实"）；把报告原型说成已实现（它是 mock-up，用户数字是编的）。

**时长**：1:50（40 + 35 + 35）。**超时就砍**：第 10 页保留"过滤只在开着时有效 / 删除更持久"；第 12 页只留"证据不足就直说"。

## ⑤ Zhao Dingcheng：婚恋与家庭案例研究 + 总结（第 13–15 页，约 2:00）

**板块核心目标**：把前面所有抽象想法**落到我们仓库里真实做过的一个案例上**（婚恋与家庭），再用"什么成立、什么不成立"收束全场。这是"从想法到数据"的闭环，也是全场结尾，必须干脆。

**屏幕上**
- 第 13 页 "Same topic, narrower view"：两个用户各 100 格（每格 100 条视频，浅色是话题）；话题都 30%（*a cocoon check sees no difference*）；群体标签 share 6% vs 13%（*odds ×2.2*）；右侧：case 规模 **2.4%** of impressions、**24%** of them take a side（*Measured · Table 4*）+ 群体标签的一句话定义 + 一个自编例子（*Invented*）。
- 第 14 页 "490 videos to notice. A button that feeds it."：左：**490** 条/样本（自己 feed **9 天** vs 参照 **114 天 ≈ 4 个月**）；右：17 天尝试的逃离表（划过 −1.1/93%、"不感兴趣" −0.9/94%、少看该话题 −0.8 但只留 2% 话题、过滤 −2.6/90%）+ *half the gain is gone in about a week*；底部三条结论。
- 第 15 页 "What is solid, what is not"：Measured / Scenario / Not shown 三卡 + 收束句 *a user cannot easily see or undo skew inside a topic; the platform is better placed to measure and correct it.*

**演讲提示**
- *Slide 13（35s）*："Now one real case: gender and marriage — 2.4% of all impressions, and a quarter of those videos take a side. Two users follow the topic at the same rate; every square is a hundred videos, the pale ones on the topic. A cocoon check sees both at 30%. Inside, one meets 6% group labels, the other 13%: same topic, twice the odds. To decide what counts as a label, a model asks one question — is a negative trait generalised to a whole gender, and does the video itself endorse it?"
- *Slide 14（55s）*："Could she notice? About 490 labelled issue videos per sample: nine days on her own feed, four months for a reference feed. And getting out costs: scrolling past −1.1, the button −0.9 because the model reads it as interest, 'show less of this topic' −0.8 but it takes the topic with it, a filter −2.6 only while it is on. Stop, and half the gain is gone in a week. Three things: counting topics cannot see this; escape is a habit, not a button, and today's button feeds the tilt; only the platform sees it without months of counting."
- *Slide 15（30s）*："What is solid: the prevalence and the recommender's response — measured. How a cocoon forms and what escape costs — scenario. What we cannot show: any effect on the real app, or on what people believe. Thank you."

**技巧**
1. 第 13 页只教"一句话定义"，用**一个例子**（"Women today only look at the bride price"，视频自述的才算）；别说"四个问题"清单。
2. 第 14 页每个发现一句"结论 + 一个数字"；"按钮反向"用**手势**（往下按、数字往上）。
3. 结尾把"measured / scenario / not shown"分清楚，说完 "Thank you" 就停。
4. 一句话伦理声明（可在第 13 页带过）："our definition counts a negative label on *any* gender and judges no position on marriage."

**坑**
- 把参考模型说成"人工金标准"（它是两个更强模型的参照，不是人标）。
- 把 2.4% / 24% 说成"全部婚恋视频"的占比（它们的口径是曝光与"take a side"）。
- 把 6% → 13% 讲成"两个不同人群"——是同一话题率下的两个 feed。
- 把案例讲成"婚恋现象评论"：我们不评价任何婚恋立场。
- 结尾发散，加新观点；或在最后一页没有区分"已测"和"模拟"。

**时长**：2:00（35 + 55 + 30）。**超时就砍**：第 13 页的例子；第 14 页逃离表只留两行。第 15 页三卡**不可砍**。

# 4 全场时间与交接表

| 时间 | 谁 | 内容 | 交接句 |
|---|---|---|---|
| 0:00–1:50 | Fu Yitong | 问题、例子、gap、研究问题 | "…Wang Junbo will show how we make this measurable." |
| 1:50–3:50 | Wang Junbo | 兴趣 vs 偏斜（三层分解）；命题 1–4 | "…Li Yitong will now show what we actually built." |
| 3:50–6:10 | Li Yitong | 真实原型；1/7；OneRec；动作能动什么 | "…Xu Ruicong will show how this plays out over thousands of videos." |
| 6:10–8:00 | Xu Ruicong | 模拟；可察觉性；报告与决策 | "…Dingcheng will now show all of this on one real case." |
| 8:00–10:00 | Zhao Dingcheng | 婚恋与家庭案例；总结 | "Thank you." |

**换人动作**：下一位在上一位说最后一句时已走到站位；交接句说完点头让位，不多说"好的"；翻页由当前讲者负责（或彩排时固定一人）。

# 5 彩排与提交安排（11-14 → 11-17）

1. **11-14（今天）**：确认分工与页码；每人读完自己对应的期末报告章节（Fu：§1–2；Wang：§3、§5.1；Li：§4、§5.1、§5.2；Xu：§5.3、§6、§7；Zhao：§4、§10）；把 cue lines 改成自己的话。（章节号按最终版报告；旧方案的 §7 是设计章，最终版 §7 是 escape 成本。）
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
| **不可砍** | 第 2 页例子；第 5 页"平台层 Λ 够不到 + Prop 1 同一个量"；第 8 页"按钮反向"；第 14 页"标注脆弱"故事；第 15 页三句话 | – |

# 附：幻灯片与期末报告的对应

| 汇报页 | 报告章节 | 证据类型 |
|---|---|---|
| 1–3 | 摘要、§1、§2 | – |
| 4 | §3.1–3.2 | 实测 + 推导 |
| 5 | 命题 1–4（报告无"目标→行动"四阶段框架与决策规则） | 推导 + 实测 |
| 6 | §4.1、§5.1 开头、§7.2 | 实测 |
| 7 | §4.2、表 4.1–4.2 | – |
| 8 | §5.1、表 5.1 | 实测 |
| 9 | §3.3–3.4、命题 1–5 | 推导 + 模拟 |
| 10 | §5.2、图 5.1、附录 B | 模拟情境 |
| 11 | §3.5（命题 6）、§5.3、图 5.2 | 推导 |
| 12 | §6、图 6.1（"决策规则三条教训"报告里没有） | 设计提议 |
| 13 | §4.1、§4.2 末（案例选择）、附录 A.3 | 实测 + 定义 |
| 14 | §4.3–4.4、表 4.3–4.4、附录 A.4 | 实测 + 模拟 |
| 15 | §7.1、§7.5 | – |
