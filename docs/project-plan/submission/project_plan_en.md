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

We will develop the method across at least two issues and evaluate it on a held-out issue. Our main outputs will be an evidence-based report design, a comparison of adaptive intervention policies and a dynamic simulation. An optional tool may demonstrate the process. We will study exposure and control, rather than claim to measure changes in users’ beliefs or well-being.

## 2. Computing and data science approach

This hybrid project uses **data analysis** to describe what users encounter, **algorithmic design** to select actions under information-retention and effort constraints, and **simulation** to test how those actions affect subsequent recommendations. We will reuse established methods where suitable.

### Data analysis: measuring viewpoint exposure

The tool sees content and interaction records $o_{\leq t}$ available up to step $t$, not the platform’s internal state. Keyword and semantic retrieval, followed by large language model (LLM) or vision–language model (VLM) analysis, will extract claims, stances, reasons and source identifiers with supporting passages or timestamps. The analysis pipeline produces an exposure summary:

$$\widehat{e}_t=\Phi(o_{\leq t})=(p_t,\mathbf{r}_t,d_t,u_t).$$

Here $p_t$ is the stance distribution for a defined claim, excluding unknown labels, $\mathbf{r}_t$ gives reason coverage, $d_t$ source repetition, and $u_t$ the unknown-label proportion. Sliding windows track two properties: concentration and change. Shannon entropy $H(p_t)=-\sum_k p_{t,k}\log p_{t,k}$ measures concentration, with lower values indicating exposure concentrated in fewer stances. Jensen–Shannon divergence $\mathrm{JS}(p_t,q)$ measures difference from an explicit reference $q$, such as earlier exposure. Neither establishes harm or implies that uniform exposure is ideal.

Independent double annotation, precision/recall, modality comparisons and a held-out issue will test measurement quality; sparse histories will remain unscored. Disagreements and alternative plausible labels for uncertain items will test whether classification errors change the conclusions.

### Algorithmic design: selecting interventions

An action-selection policy chooses $a_t=\pi(\widehat{e}_t,g,b_t)$ using the exposure summary, a confirmed reduce–retain–explore goal $g$ and remaining budget $b_t$. Over horizon $T$, we compare permitted policies by

$$\min_{\pi\in\Pi_{\mathrm{user}}}\mathbb{E}_{\pi}\!\left[\sum_{t=1}^{T}\ell(\widehat{e}_t,g)\right]\quad\mathrm{s.t.}\quad\mathbb{E}_{\pi}[C_T]\leq B,\quad\mathbb{E}_{\pi}[R_T]\geq\rho.$$

$\Pi_{\mathrm{user}}$ contains permitted policies and the expectation averages over random recommendations and responses. The loss $\ell$ measures goal mismatch; $C_T$ is effort and $R_T$ retention relative to no intervention. Budget $B$, minimum retention $\rho$ and measurement rules are fixed by test scenarios or user confirmation. Unknown content and empty feeds cannot count as success. In the parenting example, loss tracks sweeping claims and retention tracks practical advice and distinct explanations. Additional reasons require documented sources.

We will enumerate no-intervention, topic-filtering, negative-feedback, selective-filtering-plus-supplementation, and search/follow policies. Simulation estimates outcomes; infeasible candidates are excluded. If none qualifies, we report no feasible option. Given these estimates, selection is linear in candidate count. Platform actions and external-tool functions remain distinct. We do not claim global optimality.

### Simulation: testing the recommendation–feedback loop

Let $s_t$ contain recommendation history and user behavioural state. At step $t$, the recommender $\mathcal{R}$ generates exposure $x_t$, the user model $\mathcal{U}$ generates feedback $y_t$, and the selected action $a_t$ enters the state-update rule $\mathcal{F}$:

$$x_t\sim\mathcal{R}(\cdot\mid s_t),\quad y_t\sim\mathcal{U}(\cdot\mid x_t,s_t),\quad s_{t+1}\sim\mathcal{F}(\cdot\mid s_t,x_t,y_t,a_t).$$

