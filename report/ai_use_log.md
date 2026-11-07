# 生成式 AI 使用记录

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
- D3 续、v2 提示词（同一会话）：确切提示词为"有一个issue assign给我了  你检查一下"和"开始做"。Claude 读取 issue #10，运行 `agreement.py` 分析 v1 结果，起草 `agreement.md` 第 5 节、`prompt_v2.py` 与 D1 定义的修订，并给 `agreement.py` 加上分层加权估计；数字来自脚本的实际运行。影响报告第 4.3 节和附录 A。输出如何使用：待 Zhao Dingcheng 审阅后补记。
