Closes #21.

## L4-aligned main, with the earlier results preserved

- Keep topic target +.70; set main attribute target +.12 from Section 5.1. The refit gives t=.262674, c=.109545, c/t=.417036. The +1.13 and conflict pilot outputs are unchanged and explicitly upper/comparison scenarios.
- Re-run formation and S0/S1a/S1b/S3/S5/S6 under the same priors, horizons and four theta values, 20 seeds each. New gzip CSVs retain 9,760 formation snapshots and 3,840 strategy states/endpoints; figure includes a separate scale for direct output filtering.
- At theta=2 the main formation endpoint is V_sup=.05130, 95% seed-mean interval [.03892,.06368], versus .8120 in the old upper. These intervals condition on fixed calibration inputs and cannot establish that measured OneRec contrast differs from null.
- Independent zero-limit rerun matches existing c/t=0 case 14. Descriptive subtraction .12-.09229=.02771 is below the between-null-set SD .12658; existing ratio=.20 case 17 gives injection response .02760 and terminal skew about .01089. These bracket near-null sensitivity, not an empirical confidence interval.

Main selected endpoint changes at theta=2: S1a -.05760, S1b -.00898, S3 -.01478, S5 -.09199. S6 is -1.60847 under the assumed .8/.02 classifier because it directly filters output; it is not evidence of strong natural formation or feedback controllability. Long-run topic endpoints are constrained by caps, so the evidence for strong topic response comes from the L4 measurements/injection scale rather than an exaggerated narrative claim.

## Report and provenance

Only Xu's marked block in Section 5 changes; a scope check confirms Li Yitong's 5.1 and everything outside the markers are unchanged. Update the six-row table, main Formation text, upper-scenario captions, and Appendix B. Preserve the old formation figure in Appendix B and the older strategy/persistence plots as explicitly upper-scenario evidence. Leave 5.3's detection results intact.

Explain the NI point precisely: the previous .39/.78/1.17 target-response scan numerically includes ~40%, but L4's ~40% is relative to the watched column, whereas the older 78% is relative to neutral mention. They are not interchangeable update coefficients. The assigned +.5 arm is unchanged.

Validation: exact new injection contrast, all requested seed records, zero limit versus old scan, unchanged upper files, source hashes, 300-dpi PNG/PDF, all report image links and analysis size below 60 MB. New outputs use l4_main prefixes and carry measured-input hashes; no original numeric files are overwritten. AI/contribution/figure records appended. No data/GPU needed and no direct main push.
