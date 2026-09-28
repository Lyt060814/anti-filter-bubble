# 深度调研汇总：已有工作做到了哪里？研究空白在哪？

> 2026-09-28。汇总四份深度调研（论文全文 + 代码 + 数据）：
> - `A_kuaishou_ustc_lineage.md`：KuaiRec、KuaiRand、CIRS、DORL、KuaiSim（含 KuaiRand 实测、KuaiEnv 在 CPU 上跑通）
> - `B_tsinghua_cocoon_lineage.md`：Li 2022、Deep Filter Bubble 2024、Piao 2023 (*NMI*)、Hou 2023、Spotify 2020、新闻茧房 2025
> - `C_escape_user_control.md`：BEP、UCRS、YouTube stain→scrub、TikTok 2026、Mozilla、Nguyen 2014、DDIR
> - `D_simulation_models_audits.md`：Chaney 2018、T-RECS、Jiang/Mansoury、三重过滤气泡、YouTube 审计数据复现、Hosseinmardi 2024
>
> 相关分析脚本在 `analysis/deep_A_*`、`analysis/deep_D/`。

---

## 1. 已被确立的事实（可以直接引用）

| 事实 | 证据 |
|---|---|
| **算法确实会收窄曝光** | KuaiRand 同一视频池内：算法曝光的首位标签占比 0.312 vs 随机曝光 0.215；不同标签数 9.49 vs 11.87（我们自己算的，见 `analysis/deep_A_kuairand_kuairec/`） |
| **用户自己的选择往往比算法更窄** | Spotify：自主收听几乎总比算法收听更多样（Anderson 2020）；快手：实际观看多样性 < 推荐曝光多样性（Li 2022）；PACIS 2025：一年内 55.7% 的新用户陷入茧房，用户选择的作用大于算法 |
| **"茧房用户比例"随时间基本恒定，但茧房在变"深"** | Sukiennik 2024（注意：他们用中位数作阈值，"比例恒定"部分是定义造成的） |
| **负反馈和自主探索能抑制茧房** | Piao 2023 模型：γ₋（负反馈）、σ（自主探索）越大越不容易成茧；σ 从 0.04 升到 0.07 就能让部分用户脱离深度茧房 |
| **"不感兴趣"按钮的效果差异巨大** | YouTube 模拟账号：主页该话题 −88%（Liu 2024）；TikTok：−84%，但停用后会复发（Kaplan 2026）；真实用户随机对照实验：只挡住约 11%（Mozilla 2022） |
| **入茧慢、破泡可以很突然，但强烈依赖话题** | YouTube 审计数据复现：每看一个视频入茧分数最多 +0.01；切换到辟谣内容后，疫苗话题立刻 −0.53，登月话题几乎不变（`analysis/deep_D/yaudit_reanalysis/`） |
| **推荐"遗忘"历史大约需要 30 个视频** | Hosseinmardi 2024（YouTube 侧栏） |
| **轻度随机推荐不能缓解茧房** | BEP（AAAI 2026）。注意：这个结论部分是 BEP 比值形式本身造成的 |

## 2. 现有研究的共同盲点（我们发现的方法学问题）

1. **茧房怎么测，各说各话，而且结论依赖定义。**
   - 覆盖率 + 中位数阈值（Sukiennik）、熵比 s̃（Piao）、MCD（DORL / UCRS）、Isolation Index（UCRS）、BEP 比值……
   - **问题实例：** 在 KuaiRec 上，纯随机推荐的 MCD 就有约 0.8–0.87，所以 MCD 没有中性参照；BEP 的比值形式对两组"同比例变多样"不敏感。
2. **基准环境过于简化，可以被钻空子。**
   - CIRS 的 KuaiEnv 里，"用户无聊离开"是一条确定性规则（只要和上一条共享任一类别就离开）。
   - 一条不需要学习的简单规则（按热度排序、跳过同类）得分 **172.8，高于 CIRS 的 122.5**。
3. **几乎全部站在"平台"视角。**
   - 茧房指标都需要平台的全量日志；"解决方案"都是平台换算法（RL、因果、重排）。
   - UCRS 的"用户控制"是离线假设出来的，没有真实按钮、没有多轮反馈。
4. **"逃离"研究很少，而且只有 YouTube/TikTok 的黑箱审计**，结论互相矛盾（88% vs 11%）；复发只有 Kaplan 用每个话题 5 个账号测过。
5. **没有人用"真实平台公开的推荐机制"做研究。**
   - 所有模拟用的都是教科书式推荐器（矩阵分解、内容相似、RL 策略）。
   - X 2026 年 8–9 月公开的真实打分公式、权重、作者多样性、DPP：**没有人从茧房角度分析过**（见 `../../resources/x_algorithm_prior_analyses.md`）。
6. **"用户自己能否发现茧房"几乎没人量化。**
   - 已有的是"提高意识"的可视化工具：Nagulendra & Vassileva 2014（163 人，意识和控制感提升）、VisualBubble。
   - **没有人评估：用户屏幕上看得到的信号，能提前多久、多准确地发现茧房在形成。**
   - 反差：X 代码里自己就在算推荐流的多样性（`ResponseDiversityStats`：作者 HHI、熵……），但不给用户看。

## 3. Gap 矩阵