This simulation separates viewing tendencies from adjustment goals. Rule-based, data-driven, LLM-based and hybrid users will be compared against available held-out logs, including probability calibration. Recommendation memory, exploration and feedback strength will vary across experiments. Watching upsetting videos can conflict with wanting fewer recommendations of them. Each policy receives only observable records, not hidden preferences or recommender parameters.

Matched initial states and repeated random seeds will compare goal attainment, information loss, effort and recurrence. Continued intervention, stopping it and resuming earlier viewing will be tested separately. We will report averages, variation across runs and constraint-violation frequency. Sensitivity to model parameters and label errors will test robustness; simulated effects are not evidence of live-platform effects.

## 3. Related work and research focus

**Engagement and user intentions can differ.** Milli et al. [\[1\]](#ref-1) found that engagement-based ranking and stated preferences did not align for political content on Twitter. Ranking by stated preferences also risked reinforcing agreeable content. This motivates separating what attracts attention from what a user wants, without treating user control as an automatic cure. Vera and Ghosh [\[2\]](#ref-2), through interviews with 14 TikTok users, documented unwanted recommendations and efforts to remove them. Their findings support our everyday problem, but do not estimate its prevalence among Chinese users.

**Viewpoints require more than category counts.** Pecher et al. [\[3\]](#ref-3) distinguish topic drift from stance drift in a TikTok audit. Thus, studying viewpoints within a topic is not itself new. Draws et al. [\[4\]](#ref-4) consider viewpoints through both stance and underlying logic in search results. We will apply that distinction to short videos, where roles, incomplete context and repeated stories make classification harder.

**User control already has established approaches.** Wang et al.’s UCRS [\[5\]](#ref-5) allows users to influence recommendation through feature-level controls. Our setting differs because users generally cannot modify the platform’s model. We ask how they can express a more specific goal—keep following an issue while reducing unwanted claims or exploring missing reasons—and pursue it through available actions. X’s public recommendation code [\[6\]](#ref-6) provides inspectable examples of filtering and scoring mechanisms, although it does not establish how Chinese short-video platforms respond.

**Public data and simulation make parts of the study feasible.** Shang et al.’s ShortVideo dataset [\[7\]](#ref-7) links content and user behaviour, while KuaiRand [\[8\]](#ref-8) provides sequential interactions and randomly exposed videos. They offer material for content analysis and behavioural checks, but do not record users’ reflective goals. SimTok [\[9\]](#ref-9) demonstrates a recommendation loop with LLM users receiving textual video descriptions. Yoon et al. [\[10\]](#ref-10) show why simulated preferences and feedback must be checked against human data. We will therefore evaluate the user model separately from the intervention.

Together, these studies leave a practical question for our project: **can a user-facing approach identify repeated reasons within everyday issues, translate a specific adjustment goal into available actions, and compare the resulting information loss and maintenance effort?** Our contribution is to investigate this question across several issues under imperfect content understanding and limited platform access, rather than invent a new recommendation algorithm.

## 4. Feasibility, limitations and ethics

We have obtained public short-video content and interaction datasets, checked video–transcript pairs, and run initial retrieval and response-model checks. These establish access and execution, not accuracy or simulation realism.

Pilot annotation will guide sample selection to cover important cases and assess errors. We will reuse pretrained models and established statistical methods. Large-model inference requires suitable computing resources; if these are unavailable or ineffective, we can still analyse manually checked content and demonstrate the proposed control logic in a transparent simulation. The report will state which components were implemented and which remain designs.

The main limitations are incomplete video context, sparse personal histories and unknown platform responses. Observational changes after negative feedback will be reported as associations, not causal effects. Simulation results will remain conditional on their assumptions. Independently checked labels will be used where available to assess whether measurement errors make an intervention look better than it is. Broader exposure does not prove better judgement, and removing disliked views can itself narrow a feed. We will make those trade-offs visible and avoid treating opposing claims as equally credible when their evidence differs.

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
