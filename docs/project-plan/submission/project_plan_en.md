# Keeping the Topic, Widening the View

Understanding Filter Bubbles and Supporting User Control in Short-Video Feeds

| Fu Yitong | Li Yitong | Wang Junbo | Xu Ruicong | Zhao Dingcheng |
|---|---|---|---|---|
| 3036482371 | 3036289377 | 3036482682 | 3036291100 | 3036292283 |

## 1. Problem and proposed solution

Someone watching parenting videos may repeatedly encounter the claim that strict discipline is the only way to raise a successful child. Their feed still contains food, music and travel, so a chart of content categories would look diverse. Yet within parenting, the same explanation may dominate. The viewer might want fewer sweeping claims while still learning about discipline. A “not interested” button gives them little room to express that distinction.

This project asks: **How can short-video users recognise persistent limits in the viewpoints and reasons they encounter within an everyday issue, and adjust their exposure without losing information they still want?**

We study **filter-bubble risks** in Chinese-language short-video feeds: recommendation and user feedback may repeatedly favour limited viewpoints and reasons within issues such as parenting, relationships and careers. **Viewpoint exposure** is what we measure, not proof of algorithmic causation or harm. Narrow interests are not necessarily harmful, nor does every issue need equal opposing content. Our concern is selective presentation that users may not notice or may find difficult to change on their own terms.

Our proposed solution has three parts. An **exposure report** shows which claims, reasons and sources recur, with examples the user can check. A **control step** asks what the user wants to reduce, retain or explore. A **follow-up comparison** examines whether available actions achieve that goal and how much continued effort they require. For example, a user could request fewer claims that strict discipline is the only effective approach while retaining practical advice and explanations of different approaches.

The method will be developed across at least two issues and evaluated on another issue not used in development. Our main outputs will be an evidence-based report design, a comparison of intervention strategies and a dynamic simulation. A small tool may demonstrate the process, but a finished app is not required. We will study exposure and control, rather than claim to measure changes in users’ beliefs or well-being.

## 2. Computing and data science approach

This is a **hybrid project combining data analysis, algorithmic design and simulation**. Its technical core is selecting interventions that preserve useful information, then examining their effects within a recommendation–feedback loop. We will use existing methods where they fit the task.

### Understand the content

We will retrieve relevant videos using keyword and semantic search, then identify the specific claim, the speaker’s stance, supporting reasons and the evidence available in the video. Large language models (LLMs) can analyse titles and transcripts; vision–language models (VLMs) can interpret frames or video clips when dialogue, subtitles or visual context matter. A character’s line in a sketch must not automatically become the creator’s opinion.

Model outputs will include supporting passages or video segments and an “uncertain” option. Two members will independently label an evaluation sample, resolve or retain disagreements, and check model errors. Comparing titles alone with transcripts and audiovisual input will show when extra context is useful. Retrieval errors will also be checked, including relevant videos missed by the initial search.

### Describe exposure

For each issue, we will summarise the distribution of stances, recurring reasons, repeated source material and changes over time. Comparison baselines might include the user’s earlier feed or a documented collection of relevant arguments; neither automatically represents the “correct” distribution. The report will show missing information and uncertain labels rather than combine everything into a single filter-bubble score.

This analysis must distinguish content collections from personal exposure histories. We will produce individual time-based reports only where the logs contain enough relevant observations. Otherwise, we will report coverage limitations and use clearly identified constructed sequences to test the reporting method.

### Compare adjustments

The input to the control step is a user-confirmed description of what to reduce, retain and add, together with permitted actions. We will compare no intervention, broad topic filtering, targeted negative feedback, selective filtering with sourced supplementary material, and directed searching or following. We will distinguish platform controls from filtering and supplementation provided by a proposed external tool.

A simple constrained selection procedure will reject strategies that remove too much desired information, then compare the remaining options by unwanted exposure, information retained, additional reasons found and effort required. Semantic similarity can help retrieve material, but will not by itself establish whether it adds a different reason. An LLM assistant may clarify requests and call search or analysis tools; the calculations and constraints will remain independently checkable.

### Test the feedback loop

The simulation will separate the content pool, recommender, user and intervention strategy. At each step, the recommender selects content, the user responds, the platform updates its history, and the next recommendation is produced. The user’s tendency to watch something will be represented separately from their stated adjustment goal.

We will compare a transparent rule-based user with data-driven and LLM-based candidates. A promising option combines semantic interpretation with a statistical model of observable behaviour. Where matching content and logs exist, predicted behaviour must be checked against held-out records; plausible explanations alone do not establish realism. The study will retain a simple simulation if more elaborate users cannot be justified.

