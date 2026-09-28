# Deep Dive D：推荐反馈回路的仿真研究与平台审计研究（信息茧房 / filter bubble）

> 面向 HKU COMP1110 小组项目。日期：2026-09-28。
> 所有结论均来自 arXiv/开放版论文原文（用 pdfplumber 提取阅读）、本地仓库和我们自己实际跑的代码。**凡是没能读到全文的地方会明确标注。**
> 工作目录：`/tmp/claude-0/-home-user-anti-info-bubble/1f4c2ddc-5a5f-5603-ba08-ecece8726e00/scratchpad/deep_D/`（下文简称 `deep_D/`）

---

## 0. 一页速查

| # | 工作 | 类型 | 代码/数据能否复用 | 对我们最有用的一点 |
|---|---|---|---|---|
| 1 | Chaney+ 2018 (RecSys) | 仿真 | 官方代码**未找到**；T-RECS 有复现 | 用户模型（Dirichlet 偏好 + 位置偏差）、Jaccard 同质化、Gini |
| 2 | T-RECS（Lucherini+ 2021） | 仿真库 | `pip install trecs` 在现代 Python 上**直接装会失败**；我们找到一组能跑的版本组合；CPU 上约 1–3 s/50 步（MF 约 26–41 s） | 现成的 Content/Popularity/MF/Social/Random 模型 + drift + 同质化指标 |
| 3a | Jiang+ 2019 (AIES) | 理论+仿真 | 无代码，模型极简，可自己复现 | 兴趣 “degeneracy” 定义；oracle/TS/UCB/random 对比；候选池增长可减缓退化 |
| 3b | Mansoury+ 2020 (CIKM) | 离线仿真（MovieLens-1M） | 无代码链接；数据公开 | 接受概率 e^{α·rank}；流行度放大、覆盖率下降、少数群体偏移更大 |
| 3c | Kalimeris+ 2021 (KDD) | 理论+仿真+Facebook 实验 | **未能获取全文**（无 arXiv 版） | 随机推荐温度 β、偏好放大的条件、全局/个人两级缓解 |
| 4a | Geschke, Lorenz & Holtz 2019 | ABM（NetLogo） | 代码开源（GitHub + Zenodo 1407733） | 三重过滤：认知/社交/技术；12 个场景的定量表 |
| 4b | Sîrbu+ 2019 (PLoS ONE) + NDlib | ABM（有界信任） | NDlib `AlgorithmicBiasModel`，我们已跑通 | 一个参数 γ 就能表达“算法偏向相似者”，碎片化与收敛变慢 |
| 5 | Tomlein+ 2021 / Srba+ 2023 | 平台审计（YouTube） | 代码和数据都在本地仓库（48 MB）；**我们已复算出论文的 Table 并重画了曲线** | “陷入—戳破”曲线；戳破比陷入更快、更突然 |
| 6a | Mosnar+ 2025 (SIGIR) | 审计复现（TikTok） | Zenodo 16792218 **只有论文 PDF**；原始 JSON 在 GitHub `data/` | 审计结果短期有效、可复现性差；“看完视频”这个隐式信号比点赞/关注更强 |
| 6b | Pecher+ 2026 (UMAP) | 审计（TikTok 漂移） | Zenodo 19144520 **受限访问**（需学术邮箱申请）；分析代码在 GitHub | 三种 drift 的定义；误导信息类话题被“中和”、美国政治话题维持均衡 |
| 7 | Hosseinmardi+ 2024 (PNAS) | 反事实 bot（YouTube） | 数据来自商业面板，**不公开** | 反事实 bot 的设计；侧栏大约 30 个视频就“遗忘”旧偏好 |

**一句话结论**：给一年级团队的最佳路线是**用自己写的约 200 行 numpy 仿真**（参数照搬 Chaney/Jiang/T-RECS），而不是去魔改 T-RECS（它依赖太老）；实证部分**直接复用 yaudit 数据**（本地可用，pandas 十几行就能复现论文的表和图）。

---

## 1. Chaney, Stewart & Engelhardt (2018)

**Citation**：A. J. B. Chaney, B. M. Stewart, B. E. Engelhardt. *How algorithmic confounding in recommendation systems increases homogeneity and decreases utility*. RecSys '18, pp. 224–232. arXiv:1710.11214. DOI 10.1145/3240323.3240370。

**研究问题**：推荐系统用“被自己推荐影响过的数据”反复训练（algorithmic confounding），会带来什么后果？

**Bubble 的定义**：论文没有直接用 “filter bubble” 这个词做度量，而是用**用户行为同质化**（homogenization）来刻画：相似用户消费的物品集合越来越重合，而且超过了“理想推荐”下应有的程度。作者把 “tyranny of the majority” 和 niche “echo chamber” 都解释为推荐模型的 **over-exploitation**。

**模型 / 协议**
- 真实效用：$V_{ui}\sim \text{Beta}'(\rho_u\alpha_i^\top)$（Beta 分布，均值为 $\rho_u\alpha_i^\top$，方差固定为 $10^{-5}$）
- 偏好与物品属性：$\rho_u\sim\text{Dir}(\mu_\rho)$，$\alpha_i\sim\text{Dir}(\mu_\alpha)$，维度 K=20。**用户偏好不均匀**：$\tilde\mu_\rho\sim\text{Dir}(1)$，$\mu_\rho=10\tilde\mu_\rho$；**物品属性总体均匀但单个稀疏**：$\tilde\mu_\alpha\sim\text{Dir}(100)$，$\mu_\alpha=0.1\tilde\mu_\alpha$
- 用户“已知”的那部分效用：$P_{ui}=\eta_{ui}V_{ui}$，$\eta_{ui}\sim\text{Beta}'(0.98)$，其余 $Q=(1-\eta)V$ 用户自己不知道
- 选择规则（带位置偏差）：$i_u(t)=\arg\max_i\, f(\text{rank}_{u,t}(i))\cdot P_{ui}$，其中 $f(n)=n^{-0.8}$（根据点击研究拟合）
- 每个用户每步恰好交互 1 个物品，同一物品最多交互一次；每步新增 10 个物品，与推荐结果交错（interleave）
- 规模：**100 用户，1000 步，每步 10 个新物品，10 个随机种子**
- 对比 6 种推荐：popularity、content filtering（二值属性，用 NNLS 学用户偏好）、MF（Gaussian PMF with confidence weighting，a=1, b=0.001）、social filtering（社交网络由用户偏好协方差二值化得到，有同质性）、random、ideal（按真实 V 排序）
- 两种训练范式：(i) **single training**：50 步随机 “start-up” 后只训练一次，再观察 50 步；(ii) **repeated training**：10 步 start-up 后每步都用全部历史重新训练，共 90 步
- 统一打分框架：$s_{ui}(t)=\theta_u(t)\beta_i(t)^\top$，排序时 tie 要随机打破（作者特别强调这一点，否则 random 基线会占便宜）

**指标**
- 同质化：每个用户按推荐系统的 $\theta$ 找余弦最相似的伙伴 v，计算 $J_{uv}(t)=\frac{|D_u\cap D_v|}{|D_u\cup D_v|}$，**再减去 ideal 推荐下同一对用户的 Jaccard**。把伙伴换成随机配对，就得到“全局同质化”
- 效用：相对 ideal 的效用
- 物品消费不平等：Gini $G(t)=\frac{\sum_i(2RP(i,t)-|I|-1)\sum_u 1[i\in D_u(t)]}{|I|\sum_i\sum_u 1[i\in D_u(t)]}$

