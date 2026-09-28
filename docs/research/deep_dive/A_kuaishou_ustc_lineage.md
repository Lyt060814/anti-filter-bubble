# 深挖 A：快手 / 中科大（高崇铭、何向南等）信息茧房研究脉络

> COMP1110 小组项目 · 文献与代码深挖 · 2026-09-28
> 范围：KuaiRec → KuaiRand → CIRS → DORL → KuaiSim → 同一脉络的 2024–2026 工作
> 方法：用 pdfplumber 读了 5 篇 arXiv 全文（方法、实验、结果部分），读了本地 CIRS / DORL / KuaiRand 仓库源码。下载了 KuaiRand-Pure 并算了统计量，还在 CPU 上把 CIRS 的 **原版 KuaiEnv** 跑通，接了几个简单策略。
> 所有脚本和输出都在 `scratchpad/deep_A/` 下（文件路径见文末附录）。

---

## 0. 一页速览（TL;DR）

| 工作 | 这条线里的作用 | 对我们最有用的东西 |
|---|---|---|
| **KuaiRec**（CIKM'22） | 「几乎全观测」矩阵：1,411 用户 × 3,327 视频，密度 99.6% | 可以直接当「真实偏好」查表的模拟器底座（KuaiEnv） |
| **KuaiRand**（CIKM'22） | 在正常推荐流里**随机插入**视频，得到无偏（MAR）反馈，12 种信号，含 `is_hate` | 可以比较「算法推荐 vs 随机曝光」的类别集中度，也可以研究负反馈 |
| **CIRS**（TOIS'23） | 把 filter bubble 定义成「过度曝光同类内容 → 满意度下降 → 用户无聊退出」，提出 KuaiEnv | KuaiEnv 可以单独使用（我们已跑通），还有过度曝光效应公式 |
| **DORL**（SIGIR'23 最佳论文提名） | 离线 RL 的「保守主义」会造成马太效应；给出 MCD 指标和熵惩罚 | MCD 指标、重复率 vs 次日留存的实证、KuaiRand 环境 |
| **KuaiSim**（NeurIPS'23） | 快手 + 港城大做的多行为、跨会话用户模拟器（含离开和留存） | 留存模块，可以研究「茧房 → 留存」 |

**我们自己跑出来的关键数字：**

1. **KuaiRand-Pure 统计**（从 Kaggle 的 CC BY-SA 镜像下载。文件大小和官方 README 逐一吻合，行数也和官方 1,436,609 / 1,186,059 完全一致）：
   - 规模：27,285 用户，7,583 视频，2,622,668 条交互。
   - 随机曝光：`is_rand==1` 占 45.2%。这是 Pure 版本只保留候选池视频造成的，全量 27K 版本中随机替换只占约 0.37%。
   - `is_hate==1`：共 2,061 次。其中随机曝光 1,351 次（发生率 0.114%），正常推荐 710 次（0.049%）。有过 hate 的用户 722 人。
   - 日期：正常日志 2022-04-09 至 04-21、2022-04-22 至 05-08；随机日志 04-22 至 05-08。
   - 标签：`tag` 字段有 46 个类别 id，每个视频 1–3 个标签，96 个视频没有标签。
2. **算法推荐确实更集中**：11,176 个用户各抽 20 次曝光比较。正常推荐的首位标签占比 0.312，随机曝光为 0.215。20 次曝光里平均出现的不同标签数分别是 9.49 和 11.87。69.7% 的用户在算法流里更集中。
3. **「hate 之后同类曝光会不会下降」目前答不出来**：用 Pure 做粗略前后对比，差异和对照组没有区别。原因是 Pure 的序列太稀疏，需要 KuaiRand-1K 或 27K（详见 §2）。
4. **KuaiEnv 可以被一条简单规则「攻破」**：规则是「按训练集流行度排序，跳过和上一条共享类别的视频」，不需要任何学习。
   - CIRS 的设定（N=1，最多 100 轮）：这条规则累计奖励 **172.8**，满 100 轮。CIRS 官方日志最后 20 个 epoch 平均 **122.5**，CIRS w/o CI 为 99.2。
   - 30 轮设定：规则 **64.5**，CIRS 57.2。
   - 同一环境下随机策略的结果（7.08 / 8.0 轮）和官方日志（6.66 / 7.7 轮）几乎一致，说明我们复现的环境是对的。
   - 含义：这些基准里的「无聊退出」是一条确定性的类别规则，它测的其实是「策略能不能学会避开相邻同类」，而不是「能不能帮用户走出茧房」。

---

## 1. KuaiRec 卡片

**引用**：Chongming Gao, Shijun Li, Wenqiang Lei, Jiawei Chen, Biao Li, Peng Jiang, Xiangnan He, Jiaxin Mao, Tat-Seng Chua. *KuaiRec: A Fully-observed Dataset and Insights for Evaluating Recommender Systems.* CIKM 2022, pp. 540–550. arXiv:2202.10842. 网站 https://kuairec.com

**研究问题**：离线评估用的交互数据都是部分观测的（大部分用户-物品对缺失，而且缺失不是随机的）。缺失和曝光偏差到底会怎样影响推荐（特别是多轮对话推荐 CRS）的评测结论？

**对茧房/气泡的定义**：本文不直接研究茧房。它研究的是**曝光偏差**（positivity bias、popularity bias）和**数据密度**对评测的影响，后续 CIRS 和 DORL 都把它当作环境底座。

**数据怎么来的（重点：怎么让用户几乎看过所有视频）**
- 平台和时间：快手 App，2020-07-05 至 2020-09-05。
- 步骤：先去掉广告、垃圾视频和作弊账号，再挑出一批用户和视频，让这些用户尽量看过这些视频。对于还没看过的视频，作者「**操纵线上推荐规则，把这些视频插入推荐流**」，确保每个视频都被展示过并收到反馈。**这个强制曝光过程持续了 15 天。**
- **small matrix**：1,411 用户 × 3,327 视频，密度 99.6%。缺的 0.4% 是因为有些用户主动屏蔽了某些作者。
- **big matrix**：7,176 用户 × 10,728 视频，密度约 16.3%，是 small matrix 的外围数据，用于训练。small matrix 中的交互全部**从 big matrix 剔除**，这样训练和测试不重叠。
- **代表性检验**：用 6 个用户特征和 6 个视频特征做双样本 KS 检验，p 值都大于 5%，作者据此说明样本能代表全平台。
- **其他信息**：31 个人工标注的类别标签（每个视频 1–4 个）；用户特征 30 维（其中 18 个加密的 one-hot）；视频每日统计 45 个字段；社交网络。2024 年 6 月新增 `kuairec_caption_category.csv`，包含标题和三级中文类别，面向 LLM 研究。
- **许可**：CC BY-SA 4.0。

