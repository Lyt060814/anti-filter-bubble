# v5 可行性核查脚本

对应 [Research Plan v5](../../docs/project-plan/research_plan_v5.md) 与 [v5 可行性记录](../../docs/context-recovery/plan_v5_feasibility.md)。脚本在服务器 `tyu-g1:~/fb-research` 上运行，`results/` 只保存数值汇总，不含视频描述原文（RecIF 需同意条款后下载，这里不再分发）。

| 脚本 | 作用 | 环境 |
|---|---|---|
| `recif_user_item_stats.py` | 议题曝光结构、每人与每条视频的曝光分布、反馈率、关键词代理叙事的用户间离散度 | CPU，`.venv` |
| `video_history_check.py` | 核对视频推荐任务的历史是什么（结果：基准测试用户不在公开日志中） | CPU |
| `ni_confounding_check.py` | 用日志检验"曝光选择"能否解释学到的"不感兴趣"为何反向 | CPU |
| `label_pilot.py` | 用开源 LLM 给 1,800 条议题候选标注三种属性，统计流行度与反馈率 | 2×GPU，vLLM |
| `onerec_manipulation_probe.py` | OneRec 模板检查、抽样召回、话题与"不感兴趣"的操纵检验；`Maps` 提供 pid 与语义 ID 的查表 | 1×GPU，vLLM |
| `onerec_ni_header_probe.py` | 同一批视频换不同栏目标题，检验模型是否读懂"不感兴趣"的含义 | 1×GPU |
| `onerec_viewpoint_probe.py` | 精确计算语义 ID 序列概率，检验 OneRec 在议题内是否区分属性；可加随机假属性与按语义 ID 前缀分组的对照 | 1×GPU，transformers |

运行方式（服务器上）：

```bash
cd ~/fb-research
.venv/bin/python -I analysis/recif_user_item_stats.py data/recif logs/recif_user_item_stats.json
CUDA_VISIBLE_DEVICES=1,2 .venv-gpu/bin/python -I analysis/label_pilot.py models/Qwen3-30B-A3B-Instruct-2507 data/recif logs/label_pilot 1200 600 2
CUDA_VISIBLE_DEVICES=0 .venv-gpu/bin/python -I analysis/onerec_manipulation_probe.py models/OneRec-1.7B data/recif logs/onerec_probe.json 40 2000
CUDA_VISIBLE_DEVICES=0 .venv-gpu/bin/python -I analysis/onerec_ni_header_probe.py models/OneRec-1.7B data/recif logs/onerec_ni_header.json 30
CUDA_VISIBLE_DEVICES=3 .venv-gpu/bin/python -I analysis/onerec_viewpoint_probe.py models/OneRec-1.7B data/recif logs/label_pilot_labels.jsonl logs/onerec_viewpoint.json 30 0 [controls]
```

环境：`.venv` 为 pyarrow 19.0.1、pandas 2.2.3、numpy 1.26.4；`.venv-gpu` 为 torch 2.8.0+cu128、vLLM 0.11.0、transformers 4.57.1（vLLM 0.11 与 transformers 5.x 不兼容）。服务器访问 Hugging Face 不稳定时，模型从 ModelScope 下载。
