# 生成式 AI 使用记录

### 2026-11-07 · Xu Ruicong · Codex（GPT-6）· 中心化修订及继续任务
- 确切追加提示词：`继续给我完成之前的任务`
- 输入依据：PR #4 第二轮 review，要求 A=c(1-s)、B=-cs，并核查中性用户与单调性。
- 用途：修改并实际重跑 R2，准备按新版模型继续 R3–R5；图表只有实际执行结果才使用。

最终报告必须声明：用了什么工具和模型版本、影响报告哪些部分、生成入稿内容的**确切提示词**。所以从现在起，**凡是 AI 生成的内容进入了报告**（文字、表格、图、代码画出的图也算，后来改过的也算），就在这里记一条。只用于头脑风暴、没有内容进入报告的，可以不记。

格式：

```
### 日期 · 记录人 · 工具与模型
- 用途：……
- 影响的报告部分：……
- 确切提示词：（原样粘贴；多轮对话贴出生成入稿内容的那几条）
- 输出如何使用：（直接采用 / 修改后采用 / 只采用了思路）
```

## 已有记录

### 2026-11-04 至 11-07 · Li Yitong · Claude Code（Claude Opus 5.5）
- 用途：一段很长的对话，用于研究设计与数据分析。主要阶段：根据老师反馈重新设计研究问题（v4、v5、v6）；推导定义与命题；编写并运行可行性实验脚本；检索并核实文献；撰写计划、任务说明和进度记录。
- 影响的报告部分：第 3 节的定义与命题、第 4–5 节使用的实验脚本与数字、相关研究的文献核实（入稿文字待写作阶段补记）。
- 确切提示词：写作阶段把生成入稿内容的提示词逐条补在下面。
- 输出如何使用：思路与实验结果经讨论后采用；脚本在服务器上实际运行，数字来自运行结果。

### 2026-11-05 至 11-07 · Li Yitong · Qwen3-30B-A3B-Instruct-2507（本地 vLLM 推理）
- 用途：作为研究方法的一部分，给视频描述标注议题、叙事类型等属性（不是写报告）。
- 影响的报告部分：第 4 节的叙事比例、第 5 节的标签。
- 确切提示词：见 `analysis/v5_feasibility/label_pilot.py` 和 `analysis/v6/bottom_up_sample.py` 中的 `SYSTEM` 与 `TEMPLATE`，报告附录会原样列出。
- 输出如何使用：作为标签；准确率用更强的前沿模型交叉核查（任务 D3）估计后使用。

### 2026-11-07 · Zhao Dingcheng · Claude Code（Claude Opus 5.5）
- 用途：按任务 D1、D2 起草叙事类型定义和 v1 标注提示词；之后按同一条指令继续做 D3–D6，入稿时在下面补记。
- 影响的报告部分：第 4 节对叙事类型和标注方法的描述（定义与提示词会进附录）；间接影响所有用 v1 提示词得到的标签和比例。
- 确切提示词：
  > 你是 Zhao Dingcheng 的研究助手，在 COMP1110 小组项目仓库 github.com/Lyt060814/anti-filter-bubble 上工作。
  >
  > 开始前按顺序阅读：CLAUDE.md、docs/tasks/README.md、docs/tasks/zhao_dingcheng.md、report/README.md，以及 docs/project-plan/research_plan_v6.md。需要定义和命题细节时，再看 docs/project-plan/research_plan_v5.md 的第 4 节。
  >
  > 你的任务是 zhao_dingcheng.md 里的 D1–D6，按这个顺序做：
  > 1. 先做 D1（叙事类型定义）和 D2（LLM 标注提示词）。
  > 2. analysis/v6/results/dual_v0_labels.csv 出现后，做 D3 的核查分析脚本和初稿。如果文件还没出现，就先写脚本框架，用几行假数据测试。
  > 3. 然后做 D5 相关研究、D4 分类表、D6 曝光报告样稿。
  >
  > 工作规则：
  > - 先从 main 新建分支 dingcheng/d1-d2，在分支上工作；每完成一项就提交、推送，并用 gh pr create 开 PR 到 main，标题带任务编号。不要直接推送 main。
  > - 只改 analysis/v6_annotation/ 和 report/sections/ 里分给你的文件（2、4、6 节）。
  > - 仓库是公开的：不提交任何视频描述原文、账号或密钥。不做人工标注，标注全部交给 LLM。
  > - 报告小节用英文写；内部说明文件用中文。只引用核实过的文献；新加文献要写全作者、年份、出处，并核实过。
  > - 每张图表都要保存原始数据，加一个 .meta.json，并在 report/figures.md 登记。
  > - 你生成并进入报告的内容，要在 report/ai_use_log.md 记下模型和原样的提示词。
  > - 每完成一项实质性工作，在 report/contributions.md 的 Zhao Dingcheng 名下加一行。
  >
  > 遇到需要决定或有疑问的地方，写在 PR 描述里，不要自己改动别人的部分。先告诉我你的计划，再开始 D1。