**`watch_ratio` 的含义**：`play_duration / video_duration`，即观看时长除以视频时长。
- 大于 1 表示重复播放。
- 论文把「累计观看时长超过 2 倍视频时长」定义为正样本（官网示例：`like = 1 if watch_ratio > 2.0`），没有用「点赞」，因为点赞太稀疏。
- 我们实测 small matrix 的 `watch_ratio`：均值 0.907，中位数 0.769，p99 为 3.59，**最大值 571.5**。≥2 的只占 4.6%（big matrix 为 7.5%），>5 的占 0.49%。CIRS 和 DORL 的环境都把它截断在 5。

**方法（通俗讲）**：用 small matrix 当「标准答案」，从中按三种方式抽样，合成密度 10%–90% 的部分观测数据：
- 均匀随机抽样；
- 偏正向抽样：按 big matrix 中的「被喜欢次数」成比例抽；
- 偏流行抽样：Zipf 分布，P(k) ∝ 1/k^0.5。

然后比较 8 种 CRS 方法在不同合成数据上的排名，看排名是否一致。还尝试用 PMF、ExpoMF、ExpoMF-cov 补全缺失值，看能否恢复真实排名。

**指标**：AT（平均轮数）、SR@15（15 轮内成功率）、Recall@10/20（补全效果）、排名不一致次数（Table 3）。

**主要发现**
1. 在有偏曝光下，方法的绝对表现和排名都随密度剧烈变化。
2. 在多目标（MTG）设定下，**即使是均匀随机曝光**，不同密度也会给出不一致的结论。
3. 矩阵补全**只在偏差不严重时部分有用**。例如均匀曝光下，EAR 在 SR@15 上的排名不一致次数从 7 降到 5；但在 AT 上几乎没有帮助，有时还会引入新误差。

**局限和已知问题**（论文承认的 + 我们发现的）
- 作者承认：高密度不可避免地带来流行度偏差。
- **强制曝光**：small matrix 里很大一部分交互是被「插进来」的视频，时间顺序是插入流程的产物，不是自然的推荐序列。所以 small matrix 不适合研究「推荐系统怎样随时间把人推进茧房」这类动态问题。
- 我们实测：small matrix 有 **181,992 行 timestamp 为空**；big matrix 有 **2,229,837 个重复的「用户-视频」对**（重复观看），使用时要先去重或聚合。
- `watch_ratio` 和视频时长强相关：短视频容易循环播放，比值偏高。
- 只有 1,411 个用户，偏好被当成静态的。
- 版本差异：KuaiRec 2.0 把列名 `photo_id` 改成了 `video_id`，并去掉了 ID=1225 的视频，旧代码（CIRS）直接读会报 KeyError。

**代码**：数据加载脚本和统计 notebook 在 kuairec.com 与 DORL 仓库的 `environments/KuaiRec/KuaiRec-data/`。CRS 评测流程在 github.com/xiwenchao/fully_observed_demo（我们没有运行）。

**我们可以复用什么**
- small matrix 可以当「真实满意度查表」：任何推荐策略都能在上面离线算出**真实**奖励，不需要训练用户模型。
- 31 个类别标签，加上 2024 年新增的三级中文类别，可以用来算类别熵、首位类别占比等茧房指标。
- 可以引用的结论：部分观测和曝光偏差会**改变**模型排名，所以离线评测里的「diversity 提升」也要谨慎解读。

**它留下的空白**
- 没有研究茧房本身，偏好被假设为静态。
- 强制曝光的伦理与用户知情问题没有讨论。
- 没有用户主动行为（搜索、屏蔽、「不感兴趣」）如何影响曝光。
- 没有任何面向监管或非 ML 读者的解读。

---

## 2. KuaiRand 卡片

**引用**：Chongming Gao, Shijun Li, Yuan Zhang, Jiawei Chen, Biao Li, Wenqiang Lei, Peng Jiang, Xiangnan He. *KuaiRand: An Unbiased Sequential Recommendation Dataset with Randomly Exposed Videos.* CIKM 2022, pp. 3953–3957. arXiv:2208.08696. 网站 https://kuairand.com，数据在 Zenodo 10439422。许可 CC BY-SA 4.0。

**研究问题**：日志数据有曝光偏差，而已有的随机曝光数据集（Yahoo! R3、Coat、Open Bandit）规模太小，或者缺少用户 ID、时间戳、特征。能否在**真实推荐流**中大规模收集随机曝光下的用户反馈？

**茧房/气泡**：引言提到曝光偏差「会引发 filter bubbles」，但全文不定义也不测量。

**随机曝光是怎么插入的**
1. 抽一批视频，去掉广告等垃圾内容，得到**7,583 个视频的候选池**；再随机抽一批真实用户，去掉机器人（超过 20 万人）。
2. 系统每次给用户推一个视频列表时，**以固定概率（具体数值出于商业原因保密）**决定是否干预。如果干预，就从列表里随机选一个位置，用候选池中**均匀随机**抽到的视频替换。用户不知道这件事。持续时间 **2022-04-22 至 2022-05-08**。
3. 去掉随机曝光少于 10 次的用户，剩 **27,285 人**。所有 7,583 个视频都至少被插入过一次，随机干预总数 **1,186,059**。README 说全量数据中约 **0.37%** 的交互是被替换的。
4. 另外收集了这些用户在 **2022-04-08 至 04-21** 的正常推荐历史，以及跨 15 个场景（tab 0–14，每个场景一种推荐策略）的日志。

**反馈信号**：论文说有「12 种反馈信号」。日志里能看到的反馈字段是：
- 二值信号：`is_click`（双列界面是点击，单列界面是 valid_play）、`is_like`、`is_follow`、`is_comment`、`is_forward`、`is_hate`、`long_view`、`is_profile_enter`；
- 连续值：`play_time_ms`、`profile_stay_time`、`comment_stay_time`。

合计 11 个，另有 `duration_ms`、`is_rand`、`tab`、时间字段。README 没有逐一点名第 12 种信号。`is_hate` 的描述只有一句「用户 hated 这个视频」，没说明对应 App 里的哪个按钮（很可能是「不感兴趣」类操作，**需要核实**）。视频统计表里另有**聚合层面**的 `reduce_similar_cnt`（「减少类似内容」）和 `report_cnt`，但它们不在交互层面。

