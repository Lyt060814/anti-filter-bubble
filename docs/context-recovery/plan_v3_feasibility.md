# Plan v3：基础可行性检查与未完成项

2026-10-03 · 对应 [Working v3](../project-plan/working_plan_v3.md)、[Execution v3](../project-plan/execution_plan_v3.md)及[扩展调研](../project-plan/resource_review_v3.md)。这些是本轮实际取得和运行的结果，不能解释为主研究已完成。

## 1. 检查结果

| 检查 | 实际结果 | 支持／不支持 |
|---|---|---|
| 官方资源获取 | 14 个新增仓库成功取得；6 篇新增 PDF 成功取得并抽取文本；记录固定 commit／哈希 | 有可检查实物；不等于全部源码审计或论文复现 |
| ShortVideo 配对媒体 | 8/8 MP4 与 8/8 中文 ASR 下载成功；8/8 视频有可解码画面和音轨，均提取首帧及 16kHz 单声道音频 | 原视频→音画／转录输入链路可行；没有运行新 ASR、VLM 或立场标注 |
| 媒体范围 | 原视频＋ASR 共 131,388,228 bytes，视频合计约 493.84 秒；关系、育儿、职业关键词各前两个 ID，加两个对照 | 便利检查，不代表议题相关率或作者立场；命中广告／剧情／幽默文本的实际案例提醒要做语义审计 |
| KuaiSAR v2 | 完整 ZIP 845,087,902 bytes，官方 MD5 匹配；读取五表，每表最多前 5,000 行，社交表实际 612 行 | 数据可取、字段可读；未做全量统计、跨源关联或搜索效果估计 |
| 新预训练语义检索 | Qwen3-Embedding-0.6B 固定权重，CPU 生成 11×1024 向量（3 查询＋8 真实标题／ASR），全部有限，完成候选排序 | 真正运行预训练模型，非模拟输出；无独立金标准，不能报告准确率／召回率或模型最优 |
| 该次嵌入推理资源 | 加载＋推理约 11.18 秒，峰值 RSS 4,109,204 KiB，4 CPU 线程，batch=2，max_length=512；不含下载 | 只对应本小批与设置，不外推全库、长视频或 VLM；截断可能损失后文 |
| KuaiSim 原模型运行 | 未修改 KRMBUserResponse，合成张量、CPU；输出 `[2,1,2]`、状态 `[2,1,96]`，前向／反向均有限 | 原响应网络在当前环境可运行；未训练、未跑完整推荐环境，无真实性或策略效果结论 |
| KuaiSim 概率合同 | BaseModel 的 probs 已是 sigmoid(preds)，所读 whole-session 环境再次 sigmoid；0 logit 的 0.5 将变约 0.62246 后才扣相似性惩罚 | 需适配审计。只针对固定快照的这条组合路径，不声称所有配置或论文结果相同 |
| LLM_User_Simulator 复现依赖 | loader 默认要求 `dataset/MO_dataset.pkl`，环境要求 `user_response_model/best_model.pth`；快照缺失 | 方法可借鉴，不能承诺下载代码后直接复现；无顶层 LICENSE 时不默认可重分发 |
| VLM／Omni／Agent／Phoenix | 源码／接口／硬件与资源要求已检查；尚未模型端到端试跑 | 仍是有入口的候选依赖，不能标为本机已部署；当前没有可用 CUDA 运行结果 |

Qwen 嵌入权重固定为 `97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3`；模型文件 1,191,586,416 bytes。KuaiSim 固定为 `2ae32aa25a0aac103194a66e6864e3d2ac6d6580`。权重和媒体保存在外部资料目录，未复制进项目 Git。

## 2. 实际字段检查改变了哪些假设

KuaiSAR v2 的 `item_features.caption` 和 `src_inter.keyword` 在检查前缀中为数字列表，与官方编码描述相符；没有映射字典时不能恢复自然语言命题。推荐日志包含 `search`、`search_photo_related`，搜索日志包含 session、来源与点击字段，因此可研究入口和转换结构。

