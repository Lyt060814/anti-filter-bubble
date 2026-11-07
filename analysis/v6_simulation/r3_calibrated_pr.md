## R3 after merged R2: calibrated formation, escape and persistence

Rebuilt from main after #4, and synchronized groupmates' newer main including merged #6. This PR contains R3 artifacts, not the R5 report. Earlier uncalibrated R3 data is superseded.

### Calibration requested in the R2 approval

Fit the synthetic injection contrasts to the v5 pilot: topic log-exposure ratio +0.70; A-vs-B log-odds response +1.13 (group labels) / +0.65 (conflict). Topic context is an assumed 15% prior, with 10 mean-topic injections compared to 10 outside injections split 3/3/2/2. Attribute contrast compares 10 A against 10 B. These are moment fits to uncertain repository-reported anchors, not a new OneRec measurement or external validation. The Qwen-labelled v5 targets may be biased; replaceable inputs and one-at-a-time x0.5/x1.5 scans are included.

Only eta*t^2/tau and eta*c^2/tau are identified. eta=tau=1 fixes units, not measured feedback strength. Fitted c/t is 1.280 for group labels and 0.971 for conflict; both fitted points are included alongside the full 0–1 coefficient grid and .15/.59 geometry reference locations. Measured embedding geometry and generating coefficients are different quantities.

The prior 0.75 global norm projection suppresses all rare attribute updates when topic activity hits the bound. To retain the calibrated injection scale without letting topic logits grow without bound, this revision uses coordinatewise caps = 11 times the largest absolute item coordinate. Ten ordinary calibration injections remain interior. This memory/cap policy, forgetting 0.0002 (plus x10 sensitivity), homogeneous groups, gamma/a and population composition remain assumptions; please review this change explicitly. It is not claimed to be OneRec's memory mechanism.

Additional NI calibration matches positive response ratios .39/.78/1.17, retaining achieved responses/residuals. The 78% target fits an update coefficient 0.770619, demonstrating that response ratio is not update strength. The assigned S1b=+0.5 arm is preserved, with the fitted variant reported separately.

### Experiment and results

262 scenarios: both narrative families, supply 2%/10%/50%, initial topic priors 10%/15%/20%, 13 ratio-grid points plus fitted anchor, and four target/memory sensitivities per family plus stronger forgetting. Four theta values and 20 seeds per setting. Formation 6,000, active intervention 1,000, follow-up 2,000 exposures. Target sensitivity is one-at-a-time, not a full joint uncertainty distribution.

For group labels at supply=.02, prior=.15, theta=2, fitted ratio: terminal formation skew is 0.812 +/- 0.203 (pointwise 95% MC half-width). At r=.15 it is .00609; at r=.59, .1094. Mean topic exposure remains near .15. Skew uses the R2-approved **supply reference (total skew)**, not platform-referenced personal V.

| Arm | Implementation |
|---|---|
| S0 | Natural behaviour |
| S1a | On A, replace completion with -1 update |
| S1b | On A, replace completion with +0.5 update; fitted positive variant separately |
| S2 | On A, no completion update |
| S3 | Always complete encountered B |
| S4 | One extra completed B every 10 organic exposures |
| S5 | Once remove surviving A ledger, with all actual clipping factors; not counterfactual history replay |
| S6 | Expected class thinning (TPR .8, FPR .02), refill from remainder; parameters assumed pending validated v2 |
| S7 | Remove all topic output; m=0, V undefined |
| S8 | Serve fixed terminal mean u of 80 synthetic users (equal theta groups); not mean softmax probabilities |
| S9 | Reset state once |

At the main fitted group endpoint, S1a delta skew=-.736, S1b=+.014; paired difference .750 (95% CI .599–.902). The separately fitted NI variant increases skew by .110 +/- .082. Perfect-history deletion reduces skew by 1.179 with delta log m=-.00844; assumed-classifier filtering reduces by 1.783 with delta log m=-.0476. No effort-matched universal ranking is claimed. Skipping reduces by .295 with little topic loss. Removing a surviving A ledger can overshoot toward B; it is an idealized control.

### Persistence, evidence and checks

The full run produced 1,278,560 per-seed formation snapshots and 1,168,640 intervention snapshots. Following the data-volume review, the public package keeps **all seed endpoints and complete summaries**, with intermediate raw traces only for plotted cases: 65,520 formation and 971,520 intervention snapshots, plus all 461,120 half-life records. Large files use deterministic gzip (`.csv.gz`); existing snapshot cadence is 100 exposures (the review permits keeping only plotted cases). The entire analysis directory is **52.18 MB**, below 60 MB. Full uncompressed output is retained in a local sibling archive, excluded from Git. README gives regeneration and packaging commands; metadata records compression, cadence, retained cases, sizes and hashes.

This PR is rebuilt as a single clean snapshot from new main before pushing, so the main-visible commit ancestry does not contain the superseded 429 MB raw-data commits. Every figure retains corresponding numeric data and 300-dpi PNG/PDF. CSV readers, audit and replot tools accept the gzip package.

Both pre-intervention rebound and matched-S0 half-lives are stored. No initial reduction -> undefined; not halved by 2,000 -> explicit right censoring. Main fitted group S5: 20/20 initial reductions, all 20 still censored relative to matched S0. Filtering loses its direct output effect at switch-off; a history effect can remain. Effort is action counts, not comparable human time; bulk deletion counts once and needs perfect labels.

Audit passes: signed local feedback before clipping, exact calibration targets, zero-contrast invariance, identical formation/S0 starting states, S7 undefined-skew semantics, explicit censoring, PNG/PDF/source hashes. New run provenance preserves numerical commit separately from plotting commit. Required shared-file exceptions: figure registry, AI-use log and Xu contribution entries only. No main push or auto-merge.
