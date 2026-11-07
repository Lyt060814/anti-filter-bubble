# 透明推荐模型模拟

## R2 审阅修订

当前 R2 使用 `python analysis/v6_simulation/bounded_formation.py`。
按 #4 review：u 范数上限 0.75，初始议题曝光先验 4%，供给扫 2%/10%/50%，主图 2%。
参照改为供给，输出 `V_supply` 是总偏斜，不是相对平台的个人偏斜。
六个同质向量组精确聚合 A/B 和四个议题外方向，噪声取零；均为情境假设。
完整说明与待审选择见 `r2_revision_pr.md`。旧 R3–R5 结果不应作为本模型的结果使用。

全部模拟参数为情境假设，不是线上平台估计。只需 Python、numpy、matplotlib。

运行 R1：`python analysis/v6_simulation/model.py`。

A/B 配对共享噪声；c=0 时属性对比严格为零。一般独立噪声不保证这一点。
生成系数 c/t 不等于命题 2 中曝光加权的 c_j/t_j；实测的 0.15/0.59
只标记参照位置，不代表校准完成。均衡供给和初始议题比例 20% 也是假设。
R1 一阶检验固定平台参照，关闭遗忘，仅测一次反馈；包含正负更新。
小二阶系数可能与三阶项抵消，因此同时检查误差下降和绝对 O(eta^2) 界。

实测来源：docs/context-recovery/plan_v5_feasibility.md 第 3.4 节（几何）；
docs/tasks/xu_ruicong.md 及 research_plan_v5.md 第 4、7 节（曝光率、叙事比例、OneRec）。
这些是仓库已报告结果，未在本机重新测量。模拟结论不能外推为线上平台效果或信念变化。
