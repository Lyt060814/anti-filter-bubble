# COMP1110 Group Project：要求速览（团队内部参考）

> 来源：*Guidelines for Group Project* 与 *Guidelines for Project Plan (updated 2026-09-21)*。本文件是中文整理，以原文为准。

## 1. 这是一个什么样的项目

- 5 人一组，约两个月。**是"思考 + 写作"项目，不是软件项目**：代码/原型可选且**不计分**，但必须有真正的 computing / data science 技术内核。
- 需要：一个**原创的具体问题** → 文献调研 + 找到 **research gap** → 提出 computing/data science 方法（数据分析、模型、算法或系统设计）→ 清楚地写出来。
- **Topic = 一个问题/情境，不是工具，也不是宽泛领域。** 官方原文明确举例 *"social media" is too broad*。
  → 所以 **"信息茧房" 本身只是领域，不是 topic**，我们必须把它收窄成一个具体、本地、少有人研究的问题。

## 2. 创意（Creativity）怎么评

- 主要看**题目的原创性**，而不是解法的复杂度；解法可以相对标准（采集数据、简单建模、可视化）。
- 奖励：来自**具体、本地、小众**情境；把日常生活和计算以**意想不到**的方式连起来；明显来自人的好奇心。
- 必须用**充分的文献调研**证明：这个问题**没有被深入研究过**，或基于**最近约两个月内**的新事件/新成果。
- 警告：像 "Top 10 Data Science Projects for Beginners" 的题目 → 不够创意；多组撞题 = 强烈信号不够创意。
- 仅仅"对我们来说是新的"、"听起来很特别"、"离计算很远"都**不算**创意。

## 3. 技术深度

- 纯伦理/社会/哲学讨论**不合格**；要有非平凡的技术深度，且工作量足够 5 个人持续忙碌。
- 检验标准：每个成员都能指出自己在调研/设计/分析/写作/展示中**实打实的一份工作**。
- 五种项目类型及期望深度（详见原文）：
  1. **Development**：问题规格、系统设计（界面、用户流程、核心功能）、线框图/架构图/功能优先级。
  2. **Data analysis**：数据是什么、从哪来、如何获取、为何相关；描述统计、可视化、简单建模（聚类/回归/规则分类），可以用 toy data。
  3. **Algorithmic**：输入/输出/约束/成功标准；算法思路；复杂度讨论；小规模实例结果。
  4. **Simulation / Modelling**：被建模的系统；变量、状态、规则；时间步/事件；输出指标；示例运行与解读。
  5. **Hybrid**：说明各部分属于哪类；至少一部分达到上述深度；**宁可一两方面适度深入，不要多方面都浅**。

## 4. 交付物与权重

| 交付物 | 权重 | 形式 | 截止（暂定，以 Moodle 为准） |
|---|---|---|---|
| Project Plan | 20% | 小组 | **Oct 4** |
| Interim Progress Meeting（与 TA 约 5 分钟） | 3% | 小组 | Oct 20–24 |
| Interim Progress Log（半页） | 2% | 个人 | Nov 4 |
| Final Report | 45% | 小组 | Nov 15 |
| Individual Self-Reflection | 10% | 个人 | Nov 15 |
| Group Presentation（10 分钟，线下） | 20% | 小组 + 个人 | Nov 17/19/24/26 |

## 5. Project Plan 要求（4–6 页）

建议结构：
1. Title and team members
2. Problem statement and/or solution concept
3. Computing and/or data science connection
4. Literature / background review
5. Feasibility, limitations, and ethics
6. Timeline and team roles

没有单独的 "creativity" 章节：创意由 **问题陈述 + 文献综述** 共同判断。

### 各部分要点

- **Problem statement**：一个清晰的研究问题/方案概念；足够的背景；**明确 in-scope / out-of-scope**；让没参加讨论的同学能**一句话复述**问题。
- **Computing / DS connection**：点名每个概念/方法/工具，并说明**它具体做什么、如何帮助回答问题**（只列工具不够）；**写明项目类型**；表明后续能有真正的技术贡献。
- **Literature review**：约 **5–10 个来源**（论文、可靠文章、现有系统/产品、数据集、已有分析）；每个来源简短点评；写成**有综述性的概述**，不是链接列表；选材要**支撑创意主张和可行性**；如果没有完全相同的工作，就写相似问题/方法并说明我们的不同。
- **Feasibility / limitations / ethics**：需要什么数据、能否获得；下一步用什么方法；伦理（隐私、知情同意、涉及真人）；实际限制（数据访问、时间、技能）；**我们不会声称什么**。
- **Timeline & roles**：按日期或周的里程碑；**点名谁负责什么**。"大家平均分工" 不合格。

### 评分细则（Project Plan 内部权重）

| 标准 | 权重 | Excellent 的要求 |
|---|---|---|
| Creativity of topic | 25% | 明确的少有人研究或非常新的焦点，且文献让这个主张可信 |
| Connection to computing / DS | 25% | 概念被点名并与问题关联；写明项目类型；清晰指向后续技术深度 |
| Clarity of problem / solution | 25% | 问题具体；背景充分；范围清晰；外人能一句话复述 |
| Feasibility, limitations, ethics | 10% | 数据/方法/局限讲到位；伦理覆盖；对 5 个一年级学生可行 |
| Formatting & language | 10% | 标题、间距、字体、引用格式一致；参考文献可查；行文清楚 |
| Timeline & team roles | 5% | 按周/日期的里程碑；责任到人；现实可行 |

> 注意：若某项缺少必要内容（例如几乎没有文献支撑创意），该项会被**封顶在较低档**。

## 6. 其他

- Free rider：有问题尽早告诉教学团队；结束时有同伴互评表（不直接改分，只用于发现问题）。
- 可以用 AI 帮助头脑风暴，但注意撞题风险——最终题目要体现我们自己的观察与好奇心。