**三个版本**

| 版本 | 大小 | 用户 | 视频 | 正常交互 | 随机交互 |
|---|---|---|---|---|---|
| 27K | 23 GB 日志 + 23 GB 特征 | 27,285 | 32,038,725 | 322,278,385 | 1,186,059 |
| 1K | 829 MB 日志 + 3.5 GB 特征 | 1,000 | 4,369,953 | 11,713,045 | 43,028 |
| Pure | 184 MB 日志 + 10 MB 特征 | 27,285 | 7,551 / 7,583 | 1,436,609 | 1,186,059 |

Pure 只保留候选池内 7,583 个视频的日志，所以**正常序列是不完整的**（被大量过滤）。

另外，2026 年新增了补充文件（Zenodo 18159199）：`kuairand_video_categories.csv`（四级中文类别，由模型预测并附概率）和 `kuairand_video_captions.csv`（标题文本）。本次 Zenodo 对我们的网络返回 403，**没有下载**。

**我们对 KuaiRand-Pure 的实测**
- 下载来源：Kaggle 镜像 `arashnic/an-unbiased-sequential-recommendation-dataset`（CC BY-SA 4.0，50 MB zip），因为 Zenodo 被拦截。各文件大小和官方 README 一致，行数和官方统计一致。
- 存放位置：`/home/user/data/kuairand/KuaiRand-Pure/KuaiRand-Pure/data/`。
- 脚本：`analysis/kuairand_pure_stats.py`、`analysis/kuairand_concentration.py`、`analysis/hate_followup.py`。

| 指标 | 数值 |
|---|---|
| 用户 / 视频 / 总交互 | 27,285 / 7,583 / 2,622,668 |
| 随机日志 | 1,186,059 行（全部 `is_rand==1`），日期 20220422–20220508 |
| 正常日志 04-08~04-21 | 1,141,112 行，26,210 用户，日期 20220409–20220421 |
| 正常日志 04-22~05-08 | 295,497 行，25,877 用户 |
| Pure 中 `is_rand==1` 占比 | 45.2% |
| `is_hate==1` 总数 | 2,061（随机 1,351，正常 710）；有过 hate 的用户 722 人 |
| hate 发生率 | 随机 0.114%，正常 0.049% |
| 点击 / long_view / like | 正常 46.0% / 33.2% / 1.85%；随机 17.6% / 8.5% / 0.48% |
| 每用户交互数 | 中位数 73；每用户随机曝光中位数 22（最少 10，最多 1,580） |
| 标签 | 46 个 tag id；每视频 1 个（5,696）、2 个（1,759）、3 个（32）；96 个无标签 |
| 用户活跃度 | full_active 17,959，high 6,158，middle 2,133，其余是新用户和低活用户 |

**「算法推荐 vs 随机曝光」的类别集中度**（同一个 7,583 视频池内比较，比较公平）

| | 全局首位标签占比 | 前 5 标签占比 | 标签熵 | 每用户 20 次曝光中的不同标签数 | 每用户首位标签占比 |
|---|---|---|---|---|---|
| 正常推荐 | 0.257 | 0.583 | 4.08 bits | 9.49 | 0.312 |
| 随机曝光 | 0.184 | 0.514 | 4.35 bits | 11.87 | 0.215 |

69.7% 的用户（共比较 11,176 人）在正常推荐里更集中。这是「推荐算法收窄曝光」的一个**干净的描述性证据**：随机曝光提供了天然的对照组。

**「负反馈会不会减少之后同类曝光？」能否回答**：**原则上可以，但用 Pure 做不到。**
- 我们的粗略做法：对每个 hate 事件，比较该用户在事件前后正常推荐里、被 hate 视频首位标签的占比（前后各至少 5 条）。

| 事件类型 | 样本数 | 前后变化 | 标准误 |
|---|---|---|---|
| 所有 hate | 1,102 | −0.69 个百分点 | 0.34 |
| 对正常推荐视频的 hate | 587 | −1.51 个百分点 | 0.45 |
| 对随机插入视频的 hate | 515 | +0.25 个百分点 | 0.51 |
| **对照**：未点击且未 hate | 2,713 | −0.57 个百分点 | 0.21 |
| **对照**：long_view | 3,574 | −1.27 个百分点 | 0.19 |

- 结论：hate 组和对照组**没有可分辨的差异**，前后下降主要来自均值回归和时间趋势。
- 原因：Pure 的正常序列被过滤到只剩候选池视频，事件后中位数只有 9–35 条；hate 本身也很稀少。
- 要认真回答，需要 KuaiRand-1K：日志约 850 MB，但 tag 在 3.5 GB 的 video_features 里，总量超过 1 GB，本次没有下载。设计上应改用事件研究 / 双重差分，以匹配的「未 hate 同类曝光」事件为对照，按 tab 分层。

**局限**
- 插入概率保密。
- 随机视频被插在正常推荐之间，用户对它的反应会受上下文影响（位置效应、落差感）。
- 随机曝光的点击率天然很低，可能部分来自「来自陌生类别的冲击」。
- Pure 的序列不完整。
- 只有两周干预，看不到长期的兴趣变化。
- 特征大多加密，没有内容语义（2026 年补充的标题和类别部分弥补了这一点）。

**代码**：`load_data_*.py`（只是 pandas 读取示例）。DORL 仓库里有 `preprocessing_kuairand.py` 和 KuaiRand 环境。

**我们可以复用什么**
- **随机 vs 算法**这个天然对照可以直接量化「算法收窄程度」（我们已给出初步数字）。
- `is_hate` 和其他 11 种信号可以研究负反馈。
- `user_active_degree` 可以按用户类型分层。
- `tab` 可以按场景（首页、精选等）分层。

**它留下的空白**
- 没有分析茧房。
- 没有研究用户主动逃离行为（hate、搜索、关注新作者）的**后续效果**。
- 没有长期（数月）的兴趣演化。
- 没有平台机制（如「不感兴趣」按钮的实际权重）的说明。

---

## 3. CIRS 卡片

**引用**：Chongming Gao, Shiqi Wang, Shijun Li, Jiawei Chen, Xiangnan He, Wenqiang Lei, Biao Li, Yuan Zhang, Peng Jiang. *CIRS: Bursting Filter Bubbles by Counterfactual Interactive Recommender System.* ACM TOIS 42(1), Article 14, 2023（arXiv:2204.01266）。代码 github.com/chongminggao/CIRS-codes，MIT 许可。