**主要发现**（原文以图为主，几乎没有表格数值）
1. single training：训练后短暂轻度同质化，随后回落到 ideal 水平；**repeated training：除 random 外所有算法的同质化都持续上升，而效用没有相应提高**（Fig. 3）
2. 全局（随机配对）同质化：popularity 最强，MF 和 social 次之，content 最弱，但都高于 ideal（Fig. 4）
3. **效用越低的用户同质化越高**（Fig. 5 的散点和线性拟合），说明代价分布不均
4. 同质化程度相近时，物品消费分布可以差别很大，比如 MF 的 Gini 高于 content（Fig. 6）
5. 初步试了加权（propensity 类）方法，发现可以同时提高效用、降低同质化（没有展开）

**局限**：utility 被假定为静态、用户偏好不变（没有 preference drift）；每步必须交互一次；图多数字少，很难做精确比较；ideal 基线依赖对效用的假设。

**代码/数据**：作者主页 https://ajbc.xyz/projects/recsys-feedback-loops.html 只链接论文和幻灯片，**没有找到官方仿真代码**。T-RECS 论文说他们 “did not seek out source code”，而是按论文从零复现，复现代码在 https://github.com/sunnymatt/t-recs-experiments （在 T-RECS 中每组跑 400 次试验，结论定性一致）。

**我们可以复用什么**：整套用户生成参数（Dirichlet 超参数、K=20、100 用户）；位置偏差 $f(n)=n^{-0.8}$；“相对 ideal 的 Jaccard 同质化” 和 Gini 公式；single 与 repeated training 的对照设计；“每个用户一个点”的效用–同质化散点图。

**它留下的空白**：用户偏好不变；没有负反馈（跳过、“不感兴趣”）；没有多样化重排（MMR/DPP/作者多样性）；没有与真实平台审计数据做校准。

---

## 2. T-RECS（Lucherini, Sun, Winecoff, Narayanan 2021）+ 本地仓库

**Citation**：E. Lucherini, M. Sun, A. Winecoff, A. Narayanan. *T-RECS: A Simulation Tool to Study the Societal Impact of Recommender Systems*. arXiv:2107.08959。代码：https://github.com/elucherini/t-recs （本地 `/home/user/elucherini/t-recs`，最新提交 0de83a3，2022-10-05，版本 0.2.1，MIT 许可）。

**研究问题**：提供一个通用的 agent-based 仿真框架，用来研究推荐系统的社会影响，并通过“概念复现” Chaney+2018 和 Goel+2016（structural virality）来验证框架。

**框架（论文 §4 与源码）**
- 四个模块：Users（真实偏好 $U$ 与系统预测 $\hat U$ 分开存储）、Items/Creators（可以动态生成物品）、Model（推荐算法）、Metrics
- 每步流程：模型预测分数 → 给每个用户展示 `num_items_per_iter`（默认 10）个物品，可混入随机物品 → 用户按真实分数选 1 个 → 模型更新内部状态 → 记录 metrics
- 默认分数：内积（也可以换成 cosine 或自定义 `score_fn`）
- `Users(drift=…)`：用户偏好向消费过的物品向量“旋转漂移”，drift∈[0,1]
- `Users(attention_exp=…)`：选择规则为 $\arg\max_i \text{rank}^{\alpha}\cdot S_{ui}$，与 Chaney 的位置偏差相同
- `repeat_interactions=False`：不重复消费
- 内置模型（`trecs/models`）：`ContentFiltering`、`PopularityRecommender`、`ImplicitMF`（基于 lenskit ALS）、`SocialFiltering`、`RandomRecommender`、`BassModel`（信息扩散）
- 内置指标（`trecs/metrics/measurement.py`，**本版本没有 `HomogeneityMeasurement` 这个类**，同质化由 `InteractionSimilarity` 提供）：
  - `InteractionMeasurement`：每步每个物品的交互直方图
  - `InteractionSimilarity(pairs)`：给定用户对的交互集合平均 Jaccard，即 Chaney 同质化
  - `RecSimilarity(pairs)`：给定用户对的推荐列表 Jaccard
  - `InteractionSpread`：交互分布的变化（排序直方图面积差）
  - `MSEMeasurement`、`RMSEMeasurement`：预测分数与真实分数的误差
  - `AverageFeatureScoreRange`（afsr）：推荐列表的属性极差，即列表内多样性（Willemsen 2016）
  - `DiffusionTreeMeasurement`、`StructuralVirality`：扩散树与结构病毒性

**论文中的复现结果**：Chaney 复现（100 步，每步 10 个新物品，single 模式 50 步 start-up，repeated 模式 10 步 start-up，每模型 400 次试验）定性一致：repeated training 的同质化远大于 single；random 与 ideal 接近。Goel 复现（100 万节点无标度图，α∈{2.1,…,2.9}，r∈{0.1,…,0.9}，约 210 万次仿真）在 r≈0.5、α≈2.3 时，结构病毒性约 3.7，popular cascade 概率约千分之一，与原文一致。

**我们实际的安装测试**（2026-09-28，本机 CPU）
- `python3.11 -m venv … && pip install trecs` → **失败**：setup.py 硬性要求 `pandas==1.0.5`，它在 Python 3.11 上无法构建
- Python 3.8（用 `uv venv -p 3.8`）+ `uv pip install trecs` 可以装上，但 `import trecs` **失败**：新版 numpy 删掉了 `np.bool`，pandas 1.0.5 依赖它
- 降到 numpy 1.19.5 后，numba 0.58 又要求 numpy≥1.22 → 继续降级
- **可以运行的组合**：Python 3.8、trecs 0.2.1、numpy 1.19.5、pandas 1.0.5、numba 0.53.1、llvmlite 0.36.0、lenskit 0.13.1、scipy 1.10.1、networkx 3.1。安装命令：
  ```bash
  uv venv -p 3.8 venv38
  VIRTUAL_ENV=$PWD/venv38 uv pip install trecs "numpy==1.19.5" "numba==0.53.1" "lenskit==0.13.1"
  ```
- 我们的小实验（`deep_D/trecs_demo/demo.py`）：100 用户、500 物品、K=20、Chaney 式 Dirichlet 偏好、drift=0.05、attention_exp=−0.8、不重复消费、10 步 start-up + 50 步 repeated training。输出见 `deep_D/trecs_demo/demo_output.txt`：

| 模型 | 60 步耗时 (CPU) | Jaccard（相邻编号用户对，末步） | RecSim | 用户真实偏好平均两两余弦（前→后） |
|---|---|---|---|---|
| ContentFiltering | 2.5 s | 0.135 | 0.033 | 0.580 → 0.574 |
| PopularityRecommender | 1.4 s | **0.774** | 0.438 | 0.580 → **0.984** |
| RandomRecommender | 1.5 s | 0.071 | 0.010 | 0.580 → 0.860 |
| ImplicitMF | 26–41 s | 0.133 | 0.070 | 0.580 → 0.844 |

  说明：(1) 用户对取的是 (u, u+1)，**不是** Chaney 那种按相似度配对，所以这些数只能说明“能跑通”，不能当研究结论。(2) 有 drift 时，random 也会让偏好趋同（都向物品的平均方向漂移），这提醒我们 **drift 模型本身就会制造“同质化”**，必须设 drift=0 作为对照。(3) `ImplicitMF` 在 `train_between_steps=True` 时会警告“每步用最新一次交互**覆盖**重训”，与 Chaney 用全部历史重训的做法不同，是个容易踩的坑。(4) `ContentFiltering.run` 接受 `disable_tqdm`，`ImplicitMF.run` 不接受，API 不统一。

