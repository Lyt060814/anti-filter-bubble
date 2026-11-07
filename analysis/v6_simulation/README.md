# 透明推荐模型模拟

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

## 复现 R1–R5

```powershell
python analysis/v6_simulation/model.py
python analysis/v6_simulation/experiments.py formation
python analysis/v6_simulation/escape.py
python analysis/v6_simulation/ni_sensitivity.py
python analysis/v6_simulation/experiments.py detection
python analysis/v6_simulation/summarize.py
python analysis/v6_simulation/audit.py
```

仅重画：`python analysis/v6_simulation/replot.py`。依赖 numpy、matplotlib，版本见元数据。
默认四个议题外方向；形成另扫一个合并方向，暴露目录结构的敏感性。
扫描 c/t=0:0.1:1，加 0.15、0.59；theta=0/0.5/1/2；20 种子。
每个种子是独立四用户世界，平台参照由四人的平均曝光算出，用户分别对应四个 theta。
逐步精确计算概率，CSV 每 20 步保存（另存停止后第 1 步）。
形成 128,960 行；逃离 366,080 行；持续时间 11,440 行；NI 强度 21,840 行。
CI 是种子世界均值的点态 95% Monte Carlo 区间，不是样本分位区间，不代表实测参数不确定性。
summary.csv 保留每个设定的均值及区间；S7 的 V 不定义，log m 为负无穷，不参与平面图。
察觉为确定公式，不为它伪造 20 个种子或置信带。

干预时固定 R2 终点平台参照；S8 使用平均 u，不等于平均 pi。
S6 是按类精确概率削减后回填；分类器参数是假设，尚未获得 D3 核查数值。
S5、S9 是一次操作，S4 每十条自然曝光加一条 B，操作代价不等于人的时间。
停止之后恢复原偏好，不改变用户信念。两种回弹时间及右删失分别记录，不能将删失项当成 400 步。
0.78 响应比和 +0.78 eta 的更新强度不是同一量；NI 扫描仅是情境比较。

元数据保存生成时 git HEAD、工作区状态和脚本 SHA256；最终审计还验证图像 300 dpi、PNG/PDF 配对、源码与元数据。
报告小节只写模拟，不包含 Li Yitong 的 OneRec 实测段落。
运行截图是实际 audit.py stdout 在 Notepad 中的显示，未渲染假终端。

## 分支与 PR

R1–R5 使用累积分支，PR 均以 main 为目标，依次审阅/合并 R1→R2→R3→R4→R5，
前项合并后后项 diff 会缩小。未自动合并或推送 main。
`pr_bodies/` 保存每项决策和待审问题；登录 gh 后运行 `create_prs.ps1`，它会避免重复创建已开的 PR。
Git 可推送不等于 gh 已登录；不要将登录令牌放入仓库。