**研究问题**：怎样在**交互式推荐**（多轮、序列决策）里，从离线日志学到一个能「戳破」filter bubble、最大化**长期累计满意度**的策略？

**filter bubble 的定义**
- 原文说法：用户「被隔离于和其主导偏好不同的信息之外」。作者认为主要原因是算法的**过度利用（over-exploitation）**。
- 作者明确选择「**用过度曝光效应（overexposure effect）作为 filter bubble 的代理**」。
- 核心假设 Hypothesis 1：同类内容在短时间内反复曝光时，用户满意度会下降。
- 所以在这里，「茧房」被操作化为**短期重复同类内容导致的厌倦**，而不是观点、立场或长期兴趣的收窄。

**实证观察（田野研究）**
- 数据：快手 7,176 个用户，2020-08-05 至 08-11，共 34,215,294 次观看、3,110,886 个视频、31 个标签。
- 满意度用两个指标衡量：评论区停留时长、观看比例。
- 发现：(a) 过去 1 小时内看过的同标签视频越多，这两个指标越低；(b) 距离上次看同标签视频越近，指标越低。
- 这是**相关性**结论，没有控制用户活跃度、会话位置等混杂因素。

**方法（通俗讲 + 关键公式）**：三步循环。
1. 离线学一个「因果用户模型」φ_M：把满意度拆成「内在兴趣」和「过度曝光效应」。
2. 用这个用户模型给的**反事实满意度**当奖励，训练 PPO 策略。状态由 Transformer 状态追踪器加门控机制产生。
3. 在环境里评估。

关键公式：
- 过度曝光效应 (8)：
  `e_t(u,i) = α_u · β_i · Σ_{(u,i_l,t_l)∈S, t_l<t} exp( −(t − t_l)/τ × dist(i, i_l) )`
  - α_u：用户对重复的敏感度；
  - β_i：物品「耐看程度」的倒数（论文称 unendurableness，比如流行歌比古典乐更容易听腻）；
  - τ：温度参数；
  - dist：在 KuaiEnv 中是类别 multi-hot 向量的 Hamming 距离。
  - 直观理解：越相似、越近期看过的内容，贡献的厌倦越大。
- 满意度 (9)：`r̂_t = ŷ_ui / (1 + e_t(u,i))`，其中 ŷ 用 DeepFM 估计。KuaiEnv 上用 BPR 损失训练，VirtualTaobao 上用 MSE。
- 反事实干预 (11)(12)：在 RL 规划阶段执行 do(E_t = e*_t)，用**策略自己新产生的轨迹**重新计算曝光效应。`e*_t = γ* · α_u β_i Σ exp(−(t−t_l*)/τ* × dist)`，其中 γ* 固定为 10；`r̂* = ŷ/(1 + e*)`。
- 学到的参数：α_u 与用户活跃度正相关，β_i 与物品流行度正相关（Fig. 9）。

**KuaiEnv 是怎么工作的**（读源码 `environments/KuaishouRec/env/kuaishouEnv.py`）

| 组成 | 具体做法 |
|---|---|
| 用户 | 每个 episode 从 1,411 人中均匀随机抽一个 |
| 状态 | 用户 id，或上一个动作（item id） |
| 动作 | 在 3,327 个视频中选一个（整数） |
| 奖励 | small matrix 中该用户对该视频的 `watch_ratio`；截断到 5，NaN/inf 用均值填补；偏好是静态的 |
| 「无聊退出」 | 取最近 N 个已推荐视频，统计各类别出现次数。若当前视频的任一类别出现次数 > 阈值，episode 结束（退出那一步的奖励仍然计入） |
| 回合长度 | `max_turn` = 100 或 30 |
| 论文参数 | N=1，n_Q=1 |
| 实际脚本参数 | `num_leave_compute=1, leave_threshold=0`，即**只要和上一个视频共享任一类别就退出**。论文写的 n_Q=1 在 N=1 时永远不会触发，所以以代码为准 |

**指标**
- 累计满意度 Σr（主指标，100 条轨迹的平均）；
- 交互长度；
- 单轮满意度；
- 日志中还记录了 `ifeat_feat`，即主导类别占比（后来 DORL 的 MCD）。

**基线**
- 静态模型：DeepFM、IPS、PD、DICE，推荐时都用 softmax 采样；
- 简单策略：Random、ε-greedy、UCB；
- CIRS w/o CI（没有因果模块的 PPO）；
- VirtualTaobao 上用 MLP。

**数据集和环境**：只有 **VirtualTaobao**（改了退出机制：与最近 5 个推荐的欧氏距离小于 d_Q 就退出）和 **KuaiEnv**（基于 KuaiRec）两个。**没有用 Coat 或 Yahoo**，这两个在 DORL 仓库里。

**主要定量结果**：论文只给了图。我们从仓库自带日志 `reproduce_results_of_our_paper/results_all_methods/` 提取了最后 20 个 epoch 的平均值：

| KuaiEnv，最多 100 轮 | 累计奖励 | 长度 | 单轮奖励 | 主导类别占比 |
|---|---|---|---|---|
| **CIRS** | **122.5** | 99.6 | 1.23 | 0.39 |
| CIRS w/o CI | 99.2 | 98.3 | 1.01 | 0.50 |
| DeepFM + softmax | 13.8 | 5.6 | 2.46 | 0.78 |
| DICE / PD / IPS | 13.8 / 12.0 / 11.3 | 5.6 / 4.8 / 6.9 | 约 1.6–2.5 | 约 0.8 |
| Random | 6.7 | 7.7 | 0.87 | 0.80 |
| ε-greedy / UCB | 5.4 / 5.0 | 2.3 / 2.0 | 2.3 / 2.5 | 0.98 / 1.00 |

30 轮设定：CIRS 57.2，CIRS w/o CI 35.2。

论文的定性结论：
- 静态模型单轮奖励高，但很快就触发退出。
- RL 方法用更低的单轮奖励换来更长的交互。
- 当用户更挑剔（N≥4 或 d_Q≥4）时，CIRS 也不再有优势；N=5 时甚至不如 DeepFM 或 MLP。

**局限**
- 满意度 = 静态的 `watch_ratio`，偏好不会变化。
- 「无聊」是**写死的、确定性的类别规则**，没有用真实数据校准。
- 类别只有 31 个，而且粗糙。
- 用户在 episode 之间没有记忆，不存在长期茧房的形成过程。
- 田野研究是相关性分析。
- 没有真实用户实验。
- 研究对象是短期重复，不是信息多样性或观点隔离。