前 5,000 条推荐行中，4,913 行属于重复的同用户／timestamp 组合；搜索前缀中同用户／search_session_timestamp 重复更多。这些是前缀计数，不是总体重复率。结合官方[时间字段说明](https://kuaisar.github.io/detailed_statistics.html)，不能简单按行次序当精确观看序列，也不能按同用户时间去重而删掉同批不同视频。

ShortVideo 标签与转录实读表明：关键词候选不保证与目标命题相关，画面中的提问也不能直接看成整条视频结论。多模态比较应保留剧情、引用和无关项，不能只挑清楚表达立场的材料。已发布 ASR 包含情绪／音乐标记及可能转录错误，没有精确时间戳的文本不冒充已完成强制对齐。

没有用模型为这 8 条生成研究金标准，也没有将单帧观察当完整视频理解。此次样例已经被读过，后续若使用应登记为开发／可行性材料，不能当未见测试。

## 3. 原始记录与复查命令

- [资源获取](plan_v3_acquisition.json)、[补充获取](plan_v3_additional_acquisition.json)、[模拟评价仓库](plan_v3_sim_eval_acquisition.json)。失败的 KuaiSAR 仓库猜测保留原状态；实际数据来自官方 Zenodo，不覆盖失败记录。
- [媒体记录](plan_v3_media_probe.json)：源 URL、文件大小、哈希、编解码器及抽取状态。
- [KuaiSAR 记录](plan_v3_kuaisar_probe.json)：官方校验、ZIP 身份和有限前缀 schema。
- [模型推理](plan_v3_embedding_probe.json)：权重 revision、哈希、运行版本、候选排序与设置。
- [KuaiSim 检查](plan_v3_kuaisim_probe.json)：原模型输出合同及特定环境源码检查。
- [隔离环境包清单](../../analysis/context_audit/plan_v3_check_requirements.txt)。本轮建立外部 `envs/v3-check`，不修改项目生产依赖。

从项目根目录运行（资料目录作为显式参数，不依赖旧 cloud 路径）：

```bash
python3 analysis/context_audit/plan_v3_acquire.py ../anti-filter-bubble-sources
python3 analysis/context_audit/plan_v3_media_probe.py ../anti-filter-bubble-sources
python3 analysis/context_audit/plan_v3_kuaisar_probe.py ../anti-filter-bubble-sources
../anti-filter-bubble-sources/envs/v3-check/bin/python analysis/context_audit/plan_v3_embedding_probe.py ../anti-filter-bubble-sources
../anti-filter-bubble-sources/envs/v3-check/bin/python analysis/context_audit/plan_v3_kuaisim_probe.py ../anti-filter-bubble-sources
```

现有仓库不 pull/reset；媒体顺序下载遵守作者的大文件并发上限。嵌入脚本默认固定上述 revision；需要比较其他版本时显式指定 `--revision` 并另存记录，未来主实验不得不加记录地跟随模型更新。运行脚本会重写各自机器记录，正式实验另用不可变 run 目录；标注不可直接写入这些生成文件。

## 4. 最终可行性判断

**已有资源足以支撑明确的数据分析、技术设计和动态建模路线，并有真实媒体、预训练检索与原用户响应网络的运行证据。** 这强于仅有资源链接，但仍远未证明完整方案有效。

进入正式实验还必须落实：多议题样本与盲测、独立人工标签、选定 LLM/VLM/Agent 的推理环境和小批适用性、响应模型真实训练与校准、来源目录、真实轨迹准入、策略实现和跨环境实验。真人验证与生产平台接入另有实际条件。

Execution v3 用门槛和失败分支管理这些依赖：未通过就报告该能力未实现或未被验证，保留可执行的设计／机制研究。不能因为课程允许不完成整个系统，就把未验证依赖写成“100% 效果可行”；也不因它们尚未全部落实而把理想方案缩回单议题文本过滤。
