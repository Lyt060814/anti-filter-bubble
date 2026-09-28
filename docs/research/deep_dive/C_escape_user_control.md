# Deep Dive C：逃离信息茧房——用户侧控制是否有效、"可逃离性"如何度量、平台侧有哪些修复

> COMP1110 小组项目文献精读｜整理日期：2026-09-28
> 核心问题：①"不感兴趣 / 点踩 / 重置 / 偏好滑块"这类用户控制到底有没有用？②怎么量化"逃离茧房的难易度"（escapability）？③平台侧有哪些技术修复？④前人**具体做了什么、没做什么**（为了找真正的 research gap）。

**阅读深度标记**：
- 【全文精读】= 下载了 PDF 并逐节读了方法 / 实验 / 结果（数字均出自原文表格或正文）
- 【摘要 + 代码】= 全文拿不到（出版商屏蔽爬虫），只读了摘要、元数据和公开代码
- 【读图估计】= 数值是从论文图中目测读出来的，不是表格里的原始数字，引用时要写明

**对任务说明里几处引用信息的更正（写报告时请用更正后的版本）**：
1. BEP 论文（arXiv 2512.03067）的版权页写的是 **AAAI 2026**，GitHub README 也写 "AAAI 2026 paper"，不是 AAAI'25。
2. "Michiels et al. (2022)" 的正式作者顺序是 **Leysen, J., Michiels, L., Goethals, B., & Smets, A. (2022)**，Leysen 与 Michiels 为共同一作，发表于 UMAP '22 Adjunct。
3. Mozilla 报告里的 "43%" 指的是：与**对照组**相比，坏推荐率**相对**下降了约 43%。它不是"43% 的用户觉得有用"，也不是说剩下的推荐里有 43% 是坏推荐。
4. Liu, Wu & Resnick 论文正文说数据采集于 **2022 年 8 月**，但 Limitations 一节写成了 "August of 2021"，是原文自相矛盾，应以正文的 2022 年 8 月为准。另外，他们 GitHub README 写 "Not interested 移除了 97%"，而论文 Table 1 给的是**平均相对下降 88%**。引用时请以论文为准。
5. Nguyen et al. (2014) 的结论**方向**经常被误读。他们确实发现所有用户的推荐和消费都略微变窄；但**跟随推荐的用户变窄得更少**，也就是说推荐系统反而**减轻**了茧房。

---

## 目录
1. BEP：Bubble Escape Potential（Feng et al., AAAI 2026）
2. UCRS：User-controllable Recommendation Against Filter Bubbles（Wang et al., SIGIR 2022），附本地代码审计
3. DDIR：Rethinking Homogeneity in Interactive Recommendation（Li et al., ACM TWeb 2026）
4. CD-CGCN：Mitigating Filter Bubble from the Perspective of Community Detection（Tang et al., arXiv 2508.11239）（简版）
5. How to Train Your YouTube Recommender to Avoid Unwanted Videos（Liu, Wu & Resnick, ICWSM 2024）
6. When 'For You' isn't for you（Kaplan et al., ICWSM 2026）
7. Mozilla Foundation (2022) *Does This Button Work?*
8. Exploring the Filter Bubble（Nguyen et al., WWW 2014）
9. What Are Filter Bubbles Really?（Leysen, Michiels et al., UMAP 2022）+ 2023–2026 相关度量 / 审计工作速览
10. (a) 对比表："逃离 / 控制有效性"是怎么被操作化的
11. (b) 综合与研究空白（约 400 字 + 5 个具体空白）
12. 附录：可行性探针（UCRS 代码实跑、KuaiRand-Pure 负反馈稀疏度）

---

## 1. BEP — Bubble Escape Potential【全文精读】

**引用**：Feng, D., Xu, Q., Wang, Z., Hua, C., Yang, Z., & Huang, Q. (2026). *Quantifying the Potential to Escape Filter Bubbles: A Behavior-Aware Measure via Contrastive Simulation.* AAAI 2026. arXiv:2512.03067（中国科学院计算所 / 国科大）。

**研究问题**：已有的茧房指标（熵、类别覆盖率、Top-1 类别占比）只看**推荐列表本身的多样性**。这些指标分不清"用户本来就只爱看这些"（偏好建模）和"系统把用户关起来了"（信息禁锢）。作者要做一个**把用户行为考虑进去**的指标，衡量用户**主动想逃**时能逃掉多少。

**茧房的定义**：一个用户**主动尝试逃离、却仍然看不到多样内容**时，茧房才算严重（"a filter bubble is more severe when a user actively tries to escape it but still fails to see diverse content"）。

**数据**：
- MovieLens-1M 和 Amazon-Books（Ni et al. 2019 版本），都是公开数据集。
- 仿照 Agent4Rec 的做法：先选 **1000 个高频用户**作为冷启动交互集 A₀，再从中随机抽 **N = 200** 个用户，用 LLM 从他们的历史里提炼"独特口味"和社会属性（activity / conformity / diversity）。
- 驱动用户智能体的 LLM 是 **Qwen2.5-14B-Instruct-1M**，共仿真 **T = 8** 轮。

**方法（白话）**：
1. **同一批** 200 个 LLM 用户跑两遍仿真，只改"态度"：
   - **正向用户**：prompt 写着"主动拓宽视野，会看一些不符合自己口味的内容"，并且 activity 和 diversity 调到最高；
   - **负向用户**：prompt 写着"高度依赖推荐系统，先看排名靠前的"，并且 activity 和 diversity 调到最低。
2. 每一轮：用 A_{t−1} 重新训练推荐模型 → 给每个用户逐页推荐 L_{u,t} → 用户按设定的人格挑出 S_{u,t} → 把交互并入 A_t。这样就形成了一个**反馈闭环**。
3. 比较两组用户**被推荐到的类别数量**。

**关键公式**：

$$D_{u,t}=\big|\{c(i)\mid i\in L_{u,t}\}\big| \quad(\text{第 }t\text{ 轮推荐列表覆盖的不同类别数})$$