**我们的复现和发现（重要）**
- 做法：把原版 `kuaishouEnv.py` **原样复制**到 scratchpad。只做了三处必要改动：
  1. 把没用到的 `torch` 换成占位模块（step() 不需要它）；
  2. 跳过 10,728² 的纯 Python 相似度矩阵计算（很慢，而且 step() 不使用）；
  3. 用本地 KuaiRec 2.0 重建 `item_categories.json` 和 `photo_mean_duration.json`（原本在 Zenodo 的 "environment data.zip" 里，被网络拦截），并把列名 `video_id` 改回 `photo_id`。
- 环境：Python 3.11，gym 0.26，**CPU 上加载只要 3.6 秒**，100 条轨迹几秒就能跑完。
- 结果（每行 100 条轨迹，seed=0，脚本 `kuaienv_run/run_kuaienv_trivial.py`）：

| 设定 | 策略 | 累计奖励 | 长度 | 单轮奖励 | 主导类别占比 | 覆盖类别数 |
|---|---|---|---|---|---|---|
| CIRS 设定（N=1，最多 100 轮） | random | 7.08 | 8.0 | 0.91 | 0.87 | 6.7 |
| | 流行度贪心（训练集 big matrix） | 12.5 | 5.0 | 2.51 | 0.80 | 4.0 |
| | 真值贪心（oracle，作弊上界） | 28.4 | 6.4 | 4.63 | 0.91 | 5.3 |
| | ε-greedy（oracle，ε=0.1） | 28.5 | 7.0 | 4.22 | 0.90 | 5.8 |
| | **流行度 + 避开上一条类别（只用训练集）** | **172.8** | **100** | 1.73 | 0.91 | 18 |
| | oracle + 避开上一条类别 | 291.7 | 100 | 2.92 | 0.87 | 19.7 |
| CIRS 设定（N=1，最多 30 轮） | 流行度 + 避开类别（训练集） | **64.5** | 30 | 2.15 | 0.83 | 15 |
| DORL 设定（N=4，M=0，最多 30 轮） | 流行度 + 避开类别（训练集） | 64.1 | 30 | 2.14 | 0.80 | 15 |
| | random | 4.19 | 4.7 | 0.88 | 0.88 | 5.0 |

- 结论：
  - 一条**不需要学习、不看测试数据的规则**，在 CIRS 自己的环境里超过了 CIRS（172.8 对 122.5；30 轮设定下 64.5 对 57.2）。
  - 这不是说 CIRS 没价值：CIRS 需要从数据中**学出**过度曝光效应。但它说明 KuaiEnv 的退出机制是可以被「知道规则的人」精确利用的。
  - 同时说明，「更长的交互 = 更少的茧房」这个等式依赖于人为设定的退出规则。
- 注意：随机策略的结果和官方日志吻合（7.08/8.0 对 6.66/7.7），说明环境复现正确。

**代码难度**
- 技术栈：Python 3.9 + PyTorch 1.9（cu111），仓库内附带**修改过的** tianshou 和 DeepCTR-Torch，还需要 gym、scikit-learn、logzero 等。
- 算力：README 建议 8 卡服务器，训练 200–1000 个 epoch。
- 数据：需要下载 environment data.zip。
- 评价：**完整复现对大一团队偏难**。但只用 KuaiEnv 当环境、接自己写的简单策略，**非常可行**（我们已经跑通）。

**我们可以复用什么**
1. KuaiEnv 本身（加上我们的最小运行脚本）。
2. 过度曝光公式 (8)(9)：可以作为「厌倦」的**参数化**用户模型，用 KuaiRand 数据校准 τ、α、β。
3. 田野研究的指标设计：同标签 1 小时计数、同标签间隔。在 KuaiRand 上可以复刻。
4. 官方日志里的数字可以作为对比基线（上表）。

**它留下的空白**
- 茧房被窄化为短期厌倦，没有长期兴趣收窄，没有观点或信息层面的茧房。
- 退出规则没有真实数据校准，可以被利用。
- 没有用户主动逃离行为（搜索、「不感兴趣」、换 tab）。
- 没有平台机制和监管视角（例如中国《互联网信息服务算法推荐管理规定》要求提供「不针对个人特征」的选项）。
- 没有非技术受众。

---

## 4. DORL 卡片

**引用**：Chongming Gao, Kexin Huang, Jiawei Chen, Yuan Zhang, Biao Li, Peng Jiang, Shiqi Wang, Zhong Zhang, Xiangnan He. *Alleviating Matthew Effect of Offline Reinforcement Learning in Interactive Recommendation.* SIGIR 2023（最佳论文荣誉提名）。arXiv:2307.04571。代码 github.com/chongminggao/DORL-codes，MIT 许可。

**研究问题**：离线 RL 为了防止「价值高估」而引入保守主义（惩罚不确定的状态-动作对）。放到推荐里，这会不会加剧**马太效应**？怎样在保持准确的同时缓解它？

**马太效应和茧房的定义**
- 马太效应：「富者愈富」。之前数据里流行的物品或类别以后更容易被推荐，冷门的被忽略。
- 作者把它和 filter bubble 联系起来：重复推荐某些内容会伤害满意度。
- **经验证据**：在 KuaiRand-27K 和 LFM-1b（Last.fm 1.09 亿次收听）上，按日活跃度分组后，**重复率越高，次日留存（Day-1 Retention）越低**。
  - 重复率 = 当天观看次数 ÷ 不同视频数（或不同类别数）。
  - 例子：看 20 次、5 个不同视频、3 个不同类别，则视频级重复率 = 4.0，类别级 = 6.67。
  - 快手规定同一视频不推第二次，所以视频级重复很少见，类别级重复才是重点。

