# 项目说明（给 Claude Code 和组员）

HKU COMP1110（2026/27 第一学期）小组项目，五人：Fu Yitong、Li Yitong、Wang Junbo、Xu Ruicong、Zhao Dingcheng。课题：中文短视频信息流里的**观点茧房**——用户保留议题、但看到的观点越来越偏；研究它怎样形成、用户能否察觉、如何逃离。课程只评选题和内容质量，不评代码。

## 先读什么

1. [Research Plan v6](docs/project-plan/research_plan_v6.md)：当前计划（范围、研究问题、分工、报告结构、时间线）。
2. [三人协作说明与任务](docs/tasks/README.md)：Zhao Dingcheng、Xu Ruicong、Li Yitong 各自的任务、目录、PR 流程和规则。组员开工前先读自己的任务文件。
3. [Research Plan v5](docs/project-plan/research_plan_v5.md)：定义、命题与理论细节（v6 沿用）；[交接说明](docs/context-recovery/handoff_2026-11.md)：到 11-06 为止的决策和结果。
4. [v5 可行性记录](docs/context-recovery/plan_v5_feasibility.md)：所有已跑出的数字及其脚本 [analysis/v5_feasibility](analysis/v5_feasibility/)。
5. 已提交的课程提案：[docs/project-plan/submission](docs/project-plan/submission/README.md)。v1–v4 只作历史背景。

## 工作原则

- 这是课程项目，目的是体验科研流程，不提交代码。数字要么来自实际运行，要么明确标为"情境假设"并做参数扫描；不把假设写成测量结果。
- 从第一性原理出发：先想清楚什么重要、什么可测，再选方法；不为好实现而缩小问题。
- 能实测的尽量实测（推荐器对操作的反应、叙事比例）；模拟中的情境参数要报告整条曲线，不能只给一个值。
- 结论按证据分级：模拟结果不等于线上平台效果；曝光变化不等于信念变化。
- 写作用平实的中文，少用术语和修饰；引用须核实标题、作者、年份和出处。
- 改动通过检查后提交并推送，按逻辑拆成多个 commit。

## 数据与环境

- 原始数据和模型不进 Git（仓库是公开的）。不要把视频描述原文、日志、账号、密码、令牌、服务器地址写进仓库。`analysis/*/results/` 只放数值汇总。
- 主要数据：快手 RecIF（Hugging Face `OpenOneRec/OpenOneRec-RecIF`，需登录并同意条款）、清华 ShortVideo（需向数据方申请账号）、KuaiRand（公开）。模型：`OpenOneRec/OneRec-1.7B`、`Qwen/Qwen3-Embedding-8B`、`Qwen/Qwen3-30B-A3B-Instruct-2507`。
- 已跑过的实验在 Li Yitong 的 GPU 服务器上（8×A6000），工作目录结构见 [analysis/v5_feasibility/README.md](analysis/v5_feasibility/README.md)。其他人复现需要自己的 GPU 和数据账号。
- 环境要点：vLLM 0.11.0 必须配 transformers 4.57.1（5.x 不兼容）；服务器访问 Hugging Face 常断，模型可从 ModelScope 下载；后台任务用 `setsid nohup ... &` 并等待 `.done` 标记文件。
- 文档转 PDF：`bash docs/project-plan/pdf-build/build.sh <文件.md>`（需 pandoc、npm、Chromium）。
