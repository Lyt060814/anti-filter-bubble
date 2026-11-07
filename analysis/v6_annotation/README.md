# v6 标注定义、提示词与核查（Zhao Dingcheng）

| 文件 | 内容 | 任务 |
|---|---|---|
| [narrative_types.md](narrative_types.md) | 四类对立叙事的定义、判断步骤、正例和反例；群体标签的边界 | D1 |
| [prompt.md](prompt.md) | 标注提示词的说明和原文（由 `make_prompt_md.py` 从 `prompt_v1.py` 和 `prompt_md.in` 生成） | D2 |
| [prompt_v1.py](prompt_v1.py) | 提示词正式文本和解析函数，可直接替换 `analysis/v6/dual_model_check.py` 中的同名对象 | D2 |

这里只放定义、提示词、分析脚本和数值汇总。所有例子都是编写的，不含视频描述原文；标签由 LLM 在服务器上生成，见 [analysis/v6](../v6/README.md)。
