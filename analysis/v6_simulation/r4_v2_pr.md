## R4 follow-up requested in #6 approval

Use new DeepSeek v2 prevalence as the main reference: 5/500 = 1.0%. Keep v0 1.4%, v1 0.6%, earlier 1.8% and conflict 41% as version-labelled sensitivity anchors. The right panel now focuses on the v2 reference.

Add the requested open-source-classifier case using Qwen relative to DeepSeek v2: TP=4, FP=62, FN=1, TN=433, no missing rows; recall=.8, false-positive rate=62/495=.12525. These are cross-model agreement rates, not gold-standard accuracy, and only five reference-positive cases support recall. Plug-in rates are treated as known in the approximation; their uncertainty is not propagated.

3,660 deterministic settings with six classifier cases. Raw data is read from existing main; only aggregate metrics are written in this task directory. No per-video labels/reasons copied or changes to Zhao Dingcheng's files. Source hashes and task-specific meta included.
