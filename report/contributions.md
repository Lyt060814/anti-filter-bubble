# 成员贡献记录

最终报告的贡献表要列出**全部五位成员**和他们具体完成的工作，共同完成的工作可以写在多人名下。每人完成一项实质性工作后，在自己名下追加一行：日期、做了什么、产出在哪里。

## Fu Yitong
- 10 月：与 Wang Junbo、Li Yitong 一起细化研究问题；设计标注模板（议题、命题、立场、理由、来源字段）并定稿标注规范；整理参考理由语料（15 条理由、8 个来源）；搭建组内仓库与五种干预策略的规则仿真；与 Zhao Dingcheng 调研用户控制相关研究。（来源：11-04 进度记录）

## Wang Junbo
- 10 月：与 Fu Yitong、Li Yitong 细化研究问题并撰写项目计划相关部分；与 Zhao Dingcheng 搭建初版曝光报告流程，负责端到端连接与报告生成；与 Fu Yitong 设计标注模板并编写一致性检查代码；标注真实视频样本。（来源：11-04 进度记录）

## Xu Ruicong
- 2026-11-07：按 #6 合并审阅将 v2 DeepSeek 1.0% 设为察觉主参照，加入 Qwen 对照 DeepSeek 的实测查全率 .8、误报率 62/495 情境并重画，明确非金标准及小阳性样本局限。
- 2026-11-07：按审阅将 R4 独立为干净分支，加入 DeepSeek v0 1.4% 与 v1 0.6% 参照对照，保存 2,440 组解析结果，删除无关模拟元数据。
- 2026-11-07：按第二轮审阅将 R2 属性坐标供给中心化，重跑 190,320 个快照，保存中性用户及偏好/系数单调性 264 项诊断；未将微弱效应写成显著结论。
- 2026-11-07：使用 Codex 助手按 Li Yitong 的 R2 审阅重做有界模型，扫描 2%/10%/50% 供给，明确改用供给参照，保存 190,320 个快照与更清晰的图。
- 2026-11-07：使用 Codex 研究助手完成 R1 透明模型与两项数值自检，保留逐种子验证结果（analysis/v6_simulation/）。
- 10 月：准备 ShortVideo、KuaiRand 数据；从 KuaiRand Pure 构建 30 名用户、1,936 条交互的样本轨迹，检查字段完整性、去重与时长异常。（来源：11-04 进度记录）

## Zhao Dingcheng
- 10 月：与 Wang Junbo 搭建初版曝光报告流程，负责候选视频检索和 LLM/VLM 抽取（命题、立场、理由、来源）的提示词与输出格式；与 Fu Yitong 调研相关研究；与 Xu Ruicong 用生成数据测试流程。（来源：11-04 进度记录）
- 11-07：D1 写四类对立叙事（唯一正确、二元对立、焦虑渲染、群体标签）的定义、判断步骤和正反例，重点划清群体标签与单个反派的边界；D2 据此写 v1 标注提示词和解析函数，供双模型核查和全量标注使用。产出：`analysis/v6_annotation/narrative_types.md`、`prompt.md`、`prompt_v1.py`。
- 11-07：D3 写双模型核查分析脚本（混淆矩阵、查准率与查全率、kappa、校正比例、分歧归类、版本对比），分析 v0 结果：Qwen 的群体标签查准率 10%、查全率 29%、kappa 0.13，误报主要是把家庭角色和单个人物当成群体。产出：`analysis/v6_annotation/agreement.py`、`agreement.md`、`results/agreement_v0*`。
- 11-07：D5 撰写报告第 2 节相关研究（英文，四条研究线与研究空白），新增文献（Haroon 2023、Pecher 2026、Vombatkere 2024、Kalimeris 2021、Dean 2020、Zhang 2024、Sukiennik 2025、Yang 2026、Nguyen 2014）逐条用 Crossref 或 arXiv 核实。产出：`report/sections/2_related_work.md`。
- 11-07：D4 编写分类表脚本（按关键词把 LLM 自由填写的议题名归并为子议题、Wilson 区间），撰写报告第 4.2 节（分类表、读法、典型争论、排除理由）和 4.3 节（标注质量，v0 数字）。产出：`analysis/v6_annotation/taxonomy.py`、`results/taxonomy_qwen_v0*`、`report/sections/4_data_taxonomy.md`。
- 11-07：按 issue #10 分析 v1 提示词的反常结果（Qwen 阳性 4.0%→51%、DeepSeek 1.4%→0.6%，原因分别是前缀套话和规则过严），写 v2 提示词（四问分字段、一致性检查、对象默认个人、放宽推广与认同、按恶行定义的人不算性别群体），同步 D1 定义；给 `agreement.py` 加上分层抽样（关键词层 + 随机层）的曝光加权估计。产出：`agreement.md` 第 5 节、`results/agreement_v1*`、`prompt_v2.py`、`narrative_types.md`。
- 11-07：撰写附录 A（英文）：共同规则、四类叙事的定义与正反例、性别群体标签的四步判断、提示词 v0→v1→v2 的变化与结果、v2 提示词原文；把"渣男/渣女"的处理写进 D1 定义。产出：`report/sections/11_appendix_a.md`。
- 11-07：按 issue #13 用 DeepSeek 重标结果重做表 4.1（`taxonomy.py` 增加缺失处理、Qwen 对照列、小样本不拆子议题），改写第 4.2 节（区间为主、Qwen 两步高估的对照、案例选择与排除理由），附录加入 A.6 跨大类提示词原文并改准 A.4 末句。产出：`results/taxonomy_deepseek_bu*`、`report/sections/4_data_taxonomy.md`、`11_appendix_a.md`。

## Li Yitong
- 10 月：前期文献与数据核查；撰写项目计划的技术部分；与 Xu Ruicong 搭建五种策略的推荐仿真。
- 11-04 至 11-07：按老师反馈重新设计研究问题（v4–v6）；推导观点偏斜的定义与命题；在快手 RecIF 数据和 OneRec 模型上完成可行性实验（议题曝光结构、LLM 标注试点、OneRec 话题与观点层面的操纵检验、"不感兴趣"反向、embedding 属性对比、各议题数据量）；自下而上抽样 3,000 条视频的议题与叙事标注；制定三人分工与任务说明。
