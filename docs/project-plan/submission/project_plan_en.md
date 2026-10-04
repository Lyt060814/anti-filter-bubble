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

Users may not know what they are missing. The report therefore compares their exposure with reasons found in a documented issue corpus and offers possible adjustment goals for confirmation. This corpus is a limited reference, not a complete or automatically balanced account of the issue.

We will develop the method across at least two issues and evaluate it on a held-out issue. Our main outputs will be an evidence-based report design, a comparison of adaptive intervention policies and a dynamic simulation. An optional tool may demonstrate the process. We will study exposure and control, rather than claim to measure changes in users’ beliefs or well-being.

## 2. Computing and data science approach

This hybrid project uses **data analysis** to describe what users encounter, **algorithmic design** to select actions under information-retention and effort constraints, and **simulation** to test how those actions affect subsequent recommendations. We will reuse established methods where suitable.

### Data analysis: measuring viewpoint exposure

The tool sees content and interaction records $o_{\leq t}$ available up to step $t$, not the platform’s internal state. Keyword and semantic retrieval, followed by large language model (LLM) or vision–language model (VLM) analysis, will extract claims, stances, reasons and source identifiers with supporting passages or timestamps. The analysis pipeline produces an exposure summary:

$$\widehat{e}_t=\Phi(o_{\leq t})=(p_t,\mathbf{r}_t,d_t,u_t).$$

Here $p_t$ is the stance distribution for a defined claim, excluding unknown labels, $\mathbf{r}_t$ gives reason coverage, $d_t$ source repetition, and $u_t$ the unknown-label proportion. Sliding windows track two properties: concentration and change. Shannon entropy $H(p_t)=-\sum_k p_{t,k}\log p_{t,k}$ measures concentration, with lower values indicating exposure concentrated in fewer stances. Jensen–Shannon divergence $\mathrm{JS}(p_t,q)$ measures difference from an explicit reference $q$, such as earlier exposure. Neither establishes harm or implies that uniform exposure is ideal.

Independent double annotation, precision/recall and a held-out issue will test measurement quality. Comparing title-only, transcript-based and visual-context analysis will test whether added modalities resolve errors such as attributing a character’s speech to the creator. Sparse histories will remain unscored. Disagreements and alternative plausible labels for uncertain items will test whether classification errors change the conclusions.

### Algorithmic design: selecting interventions

An action-selection policy chooses $a_t=\pi(\widehat{e}_t,g,b_t)$ using the exposure summary, a confirmed reduce–retain–explore goal $g$ and remaining budget $b_t$. Over horizon $T$, we compare permitted policies by

$$\min_{\pi\in\Pi_{\mathrm{user}}}\mathbb{E}_{\pi}\!\left[\sum_{t=1}^{T}\ell(\widehat{e}_t,g)\right]\quad\mathrm{s.t.}\quad\mathbb{E}_{\pi}[C_T]\leq B,\quad\mathbb{E}_{\pi}[R_T]\geq\rho.$$

$\Pi_{\mathrm{user}}$ contains permitted policies and the expectation averages over random recommendations and responses. The loss $\ell$ measures goal mismatch; $C_T$ is effort and $R_T$ retention relative to no intervention. Budget $B$, minimum retention $\rho$ and measurement rules are fixed by test scenarios or user confirmation. Unknown content and empty feeds cannot count as success. In the parenting example, loss tracks sweeping claims and retention tracks practical advice and distinct explanations. Additional reasons require documented sources.

We will enumerate no-intervention, topic-filtering, negative-feedback, selective-filtering-plus-supplementation, and search/follow policies. Simulation estimates outcomes; infeasible candidates are excluded. If none qualifies, we report no feasible option. Given these estimates, selection is linear in candidate count. Comparisons will show whether selective control retains more wanted information than removing the whole topic, and at what cost. Platform actions and external-tool functions remain distinct. We do not claim global optimality.

### Simulation: testing the recommendation–feedback loop

Let $s_t$ contain recommendation history and user behavioural state. At step $t$, the recommender $\mathcal{R}$ generates exposure $x_t$, the user model $\mathcal{U}$ generates feedback $y_t$, and the selected action $a_t$ enters the state-update rule $\mathcal{F}$:

$$x_t\sim\mathcal{R}(\cdot\mid s_t),\quad y_t\sim\mathcal{U}(\cdot\mid x_t,s_t),\quad s_{t+1}\sim\mathcal{F}(\cdot\mid s_t,x_t,y_t,a_t).$$

This simulation separates viewing tendencies from adjustment goals. The recommender will rank candidates using content relevance and past feedback, with exploration and decaying memory; viewing and negative signals update later rankings. A transparent version will serve as a baseline for a model trained on interaction histories. Rule-based, data-driven, LLM-based and hybrid users will be compared against available held-out logs, including probability calibration. We will also check whether changing the user model reverses which intervention performs best. Watching upsetting videos can conflict with wanting fewer recommendations of them. Each policy receives only observable records, not hidden preferences or recommender parameters.

