---
title: "COMP1110 小组汇报方案 v3（10 分钟 · 5 人 · 14 页）"
subtitle: "Same topic, narrower view · 按最终报告重排"
---

# 0 这一版改了什么

v3 是另起的一套幻灯片 [slides_v3.html](slides_v3.html)，沿用 v2 的视觉风格（深色胶片底、Cormorant 标题、等宽小字、印章、方格），**内容按最终报告重新编排**。v2 的 [slides.html](slides.html) 和 [plan_v2.md](plan_v2.md) 保留不动。

和 v2 相比：

| v2 的问题 | v3 的处理 |
|---|---|
| "性别标签"到第 13 页才解释，前面的数字观众不知道在数什么 | 第 2 页用开场谜题直接定义，后面所有数字都数同一种视频 |
| 4.1% → 6.2% → 12.7% 出现 5 次；探针、检测、逃离表各出现 2 次 | 每个结论只讲一次，按 RQ1 → RQ4 顺序 |
| 第 5 页整页公式（η·c、TPR/FPR、Λ），第 11 页 "80% power" | 不出现公式和统计术语；用"两个旋钮""倾斜的舞台""硬币"三个类比 |
| 没有一页讲我们怎么做的 | 第 6 页讲四种证据，第 7 页讲标注和检验 |
| 第 12 页"曝光报告" mock-up 和第 15 页 "user study of the report"，最终报告里已没有 | 删除 |
| 引用旧版报告的章节号、图号 | 删除；每页只用一个印章标证据来源（From the logs / OneRec probe / Simulation / Counting bound） |
| 屏幕上没有研究问题 | 第 3 页列出四个 RQ，底部进度条全程高亮当前 RQ |
| "不感兴趣"反向这个最有意思的结果埋在表里 | 第 9 页埋下（探针），第 12 页收回（逃离），第 14 页变成平台该做的事 |
| 计时 10:00，没有余量 | 9:30，留 30 秒 |

**数字口径**：所有数字和结论都取自最终报告（`report/latex`，由 `figures/src/study.py` 生成的 `generated/numbers.tex` 和 `results.json`）。第 10、13 页的曲线直接用报告模拟的数据，不是手画的。幻灯片里不出现关于研究性质的说明，和报告一致。

# 1 一句话主线

> 一个 feed 可以保留你喜欢的话题，却让你看到的观点越来越偏。偏斜一部分来自平台、人人都有；另一部分来自你自己的观看，你能把它降下来，但只有一直坚持才行。

全场只教**一个新概念**（兴趣 ≠ 偏斜），只跟**一种叙事**（把负面特征安在整个性别上的"性别标签"），只用**一种说法讲比例**（"每 N 条一条"），每页只有**一句结论**作标题。

# 2 逐页大纲

