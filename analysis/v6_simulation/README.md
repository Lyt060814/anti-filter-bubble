# 透明推荐模型模拟

## R3：按组员要求校准后的版本

Python >=3.10，numpy、matplotlib。运行：

```powershell
python analysis/v6_simulation/calibrated_run.py
python analysis/v6_simulation/ni_calibration.py
python analysis/v6_simulation/package_results.py
python analysis/v6_simulation/calibrated_audit.py
python analysis/v6_simulation/report_numbers.py
```

仅重画：`python analysis/v6_simulation/calibrated_replot.py`。
完整设计、单位约定、坐标截断的假设、校准目标与 ±50% 单因素扫描见 `r3_calibrated_pr.md`。
校准不是独立验证；原 R2 是 1,200 步、有界范数的审阅版本，本 R3 以 6,000 步和坐标截断做单独的试点匹配情境，不能混用。
每个 CSV 保留各设定/各种子的结果；形成每100步存，逃离全设定保留端点，指定主情境另存每100步轨迹。
持续时间区分无初始改善、已观察到回弹、右删失；总偏斜使用供给参照。

### 公开包与完整本地数据

按审阅保留所有种子的端点和完整汇总，稠密原始形成轨迹只保留主图五组情境，逃离只保留主图两组情境（间隔100步）。
大文件以确定性 gzip level 9 存成 `.csv.gz`，标准库 `gzip.open(path,'rt')` 或 pandas 可直接读。
`packaging_manifest.json` 与各图 meta 记录保存策略、压缩方式、行数、大小、文件哈希和完整源哈希。
整个 analysis/v6_simulation 当前约52 MB。R2 已批准的完整形成 CSV 也仅作无损 gzip 压缩，未删任何行。
完整未压缩本地数据在仓库外的同级 `simulation_full_runs/calibrated_v1/`，不会提交；不同校准版本应使用新的本地归档目录。
重新执行 calibrated_run.py 会产生完整 CSV；执行 package_results.py 再生成公开小包。脚本不会以新结果覆盖不同内容的旧完整归档。

## R2 审阅修订

当前 R2 使用 `python analysis/v6_simulation/bounded_formation.py`。
按 #4 review：u 范数上限 0.75，初始议题曝光先验 4%，供给扫 2%/10%/50%，主图 2%。
参照改为供给，输出 `V_supply` 是总偏斜，不是相对平台的个人偏斜。
六个同质向量组精确聚合 A/B 和四个议题外方向，噪声取零；均为情境假设。
二轮审阅后属性按供给中心化：A=c(1-s)、B=-cs；264 项诊断全部通过，单调性是非递减，允许有限样本中的并列，不声称差异显著。
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