Matched initial states and repeated random seeds will compare goal attainment, information loss, effort and recurrence. Continued intervention, stopping it and resuming earlier viewing will be tested separately. We will report averages, variation across runs and constraint-violation frequency. Sensitivity to model parameters and label errors will test robustness; simulated effects are not evidence of live-platform effects.

## 3. Related work and research focus

**Engagement and user intentions can differ.** Milli et al. [\[1\]](#ref-1) found that engagement-based ranking and stated preferences did not align for political content on Twitter. Ranking by stated preferences also risked reinforcing agreeable content. Vera and Ghosh [\[2\]](#ref-2) interviewed 14 TikTok users about unwanted recommendations and attempts to remove them. These studies motivate separating attention from confirmed goals; they do not establish the problem’s prevalence among Chinese users.

**Viewpoints require more than category counts.** Pecher et al. [\[3\]](#ref-3) distinguish topic drift from stance drift in a TikTok audit, so within-topic viewpoint analysis is not itself new. Draws et al. [\[4\]](#ref-4) consider stance and underlying logic in search results. This supports examining reasons as well as positions, with additional challenges from roles and incomplete context in short videos.

**Control and its persistence are already studied.** Wang et al.’s UCRS [\[5\]](#ref-5) offers feature-level recommendation controls. Using controlled TikTok accounts, Kaplan et al. [\[6\]](#ref-6) compare skipping with “not interested” and test recurrence when accounts resume watching the target topic. Compass [\[7\]](#ref-7) supports reflective preference refinement on YouTube Shorts, combining simulated engagement with direct filtering and supplementation; its field study involved 15 users over ten days. We can build on these approaches. Our focus is the joint evaluation of exposure to claims and reasons, information retention and maintenance effort within an issue the user still follows. X’s public code [\[8\]](#ref-8) supplies inspectable filtering and scoring mechanisms, not evidence of Chinese platforms’ rules.

**Data and simulation support partial validation.** ShortVideo [\[9\]](#ref-9) links content and behaviour; KuaiRand [\[10\]](#ref-10) provides interaction sequences and randomly exposed videos. Neither records reflective goals. SimTok [\[11\]](#ref-11) demonstrates a recommendation loop with LLM users reading video descriptions. Yoon et al. [\[12\]](#ref-12) evaluate simulated preferences and feedback against human data, supporting separate evaluation of our user model. Platform audits inform experimental conditions, rather than supplying directly transferable effect sizes.

Our research question brings these strands together: **can users reduce a particular claim or explore missing reasons while retaining useful content on the same issue, and what effort does this require?** We investigate this across issues under imperfect content understanding and limited platform access. Our contribution is an evidence-based evaluation of this combined problem.

## 4. Feasibility, limitations and ethics

We need interpretable content and interaction histories. We have obtained ShortVideo samples and KuaiRand-1K/Pure logs with supplementary captions and categories. Eight ShortVideo video–transcript pairs were retrieved and the videos decoded; pretrained semantic retrieval and an untrained user-response network also ran. These checks establish access and execution, not transcription accuracy, model validity or complete feed coverage. ShortVideo’s sampled histories may be discontinuous, so content and trajectory coverage need separate checks. KuaiRand’s random exposures come from a limited video pool, not a complete feed with personalisation disabled.

Next, pilot retrieval and independent annotation will guide issue selection, sample size and error analysis. We will benchmark pretrained LLM/VLM content analysis and rule-based, learned and LLM-based users, measuring resource use on small batches before scaling. If a component fails validation or exceeds available resources, we will use manually checked content or a transparent rule-based simulation, and state the resulting limits. The report will distinguish implemented, validated and proposed components.

Incomplete context or ambiguous speech will receive unknown labels; visual checks and alternative plausible labels will test their effect. History coverage and uncertainty will determine whether an issue-level report is supportable. Unknown platform responses require sensitivity experiments. Negative-feedback associations are not causal effects, and simulated improvements do not establish live-platform or belief changes. Broader exposure does not prove better judgement; selective filtering may narrow a feed further. We will expose these trade-offs and preserve distinctions in evidence quality.

The core uses released research data and simulated users. Goals are explicit test scenarios, not inferred wishes of people in anonymous logs. We will follow data terms, avoid re-identification, minimise personal details and avoid uploading individual viewing histories to external AI services. Public video material will be checked for permitted use and personal information before external processing. Annotators may skip distressing content. Optional human testing requires informed consent and confirmation of applicable course or university requirements; core experiments are offline.

## 5. Timeline and responsibilities

Dates follow the course guidelines and remain subject to Moodle announcements.

| Dates, 2026 | Milestone | Lead |
|---|---|---|
| 5–11 Oct | Select issues, inspect data, pilot independent labels and freeze evaluation approach | Fu Yitong, Wang Junbo |
| 12–18 Oct | Evaluate content understanding; draft exposure report and control comparison | Zhao Dingcheng, Wang Junbo, Li Yitong |
| 19–24 Oct | Worked example and initial simulation ready by 19 Oct; interim meeting 20–24 Oct | Xu Ruicong, Li Yitong; all |
| 25–31 Oct | Compare interventions, assumptions and performance on the held-out issue | Li Yitong, Xu Ruicong, Zhao Dingcheng |
| 1–8 Nov | Consolidate results and report draft; individual progress logs due 4 Nov | All; Wang Junbo coordinates |
| 9–15 Nov | Review claims and references; submit report and individual reflections | All |
| 16–26 Nov | Rehearse and present on the assigned course date | Wang Junbo; all |

| Member | Main responsibility |
|---|---|
| Fu Yitong | Problem definition, literature synthesis, viewpoint annotation and error analysis |
| Li Yitong | Technical integration, constrained intervention algorithm, recommender–user simulation and sensitivity experiments |
| Wang Junbo | User goals, exposure report and control design, independent annotation, report editing |
| Xu Ruicong | Data preparation, trajectory coverage, behavioural modelling and statistical evaluation of simulated users |
| Zhao Dingcheng | Semantic retrieval, LLM/VLM analysis, evidence checking and cross-issue evaluation |

Fu Yitong and Wang Junbo will independently annotate samples under a protocol developed with Zhao Dingcheng, then review disagreements together. Each member will write a substantive section and review another’s. Weekly meetings will track evidence and progress.

## References

[\[1\]]{#ref-1} Milli, S., Carroll, M., Wang, Y., Pandey, S., Zhao, S., & Dragan, A. D. (2025). [*Engagement, User Satisfaction, and the Amplification of Divisive Content on Social Media*](https://doi.org/10.1093/pnasnexus/pgaf062). PNAS Nexus, 4(3), pgaf062.

[\[2\]]{#ref-2} Vera, J. A., & Ghosh, S. (2025). [*“They’ve Over-Emphasized That One Search”: Controlling Unwanted Content on TikTok’s For You Page*](https://arxiv.org/abs/2504.13895). arXiv:2504.13895.

[\[3\]]{#ref-3} Pecher, B., et al. (2026). [*Algorithmic Audit of Personalisation Drift in Polarising Topics on TikTok*](https://doi.org/10.1145/3774935.3806161). UMAP 2026.

[\[4\]]{#ref-4} Draws, T., et al. (2023). [*Viewpoint Diversity in Search Results*](https://doi.org/10.1007/978-3-031-28244-7_18). ECIR 2023, pp. 279–297.

[\[5\]]{#ref-5} Wang, W., Feng, F., Nie, L., & Chua, T.-S. (2022). [*User-Controllable Recommendation Against Filter Bubbles*](https://doi.org/10.1145/3477495.3532075). SIGIR 2022, pp. 1251–1261.

[\[6\]]{#ref-6} Kaplan, L., Patel, D., Gerzon, N., Mislove, A., & Sapiezynski, P. (2026). [*When “For You” Isn’t For You: Measuring User Agency in TikTok’s Algorithmic Feed*](https://arxiv.org/abs/2605.10690). arXiv:2605.10690.

[\[7\]]{#ref-7} Barua, A., Wang, L., & Zhang, A. X. (2026). [*Compass: Continuously Aligning Social Media Feeds via In-Situ Reflections*](https://arxiv.org/abs/2608.04274). UIST 2026; arXiv:2608.04274.

[\[8\]]{#ref-8} xAI. (2026). [*x-algorithm*](https://github.com/xai-org/x-algorithm/tree/b79b947ce9283c786822274ef8fe208c33c585b2) [Source code, commit b79b947].

[\[9\]]{#ref-9} Shang, Y., Gao, C., Li, N., & Li, Y. (2025). [*A Large-scale Dataset with Behavior, Attributes, and Content of Mobile Short-video Platform*](https://arxiv.org/abs/2502.05922). WWW Companion 2025, pp. 793–796.

[\[10\]]{#ref-10} Gao, C., et al. (2022). [*KuaiRand: An Unbiased Sequential Recommendation Dataset with Randomly Exposed Videos*](https://doi.org/10.1145/3511808.3557624). CIKM 2022, pp. 3953–3957. [Caption/category supplement](https://zenodo.org/records/18159199).

[\[11\]]{#ref-11} Sukiennik, N., Wang, H., Zeng, Z., Gao, C., & Li, Y. (2025). [*SimTok: Simulating Filter Bubble on Short-video Recommender System with Large Language Model Agents*](https://arxiv.org/abs/2504.08742). arXiv:2504.08742.

[\[12\]]{#ref-12} Yoon, S., He, Z., Echterhoff, J. M., & McAuley, J. (2024). [*Evaluating Large Language Models as Generative User Simulators for Conversational Recommendation*](https://aclanthology.org/2024.naacl-long.83/). NAACL 2024, pp. 1490–1504.