| 工作 | 平台/数据 | 视角 | 入茧 | 发现 | 逃离 | 复发 | 真实平台机制 | 方法 |
|---|---|---|---|---|---|---|---|---|
| Li 2022 / Sukiennik 2024 | 快手日志（不公开） | 平台 | ✅ | — | — | — | — | 日志测量 |
| Piao 2023 (*NMI*) | 快手 + MIND | 平台/模型 | ✅ | — | 部分（γ₋, σ） | — | — | 动力学模型 |
| Anderson 2020 | Spotify | 平台 | ✅ | — | — | — | — | 日志测量 |
| CIRS / DORL / DDIR | KuaiRec/KuaiRand | 平台 | ✅ | — | 平台算法 | — | — | 离线 RL |
| UCRS | ML-1M 等 | 平台（假设的用户控制） | ✅ | 平台侧检测 | 离线假设 | — | — | 反事实推理 |
| BEP (AAAI'26) | ML-1M、Amazon | 平台/模拟 | — | — | ✅ 指标 | — | — | LLM 模拟用户 |
| SimTok | 合成 | 模拟 | ✅ | — | 平台权重 | — | — | 20 个 LLM 智能体 |
| Liu 2024 | YouTube | 用户 | ✅ | — | ✅ | — | 黑箱 | 模拟账号审计 |
| Kaplan 2026 | TikTok | 用户 | ✅ | — | ✅ | ✅（n=5） | 黑箱 | 模拟账号审计 |
| Mozilla 2022 | YouTube | 用户 | — | — | ✅ | — | 黑箱 | 真实用户随机对照实验 |
| Tomlein/Srba | YouTube | 用户 | ✅ | — | ✅（看辟谣） | — | 黑箱 | 模拟账号审计 |
| Nagulendra 2014 | 自建社交网络 | 用户 | — | 意识提升 | 控制 | — | — | 可视化 + 用户研究 |
| Chaney 2018 / T-RECS | 合成 | 平台 | ✅ | — | — | — | — | 模拟 |
| **我们（候选）** | X 2026 公开机制 + KuaiRec/KuaiRand 校准 | **用户** | ✅ | **✅ 早期预警** | **✅ 逃离成本** | **✅** | **✅ 白箱** | 代码分析 + 模拟 + 设计 |

**结论：**
- "发现"这一列几乎全空，"复发"这一列只有一个样本很小的工作；
- "真实平台机制"这一列要么是空的，要么是黑箱。
- 我们候选问题的空白**站得住**。

## 4. 我们可以直接复用的东西

| 可复用 | 来源 | 用途 |
|---|---|---|
| Piao 四参数模型（β, γ₊, γ₋, σ）和 s̃ 三档分类，代码公开（MIT） | tsinghua-fib-lab/Adaptive-Information-Dynamic-Model | 理论框架：把 X 的机制映射到 β/γ₋，把用户操作映射到 σ；s̃ 作为"茧房深度"的标准答案 |
| X 打分公式、权重、作者多样性、DPP | `xai-org/x-algorithm` + 我们的代码地图 | 模拟器里的推荐器 |
| KuaiRec（类别、用户偏好）、KuaiRand（算法 vs 随机的收窄比例） | 已下载 | 设定用户偏好；校准"推荐会收窄多少" |
| YouTube 审计曲线、"约 30 个视频遗忘"、88% / 84% / 11% | Srba / Hosseinmardi / Liu / Kaplan / Mozilla | 校准和检验模拟器（曲线形状、效果量级的合理范围） |
| UCRS 的纯 Python 指标函数（Isolation Index、MCD、Coverage） | 本地 `/home/user/wenjiewwj/ucrs` | 多指标对比（无开源许可证，引用时说明） |
| KuaiEnv（CPU 可跑） | CIRS 代码 | 备用环境 / 对照 |
| Chaney 式模拟设定（Dirichlet 偏好、位置偏差、K = 20 等） | Chaney 2018 | 模拟参数的合理起点 |

## 5. 对核心问题的判断

候选核心问题：
> **How early can users detect — and how cheaply can they escape — an information cocoon under X's open-sourced feed algorithm?**

- **创意 / 空白：** 发现（用户视角的早期预警）+ 逃离成本 + 复发，放在**真实平台公开的机制**里研究，现有工作没有覆盖（见第 3 节）。再加上 X 代码 2026 年 8–9 月才公开，符合"非常新"。
- **技术深度：** 代码分析、数据校准（KuaiRec/KuaiRand）、模拟、指标设计、工具设计，每一部分都有明确的技术内容。
- **可信度：** 有真实数据证据（KuaiRand 的收窄比例、YouTube 曲线）和经典模型（Piao）做锚点。
- **必须诚实说明：**
  - 模拟的是"X 公开的机制"，不是"真实的 X"；
  - "不感兴趣"如何改变模型预测需要假设，要做敏感性分析；
  - "负反馈后同类内容是否减少"用公开真实数据答不了（KuaiRand-Pure 里只有 2,061 次"讨厌"，前后变化与对照组无差异），只能以模拟为主。

## 6. 待办

- [ ] 团队确认核心问题
- [ ] 在 Google Scholar、知乎、CSDN 上再确认"没人从茧房角度分析过 X 2026 代码"
- [ ] 下载 Piao 的代码，看能否直接复用
- [ ] 若需要真实数据回答负反馈问题：评估下载 KuaiRand-1K（4.3 GB），做事件研究