- 输出如何使用：Claude 起草定义、例子和提示词，Zhao Dingcheng 审阅后采用（审阅后在此补记修改情况）。例子都是编写的，不来自视频描述。
- D3（同一会话）：确切提示词为"开始 D3"。Claude 编写并运行 `agreement.py`，起草 `agreement.md` 的数字与解读；数字来自脚本对 `dual_v0_labels.csv` 的实际运行。分歧类型由关键词规则归类，Claude 逐条读过两个模型的依据并核对。
- D5（同一会话）：确切提示词为"开始 D5"。Claude 根据仓库内已核实的文献笔记（`docs/project-plan/references_verified.md`、`docs/research/`）起草第 2 节英文全文和参考文献条目；新增文献的作者、年份、出处和页码通过 Crossref API 与 arXiv 页面核实。影响报告第 2 节和第 9 节的参考文献。输出如何使用：待 Zhao Dingcheng 审阅后补记。
- D4（同一会话）：确切提示词为"开始 D4"。Claude 编写并运行 `taxonomy.py`，起草第 4.2、4.3 节英文全文；表 4.1 由脚本生成，4.3 的数字来自 D3 的 `agreement_v0.json`。"典型争论"是 Claude 根据 LLM 给出的议题名编写的示意，不来自视频描述。影响报告第 4 节。输出如何使用：待 Zhao Dingcheng 审阅后补记。

### 2026-11-07 · Xu Ruicong · Codex（GPT-6；本会话未提供更细模型版本）
- 用途：实现、执行和检查 R1–R5；生成模拟图、样本量计算和英文模拟小节。
- 影响的报告部分：第 5 节模拟与察觉部分，F-R2、F-R3、F-R3P、F-R4，以及运行截图。仅最终实际产出入稿；没有复测 OneRec 或真实数据。
- 确切提示词（原样）：

```text
你是 Xu Ruicong 的研究助手，在 COMP1110 小组项目仓库 github.com/Lyt060814/anti-filter-bubble 上工作。

开始前按顺序阅读：CLAUDE.md、docs/tasks/README.md、docs/tasks/xu_ruicong.md、report/README.md，以及 docs/project-plan/research_plan_v6.md 和 docs/project-plan/research_plan_v5.md 的第 4 节（定义与命题 0–4，尤其是命题 2 和 4）。

你的任务是 xu_ruicong.md 里的 R1–R5：用 Python（numpy、matplotlib）实现透明推荐模型的模拟，并完成察觉所需样本量的计算。不需要任何数据或 GPU。按这个顺序做：
1. 先做 R1：在 analysis/v6_simulation/ 实现模型，通过两项自检（c=0 时 V 不增长；一步更新的 ΔV 与命题 2 的一阶公式相符）。
2. 然后做 R2 形成、R3 逃离（十种策略，含"不感兴趣"负向和 OneRec 式反向两种实现，以及停止后的持续性）、R4 察觉。
3. 最后做 R5，写报告的模拟小节。

工作规则：
- 先从 main 新建分支 ruicong/r1-model，在分支上工作；每完成一项就提交、推送，并用 gh pr create 开 PR 到 main，标题带任务编号。不要直接推送 main。
- 只改 analysis/v6_simulation/ 和 report/sections/5_case_study.md 里的模拟部分。
- 所有参数都是情境假设：要在代码和图注里标明，并按任务说明做参数扫描（c/t 从 0 到 1，θ 取 0、0.5、1、2，每个设定 20 个随机种子，报告均值和 95% 区间），不要只报一个值。需要用到的实测数字（c/t 约 0.15 和 0.59、议题占比中位数 1.6%、p90 3.6%、OneRec 里"不感兴趣"约为中性提及效果的 78% 且方向为正）都写在任务说明里，引用时注明出处。
- 每个设定、每个种子的结果都存成 CSV；每张图配一个 .meta.json（参数、种子、脚本、git 提交号、证据类型）；图存 PNG（300 dpi）和 PDF 两种，并在 report/figures.md 登记；放一张运行输出的截图到 report/screenshots/。
- 报告小节用英文写。你生成并进入报告的内容，要在 report/ai_use_log.md 记下模型和原样的提示词；每完成一项实质性工作，在 report/contributions.md 的 Xu Ruicong 名下加一行。
- 仓库是公开的：不提交任何密钥或数据原文。

遇到需要决定或有疑问的地方，写在 PR 描述里。先告诉我你的计划和模型的具体实现方式，再开始 R1。
```

- 输出如何使用：代码实际运行；图和英文模拟小节作为初稿，等待 Xu Ruicong 与组员审阅。参数、分类器质量与种子人群为情境假设，实测锚点只引用仓库记录。


### 2026-11-07 · Xu Ruicong · Codex（GPT-6）· R2 审阅修改
- 用途：按 PR #4 的 review 修正形成模拟，暂不更新报告结论。
- 确切追加提示词：
```text
你重新把前面几个提一下pr
这是一个三个人的合作项目，所以你要不定期看一下groupmate的进展和comment
```
- 附加依据：PR #4 于 2026-11-07 的 CHANGES_REQUESTED 审阅；四项要求和选取方案逐项保存在本 PR 描述与 bounded_formation.py。
- 输出如何使用：实际运行；供给参照总偏斜不再称为平台参照个人偏斜，R3–R5 待 R2 合并后重跑。