**方法（通俗讲 + 关键公式）**
- 基于 MOPO 的模型式离线 RL：用 DeepFM 学一个用户模型（世界模型）当伪环境，给策略打分。
- MOPO 的奖励：`r̃ = r̂ − λ·p(s,a)`，惩罚项 p 取模型的不确定性。作者指出，λ 越大（越保守），单轮奖励越高，但 **MCD 也越高**（Fig. 3），即马太效应越强。
- DORL 的奖励 (9)：`r̃(s,a) = r̂(s,a) − λ₁ P_U + λ₂ P_E`
  - **P_U**：不确定性惩罚，取 K 个高斯概率 DeepFM 集成中预测方差的最大值，同时包含认知不确定性和偶然不确定性。
  - **P_E**：熵项，定义为 `P_E = −D_KL(π_β(·|s) ‖ π_u(·|s)) = H(π_β(·|s)) − log|A|`。π_β 是日志里的行为策略，π_u 是均匀策略。
  - 实际计算：在所有日志里找出「前 k 个物品构成的集合 → 下一个物品」这样的子序列，统计频率得到熵，再对 k=1,2,… 求和，归一化到 (0,1]。
  - 直观理解：如果日志在某个状态下只推过很少几种东西（熵低），模型对那里的「高分」就不太可信，于是给低熵状态更多惩罚。这样**间接鼓励策略走向更多样的状态**，作者称之为「反事实探索」。
- 其余部分：状态追踪器是最近 N 个（物品嵌入 ⊕ 奖励）的平均；策略用 Actor-Critic。

**指标**
- R_tra：累计奖励；
- R_each：单轮奖励；
- Length：长度；
- **MCD（Majority Category Domination）**：推荐物品中属于「主导类别」的比例。主导类别是训练集正反馈里覆盖 80% 的最热门类别；论文说 KuaiRand 是 13/46，KuaiRec 是 12/31。

**环境**
- KuaiEnv：KuaiRec small matrix，奖励是归一化观看比例。
- **KuaiRand 环境**：用 KuaiRand-Pure 的**随机曝光日志做矩阵补全**，得到 27,285 × 7,583 的「真值」矩阵，奖励是 `is_click`。这是一个模拟出来的矩阵，不是真实的全观测数据。
- 退出机制：前 N 轮里有超过 M 个同类别物品就退出；主实验 M=0，N=4，最多 30 轮。
- 另外代码里还有 Coat 和 Yahoo 环境。

**主要定量结果**（Table 2，200 个 epoch 平均）

| | KuaiRec R_tra | 长度 | MCD | KuaiRand R_tra | 长度 | MCD |
|---|---|---|---|---|---|---|
| UCB | 3.61 | 4.2 | 0.81 | 1.65 | 4.4 | 0.79 |
| ε-greedy | 3.52 | 4.2 | 0.82 | 1.71 | 4.9 | 0.77 |
| BCQ | 2.12 | 3.0 | 0.67 | 0.85 | 2.0 | 1.00 |
| MBPO | 12.04 | 15.6 | 0.36 | 10.93 | 25.3 | 0.31 |
| IPS | 12.83 | 16.7 | 0.22 | 3.63 | 16.8 | 0.20 |
| MOPO | 11.43 | 12.8 | 0.48 | 10.93 | 25.0 | 0.34 |
| **DORL** | **20.49** | **26.7** | 0.38 | **11.85** | **27.6** | 0.30 |

- 提高 λ₂（熵惩罚）会让交互更长、MCD 更低（Fig. 8）。
- N=1 时其他模型式方法可以超过 DORL；N>3 时 DORL 最好（Fig. 9）。
- 超参：KuaiRand 取 λ₁=0.01，λ₂=0.05；KuaiRec 取 λ₁=0.05，λ₂=5。

**我们对 MCD 的核查**
- 仓库里的 `feature_domination.pickle` 按代码规则算出的主导类别是 KuaiRec 10 个、KuaiRand 12 个，和论文写的 12 个、13 个略有出入。
- 更关键的是：在 KuaiRec small matrix 中，主导类别覆盖了约 **83%** 的视频。所以**均匀随机策略的 MCD 就有 0.8–0.87**（我们实测 0.865，CIRS 日志中 Random 为 0.797）。
- 而 DORL 的 MCD 是 0.38，IPS 是 0.22，**远低于随机水平**。这说明这些策略其实是在系统性地「避开」热门类别，而不是「中性地多样」。
- 结论：**MCD 没有中性参照点**，数值越低不一定越好。使用时应该报告「相对随机基线」的值，或者改用类别熵、和用户兴趣分布的 KL（校准度）等指标。

**局限**
- 同样依赖写死的类别退出规则。
- KuaiRand 环境的「真值」来自矩阵补全，是模拟的。
- 马太效应只在类别层面度量。
- 次日留存的实证是相关性结论。
- 没有用户侧行为。
- 我们的实验显示，「避开前 N 个类别」这一条规则在 N=4 时就能跑满 30 轮（DORL 平均 26.7 轮），但两边的奖励尺度不同（DORL 用的是归一化奖励），所以只能比较长度。

**代码**
- 技术栈：Python 3.10，torch，**tensorflow**，numba，gym，scikit-learn；需要作者 fork 的 tianshou。
- 数据：环境包解压后约 **12 GB**（来自作者 NAS 或 USTC 盘）。README 推荐 8 卡服务器。
- 好处：仓库附带了全部论文日志（`results_for_paper/`），可以直接画图、做表。Coat 和 Yahoo 环境很小，跑得快。
- 评价：完整复现偏难；读日志、复用 MCD 评估函数（`src/core/evaluation/evaluator.py`）和环境类很容易。

**我们可以复用什么**
1. MCD 指标（`get_feat_dominate_dict`），最好加上随机基线归一化。
2. **重复率 → 次日留存**的分析框架：可以在 KuaiRand-1K 或 27K 上复刻，也能换成「类别熵」。
3. KuaiRand 环境类（如果能拿到 12 GB 数据包）。
4. 可以引用的结论：「保守的离线 RL 会放大马太效应」，以及「重复率与次日留存负相关」。

**它留下的空白**
- 马太效应只在类别层面，没有内容语义。
- 留存结论只是相关性，没有因果。
- 没有用户干预或逃离行为。
- 没有平台规则（如同一视频不重复推送）以外的机制分析。
- 没有监管视角。

---

## 5. KuaiSim 卡片（简要）

**引用**：Kesen Zhao, Shuchang Liu, Qingpeng Cai, Xiangyu Zhao, Ziru Liu, Dong Zheng, Peng Jiang, Kun Gai. *KuaiSim: A Comprehensive Simulator for Recommender Systems.* NeurIPS 2023。arXiv:2309.12645。代码 github.com/Applied-Machine-Learning-Lab/KuaiSim，Apache-2.0。作者来自快手和香港城市大学，**不是高崇铭团队**，但同样用快手数据。