**第一年学生能用吗？** 能用，但**不推荐作为主力**。优点：3 行代码就能跑，有现成的 Chaney 指标，示例 notebook 较完整（`examples/quick-start.ipynb`、`complete-guide.ipynb`、`advanced-metrics.ipynb`）。缺点：需要专门的 Python 3.8 环境和一组固定的老版本依赖；仓库从 2022 年起就没人维护；要加“不感兴趣”、作者多样性、DPP 重排，必须继承 `BaseRecommender` 并理解它内部的矩阵约定，而这部分文档很薄。**建议**：只把 T-RECS 当作“对照/校验”（比如用它复现一条 Chaney 曲线来检验我们自写仿真是否合理），主仿真自己用 numpy 写。

**它留下的空白**：没有负反馈动作；没有重排/多样化模块；没有多指标仪表盘；依赖已经过时。

---

## 3. 反馈回路理论三篇（简述）

### 3a. Jiang, Chiappa, Lattimore, György, Kohli (2019) — *Degenerate Feedback Loops in Recommender Systems*，AIES '19，arXiv:1902.10730（DeepMind）
- **定义**：把 **echo chamber** 定义为用户兴趣因反复接触而被正向或负向强化；把 **filter bubble** 定义为系统只挑有限内容给用户（沿用 Pariser），两者分开讨论。用户兴趣 $\mu_t(a)$ 如果满足 $\limsup_t\|\mu_t-\mu_0\|_2=\infty$，叫**弱退化**（weak degeneracy）；如果 $\lim=\infty$，叫**强退化**。
- **理论**：Theorem 1/2 表明，在很弱的条件下（兴趣高于某阈值时有非零概率继续上漂，低于时继续下漂），只要某个物品被展示无穷多次，兴趣就会退化。系统只能**控制退化的速度**。线性动态 $\mu_{t+1}=(1+k)\mu_t+b$ 下，oracle 模型配贪心策略退化最快。
- **仿真**：单用户；每步从 m 个候选中推 l=5 个；点击 $c\sim\text{Bernoulli}(\sigma(\mu_t(a)))$；点击则 $\mu$ 加 $\delta(a)$，否则减 $\delta(a)$，$\delta\sim U[-0.01,0.01]$，$\mu_0\sim U[-1,1]$；T=5000（部分实验 20000）；m=100（或 10–10^4）；30 次重复。
- **比较对象**：Random、Oracle（$\theta=\mu$）、Optimal Oracle（按 $\delta$ 选）、UCB、Thompson Sampling；以及 Oracle 加噪声 $U[-\epsilon,\epsilon]$（ε=0…20）。
- **发现**：退化速度 Optimal Oracle > Oracle > TS > UCB > Random。**除 Random 外，很快 top 物品和 top 兴趣都收缩到 5 个最被强化的物品**。少量随机噪声反而可能**加速**退化，噪声大了才减速。**候选池增长**（至少线性增长）是避免退化的必要条件；池更大时 UCB 最能减缓退化，而 Oracle 反而更快。
- **复用**：点击和兴趣更新规则非常适合一年级实现（每步 5 行代码）；degeneracy speed $\|\mu_t-\mu_0\|_2/t$ 可以直接当指标。**代码**：未公开，但模型足够简单，可以自己写。
- **空白**：只有单用户、物品彼此独立、没有群体层面的指标。

### 3b. Mansoury, Abdollahpouri, Pechenizkiy, Mobasher, Burke (2020) — *Feedback Loop and Bias Amplification in Recommender Systems*，CIKM '20，arXiv:2007.13019
- **离线仿真协议**：MovieLens-1M（6040 用户、3706 部电影、1,000,209 条评分；4331 男性 / 1709 女性）；每轮 80/20 切分并训练 → 为每个用户生成推荐 → 按**接受概率** $p(i|R)=e^{\alpha\cdot\text{rank}_i}$（α<0）决定选中哪个 → 用 IRT 式估计评分 $\omega=\bar s_u+sd(s_u)\bar s_i+\eta$，四舍五入并截断到 [1,5] 后加入用户画像。共 T=20 轮。算法：UserKNN、BPR（都用 50 个因子/邻居）、MostPopular。
- **理论**：$P_{R_t}\propto P_{D_t}+\theta_t$，因此 $P_{D_{t+1}}=P_{D_t}+\frac{K\theta_t}{|D_t|+K}$，平均流行度单调上升。
- **指标与发现**：推荐的平均流行度逐轮上升（BPR 最陡）；aggregate diversity（覆盖率）下降；用户画像与初始画像的 genre 分布 KL 散度随轮次上升；男女两组 genre 分布之间的 KL 大幅下降，即**群体同质化**；**少数群体（女性）的偏移明显大于男性**，并且逐渐被拉向以男性为主的总体分布。
- **复用**：接受概率公式、覆盖率、画像 KL 散度、按群体分解（主流/小众用户）。**代码**：论文没有给链接；数据公开。
- **空白**：只有 20 轮；用户“真实偏好”没有建模（只模拟画像表示）；没有缓解策略实验（只作为未来工作提出）。

### 3c. Kalimeris, Bhagat, Kalyanaraman, Weinsberg (2021) — *Preference Amplification in Recommender Systems*，KDD '21, pp. 805–815
- ⚠️ **没有 arXiv 版，未能读到全文**。以下内容来自 Meta Research 官方博客摘要（research.facebook.com/blog/2021/08/…）和后续论文（Chee+ KDD'24, arXiv:2406.09882）中的引用，**细节请以原文为准**。
- **模型**：协同过滤 / 低维 MF；用户偏好随时间“轻微自我强化”（对与自己正相关的推荐物品偏好上升，负相关则下降）；推荐是随机的，由参数 **β** 控制确定性（β 大时近似 top-N，β 小时更多样）；**α** 表示问题内容的比例。
- **定义与发现**：preference amplification 指“哪怕用户对某类推荐只有轻微偏好，也会导致该类推荐越来越集中”，系统不存在让用户偏好稳定的不动点。仿真中初始喜欢的物品被推荐的概率越来越高，不喜欢的趋于 0；**β 越大强化越强**。
- **缓解**：全局层面（移除问题实体）和个人层面（针对重度暴露用户降权）；在 Facebook 视频推荐的真实实验中，对重度暴露用户降权 borderline 内容，据博客描述**总体参与度约 +2%**，同时问题内容暴露下降。
- **复用**：softmax(β·score) 随机推荐是一个很好的“探索强度”旋钮，可以和 Jiang 的 ε 噪声对照。

---

## 4. 观点动力学 ABM 两篇 + NDlib

### 4a. Geschke, Lorenz & Holtz (2019) — *The triple-filter bubble: Using agent-based modelling to test a meta-theoretical framework for the emergence of filter bubbles and echo chambers*，Br J Soc Psychol 58(1):129–149。DOI 10.1111/bjso.12286（开放获取，全文取自 PsychArchives）
- **问题**：信息在个体（认知）、社交、技术（推荐）三个层面被过滤，什么条件下社会会碎片化成彼此隔绝的 echo chamber？
- **定义**：filter bubble 是个体层面的结果（个人的信息环境变窄）；echo chamber 是一群态度相近的人共享一个信息环境，并且与其他社群断开。
- **模型**（NetLogo 代码 `TripleFilterBubble.nlogo`，已逐行阅读）：
  - 500 个 “guys”，位于 2D 态度空间（`dims=2`）；朋友网络为 4 组随机图，平均 20 个朋友，`fraction-inter=0.2`
  - 每个 guy 记忆最多 `memory=20` 个 info-bit，**态度等于记忆中 info-bit 的均值**
  - 整合概率 $f(d;D,\delta)=\frac{D^\delta}{d^\delta+D^\delta}$，基线 **D=0.3**（acceptance latitude），**δ=20**（sharpness；δ→∞ 时退化为有界信任模型）；记忆满时随机遗忘一条
  - 新信息模式：`individual`（每人各自随机生成一条）、`central`（每步一条，推给所有人，代表大众媒体）、`select close infobits`（推荐已有的、距离 < D 的 info-bit，即“个性化推荐”）、`select distant infobits`（推荐距离 ≥ D 的，即“反推荐”）
  - 社交 posting：每人随机转发一条记忆给所有朋友；refriend：以一定概率断开态度远的朋友，改连朋友的朋友
  - 12 个场景，各跑 10^4 步
