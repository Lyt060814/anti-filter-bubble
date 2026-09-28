# Feasibility Pilot：用户能否从"屏幕可见信号"提前察觉 information cocoon？（Detection half）

> COMP1110 Project Plan 可行性部分 · 数据：KuaiRec 2.0 big_matrix（主）+ KuaiRand-Pure（复核）
> 代码与输出都在本目录：`01_prep_kuairec.py` → `02_kuairec_userday.py` → `03_describe.py` → `05_evaluate.py` → `06_extra.py` → `07_figures.py`（公共函数在 `detect_lib.py`；每步输出在对应的 `.out` 文件）。

## 0. 一句话结论

- **管线跑得通**：用户在前 20 条内容里能看到的信号，尤其是 **S20（前 20 条里占比最高的类别的份额）**，确实带有预警信息。预测"未来 3 天会进入 cocoon 状态"时，test AUC 为 **0.73（单一阈值规则 S20 ≥ 0.5）/ 0.78（screen-only logistic regression）**；platform-side 全信息的上限参考是 **0.85**。**Information gap ≈ 0.08 AUC（95% CI 0.06–0.11）**。
- **但结果有三个重要保留**：
  1. KuaiRec 里"相对自身 baseline 的真实收窄"很少见。X=15% 的事件中约有一半能用抽样噪声解释（观测 2.0% 的 user-days，噪声 null 为 1.1%）；按整段合并计算，几乎没有用户下降 ≥15%。
  2. 事件集中在低活跃用户身上（噪声更大），并且集中在第 58–60 天的一次全平台波动（占 44% 的事件）。
  3. 光用"今天看了多少条"（activity，log n）就能拿到 AUC 0.83。
- **所以最终设计必须校准噪声并控制 activity**（见第 6 节）。KuaiRand-Pure 太稀疏，无法做 user-day 复现（只有 3% 的 user-days 达到 20 条）。

---

## 1. 数据事实与清洗

| 项目 | 数值 |
|---|---|
| big_matrix 原始行数 | 12,530,806（7,176 users × 10,728 videos），全部有 timestamp |
| 完全重复（user, video, timestamp） | 968,005 行 → 删除（日志重复） |
| 同一 user–video 在同一天内重复出现 | 再删 361,978 行，只保留当天第一次（多数重复播放的间隔是 0 秒，属于循环重播，不算新 exposure） |
| 跨天重复出现 | **保留**（间隔中位数约 3 周，说明 feed 确实又推了一次） |
| 最终 exposures | **11,200,823** |
| 类别 | `kuairec_caption_category.csv` 的 first_level_category：38 个已知类别 + UNKNOWN。**UNKNOWN（0.15%）不计入 entropy 和 D20/S20**，只在计数 n 中出现 |
| author | `item_daily_features.author_id`（每个 video 取众数），覆盖 100% |
| **实际有数据的日期（重要）** | 不是"第 2、6 周缺失"那么简单：**只有 28 天，分成 3 段连续区间**：A = 07-05..07-12（day 0–7），B = 08-01..08-10（day 27–36），C = 08-27..09-05（day 53–62）。两段之间分别断了 19 天和 16 天 |
| 每个 user-day 的 exposures | 中位数 39，P25 = 18，P75 = 76，P90 = 134；**72.3% 的 user-days ≥ 20 条**（90.5% ≥ 10） |

**数据迫使设计做的调整**：每段最长只有 10 天，原设计的"rolling 7-day entropy + 未来 7 天 horizon"放不进任何一段。因此改为：**rolling window W = 3 天（不跨段），horizon H = 3 天（必须在同一段内）**。baseline = day 0–6（即绝大多数用户的"前 7 个活跃日"；6,728/7,176 的用户从 day 0 开始活跃）。

## 2. 精确定义

**Unit = user-day (u, t)**。当天的 exposures 按 timestamp 排序。