**模拟什么**
- **即时反馈模块**：用 Transformer 编码用户历史，输出多种行为的概率。其中减去 `ρ × item_correlation(推荐列表)`，用来模拟用户对**列表内多样性**的需求。
- **离开模块**：用户有一个「耐心值」，初始等于最大会话长度，每一步按即时奖励扣减，低于阈值 T 就离开。
- **留存模块**：次日回访概率 `p_ret = b_u + λ₁ r_t + λ₂ b`（个人偏置 + 满意度偏置 + 全局偏置），回访天数服从几何分布，最多 10 天。
- 支持三类任务：请求级（列表推荐）、会话级（RL）、跨会话级（留存优化）。
- 数据：KuaiRand-Pure（50-core 过滤，每天算一个会话；27,077 用户，7,551 物品，246,738 个会话），也可以换成 ML-1m。

**结果**
- 会话级：HAC 最好，深度 14.98，总奖励 10.17。
- 跨会话：RLUR 回访天数 3.48，留存率 0.607。
- 和 RecSim、RL4RS、VirtualTaobao 等比较时，KuaiSim 的 AUC 最高（0.723）。

**对新手是否友好**
- 中等偏难。
- 有 shell 脚本（先训练用户反馈模型，再生成会话数据，最后跑基线），要求 Python 3.8 + PyTorch，需要 KuaiRand-Pure 和一个预处理 notebook。
- README 没写 GPU 要求。星标 38，维护较少。
- 本次**没有运行**。

**对茧房研究的价值**
- 它的离开和留存模块可以用来问「多样性不足会不会降低留存」。
- 但多样性只体现在「列表内相关性」和 ILD/coverage 指标里，没有跨时间的类别收窄。

**留下的空白**
- 茧房和马太效应都没有专门度量。
- 用户模型是黑箱，很难解释「为什么离开」。
- 没有用户主动行为。

---

## 6. 同一脉络的其他工作（2023–2026）

| 工作 | 与茧房的关系 | 备注 |
|---|---|---|
| **SPRec: Self-Play to Debias LLM-based Recommendation**（WWW'25，arXiv:2412.09243，Gao, Chen, Yuan, Huang, Yu, He） | 发现**DPO 对齐会让 LLM 推荐偏向少数物品、加剧 filter bubble**，用自博弈的 SFT+DPO 纠偏 | LLM 推荐里的茧房，和 X/ChatGPT 类问题相关 |
| **DLCRec**（WSDM'25，arXiv:2408.12470，Chen, Gao 等 + 快手） | LLM 推荐多样性下降；让用户指定「想要几个类别」来控制多样性 | 用户可控的多样性 |
| **How Do Recommendation Models Amplify Popularity Bias? A Spectral Perspective**（WSDM'25 最佳论文，arXiv:2404.12008，Lin, Gao, Chen 等） | 流行度被记在分数矩阵的主奇异向量里，维度坍缩会放大它；用谱范数正则化纠偏 | 马太效应的机理解释 |
| **BiLLP: LLMs are Learnable Planners for Long-Term Recommendation**（SIGIR'24，arXiv:2403.00843） | 用 LLM 做长期规划，**用的是 CIRS 和 DORL 同款的交互环境与退出规则** | 继承了同一套评测范式 |
| **MocDT: Future-Conditioned Recommendations with Multi-Objective Controllable Decision Transformer**（arXiv:2501.07212） | 准确度和多样性等多目标可以直接「指定」 | 离线 RL 续作 |
| **Agentic Feedback Loop Modeling**（SIGIR'25，arXiv:2410.20027，Cai, …, Gao, …, He） | 推荐 agent 和用户 agent 互相反馈；用 LLM 模拟用户 | 讨论过反馈回路的偏差 |
| **Tunable LLM-based Proactive Recommendation Agent**（ACL'25，Wang, Gao, Wang, Li, Feng） | **主动推荐**：多步引导用户形成潜在兴趣，明确以对抗回音室为目标 | 「平台主动带用户出茧房」的方向 |
| 相邻但**不是**本脉络：*Uncovering the Deep Filter Bubble*（WWW'24，Sukiennik, **Chen Gao**, Nian Li；清华，不是高崇铭） | 用某头部中国短视频平台一年数据和三级类别，定义「深度茧房」：在宽兴趣内部的狭窄曝光 | **注意作者同姓不同人**；数据不公开，但定义可以借鉴 |
| 相邻：*RecLoop*（arXiv:2606.17707，2026） | 用 LLM 用户 agent 做闭环模拟，看生成式推荐会不会加深信息茧房 | 2026 年的最新方向 |
| 相邻：*RecBot / Interactive Recommendation Feed*（arXiv:2509.21317，淘宝） | 用户在推荐流里用**自然语言指令**主动调整策略 | 工业界的「用户侧逃离」，可以作为对照 |

补充：同圈子（中科大、新国大）较早还有 *User-controllable Recommendation Against Filter Bubbles*（Wang 等，SIGIR 2022）。**本次没有核实原文**，引用前需要确认。

---

## 7. 综合（Synthesis）

**这条研究线怎样理解 filter bubble**：它把问题完全放在**推荐系统优化**的框架里，而且要解决的是**平台的长期指标**。
- CIRS 把「茧房」操作化为「短期内同类内容过度曝光 → 满意度下降 → 用户无聊离开」；
- DORL 把它归为离线 RL 保守主义造成的**马太效应**（类别集中，用 MCD 度量），并用「重复率越高，次日留存越低」来论证它伤害用户；
- KuaiSim 进一步把「离开」和「留存」建模为用户模拟器的一部分。

所以在这里，打破茧房 = **延长会话、提高留存**。这是一个平台和用户利益一致的叙事。

**隐含的假设**
1. 用户偏好是静态的，由 `watch_ratio` 或点击决定（KuaiRec small matrix 被当作「真值」）；
2. 「厌倦」是确定性的、只看类别重叠的规则，而且没有用真实数据校准；
3. 类别标签（31 或 46 个）足以代表「信息多样性」；
4. 用户是被动的，只会看或者离开，不会搜索、点「不感兴趣」或换 tab；
5. 更长的会话等于更少的茧房。

这些假设让问题变成干净的 ML 基准，但也让结论依赖模拟器的设计。我们的实验说明：一条「避开上一条同类」的手写规则就能在 KuaiEnv 中超过 CIRS，而 MCD 指标没有中性参照。整条线**没有讨论**观点和信息层面的茧房、用户主体性、平台真实机制，也没有涉及监管（例如 2022 年施行的《互联网信息服务算法推荐管理规定》第十七条要求提供「不针对个人特征的选项」或便捷关闭算法推荐；2024 年「清朗·网络平台算法典型问题治理」专项行动点名整治「信息茧房」。**这两条请在引用前核对原文**）。