- **定量结果**（论文 Table 1，10^4 步后的平均距离，数值越小越“泡泡”）：

| 场景 | 新信息模式 | posting | D | refriend | 到 info-bits | 到 info-sharers | 到 friends |
|---|---|---|---|---|---|---|---|
| 1 | individual | off | 0.3 | 0 | 0.182 | —（没有共享 bit） | 0.840 |
| 2 | central | off | 0.3 | 0 | 0.182 | 0.285 | 0.890 |
| 3 | individual | on | 0.3 | 0 | 0.150 | 0.045 | 0.520 |
| 4 | central | on | 0.3 | 0 | 0.150 | 0.044 | 0.730 |
| 5 | filter close | off | 0.3 | 0 | 0.164 | 0.075 | 0.593 |
| 6 | filter distant | off | 0.3 | 0 | 0.278 | 0.295 | 0.829 |
| 7 | filter close | on | 0.3 | 0 | 0.144 | 0.042 | 0.707 |
| 8 | filter distant | on | 0.3 | 0 | 0.148 | 0.042 | 0.692 |
| 9 | individual | on | 0.3 | 0.01 | 0.156 | 0.041 | 0.038 |
| 10 | individual | on | 0.3 | 1 | 0.153 | 0.031 | 0.029 |
| 11 | individual | on | 0.5 | 0 | 0.257 | 0.075 | 0.070 |
| 12 | central | off | 0.5 | 0 | 0.307 | 0.456 | 0.579 |

  （表格是旋转排版，我们逐字反转解析；按原文，列依次为 info-bits / info-sharer / friends。）
- **结论**：只有认知过滤加中心化媒体（场景 2）就会出现 echo chamber，但群体之间仍共享部分信息；加上社交 posting（3、4）后，群体彼此**完全断开**；**“推荐相近信息”即使没有 posting，效果也与 posting 相当**（场景 5）；“推荐远距离信息”能在一段时间内维持一个连通的 info-sharer 网络（6），但开了 posting 后仍会分裂（8）；refriend 让朋友网络也按态度分化（9、10），但它不是碎片化的主要驱动；D=0.5 时社交媒体反而可能促成共识（11）。
- **代码**：https://github.com/janlorenz/TripleFilterBubble ，Zenodo https://doi.org/10.5281/zenodo.1407733 ，NetLogo 6.0.4；`TripleFilterBubble_Web.nlogo` 可以直接在 NetLogo Web 浏览器里跑。
- **复用**：整合概率 $f(d;D,\delta)$ 可以直接作为我们用户模型里“看到内容后是否接受/漂移”的规则；“close / distant 推荐”就是现成的**最小推荐对照组**；三种平均距离指标可以直接拿来用。
- **空白**：没有真正的推荐模型（没有学习、没有反馈回路里的“系统估计”）；结果只报告单次运行，没有置信区间；NetLogo 与我们用 Python 的课程要求不一致。

### 4b. Sîrbu, Pedreschi, Giannotti, Kertész (2019) — *Algorithmic bias amplifies opinion fragmentation and polarization: A bounded confidence model*，PLoS ONE 14(3): e0213246，arXiv:1803.02111
- **模型**：在 Deffuant 有界信任模型基础上修改。观点 $x\in[0,1]$，初始均匀分布；先随机选 i，再按 $p_i(j)=\frac{d_{ij}^{-\gamma}}{\sum_{k\ne i}d_{ik}^{-\gamma}}$ 选交互对象 j（$d_{ij}=|x_i-x_j|$，下界 $d_\epsilon=10^{-4}$）；若 $d_{ij}\le\epsilon$，则 $x_i\leftarrow x_i+\mu(x_j-x_i)$，j 同理，**μ=0.5**（即两人都取平均）。γ=0 时就是原始模型。
- **指标**：有效簇数 $C=\frac{(\sum_i c_i)^2}{\sum_i c_i^2}$（cluster participation ratio）；收敛所需交互次数 / N。
- **结果**：N=500，每组 85 次运行。ε=0.35 时原模型收敛为 1 个簇，**γ≥1.3 开始出现新簇**；ε=0.32 时 γ=1.6 的平均簇数接近 2；ε=0.2 时 γ 把簇数从 2 推向 3。收敛时间随 γ 近似按 **exp(3.4γ)** 增长（ε=0.4），所以“弱偏置在实际中也能阻碍共识”。N 越小越容易分裂（N∈{100,250,500,750,1000}）。
- **NDlib 实现**（`ndlib.models.opinions.AlgorithmicBiasModel`，NDlib 6.0.1）：参数只有 `epsilon`、`gamma` 和可选的 `initial_opinion_distribution`（uniform/normal/bimodal/polarized…）；**μ 固定为 0.5**；距离下界是 1e-5（论文为 1e-4）；每次 `iteration` 执行 N 次配对交互；可以用任意 networkx 图（只在邻居中选 j）。同目录下还有 `AlgorithmicBiasMediaModel`（加入媒体节点）。
- **我们实跑**（`deep_D/ndlib_demo/abm.py`，Python 3.11；**`pip install ndlib` 漏装了 `six` 和 `scikit-learn`，需要手动补装**）：完全图 N=200，ε=0.32，200 次 iteration，3 个种子：γ=0 → 有效簇数 1.06；γ=1.0 → 2.06；γ=1.6 → 9.00（此时仍未收敛，正好体现了“收敛极慢”）。每组约 7–8 s（CPU）。结果与论文定性一致。
- **复用**：γ 是一个“算法同质推荐强度”的单参数旋钮，可以接到我们的仿真里作为“社交层 / 评论区”的附加模块；有效簇数公式可以直接用。
- **空白**：观点是一维的；没有物品/内容，也没有推荐系统的学习过程；γ 只是一个抽象参数，与真实排序器没有对应关系。

---

## 5. YouTube 误导信息泡泡审计：Tomlein+ 2021 与 Srba+ 2023

**Citation**
- M. Tomlein, B. Pecher, J. Simko, I. Srba, R. Moro, E. Stefancova, M. Kompan, A. Hrckova, J. Podrouzek, M. Bielikova. *An Audit of Misinformation Filter Bubbles on YouTube: Bubble Bursting and Recent Behavior Changes*. RecSys '21（**Best Paper**）。arXiv:2203.13769。DOI 10.1145/3460231.3474241
- I. Srba, R. Moro, M. Tomlein, … M. Bielikova. *Auditing YouTube's Recommendation Algorithm for Misinformation Filter Bubbles*. ACM TORS 1(1), Article 6 (2023)。arXiv:2210.10085。DOI 10.1145/3568392
- 代码与数据：https://github.com/kinit-sk/yaudit-recsys-2021 （本地 `/home/user/kinit-sk/yaudit-recsys-2021`，最新提交 6a94493，2023-01-28）

