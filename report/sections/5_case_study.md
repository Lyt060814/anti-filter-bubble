<!-- BEGIN XU RUICONG SIMULATION: material outside these markers belongs to other authors -->
## 5.2 Simulation: formation and escape

The pilot-matched scenarios show narrative skew growing while topic exposure stays similar. Controls differ in their effectiveness and collateral cost; these are conditional simulation results, not measured online-platform or belief changes.

We represent target-narrative videos A, other within-topic videos B, and four outside topics as six homogeneous groups. Recommendation is weighted softmax, π(i) ∝ wᵢ exp(u·vᵢ/τ). A/B share topic coordinate t and have supply-centred attribute coordinates c(1−s)/−cs, where s is A's supply share. Completion probability is σ(−1+1[topic]+θ1[A]); completion updates u, with forgetting and coordinatewise clipping. We calculate topic exposure m exactly. V_sup=log(π(A)/π(B))−log(s/(1−s)) is the **total skew of Section 3.2**, not personal skew relative to a platform population. Twenty seeds give pointwise 95% Monte Carlo intervals for means. Full methods and parameters are in [Appendix B](../../analysis/v6_simulation/appendix_b.md).

| Quantity | Main values and sensitivity | Evidence status |
|---|---|---|
| Injection targets | Topic +0.70; attribute +1.13/+0.65; NI response 78%; each target ±50% separately | Uncertain v5 OneRec pilot anchors; attribute labels were Qwen-based |
| Interest and supply | Initial topic 10%/15%/20%; A supply 2%/10%/50%; main .15/.02 | Assumed heavy-viewer scenarios, not supply estimates from exposure |
| Representation | c/t=0–1 plus .15/.59 and fitted 1.280/.971; η=τ=1 fixes units | Moment fit identifies only ηt²/τ and ηc²/τ |
| Response and memory | θ=0/.5/1/2; forgetting .0002, with .002 sensitivity; coordinate caps | Assumed; not OneRec's identified memory |
| Duration and replication | 6,000 formation, 1,000 active, 2,000 follow-up exposures; 20 seeds | Assumed design; counts are not elapsed time |
| Filtering | Benchmark recall/FPR .8/.02; v2 sensitivity .8/.1253 | Benchmark assumed; v2 is cross-model agreement, not gold-standard accuracy |

### Formation

Stronger attribute contrast permits substantial skew without losing the topic. At θ=2, main-scenario terminal V_sup is .0061 at c/t=.15, .1094 at .59, and .8120 at the fitted ratio (95% interval .6088–1.0152); mean m is .1516. Neutral-user skew is consistent with zero. The stable topic plateau partly follows from the clipping policy, not validated platform stability. Calibration reproduces pilot injection contrasts rather than actual OneRec histories; Qwen-labelled targets may be biased and need replacement by the forthcoming L4 replication.

![Calibrated formation](../../analysis/v6_simulation/figures/formation_calibrated.png)

**Figure F-R3-formation.** Synthetic group-label scenarios, supply .02 and prior .15. Time panels show selected ratios; the last row shows the full coefficient sweep. Bands are pointwise 95% Monte Carlo intervals.

### Escape

Ideal deletion and filtering produce the largest reductions, but their costs and assumptions differ. Arms are S0 natural behaviour; S1a negative NI/S1b positive-.5 NI; S2 skip A; S3 complete B; S4 search B; S5 delete surviving A contributions; S6 filter; S7 remove the topic; S8 serve the mean user state; S9 reset. Effort is not matched across arms; deletion assumes perfect labels and counts one bulk action.

At the fitted group-label ratio, S1a changes skew by −.7364 and S1b by +.0140; their paired difference is .7504 (95% interval .5991–.9018). A separate fit of the 78% NI response gives coefficient .7706 and skew change +.1098. Deletion reduces skew by 1.1788 with Δlog m=−.0084, versus 1.7833/−.0476 for benchmark filtering. A v2-classifier main-case rerun gives −1.6551/−.1453: filtering still lowers skew, but loses more topic exposure. This supplements, rather than replaces, the full-grid benchmark.

S3 does not reverse accumulated skew: ΔV_sup≈+.002, compared with +.102 under S0. Proposition 1 predicts a negative **local** B effect, but its contrast is −c²s versus c²(1−s) for A. At 2% supply, each B update carries only about 1/49 of A's attribute signal. Continued A feedback, clipping and forgetting limit cumulative escape. Ordinary B content is not a strongly opposed counter-narrative.

![Strategy comparison](../../analysis/v6_simulation/figures/escape_calibrated.png)

**Figure F-R3-escape.** Synthetic main-case endpoint effects at θ=2. Bars are pointwise 95% intervals. S7 has m=0 and undefined skew, so it is omitted. Filtering here uses the assumed benchmark classifier.

### Persistence

Output controls lose their direct effect on removal, while changed histories can persist. Both pre-intervention rebound and improvement relative to matched S0 are recorded. No initial improvement has an undefined half-life; improvement not halved within 2,000 follow-up exposures is right-censored. In the fitted main case, all 20 deletion runs improve over S0 initially and all remain censored; this is not an observed 2,000-exposure half-life or a claim about OneRec's finite history.

![Persistence](../../analysis/v6_simulation/figures/persistence_calibrated.png)

**Figure F-R3-persistence.** Difference from matched S0 after stopping. Output controls are removed before the first natural follow-up draw; preferences resume unchanged. Bands are pointwise 95% intervals.

## 5.3 Detectability

Rare-narrative detection is demanding, and false positives can overwhelm the signal. We use Proposition 6's independent two-arm approximation at significance .05 and power .8. With the v2 reference prevalence 1.0% and twice the odds, the assumed classifier needs 6,475 same-topic videos per arm, or 404,688 total exposures at topic rate 1.6%. The v2 Qwen error profile raises these to 33,070 and 2,066,875. Two newly collected arms double the totals.

![Detection requirements](../../analysis/v6_simulation/figures/detection_revised.png)

**Figure F-R4-revised.** Deterministic 2–8× odds scenarios. Left: v2 and historical prevalence anchors. Right: v2 under the assumed and Qwen-cross-check classifiers, at topic rates 1.6%/3.6%. There is no seed-based confidence band.

The cross-check has 62 false positives against four true positives relative to DeepSeek. At that error profile, ordinary personal histories provide far too little evidence for reliable detection in this scenario; this does not establish universal impossibility for open-source classifiers. Only five reference-positive samples support recall estimation, model agreement is not gold-standard accuracy, and rate uncertainty/autocorrelation are not propagated. A nonpersonalized reference also cannot reveal all platform-wide amplification.

All seed endpoints, summaries, compressed numeric files and provenance are retained. The [runtime screenshot](../screenshots/ruicong_calibrated_run.png) shows actual audit output. Appendix B documents the model, filtering convention (Proposition 3), calibration limits, censoring and reproduction.
<!-- END XU RUICONG SIMULATION -->