**大一团队可以可信地填补的空白**（按可行性排序，新颖性如实说明）

1. **「基准体检」：简单规则 vs 复杂 RL**
   - 做法：系统地展示 KuaiEnv 和 DORL 的退出规则能被类别轮换规则利用（我们已有初步结果：172.8 对 CIRS 122.5）。再提出**用 KuaiRand 真实数据校准的随机退出模型**，例如从日志估计「近 k 条同类数 → 短看或划走的概率」，在新环境下重新比较简单策略。
   - 新颖性：中等。「模拟器有效性」是已知的一般议题，但针对 KuaiEnv 的具体批评我们没有检索到（需要再查）。
   - 算力：只需 CPU。
2. **「算法到底把曝光收窄了多少」的描述性研究**
   - 做法：用 KuaiRand 的随机曝光当对照（我们已测：首位标签占比 0.31 对 0.22，不同标签数 9.5 对 11.9）。按用户活跃度、tab、时间（4 月 8 日到 5 月 8 日）分层，报告对非技术读者也能看懂的指标。
   - 新颖性：偏低到中等。数据集论文没有做这个分析，适合课程项目，而且完全可复现。
3. **用户主动逃离行为的效果**
   - 做法：(a) 用 KuaiRand-1K 的完整序列（约 4.3 GB）做事件研究，看 hate、关注新作者之后同类曝光有没有变化（Pure 上我们的粗略结果不显著，这本身就是一个诚实的起点）；(b) 在 KuaiEnv 里给模拟用户加上「不感兴趣」「搜索新类别」动作，看需要多少次主动操作才能明显提高类别熵。
   - 新颖性：中等。这条脉络完全没有做用户侧；工业界有 RecBot 这类相邻工作；SIGIR'22 的用户可控推荐需要核实。
4. **指标批判与改进**
   - 做法：说明 MCD 低于随机基线的含义，提出「相对随机的 MCD」、类别熵、和用户兴趣分布的 KL（校准度），在 CIRS 和 DORL 官方日志上重新计算（日志都在仓库里，不需要训练）。
   - 新颖性：中等偏低，但成本极低。
5. **把监管机制放进模拟**
   - 做法：在 KuaiEnv 里实现「非个性化选项」或「一键关闭算法推荐」（对应《算法推荐管理规定》第十七条），也可以实现按比例混入非个性化内容，量化满意度和多样性之间的取舍，写成政策简报。
   - 新颖性：在 CS 文献里这个组合较少见，但要说清楚这是「玩具模拟」，不代表真实平台效果。

---

## 附录 A：本次产出的文件（均为绝对路径）

- 报告：`/tmp/claude-0/-home-user-anti-info-bubble/1f4c2ddc-5a5f-5603-ba08-ecece8726e00/scratchpad/deep_A/deep_A_kuaishou_lineage.md`
- 论文 PDF 和抽取的文本：`.../scratchpad/deep_A/{2202.10842,2208.08696,2204.01266,2307.04571,2309.12645}.{pdf,txt}`
- KuaiRand-Pure 数据：`/home/user/data/kuairand/KuaiRand-Pure/KuaiRand-Pure/data/`（Kaggle 镜像 zip 的 md5 为 `2f7eba04da3af32c3951327720468881`）
- 统计脚本和输出：`.../scratchpad/deep_A/analysis/`，包括 `kuairand_pure_stats.py/.out`、`kuairand_concentration.py/.out`、`hate_followup.py/.out`、`kuairec_stats.py/.out`
- KuaiEnv 最小运行：`.../scratchpad/deep_A/kuaienv_run/`
  - `kuaishouEnv_orig.py`：原版逐字复制；
  - `run_kuaienv_trivial.py` 和 `run_len30.py`：运行脚本；
  - `kuaienv_trivial_results*.csv/.txt`：结果；
  - `shim/torch`、`core/util.py`：两个占位模块；
  - 虚拟环境在 `.../scratchpad/deep_A/venv`。
  - 运行命令：`cd .../kuaienv_run && ../venv/bin/python run_kuaienv_trivial.py`

## 附录 B：运行 CIRS 和 DORL 时踩到的坑

1. Zenodo 对当前网络返回 403，拿不到 CIRS 的 environment data.zip 和 KuaiRand 的补充类别文件。KuaiRand-Pure 改从 Kaggle 镜像获取。
2. KuaiRec 2.0 的列名是 `video_id`，旧代码写的是 `photo_id`。
3. CIRS 论文写 n_Q=1，脚本实际用 `leave_threshold=0`。
4. `get_distance_mat` 用 Python 双重循环计算 10,728² 的矩阵，非常慢，而 step() 并不使用它。
5. KuaiEnv 在模块顶部 import torch，但 step() 不需要。
6. 用的是旧版 gym API（step 返回 4 元组）；gym 0.26 下直接调用类方法没有问题。
7. DORL 需要 tensorflow 和 12 GB 的环境数据。

## 参考来源

- KuaiRec：https://arxiv.org/abs/2202.10842 ，https://kuairec.com/
- KuaiRand：https://arxiv.org/abs/2208.08696 ，https://kuairand.com/ ，https://github.com/chongminggao/KuaiRand ，Kaggle 镜像 https://www.kaggle.com/datasets/arashnic/an-unbiased-sequential-recommendation-dataset
- CIRS：https://arxiv.org/abs/2204.01266 ，https://github.com/chongminggao/CIRS-codes
- DORL：https://arxiv.org/abs/2307.04571 ，https://github.com/chongminggao/DORL-codes
- KuaiSim：https://arxiv.org/abs/2309.12645 ，https://github.com/Applied-Machine-Learning-Lab/KuaiSim
- 其他：https://arxiv.org/abs/2412.09243 ，https://arxiv.org/abs/2408.12470 ，https://arxiv.org/abs/2404.12008 ，https://arxiv.org/abs/2403.00843 ，https://arxiv.org/abs/2501.07212 ，https://arxiv.org/abs/2410.20027 ，https://aclanthology.org/2025.acl-long.944/ ，https://arxiv.org/abs/2403.04511 ，https://arxiv.org/abs/2606.17707 ，https://arxiv.org/abs/2509.21317 ，高崇铭主页 https://chongminggao.com/