**研究问题**：RQ1：与 Hussein+ 2020（2019 年中）相比，YouTube 的个性化行为有没有变化？RQ2：先看误导视频“陷入”泡泡，再看辟谣视频，能不能“戳破”泡泡？戳破的动态是什么样的？

**Bubble 的定义**：misinformation filter bubble 指推荐或搜索结果中与用户已看过内容**同立场**（支持误导）的内容比例上升。

**协议**（sockpuppet audit）
- 5 个话题（沿用 Hussein）：9/11 阴谋论、登月造假、chemtrails、地平说、反疫苗；每个话题 **10 个 bot**，共 **50 次 bot run**，时间为 2021-03-02 至 03-31；地理位置为美国 N. Virginia；Chrome 88 + uBlock
- Phase 0：新建账号，访问首页并执行搜索，得到基线
- Phase 1（promoting）：依次观看 **40** 个支持误导的种子视频（从最热门的 $n_s=40$ 个中选），每个看 $t_{watch}=30$ 分钟或看完；每看 2 个视频执行一次搜索阶段（从 Q 中轮流选查询词）；每看一个视频都保存侧栏推荐（top-20）和首页
- Phase 2（debunking）：观看 **40** 个辟谣视频，其余步骤相同
- Phase 3：清空历史
- 规模：观看 3,951 个视频；推荐 78,763 条（去重后 8,526）；搜索 10,075 次（结果 201,404 条，去重后 942）；访问首页 3,990 次（结果 116,479 条，去重后 9,977）；共 17,405 个不同视频，来自 6,342 个频道

**标注方案**：−1 = 辟谣；0 = 中立；1 = 支持误导；2/3/4 = 与话题无关的辟谣/中立/支持；5 = 与误导无关；6 = 外语；7 = 无法判断；8 = 已删除；9/10 = 嘲讽类（算作辟谣）。归一化后：支持→+1，辟谣→−1，其余→0。种子视频重新标注时，作者之间 Cohen's κ=0.815，与 Hussein 标注之间 κ=0.688。人工共标注 **2,914 个不同视频**（覆盖 255,844 次出现），其中支持 244、辟谣 628、中立 184、与误导无关 1,829、其他 29。TORS 版另外训练了三分类模型（Hou+2019 的 SVM/XGBoost 重实现和 Papadamou 模型），**准确率 0.82**，为 13,801 个视频预测标签（因伦理原因**不公开**预测标签，只公开聚合结果）。

**指标**
- normalized score（列表内标注的平均值，−1…1，用于推荐与首页）
- SERP-MS（按排名加权的误导分数，用于搜索）
- DIFF-TO-LINEAR（TORS 版新增：斜率相对线性趋势的偏差）
- 检验方法：Mann–Whitney U + Bonferroni 校正（α=0.01）

**主要结果（带数字）**
- RQ1：与 Hussein 相比整体**没有显著改善**（SERP-MS 均值 −0.46→−0.42，top-6 推荐 −0.07→−0.04，都不显著）。反疫苗话题变差（up-next 中辟谣比例 77%→19%，支持比例 1%→11%）；登月话题变好（辟谣比例 23%→40%）
- RQ2：top-10 推荐从 S1→E1 显著变差（−0.07→0.01，p=0.0397；9/11 的支持比例 14%→43%），从 E1→E2 显著改善（0.01→−0.27，p=1.8e−9）。**搜索结果基本没有形成泡泡**。首页（TORS 版）S1→E1 变差（−0.17→−0.09，p=0.0002），E1→E2 在 4/5 个话题上显著改善
- **动态**：陷入过程大致是线性、渐进的；**戳破过程远快于线性**（DIFF-TO-LINEAR：推荐 −3.3 到 −11.5，首页 −3.9 到−11.9）。第 41 个视频（切换到辟谣）后分数**突然下降**，作者解释为推荐的“强上下文性”

**本地仓库检查**（48 MB 数据，没有使用 LFS，CSV 可直接读取）

| 文件 | 大小 | 行数 | 关键列 |
|---|---|---|---|
| `Data/raw_data/recommendations.csv` | 9.6 MB | 78,763 | youtube_id, position(1–20), watched_youtube_id, bot_id, topic, seed_sequence(1–80), annotation, normalized_annotation, annotation_label, normalized_label, sequence_name(A: start / B: end of phase 1 / C: end of phase 2 / 数字), started_at |
| `Data/raw_data/search_results.csv` | 25 MB | 201,404 | …, query（25 个）, position, seed_sequence(0–80) … |
| `Data/raw_data/home_page_results.csv` | 13 MB | 116,479 | …（首页没有专门标注，只有在推荐或搜索中出现过的视频带有标签） |
| `Data/normalized_data/encountered_videos.csv` | 104 KB | 2,914 | youtube_id, original_label, normalized_label |
| `Data/normalized_data/seed_videos.csv` | 16 KB | 488 | youtube_id, topic, stance（每个话题支持/辟谣各约 40–68 个） |
| `Data/normalized_data/train.csv` | 136 KB | 2,622 | youtube_id + annotation（其余元数据需要调用 YouTube API 补全） |
| `Data/normalized_data/videos_metadata.csv` | 1.1 MB | 15,837 | 只有时长和出现计数，标题等为空 |
| `Data/predicted_data/*_with_predicted_grouped.csv` | 12–24 KB | 400 / 404 | topic, seed_sequence, score（人工 + ML 标签的均值）, annotated（人工标注占比） |

- 推荐表中 normalized_annotation 非空的行约 56k/78.8k（因为同一视频的标签会传播到它的每次出现）；top-10 中每个 seed_sequence 的人工标签覆盖率平均为 66%（chemtrails）到 86%（moonlanding）
- 代码：`Code/`（Selenium bot + Postgres/alembic + docker）；`Notebooks/`（rq1、rq2-statistical-tests、rq2-trends、normalize-annotations、Hou 模型重实现）

**我们的复算**（`deep_D/yaudit_reanalysis/reanalyse.py`，pandas + scipy，约 5 秒）
1. 按“每个 (bot, 观看视频) 的 top-10 推荐列表，取人工标签的平均值”计算 normalized score，用 seed_sequence {1,2}/{39,40}/{79,80} 作为 S1/E1/E2，**几乎逐位复现了 Tomlein Table 4 / Srba Table 10**：

| 话题 | S1 | E1 | E2 | p(S1–E1) | p(E1–E2) | p(S1–E2) | 支持比例 S1→E1→E2 | 论文值 (S1/E1/E2) |
|---|---|---|---|---|---|---|---|---|
| 9/11 | 0.10 | 0.43 | 0.07 | 2.1e−5 | 2.0e−6 | 0.66 | 13.5%→43.9%→12.7% | 0.10/0.42/0.07 |
| chemtrails | 0.00 | 0.04 | −0.15 | 0.94 | 9.7e−4 | 1.7e−4 | 1.0→8.1→3.5% | 0/0.05/−0.15 |
| flat earth | −0.17 | −0.08 | −0.47 | 0.16 | 2.7e−6 | 8.2e−5 | 2.3→8.3→1.0% | −0.17/−0.06/−0.47 |
| moon landing | −0.20 | −0.40 | −0.42 | 0.051 | 0.28 | 0.014 | 11.2→1.0→1.1% | −0.2/−0.4/−0.42 |
| vaccines | −0.09 | 0.05 | −0.37 | 0.0019 | 2.6e−6 | 9.2e−5 | 1.6→13.9→0.0% | −0.1/0.04/−0.37 |