| 页 | 讲者 | 时长 | 标题 | 屏幕上 | 印章 |
|---|---|---|---|---|---|
| 1 | Fu | 0:15 | Viewpoint Cocoons | 标题、五人姓名 | – |
| 2 | Fu | 0:50 | Same topic. Which feed is a cocoon? | 两个 100 格 feed：婚恋都占 30%（茧房自测同分）；里面性别标签 1/16 对 1/8。右侧定义和两个例句 | 小字注明 feed 为示意，比例来自日志 |
| 3 | Fu | 0:35 | Today's checks count topics, not views | 三条"别人测什么"被划掉 → "我们测什么"；底部四个 RQ | – |
| 4 | Wang | 0:35 | Interest and skew are two different dials | 二维图：横轴兴趣、纵轴偏斜；Feed A、B 同兴趣不同偏斜；茧房自测只读横轴 | – |
| 5 | Wang | 0:45 | Part of the tilt is everyone's. Part is yours. | 同心圆 + 三级台阶：1/24（供给 4.1%）→ 1/16（平台层 6.2%）→ 1/8（个人层 12.7%）；按钮只够到内圈 | From the logs |
| 6 | Wang | 0:30 | Four ways into a closed recommender | 数据（160,412 用户、7,530 万曝光）→ 标注 → 四种证据（日志、探针、模拟、计数），各标对应 RQ | – |
| 7 | Zhao | 0:45 | One model labels, two stronger ones check | 四类对立叙事各一句例句（附报告类型名）；群体标签四个条件，反驳不算；DeepSeek + GPT 复核 1,200 条，κ 0.78；漏标 21% 的群体标签、在其他视频里误标 1%，已校正 | – |
| 8 | Zhao | 0:50 | One in five takes a side, and ranking favours them | 1 in 5（18.4%）点阵；评论 ×1.85、分享 ×1.33、"不感兴趣" ×1.74（相关，不只是认可）；五个议题域展示/供给几率 ×1.18–1.49；性别标签一行小字回指第 5 页 | From the logs |
| 9 | Li | 0:55 | Change a history, and the recommender follows | 示意：换入 10 条 → OneRec → 下一步推荐；话题 +1.01、叙事 +0.67、随机 ≈0；框：标"不感兴趣"叙事仍 +0.29 | OneRec probe |
| 10 | Li | 0:45 | Three months: same topic, twice the odds | 模拟曲线：话题粉几率 24 天到一半、89 天翻倍；话题占比平在 30%；随意观众几乎不动 | Simulation · 400 users |
| 11 | Xu | 0:45 | To notice it, you need a second feed | 硬币类比；490 条/每个 feed；自己 9 天 / 无个性化参照 114 天 / 平台公布参照 6 天（310 条） | Counting bound |
| 12 | Xu | 0:55 | Every way out has a price | 散点：横轴保留话题、纵轴去掉偏斜，11 种策略，点名 5 种；三条结论 | Simulation |
| 13 | Xu | 0:25 | … and nothing lasts | 4 条轨迹：行动 17 天后停止，全部回升；一周内少一半 | Simulation · 400 users |
| 14 | Fu | 0:40 | Keep the topic, widen the view | 用户能做什么 / 只有平台能做什么；一行证据来源与边界；收束句 | – |

**各人时长**：Fu 2:20（1–3、14）· Wang 1:50（4–6）· Zhao 1:35（7–8）· Li 1:40（9–10）· Xu 2:05（11–13）。合计 **9:30**。

分工依据报告附录 A 的贡献表：Fu 做问题定义与用户控制综述，开场和收尾；Wang 一直负责"兴趣 vs 偏斜"；Zhao 定义叙事类型和群体标签规则、做双模型一致性分析；Li 做 OneRec 探针；Xu 做模拟、逃离和检测样本量。

# 3 讲稿要点（English cue lines，用自己的话说；完整版在幻灯片里按 N 查看）

**Fu Yitong（1–3）**
- *2*："Two feeds, both thirty percent marriage. A cocoon check gives them the same score. Look inside: feed A meets a gender label one video in sixteen, feed B one in eight — twice the odds. Feed B kept the topic and narrowed the view. That is a viewpoint cocoon."
- *3*："Today's checks count topics. Viewpoint studies look at politics, from outside. Button studies count what a button removes, not what it costs. Four questions: how common, how it forms, can you notice, can you get out. Wang Junbo."

**Wang Junbo（4–6）**
- *4*："Two dials: interest and skew. A cocoon is high skew, whatever the interest. A cocoon check reads only the horizontal axis."
- *5*："A stage tilted for everyone, and a person who leans further. One in twenty-four on offer, one in sixteen shown to everyone — the platform layer — one in eight for the most skewed tenth of heavy viewers — the personal layer. Every button reaches only the inner ring."
- *6*："We cannot open the app, so four ways in: logs, a model trained on them, a simulation, and a counting bound. Zhao Dingcheng."

**Zhao Dingcheng（7–8）**
- *7*："One open model reads every description. A group label needs all four: a whole gender, a negative trait, all or most, in its own voice; rebuttals don't count. Two stronger models relabel twelve hundred videos; kappa 0.78; we correct for the errors that remain. Either gender counts; we take no side on marriage."
- *8*："One issue video in five takes a side. Nearly twice the comments, but also more 'not interested': attention, not simply approval. And ranking shows them more often than they exist, in every issue area, up to one and a half times the odds. What does a user's own history add? Li Yitong."

**Li Yitong（9–10）**
- *9*："Swap ten videos into a real history and compute what OneRec recommends next. Topic +1.01, narrative two-thirds of that, chance stays at zero: the model tells the narrative apart. Remember this: mark the same videos 'not interested', and the narrative still goes up."
- *10*："A simulation driven by that response. Half-way in 24 days, twice the odds by three months, topic share flat at 30 percent. A casual viewer barely moves. Could this fan notice? Xu Ruicong."