Screen-visible signals（只用当天前 N = 20 条；不足 20 条的 user-day 不进入评估）：
- **D20**：前 20 条中不同的已知类别数。
- **S20**：前 20 条中出现最多的类别的份额（top-category share）。
- **A20**：重复作者率 = 1 − (#distinct authors / #items)。
- **NOV20**：前 20 条中，类别不在该用户"前 7 个活跃日"全部 exposures 里出现过的比例（用户第一个活跃日记为 NaN）。
- 个人化和趋势版本：rD20 = D20 − 用户 baseline 期 D20 均值；rS20 同理；dD20 / dS20 = 今天的值 − 前两天的均值（同段内）。

Platform-side signals（用当天及近几天的全部 exposures）：
- **H_day**：当天全部 exposures 的 normalised category entropy。
- **R3（RW）**：t−2..t 三天合并后的 normalised entropy（要求在同一段内，且已知类别 exposures ≥ 30）。
- relRW = R3 / B；dH_day 为趋势项。
- Entropy 统一定义为 Shannon entropy 加 **Miller–Madow 小样本校正**（+(m−1)/2n），再除以 ln 38，避免"看得少 → entropy 被机械性低估"。

Baseline：B_u = day 0–6 所有已知类别 exposures 合并后的 entropy。要求 ≥ 4 个活跃日且 ≥ 100 条；5,830 个用户满足。

Outcome：
- **Cocoon state** ev_X(u,t) = [R3(u,t) ≤ (1 − X)·B_u]，X ∈ {15%, 25%}。
- **Label** y_X(u,t) = t+1..t+H（H = 3）中任一天处于 cocoon state。要求这 3 天都在同一段、且 R3 都有定义（避免 censoring）。
- **At-risk 样本**：post-baseline（段 B、C），当天 R3 有定义且**当前不在 cocoon state**，并且当天 n ≥ 20。可预测的日子为 day 29–33 和 55–59。
- **Continuous outcome**：ΔR = R3(t+3) − R3(t)（不重叠的下一个窗口）。

**噪声 null（parametric bootstrap）**：假设用户真实偏好 = 其 baseline 类别分布，从中按真实的 baseline 条数和窗口条数各重抽一次 multinomial，重新计算 "event"。这给出"完全没有收窄时，仅靠抽样误差也会出现的 event 率"。

评估：按**用户**随机切成 70/30 train/test（seed 42），避免同一用户同时出现在 train 和 test。单信号规则的方向和阈值（在 train 上最大化 F1）都只在 train 上确定；logistic regression 先 StandardScaler。AUC 的 95% CI 通过对 test 用户做 cluster bootstrap（300 次）得到。

## 3. 描述性事实

| 指标 | 数值 |
|---|---|
| Screen 信号（n ≥ 20 的 user-days） | D20 均值 11.5（中位数 12）；S20 均值 0.27；**A20 中位数 0、均值 0.016；NOV20 中位数 0、均值 0.035**。后两者几乎恒为 0，信息量很低 |
| Baseline entropy B | 均值 0.80（sd 0.046，范围 0.50–0.89） |
| 人群平均 R3 的走势 | 段 A 约 0.78 → 段 B 约 0.82 → 段 C 约 0.80：**整体没有随时间收窄，反而略微变宽** |
| Cocoon-state 占 post-baseline user-days 的比例 | X=15%：**2.04%**（噪声 null 1.07%）；X=25%：**0.35%**（null 0.08%） |
| 至少有 1 天处于 cocoon state 的用户 | X=15%：16.8%；X=25%：3.6% |
| 首次事件出现的时间 | X=15%：中位数在 day 58（约 baseline 后第 8 周），70% 首次出现在段 C；**44% 的事件 user-days 落在 day 58–60**。这是一次全平台波动（那几天人群平均 R3 降到 0.776），不完全是个人层面的 cocoon |
| 持续性 | P(t+1 仍在 cocoon ∣ t 在 cocoon) = 0.42（X=15%）/ 0.33（X=25%）：多数"进入"只持续 1 天 |
| 是否集中在 heavy users？ | **相反**。按 baseline 日均 exposures 分四组，出现过事件的比例：Q1 最轻（21.6 条/天）为 29.6%，Q2 14.7%，Q3 11.3%，Q4 最重（63.7 条/天）11.7%。Q4 只贡献 15% 的事件 user-days |
| 更严格窗口（≥ 90 条/3 天，`kuairec_mw90`） | 事件比例 0.31% vs null 0.13%（X=15%）；至少有过事件的用户 2.6%（X=15%）/ 0.26%（X=25%，仅 14 人） |
| 整段合并（每段约 10 天、几百条，几乎没有噪声） | 段 C 相对 baseline：entropy 变化中位数 **+2.5%**；下降 ≥10%：1.08%（null 0.33%）；下降 ≥15%：0.26%（null 0.02%）；**上升 ≥10%：7.9%** |

解读：在 KuaiRec（2020 年快手、限定在 10,728 个视频的子池）里，**按"自身 baseline 下降 ≥15%"定义的持续性 cocoon 很罕见**。短窗口事件里约一半是抽样噪声，剩下的相当一部分是全平台的共同波动。真实的个人收窄存在（整段下降 ≥10% 的比例是 null 的 3 倍，≥15% 的比例是 null 的 10 倍以上），但只占约 1% 的用户。

## 4. Early-warning 结果（主设定：N=20, W=3, H=3, min_win=30）

**X = 15%**：43,897 个 at-risk user-days，5,555 个用户，base rate 2.28%，test 中有 291 个正例。

| 模型 | 类型 | Test AUC | AP (PR-AUC) | Precision | Recall | Alarm rate |
|---|---|---|---|---|---|---|
| S20 ≥ 0.50（单一规则，最佳 screen 信号） | screen | **0.733** | 0.065 | 0.103 | 0.192 | 4.2% |
| rS20（相对个人 baseline） | screen | 0.680 | 0.053 | 0.078 | 0.137 | 3.9% |
| D20（低 = 报警） | screen | 0.643 | 0.046 | 0.068 | 0.137 | 4.5% |
| rD20 | screen | 0.611 | 0.041 | 0.067 | 0.120 | 4.0% |
| A20 | screen | 0.570 | 0.036 | 0.056 | 0.124 | 4.9% |
| dS20 / dD20（3 天趋势） | screen | 0.561 / 0.536 | — | — | — | — |
| NOV20 | screen | 0.536 | 0.026 | 0.047 | 0.076 | 3.6% |
| **LR screen**（8 个 screen 特征） | screen | **0.776** [0.744, 0.805] | 0.090 | 0.121 | 0.237 | 4.4% |
| H_day（今天全量 entropy，单一规则） | platform | 0.824 | 0.163 | 0.184 | 0.306 | 3.7% |
| R3 | platform | 0.800 | 0.131 | 0.163 | 0.405 | 5.5% |
| **LR platform** | platform | **0.854** [0.829, 0.875] | 0.203 | 0.243 | 0.344 | 3.2% |
| LR screen + platform | both | 0.863 | 0.213 | 0.243 | 0.375 | 3.4% |
| *Activity only（log n）* | reference | *0.830* | 0.082 | 0.101 | 0.326 | 7.2% |
| LR screen + log n | screen | 0.868 | 0.165 | 0.187 | 0.323 | 3.8% |
| LR platform + log n | platform | 0.876 | 0.209 | 0.225 | 0.361 | 3.6% |

- **Information gap**：LR 层面 0.854 − 0.776 = **0.078**（bootstrap 95% CI 0.056–0.105）；最佳单一规则层面 0.824 − 0.733 = 0.091。在 AP 上差距更明显：0.203 对 0.090，platform 约为 screen 的 2.3 倍。
- **Activity 混杂**：log n 单独就有 0.83，因为轻度使用日的 entropy 噪声大，更容易"掉线"。只看 n ≥ 50 的 user-days 时，LR screen 0.70，LR platform 0.76，差距仍约 0.05。
- **X = 25%**（test 中只有 56 个正例）：S20 规则 0.795，LR screen 0.842 [0.77, 0.90]，LR platform 0.891 [0.83, 0.94]，gap 0.048 [0.016, 0.081]。
- **Continuous outcome ΔR**（test 集 Spearman）：S20 +0.13，D20 −0.13，rS20 +0.16；R3 −0.44（主要是 regression to the mean）。Linear model 的 R²：screen 0.066，platform 0.21。
- **严格窗口版本（mw90）**：screen 与 platform 的 AUC 都接近 0.90（gap 0.006，CI 跨 0），但 test 正例只有 35 个，**不稳定，不作为主结论**。
- 在 LR screen 中权重最大的是 S20（标准化系数 +1.14），其次是 rD20 和 dS20。A20 和 NOV20 基本没有贡献。

**Lead time 和 false alarm**（X=15%，test 用户中共 248 个"首次事件"，即段内首次事件、且之前至少有 1 个可观测日）：

| 规则 | 事件前报警的比例（detected） | Lead time 中位数（均值） | 无事件的 user-segment 中报警过的比例 | 报警 user-day 占比 |
|---|---|---|---|---|
| S20 ≥ 0.50 | 27% | 2 天（2.6） | 19% | 2.7% |
| LR screen | 28% | 2 天（2.4） | 14.5% | 2.8% |
| LR platform | 39% | 2 天（1.8） | 10.4% | 2.4% |

也就是说，最佳的简单 screen 规则只能提前约 2 天（最长 7 天）捕获约 1/4 的事件；它的报警中只有约 10% 在 3 天内真的出现事件，也就是 alarm-level 的误报约 90%。见图 fig2。

**"现在就能看出来"（nowcasting）**：同一天内 D20 与 H_day 的 Spearman 相关为 0.47，S20 为 −0.47（n ≥ 20）。n 越大，相关性越弱（n ≥ 100 时为 0.33），因为前 20 条只占当天很小的一部分。

## 5. KuaiRand-Pure 复现（is_rand == 0，类别用第一个 tag，43 个 tag）

- **User-day 设计不可行**：standard log 每个 user-day 中位数只有 2 条，P90 为 9 条，**只有 3.0% 的 user-days ≥ 20 条**。4/11 之后日志量急剧下降（Pure 版本是抽样后的子集）。所以只做了两个静态检查。
- Screen 信号与全量 entropy 的一致性（04-08..04-21，≥ 60 条的 6,232 个用户，用"首 20 条"对比"全部"）：D20 与全量 entropy 的 Spearman 为 **0.61**，S20 为 **−0.58**，与 KuaiRec 方向一致且更强。
- 收窄检查（week 0 对比之后，两边都 ≥ 50 条的 1,040 个用户）：entropy 变化中位数 +3.9%；下降 ≥15% 的比例 3.4%，**低于**噪声 null 的 4.1%。即**没有超出噪声的收窄证据**，与 KuaiRec 一致。

## 6. 什么行得通、什么行不通，以及对最终设计的建议

行得通：
- N = 20 在 KuaiRec 里 72% 的 user-days 可以达到。
- S20 是最好、最容易向用户解释的单一信号："今天前 20 条里是否有 ≥ 10 条来自同一类？"
- User-level split、cluster bootstrap CI 和 lead-time 计算整套流程都能跑通。

行不通或需要修改：
- A20、NOV20 在 N = 20 时几乎恒为 0（KuaiRec 的作者很分散；7 天记忆几乎覆盖所有类别）。**建议删掉，或把 NOV 的记忆窗口缩短到 1 天**。
- 3 天趋势特征（dD20、dS20）几乎没有用。
- 用 X = 15% 的短窗口事件做 outcome 时，噪声占比约 50%，而且受全平台波动和 activity 混杂影响。X = 25% 时事件太少。

**建议的最终设计**：
1. **Outcome**：相对个人 baseline 的下降，窗口 ≥ 90 条（或 3 天且 ≥ 30 条/天），并且**同时满足**两个条件：(a) 下降 ≥ X（X = 10–15%）；(b) 超过该用户 parametric-bootstrap null 的 95% 分位。此外，**减去当天的人群平均变化**（相当于 day fixed effect），以去除像 day 58–60 那样的全平台波动。同时报告 continuous ΔR。
2. **Screen signals**：S20、D20，以及它们相对个人 baseline 的版本；N = 20 为主，N = 10 和 N = 40 做敏感性分析。
3. **Metrics**：AUC 与 **PR-AUC**（事件罕见时比 AUC 更有信息量），都附 user-cluster bootstrap CI；precision/recall 在固定 alarm rate（比如 5%）下报告；lead time、detected share、每个 user-segment 的 false-alarm 率；**必须同时报告 activity-only baseline 和噪声 null 的 event 率**；information gap = platform − screen，并在 n ≥ 50 的子集上复核。
4. 由于真实日志里"真正的 cocoon"很少，**建议 detection 的主实验放到基于 X 开源算法的 simulator 上**（在那里可以控制收窄的发生），KuaiRec 用来：(i) 校准 simulator 里的 S20 / D20 分布和日常 entropy 噪声；(ii) 作为"真实世界里信号 ↔ 状态一致性"的外部验证（D20 与 H_day 相关 0.47）。

## 7. 局限

- **Exposure ≠ impression**：big_matrix 记录的是"播放（至少开始）"，不是 feed 实际展示的内容；划走没播放的条目看不到。并且只覆盖 10,728 个视频的子池，所以"前 20 条"不等于用户屏幕上真正的前 20 条。
- 2020 年的快手，不是 X/Twitter；推荐算法、类别体系（38 个一级类）和内容形态都不一样。结论只能说明"方法可行、量级参考"。
- 数据只有 28 天，分成 3 段，不支持 7 天窗口和 7 天 horizon；两段之间 16–19 天的空档里发生了什么完全未知。NOV20 的"前 7 个活跃日"会跨越空档。
- Baseline 本身可能已经处于 cocoon 状态（数据开始前用户已经使用平台很久），所以"相对 baseline 的下降"只能衡量**进一步**收窄。
- 事件样本少（X=25% 在 test 中只有 56 个正例；mw90 只有 35 个或 9 个），CI 较宽。Train/test 只切了一次（CI 覆盖的是 test 抽样误差，没有覆盖切分方式带来的误差）。
- Entropy 基于单层类别，同一类内部的收窄（比如只看某个明星）看不到。A20 可以部分补充这一点，但在这里几乎为 0。
- KuaiRand-Pure 是抽样日志，太稀疏，只能做静态复核。

## 图

- `fig1_auc_comparison.png`：screen 与 platform 的 AUC 对比（X = 15% 和 25%，LR 带 95% CI）。
- `fig2_lead_time.png`：首次报警到事件的 lead time 分布，附 detected share 和 false-alarm 率。
- `fig3_events_by_day_and_example.png`：左图为每天处于 cocoon state 的用户比例与噪声 null（可以看到 day 58–60 的全平台波动）；右图为一个 test 用户的时间线，S20 在第 58 天报警，第 59 天 R3 跌破阈值。