2. 我们重画的“陷入—戳破”曲线见 `deep_D/yaudit_reanalysis/bubble_curves.png`（5 个小图；蓝线为只用人工标签的 3 点滑动平均，橙线为作者公开的人工 + ML 聚合文件；阴影表示 debunking 阶段）。完整序列数据在 `rec_top10_curve_manual_labels.csv`。第 36–40 个视频与第 41–45 个视频的均值跳变：vaccines **−0.53**，flatearth −0.28，chemtrails −0.15，9/11 −0.07（9/11 的戳破是渐进的），moonlanding −0.06（本来就没形成泡泡）。Phase 1 线性斜率只有每个视频 +0.011（9/11）到 −0.003，**陷入慢，戳破快**。
3. 注意事项：只用人工标签的曲线存在覆盖率偏差（未标注的视频被丢掉）；bot 之间的方差很大（Tomlein 自己也提到，相同配置下只有约 70% 的推荐相同）。

**局限**：只有 5 个话题、美国地理位置、只看 2021 年 3 月；bot 只“看”不点赞/订阅；首页没有人工标注；ML 标签不公开；平台变化后的可复现性有限（Mosnar+2025 在 TikTok 上证实了这一点）。

**我们可以复用什么**：(i) 数据可以直接作为**实证锚点**，用来校准仿真，比如“40 步陷入后第 41 步切换，泡泡指标多少步内回落到基线”；(ii) S1/E1/E2 + Mann–Whitney 的分析模板；(iii) −1/0/+1 归一化标注方案。

**它留下的空白**：没有做“看多少辟谣视频才够”的剂量–反应实验（固定是 40 个）；没有“不感兴趣 / 不推荐此频道”等显式负反馈；没有与仿真模型对照；bot 间异质性（为什么有的 bot 陷得深）没有深入分析。

---

## 6. TikTok 审计两篇

### 6a. Mosnar, Skurla, Pecher, Tibensky, Jakubcik, Bindas, Sakalik, Srba (2025) — *Revisiting Algorithmic Audits of TikTok: Poor Reproducibility and Short-term Validity of Findings*，SIGIR '25，arXiv:2504.18140，DOI 10.1145/3726302.3730293
- **问题**：RQ1：Boeker & Urman（2022）、Vombatkere+（2024）、Mousavi+ 的 TikTok sockpuppet 审计能复现吗？RQ2：location、watch、like、follow 等个性化因素的作用在今天还成立吗？
- **协议**：每个场景一对 bot（control 与 personalised），各自在 For You 页刷 **250 个视频**（每个视频看 100% 或最多 120 秒），每个用户重复 4 次 run（通过 cookie 保留历史），时间为 2025 年 1–2 月，美国代理，使用 nodriver 驱动的 Chrome。17 个场景 [S0–S16]：国家（德/法/罗/乌）、随机 25 个视频看 50/75/100/200%、按兴趣 hashtag（电影、美食、游戏、宠物、喜剧、情感…）看 50/200/400%、随机点赞 10 个、按兴趣点赞、点赞 top-30 创作者、关注 5 或 10 个随机创作者。
- **指标**：没有人工标注，只用 hashtag Jaccard 相似度和更宽松的 “basic match”（有一个 hashtag 或子串相同就算 100%）；视频播放量（流行度）的变化；兴趣 hashtag 视频所占比例。
- **发现**：两个并行的默认 bot 之间 feed 的 Jaccard 只有约 **10%**，同一 bot 内部约 20%（参考研究当年约 35%），说明**探索明显增强**；location 影响很强（control 之间为 25–38%，跨国家时低一个数量级）；**watch（观看时长）是最强的个性化信号，其次是 follow，like 最弱**（随机点赞反而触发探索），这与参考研究“follow 最强”的结论相反；按兴趣点赞时，前约 1000 个视频以探索为主，之后转为强利用；兴趣视频占比约 36%，关注创作者的视频约 6%；只有看到 **400%** 时长才显著增强个性化（参考研究称超过 75% 后就无增益）；前 125 个与后 125 个视频相比流行度普遍下降（−2% 到 −67%，control 也下降）；5 个 bot 被封号，结束后又有 15 个被封；更换指标（Jaccard 还是 basic match）会让结论变化。
- **数据**：Zenodo 16792218（CC-BY-4.0）**只有一个文件：`SIGIR_2025_TikTok_reproducibility_paper.pdf`（707,682 B）**，没有数据。代码和原始 JSON 在 https://github.com/kinit-sk/tiktok-algorithmic-audit-reproducibility （`data/` 下有 21 个场景目录，结构为 scenario → user type → run → interactions/responses 的 JSON 加截图；另有 `gdpr_analysis/` 存放 GDPR 导出数据）。当前会话的 GitHub API 被代理阻断，**没有下载和逐一核对大小**。
- **复用**：“control 与 personalised 成对 bot”的设计；**以 hashtag 集合相似度作为无需标注的泡泡指标**，这个指标可以直接移植到我们的仿真里（物品带“标签集合”）。
- **空白**：没有人工标注，指标脆弱；每个场景只有 1–2 次重复；没有做长时间的纵向跟踪。

### 6b. Pecher, Bindas, Jakubcik, Tuna, Tibensky, Liska, Sakalik, Suty, Mosnar, Hossner, Srba (2026) — *Algorithmic Audit of Personalisation Drift in Polarising Topics on TikTok*，UMAP 2026，arXiv:2603.20723（Zenodo 记录中写的预印本号是 2603.05653，**与用户提供的编号不一致**；我们读的 2603.20723 标题相符），DOI 10.1145/3805689.3812355
- **三种 drift 的定义**：preference-aligned drift（兴趣视频与无关视频之比的变化）；polarisation-topic drift（极化话题与中性话题 cooking 之比，取值 +1…−1）；polarisation-stance drift（support 与 oppose 立场之比，+1…−1）。
- **协议**：4 个极化话题（地平说、疫苗、气候变化、美国政治，各分 support/oppose 两种立场）加中性话题 cooking。用户分 3 组：neutral+polarising 32 人、polarising-only 32 人、mixed-polarity 4 人（仅美国政治）。性别 50:50，年龄 18–24，美国代理，2025 年 9 月与 2026 年 1 月进行。**Seed 阶段**：搜索关键词，看、点赞、收藏 25 个目标视频（1 天）。**交互阶段**：15 天（第三组 9 天），每天 60 分钟刷 For You 页，**由 LLM 充当“用户交互预测器”**判断视频是否符合用户兴趣（GPT-4.1 + Whisper large-v3-turbo 转写；话题准确率 95–98%，立场准确率 90–100%，评估集 350 个视频）；符合则看完并点赞，否则 1–2 秒后跳过。共遇到 **超过 8 万个不同视频**，没有账号被封。结果按 30 分钟分箱，用回归拟合 drift。
- **发现**：preference-aligned drift 很强（兴趣视频很快升到约 60–80%，约 80% 像是上限）；**误导信息类话题（气候、疫苗、地平说）出现“中和”式 topic drift**，cooking 逐渐占据 feed（气候话题 15 天只遇到 6 个相关视频）；美国政治保持均衡，政治视频比例一直很高；立场层面基本是“维持用户原立场”的均衡；两种立场都关注的美国政治用户会轻微偏向 oppose（左倾）（drift 从 −0.7 到 −0.8，p=2.1e−22）；第 3 天、第 6 天出现“探索期”（相关视频降到约 20%）。
- **数据**：Zenodo 19144520 **restricted**（需要学术邮箱验证后申请，文件列表 API 返回 403），描述为 agent 与 TikTok 的交互记录（CSV）；分析代码在 https://github.com/kinit-sk/ai-auditology-personalisation-drift-tiktok （需要自备三个 CSV：`…_32_agents_polarizing_only.csv`、`…_US_politics_4_agents_mixed_polarity.csv`、`…_32_agents_polarizing_plus_neutral.csv`）。**我们没有下载。**
- **复用**：三种 drift 的比值定义（非常适合直接用作仿真指标）；“LLM 作为用户模型”的思路（对一年级来说偏重，可以只在报告中讨论）。
- **空白**：每个组合只有 4 个用户；只用美国代理和 18–24 岁画像；没有“戳破”阶段，也没有负反馈按钮。