Experiments will compare continued intervention with stopping it, under different assumptions about recommendation memory, exploration and responses to negative feedback. Outputs will include whether a goal is reached, exposure steps required, useful information lost, actions taken and whether the unwanted pattern returns. Repeated runs will test sensitivity to model assumptions; the simulator does not reproduce a live platform.

## 3. Related work and research focus

**Engagement and user intentions can differ.** Milli et al. [\[1\]](#ref-1) found that engagement-based ranking and stated preferences did not align for political content on Twitter. Ranking by stated preferences also risked reinforcing agreeable content. This motivates separating what attracts attention from what a user wants, without treating user control as an automatic cure. Vera and Ghosh [\[2\]](#ref-2), through interviews with 14 TikTok users, documented unwanted recommendations and efforts to remove them. Their findings support our everyday problem, but do not estimate its prevalence among Chinese users.

**Viewpoints require more than category counts.** Pecher et al. [\[3\]](#ref-3) distinguish topic drift from stance drift in a TikTok audit. Thus, studying viewpoints within a topic is not itself new. Draws et al. [\[4\]](#ref-4) consider viewpoints through both stance and underlying logic in search results. We will apply that distinction to short videos, where roles, incomplete context and repeated stories make classification harder.

**User control already has established approaches.** Wang et al.’s UCRS [\[5\]](#ref-5) allows users to influence recommendation through feature-level controls. Our setting differs because users generally cannot modify the platform’s model. We ask how they can express a more specific goal—keep following an issue while reducing unwanted claims or exploring missing reasons—and pursue it through available actions. X’s public recommendation code [\[6\]](#ref-6) provides inspectable examples of filtering and scoring mechanisms, although it does not establish how Chinese short-video platforms respond.

**Public data and simulation make parts of the study feasible.** Shang et al.’s ShortVideo dataset [\[7\]](#ref-7) links content and user behaviour, while KuaiRand [\[8\]](#ref-8) provides sequential interactions and randomly exposed videos. They offer material for content analysis and behavioural checks, but do not record users’ reflective goals. SimTok [\[9\]](#ref-9) demonstrates a recommendation loop with LLM users receiving textual video descriptions. Yoon et al. [\[10\]](#ref-10) show why simulated preferences and feedback must be checked against human data. We will therefore evaluate the user model separately from the intervention.

Together, these studies leave a practical question for our project: **can a user-facing approach identify repeated reasons within everyday issues, translate a specific adjustment goal into available actions, and compare the resulting information loss and maintenance effort?** Our contribution is to investigate this question across several issues under imperfect content understanding and limited platform access, rather than invent a new recommendation algorithm.

## 4. Feasibility, limitations and ethics

We have obtained public short-video content and interaction datasets, checked video–transcript pairs, and run initial retrieval and response-model checks. These establish access and basic execution, not classification quality or realistic simulation.

Pilot annotation will guide sample selection to cover important cases and assess errors. We will reuse pretrained models and established statistical methods. Large-model inference requires suitable computing resources; if these are unavailable or ineffective, we can still analyse manually checked content and demonstrate the proposed control logic in a transparent simulation. The report will state which components were implemented and which remain designs.

The main limitations are incomplete video context, sparse personal histories and unknown platform responses. Observational changes after negative feedback will be reported as associations, not causal effects. Simulation results will remain conditional on their assumptions. Broader exposure does not prove better judgement, and removing disliked views can itself narrow a feed. We will make those trade-offs visible and avoid treating opposing claims as equally credible when their evidence differs.

The core work uses publicly released research data and simulated users. Offline adjustment goals will be specified as test scenarios, not inferred as the wishes of people in anonymous logs. We will follow dataset terms, avoid identifying individuals, and keep unnecessary personal details out of examples and shared outputs. Any external AI processing must respect the source’s permitted use and avoid sending identifiable histories. Human testing is optional; before recruitment, we would confirm applicable course or university requirements and obtain informed consent. No live account automation or platform intervention is needed for the core study.

## 5. Timeline and responsibilities

Dates follow the course guidelines and remain subject to Moodle announcements.

| Dates, 2026 | Milestone | Lead |
|---|---|---|
| 4 Oct | Submit plan; confirm question and responsibilities | Li Yitong; all |
| 5–11 Oct | Select issues, inspect data, pilot labels and freeze evaluation approach | Fu Yitong, Xu Ruicong, Zhao Dingcheng |
| 12–18 Oct | Evaluate content understanding; draft exposure report and control comparison | Zhao Dingcheng, Wang Junbo, Li Yitong |
| 19–24 Oct | Prepare a worked example and initial simulation for the interim meeting | Xu Ruicong, Li Yitong; all |
| 25–31 Oct | Compare interventions, assumptions and performance on the held-out issue | Li Yitong, Xu Ruicong, Zhao Dingcheng |
| 1–8 Nov | Consolidate results and report draft; individual progress logs due 4 Nov | All; Wang Junbo coordinates |
| 9–15 Nov | Review claims and references; submit report and individual reflections | All |
| 16–26 Nov | Rehearse and present on the assigned course date | Wang Junbo; all |

| Member | Main responsibility |
|---|---|
| Fu Yitong | Problem definition, literature synthesis, viewpoint annotation and interpretation of content errors |
| Li Yitong | Technical integration, constrained intervention algorithm, recommender–user simulation and sensitivity experiments |
| Wang Junbo | User adjustment goals, exposure report and control-flow design, independent annotation and report editing |
| Xu Ruicong | Data preparation, trajectory coverage, behavioural modelling and statistical evaluation of simulated users |
| Zhao Dingcheng | Semantic retrieval, LLM/VLM content analysis, evidence checking and cross-issue evaluation |

Fu Yitong and Wang Junbo will independently annotate the evaluation sample using a protocol developed with Zhao Dingcheng; disagreements will be reviewed together. Each member will write a substantive section and review another’s work. Weekly meetings will track evidence, dependencies and progress.

## References

[\[1\]]{#ref-1} Milli, S., Carroll, M., Wang, Y., Pandey, S., Zhao, S., & Dragan, A. D. (2024). [*Engagement, User Satisfaction, and the Amplification of Divisive Content on Social Media*](https://arxiv.org/abs/2305.16941v6). arXiv:2305.16941, version 6.

[\[2\]]{#ref-2} Vera, J. A., & Ghosh, S. (2025). [*“They’ve Over-Emphasized That One Search”: Controlling Unwanted Content on TikTok’s For You Page*](https://arxiv.org/abs/2504.13895). arXiv:2504.13895.

[\[3\]]{#ref-3} Pecher, B., et al. (2026). [*Algorithmic Audit of Personalisation Drift in Polarising Topics on TikTok*](https://arxiv.org/abs/2603.20723). UMAP 2026.

[\[4\]]{#ref-4} Draws, T., et al. (2023). [*Viewpoint Diversity in Search Results*](https://doi.org/10.1007/978-3-031-28244-7_18). ECIR 2023, pp. 279–297. [doi:10.1007/978-3-031-28244-7_18](https://doi.org/10.1007/978-3-031-28244-7_18).

[\[5\]]{#ref-5} Wang, W., Feng, F., Nie, L., & Chua, T.-S. (2022). [*User-Controllable Recommendation Against Filter Bubbles*](https://doi.org/10.1145/3477495.3532075). SIGIR 2022, pp. 1251–1261. [doi:10.1145/3477495.3532075](https://doi.org/10.1145/3477495.3532075).

[\[6\]]{#ref-6} xAI. (2026). [*x-algorithm*](https://github.com/xai-org/x-algorithm/tree/b79b947ce9283c786822274ef8fe208c33c585b2) [Source code, commit b79b947].

[\[7\]]{#ref-7} Shang, Y., Gao, C., Li, N., & Li, Y. (2025). [*A Large-scale Dataset with Behavior, Attributes, and Content of Mobile Short-video Platform*](https://arxiv.org/abs/2502.05922). WWW Companion 2025, pp. 793–796.

[\[8\]]{#ref-8} Gao, C., et al. (2022). [*KuaiRand: An Unbiased Sequential Recommendation Dataset with Randomly Exposed Videos*](https://doi.org/10.1145/3511808.3557624). CIKM 2022, pp. 3953–3957. [doi:10.1145/3511808.3557624](https://doi.org/10.1145/3511808.3557624).

[\[9\]]{#ref-9} Sukiennik, N., Wang, H., Zeng, Z., Gao, C., & Li, Y. (2025). [*SimTok: Simulating Filter Bubble on Short-video Recommender System with Large Language Model Agents*](https://arxiv.org/abs/2504.08742). arXiv:2504.08742.

[\[10\]]{#ref-10} Yoon, S., He, Z., Echterhoff, J. M., & McAuley, J. (2024). [*Evaluating Large Language Models as Generative User Simulators for Conversational Recommendation*](https://aclanthology.org/2024.naacl-long.83/). NAACL 2024, pp. 1490–1504.
