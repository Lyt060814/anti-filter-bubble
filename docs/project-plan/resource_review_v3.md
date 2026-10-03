# v3 扩展调研：资源实物、方法选择与设计变化

2026-10-03。为 [Working v3](working_plan_v3.md) 与 [Execution v3](execution_plan_v3.md) 提供依据。本轮扩大到内容检索、多模态理解、工具调用、可控推荐、用户仿真与离线评价；沿用已有问题研究的[逐项来源台账](../context-recovery/plan_source_review.md)，没有把历史阅读伪装成本轮新实验。

本轮检索入口包括 arXiv、ACL Anthology、作者／机构官方仓库、数据官方站与 Zenodo。搜索结果只用于发现，决定采用与否依据实际正文、源码或字段。阅读范围以下逐项列出；下载不代表全仓库逐行审计，方法对照不代表已经复现结果。

## 1. 总体决定及相对 v2 的变化

| v2 尚未落实的部分 | 本轮证据 | v3 的决定 |
|---|---|---|
| 多模态理解主要停留在候选描述 | 下载 8 条 ShortVideo 原视频与配对 ASR，全部解码；实际样例包含对话、带引用的说法和关键词误收 | 将多模态表示和取证流程设为主线实验；不以这 8 条定义规模或真值 |
| 检索以关键词资产为中心 | 新查 BGE、Qwen3 文本与视觉检索的代码入口 | 比较词法／语义／多模态召回，审计未命中；关键词只是一种对照 |
| Agent 作为额外功能 | Qwen-Agent、InteRecAgent 已有语义意图→检索／排序工具的实现 | 按需取证、目标确认、来源补充、策略调用进入主候选；统计和约束独立计算 |
| CPU 规则世界起步，LLM 用户可选 | SimTok、KuaiSim、混合用户模型和独立模拟评价提供不同方法；原仓库暴露依赖／概率接口问题 | U1 数据、U2 Agent、优先检验 U3 混合；U0 是机制对照。先验证用户模型，再评价干预 |
| 新数据只看文档 | 完整取得 KuaiSAR v2 压缩包并校验，读取各表前缀 | 用搜索／推荐结构，保留编码语义和批次时间边界，不拿它直接测观点 |
| 开放源码默认为可直接使用 | LLM_User_Simulator 缺默认数据／checkpoint；KuaiSim 特定路径重复 sigmoid | 分开“直接组件”“需适配”“只借鉴方法”；先审接口，不能承诺整套原研究开箱复现 |
| 更多资源可能变成更多支线 | 课程要求 hybrid 中至少一部分深入，软件非必需 | 所有资源服务同一发现—调整—维持问题，不按仓库数量分任务，不为方法原创加复杂度 |

保留 v2 的核心论证：兴趣集中不必有害、类别多样不排除同题偏斜、行为不等于认可、参照不等于真值、未知不当中立、用户控制与认知收益分层。v3 改的是完整技术路线和验证力度，并非再次换题。

## 2. 本轮取得与实际阅读的资源

14 个新增仓库快照取得成功，另一次猜测的 `KuaiSAR/KuaiSAR` 仓库地址失败；随后使用官方站指向的 Zenodo 获得数据，不把失败记成成功。新增 6 篇 PDF 取得并转为文本；仓库内另有模型技术报告。版本及文件身份见[主清单](../context-recovery/plan_v3_acquisition.json)、[补充清单](../context-recovery/plan_v3_additional_acquisition.json)、[用户模拟评价仓库](../context-recovery/plan_v3_sim_eval_acquisition.json)。原资料、视频和模型留在外部资料根目录。

### 2.1 内容检索与理解