---

## 7. Hosseinmardi, Ghasemian, Rivera-Lanas, Horta Ribeiro, West, Watts (2024) — *Causally estimating the effect of YouTube's recommender system using counterfactual bots*，PNAS 121(8) e2313377121，arXiv:2308.10398

- **问题**：用户看到的偏激内容，有多少是推荐系统**造成**的，而不是用户自己偏好的结果？
- **方法（counterfactual bots）**：以真实用户的历史为模板（美国代表性桌面浏览面板，**87,988 人**，2021-10 至 2022-12）。从观看量 ≥140 的 4,583 人中抽出 24,871 段长度为 120 的轨迹，聚成 8 个党派“原型”（ψfL…ψfR，ψfR 又细分为 low/medium/high），最终选出 **125 个焦点用户**（刻意过采样极右）。
  - **实验 A（推荐偏差）**：4 个登录 bot 同时照着焦点用户的前 N=60 个视频观看（learning phase）；之后 control bot 继续照原轨迹看 60 个，3 个反事实 bot 分别按规则走 60 步：“up next”（侧栏第一个）、“random sidebar”（侧栏 top-30 中随机）、“random homepage”（首页 top-15 中随机）。平均每个焦点用户重复 2.61 次，共 **1,304 条轨迹**，观看时长超过 640,975 分钟。定义 $\hat y_{pref}=y_{expr}-y_{alg}$，也就是用户自身偏好造成的那部分党派倾向。
  - **实验 B（遗忘时间）**：44 个焦点用户（17 个 ψfR-high，27 个 ψfR-medium）。control 看 120 个极右视频；counterfactual 看同样的前 30 个后切换到一个中间派用户的 90 个视频。另一组对比短历史（30）与长历史（120）。共 233 条轨迹，45,435 个视频。
- **党派分数**：以频道为单位打分（沿用已有频道标签），同一频道的所有视频分数相同。
- **发现（带数字）**：(1) 反事实 bot（只跟推荐走）**平均比真实用户看得更不党派化**，用户越极端差距越大；$\alpha$ 在 up next、random sidebar、random home 三种规则下都显著为正；random homepage 最温和。(2) 连续看党派视频的“爆发”预测之后更党派化，但原因是**用户偏好变了，而不是推荐突然推更多**。(3) **遗忘时间**：切换到温和内容后，**侧栏推荐大约 30 个视频内就与中间派用户无法区分**，极右视频比例在观察期的第 30–40 步降到 0；首页更慢，大约 30 步后平均分数接近中性，但到第 90 步仍有少量非零的极右视频。(4) 历史更长（120 vs 30）**不改变侧栏的遗忘速度，但会让首页遗忘更慢**。(5) 换成 “establishment” 分数结论类似，换成流行度则没有一致效应；左派用户和订阅频道的情形结论相似。
- **结论**：至少在 2019 年 YouTube 改版之后，用户消费主要反映个人偏好，推荐整体起**温和化**作用。
- **局限**：只看桌面端和登录 bot；党派分数以频道为单位；bot 不产生真实用户的点赞/评论信号；面板数据是商业数据。
- **代码/数据**：arXiv 版中**没有找到公开数据或代码链接**；面板属于商业数据，不可复现。
- **复用**：“同一段历史 + 不同后续规则”的反事实设计**在仿真里几乎零成本**（同一个随机种子复制用户，一份照原偏好，一份照推荐走）；“遗忘时间”（切换后多少步指标回到基线）是一个很好的、可以与 Srba 的“戳破”对照的指标，并且有 **~30 步** 的真实参照值。
- **空白**：没有显式负反馈；没有 Shorts/TikTok 式的短视频 feed；遗忘速度与推荐多样化策略之间的关系没有研究。

---

## (a) 推荐给我们团队的最小仿真设计（纯 numpy，约 200–300 行）

**目标**：在同一个可控世界里比较不同排序策略对“茧房”的影响，并用 yaudit 的真实曲线（戳破快、陷入慢）和 Hosseinmardi 的“约 30 步遗忘”做**粗校准**。

**1. 世界与变量**
- K=8 个话题（topic）；A=100 个作者，每个作者主要写 1–2 个话题（作者向量来自 Dirichlet(0.1)）；每步新增 50 个物品，物品话题向量 $x_i$ 来自作者分布加噪声，另带一个作者 id 和质量 $q_i\sim\text{Beta}(2,5)$。【物品稀疏、属性均匀：Chaney；作者维度：X 算法】
- N=200 个用户，真实偏好 $p_u\in\Delta^K$，$p_u\sim\text{Dir}(10\cdot\text{Dir}(1))$，即偏好不均匀。【Chaney】
- 系统对用户的估计 $\hat\theta_u$：按话题对交互做指数衰减计数（半衰期 H 可调），这对应一种最简单的 content-based 学习。【Chaney 附录 A.2、T-RECS】
- T=200 步，≥20 个随机种子，报告均值和 95% CI。【Jiang：30 次重复；T-RECS：400 次】

**2. 用户行为（每步看一个 k=10 的 slate）**
- 位置偏差 $w(r)=r^{-0.8}$【Chaney】；对位置 r 的物品，点击概率 $P(\text{click})=w(r)\cdot\sigma(\beta_u(p_u\cdot x_i)+\gamma q_i-b)$【Jiang 的 sigmoid 点击】。
- 动作：click/like、skip、**“不感兴趣”（NI）**：当 $p_u\cdot x_i<\tau$ 时以概率 $\rho_{NI}$ 触发。NI 会让系统在该用户的 $\hat\theta_u$ 上把这个话题（以及这个作者）降权，例如乘以 0.5，并屏蔽该作者 M 步。【负反馈：X 算法中的 not interested / mute / block；各篇审计都缺少这一动作】
- 偏好漂移（可开关）：click 后 $p_u\leftarrow\text{normalize}((1-\eta)p_u+\eta\,x_i)$，只有当 $\|p_u-x_i\|<D$ 时才漂移，即使用有界接受【T-RECS drift，Geschke $f(d;D,\delta)$，Sîrbu ε】；η∈{0, 0.02, 0.05}。**必须包含 η=0 的对照**，因为我们在 T-RECS 中看到仅靠 drift 就会让 random 推荐下的用户也趋同。

