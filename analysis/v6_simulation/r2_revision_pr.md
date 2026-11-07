## R2 revised against the review

This branch is rebuilt from current main (0453323), containing the merged R1 and groupmates' D1–D5 work. It contains only the revised R2 simulation and expressly required figure/AI/contribution log entries. It excludes R3–R5 and their obsolete conclusions.

1. **Bound interest:** project u onto the radius-0.75 ball after each update. Use a fixed 4% prior topic mass as an explicit synthetic scenario. All 190,320 saved snapshots remain within 2%–20% topic exposure. An analytic upper bound for natural positive updates is below 20% across c/t=0–1. This is scenario design, not calibration to RecIF's measured median 1.6% / p90 3.6%.
2. **Reference:** select the reviewer's permitted supply-reference alternative. The metric is now explicitly **V_supply = total skew relative to supply**, not personal skew relative to the platform population. No four-person population average is used. This model cannot separate global amplification and personal skew; report integration must retain that limitation.
3. **Supply:** scan 2%, 10%, 50%, main figure 2%. DeepSeek v0's 1.4% is exposure prevalence, not a measured supply proportion; it motivates a rare-attribute scenario but does not identify supply. The six homogeneous vector groups exactly aggregate identical-within-group items. Nuisance is zero in this transparent revision.
4. **Readable figures:** m_t and V_supply versus time with pointwise 95% Monte Carlo bands, and a separate mean-only (m,V_supply) plane. No cross-shaped error bars.

Full grid: 13 generating coefficient ratios including .15 and .59, four theta values, 20 seeds, three supplies, 1,200 steps. Per-seed snapshots, endpoint means/intervals, 300-dpi PNG, PDF and provenance are saved. The measured geometric ratio and generating c/t remain different quantities.

Checks: c=0 invariance; signed first-order feedback before projection; norm bound and topic-range assertions on every step. Projection changes the derivative at the boundary, so the unprojected Proposition 2 formula is not claimed to hold there.

## Review dependencies

Important result: with rare A supply (2%), symmetric +c/-c attribute updates are dominated by frequent B interactions. The assumed theta range need not overcome that imbalance: the main trajectories drift toward B rather than amplify A. This is a substantive model limitation/counterexample, not a failed check to tune away. The 50% supply sensitivity separates this count imbalance from preference effects. We must not retain the earlier unconditional conclusion that positive theta guarantees A amplification. Please review whether exposure-centred attribute updates or an explicitly calibrated response model would be more appropriate before extending this model to R3.

Please review/merge R2 first. R3 (#3), R4 (#6), R5 (#7) still contain outdated results and must not be merged yet. After R2 is merged they need separate clean branches from new main; rerun R3, add p0=1.4% and task-specific metadata to R4, and rewrite R5 from corrected results. No automatic merge or main push.
