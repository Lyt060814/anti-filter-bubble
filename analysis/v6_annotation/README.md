# v6 标注定义、提示词与核查（Zhao Dingcheng）

| 文件 | 内容 | 任务 |
|---|---|---|
| [narrative_types.md](narrative_types.md) | 四类对立叙事的定义、判断步骤、正例和反例；群体标签的边界 | D1 |
| [prompt.md](prompt.md) | 标注提示词的说明和当前版本原文（由 `make_prompt_md.py` 从当前提示词模块和 `prompt_md.in` 生成） | D2 |
| [prompt_v2.py](prompt_v2.py) | **当前**提示词（v2，issue #10）：四问分字段、解析检查四问与标签一致；可直接替换 `analysis/v6/dual_model_check.py` 中的同名对象 | D2、D3 |
| [prompt_v1.py](prompt_v1.py) | v1 提示词，保留供复现 v1 结果 | D2 |
| [agreement.py](agreement.py) | 双模型核查分析：混淆矩阵、查准率与查全率（Wilson 区间）、Cohen's kappa（自助法区间）、校正比例、分歧归类、版本对比；`--selftest` 用假数据自检 | D3 |
| [agreement.md](agreement.md) | 核查结果与解读（当前为 v0） | D3 |
| [taxonomy.py](taxonomy.py) | 自下而上抽样的分类表：各大类曝光占比、对立叙事比例、叙事类型、子议题（关键词归并 LLM 自由填写的议题名） | D4 |
| [design_mockup.py](design_mockup.py) | 观点曝光报告样稿（图 6.1）：每个数字注明示意／公式／模拟，图存在 `figures/` | D6 |
| `results/` | `agreement_<版本>.json`、混淆矩阵、分歧清单（只含 pid、标签和类别）、`.meta.json`（D3）；`taxonomy_<来源>*`（D4） | D3、D4 |

这里只放定义、提示词、分析脚本和数值汇总。所有例子都是编写的，不含视频描述原文；标签由 LLM 在服务器上生成，见 [analysis/v6](../v6/README.md)。