| 官方来源 | 本轮实际检查范围 | 用途与决定 |
|---|---|---|
| [ShortVideo_dataset](https://github.com/tsinghua-fib-lab/ShortVideo_dataset) | 已有 README／采样表，官方文件目录，新下载 MP4/ASR、ffprobe 与画面／音轨解码；读 8 条转录并查看一条首帧 | 数据入口可行；文本与音画匹配可做。8 条按关键词便利选择，非代表审计；标签命中可能是广告、剧情、无关内容 |
| [Qwen3-VL](https://github.com/QwenLM/Qwen3-VL) | README 的视频推理与配置；`qwen-vl-utils/.../vision_process.py` 的取帧、fps、起止时间处理 | VLM 候选；其视觉视频输入不能自动当作读取音轨，另供 ASR。未下载／运行该模型权重 |
| [Qwen3-Omni](https://github.com/QwenLM/Qwen3-Omni)；[报告](https://arxiv.org/abs/2509.17765) | README 的 Transformers/vLLM、`use_audio_in_video`、硬件表，论文架构／能力说明；未做本任务 benchmark | 音画联合候选；文档中的服务路径有音频处理差异。需实测模型服务或 GPU 环境，不能假设当前 CPU 路径已经部署 |
| [SenseVoice](https://github.com/FunAudioLLM/SenseVoice) | README 的中文音频、使用、许可证说明及已有 ShortVideo 转录格式 | 中文 ASR／音频线索候选；情绪标签不当立场。代码和权重条款分开；本轮使用已发布 ASR，未运行该模型 |
| [FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding)；[BGE-M3](https://arxiv.org/abs/2402.03216) | 推理文档的 dense/sparse/multivector 和 reranker，论文方法与任务说明；未复现 benchmark | 多语检索候选；相关性向量不表示支持／反对，后续语义抽取另做 |
| [Qwen3-Embedding](https://github.com/QwenLM/Qwen3-Embedding) | README 的模型规格、last-token pooling、归一化与指令；下载 0.6B 权重并做真实材料 CPU 推理检查，结果见可行性记录 | 文本检索有可运行入口；小批相似度不是召回率、立场准确率或最佳模型证据 |
| [Qwen3-VL-Embedding](https://github.com/QwenLM/Qwen3-VL-Embedding) | README、`src/models/qwen3_vl_embedding.py` 的视频输入／抽帧／表示接口 | 多模态检索候选，有原视频时可查标题漏收；未下载权重／运行，非语义分类器 |

没有把所有可找到的 VLM 全部拉入正式比较。上述候选覆盖文本、视觉＋转录、原生音画三种有实质区别的条件；如开发材料显示其他可获得模型更合适，按同协议替换并留选择记录。InternVL/PaddleOCR 是此前已核查入口的备选，本轮没有新克隆或实测，不把它们计入新增实物成果。

本轮媒体观察的设计含义：某关系关键词样例实际上是商品演示；另一条是夫妻剧情；育儿样例同时出现对话和名人归因；职业命中里有与剪发相关的幽默文本。这里只记录错误风险，未经双标不形成作者立场金标准。视频内容里的事实主张也未因下载成功就被核实。

### 2.2 用户目标、工具与干预

| 官方来源 | 实际检查 | 用途与限制 |
|---|---|---|
| [Qwen-Agent](https://github.com/QwenLM/Qwen-Agent) | README 与 `examples/assistant_qwen3.py` 的模型端点、工具清单和交互入口 | 可复用工具编排；需要模型服务与本项目领域工具。未调用模型，不把演示工具清单直接当正式权限 |
| [InteRecAgent / RecAI](https://github.com/microsoft/RecAI/tree/main/InteRecAgent) | README 与 `llm4crs/ranking/reco_model_tool.py` 的 prefer/unwanted、候选缓冲区和排序调用 | 借用自然语言→查询／检索／排序分工。其现有商品／电影数据及兴趣项不是观点 T/K/A，需要适配且用户确认 |
| [UCRS](https://github.com/WenjieWWJ/UCRS) | 复读原有快照 README 的 FM/NFM 训练、用户／物品控制及 checkpoint 入口 | 作为能修改推荐模型的研究上界。原框架无需重发明，但不能假装用户拥有平台特征控制权；本轮未复现实验 |
| [OpenOneRec](https://github.com/Kuaishou-OneRec/OpenOneRec) | README 的模型、item token、训练与许可；`benchmarks/README.md` 及任务目录 | 指令推荐与任务评价的扩展对照；内容 token 需对应映射，部分评估需外部模型。不把通用指令成绩称为观点控制成绩，暂不作主线前置条件 |
| [RADio](https://github.com/svrijenhoek/RADio) / MMR 等已有资源 | 沿用前轮的规范目标、参照与多样性分析，非本轮新复现 | 简单重排／去冗余按本任务适配即可；新增理由和真实来源仍要单独核查 |

自然语言控制的技术价值在于减少意图被压缩成一个按钮的损失。工具框架只是实现手段，系统必须展示误删和取舍；禁止以模型生成“相反观点”代替来源检索。是否需要多个 Agent 由任务依赖决定，未预设多 Agent 必优。

### 2.3 用户模拟与可信度

| 来源 | 实际阅读／检查 | 对本项目的决定 |
|---|---|---|
| [SimTok](https://arxiv.org/abs/2504.08742v1) | 复核 §2 方法、§3–4 实验与 §6 限制；原 PDF 在本地 | 可借闭环，不能把文本标题输入叫真正刷视频；类别覆盖／正反馈代理不直接作为我们的成功指标 |
| [KuaiSim](https://arxiv.org/abs/2309.12645)；[代码](https://github.com/Applied-Machine-Learning-Lab/KuaiSim) | 论文 §3 的即时响应、退出、retention，README、`KRMBUserResponse.py`、`model/general.py`、`KREnvironment_WholeSession_GPU.py`；实际运行原响应网络 CPU 前向／反向 | 多反馈模型可作为 U1 基础，真实训练和长期校验仍未做。退出、跨 session、相似性惩罚是需要审计的假设 |
| [LLM-Powered User Simulator](https://arxiv.org/abs/2412.16984)；[代码](https://github.com/Applied-Machine-Learning-Lab/LLM_User_Simulator) | 方法的语义特征／匹配／统计集成、实验任务；`environment/env.py`、Yelp loader/config、SASRec 入口 | 支持优先检验混合方法；不能照搬原任务标签为观点认可。公开快照缺默认数据和权重，按方法适配，不承诺直接复现 |
| [YuLan-Rec / RecAgent](https://github.com/RUC-GSAI/YuLan-Rec) | README 的画像、记忆、行为、运行数据与 API 配置 | 提供有记忆 Agent 的组织参考；电影与社交场景需转换，记忆“像人”是建模选择，不是外部验证 |
| [模拟用户评价，NAACL 2024](https://aclanthology.org/2024.naacl-long.83/)；[代码](https://github.com/granelle/naacl24-user-sim) | 正文任务／方法／结果及限制，README、`t2_bin_preference/generate.py`；库含部分数据，其他数据按作者指引另取 | 借用偏好分布、请求与反馈一致性的独立检验；早期模型／电影对话的偏差不当当前所有模型的定论；未运行其 API 实验 |
| [CIRS](https://github.com/chongminggao/CIRS-codes) / 本仓库旧 pilot | 沿用已核查的矩阵反馈、退出阈值与旧复发假设 | 透明机制／有限池对照，不作为观点转变真值；新模型不能沿用旧类别成功指标 |

**必须先修正的 KuaiSim 接口条件**：固定快照 `2ae32aa25a0aac103194a66e6864e3d2ac6d6580` 的 `model/general.py` 将 `preds` 经 sigmoid 放入 `probs`；所检查的 `KREnvironment_WholeSession_GPU.py` 又对该字段施加 sigmoid 后减相似性惩罚。原 `KRMBUserResponse` 小批前向核实了前一合同。例如 logit=0 时第一步得到 0.5，第二步变成约 0.62246。适配必须明确传 logits 还是 probabilities，并为其做数值核查；本轮未修改第三方源码、未重跑整环境，不由此断言所有环境或论文原结果都受影响。详见[检查记录](../context-recovery/plan_v3_kuaisim_probe.json)。

LLM_User_Simulator 的 `YelpLoader` 读取 `dataset/MO_dataset.pkl`，环境加载 `user_response_model/best_model.pth`，快照没有这两项，且未见顶层 LICENSE。将它定位为方法依据比安排直接集成更可执行；公开可读不自动授权重分发代码／资产。

### 2.4 新数据与评价方法

| 来源 | 本轮实际取得／检查 | 采用与边界 |
|---|---|---|
| [KuaiSAR 官方](https://kuaisar.github.io/)；[Zenodo 8181109](https://zenodo.org/records/8181109) | 完整 `KuaiSAR_v2.zip`，845,087,902 bytes，官方 MD5 匹配；每表最多前 5,000 行读取 | 有推荐／搜索／用户／物品／社交表。caption 与 keyword 实物是数字列表，不能直接读语义；同用户时间重复说明严格视频先后需额外处理。前缀统计不是总体比例 |
| [KuaiRand](https://kuairand.com/) / [KuaiRec](https://kuairec.com/) | 沿用已下载全量版本及核查，不重复宣称新获取 | 1K/Pure 多反馈、有限随机池、KuaiRec 近全观测矩阵各自服务验证；27K 新增规模尚未下载，不是当前主实验输入 |
| [Open Bandit Pipeline](https://github.com/st-tech/zr-obp)；[论文](https://arxiv.org/abs/2008.07146) | 新克隆，README、`obp/ope/estimators.py` 的 pscore/action_dist 与 IPS 接口；PDF 的任务设定 | OPE 是有前提的成熟方案。普通点击日志不提供按钮处理概率；随机插入也不自动识别新动作序列的长期结果。本轮未运行 OPE |
| 原 TikTok／YouTube 审计 | 已有全文和代码的阅读状态见旧台账，v3 选择主张相关的可复算部分 | 各平台、时点、入口和操作不同；不能合成按钮强度榜或完整中国平台结论 |

## 3. 尚未完成及为何不影响本轮规划定稿

未完成：跨议题人工金标准、VLM/Omni/Agent 的本任务实测、KuaiSim 真实训练与长序列验证、生产平台控制、真人意图与获益评价。没有宣称所有可得资源都已穷尽、全部文献已复现或已选出最高准确率模型。

本轮定稿需要的是更广且与问题相关的候选覆盖、实际输入与代码检查、可运行路径证据、明确缺口和有判据的执行方案。这些已转为 WP0–WP7；真正的模型竞赛、标注与干预实验属于执行阶段。模型选择保留可证伪性，研究主线与评价合同保持稳定。

## 4. 本版正式 Plan 建议保留的来源组

压缩到课程 4–6 页时，不把所有工具逐个写进文献综述。约 5–10 项精选：问题定义／参与与认可错位、短视频同题立场审计、用户控制困扰、UCRS、观点与理由度量、ShortVideo、KuaiRand/KuaiRec 的数据依据、SimTok、KuaiSim／混合用户方法、独立用户模拟评价。可按实际篇幅从各组选择，不把多个独立来源伪装成一项引用。

工程工具的版本和资源表放附属材料；正文重点说明**它们如何帮助回答这个具体问题，以及什么证据会让我们放弃一种方法**。
