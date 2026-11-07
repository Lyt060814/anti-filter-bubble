# 图表登记


每完成一张图或表，加一行。编号在整合时统一。

| 临时编号 | 内容 | 结果文件 | 图片 | 证据类型 | 负责 | 状态 |
|---|---|---|---|---|---|---|
| T-bottom-up | 各大类议题的曝光占比与对立叙事比例 | `analysis/v6/results/bottom_up_summary.json` | （待画） | 实测（LLM 标注，未核查） | Li Yitong | 数据已有 |
| T-agreement | 双模型核查：群体标签混淆矩阵、Qwen 查准率与查全率、kappa；分歧类型 | `analysis/v6_annotation/results/agreement_v0.json`、`agreement_v0_confusion.csv`、`agreement_v0_disagreements.csv` | 表，不需要图 | 实测（LLM 对照更强的 LLM，非人工金标准） | Zhao Dingcheng | v0 已有，待 v1 更新 |
| T-taxonomy（表 4.1） | 各大类的曝光占比、对立叙事比例（Wilson 区间）、叙事类型与主要子议题；末列为 Qwen 在同一批曝光上的对照 | `analysis/v6_annotation/results/taxonomy_deepseek_bu.csv`、`_subissues.csv`、`_table.md`、`.meta.json`（对照：`taxonomy_qwen_v0*`） | 表 | 实测（DeepSeek V4 Pro 标注，跨大类提示词；无人工核查） | Zhao Dingcheng | 已按 #13 更新 |
| F-R4-revised | 察觉：版本参照及分类器敏感性 | `analysis/v6_simulation/results/detection_revised.csv`、同名 meta | `analysis/v6_simulation/figures/detection_revised.png` / `.pdf` | 解析情境；占比引用分版本核查 | Xu Ruicong | 已运行 |
| F-R3-formation | 试点响应匹配后形成 | `analysis/v6_simulation/results/calibrated_formation_group.csv.gz`、`_conflict.csv.gz`、`_summary.csv.gz`；`formation_calibrated.meta.json` | `analysis/v6_simulation/figures/formation_calibrated.png` / `.pdf` | 试点锚点拟合的合成情境，不是线上效果 | Xu Ruicong | 已运行 |
| F-R3-escape | 11 策略及 NI 校准补充 | `analysis/v6_simulation/results/calibrated_escape_<family>_s<supply>.csv.gz`、`calibrated_escape_summary.csv.gz`、`ni_calibrated_sensitivity.csv`；`escape_calibrated.meta.json` | `analysis/v6_simulation/figures/escape_calibrated.png` / `.pdf` | 合成情境 | Xu Ruicong | 已运行 |
| F-R3-persistence | 停止后相对 S0 的持续性 | `analysis/v6_simulation/results/calibrated_persistence.csv.gz`、上述逃离 CSV；`persistence_calibrated.meta.json` | `analysis/v6_simulation/figures/persistence_calibrated.png` / `.pdf` | 合成情境，含右删失 | Xu Ruicong | 已运行 |
| T-R3-calibration | 全设定校准输入、实现系数、注入响应及 NI 校准 | `analysis/v6_simulation/results/calibration_targets.csv`、`ni_response_calibration.csv`；`formation_calibrated.meta.json`、`ni_response_calibration.meta.json` | 表，报告参数节引用 | 试点锚点与情境参数分开 | Xu Ruicong | 已保存 |
| F-R2-revised | 有界形成：m_t、供给参照总偏斜和均值状态平面 | `analysis/v6_simulation/results/formation_bounded.csv`、`formation_bounded_summary.csv`、同名 meta | `analysis/v6_simulation/figures/formation_bounded.png` / `.pdf` | 情境假设；20 种子点态 95% Monte Carlo 区间 | Xu Ruicong | 按 #4 审阅重跑；主图供给 2% |
