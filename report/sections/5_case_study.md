<!-- BEGIN XU RUICONG SIMULATION: material outside these markers belongs to other authors -->
## Pilot-matched simulation and detectability

The simulations show how the same feedback mechanism can create and reduce narrative skew, conditional on a specified representation and memory policy. They are synthetic experiments fitted to a few pilot responses, not measurements of an online platform or users' beliefs. We use six homogeneous groups: A (the target narrative), B (other videos within the topic), and four outside topics. Recommendation is a weighted softmax, π(i) ∝ wᵢ exp(u·vᵢ/τ), where w supplies the initial topic and narrative shares. Topic items share coordinate t. Their attribute coordinates are c(1−s) for A and −cs for B, where s is A's assumed supply share. Thus B is not coded as strongly anti-A, and the supply-weighted attribute mean is zero.

An exposed item is completed with probability σ(−1+1[topic]+θ1[A]); completion adds ηvᵢ to the user state. Forgetting acts at every organic exposure. Each state coordinate is clipped to eleven times the largest absolute item coordinate. This allows ten calibration injections without clipping and prevents unbounded scores. Coordinatewise clipping preserves attribute memory when topic coordinates saturate, but it is an assumed policy, not an identified OneRec mechanism. There is no within-group item heterogeneity or noise.

We compute topic exposure m=π(A)+π(B) exactly. Following the reviewed R2 design, skew is measured relative to supply: V_sup=log(π(A)/π(B))−log(s/(1−s)). This is **total skew**, not the platform-referenced personal V defined in the theory section. These runs cannot separate global amplification from individual personalization. Intervention changes use the same fixed supply reference. Twenty independent seeds per setting give pointwise 95% Monte Carlo intervals for means, using mean ±2.093·SD/√20; these intervals do not represent uncertainty about real platforms.

| Quantity | Inputs or scan | Evidence status |
|---|---|---|
| Topic injection contrast | Log topic-exposure ratio +0.70 | Repository-reported OneRec v5 pilot, feasibility §3.1; uncertain calibration input |
| Attribute injection contrast | +1.13 for group labels; +0.65 for conflict | OneRec v5 pilot, §3.3; used Qwen labels, pending stronger-label replication |
| Positive NI response | About 78% of neutral-mention response | OneRec v5 pilot, §3.2; not directly an update coefficient |
| Calibration sensitivity | Each target separately ×0.5 and ×1.5 | Assumed stress tests, not a joint confidence region |
| Effective scale and units | η=τ=1; t≈0.263; fitted c≈0.336 or 0.255 | Unit convention plus moment fit; only ηt²/τ and ηc²/τ are identified |
| Initial topic share | 10%, 15%, 20%; main case 15% | Heavy-viewer scenarios, not the typical RecIF user |
| A supply within topic | 2%, 10%, 50%; main case 2% | Assumed supply; exposure prevalence does not identify it |
| Generating c/t | 0–1 in 0.1 steps, plus 0.15, 0.59 and each fitted ratio | Scenario scan; embedding contrast anchors are not fitted generating coefficients |
| Preference and memory | θ=0, 0.5, 1, 2; forgetting 0.0002, with ×10 sensitivity | Assumed response and memory rules |
| Horizon | 6,000 formation, 1,000 active, 2,000 follow-up exposures | Assumed experimental duration; no elapsed-time conversion |
| Output classifier | Main-grid benchmark: recall 0.8, false-positive rate 0.02; v2 sensitivity: 0.8, 62/495 | Benchmark assumed; v2 rates are cross-model agreement estimates, not gold-standard accuracy |

Moment matching uses a fixed synthetic 15% topic-prior context: ten mean-topic injections versus ten outside injections split 3/3/2/2 across outside topics, and ten A versus ten B injections for the attribute contrast. It matches aggregate response targets, not the actual videos or histories used in OneRec. The fitted group-label coefficient ratio is 1.280, outside the original 0–1 grid; the conflict ratio is 0.971. We retain both fitted points and the original grid. The 262 settings also vary supply and interest priors; target sensitivities are one-at-a-time at the main prior and supply. Full per-seed outputs and calibration residuals are retained in the repository.

### Formation

![Pilot-matched formation and full coefficient sweep](../../analysis/v6_simulation/figures/formation_calibrated.png)

