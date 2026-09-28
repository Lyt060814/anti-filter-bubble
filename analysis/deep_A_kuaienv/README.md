# KuaiEnv trivial-policy runs (from deep dive A)

Scripts that load the original CIRS `KuaiEnv` environment (github.com/chongminggao/CIRS-codes) on CPU and run
simple non-learning policies (random, popularity, popularity + "skip if shares a category with the previous item").
The environment code itself and the rebuilt KuaiRec json files are NOT included here; they live in the CIRS repo /
KuaiRec data. See `docs/research/deep_dive/A_kuaishou_ustc_lineage.md` for how they were set up and what the results mean.