**Xu Ruicong（11–13）**
- *11*："Like spotting a loaded coin: you need many flips, and a fair coin. 490 videos from each feed: nine days of your own, four months for the reference. Six days if the platform published one."
- *12*："Eleven ways out for seventeen days. Platform settings remove the skew by removing the topic. 'Not interested' does worse than scrolling past — each press is read as interest. A filter goes furthest without the recommender's help."
- *13*："Stop, and every curve climbs back; half the gain is gone in a week. Escape is a habit, not a button. Fu Yitong."

**Fu Yitong（14）**："A user can lower their own layer and must keep doing it. Only the platform can measure the view inside each topic, publish the reference, fix the button, and decide what ranking amplifies. We measure what people see, not what they believe. Next time a check calls your feed diverse, look inside the topic. Thank you."

# 4 讲法上的几个约定

1. **比例一律说"每 N 条一条"**：1/24、1/16、1/8。百分比只出现在小字里。
2. **只用三个类比**：两个旋钮（第 4 页）、倾斜的舞台（第 5 页）、灌铅的硬币（第 11 页）。
3. **伏笔**：第 9 页说 "remember this"，第 12 页说 "remember: each press is read as interest"，第 14 页说 "fix the button"。
4. **证据类型口头带一句**：日志里看到的 / 模型实验 / 模拟 / 计算。第 14 页底部一行总结，并说明只测曝光、不测观念。
5. **交接句**是一个问题，下一位接着回答：Fu → Wang "how we make this measurable"；Wang → Zhao "how common"；Zhao → Li "what does a user's own history add"；Li → Xu "could this fan notice"；Xu → Fu "what does this mean"。

# 5 超时时怎么砍

| 优先级 | 砍什么 | 省 |
|---|---|---|
| 1 | 第 6 页只说一句"四种证据"；第 7 页不念四类例句 | ~20s |
| 2 | 第 8 页只讲 1 in 5 和供给对展示；第 11 页去掉"平台公布 6 天" | ~15s |
| 3 | 第 12 页只讲结论 01、02 | ~15s |
| **不可砍** | 第 2 页谜题；第 5 页三级台阶；第 9 页"不感兴趣"；第 12 页"按钮不如划走"；第 14 页收束句 | – |

# 6 没有 Q&A，提前回答

| 听众会想 | 哪页回答 |
|---|---|
| 这和"话题多样性"有何不同？ | 2、4 |
| 数据从哪来？标注可靠吗？ | 6、7 |
| 推荐器真的会放大吗？ | 9 |
| 是平台的问题还是用户自己的？ | 5、8、14 |
| 用户能自己发现吗？ | 11 |
| 按钮管用吗？ | 9、12 |
| 是不是在评价婚恋观？ | 7（一句话声明） |
| 哪些来自日志、哪些来自模拟？ | 每页印章；14 |

# 7 操作与提交

- 打开 `slides_v3.html`（Chrome/Edge），按键与 v2 相同：→/空格 翻页，N 讲稿，T 计时，F 全屏。地址后加 `?static` 关闭动画，用于导出 PDF。
- 导出 PDF：Chrome 打开 `slides_v3.html?static`，逐页截图或打印；提交前检查 14 页的讲者姓名都在右上角。
- 完整演讲稿见 [script_v3.md](script_v3.md)，幻灯片里按 N 看到的讲稿由它生成。
- 修改：编辑 `v3/` 下的 `sections.html`（页面）、`enters.js`（图表）、`build.py`（计时）或 `script_v3.md`（讲稿），再运行 `python3 presentation/v3/build.py .` 重新生成。`v3/data.json` 是从报告 `results.json` 导出的模拟曲线。

# 附：幻灯片与最终报告的对应

| 页 | 报告位置 |
|---|---|
| 2、4 | §1 引言（图 1）、§2.1 两个坐标 |
| 5 | §2.2 三层偏斜；§3.3 "Ranking shows them more often…"；§4.1 日志中的个人层 |
| 6 | 图 2（研究设计）、§3.1 数据 |
| 7 | §3.2 标注流程（叙事类型表、质量表） |
| 8 | §3.3 结果 |
| 9 | §4.2 探针实验 |
| 10 | §4.3 模拟 |
| 11 | §5 检测（RQ3） |
| 12–13 | §6 逃离（RQ4）、策略表与逃离图 |
| 14 | §8 讨论、§9 结论 |
