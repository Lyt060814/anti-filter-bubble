# 两份 v1 plan 的来源复核台账

2026-10-02。对应 `working_plan_v1.md` 和 `execution_plan_v1.md`。这是原始材料阅读与实物检查记录，不是把搜索结果重新列一遍，也不是声称所有论文的附录都已逐页读完。以下区分：**正文**＝已读与主张有关的方法、结果或讨论；**局部**＝只取得摘要、页面或部分正文；**实物**＝已检查下载的数据或源码。全文取不到的明确保留缺口。

本机资料根目录：`/home/yitongli/Courses/26full/COMP1110/anti-filter-bubble-sources/`。`papers/` 存 PDF 和提取文本，`code/` 存固定版本克隆，`data/` 存数据，`web/` 存网页。大型文件不加入本仓库。版本和文件校验见 `resource_manifest.json`；文件下载成功不等于研究结论已经复现。

解释和下一步建议见 [第一性原理复核](../project-plan/first_principles_review.md)。之前的 [source_audit.md](source_audit.md) 保留第一次接手时的发现；本页与实物检查记录更新了其中的访问状态。

## 1. 课程和问题价值

| 来源 / 阅读状态 | 原文给出的依据 | 对本项目的限制或更正 |
|---|---|---|
| 用户上传 COMP1110 Project Plan / Group Project Guidelines，正文 | Plan 4–6 页，约 5–10 个精选来源；问题、创造性、computing 联系各占 25%；不要求完整生产系统 | 不应把大量下载、训练模型或系统规模当作创造性。Hybrid 至少一个部分有实质深度；日期表注明 Moodle 为准 |
| [Nguyen, Echo Chambers and Epistemic Bubbles](https://philarchive.org/rec/NGUECA)，作者稿正文，`nguyen` | 声音缺席与对外部来源不信任是不同结构；重复接触不等于独立证据 | 不是“主题茧房 vs 观点茧房”的原始出处；补充反方信息未必能打破不信任结构 |
| [Leysen et al., 2022](https://doi.org/10.1145/3511047.3538028)，正文，`leysen` | 将技术茧房操作化为推荐多样性随时间下降，明确 structural / topic / viewpoint 三维及多方参与者 | 文献早已区别主题与观点；该定义仍不自动包含伤害或用户不认可，不能当唯一正确概念 |
| [Reuters Institute, 2022 review](https://reutersinstitute.politics.ox.ac.uk/echo-chambers-filter-bubbles-and-polarisation-literature-review)，网页正文，`web/page-20` | 回顾回音室、过滤气泡、极化证据与测量差异 | 不可缩写为“只测内容、不测观点，所以对我们无关” |
| [Hartmann et al., 2025](https://doi.org/10.1007/s42001-025-00381-z)，正文，`hartmann2025` | 129 项研究，比较概念、方法、尺度与结论 | 2024 预印本为 112 项；最终版并不是“普遍否定茧房”。证据异质性是设计测量的理由 |
| [Kleinberg et al., 2024](https://arxiv.org/abs/2202.11776)，正文，`kleinberg` | 模型、调查和设计分析说明 engagement 不能唯一识别 welfare | 不证明任一具体平台存在故意操纵，也不直接测立场改变 |
| [Bursztyn et al., Social Media and Collective Welfare](https://www.econstor.eu/bitstream/10419/283302/1/1866380753.pdf)，工作论文相关正文，`bursztyn` | 使用决策的外部选项与网络外部性，会使继续使用和偏好“平台不存在”同时发生 | 使用的效用与平台整体存在的福利不是同一问题；不能当作短视频成瘾或观点操纵的直接估计 |
| [Chaney et al., 2018](https://arxiv.org/abs/1710.11214)，正文，`chaney` | 模拟推荐反馈如何造成消费同质化及混杂 | 模型中固定潜在偏好；消费同质化不是实测的人类信念改变 |
| [Piao et al., 2023](https://doi.org/10.1038/s42256-023-00731-4)，局部；[作者代码](https://github.com/tsinghua-fib-lab/Adaptive-Information-Dynamic-Model)实物 | 已读公开模型、用户反馈规则、数据字段，含经验聚合数据和模拟 | 出版社正文未取得；不能称全文已读。模拟参数 α 混合模型得分与内在兴趣，不是从自然实验识别的操纵效应 |
| [Törnberg, 2026](https://doi.org/10.1371/journal.pone.0347207)，正文，`tornberg` | 群体退出/重组的简约模型展示“适量个性化”也可能维持混合群体 | Reddit 案例是启发性比较；不是对短视频实际政策的因果验证 |

## 2. 曝光、态度和社会认知：不能互相替代

| 来源 / 阅读状态 | 研究设计、结果 | 本项目应如何使用 |
|---|---|---|
| [Nyhan et al., Nature 2023](https://doi.org/10.1038/s41586-023-06297-w)，正文，`nyhan` | Facebook 23,377 人，约三个月减少同立场来源曝光；预定态度指标未检出变化 | 直接涉及政治态度，不能归为“只研究内容类目”的反方；曝光改变不是态度改变的充分条件 |
| [Guess et al., Science 2023](https://doi.org/10.1126/science.abp9364)，局部，[作者摘要页](https://andyguess.com/publication/doi-10-1126-science-abp-9364/) | 时间流改变使用及内容曝光，但研究期内关键态度指标无显著变化 | 出版社 PDF 访问受阻，不能声称读完方法附录；已有 [2024](https://pubmed.ncbi.nlm.nih.gov/39637002/) 与 [2026](https://pubmed.ncbi.nlm.nih.gov/41855352/) 更正记录，细节主张须结合更正后版本 |
| [Gauthier et al., Nature 2026](https://doi.org/10.1038/s41586-026-10098-2)，正文，`gaut2026` | 2023 年 X 实验，开启算法流改变部分时事/政策态度，关闭不对称；关注行为提供持续机制线索 | 党派认同、情感极化仍有零结果；实验日期与 2026 开源代码版本不同 |
| [Milli et al., PNAS Nexus 2025](https://arxiv.org/abs/2305.16941)，正文，`milli` | 806 人，算法/时间排序内容及自述偏好的对比；算法放大部分负面内容 | 不是长期 feed RCT；全体内容自述偏好略偏算法，政治内容方向相反；按自述偏好排序也可能增加同阵营曝光 |
| [Piccardi et al., Science 2025](https://doi.org/10.1126/science.adu5584)，正文，`piccardi` | 美国党派用户的 X 重排实验；降低/提高敌对政治内容改变组间温度，若干其他结果为零 | 不是“增加任意反方观点都有效”；参与者筛选、平台、十天实验限制外推 |
| [Bail et al., PNAS 2018](https://doi.org/10.1073/pnas.1804840115)，全文已取，`bail` / Europe PMC | 关注相反政治阵营信息的 Twitter 现场实验 | 不能假设单纯更多跨立场接触必然去极化；具体处理与人群重要 |
| [Brady et al., Nature 2026](https://doi.org/10.1038/s41586-026-10536-1)，新增，正文，`brady2026`，[作者 PDF 入口](https://williamjbrady.com/research) | 2,000 人随机使用自建 Bluesky feed 八周；参与度排序放大 IME/toxic 内容，部分社会规范判断改变；分析样本因排除为 1,475 人 | 与“误以为大家都这样想”直接相关；方向有反直觉的**低估**，不能改写成总是高估；自身参与行为无显著差异；不代表中国短视频 |
| [NYU TikTok audit](https://arxiv.org/abs/2501.17831)，正文，`partisan_tiktok`；代码实物 | 2024 美国大选期、跨州机器人条件化；党派一致/不一致曝光和负面党派内容不同 | 转录+LLM 的立场标签有遗漏视觉线索的限制；没有随机改变真人投票偏好。当前 arXiv 与早版摘要数字不能混用 |
| [Amnesty, Driven into Darkness](https://www.amnesty.org.uk/knowledge-hub/all-resources/report-driven-into-darkness/)，报告正文，`amnesty` | 自伤/心理健康场景；40 个自动账号中 31 个完成可分析轨迹，另有手工账号；按画像和标签观察曝光变化 | 这类伤害不等于观点茧房；画像审计不是实际儿童的心理结果随机实验，也不给出所有用户的平均伤害 |
| [Molly Russell 验尸官预防死亡报告](https://www.judiciary.uk/prevention-of-future-death-reports/molly-russell-prevention-of-future-deaths-report/)，正文，`molly_coroner` | 2022 年案件中，验尸官指出算法选择、未经请求提供内容及连续观看的作用 | 具体案件的法律认定，不是短视频平台平均伤害率或普遍因果效应 |
| [Shi & Li, Digital Journalism 2025](https://doi.org/10.1080/21670811.2025.2450312)，局部 | 原始论文存在；媒体报道已取得 | 出版社全文未取到，不能继承报道对“算法训练/意见/立场”的所有因果表述 |
| [渠润泽、徐敬宏，新闻与传播研究 2026(3)](https://sjc.bnu.edu.cn/docs/2026-05/a83991a68bec4b19a7a357bf5bb6138b.pdf)，正文，`quxu` | 509 份自陈问卷，SEM 与 fsQCA | 横截面关联；原文要求进一步干预实验。透明度不是无条件万能解药；“看见本身已经被证实有效”需撤回 |

## 3. 控制与审计的已有研究线

| 来源 / 阅读状态 | 关键核对 | 对 v1 的修改 |
|---|---|---|
| [Mozilla RegretsReporter 2022](https://assets.mofoprod.net/network/documents/Mozilla-Report-YouTube-User-Controls.pdf)，正文，`mozilla` | 参与者随机分反馈通路；拒绝视频与后续视频组成相似性对；约 4 万对人工标签辅助模型；相对控制组 NI 约 11%、dislike 12%、删历史 29%、不推频道 43% | 不是四类反馈使“全部不想看的内容”减少的通用比例；自愿安装扩展样本、自陈访谈和随机处理三层证据要分开 |
| [Boeker & Urman 2022](https://arxiv.org/abs/2201.12271)，正文，`boeker` | TikTok 浏览器配对机器人，测试位置/语言、关注、点赞和观看；关注影响最强 | 不含今天同版本的 NI 测量；不能把行为匹配视作平台内部状态相等 |
| [Liu, Wu & Resnick 2024](https://ojs.aaai.org/index.php/ICWSM/article/view/31363)，正文，`liu2024`；[代码](https://github.com/avliu-um/youtube-disinterest)实物 | 四话题，每话题七策略×五，40 次 stain / 40 次 scrub；首页 NI −88%，删历史 −77%，不推频道 −49%，dislike −45%；视频页弱 | 原计划把删历史说成弱、把代码写 youtube-burst，均须更正；与 Mozilla 不是同一个分母 |
| [Kaplan et al., 2026](https://arxiv.org/abs/2605.10690)，正文，`kaplan` | 15 次实验＝三话题×五次；播种 **25** 条；阶段各 200 条；复发阶段重新观看目标内容 | 不是总共 15 个账号，不是播种 50 条，不是“什么也不做就复发”；克隆的是指定行为历史 |
| [Hosseinmardi et al., PNAS 2024](https://doi.org/10.1073/pnas.2313377121)，正文，`web/hosseinmardi.xml` | 模仿真人历史后与规则机器人比较；转向温和内容后侧栏约 30 条趋近温和参照，首页残留更久 | 2021–22 历史在 2023 重放、压缩时间、桌面样本；频道级意识形态；不是用户刷任意 30 条就重置整个系统 |
| [Tomlein et al., RecSys 2021](https://arxiv.org/abs/2203.13769)，正文，`tomlein`；[代码/数据](https://github.com/kinit-sk/yaudit-recsys-2021)实物 | 先看谣言再看辟谣，按搜索/推荐分开；推荐气泡和下降因话题而异 | 不是主题 entropy 研究；已有观点/谣言方向干预先例 |
| [Srba et al., TORS](https://arxiv.org/abs/2210.10085)，正文，`srba2023` | 扩展上述 YouTube misinformation 审计，含首页和时间动态 | 与 Tomlein 有研究谱系重叠，不应算作完全独立验证 |
| [Haroon et al., PNAS 2023](https://doi.org/10.1073/pnas.2213020120)，正文，`haroon` | 10 万机器人，测一致性、极端程度及问题频道曝光 | **发表版本正文没有 plan 所称的去偏干预实验**；RL 注入与左右差异出现在作者早期[研讨会幻灯片](https://bpb-us-e2.wpmucdn.com/faculty.sites.uci.edu/dist/8/913/files/2023/01/symposium22-Muhammad-Haroon-YouTube.pdf)，`haroon_slides`。不能合为一个 PNAS 结果 |
| [Brown et al., YouTube audit](https://www.jamesbisbee.com/assets/pdf/yt_recs_ideology.pdf)，正文局部，`brown` | 2020 年真实账号实验区分 echo chambers、rabbit holes、radicalization；较窄且温和保守，未见激进化路径 | 作者网站现稿有后续修订，勿统一称“2022 版”；内容收窄也可能不增加极端 |
| [Dynamics of Algorithmic Content Amplification on TikTok](https://arxiv.org/abs/2503.20231)，正文相关段，`amplification` | gaming/food 两主题、观看时长条件；每条件 14 次，另设的中性账号基线未成功 | 前 200 条不是所有用户/所有命题的形成阈值，话题/标签代理不等于观点；不能写成有成功中性对照 |
| [Pecher et al., UMAP 2026](https://arxiv.org/abs/2603.20723)，新增正文，`drift2026`；[代码](https://github.com/kinit-sk/ai-auditology-personalisation-drift-tiktok)实物 | 三组账号、逾 8 万视频，分开标主题与同题立场；中性 cooking 后的变化与争议议题有关，政治立场偏移有别于谣言主题 | **已有短视频同题立场审计**，不能声称观点研究几乎为零；没有测本项目拟议的意图反馈控制。分类验证样本经选取且较清楚，不能把其高准确率当自然 feed 保证 |
| [Revisiting Algorithmic Audits of TikTok](https://arxiv.org/abs/2504.18140)，正文，`revisiting`；[代码](https://github.com/kinit-sk/tiktok-algorithmic-audit-reproducibility)实物 | 复现中时间、平台行为和自动化稳定性会改变结果 | 需要版本、时间和重复实验；不意味着所有审计只能作为无价值案例 |
| [“They've over-emphasized that one search”](https://arxiv.org/abs/2504.13895)，正文，`unwanted` | 14 名 TikTok 用户访谈；不想要的内容与控制困扰 | 用户解释是经验/folk theory，不能证明平台内部到底采用什么机制 |
| [AutoLike 2025](https://arxiv.org/abs/2502.08933)，正文相关段，`autolike` | 提出主动代理/RL 框架；实际小规模测试采用分类概率 > .5 就点赞、否则划走的简化策略，8 次约 150–200 条 | 不把框架中的 RL 当作已训练并充分评估的策略；是引导先例，不等于拟议的命题级透明控制 |
| [Li et al., ICWSM 2026](https://ojs.aaai.org/index.php/ICWSM/article/view/42704)，正文，`li2026` | 18 条件、每条件 1,000 个浏览器代理；降权/替换后选择影响真实 YouTube 后续推荐；位置选择模型是模拟的 | **不是完全离线的虚构推荐器仿真**，也不是平台原生 NI 按钮；内容分类器定义的 harm 与本项目观点充分性不同 |
| [Beyond the Checkbox 2026](https://arxiv.org/abs/2601.18405)，正文，`checkbox` | 审阅公开 DSA 审计报告；不同平台验证深度不同 | YouTube 审计称检查过选项改变前后输出；故“没有任何独立行为证据”过强。作者只能核对报告所写，不能核对实际实施 |
| [Srba et al., PMLR 2025](https://proceedings.mlr.press/v294/srba25a.html)，正文，`srba2025` | 模型化审计的方法论/立场文，强调多轮反馈 | 不把提出框架写成已经大规模验证完成 |
| [Larooij & Törnberg 2025](https://arxiv.org/abs/2508.03385)，正文，`larooij` | 生成式社会仿真比较亲社会干预，依赖结构和假设 | 模型无现实推荐器，条件性结论，不是行为实测的替代物 |

## 4. 立场识别与度量

| 来源 / 阅读状态 | 实际取得的东西 | 限制 |
|---|---|---|
| [Geifman & El-Yaniv, Selective Classification, 2017](https://arxiv.org/abs/1705.08500)，10-03 新增；已读 [HTML 正文](https://arxiv.org/html/1705.08500v2)引言与 §2–3，未复现 | 分类器与拒绝函数分开；以回答覆盖率和已回答项的错误率评价，说明如何选择阈值 | 保证依赖同分布独立抽样等条件；不直接适用于存在时序／跨议题漂移的短视频。不把模型自报置信度当正确率；Working v2 借用评价思路，不宣称移植风险保证 |
| [Khiabani & Zubiaga, ESWA 2025](https://www.zubiaga.org/publications/files/jamadi2025eswa.pdf)，任务定义与方法比较，`stance_survey` | 区分给定目标、跨目标和零样本立场识别，比较数据与方法；None 与 Neutral 的定义因任务而异 | 不能把别的数据集上的标签体系或分数直接移植到自然短视频，更不能由内容作者的立场推出观看者的信念 |
| [C-STANCE, ACL 2023](https://aclanthology.org/2023.acl-long.747/)，正文；[数据](https://github.com/chenyez/C-STANCE)实物 | Subtask A train/dev/test 合计 **48,126** 文本—目标对 | 作者提醒 Subtask B 的 `In Use == 0` 样本要排除以免泄漏；微博目标对不等于短视频标题真值；未见 LICENSE |
| [ORCHID, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.582/)，正文；[数据](https://github.com/xiutian/OrChiD)实物 | 论文 1,218 场/476 题；本次公开 JSON **1,134** 场 | 公开文件与论文规模不同；辩论的明确角色、双边命题、完整语境优于自然 feed 条件 |
| [C-MTCSD, WWW Companion 2025](https://arxiv.org/abs/2504.09958)，正文；[数据](https://github.com/yangyi626/C-MTCSD)实物 | 五话题 **24,264** 条；JSON 存上下文索引，CSV 有对应文本 | GPT-4 零样本 64.07 是该表 Fav/Against F-average，**不是所有中文立场识别的性能上限**，也不能冒充三分类 macro-F1 |
| [DGTA 2026](https://arxiv.org/abs/2601.19802)，正文；[数据](https://github.com/17Huaaa/DGTA-stance-detection)实物 | 六个 JSON 列表合计 **70,931**；开放目标、多目标格式 | 240 个选定用户、LLM 一致性与人工过滤；剔除模糊目标后比自然 feed 容易；未见 LICENSE |
| [ProsCons](https://doi.org/10.1007/s11280-023-01191-x)，局部 | 245 目标、32,667 posts 的多属性中文基准描述 | 名称不是 ProCons；数据须联系作者，未公开取得；本次没有发送邮件 |
| [TikStance 2026](https://arxiv.org/abs/2607.15240)，正文，`tiktok_stance` | 161 视频、13,876 评论，跨目标/评论关系标注 | 评论立场不等于视频作者立场；高参与美国政治抽样；α .72–.74 是该任务结果，不是万能验收线 |
| [RADio, RecSys 2022](https://arxiv.org/abs/2209.13520)，正文；[代码](https://github.com/svrijenhoek/RADio)实物 | 规范目标、不同参照、秩权重与 f-divergence | **Alternative Voices 是发声者群体，不等于议题内正反立场**；Calibration 也不限主题；论文的操作化不宜不加验证照搬 |
| [Draws et al., nDJS](https://arxiv.org/abs/2010.14531)，正文相关公式，`ndjs` | 排序前缀相对集合分布的 viewpoint fairness 指标、7 点量表 | 把 q 改成自述目标是方法扩展；JS 与 sqrt(JS) 不同；搜索排名权重不能无解释用于已观看的时间序列 |
| [Draws et al., ECIR 2023](https://pure.tudelft.nl/ws/portalfiles/portal/150434223/978_3_031_28244_7_18.pdf)，正文，`draws2023` | stance × logic 的 viewpoint 定义和 nDVB；搜索多样化验证 | “逻辑/理由”值得借鉴；均衡理想与健康误导信息的 false balance 是作者也指出的限制 |
| [Chinese Rumor Dataset](https://github.com/thunlp/Chinese_Rumor_Dataset)，实物 | JSONL **31,669** 条 | 谣言类别/真假不等于发帖者对指定主张的态度；不能当短视频辟谣立场金标准 |
| [CED](https://github.com/thunlp/CED)，README 与实物 | 早期谣言检测数据和工具 | 检测谣言的任务、时间组织和对话结构与本项目不同 |

## 5. 数据、模拟、开源系统

| 来源 / 阅读状态 | 本次检查范围 | 不能继承的过强表述 |
|---|---|---|
| [X x-algorithm](https://github.com/xai-org/x-algorithm)，实物，`b79b947` | Phoenix 请求/反馈路径、VM 评分、topic/keyword/author filter、DPP、cold-start、统计 side-effect | 默认参数≠真实部署；负概率权重≠单次点击罚分；1,024≠所有记忆；存在 excluded topics 硬过滤通路 |
| [KuaiRand](https://github.com/chongminggao/KuaiRand)，正文与实物 | 1K、Pure、2026 标题/预测类目补充；原始数量与旧清洗脚本溯源 | 随机插入精选池≠全库关闭个性化；is_hate 没有用户意图；不同入口 tab 不能混称同一种 feed |
| [KuaiRec](https://github.com/chongminggao/KuaiRec)，正文与实物 | 2.0 数据、小矩阵、补充标题/类目 | **不是“真实兴趣的唯一严格真值”**：有限池、挑选高密度、15 天补曝光、观看比率作为偏好代理；99.6% 不证明无流行度偏差 |
| [ShortVideo_dataset](https://github.com/tsinghua-fib-lab/ShortVideo_dataset)，正文与实物 | 抽样 CSV、类目表、24 份实际 ASR；[数据集论文](https://arxiv.org/abs/2502.05922) | 794,053 标签行需折叠到 129,483 曝光；很稀疏；不是用户上传的 SimTok 论文；完整视频/ASR未全量下载 |
| [MicroLens](https://github.com/westlake-repl/MicroLens)，论文/README/[门户](https://recsys.westlake.edu.cn/) | 已克隆代码，核对构建过程与访问条款；100K 交互/标题下载返回 403，未取得原始数据 | **交互主要是评论，不是完整曝光/观看序列**；无 NI；门户禁止视频再分发；不为此项目下载数百 GB 视频 |
| [HOTVCOM, ACL Findings 2024](https://aclanthology.org/2024.findings-acl.130/)，正文 | 约 94k 抖音视频、137m 评论；多模态评论生成研究 | 未找到可用公共数据下载入口；评论生成数据不能直接完成用户曝光审计 |
| [SimTok](https://arxiv.org/abs/2504.08742)，正文与用户上传 v1，`simtok` | 20 agents、4,000 视频池、反馈模型、多层类目覆盖评价 | 类目覆盖低于中位数定义气泡是相对标准，不是有害观点真值；LLM 反馈满意度不是人类福利；加权 BCE 公式若按负权重直译须另行核对 |
| [PersonaAct](https://arxiv.org/abs/2601.22547)，正文；[代码/数据](https://github.com/Silung/PersonaAct)实物 | 下载的论文：2 用户/1,719 交互/27 sessions；仓库现在描述 8 personas/4,485/86，需分版本 | 逃离审计两画像、400+400 步、BEP 是分布变动；画像 A 中快手低于抖音，不能写抖音两个画像都最难逃离 |
| [UCRS](https://arxiv.org/abs/2204.13844)，正文与[代码](https://github.com/WenjieWWJ/UCRS) | 细粒度/粗粒度可控推荐，离线基准和合成控制目标 | 常用最大类别等构造用户目标，不等于收到了真实人的反思偏好；不是对现有 NI 按钮的实测 |
| [CIRS](https://github.com/chongminggao/CIRS-codes)，论文与代码 | 用户模型、连续交互环境、反馈循环设计参考 | 用户离开/厌倦规则预置，不能拿最适应该规则的策略当真实平台最优方案 |
| [DORL, SIGIR 2023](https://arxiv.org/abs/2307.04571)，相关正文，`dorl` | 讨论离线 RL 保守性与流行度强化；真实日志按活跃度分组观察重复率与次日留存，模型中调整惩罚 | 分组关联仍非重复曝光的因果效应；留存不等于反思认可或观点质量 |
| [BEP, Feng et al.](https://arxiv.org/abs/2512.03067)，相关正文，`bep` | 主动探索/依赖推荐两种 LLM 画像，对比类别覆盖；公式为两组覆盖的比值再按轮平均 | 虽称 escape potential，公式不是实际逃离概率，且可大于 1；**与 PersonaAct 同名 BEP 的 JS 分布距离不是同一个量** |
| [Deep Filter Bubble, WWW 2024](https://arxiv.org/abs/2403.04511)，相关正文，`deepbubble` | 分层类别覆盖、相对同周用户中位数判“入茧”，分析一年日志与人口学 | “deep”指类别层级，不等于观点深层封闭；中位数阈值不能证明约一半人受到有害茧房影响；覆盖仍受活动量影响 |
| [DDIR](https://doi.org/10.1145/3828182)，局部；[代码](https://github.com/16061025/DDIR)实物 | README、用户模型/RL入口；作者说明完整环境和复现步骤待补 | 正文访问受阻；不把仓库存在写成已可端到端复现 |
| [BGE-small-zh](https://huggingface.co/BAAI/bge-small-zh-v1.5)，模型/旧 benchmark | 可用作相似性与内容重复的辅助表示 | 向量接近不等于同立场；支持和反对同一命题可能非常相近 |
| DeepSeek API，计划中的工具 | 当前没有调用 API，也没有读取密钥或核实余额 | 旧 cloud 的余额、价格、CPU benchmark 是旧环境记录；不可作为新环境已验证状态 |

## 6. 国内背景、产品与监管

| 来源 | 核对结果和使用边界 |
|---|---|
| [CNNIC 第 56 次报告](https://www.cnnic.net/NMediaFile/2025/0730/MAIN1753846666507QEK67ZS9DH.pdf)，已下载原报告，`cnnic56` | 10.68 亿/95.1% 是截至 **2025-06** 的短视频口径；不要叫 2026 当前值。网络视频的 96.7% 是另一口径。覆盖规模支持现实相关性，不证明伤害发生率 |
| [网络视听报告 2025，新华社](http://www.news.cn/ent/20250327/65fa067f4b614f308c8b1217bf6f976d/c.html) | 156 分钟等使用强度数字应保留原统计口径和年份；不能与 CNNIC 不同期样本直接拼接成同一调查 |
| [中青报大学生调查](https://xinwen.bjd.com.cn/content/s675f7884e4b06b0a56244855.html) | 3,694 份、78% 想减少依赖，同时 **60.3% 对推荐内容满意**；选择性只引用负面会歪曲原材料；报道中的“偷听”是受访者解释，不是已证机制 |
| [老年防沉迷报告报道](https://m.bjnews.com.cn/detail/1734745106168700.html) | 时间/短剧使用和风险线索；非立场偏斜的因果研究 |
| 清华 7,778 人报告 | 可定位的发布线索是 2023 年，完整方法尚未取得；媒体中的若干人数和比例不相符，不继续引用精确比例 |
| [深圳算法素养 1,215 人报告报道](https://static.nfnews.com/content/202511/11/c11899846.html?enterColumnId=46586) | 发布主体线索指向深圳大学，报道提到 5 平台代理、1,215 问卷与 20 访谈；不能写成中传自己的同一调查；完整抽样方法未取得 |
| [陈昌凤、仇筠茜 2020，作者书目页](https://xinwenxueyuan.cuc.edu.cn/_t722/2021/0610/c7649a182802/page.htm) | 《新闻大学》的“在西方”和《新闻与写作》的“在中国”是两篇论文；第二作者为**仇筠茜**，不应误记为邱云芊；完整正文未取得，不能把概念批评缩成否定一切观点封闭 |
| [施颖婕等 2022，作者书目页](https://xsgyy.sufe.edu.cn/ef/40/c19267a257856/page.htm) | 《网络媒介“茧房效应”的类型化、机制及其影响——基于“中国大学生社会心态调查（2020）”的中介分析》，《新闻与传播研究》5 期；全文未取得，不能用其证明国内没有研究观点 |
| [2022 算法推荐规定](https://www.cac.gov.cn/2022-01/04/c_1642894606364259.htm) | 第 16、17 条的公开说明、非个人特征选项/便捷关闭、用户标签选择删除是设计背景；条文不证明功能实际有效 |
| [2024 清朗通知](https://www.gov.cn/zhengce/zhengceku/202411/content_6989143.htm) | 明确将算法典型问题和功能治理列入议题；不是针对每家平台的量化实测 |
| [网信办 2025-05-22 原文](https://www.cac.gov.cn/2025-05/22/c_1749536203490537.htm) | 承认功能效果仍不足并列举整改；**没有按钮效果量或随机实验，也没有具体量化关闭个性化的效果** |
| [抖音备案说明](https://lf3-cdn-tos.draftstatic.com/obj/ies-hotsoon-draft/douyin_agreement/70c3d13a-73cf-403a-8ecf-a16f70887c21.html)；[安全中心报道](http://www.news.cn/tech/20250417/9b2e3622d8764c408c2b667bf73d1d29/c.html) | 自述多目标、探索、打散、随机内容等；不是 X 架构的验证。25 类/默认 9 类是产品呈现线索，未在本次真实账号操作验证 |
| [TikTok 2023 DSA 公告](https://newsroom.tiktok.com/en-eu/compliance-digital-services-act-eu?lang=en) | 非个性化模式按地区/语言热门内容；不是均匀随机、更不是真实世界观点比例；与 Refresh 区分 |
| [TikTok 2025 控制功能](https://newsroom.tiktok.com/tiktoks-new-features-to-help-you-control-your-scroll?lang=en-AU) | Manage Topics 调频，官方明确不完全消除主题；Smart Keyword Filters 扩展同义词等；仍不是已验证的命题级立场控制 |
| [Instagram 2024 Reset](https://about.fb.com/news/2024/11/introducing-recommendations-reset-instagram/) | Explore/Reels/Feed 推荐重置，可复查关注；随后仍继续个性化；并非永久关闭 |
| [Douyin 口服糖尿病药视频](https://formative.jmir.org/2024/1/e57720/)，正文 XML，`web/jmir_diabetes.xml` | 单次搜索前 200 条中纳入 138 条，136 位发布者为医生，14 条含错误信息；DISCERN、可理解性和可操作性是不同维度。不是纵向 feed 审计，**不能由质量问题推出同一命题正反内容都足够** |
| [登革热内容](https://infodemiology.jmir.org/2025/1/e76474)，正文 XML，`web/jmir_dengue.xml` | 搜索 324 条中纳入 156 条，质量指标较低；排除广告、无声和个人经历等内容，样本并非完整自然 feed。已读[更正](https://infodemiology.jmir.org/2025/1/e85305)：更正参考文献，不改变正文引用编号；不能主张医学两方证据等重 |
| “抖音健康辟谣短视频研究”、关闭个性化后热度下降的产品经理文章 | v1 未给出足够精确书目信息；仍是未完全定位的线索，不升级成已核事实 |

## 7. 阅读后仍然开放的问题

1. 新颖性要用**交集上的区别**表达：日常具体议题、理由/叙事而非只删主题、曝光解释与可表达控制意图相连。不能证明“从来没人研究过”；已有 viewpoint diversity、可控推荐、原生按钮审计和谣言去兴趣研究。
2. 中文短视频原始数据是否有足够密度的**同一命题**，以及标题能判断多少，须由数据决定。下载不是可测性证明。
3. 所有实物检查是恢复上下文和识别限制，不是已经完成 WP1–WP6。未训练替代 Phoenix、未调用标注 API、未做真人实验、未在真实平台自动建号。
4. 访问缺口包括 Guess 更正后全文、Shi & Li、Piao 出版版、DDIR 全文、ProsCons 数据、部分国内调查完整方法及未命名文献；不得在最终参考文献里用“已全面核验”统一盖章。
