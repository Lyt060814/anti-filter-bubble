# Xu Ruicong 的任务（v6）

你负责案例研究的模拟和察觉计算：RQ2、RQ3 的主要图表，以及报告第 5 节的模拟部分。先读 [Research Plan v6](../project-plan/research_plan_v6.md)、[v5 第 4 节（定义与命题）](../project-plan/research_plan_v5.md) 和 [协作说明](README.md)。工作目录：`analysis/v6_simulation/`。只需要普通电脑上的 Python（numpy、matplotlib），不需要数据和 GPU。

## 模型说明（透明推荐模型，即 v5 命题 2 的模型）

**视频**：议题内 A 类（群体标签叙事）和 B 类（议题内其他视频），加上议题外视频。每条视频是一个 $d$ 维向量：

$$v_i = t\cdot e_{\text{议题}}\,\mathbb 1[i\in I_k] + c\cdot e_{\text{属性}}\,(\mathbb 1[i\in A]-\mathbb 1[i\in B]) + \varepsilon_i ,$$

- $t$ 控制话题对比，$c$ 控制属性对比，$\varepsilon_i$ 是随机噪声；
- 议题外视频可以分成几个其他话题。

**推荐**：$\pi_u(i)\propto \exp(\langle u, v_i\rangle/\tau)$，每步按 $\pi_u$ 抽一条给用户。

**用户**：看到视频 $i$ 后，以概率 $\sigma(a+\gamma\,\mathbb 1[i\in I_k]+\theta\,\mathbb 1[i\in A])$ 看完。$\theta>0$ 表示他偏好 A 类叙事。

**更新**：看完则 $u\leftarrow u+\eta\, v_i$。可加遗忘：$u\leftarrow (1-\lambda)u+\dots$，或只保留最近 $W$ 次互动。

**指标**：
- 每一步精确计算 $m=\pi(I_k)$ 和 $p=\pi(A)/\pi(A\cup B)$，不靠抽样；
- $V=\operatorname{logit}p-\operatorname{logit}\bar p$，其中 $\bar p$ 是全体模拟用户的平均曝光算出的平台平均。

**参数**：都是情境假设，要扫描。属性对比和话题对比之比 $c/t$ 用我们在 Qwen3-Embedding 里测得的数作中心：群体标签约 0.15，冲突叙事约 0.59（[v5 可行性记录 3.4 节](../context-recovery/plan_v5_feasibility.md)），扫描 0 到 1。$\theta$ 取 0、0.5、1、2。每个设定跑 20 个随机种子，报告均值和 95% 区间。

## R1 框架（11-09）

写 `analysis/v6_simulation/model.py`（或 notebook），实现上面的模型，并做两项自检：

1. $c=0$ 时，无论 $\theta$ 多大，$V$ 都不增长（命题 2 的"对偶"）；
2. 一步更新后，$V$ 的变化和命题 2 的一阶公式 $\Delta V\approx\frac{\eta}{\tau}[\bar s_j(A)-\bar s_j(B)]$ 相符。

## R2 形成（11-11）

从中性用户出发，跑 $T$ 步自然行为，画出 $(m_t, V_t)$ 轨迹：

- 横轴兴趣、纵轴偏斜，不同 $\theta$ 和 $c/t$ 分别画；
- 结论要回答：观点偏斜是否比议题占比长得慢？由什么决定？

## R3 逃离（11-11）

从 R2 中 $\theta$ 较大用户的终点出发，执行策略一段时间，再恢复自然行为。策略包括：

| 编号 | 策略 | 实现 |
|---|---|---|
| S0 | 什么都不做 | 继续自然行为 |
| S1a | "不感兴趣"（负向更新） | 看到 A 时 $u\leftarrow u-\eta_{\text{NI}} v_i$ |
| S1b | "不感兴趣"（OneRec 式反向） | 看到 A 时 $u\leftarrow u+0.5\,\eta\, v_i$。OneRec 实测：放进"不感兴趣"栏的内容，效果约为中性提及的 78%，方向为正 |
| S2 | 快速划过 A | 看到 A 时不看完 |
| S3 | 多看 B | 看到 B 时一定看完 |
| S4 | 主动搜索 B | 每若干步额外看一条 B |
| S5 | 删除历史中的 A | 撤销过去 A 的更新 |
| S6 | 关键词 / LLM 过滤 | 按查全率和误报率从推荐中删去被判为 A 的视频；查全率、误报率之后用 Zhao Dingcheng 核查得到的数 |
| S7 | 关闭议题 | 删去全部议题视频 |
| S8 | 关闭个性化 | 用平台平均 $\bar u$ 推荐 |
| S9 | 重置 | $u$ 回到初始值 |

指标：$\Delta V$、$\Delta\log m$、B 类的保留比例、操作次数（努力），以及停止后 $\Delta V$ 回到一半所需的步数（持续时间）。

图：
- 策略平面图：横轴 $\Delta\log m$，纵轴 $\Delta V$。理想位置是 $\Delta V$ 明显为负、同时 $\Delta\log m$ 接近 0（降低偏斜而不丢议题），图上标出这个方向；
- 持续性曲线。

结论要回答：哪种策略在不丢议题的前提下最有效？S1a 和 S1b 差多少？

## R4 察觉（11-11）

按 v5 命题 4 实现样本量公式，画出所需同议题视频数随偏斜大小（2–8 倍）的变化：

- 参照占比 $p_0$ 取 1.8%（群体标签）和 41%（冲突叙事）；
- 分类器查全率和误报率先取 0.8、0.02，之后换成 D3 的实测值；
- 再按真实议题曝光率换算成总曝光次数：RecIF 中每人议题占比中位数 1.6%，p90 为 3.6%。

可选：在 R2 的模拟轨迹上做序贯检验，看偏斜出现多少步后能被发现。

## R5 报告小节（11-12）

写 `report/sections/5_simulation.md`：模型一段、参数表（注明哪些是情境假设、哪些来自实测）、四张图、每张图配一段结论。图存到 `analysis/v6_simulation/figures/`。