**Figure F-R3-formation.** Synthetic group-label scenarios at 2% A supply and 15% initial topic exposure. Time panels show selected coefficient ratios; the final row shows the complete ratio sweep, including the fitted point. Bands are pointwise 95% Monte Carlo intervals over 20 seeds. All response and memory rules remain conditional assumptions despite the pilot-matched injection scale.

At θ=2, mean terminal total skew is 0.0061 at c/t=0.15, 0.1094 at 0.59, and 0.8120 at the fitted ratio, with respective interval half-widths 0.0014, 0.0282 and 0.2032. The last value corresponds to approximately 2.25 times the supply odds, while mean topic exposure remains 0.1516. Neutral-user skew at the fitted ratio is 0.0285 with interval [−0.1530, 0.2101], consistent with zero. Representation contrast and preference can therefore change narrative composition while topic exposure remains similar. The stable topic plateau partly follows from the clipping policy; it is not evidence that real platforms have the same stability. The smaller attribute scale in the conflict pilot does not establish which narrative is more harmful or more prevalent.

### Escape and persistence

All eleven arms start from identical formation states. S0 continues natural behaviour. On encountering A, S1a replaces completion with a negative unit update, S1b with a positive 0.5 update, and S2 with no update. S3 always completes encountered B; S4 adds one completed B every ten organic exposures. S5 once removes surviving A contributions, including their actual historical clipping factors; this is an idealized ledger deletion, not counterfactual replay of the whole history. S6 thins A/B output by the assumed classifier rates and refills from the remainder. S7 removes all topic output. S8 serves using the fixed mean terminal state of the 80 synthetic users; S9 resets once. S8 uses a mean state, not a mean probability distribution, and need not yield zero total skew.

![Calibrated strategy comparison](../../analysis/v6_simulation/figures/escape_calibrated.png)

**Figure F-R3-escape.** Synthetic effects after 1,000 active exposures, at θ=2, supply 2% and prior 15%. Left: c/t=0.59; right: fitted group-label ratio 1.280. Bars are pointwise 95% Monte Carlo intervals. Preferred outcomes lower skew near Δlog m=0. S7 has m=0 and undefined skew, so it is omitted from the plane.

At the fitted ratio, negative NI reduces skew by 0.7364 with mean Δlog m=−0.0120, whereas the assigned positive-0.5 arm changes skew by +0.0140. Their paired mean difference is 0.7504 (95% interval 0.5991–0.9018). This does not mean every positive update produces a larger cumulative effect than natural behaviour: the intervention replaces a stochastic completion, and forgetting still acts. A separate fit of the 78% positive NI response gives coefficient 0.7706, rather than 0.78; that fitted arm increases skew by 0.1098 (95% half-width 0.0822). Its response-target sensitivity also includes 39% and 117%.

Under idealized controls, ledger deletion gives ΔV_sup=−1.1788 with Δlog m=−0.0084, while filtering gives −1.7833 with −0.0476. Skipping A yields −0.2954 with −0.0058. Thus filtering gives the largest immediate reduction in this main case, while deletion and skipping retain more topic exposure. These are conditional comparisons, not a universal or effort-matched ranking. The filter uses the assumed benchmark classifier; the v2 cross-check instead finds Qwen false-positive rate 62/495≈12.5%, which can substantially increase collateral removal of B. Deletion and feedback assume perfect knowledge of A. Bulk deletion counts as one action, whereas search adds 100 watched items and always-complete-B acts on about 147 encountered items. Action counts are not equivalent human costs, and deletion can overshoot toward B.

Completing more encountered B (S3) does not reverse the main case's accumulated skew: mean ΔV_sup=+0.0020 with 95% half-width 0.0720, compared with +0.1019 under S0. This qualifies the practical expectation of positive substitution. In the centred coding, a B update's local attribute contrast is −c²s, whereas an A update's is c²(1−s). At 2% supply, the B signal per update is about 1/49 of A's. Proposition 2 predicts the correct negative local sign but does not guarantee a large cumulative reduction when natural A feedback continues; clipping and forgetting also affect the longer trajectory. B here means ordinary within-topic content, not strongly opposed counter-narratives.