**3. 待比较的推荐器**
- R0 Random【Chaney、Jiang】
- R1 Popularity（按近期点击数）【Chaney、Mansoury】
- R2 Greedy content：$s=\hat\theta_u\cdot x_i$ 取 top-k【Chaney】；另设 R2-ε：ε-greedy / softmax(β·s) 采样【Jiang 噪声 ε；Kalimeris 的 β】
- R3 **X 式加权分**：$s=\sum_a w_a\hat P(a)$，其中 $\hat P(\text{like})=\sigma(\hat\theta\cdot x)$，$\hat P(\text{NI})$ 由该用户历史 NI 率与话题估计得到。权重取自 xai-org/x-algorithm 的 `home-mixer/params/param.rs`（2026-09-28 从 main 分支读取）：Favorite **0.5**、Reply 5.0、Retweet 1.0、Share 2.0、Dwell 0.05、**NotInterested −43.2**、MuteAuthor −58.8、BlockAuthor −31.2、Report −234.0。只保留 like、NI 两到三项即可。**注意**：这些权重乘的是**预测概率**，不是计数（README 明确说明）。
- R4 = R3 + **作者多样性衰减**：同一作者在候选列表中第 k 次出现（按分数排序，k 从 0 开始），分数乘以 $m=(1-f)\cdot d^{k}+f$。公式见 `xai-value-model/scoring.rs::diversity_multiplier`；单元测试中用的是 d=0.5，f=0.25，线上值未公开。
- R5 = R3 + **DPP 重排**：核矩阵 $L=\text{diag}(e^{\lambda s})\,S\,\text{diag}(e^{\lambda s})$，S 为物品话题向量的余弦相似度，用贪心 MAP 选 k 个（Chen, Zhang & Zhou 2018 的 fast greedy DPP；X 的 `vm-ranker/` 在 README 中也写明 “reorders them with a determinantal point process over their embeddings”）；λ 控制相关性与多样性的权衡。再加一个简单的 MMR 作为对照。
- （可选）R6：Ideal，即按真实 $p_u$ 排序【Chaney 的基线】。

**4. 指标（每步记录）**
- 个体茧房：最近 W=20 次消费的话题熵 $H_u$，或 Gini-Simpson 指数；以及与初始偏好的 KL 散度 $KL(\bar c_u\|p_u^0)$【Mansoury】
- 兴趣退化：$\|p_u(t)-p_u(0)\|_2$ 与退化速度【Jiang】
- 群体同质化：最近邻配对的 Jaccard 减去 Ideal 下的值【Chaney eq.7；T-RECS `InteractionSimilarity`】
- 物品/作者层面：消费 Gini【Chaney eq.8】、覆盖率（aggregate diversity）【Mansoury】、作者份额的 HHI
- 效用：累计 $p_u\cdot x_i$ 相对 Ideal 的比例，以及 NI 率（体验代价）【Chaney】
- 三种 drift 比值：兴趣话题占比、极化/中性占比、立场占比【Pecher+2026】
- **陷入—戳破曲线与遗忘时间**：让一个“sockpuppet”用户在前 40 步只点击话题 A，之后 40 步只点击话题 B，记录 top-10 中 A 的占比；遗忘时间定义为 A 占比回到基线 ±5% 所需的步数【Srba 协议；Hosseinmardi “forgetting time”；以 yaudit 真实数据中的跳变和约 30 步作为参照】

**5. 实验矩阵（一年级可完成的范围）**
- E1：R0–R5 × η∈{0, 0.05}，看茧房与效用的前沿（每个推荐器在“熵–效用”图上一个点）
- E2：NI 按钮的剂量效应：$\rho_{NI}\in\{0, 0.1, 0.3\}$ × NI 权重 {0, −10, −43.2}
- E3：多样性旋钮扫描：作者衰减 d∈{1, 0.7, 0.5, 0.3}，DPP λ 取若干值，画 Pareto 曲线
- E4：陷入—戳破的仿真版本，与 yaudit 曲线（`deep_D/yaudit_reanalysis/rec_top10_curve_manual_labels.csv`）做**形状**比较（例如切换后跳变幅度 / 陷入斜率之比），而不是比较绝对值

**6. 验证**：用 T-RECS（Python 3.8 环境）复现一条 Chaney 式 repeated-training 同质化曲线，与我们自写的 R2 在相同参数下对比，作为 sanity check。

---

## (b) 综合与研究空白（约 400 字）

以上工作分成两条互不对接的线。**仿真线**（Chaney、T-RECS、Jiang、Mansoury、Kalimeris、Geschke、Sîrbu）一致表明：只要推荐按估计偏好**贪心利用**，并且用被推荐污染过的数据反复训练，就会出现行为同质化、兴趣退化和流行度放大；而且代价不均，少数群体和低效用用户受影响更大。但这些模型的用户只有“点或不点”，推荐器只有 popularity、MF、bandit 这类教科书算法，**没有一篇把真实平台已经采用的纠偏组件（负反馈权重、作者多样性衰减、DPP 重排）放进回路里测试**。**审计线**（Tomlein/Srba、Mosnar、Pecher、Hosseinmardi）给出了真实平台上的曲线：YouTube 泡泡陷入慢、戳破快（我们复算出 vaccines 在切换处跳变 −0.53）；侧栏约 30 个视频就“遗忘”旧偏好；TikTok 的误导类话题被中和、政治话题维持均衡。可是审计结果**短期有效、难以复现**（Mosnar），也无法打开黑箱去解释原因。

一年级团队可以可信地填补的空白（我们如实评估了新颖度）：
1. **把 2026 年开源的 X 排序公式要素放进玩具反馈回路**：加权负反馈（NI −43.2 等）、作者多样性衰减 $(1-f)d^k+f$、DPP 重排，比较它们对茧房和效用的影响。**新颖度中等**：DPP/MMR 多样化本身早有研究，但用真实的 X 权重结构做受控对比的公开工作很少（据我们检索所及）。
2. **“不感兴趣”按钮的剂量–反应**：用户主动负反馈能否、以多快速度戳破茧房？现有审计都只“看”不点负反馈。**新颖度中等**，结论也可以反过来设计真实的小规模手动审计。
3. **仿真与审计的形状校准**：用 yaudit 公开数据的“陷入斜率 / 戳破跳变”和 Hosseinmardi 的约 30 步遗忘时间作为目标，检验哪种用户和推荐器假设能复现这种“非对称”。**新颖度较高，但结论只能定性**，需要谨慎表述。
4. **可复现性小贡献**：记录 T-RECS 和 NDlib 在现代 Python 上的安装问题和一组可运行的版本组合，并把 yaudit 的表格用 20 行 pandas 复算（我们已经验证与论文一致）。这属于工程贡献，**新颖度低但完全可信**。
5. **漂移假设的敏感性**：展示“同质化”有多少来自用户漂移假设本身（η=0 对照；我们在 T-RECS 中看到仅靠 drift 就能让 random 推荐下的用户趋同）。**新颖度低到中等**，但这是很多仿真论文忽略的方法学提醒。

**诚实声明**：以上都是在已有框架内的小规模组合与校准，不是新理论；结论必须限定为“在该玩具模型与参数下”。

---

## 附：本次产出的文件
- `deep_D/deep_D_simulation_audits.md`（本文件）
- `deep_D/papers/*.pdf|*.txt`（全部论文的 PDF 与抽取文本；`TFB.nlogo`；NDlib `ABM.py`）
- `deep_D/trecs_demo/demo.py`, `demo_output.txt`（T-RECS 实跑；环境 `deep_D/venv38`）
- `deep_D/ndlib_demo/abm.py`, `out.txt`（NDlib 实跑；环境 `deep_D/venv311`）
- `deep_D/yaudit_reanalysis/reanalyse.py`, `S1_E1_E2_table.csv`, `rec_top10_curve_manual_labels.csv`, `bubble_curves.png`
- `deep_D/xalgo_README.md`, `xparam.rs`, `xscoring.rs`（X For You 算法的权重与多样性代码快照，2026-09-28）
