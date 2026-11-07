# 图表登记


每完成一张图或表，加一行。编号在整合时统一。

| 临时编号 | 内容 | 结果文件 | 图片 | 证据类型 | 负责 | 状态 |
|---|---|---|---|---|---|---|
| T-bottom-up | 各大类议题的曝光占比与对立叙事比例 | `analysis/v6/results/bottom_up_summary.json` | （待画） | 实测（LLM 标注，未核查） | Li Yitong | 数据已有 |
| T-agreement（表 4.3） | 双模型核查：v0/v1/v2 三版提示词下的性别群体标签数、Qwen 查准率与查全率、kappa；v2 的四问分歧位置 | `analysis/v6_annotation/results/agreement_v0.json`、`agreement_v1.json`、`agreement_v2.json`（含 `question_divergence`）及各自的混淆矩阵、分歧清单、meta | 表 | 实测（LLM 对照更强的 LLM，非人工金标准） | Zhao Dingcheng | v2 已更新 |
| T-taxonomy（表 4.1） | 各大类的曝光占比、对立叙事比例（Wilson 区间）、叙事类型与主要子议题；末列为 Qwen 在同一批曝光上的对照 | `analysis/v6_annotation/results/taxonomy_deepseek_bu.csv`、`_subissues.csv`、`_table.md`、`.meta.json`（对照：`taxonomy_qwen_v0*`） | 表 | 实测（DeepSeek V4 Pro 标注，跨大类提示词；无人工核查） | Zhao Dingcheng | 已按 #13 更新 |
| T-strat（表 4.2） | 分大类分层样本：五个研究大类内对立叙事的加权比例（层内自助法区间）、flash 粗筛被参照确认的比例、叙事类型 | `analysis/v6_annotation/results/taxonomy_strat_ds.csv`、`_table.md`、`.meta.json` | 表 | 实测（deepseek-flash 粗筛 + DeepSeek V4 Pro 标注；无人工核查） | Zhao Dingcheng | 已按 #13 更新 |
| F-R4-revised | 察觉：版本参照及分类器敏感性 | `analysis/v6_simulation/results/detection_revised.csv`、同名 meta | `analysis/v6_simulation/figures/detection_revised.png` / `.pdf` | 解析情境；占比引用分版本核查 | Xu Ruicong | 已运行 |
| F-R3-formation | 试点响应匹配后形成 | `analysis/v6_simulation/results/calibrated_formation_group.csv.gz`、`_conflict.csv.gz`、`_summary.csv.gz`；`formation_calibrated.meta.json` | `analysis/v6_simulation/figures/formation_calibrated.png` / `.pdf` | 试点锚点拟合的合成情境，不是线上效果 | Xu Ruicong | 已运行 |
| F-R3-escape | 11 策略及 NI 校准补充 | `analysis/v6_simulation/results/calibrated_escape_<family>_s<supply>.csv.gz`、`calibrated_escape_summary.csv.gz`、`ni_calibrated_sensitivity.csv`；`escape_calibrated.meta.json` | `analysis/v6_simulation/figures/escape_calibrated.png` / `.pdf` | 合成情境 | Xu Ruicong | 已运行 |
| F-R3-persistence | 停止后相对 S0 的持续性 | `analysis/v6_simulation/results/calibrated_persistence.csv.gz`、上述逃离 CSV；`persistence_calibrated.meta.json` | `analysis/v6_simulation/figures/persistence_calibrated.png` / `.pdf` | 合成情境，含右删失 | Xu Ruicong | 已运行 |
| T-R3-calibration | 全设定校准输入、实现系数、注入响应及 NI 校准 | `analysis/v6_simulation/results/calibration_targets.csv`、`ni_response_calibration.csv`；`formation_calibrated.meta.json`、`ni_response_calibration.meta.json` | 表，报告参数节引用 | 试点锚点与情境参数分开 | Xu Ruicong | 已保存 |
| S-R5-calibrated | 压缩后审计运行输出截图 | `report/screenshots/calibrated_run_output.txt`、截图同名 `.meta.json` | `report/screenshots/ruicong_calibrated_run.png` | 实际执行证据；日志内实验是合成情境 | Xu Ruicong | 已保存 |
| T-R5-filter-v2 | v2 分类器直接过滤及主情境动态敏感性 | `analysis/v6_simulation/results/filter_v2_instant.csv.gz`、`filter_v2_dynamic.csv.gz` 及各自 `.meta.json` | 第 5 节文字比较，未新增图 | 合成/解析敏感性，分类器输入为跨模型一致率 | Xu Ruicong | 已运行；不替代完整网格基准 |
| F-R2-revised | 有界形成：m_t、供给参照总偏斜和均值状态平面 | `analysis/v6_simulation/results/formation_bounded.csv`、`formation_bounded_summary.csv`、同名 meta | `analysis/v6_simulation/figures/formation_bounded.png` / `.pdf` | 情境假设；20 种子点态 95% Monte Carlo 区间 | Xu Ruicong | 按 #4 审阅重跑；主图供给 2% |
| F-D6-mockup（图 6.1） | 观点曝光报告样稿：议题占比、与非个性化参照比较及"证据不足"、各操作的预期效果与议题保留、不声称什么 | `analysis/v6_annotation/results/exposure_report_mockup.csv`、`.meta.json` | `analysis/v6_annotation/figures/exposure_report_mockup.png`、`.pdf` | 混合：示例用户为示意（编造）；证据门槛为命题 6 公式；操作效果为第 5.2 节模拟（情境假设） | Zhao Dingcheng | 初稿 |
| F-L4-main | L4 对齐的弱形成和指定策略端点 | `analysis/v6_simulation/results/l4_main_formation.csv.gz`、`l4_main_endpoints.csv.gz`、`l4_main_summary.csv`、`l4_main_calibration.csv`、`l4_main.meta.json` | `analysis/v6_simulation/figures/l4_main.png` / `.pdf` | 合成主情形，校准输入来自 L4；旧图保留为上限 | Xu Ruicong | issue #21 重跑 |
