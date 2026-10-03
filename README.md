# anti-info-bubble

COMP1110 (HKU, 2026/27 Sem 1) group project on information cocoons / filter bubbles (信息茧房).

> **Current direction (2026-10-03):** [Working plan v3](docs/project-plan/working_plan_v3.md) and [Execution plan v3](docs/project-plan/execution_plan_v3.md) are the final planning baseline. They connect multi-issue, evidence-grounded video understanding, exposure diagnosis, user-confirmed interventions and validated dynamic simulation. LLM/VLM and hybrid user models are primary candidates, selected through task-specific evaluation. [Expanded resource review](docs/project-plan/resource_review_v3.md) records source/code inspection; [feasibility checks](docs/context-recovery/plan_v3_feasibility.md) separate real downloads and smoke runs from uncompleted experiments. A user tool is optional. The [bilingual course proposal](docs/project-plan/submission/README.md) condenses this direction into the required submission format.

> **Deep reading of the two v1 plans:** [第一性原理复核](docs/project-plan/first_principles_review.md) explains the revised problem framing; [来源台账](docs/context-recovery/plan_source_review.md) and [数据与源码实物检查](docs/context-recovery/data_and_code_review.md) record what the primary sources and downloaded resources actually support.

**Current question (pending final team confirmation):**
*How can short-video users discover persistent limits in the viewpoints, reasons and narratives they encounter, then choose and evaluate ways to broaden their information while retaining valuable content and control over their choices?*

**Current course proposal (shared with teammates for review; not submitted to the course platform):** [English PDF](docs/project-plan/submission/Project_Plan_EN.pdf) · [中文 PDF](docs/project-plan/submission/Project_Plan_ZH.pdf). Editable Word and Markdown versions are in [submission/](docs/project-plan/submission/README.md); member names, student IDs and named responsibilities are included.

Earlier course Project Plan: `docs/project-plan/Project_Plan.pdf` (source: `project_plan.md`; Word: `Project_Plan.docx`). These files still describe the detect-and-escape draft and have not been regenerated from v3. Decision history and source checks: [上下文恢复与续接入口](docs/context-recovery/README.md).

## Repository layout

| Path | What it is |
|---|---|
| `docs/00_requirements_summary.md` | 课程要求与评分细则中文速览 |
| `docs/01_topic_candidates.md` | 候选题目对比与推荐方案（讨论稿） |
| `docs/research/` | 第一轮调研笔记（文献、政策、审计方法、模型）+ 文献核对清单 |
| `docs/resources/` | 第二轮资源清单（数据集、代码、X 算法代码地图、自采数据、破茧方案）— **从 `docs/resources/README.md` 开始看** |
| `sources/` | [外部资源管理](sources/README.md)：核心代码 submodule、版本清单与本地数据／模型缓存 |
| `analysis/` | 探索性分析脚本（数据不入库，见脚本注释的下载地址） |
| `docs/project-plan/` | [版本与阅读入口](docs/project-plan/README.md)：当前 v3、正式提交稿和历史方案 |

## Key dates (tentative — confirm on Moodle)

| Deliverable | Due |
|---|---|
| Project Plan | Oct 4 |
| Interim Progress Meeting | Oct 20–24 |
| Interim Progress Log | Nov 4 |
| Final Report + Self-Reflection | Nov 15 |
| Group Presentation | Nov 17/19/24/26 |