$$\widehat{BEP}_t(R)=\frac{\sum_{u\in U} D_{u,t}}{\sum_{u\in U} D'_{u,t}},\qquad \widehat{BEP}(R)=\frac1T\sum_{t=1}^{T}\widehat{BEP}_t(R)$$

其中 D 是正向用户的类别数，D′ 是负向用户的类别数。按设计 BEP ≥ 1，**BEP 越小说明茧房越严重**（再怎么努力也逃不出去）。作者强调的一个性质是：如果两组用户的多样性按**同样比例**上升，BEP 不变，也就是说它对"一刀切"式的多样化保持不变。

**测试的模型**：Random、BPR-MF、LightGCN、Caser、DiffRec、TiCoSeRec。准确率用 HR@20、NDCG@20、MAP，并用 leave-one-out 划分数据。

**主要定量结果**：
- **仿真用户是否像真人**（Table 1–2）：正向行为预测的 Precision 0.67 / Recall 0.76 / Acc 0.68 / F1 0.70；负向为 0.72 / 0.58 / 0.68 / 0.63；和真人评分分布的 KL 散度约 0.125。作者据此称"对齐度约 70%"。
- **动机实验**（Fig. 2）：在 ml-1m 上，把用户行为改成正向（LightGCN-positive）带来的多样性差异，**比把 LightGCN 换成 TiCoSeRec 带来的差异还大**。也就是说，用户行为对多样性的影响不亚于算法本身。
- **弱化行为**（Table 3，ml-1m）：Random 的 HR@20 = 0.001，BEP = 1.35，弱化行为后 BEP-weak = 1.20；TiCoSeRec 的 HR@20 = 0.257，BEP = 1.24，弱化后 BEP-weak = 1.05。排序保持不变。
- **准确率与茧房的两难**（Fig. 4）：准确率和 BEP **负相关**。序列模型（Caser、TiCoSeRec）落在"高准确、低 BEP"区，非序列模型（MF、LightGCN、DiffRec）落在"低准确、高 BEP"区。ml-1m 上 BEP 大约在 1.20–1.35 之间，Amazon-Books 上大约在 1.12–1.20 之间【读图估计】。
- **"轻度随机推荐无效"**（Fig. 5，RQ5）：把 LightGCN 或 TiCoSeRec 推荐列表中 k = 10%…90% 的位置替换成随机物品，结果是：
  - BEP 随 k **非单调**变化：k 升到约 **30%** 时 BEP 反而**降到最低**；
  - 约 **70%** 时才回到原来的水平；
  - **80–90%** 时才超过原水平，但此时模型已经接近纯随机推荐。
  - 以 LightGCN 为例，BEP 大约在 1.23–1.35 之间【读图估计】。
  - 作者的结论是："随机性并不能帮助更好地平衡防茧房与准确率"。
- **不同用户群**（Fig. 6）：
  - activity 越高 → BEP 越**低**（越活跃的用户越被"锁住"）；
  - diversity 越低 → BEP 越低；
  - conformity 与 BEP 没有明显关系；
  - 偏好惊悚、动作、犯罪片的用户 BEP 较高，偏好纪录片、动画的用户 BEP 较低，呈现长尾特征。

**局限（我们的批判性阅读）**：
1. **行为和属性混在一起**：正向组不仅 prompt 不同，activity 和 diversity 也被调到最高；负向组全部调到最低。因此 BEP 测到的是"意图 + 活跃度 + 多样性偏好"的**合成效应**，不是单纯的"想逃"意图。
2. **多样性只数类别个数**：D = 不同类别的数量，不看比例或熵。对 ml-1m 这种一部电影有多个类别标签的数据很粗糙。
3. **"轻度随机无效"有一部分是定义造成的**：随机替换**同时**提高了两组用户的多样性，而 BEP 是一个比值，对同比例上升本来就不敏感（这正是作者宣称的性质）。所以这个结论有一部分来自 BEP 的构造本身，不完全是经验发现。这一点可以作为我们的方法论切入点。
4. **规模小**：只有 200 个 LLM 用户和 8 轮，没有误差条或显著性检验；仿真用户与真人的对齐度只有约 70%。
5. **不含真实的负反馈按钮**："正向用户"的做法是主动去看不喜欢的内容，而不是点"不感兴趣"。所以 BEP 测的是**靠主动探索来逃离**，不是**靠负反馈来逃离**。

**代码 / 数据**：https://github.com/fengdifu24/bepmetric 。截至 2026-09-28，README 只写着 "our code will be available soon"，仓库里只有 `resources/` 文件夹（放示意图），**没有可运行代码**。数据集是公开的 ml-1m 和 Amazon-Books。

**我们可以复用什么**：
- **对照仿真**这个思路：同一个推荐器，分别用"想逃"和"不想逃"两组用户跑，然后看比值。可以把用户换成**规则型智能体**（不需要 LLM，更便宜、更可复现）。
- 他们的公式（2）–（5）可以直接照搬。
- "准确率–BEP 散点图"这种呈现方式也可以借用。

**它留下的空白**：
- 没有测试**负反馈按钮**（不感兴趣、点踩），只测了"主动多看"；
- 没有测**持久性和复发**；
- 只用了电影和图书数据，没有短视频，也没有中文平台；
- 代码没有公开，无法复现；
- BEP 对"同比例多样化"不敏感，这个设计会系统性低估随机注入的效果，值得补充一个**绝对差值**型或**逃离所需步数**型的指标。

---

## 2. UCRS — User-controllable Recommendation Against Filter Bubbles【全文精读 + 本地代码审计】

**引用**：Wang, W., Feng, F., Nie, L., & Chua, T.-S. (2022). *User-controllable Recommendation Against Filter Bubbles.* SIGIR '22, pp. 1251–1261. arXiv:2204.13844. DOI 10.1145/3477495.3532075。

**研究问题**：现有的去茧房方法（多样性、公平性、校准）通常要**牺牲准确率**，而且用户只能靠反复点赞、点踩来**被动**纠偏，响应很慢。作者主张让**用户自己决定**是否破茧、破哪个茧，并提出 **UCRS 原型**，包含三部分：
- ① 茧房**预警**；
- ② 四类**控制命令**；
- ③ 在推理阶段**实时响应**（不需要重新训练模型）。

**茧房的定义与检测**（§3–4.2.1）：
- 用 FM 训练后取每个用户的 top-10 推荐。结果发现推荐分布**继承并放大**了历史分布（bias amplification）：男女用户在 DIGIX-Video 上的类别差异被放大；在 Amazon-Book 和 ML-1M 上，历史里最大的类别在推荐里的占比更高。
- 基于此定义了三个检测指标：
  - **Coverage**：推荐列表中不同类别的数量；
  - **Isolation Index**：改编自 Gentzkow & Shapiro (2011) 的意识形态隔离指数：
  $$s=\sum_{i\in I}\Big(\frac{a_i}{a_n}\cdot\frac{a_i}{a_i+b_i}\Big)-\sum_{i\in I}\Big(\frac{b_i}{b_n}\cdot\frac{a_i}{a_i+b_i}\Big)$$
  其中 a_i、b_i 分别是 a 组、b 组中被推荐了物品 i 的用户数，a_n = Σ a_i。s ∈ [0,1]，越大说明两组被推荐的内容越隔离。如果有多个组，就对所有两两组合取平均。
  - **MCD（Majority Category Domination）**：用户历史中最大类别在推荐列表里的占比。
- 论文提出可以用启发式规则把这些指标映射成 1–5 级的"茧房严重度"提醒用户，但**并没有实现或评估**这个预警功能。

**四类控制命令**（用 do-calculus 形式化为 P(R | D, do(C))）：

| | 细粒度（fine-grained） | 粗粒度（coarse-grained） |
|---|---|---|
| 用户特征 | c_u(+x̂, α)："多推一些别的人群（如年轻人）喜欢的" | c_u(−x̄, α)："不要被我的年龄段 / 性别限制" |
| 物品特征 | c_i(+ĥ, β)："多推某个目标类别（如爱情片）" | c_i(−h̄, β)："少推我历史里最大的那个类别" |

**方法——UCI（User-Controllable Inference）**：
- **反事实推理**：用户 ID 的表示已经编码了"过时的兴趣"（交互是混杂因子）。因此在推理时减去 ID 表示的因果效应：
$$Y_{u,i}-\alpha\,(Y_{u,i}-Y_{\hat u,i})=(1-\alpha)f(u,i)+\alpha f(\hat u,i)$$
  其中 û 表示去掉 ID 表示后的用户。
- **用户特征控制**：细粒度控制就是把特征改成目标组（例如年龄从 30 改成 18），粗粒度控制就是把原特征丢掉，然后再按上式推理。
- **物品特征控制**：采用可控的排序策略
$$Y'_{u,i}=Y_{u,i}+\beta\cdot r(i),\quad r(i)=\begin{cases}2 & \hat h_i=1\ (\text{细粒度目标类})\\0 & \bar h_i=1\ (\text{粗粒度：历史最大类})\\1&\text{otherwise}\end{cases}$$
- **目标类别预测**：粗粒度控制时，用户不知道自己想要什么，所以按时间把用户历史切成前后两段，用 MLP 从前段的类别分布预测后段的分布；再施加干预 do(h̄ = 0)，取 top-K 类作为目标类。

**数据**（Table 1，都是公开数据）：

| 数据集 | 用户 | 物品 | 交互 | 密度 | 类别数 |
|---|---|---|---|---|---|
| DIGIX-Video（华为 2021 DIGIX 挑战赛，Kaggle） | 7,643 | 15,526 | 316,045 | 0.0027 | 135 |
| ML-1M | 6,040 | 3,883 | 575,276 | 0.0245 | 18 |
| Amazon-Book | 29,115 | 16,845 | 1,712,409 | 0.0035 | 29 |

- 预处理：10-core，评分 ≥ 4 视为正样本，**按时间** 80/10/10 划分。
- 用户特征控制只在 DIGIX 上评估（只有它有年龄和性别）：细粒度以性别为对象，粗粒度以年龄为对象。
- 物品特征控制只评估"**训练集最大类别 ≠ 测试集最大类别**"的偏好迁移用户，三个数据集分别是 4,320 / 3,806 / 5,155 人。
- 细粒度控制中的"目标类别"直接取**测试集的最大类别**，相当于先知信息，所以 F-UCI 被当作上界（UB）。

**评测指标**：Recall@10、NDCG@10；Iso-Index↓、Coverage↑；
- **DIS-EUC**↓ = dis(d_u, ĝ_u) − dis(d_u, ḡ_u)，其中 dis 是欧氏距离，d_u 是该用户推荐的类别分布，ĝ_u 是目标组的平均类别分布，ḡ_u 是原所属组的平均类别分布；
- **W-NDCG**：目标类正样本记 2 分，非目标类正样本记 1 分，负样本记 0 分；
- **MCD**↓、**TCD**（目标类别占比）↑。

**主要结果**：
- **粗粒度用户特征控制**（Table 2，DIGIX）：
  - FM：Iso-Index 0.1082 → **0.0777**（相对下降约 28%），Recall 0.0758 → 0.0767，Coverage 9.52 → 9.88；
  - NFM：Iso-Index 0.1144 → 0.0760。
  - 相比之下，maskUF / woUF 这些"只删掉特征"的简单做法几乎没有效果，因为用户 ID 表示里仍然编码了原有的兴趣。
- **细粒度用户特征控制**（Table 3，FM）：Iso-Index 0.1161 → 0.0979，DIS-EUC 0.0568 → 0.0516，Recall 0.0861 → 0.0870。作为对照，Fairco 的 NDCG 下降了 **15.38%**。
- **物品特征控制**（Table 4）：

| | MCD | TCD | Recall | Coverage |
|---|---|---|---|---|
| ML-1M，FM | 0.5994 | 0.2222 | 0.0659 | — |
| ML-1M，C-UCI | **0.2466** | 0.3334 | 0.0770 | — |
| ML-1M，Reranking | 0.1000 | — | — | — |
| Amazon-Book，FM | 0.5353 | 0.2305 | — | 3.02 |
| Amazon-Book，C-UCI | 0.0213 | 0.6310 | — | **2.08** |

  注意 Amazon-Book 上 C-UCI 的 Coverage 反而**下降**了。原因是它把推荐集中到了目标类别，从一个茧跳进了另一个茧。
- **α、β 的剂量效应**（Fig. 6）：α 越大，隔离越轻、多样性越高；准确率先升后降，但下降比较平缓。
- **反事实推理消融**（Table 5）：加上反事实推理后，NFM-F-UCI 的 MCD 从 0.3525 降到 0.3319，Recall 从 0.2094 升到 0.2125。

**局限**：
1. **"用户控制"完全是离线假设的**：假设用户发出了命令，然后评估模型对命令的响应。没有真实用户，没有 UI，也没有研究用户是否会用、是否知道这个功能。
2. **没有反馈闭环和时间维度**：只做了一次推理，没有研究多轮之后茧房会不会回来。
3. 用户特征控制只在一个数据集（DIGIX）上测试；ML-1M 被作者自己判定为不适合（77% 的用户最爱的类别是剧情或喜剧）。
4. 细粒度控制的目标类别用的是**测试集的先知信息**；粗粒度控制的效果本质上是"预测用户下一阶段的兴趣"，和"帮用户破茧"是两回事。
5. 茧房预警的阈值和分级没有实现。

**本地代码审计**（`/home/user/wenjiewwj/ucrs`，只读）：
- **结构**：
  - `code/FM_NFM/`：FM/NFM 的训练、`evaluate.py`，以及指标工具 `item_side_utils.py`、`user_side_utils.py`；
  - `code/UCI/user_coarse_controls/`、`user_fine_controls/`、`item_controls/{Reranking, fine_coarse_UCI}/`：四类控制的推理脚本；
  - `data/{DIGIX, ml_1m, amazon_book}`：预处理好的 `.npy` 文件；
  - 总大小约 189 MB。
- **依赖**：Python 3.7.3，PyTorch 1.4.0，numpy 1.16.4。代码里有 **133 处 `.cuda()`**，写死了必须用 GPU，要在 CPU 上跑得改代码。本机没有装 torch。
- **数据**：**三个数据集都已包含**（DIGIX 57 MB，Amazon-Book 52 MB，ML-1M 14 MB）。格式是预处理后的 `.npy`：`training_list` 是 (user, item) 对，`item_category` 是字典 item → [类别]，`user_feature` 等。**没有原始时间戳**。
- **预训练模型**：`code/FM_NFM/best_models/` 里有 6 个 `.pth`，另外还有每个模型的 **`*_top100_result.npy`**（每个用户的 top-100 推荐列表，字典格式），共 66 MB。
- **许可证**：README 只写了 "NUS © NExT++"，**没有开源许可证**。可以用于学习和引用，但如果要再分发，需要注意。
- **实现细节**：
  - 用户特征的 UCI 在 `UCI_coarse_user_control.py` 中实现为把用户 ID 特征的取值乘以 α（`alpha_list = [0.8, 1.0]`，其中 1.0 对应 maskUF）。
  - 对 FM 来说，ID 特征的所有交互项都是 ID 取值的一次函数（FM 没有自交互项），所以这种写法**恰好等价于**式（2），对应论文里的 α = 0.2。
  - 对 NFM（有 MLP）则只是近似。
- **可直接复用的指标实现**：
  - `code/UCI/user_coarse_controls/user_side_utils.py` 中的 `multi_isolation_index()`（第 317 行起）：多组两两 Isolation Index；以及 `get_item_gender_interaction()`：两组版本；
  - `code/FM_NFM/item_side_utils.py` 中的 `get_category_num / get_category_A_D`：Coverage，以及相对历史的 Coverage 变化；
  - 同一文件中的 `get_GA_GD`：GD 就是 MCD，GA 是"放大量"（推荐占比减历史占比），target_GD 就是 TCD。
  - 这些函数都是**纯 Python/numpy**，不依赖 torch。

**我们可以复用什么**：
- Isolation Index、MCD、TCD、Coverage 这四个现成指标（纯 Python）；
- 现成的 top-100 推荐结果，**不用 GPU** 就能做"茧房诊断"练习（见附录 A 的实跑结果）；
- "四类控制命令"的分类框架，可以作为描述平台真实按钮的概念框架：比如"不感兴趣"约等于粗粒度的物品特征控制，而抖音的"内容偏好设置"约等于细粒度的物品特征控制。

**它留下的空白**：
- 控制是**假设出来的**，没有检验真实按钮；
- 没有多轮反馈，没有复发研究；
- 没有"负反馈"这类最常见的控制方式（它的控制是正向的"给我更多 X"或"少给我最大类"，是**命令式**的，不是逐条点"不感兴趣"）；
- 没有中文短视频平台（DIGIX 是华为视频的数据，是长视频或影视类）。

---

## 3. DDIR — Rethinking Homogeneity in Interactive Recommendation【摘要 + 代码】

**引用**：Li, P., Shi, X., Xie, H., Xia, C., & Shang, M. (2026). *Rethinking Homogeneity in Interactive Recommendation: Dynamic Fine-Grained Control for Mitigating Filter Bubbles.* ACM Transactions on the Web. DOI 10.1145/3828182（2026-08-14 在线发表；中科院重庆绿色智能技术研究院 / 中国科学技术大学；CC-BY 开放获取）。**找不到 arXiv 版本**。ACM 页面对爬虫返回 403，因此下面的内容来自 Crossref/Semantic Scholar 上的摘要和 GitHub 代码。

**研究问题**：以往研究普遍认为"同质化"是坏事。作者在交互式推荐（IRS）中做了**细粒度分析**，发现同质推荐在**重复的早期阶段是有益的**，之后才变得有害。因此问题变成：能否**动态**控制同质化的程度？

**茧房的操作化**（从代码推断，继承自 CIRS/DORL 系列的 KuaiEnv 环境）：见 `environments/KuaishouRec/env/kuaishouEnv.py` 中的 `_determine_whether_to_leave`。当前推荐物品的任一类别，如果在**最近 `num_leave_compute` 条推荐**里出现次数超过 `leave_threshold`，用户就**离开**（会话结束）。默认参数是 5 和 1。换句话说，茧房被定义为"**短窗口内同类别重复** → 用户流失"，评估时则用**会话长度**和**累计奖励**来衡量。

**方法**：一个离线的、基于模型的强化学习框架 DDIR，包括：
- Transformer 状态编码器（捕捉随时间变化的多样性偏好）；
- "对同质化友好"的多样性模型（估计用户对重复内容不断变化的容忍度）；
- 去偏兴趣模型（把内在偏好和从众偏差分开，并考虑物品质量）；
- 三者共同指导策略学习。

**数据**：KuaiEnv（基于 KuaiRec）和 KuaiRand。二者都是快手公开的真实日志，由 Chongming Gao 等人构建成强化学习环境。

**指标**（从 `reproduce_results_of_our_paper/table_main_result.py` 可见）：
- R_tra：整条轨迹的累计奖励；
- R_each：单步奖励；
- Length：交互长度；
- **MCD**：同 UCRS 的"多数类别占比"。

对比的基线包括 CIRS、DORL、CWM、IPS、DICE、DeepFM、PD。

**主要结果**（摘要）：在 KuaiRand 仿真环境中，与最强基线相比，平均会话长度 **+4.35%**，长期参与度 **+25.65%**。至于"同质化早期有益"具体的重复次数阈值和曲线，全文拿不到，**无法核实**。

**局限**：
- 离开机制是**人为设定的规则**（同类重复超过阈值就离开），并不是从真实用户行为里学出来的；
- 优化目标是"参与度"，破茧只是手段，不是目标；
- 用户**没有**任何控制权，所有控制都在平台侧。

**代码 / 数据**：https://github.com/16061025/DDIR 。README 只有两句话："run the .py files in `reproduce_results_of_our_paper`… complete environment setup… will be provided later"。仓库里有 `core/`、`environments/{KuaiSim, KuaishouRec}`、自带的 `tianshou/` 和 `DeepCTR-Torch/`，还有结果和画图脚本。**环境配置不完整**，跑起来有一定难度。

**我们可以复用什么**：
- KuaiEnv 的"**重复即离开**"规则，是一个非常好懂、可以写进报告的**茧房代价模型**，可以直接拿来构造我们自己的简易仿真；
- "同质化并不总是坏事，先有益后有害"这个观点，可以用来平衡报告的立场。

**它留下的空白**：
- 纯粹是平台侧的强化学习方案，没有用户控制，没有负反馈按钮；
- 离开阈值是人为设定的；
- 没有检验它的仿真结论与真实平台上的"不感兴趣"行为（KuaiRand 中的 `is_hate` 字段）是否一致。

---

## 4. CD-CGCN — Mitigating Filter Bubble from the Perspective of Community Detection【全文浏览，简版】

**引用**：Tang, M., Huang, X., & Sang, J. (2025). *Mitigating Filter Bubble from the Perspective of Community Detection: A Universal Framework.* arXiv:2508.11239（北京交通大学）。

**茧房定义**：在用户–物品二部图上跑 Louvain 社区发现。如果推荐列表中与用户**同属一个社区**的物品占比过高，就视为茧房。

**指标**：
$$\text{ILFBI@}k=\frac{\sum_{u}\sum_{i\in \text{Top-}k(u)}\mathbb 1[C_i=C_u]}{|U|\cdot k}$$
另外还有 **CGI@k**：推荐物品在各社区之间分布的 Gini 系数。

**证据**：
- 在 Gowalla 上，用户训练集中 **78%** 的交互是社区内物品，而基础模型的 top-20 推荐中社区内物品占 **90%**，说明模型放大了社区内聚。
- 用户的初始 ILFBI 越高，推荐后 ILFBI 的增量越大。

**方法**：
- 条件判别器 + 社区重加权 GCN，做**对抗学习**，去掉 embedding 中的社区属性，并用梯度反转层（GRL）实现端到端训练；
- 引入社区增强的负采样；
- 推理时按用户自身的茧房程度自适应融合：
$$\eta_u=\frac{ILFBI^{init}_u}{2\,\overline{ILFBI^{init}}},\qquad Y_{u,i}=\eta_u Y^{CD}_{u,i}+(1-\eta_u)Y^{BM}_{u,i}$$

**数据**：

| 数据集 | 用户 | 物品 | 交互 | 社区数 |
|---|---|---|---|---|
| Gowalla | 29,858 | 40,981 | 1,027,370 | 18 |
| Amazon-Book | 52,643 | 91,599 | 2,984,108 | 9 |
| ML-2k | 2,095 | 5,254 | 367,761 | 6 |

基础模型是 MF、NGCF、LightGCN、DGCF。

**结果示例**（Table II，@20）：
- MF 在 Amazon-Book 上：ILFBI 0.7757 → **0.6864**，Recall 0.0315 → 0.0362；
- LightGCN 在 Gowalla 上：ILFBI 0.9091 → 0.8858；
- 对比基线有 MMR、公平性方法、IPS，CD-CGCN 通常能同时改善准确率和 ILFBI。

**局限 / 空白**：
- 静态的离线评估，没有反馈闭环，没有用户控制；
- "社区"只是一个图结构上的代理，不对应主题或观点；
- 论文中没有找到代码链接。

**我们可以复用什么**：ILFBI 很容易实现（Louvain 社区发现 + 比例计算），可以作为"类别之外"的第二种茧房度量。

---

## 5. How to Train Your YouTube Recommender to Avoid Unwanted Videos【全文精读】

**引用**：Liu, A., Wu, S., & Resnick, P. (2024). *How to Train Your YouTube Recommender to Avoid Unwanted Videos.* ICWSM 2024. arXiv:2307.14551（密歇根大学）。

**研究问题**：
- RQ1：连续观看同一主题会不会让首页和视频页的推荐被"染色"？染色来自已经看过的频道，还是新频道？
- RQ2：**反复**使用某一种清除策略，能在多大程度上去除这种主题？
- RQ3：真实用户对这些按钮的**知晓率、使用率、主观有效性**如何？

**"茧房"的定义**：作者刻意不用 "bubble" 这个词，而是用 **stain**（染色），定义为推荐中属于指定主题的**百分比**。理由是染色从来没有超过 50%，说不上被"包围"。

**方法（sock puppet，染色–清除协议）**：
- **4 个主题**：Alt-Right、Antitheism、Political Left、Political Right。主题用前人整理的**频道列表**来界定。
- **7 种策略**：
  - None：对照组，只刷新；
  - Watch neutral：看中立的主流新闻；
  - 基于历史的两种：Dislike（回到染色期看过的视频点踩）、Delete（从观看历史中删除最近看的视频）；
  - 基于推荐的三种：**Not interested**、**Don't recommend channel**（No channel）、Dislike recommended（点开推荐视频直接点踩）。基于推荐的策略只对首页上**第一个**属于该主题频道的推荐执行。
- **每个主题**：7 种策略 × 每种 5 个账号 = **35 个账号并行**；4 个主题共投放 **140 个**，**139 个**跑成功。5 个染色视频列表在策略之间做了**拉丁方式**的配平。
- **流程**：
  - 染色期：看 **40 个视频**，每个最多 30 分钟；
  - 清除期：执行 **40 次**所分配的策略；
  - 最后通过 MyActivity 清空账号的所有活动。
  - 在 P1（开始）、P2（染色后）、P3（清除后）三个时间点各抓取首页和视频页的 **top-10** 推荐，共 **8,330 条**。
- **环境**：2022 年 8 月，AWS Ohio（us-east-2）机房，每个账号独立 IP，Chrome 装了广告拦截，账号生日统一、性别选"不透露"。
- **标注**：在**频道层面**做人工编码，两名标注者的最终 Cohen's κ 为 0.660 / 0.822 / 0.854 / 0.945。
- **检验**：Wilcoxon 符号秩检验，α = 0.05。

**主要结果**（Table 1、3、4）：

- **染色期**（首页，P1 → P2，全部显著）：Alt-Right **2% → 20%**，Antitheist 11% → 37%，Left 6% → 28%，Right 9% → 29%。视频页只有 Antitheist 和 Right 显著。任何情况下染色都没有超过一半。
- **清除期**（首页，P2 → P3，四个主题的平均相对变化）：

| 策略 | None | Watch neutral | Delete | Dislike | **Not interested** | No channel | Dislike rec. |
|---|---|---|---|---|---|---|---|
| 平均相对变化 | +32% | −38% | −77% | −45% | **−88%** | −49% | −30% |

  - 只有 **Not interested 和 No channel 在四个主题上都显著**。Delete 在 3 个主题上显著，Watch neutral 和 Dislike rec. 在 2 个主题上显著。
  - Not interested 之后 P3 的染色比例：Alt-Right 0%、Antitheist 2%、Left 10%、Right 2%。
- **视频页**：任何策略都**没有显著的清除效果**。作者推测视频页推荐主要受当前正在播放的视频驱动。
- **细分**：
  - Not interested 同时清掉了被操作过的频道和**同主题的新频道**；
  - No channel 剩下的染色几乎全部来自**新频道**，被操作过的频道残留只有 0–2%；
  - Watch neutral 剩下的染色有一半以上来自原来的频道。
- **调查**（Prolific，N = 300，通过注意力检查的 274 人，做了事后分层加权）：

| 按钮 | 知晓率 | 使用率（知晓者中） | 主观有效性（1–5） |
|---|---|---|---|
| Delete | 51.41% | 53.64% | 3.76 |
| Dislike | 93.94% | 37.75% | 2.52 |
| **Not interested** | **56.03%**（约 44% 不知道） | 82.83% | 3.42 |
| Don't recommend channel | 35.37% | 80.53% | **4.10** |

  也就是说，用户的主观感受（最信 No channel）和审计结果（Not interested 最有效）**不一致**。

**局限**：
- 每个格子只有 5 个账号，样本很小；只有 4 个政治或宗教类主题；单一地点、单一时间点；
- 频道层面的标注比较粗；
- 只看了 **40 次操作之后的一个时间点**，**没有测持久性和复发**；
- 每个账号只用一种策略，没有测组合；
- 账号都是全新的，和长期真实用户不同；
- 只有桌面端 YouTube，没有 Shorts，也没有移动端。

**代码 / 数据**：https://github.com/avliu-um/youtube-disinterest 。技术栈是 Python + Selenium + undetected-chromedriver + AWS S3/Terraform，附带分析用的 notebook、频道列表（`communities/`）、标注模板和标注后的推荐数据。调查的原始数据出于匿名考虑**已删除**。README 中"97%"的说法和论文的 88% 不一致。要重跑需要 Google 账号和 AWS，而且 YouTube 的界面已经变了，**现在基本无法原样运行**，但数据可以重新分析。频道标注结果另见论文脚注里的 tinyurl 链接。

**我们可以复用什么**：
- **染色 → 清除 → 测量**的三段式协议，以及 P1/P2/P3 的测量点设计；
- 策略的分类（基于历史 vs 基于推荐）；
- "知晓率 × 使用率 × 主观有效性"的调查量表（可以翻译后用在 HKU 学生身上）；
- 公开的已标注推荐数据，可以用来重新分析。

**它留下的空白**：
- 只有 YouTube，只有美国；
- 没有复发研究；
- 没有中文平台，也没有监管要求的"破茧"功能（比如关闭个性化推荐）；
- 没有测"重置推荐"这类功能；
- 调查人群是美国成年人。

---

## 6. When 'For You' Isn't For You — TikTok 用户能动性审计【全文精读】

**引用**：Kaplan, L., Patel, D., Gerzon, N., Mislove, A., & Sapiezynski, P. (2026). *When 'For You' Isn't For You: Measuring User Agency in TikTok's Algorithmic Feed.* ICWSM 2026. arXiv:2605.10690（东北大学）。

**研究问题**：
1. FYP 对用户信号的个性化程度有多大？
2. 用户表达"不想看"之后，系统会不会响应？
3. 用户**停止**表达"不想看"之后，内容会不会**卷土重来**（relapse）？

**茧房 / 个性化的操作化**：每个阶段的 200 个 FYP 视频中，属于目标主题的视频**个数或占比**。

**方法**：
- **3 个主题**：cooking（常见、无害）、fitness（常见、可能引发身体形象焦虑）、sports betting（少见、可能有害）。每个主题跑 **5 轮**独立实验，共 **15 轮**；每轮新建 **6 个账号**。
- **Phase 1（个性化）**：
  - Watch Topic 账号：搜索主题词，看前 25 个搜索结果（seed），再刷 200 个 FYP 视频，遇到主题视频就看完，其他视频"跳过"（观看 0.2–2 秒）；
  - 同时运行一个 Baseline 账号，所有视频都跳过。
- **Phase 2（表达不感兴趣）**：用**账号克隆**技术把 Watch Topic 账号复制成 4 个：
  - 2 个 **Gives Implicit Signal**：主题视频一律跳过；
  - 2 个 **Gives Explicit Signal**：主题视频看完后标记 **'Not Interested'**。注意这个按钮藏在"分享"菜单或长按菜单里，很难找到。
  - 另外有 Cloned Baseline 和 Non-cloned Baseline 两个对照账号。
- **Phase 3（复发）**：每种信号的两个账号中，一个继续发出负信号，另一个**停止**负信号并恢复观看主题视频（Ceases …）。
- **复发的定义**：Ceases 账号比对应的 Continues 账号**显著**收到更多主题视频（双比例 z 检验，99% 置信水平）。
- **技术手段**：
  - Android 模拟器 + UIAutomator2 控制界面；
  - mitmproxy + SSL unpinning 抓取流量获取视频元数据；
  - 逆向 protobuf（Square Wire）和 Zstandard 字典，用 Frida hook `ttEncrypt` 伪造安全头，从而**重放流量来克隆账号**；
  - 用 `/api/v2/feed` 接口"只取不看"，在不影响算法的前提下测量个性化程度。
  - 克隆验证：4 个克隆账号与原账号在统计上**不可区分**，并且都显著高于 3 个基线账号。
- **分类**：用 ChatGPT-3.5 判断视频是否属于主题。人工标注的 Fleiss κ 为 0.922 / 0.937 / 0.963；ChatGPT 相对人工多数票的准确率为 0.943 / 0.940 / 0.956，cooking 的召回率只有 0.791（所以测出来的个性化程度是**下界**）。

**主要结果**：
- **Phase 1**：200 个视频中，cooking 和 sports betting 各有 **89 个（44.5%）**是主题视频，fitness 有 **76 个（38%）**。基线账号中 cooking 为 17 个（8.5%），fitness 和 sports betting 各 3 个（1.5%）。
- **Phase 2 先导实验（cooking）**：继续观看的账号中主题视频占 30.5%；隐式信号降到 **16%**（相对 −47.5%）；显式 Not Interested 降到 **4.75%**（相对 **−84.4%**），与非个性化基线**没有显著差异**。
- **Phase 2 全部 15 轮**：两种信号都能让主题内容减少。多数轮次里显式信号**显著优于**隐式信号，但隐式信号**和显式一样有效**的轮次也有：cooking 2/5、fitness 2/5、sports betting 1/5。
- **Phase 3 复发**（出现复发的轮数 / 5）：

| | cooking | fitness | sports betting |
|---|---|---|---|
| 停止**隐式**信号 | **5/5** | 4/5 | 2/5 |
| 停止**显式**信号 | 2/5 | 2/5 | 1/5 |

  结论：显式信号的效果**更持久**，但**三个主题都能触发复发**，也就是说，负反馈的效果会被之后重新产生的正向行为**覆盖**。

**局限**（作者自述加我们的补充）：
- 只模拟了观看、跳过、不感兴趣三种行为，没有点赞、分享、举报、关注；
- 账号是全新的，而且只盯一个主题，比真实用户"执着"得多；
- 只有美国、单一时间点，每个主题 n = 5；
- 负反馈阶段没有用新主题"替代"旧主题；
- 统计上显著，不代表**符合用户的期望**，作者明确说"两者可以同时为真"；
- 克隆技术涉及逆向工程，有法律和服务条款上的风险。

**代码 / 数据**：论文检查清单写明 **"No new datasets are being curated or released"**；论文中**没有**给出实验代码仓库，只开源了一个通用的 protobuf 反编译工具 `lumaaaaaa/protoextract`；分类 prompt 在附录 A.1。**不可复现**，而且其技术路线（逆向加密、克隆）**不适合本科一年级团队**。

**我们可以复用什么**：
- **三阶段设计**（个性化 → 负反馈 → 复发），尤其是"**复发**"这个概念和它的操作化（Continue 与 Cease 的对照）；
- 显式与隐式负反馈的二分法；
- 双比例 z 检验这种简单的统计方法；
- "只取不看"式的测量思想：测量本身不能污染被测量的系统。

**它留下的空白**：
- 没有中国平台（抖音、快手、小红书）；
- 没有测试"内容偏好设置"、"关闭个性化"、"刷新 / 重置"等功能；
- 没有公开数据；
- 复发研究只有 5 次重复、3 个主题，而且是用 sock puppet 做的，**没有**在大规模日志或仿真里做过。

---

## 7. Mozilla Foundation (2022) *Does This Button Work?*【全文精读（PDF 报告）】

**引用**：Ricks, B., & McCrosky, J. (2022). *Does This Button Work? Investigating YouTube's Ineffective User Controls.* Mozilla Foundation, 2022-09-20. 报告 PDF：assets.mofoprod.net/network/documents/Mozilla-Report-YouTube-User-Controls.pdf

**研究问题**：YouTube 的用户控制（Dislike、Not interested、Don't recommend channel、Remove from watch history）能在多大程度上**阻止**用户不想要的推荐？用户对这些控制又有什么样的感受？

**方法**：
- **数据来源**：浏览器扩展 **RegretsReporter**，这是一个**真实用户**参与的**随机对照实验**。扩展在每个推荐上叠加一个 "Stop recommending" 按钮，按下后**在后台随机触发**以下之一：Dislike、Not interested、Don't recommend channel、Remove from history；如果用户在**对照组**，则什么都不做。另外还有一个 **UX 对照组**，这组用户看不到按钮，用来测试界面设计对反馈频率的影响。
- **规模**：
  - 时间：2021-12-02 至 2022-06-26；
  - 22,838 人报名，清洗后剩 **22,722 名参与者**；其中 6,147 人至少拒绝过一次视频，共拒绝 **30,314 个**视频；
  - 被推荐的视频共 **567,880,195 个**；可分析的"被拒视频 × 后续推荐"视频对共 **162,983,496 对**。
- **坏推荐的定义**：如果后续推荐和被拒视频**过于相似**，就算一条"坏推荐"。
  - 由 24 名埃克塞特大学的研究助理按统一规则标注了 **44,434 对**（其中可接受 75%、坏推荐 22%、不确定 3%），并用主动学习的方式选样；
  - 再训练一个**语义相似度模型**给其余的视频对打分。
- **指标**：**坏推荐率**是某一实验组所有视频对中坏推荐的比例。"阻止了多少"是与对照组相比，坏推荐率的**相对降幅**。对照组中模型估计的坏推荐率约为 **2.3%**。
- **调查**：2,757 名 RegretsReporter 用户，外加 5 个半结构化访谈。

**主要结果**：

| 控制 | Don't recommend channel | Remove from watch history | Dislike | Not interested |
|---|---|---|---|---|
| 相对对照组阻止的坏推荐比例 | **约 43%** | 约 29% | 约 12% | **约 11%** |

- **同频道推荐**：对照组中，拒绝之后仍来自同一频道的推荐约占 0.4%；Don't recommend channel 组降到约 0.1%，但**并没有降到 0**。
- **首页 vs 侧边栏**：控制在**首页**略有效，在侧边栏更弱。
- **时间效应**：各控制的效果**不随时间变化**；但所有组的坏推荐率都会随着时间自然下降，说明兴趣模型本身会衰减。
- **UX 实验**：一键按钮让反馈频率从每千次观看 37 次提高到 80 次（在剔除极端用户后，50 对 23 次，显著），也就是**提高了一倍多**，而且观看率没有下降。
- **调查**：39.3% 的人认为控制"完全没影响"，23.0% 认为"效果不一"，27.6% 认为"有变化"；78.3% 提到自己用过官方的反馈工具。

**局限**：
- 参与者是 Mozilla 的受众，**不具代表性**，而且只有桌面端 Firefox/Chrome 和英文界面；
- 相似度是"坏"的**代理**：用户拒绝一个视频，不一定意味着讨厌整个主题；
- 各组之间只比较了**相对**降幅，绝对的坏推荐率很低（约 2.3%）；
- 这份报告是倡导性报告，**没有同行评审**。

**数据公开情况**：2023-05-16 在 Hugging Face 发布了 `mozilla-foundation/youtube_regrets`，**CC0 许可**，但需要登录并同意条款才能下载。内容包括：
- RR2 Regrets：20,633 行，即用户按下 "Stop recommending" 的视频；
- **RR2 Recommendations：96,001,836 行，115.72 GB**。

从数据卡的字段来看，**只有**日期、国家、视频 ID、标题、频道、描述、播放量，**看不到实验组别或用户 ID 字段**（我们没有下载全量数据核实）。所以很可能**无法复现分组效果分析**，但可以做描述性分析。

**我们可以复用什么**：
- **"坏推荐率"的定义**（被拒内容与后续推荐的相似度）；
- **随机对照 + 对照组**的设计思想；
- "效果 = 相对对照组的降幅"这种报告方式；
- UX 实验的结论：按钮越容易找到，反馈越多。这一点可以直接对照 TikTok 把 Not Interested 藏在"分享"菜单里的做法，也可以用来讨论中国平台按钮的位置。

**它留下的空白**：
- 只有 YouTube；
- 公开数据很可能不带分组信息；
- 没有中文或短视频场景；
- **在 "Not interested" 的效果上，与 Liu et al.（最有效，−88%）的结论几乎相反**（Mozilla 测得只有约 11%）。两者的样本、指标和时间都不同，这个**矛盾本身就是值得讨论的点**：是"主题层面的染色比例"更合适，还是"单个被拒视频的相似推荐"更合适？

---

## 8. Exploring the Filter Bubble（MovieLens）【全文精读】

**引用**：Nguyen, T. T., Hui, P.-M., Harper, F. M., Terveen, L., & Konstan, J. A. (2014). *Exploring the Filter Bubble: The Effect of Using Recommender Systems on Content Diversity.* WWW '14, pp. 677–686. DOI 10.1145/2566486.2568012。全文 PDF 可以在 IW3C2 的存档下载：archives.iw3c2.org/www2014/proceedings/proceedings/p677.pdf

**研究问题**：
- RQ1：推荐系统会不会让用户接触到的内容**随时间变窄**？
- RQ2：**采纳推荐**的用户和**不采纳推荐**的用户，体验有什么不同？

**茧房的定义**：个人层面的内容多样性随时间下降。

**数据**：
- MovieLens 的真实日志，时间是 **2008 年 2 月至 2010 年 8 月（论文写的是 "21 months"）**。由于前后有日志缺失，前后各留了一个月作为缓冲。
- 推荐算法是 item-item 协同过滤，推荐页面是 "Top Picks For You"，默认显示 15 部电影。
- 只分析在这段时间内首次评分、并且至少有 3 个"评分块"的用户，共 **1,405 人**，贡献了 173,010 条评分，涉及 10,560 部电影，访问 Top Picks 页面 150,759 次。
- 这份日志**不公开**。tag genome 是公开的，但他们用的是 2013 年 4 月的快照：9,543 部电影 × 1,128 个标签。

**方法**：
- **评分块**：去掉每个用户的前 15 个评分和随后 3 个月的评分，然后每 **10 个连续评分**划为一块。
- **"采纳了推荐"**：用户评分的这部电影，在评分前的 **3 小时到 3 个月**之间曾出现在他的 Top Picks 里。
- **分组**：
  - **Following Group**：至少 **50%** 的评分块里采纳过推荐，共 **286 人**；
  - **Ignoring Group**：**从未**采纳过推荐，共 **430 人**（其中 52 人从来没打开过 Top Picks）。
- **内容多样性**：每部电影表示为 tag genome 向量，两部电影之间的距离是
$$d(m_i,m_j)=\sqrt{\sum_{k}\big[rel(t_k,m_i)-rel(t_k,m_j)\big]^2}$$
  一个列表的多样性是列表内**平均**两两距离（同时报告**最大**两两距离）。推荐多样性用 top-15 计算，消费多样性用每块的 10 部电影计算。
- **体验**：块内平均评分，以及对应的百分位。
- **检验**：组内用配对 t 检验，组间用 Welch t 检验。

**主要结果（注意方向）**：
- **RQ1，推荐的多样性**（top-15 平均距离）：
  - 全体用户 25.02 → 24.67（p = 2.43e-6），**显著但幅度很小**；
  - Following 组 25.22 → 24.80（p = 0.014）；
  - Ignoring 组 24.74 → 24.51（p = 0.087）；
  - Following 组收到的推荐始终**比 Ignoring 组更多样**（组间 p = 0.0037 和 0.041），但差距从 0.48 缩小到 0.29。
- **RQ2a，消费的多样性**（每块平均距离）：
  - 全体用户 26.60 → 26.01（p = 1.5e-12）；
  - **Following 组 26.67 → 26.30**（下降 0.37）；
  - **Ignoring 组 26.59 → 25.86**（下降 0.73，是 Following 组的约 2 倍）；
  - 起点没有差异（p = 0.616），终点有差异（p = 0.006）；用最大距离算，结论相同。
- **RQ2b，体验**（平均评分）：
  - Following 组 3.69 → 3.68（p = 0.7，基本不变）；
  - Ignoring 组 3.74 → **3.55**（p = 3e-11）；
  - 换算成百分位：Following 组下降 1.2 个百分位，Ignoring 组下降 **18.86** 个百分位。
- **结论**：所有人的消费都会**自然变窄**（这是一种人自身的趋势，不完全是算法造成的）；**采纳推荐反而减缓了变窄**，并带来更好的体验。所以推荐系统在这个场景里起的是"**拓宽**"作用。后来 Aridor et al. (2020) 用理论模型解释了这一现象。

**局限**：
- 是观察性研究，存在**自选择**问题：愿意采纳推荐的人本身可能就更爱探索；
- 电影领域、2008–2010 年、item-item 协同过滤，和今天的短视频加深度模型相去甚远；
- 效应量很小（距离只变了 0.3–0.7，而全库电影距离的标准差是 4.45）；
- "采纳推荐"的时间窗口（3 小时到 3 个月）是启发式的。

**代码 / 数据**：日志不公开。tag genome 可以在 MovieLens 的 Tag Genome 数据集里获得（公开）。

**我们可以复用什么**：
- **"跟随 vs 忽略"的分组设计**：可以换成"**用负反馈 vs 不用负反馈**"的分组，这正是 KuaiRand 的 `is_hate` 可以支持的；
- 分块来控制活跃度差异的技巧；
- 把"自然变窄"作为基线的思想：**不能把所有变窄都归咎于算法**。

**它留下的空白**：
- 研究的是"采纳推荐"，而不是"拒绝推荐"或负反馈；
- 只有电影、美国，年代久远；
- 没有短视频，没有中文平台。

---

## 9. What Are Filter Bubbles Really?【全文精读】+ 2023–2026 相关度量 / 审计速览

**引用**：Leysen, J., Michiels, L., Goethals, B., & Smets, A. (2022). *What Are Filter Bubbles Really? A Review of the Conceptual and Empirical Work.* UMAP '22 Adjunct. DOI 10.1145/3511047.3538028。PDF：adrem.uantwerpen.be/bibrem/pubs/bubbles.pdf

**操作化定义**（原文）：
> "A technological filter bubble is **a decrease in the diversity of a user's recommendations over time, in any dimension of diversity, resulting from the choices made by different recommendation stakeholders**."

这个定义有四个要素：
1. **多样性**：包括结构多样性（信息来源）、主题多样性、观点多样性；
2. **推荐**：测的是推荐给用户的内容，不是用户实际消费的内容；
3. **时间**：必须是纵向的，最好从推荐系统"认识"用户之前就开始测；
4. **推荐的利益相关方**：用户、内容提供者、系统。

**对既有研究的重新归类**：只有 4 项研究完全符合这个定义：Nguyen et al. 2014（MovieLens）、Bountouridis et al.（SIREN 新闻仿真）、Tomlein et al. 2021（YouTube 虚假信息审计，观看辟谣视频可以"戳破"茧房）、Lu et al.（新闻网站干预实验）。其余大量研究只是在**某一时刻**比较不同用户或不同算法的多样性，**不能**作为茧房存在的证据。

**对我们的意义**：
- 按这个定义，"**逃离**"应该被操作化为：**用户做出某种选择之后，推荐多样性的下降被逆转，或者在一段时间内被止住**。
- 必须说明：测的是哪个维度的多样性、推荐还是消费、时间跨度多长、是谁的选择（用户按按钮，还是平台注入）。
- 我们的项目可以用这四个要素给每一篇文献归类，并用它来检验自己的实验设计是否合格。

**2023–2026 年补充检索结果**（检索词：escape filter bubble、user agency recommender audit、negative feedback effectiveness、not interested button）：

| 工作 | 要点 | 与本主题的关系 | 阅读深度 |
|---|---|---|---|
| Wang, Y. et al. (Google), *Learning from Negative User Feedback and Measuring Responsiveness for Sequential Recommenders*, RecSys '23, arXiv 2308.12256 | 把点踩和跳过作为**训练标签**（"not-to-recommend" 损失）。线上 A/B 测试中点踩率 −2.44%，对同一创作者的重复点踩 −9.60%。提出**反事实仿真**来测"响应度"：同一段历史在第 k 步分别给正反馈和点踩两个分支，比较第 k+1 步推荐与最后一个物品的相似度变化。点踩只作为输入特征时，相似推荐下降 22.7%（内容）/ 22.8%（创作者）；同时作为输入特征和训练标签时，下降 **60.8% / 64.1%** | **平台自己的"负反馈响应度"指标**，和 BEP 的对照仿真思路相通；说明负反馈**要进入训练目标才真正起作用** | 全文浏览 |
| Sukiennik, N. et al. (Tsinghua), *SimTok: Simulating Filter Bubble on Short-video RS with LLM Agents*, arXiv 2504.08742 | 用真实短视频数据加 LLM 用户智能体仿真茧房的形成，并测试冷启动比例、反馈权重等**干预**（例如调换"只看"与"看并点赞"的权重），报告熵等指标的变化 | 可以借鉴它在中文短视频场景下做"**反馈权重干预**"的仿真思路 | 摘要 + 快速浏览 |
| Shi, W. & Li, J. (2024), *New Digital Divide Shaped by Algorithm? Evidence from Agent-Based Testing on Douyin's Health-Related Video Recommendation*, Communication Research；以及 Digital Journalism 13(7) (2025) *News Diversity Under Algorithms… on Chinese TikTok (Douyin)* | **抖音上确实已经有 sock puppet（agent-based testing）审计**。后者发现算法推荐的新闻类别比随机推荐更多样 | 说明"在抖音做审计"本身**不算新**；但这两项研究**据我们检索并未针对"不感兴趣"或"内容偏好设置"等用户控制** | 只读了摘要和新闻报道，**未读全文，需要核实** |
| 抖音 2025 年 4 月"安全与信任中心"开放日（新华网报道） | 平台自述用多样性打散、多兴趣召回、随机推荐、"不感兴趣不再展现"、关闭个性化、内容偏好设置等手段来"破茧" | **平台的自我陈述，缺少独立验证**，这正是研究空白所在 | 新闻报道 |
| Tomlein et al. (2021, RecSys) / Srba et al. (2023, TORS) | YouTube 虚假信息审计：先看宣扬虚假信息的视频，再看辟谣视频，可以"戳破茧房"，但搜索结果和推荐的反应不同 | 属于**"用观看新内容来逃离"**的策略，对应 Liu et al. 中的 Watch neutral | 只读了 Leysen et al. 的转述 |

---

## 10. (a) 对比表：各工作如何操作化"茧房"与"逃离 / 控制有效性"

| 工作 | 平台 / 环境 | 茧房（或 stain）的操作化 | "逃离 / 控制有效"的操作化 | 被测试的用户动作 | 时间维度 / 复发 | 真实平台？ | 代码 / 数据可得性 |
|---|---|---|---|---|---|---|---|
| **BEP**（Feng 2026） | ml-1m、Amazon-Books，LLM 用户仿真 | 每轮推荐覆盖的**类别数** D_{u,t} | **BEP = Σ正向用户 D ÷ Σ负向用户 D**，对 T 轮取平均；越接近 1 说明越难逃 | "主动多看不喜欢的内容"（prompt 加属性设置） | 8 轮反馈闭环；无复发 | 否（仿真） | 代码**尚未发布**；数据公开 |
| **UCRS**（Wang 2022） | DIGIX、ML-1M、Amazon-Book，离线 | Isolation Index、MCD、Coverage | 在假设用户发出命令后：Iso-Index、MCD **下降**，TCD、W-NDCG **上升**，同时准确率不降 | 4 类**命令式**控制（参数 α、β 表示强度） | 单次推理；无复发 | 否 | **代码 + 数据 + 预训练模型齐全**（需要 GPU，无开源许可证） |
| **DDIR**（Li 2026） | KuaiEnv、KuaiRand 强化学习仿真 | 短窗口内同类别重复超过阈值 → 用户离开；MCD | 会话长度、累计奖励上升，MCD 下降 | 无用户控制（平台侧强化学习） | 会话内的动态 | 否（基于真实日志的仿真） | 代码已公开，但环境配置不完整 |
| **CD-CGCN**（Tang 2025） | Gowalla、Amazon-Book、ML-2k | ILFBI@k（同社区物品占比）、CGI@k | ILFBI 和 CGI 下降，准确率不降 | 无（平台侧模型） | 无 | 否 | 未找到代码 |
| **Liu, Wu & Resnick**（ICWSM 2024） | YouTube 桌面端，sock puppet | **stain = 主题推荐占比**（首页和视频页的 top-10） | 清除期 P2 → P3 的**相对下降**（Wilcoxon 检验）；另有知晓率、使用率、主观有效性调查 | Not interested、No channel、Dislike、Dislike rec.、Delete、Watch neutral | 40 次操作后的一个时间点；**无复发** | **是** | 代码和标注数据已公开（难以原样重跑） |
| **Kaplan et al.**（ICWSM 2026） | TikTok 移动端，sock puppet + 账号克隆 | 200 个 FYP 视频中的主题视频数 | 显式与隐式负反馈下的主题占比（z 检验）；**复发 = 停止负反馈后显著反弹** | Not Interested（显式）、跳过（隐式） | 3 × 200 个视频；**唯一测了复发的工作** | **是** | **未公开** |
| **Mozilla**（2022） | YouTube，22,722 名真实用户，随机对照实验 | 被拒视频与后续推荐的**相似对**（坏推荐） | **相对对照组的坏推荐率降幅** | Dislike、Not interested、No channel、Remove history | 按拒绝后的时间分层（1 周、4 周、更久） | **是（真实用户）** | 数据在 HF 上公开（CC0，需同意条款）；很可能**不含实验组别** |
| **Nguyen**（2014） | MovieLens 真实日志 | tag genome 平均两两距离随时间下降 | 采纳推荐的一组比忽略推荐的一组**变窄更少** | 采纳推荐（正向） | 约 2 年，纵向 | **是（观察性）** | 日志不公开 |
| **Leysen / Michiels**（2022） | 概念综述 | "推荐多样性随时间下降"（任意维度，由某个利益相关方的选择引起） | （隐含）下降被逆转或止住 | — | 强调必须纵向 | — | — |
| **Wang (Google) 2023** | YouTube 类产品，线上 A/B + 反事实仿真 | — | **响应度** = 点踩分支与正反馈分支在第 k+1 步推荐相似度的相对变化 | 点踩、跳过 | 只看下一步 | 是（平台内部） | 不公开 |

**一句话总结**：审计类研究（YouTube 和 TikTok）测的是"**主题占比能降多少**"，而且只有 Kaplan 测了"**会不会反弹**"；机器学习类研究测的是"**模型在假设或仿真的用户下能不能更多样**"。**两类研究之间没有接口**：没有人用**公开的真实负反馈日志**去检验"负反馈之后同类内容的曝光是否下降、能维持多久"，也没有人检验中国平台上**监管推动的"破茧"功能**。

---

## 11. (b) 综合与研究空白

**综合（约 400 字）**：
现有证据可以概括成三句话。
第一，**用户侧的控制"有用，但有限，而且不稳定"**。YouTube 的 sock puppet 审计显示 "Not interested" 能让首页的主题占比平均下降 88%，TikTok 的显式 Not Interested 能把主题内容压到接近基线；但 Mozilla 在真实用户上测到的坏推荐阻止率只有 11–43%，而且 TikTok 在三个主题上都出现了**复发**。结论的差异主要来自**指标**：主题占比和单个被拒视频的相似推荐是两种不同的量；也来自**场景**：新账号加单一主题，和真实用户的混合兴趣很不一样。
第二，**"可逃离性"的度量还处在起步阶段**。BEP 是目前唯一**以用户意图为条件**的指标，但它只数类别个数，把"想逃"和"活跃度"混在一起，而且由于比值形式，它天然看不出同比例的多样化。Google 提出的"响应度"是平台内部的对应物，但只看下一步。
第三，**平台侧的修复**大多在准确率约束下重排、做反事实推理或对抗去偏（UCRS、CD-CGCN、DDIR），评估基本都是离线或仿真，而且普遍**不对接真实的按钮**。DDIR 还提醒我们：**适度的同质化可能是有益的**。
最后，Nguyen (2014) 提示，消费变窄有一部分是**人自身的趋势**，推荐甚至可能减缓变窄。任何研究都应该设置"不干预"基线，以区分"自然变窄"和"算法变窄"。

**一年级团队可以可信地填补的 5 个空白**（附新颖性的诚实评估）：

1. **用 KuaiRand 的真实负反馈做"事件研究"（最推荐）**：以每条 `is_hate = 1` 为事件，比较事件前后 N 次曝光中**同一 `tag` 的曝光占比**，对照组是同一用户在没有点踩时的时刻，或者是匹配的其他用户。`is_rand = 1` 的随机曝光可以作为"不受个性化影响"的参照。
   - **新颖性**：据我们检索，**还没有论文在公开的中文短视频日志上报告"点踩后同类曝光是否下降、能维持多久"**。DDIR、DORL 只是把 KuaiRand 当作强化学习环境，并没有做这个描述性分析。
   - **风险**：这是观察性分析，只能报告**关联**；`is_hate` 非常**稀疏**（见附录 B，Pure 版本只有约 0.4–1.1‰），需要改用 KuaiRand-1K（1.1 GB）或 27K；日志只覆盖 2022 年 4–5 月的约 1 个月。
2. **在同一个开源仿真器里横向比较"逃离策略"**：用 ML-1M 或 KuaiRand 加一个简单的矩阵分解反馈闭环，比较以下策略：
   - (a) 按 X 公开的权重惩罚负反馈：X 2023 年开源的 Heavy Ranker 中 `negative_feedback_v2` 权重是 **−74**，`report` 是 −369，`fav` 是 0.5，`reply` 是 13.5。**注意**：这些权重乘的是**预测概率**，不是"点一次就扣分"的更新规则，所以需要自己假设负反馈如何改变这个预测概率，这一点必须写进报告；
   - (b) 只跳过（隐式负反馈）；
   - (c) 主动多看其他内容（BEP 的正向行为）；
   - (d) 平台随机注入 k% 的内容；
   - (e) 重置画像。
   统一用 BEP、MCD、Isolation Index 加上"逃离所需步数"来比较。
   - **新颖性**：中等。单个策略的仿真前人都做过，但**把用户按钮和平台注入放在同一套指标下比较**的工作我们没有找到。
3. **"复发半衰期"**：在仿真里复刻 Kaplan 的三阶段设计（个性化 → 负反馈 → 停止负反馈），量化停止负反馈后主题占比回到阈值所需的步数，并比较显式和隐式负反馈的持久性。
   - **新颖性**：较高。复发目前**只有** Kaplan 用 sock puppet 测过（每格 n = 5），还没有人在仿真或日志里做过。
4. **BEP 的方法论补丁**：证明并用实验演示"比值型 BEP 对同比例多样化不变"会导致"轻度随机无效"的结论有一部分是指标造成的；提出一个差值型指标 ΔD = D − D′，或"逃离步数"，作为补充。
   - **新颖性**：小而扎实，属于**方法学上的澄清**，适合写成报告里的讨论部分。
5. **中国平台"破茧"功能的小规模对照审计或问卷**（可选）：针对抖音、小红书的"不感兴趣"、"内容偏好设置"、"关闭个性化推荐"，用 2–3 个新账号在两个主题上手动做"染色 → 清除"的小实验；或者仿照 Liu et al. 的量表，调查 HKU 学生的知晓率、使用率和主观有效性。
   - **新颖性**：**控制功能**层面的独立检验确实缺乏（已有的抖音审计关注的是新闻和健康内容的多样性）。但样本很小、是手动操作、受服务条款限制，**只能作为探索性的证据**，不能下因果结论。

**建议**：以空白 1 为主（真实数据加上最清楚的 gap），辅以空白 2 和 3（在仿真里比较策略并测复发），空白 4 放进讨论部分，空白 5 视时间和伦理审批情况决定是否做。

---

## 12. 附录：可行性探针（本次实际运行）

**A. UCRS 预计算结果不需要 GPU 就能直接用于茧房诊断**（只读 `/home/user/wenjiewwj/ucrs`，纯 numpy）：
- 数据：读取 `FM_ml_1m_*_top100_result.npy`（6,035 个用户）、`training_list.npy` 和 `item_category.npy`（ML-1M 共 18 个类别）。
- 在**全体用户**上计算：
  - 历史最大类别在 top-10 推荐中的占比 = **0.290**；
  - 相对历史占比的"放大量" = +0.013；
  - top-10 覆盖的类别数平均为 **8.47**。
- 与论文对比：论文 Table 4 中 ML-1M 上 FM 的 Coverage 是 8.66，和我们算出的 8.47 接近。论文的 MCD 是 0.599，与我们的 0.290 不同，原因是论文只在"偏好迁移用户"子集上计算，而且 GD 的归一化方式也不同。**不能直接对比**，但这说明整条管线可以跑通。

**B. KuaiRand-Pure 中负反馈的稀疏程度**（从 zenodo 10439422 下载，47 MB，CC BY-SA 4.0）：

| 日志 | 行数 | `is_hate` 次数 | 每千次比例 | 有过点踩的用户数 |
|---|---|---|---|---|
| 标准推荐 4/08–4/21 | 1,141,112 | 480 | 0.42‰ | 258 |
| 标准推荐 4/22–5/08 | 295,497 | 230 | 0.78‰ | 144 |
| **随机曝光** 4/22–5/08（`is_rand = 1`） | 1,186,059 | 1,351 | **1.14‰** | 459 |

- 随机曝光的点踩率比个性化推荐**更高**，这是个性化起作用的一个旁证。
- 标准日志中的点踩主要发生在 `tab = 1`（480 次里有 375 次）。
- 视频的 `tag` 共有 110 种，约 24% 的视频有多个 tag。
- **结论**：Pure 版本的样本太少，不足以做事件研究，**应改用 KuaiRand-1K**（1,000 个用户，1,170 万条交互，压缩包 1.1 GB）。KuaiRand-1K 中的实际点踩数量尚未统计，需要在开题时先确认。

---

### 参考链接
- BEP：https://arxiv.org/abs/2512.03067 ｜ 代码仓库（空）：https://github.com/fengdifu24/bepmetric
- UCRS：https://arxiv.org/abs/2204.13844 ｜ https://github.com/WenjieWWJ/UCRS （本地：/home/user/wenjiewwj/ucrs）
- DDIR：https://doi.org/10.1145/3828182 ｜ https://github.com/16061025/DDIR
- CD-CGCN：https://arxiv.org/abs/2508.11239
- Liu, Wu & Resnick：https://arxiv.org/abs/2307.14551 ｜ https://github.com/avliu-um/youtube-disinterest
- Kaplan et al.：https://arxiv.org/abs/2605.10690
- Mozilla 报告：https://assets.mofoprod.net/network/documents/Mozilla-Report-YouTube-User-Controls.pdf ｜ 数据：https://huggingface.co/datasets/mozilla-foundation/youtube_regrets ｜ 新闻稿：https://www.mozillafoundation.org/en/blog/mozilla-investigation-youtubes-dislike-button-other-user-controls-largely-fail-to-stop-unwanted-recommendations/
- Nguyen et al. 2014：https://archives.iw3c2.org/www2014/proceedings/proceedings/p677.pdf
- Leysen, Michiels et al. 2022：https://adrem.uantwerpen.be/bibrem/pubs/bubbles.pdf
- Aridor et al.（对 Nguyen 结果的理论解释）：https://arxiv.org/abs/1904.10527
- Wang et al. (Google) 2023：https://arxiv.org/abs/2308.12256
- SimTok：https://arxiv.org/abs/2504.08742
- 抖音相关审计：https://journals.sagepub.com/doi/10.1177/00936502241262056 ；https://www.tandfonline.com/doi/full/10.1080/21670811.2025.2450312
- 抖音算法开放日报道：http://www.news.cn/tech/20250416/cb30d07cc64f497b938b82f551204e05/c.html
- KuaiRand：https://kuairand.com/ ｜ https://zenodo.org/records/10439422
- X Heavy Ranker 权重：https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md
