## R4, rebuilt from current main

This PR now contains only the independent detection calculation and required figure/AI/contribution logs. It no longer brings R3 or obsolete simulation results into main.

Use Proposition 4's two-arm independent-sample normal approximation with one-sided significance .05 and power .8. Add the requested **1.4% DeepSeek v0** reference, retain historical 1.8% and conflict 41% anchors, and include the new 0.6% DeepSeek v1 value only as a prompt-sensitive comparison. Different model/prompt versions are explicitly identified; none is assumed to be ground truth.

At 1.4% prevalence and 2x odds, the formula gives 3,827 same-topic videos per arm, or 239,188 total exposures per arm at topic rate 1.6%. Both independently collected arms double the total. CSV contains 2,440 deterministic settings, including five assumed classifier cases and topic rates 1.6%/3.6%.

Metadata is now task-specific: no theta, recommendation coefficients, simulation seed population, intervention lengths or other irrelevant simulation defaults. No artificial random replicates or CI bands. PNG is 300 dpi with PDF counterpart and full numeric CSV.

The current v0/v1 Qwen classification checks are unreliable. Therefore alpha=.8 and beta=.02 remain assumptions, not D3 measurements. Await validated v2 before replacing them. Autocorrelation and classifier uncertainty are not captured by this approximation. No new data, GPU, credentials or direct push to main.
