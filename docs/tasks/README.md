# 三人协作说明（v6，2026-11-07 至 11-15）

计划见 [Research Plan v6](../project-plan/research_plan_v6.md)。每人的任务说明：

| 人 | 任务说明 | 主要目录 |
|---|---|---|
| Zhao Dingcheng | [zhao_dingcheng.md](zhao_dingcheng.md)：叙事定义与标注规范、人工核查、相关研究、曝光报告样稿 | `analysis/v6_annotation/`、`report/sections/` 中自己的节 |
| Xu Ruicong | [xu_ruicong.md](xu_ruicong.md)：透明模型模拟、察觉样本量 | `analysis/v6_simulation/`、`report/sections/` 中自己的节 |
| Li Yitong | [li_yitong.md](li_yitong.md)：服务器上的标注与 OneRec 实验、理论、整合、审阅 | `analysis/v6/`、`report/` |

## 流程

1. 拉取最新 `main`，从它新建自己的分支：`dingcheng/<主题>` 或 `ruicong/<主题>`。
2. 只改自己负责的目录和报告小节；需要改别人的文件时，在 PR 里说明。
3. 小步提交，提交信息写清楚做了什么。完成一块就推送并开 Pull Request 到 `main`，标题写任务编号（如 `[D2] 标注规范初稿`）。
4. Li Yitong（用 Claude Code）审阅 PR，在 PR 里留意见；改完后合并。
5. 有问题在 PR 或群里提，不要等到截止前。

## 规则

- **仓库是公开的**：不提交视频描述原文、日志原始数据、账号、密码、令牌或服务器地址。需要原文的材料（如待核查的视频描述）由 Li Yitong 私下发送，只提交视频 ID（pid）和标签、汇总数字。
- **证据分级**：每个数字注明来源——"实测"（来自数据或真实模型）或"情境假设"（模拟中设定的参数）。情境参数要做扫描，报告整条曲线，不只报告一个值。
- **写作**：平实的中文，先给结论再给依据；引用只用核实过的文献（见 [v5 第 5 节](../project-plan/research_plan_v5.md) 与 [v5 可行性记录第 6 节](../context-recovery/plan_v5_feasibility.md)），新增引用要写全作者、年份、出处。
- **可以用 Claude Code**：在仓库根目录打开，它会读 [CLAUDE.md](../../CLAUDE.md)。告诉它"读 docs/tasks/<你的文件>.md，帮我完成任务 X"。

## 时间线

| 日期 | 节点 |
|---|---|
| 11-07 | 发布任务；Li Yitong 发送私有材料 |
| 11-09 | 定义与标注规范（D1、D2）、模拟框架能跑（R1）各开一个 PR |
| 11-11 | 首批结果：人工核查（D3）、模拟主图（R2、R3）、察觉曲线（R4） |
| 11-12 | 报告各节初稿 PR |
| 11-13 至 11-14 | 整合、互审、修改 |
| 11-15 | 提交报告 |
