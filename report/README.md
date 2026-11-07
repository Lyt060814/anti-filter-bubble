# Final Report 工作区

依据 *COMP1110 Guidelines for Final Report*（2026-10-31 版，原文以 Moodle 为准）。报告 11-15 提交，PDF 或 Word。

## 课程硬性要求

- **独立成文**：读者没看过 Project Plan。所有背景、定义、方法都要在报告里讲清，不能写"见我们的计划"。
- **不交代码**：代码不评分。实现工作只能通过文字、图表和截图（附说明）体现，所以评分所需的一切都要写进报告。
- **篇幅**：约 10–20 页，纵向版式，连贯的段落配图表。图表编号、标题清楚，格式统一。
- **必需部分**：
  - 摘要（约 250 词，必须明确写出研究空白）；
  - 成员贡献表（**五人都要列**，写具体完成了什么）；
  - 参考文献（正文引用与文末条目一一对应）；
  - 生成式 AI 使用声明（即使没用也要写）。
- **完成与计划要分开**：示例、合成数据、假设性结果都要明确标注，不能把预期写成观察结果。能用小算例说明方法的，就放一个。
- **AI 声明**：每一处用 AI 生成、后来进入报告的材料，都要写明工具与模型版本、影响哪些部分、**确切的提示词**。长对话可以概括，但生成入稿内容的提示词要原样给出。见 [ai_use_log.md](ai_use_log.md)。

评分权重：技术深度 30%、批判性思考与解读 20%、摘要与研究空白 15%、文献综述 15%、结构与写作 10%、参考文献 5%、贡献表 5%。

## 语言与结构

报告用**英文**撰写（课程以英文授课，此前的进度记录也是英文）；仓库内部的计划和任务说明仍用中文。各节写在 `sections/` 下，文件名带编号。预计约 15 页：

| 文件 | 节 | 约页数 | 负责 |
|---|---|---:|---|
| `0_abstract.md` | Abstract（约 250 词） | 0.5 | Li Yitong |
| `1_introduction.md` | Introduction：问题情境（大学生视角）、研究问题、贡献 | 1.5 | Li Yitong |
| `2_related_work.md` | Related work | 2 | Zhao Dingcheng |
| `3_concepts.md` | Concepts and theory：$(m,V)$、三层分解、命题 | 2.5 | Li Yitong |
| `4_data_taxonomy.md` | Data and narrative distribution（RQ1），含双模型核查 | 2.5 | Zhao Dingcheng、Li Yitong |
| `5_case_study.md` | Case study（RQ2、RQ3）：OneRec 实测、模拟、察觉 | 4 | Xu Ruicong、Li Yitong |
| `6_design.md` | Design implications：曝光报告样稿 | 1 | Zhao Dingcheng |
| `7_discussion.md` | Limitations, ethics, conclusions | 1 | Li Yitong |
| `8_contributions.md` | Team member contribution | 0.5 | 全组，见 [contributions.md](contributions.md) |
| `9_references.md` | References | 1 | Zhao Dingcheng 统一格式 |
| `10_ai_declaration.md` | Declaration of generative AI use | 1 | 各人从 [ai_use_log.md](ai_use_log.md) 汇总 |

## 为报告留存数据（所有人）

报告不能附代码，所以每个图表背后的数据都要留在仓库里，方便核对、重画和回答提问：

1. **每张图、每张表对应一个结果文件**：`<工作目录>/results/<图名>.csv`（或 `.json`），存画图用的原始数字，而不只是均值。例如模拟要保存每个种子的结果，OneRec 实验要保存每个用户的结果。
2. **同一目录放一个 `<图名>.meta.json`**，记录：参数、随机种子、样本量、生成脚本路径、提交号（`git rev-parse --short HEAD`）、日期，以及数字属于"实测"还是"情境假设"。
3. **图片存为 PNG（300 dpi）和 PDF 两种**，放在 `<工作目录>/figures/`，文件名与结果文件对应。
4. **截图**：可以证明工作量的界面或输出（例如 OneRec 的输入格式、标注界面、模拟运行输出），存到 `report/screenshots/`，并附一句说明。截图不能包含视频描述原文或账号信息。
5. **登记**：每完成一张图，在 [figures.md](figures.md) 加一行。