A supplementary rerun of the two main fitted cases replaces the benchmark classifier with the v2 Qwen-versus-DeepSeek rates, retaining the same seeds and dynamics. In the group-label case it gives ΔV_sup=−1.6551 and Δlog m=−0.1453, versus −1.7833 and −0.0476 under the benchmark. This is a main-case sensitivity, not a full-grid replacement. A separate instantaneous-filter calculation over all formation endpoints also retains each seed's predicted collateral loss. Neither calculation propagates uncertainty in the cross-model error rates.

![Persistence after interventions stop](../../analysis/v6_simulation/figures/persistence_calibrated.png)

**Figure F-R3-persistence.** Synthetic follow-up relative to matched S0, with the same main settings. Step 0 retains the active control for endpoint measurement; output controls are removed before the next natural exposure. Bands are pointwise 95% Monte Carlo intervals. The original completion preferences resume in every arm.

Filtering loses its direct output effect immediately, though the history learned while filtering may retain an effect. History-changing operations can persist longer under this assumed memory rule. We save both the task-defined rebound halfway toward pre-intervention skew and a separate half-life of improvement relative to matched S0. No initial reduction means an undefined rebound time. A reduction not halved within 2,000 follow-up exposures is right-censored, not assigned a 2,000-exposure half-life. In the main fitted case, all 20 deletion runs improve on matched S0 initially and all 20 remain censored at the horizon; negative NI has 19 initial improvements, 18 censored. These statements do not estimate OneRec's finite-history persistence.

### How much exposure is needed to notice skew?

For classifier recall α and false-positive rate β, observed prevalence is q=β+(α−β)p. We apply the independent two-arm normal approximation in Proposition 4, at one-sided significance 0.05, power 0.8 and equal user/reference sample sizes. Odds multiplier r gives p_u=rp₀/(1−p₀+rp₀). Each arm requires approximately

$$n=\frac{(z_{0.95}+z_{0.8})^2[q_u(1-q_u)+q_0(1-q_0)]}{(\alpha-\beta)^2(p_u-p_0)^2}.$$

![Detection exposure requirements](../../analysis/v6_simulation/figures/detection_revised.png)

**Figure F-R4-revised.** Deterministic sample-size scenarios for odds multipliers 2–8. The main reference is DeepSeek v2, 5/500=1.0%. The left panel also retains version-specific historical anchors (v0 1.4%, v1 0.6%, earlier Qwen 1.8%, conflict 41%); the right focuses on v2 at RecIF topic-rate anchors 1.6%/3.6%. It compares the assumed classifier α=0.8, β=0.02 with Qwen-versus-DeepSeek v2 rates α=4/5=0.8 and β=62/495≈0.1253. The CSV includes six classifier cases; there is no seed-based confidence band.

At the v2 1.0% reference and twice the odds, the assumed classifier requires 6,475 same-topic videos per arm, or 404,688 total exposures per arm at topic rate 1.6%. Using the v2 Qwen cross-check rates instead gives 33,070 and 2,066,875. Historical 1.4% and 1.8% anchors give 3,827 and 2,636 same-topic videos under the assumed classifier; the prompt-sensitive 0.6% value gives 15,185. Two newly collected arms double total exposures. These are exposure counts, not time estimates. The five v2 reference-positive videos give weak support for recall estimation; model agreement is not gold-standard accuracy, and its sampling uncertainty is not propagated. Autocorrelation and reference mismatch can also increase requirements. A nonpersonalized reference detects deviation from that mode, not absence of platform-wide amplification.

For a user-side tool with this Qwen error profile, false positives overwhelm the rare-narrative signal: the cross-check has 62 false positives against four true positives relative to DeepSeek. The required evidence is roughly five times the already-demanding assumed-classifier case. Detection would therefore be impractical for ordinary personal histories in this tested scenario; this is not a claim that every open-source classifier, or detection with improved labels, is impossible.

The full run generated 1,278,560 formation snapshots and 1,168,640 strategy snapshots. The compact public package retains all seed endpoints and complete summaries, with 65,520 raw formation snapshots and 971,520 strategy snapshots; dense raw traces are limited to plotted cases. Large files use gzip, with selection rules and hashes in the metadata. The audit verifies feedback, injection contrasts, zero contrast, identical formation/intervention starts and censoring. The [runtime screenshot](../screenshots/ruicong_calibrated_run.png) accompanies the actual audit stdout. Pilot-matching is a scale check; extrapolation to online controls, beliefs or causal user welfare remains unsupported.
<!-- END XU RUICONG SIMULATION -->
