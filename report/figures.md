# 图表登记

| F-R4-revised | 察觉：1.4% 新参照及版本敏感性 | `analysis/v6_simulation/results/detection_revised.csv`、同名 meta | `analysis/v6_simulation/figures/detection_revised.png` / `.pdf` | 解析情境，分类器假设；占比引用分版本核查 | Xu Ruicong | 已运行 |

每完成一张图或表，加一行。编号在整合时统一。

| 临时编号 | 内容 | 结果文件 | 图片 | 证据类型 | 负责 | 状态 |
|---|---|---|---|---|---|---|
| T-bottom-up | 各大类议题的曝光占比与对立叙事比例 | `analysis/v6/results/bottom_up_summary.json` | （待画） | 实测（LLM 标注，未核查） | Li Yitong | 数据已有 |
| T-agreement | 双模型核查：群体标签混淆矩阵、Qwen 查准率与查全率、kappa；分歧类型 | `analysis/v6_annotation/results/agreement_v0.json`、`agreement_v0_confusion.csv`、`agreement_v0_disagreements.csv` | 表，不需要图 | 实测（LLM 对照更强的 LLM，非人工金标准） | Zhao Dingcheng | v0 已有，待 v1 更新 |
| T-taxonomy（表 4.1） | 各大类的曝光占比、对立叙事比例（Wilson 区间）、叙事类型与主要子议题 | `analysis/v6_annotation/results/taxonomy_qwen_v0.csv`、`_subissues.csv`、`_table.md`、`.meta.json` | 表 | 实测（Qwen 标注，未核查） | Zhao Dingcheng | 初稿；待 DeepSeek 重标后重新生成 |

| F-R2-revised | 有界形成：m_t、供给参照总偏斜和均值状态平面 | `analysis/v6_simulation/results/formation_bounded.csv`、`formation_bounded_summary.csv`、同名 meta | `analysis/v6_simulation/figures/formation_bounded.png` / `.pdf` | 情境假设；20 种子点态 95% Monte Carlo 区间 | Xu Ruicong | 按 #4 审阅重跑；主图供给 2% |
