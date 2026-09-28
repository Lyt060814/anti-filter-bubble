# KuaiRec / KuaiRand：数据集由来与已有研究

> 2026-09-27 整理。✅ = 已打开 arXiv 原页面或 Semantic Scholar API 核实；引用数取自 Semantic Scholar，时间为 2026-09-27。

## 1. 数据集本身

| | KuaiRec ✅ | KuaiRand ✅ |
|---|---|---|
| 论文 | Gao, C., Li, S., Lei, W., Chen, J., Li, B., Jiang, P., He, X., Mao, J., & Chua, T.-S. (2022). *KuaiRec: A Fully-observed Dataset and Insights for Evaluating Recommender Systems*. CIKM '22. arXiv:2202.10842 | Gao, C., Li, S., Zhang, Y., Chen, J., Li, B., Lei, W., Jiang, P., & He, X. (2022). *KuaiRand: An Unbiased Sequential Recommendation Dataset with Randomly Exposed Videos*. CIKM '22 Resource Paper. arXiv:2208.08696 |
| 作者背景 | 中国科学技术大学（何向南团队）、新加坡国立大学、四川大学，加上快手员工（Li Biao、Jiang Peng 等） | 同一团队 |
| 为什么做 | 推荐系统很难离线评估：已有数据是"部分观测"的，没被推荐过的内容不知道用户会不会喜欢。于是让 1,411 个用户几乎被曝光了全部 3,327 个视频 | 线上日志有**曝光偏差**（只记录算法选中的内容）。于是在两周内往推荐流中**随机插入视频**，记录用户对这些随机视频的 12 种反馈（点击、点赞、观看时长等） |
| 论文自己的发现 | 数据密度和曝光偏差会**改变不同推荐算法的优劣排名**，而用模型去"猜"缺失交互只能在部分情况下补救 → 证明全观测数据是必要的 | 这是一篇**资源论文**：主要贡献是数据本身，用于去偏、交互式推荐、长序列建模等研究 |
| 引用数 | 286 | 218 |

**结论：** 两个数据集都是**为学术研究而发布的**。原始目的是**评估推荐算法**和**消除曝光偏差**，**不是**为了研究信息茧房。但它们很快被用来研究茧房。

## 2. 用它们研究"茧房"的已有工作

### 2.1 同一团队：直接研究 filter bubble ✅

- **CIRS**：Gao, C., Wang, S., Li, S., Chen, J., He, X., Lei, W., Li, B., Zhang, Y., & Jiang, P. (2023). *CIRS: Bursting Filter Bubbles by Counterfactual Interactive Recommender System*. ACM TOIS. arXiv:2204.01266。引用 137。
  - **核心观点：** 一直推用户喜欢的东西会造成"过度曝光"，让用户**厌倦、满意度下降**。所以茧房应该放在**交互式、多轮**的推荐里研究，目标是**长期满意度**。
  - **方法：** 离线强化学习 + 因果推断。先从历史数据学出一个"会因过度曝光而厌倦"的因果用户模型，再用它训练推荐策略。
  - 用 KuaiRec 搭了一个评估环境 **KuaiEnv**；代码公开。
  - **结论：** CIRS 能"破泡"，并获得更高的长期满意度。
- **DORL**：Gao, C., Huang, K., et al. (2023). *Alleviating Matthew Effect of Offline Reinforcement Learning in Interactive Recommendation*. SIGIR '23. arXiv:2307.04571。引用 97。
  - 发现：常用的离线强化学习推荐方法会造成严重的**马太效应**，热门的类别越推越多，冷门的越来越少。
  - 方法：加一个惩罚项，惩罚会导致"状态不够多样"的动作。
  - 在 KuaiRec 和 KuaiRand 上实验。
- **KuaiSim**：Zhao, K., et al. (2023). *KuaiSim: A Comprehensive Simulator for Recommender Systems*. arXiv:2309.12645（快手团队）。基于 KuaiRand 的用户模拟器。

### 2.2 其他团队的相关研究 ✅

- **Deep Filter Bubble**：Sukiennik, N., Gao, C., & Li, N. (2024). *Uncovering the Deep Filter Bubble: Narrow Exposure in Short-Video Recommendation*. WWW '24. arXiv:2403.04511（清华，使用"中国头部短视频平台"一年的数据，有三级类别）。
  - 定义了"深茧房"：在大类兴趣内部，只看到很窄的细分内容。
  - **发现：处于茧房中的用户比例随时间基本不变，但茧房的"深度构成"在变**；某些人群更容易看到窄内容；**隐式反馈信号可以减少茧房形成**。
  - 与我们 KuaiRec 快速查看的结果（"被展示的多样性"两个月内基本稳定）方向一致。
- **Bubble Escape Potential（BEP）**：Feng, D., Xu, Q., Wang, Z., Hua, C., Yang, Z., & Huang, Q. (2025). *Quantifying the Potential to Escape Filter Bubbles: A Behavior-Aware Measure via Contrastive Simulation*. AAAI '25. arXiv:2512.03067。
  - 提出一个"**逃离茧房的难易程度**"指标：给合成用户设定不同的行为倾向（正反馈 vs 负反馈），比较由此产生的曝光差异。
  - **发现：推荐准确度和"可逃离性"之间存在两难；轻度随机推荐不能缓解茧房（反直觉）。**
  - 和"破茧按钮有没有用"的问题**高度相关**。

### 2.3 统计

在引用这三篇论文的工作中，标题含 bubble / cocoon / diversity / Matthew / popularity / fair / polariz 等关键词的：KuaiRec 25 篇、KuaiRand 20 篇、CIRS 29 篇（有重叠）。完整引用列表见同目录 `kuai_citations.json`（Semantic Scholar API 导出）。
- 主体是**机器学习方法论文**：提出新的 RL、因果、公平性算法，并与已有基线比较。
- 2025–2026 年仍有新工作，例如：*Rethinking Homogeneity in Interactive Recommendation: Dynamic Fine-Grained Control for Mitigating Filter Bubbles*（ACM TWeb 2026）、*Mitigating Filter Bubble from the Perspective of Community Detection*（arXiv 2508.11239）、*Understanding the Information Cocoon: A Multidimensional Assessment…*（arXiv 2509.11139）。

## 3. 对我们意味着什么

1. **"用 KuaiRec/KuaiRand 研究茧房"本身不新**，而且已有工作的技术门槛（离线强化学习、因果推断）远超一年级。我们**不能**把"提出一个更好的破茧算法"作为卖点。
2. **可以直接复用和引用：**
   - CIRS 的 KuaiEnv 环境和代码；
   - Deep Filter Bubble 的"深茧房"定义与发现；
   - BEP 的"可逃离性"思路以及"轻度随机推荐无效"的结论。
   这些可以作为我们的**基线**和**对照**。
3. **可能的空白（需进一步核实）：**
   - 已有工作几乎都是 ML 方法视角。用**真实平台的真实机制**（X 2026 的公开打分公式、中国平台的破茧功能）去做**透明、可解释**的比较，似乎没人做。
   - KuaiRand 的 `is_hate` 负反馈 + `is_rand` 随机曝光，能直接检验"**用户点了讨厌之后，该类内容是否减少、持续多久**"。尚未找到专门做这件事的论文（**待确认**）。
   - 把这类数据分析与**中国监管要求的"破茧"功能**、**2026 年 9 月的政策讨论**联系起来，已有 ML 文献不涉及。
