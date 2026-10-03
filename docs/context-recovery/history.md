# 提交历史恢复

基线 `64b14d461adb71c3b94d49f7fcc855efa8b60efb`；全部 30 个 commit。下表转换为北京时间；原始时区可在 git 中查询。

| Commit | 北京时间 | 说明 |
|---|---|---|
| `a3cd594` | 2026-09-28 06:38:59 | Initial commit |
| `d2985e0` | 2026-09-28 06:49:02 | Add Chinese summary of project and project-plan requirements |
| `c3cae6d` | 2026-09-28 06:55:02 | Add research notes on regulation, platform anti-cocoon features, news and HK context |
| `060e6f7` | 2026-09-28 06:55:18 | Add research notes on simulation models, datasets and existing anti-bubble tools |
| `9f5f813` | 2026-09-28 06:55:44 | Add core filter-bubble / information-cocoon literature notes |
| `20f75c3` | 2026-09-28 07:00:23 | Add topic candidates, research index/checklist, audit notes and Project Plan draft |
| `c1b29fe` | 2026-09-28 07:32:14 | Add solution-side resource inventory (anti-cocoon algorithms, interventions, tools) |
| `f3c018c` | 2026-09-28 07:42:24 | Add second-round resource inventory, X code map, and KuaiRec quick-look script |
| `fc3f2c8` | 2026-09-28 08:00:24 | Add notes on KuaiRec/KuaiRand origins and prior filter-bubble research using them |
| `c9f658f` | 2026-09-28 09:55:10 | Add deep dive on Tsinghua information-cocoon research lineage |
| `465a2e8` | 2026-09-28 09:57:29 | Add Kuaishou/USTC lineage deep dive and KuaiRand/KuaiEnv exploratory analyses |
| `3823416` | 2026-09-28 10:00:13 | Add simulation/audit deep dive with yaudit re-analysis, T-RECS and NDlib demos |
| `99bde6c` | 2026-09-28 10:19:11 | Add escape/user-control deep dive and cross-lineage gap synthesis |
| `988ddfb` | 2026-09-28 10:53:50 | Add detection pilot on KuaiRec (screen-visible vs platform early-warning signals) |
| `b155e52` | 2026-09-28 10:54:59 | Add verified APA reference list for the Project Plan |
| `1b09eb0` | 2026-09-28 11:02:26 | Add X-like escape simulator pilot (code, results, figures) |
| `fdece73` | 2026-09-28 11:08:15 | Add complete Project Plan (Markdown, Word, PDF) for the detect-and-escape question |
| `20cf0c9` | 2026-10-01 22:06:50 | Add .gitignore for Python caches and derived parquet data |
| `a1d39b7` | 2026-10-01 22:21:54 | Update X code map and Project Plan to x-algorithm commit b79b947 (2026-10-01) |
| `2161da2` | 2026-10-02 11:42:50 | Add data feasibility checks: ShortVideo profile, category alignment, embeddings, compute, off-interest acceptance, LLM benchmark |
| `95153b7` | 2026-10-02 12:01:55 | Add small LLM-user pilots (DeepSeek flash) on ShortVideo and KuaiRand random exposures |
| `061709e` | 2026-10-02 12:10:41 | Parameterise LLM pilot 2 by model and thinking mode; add variant comparison script |
| `f53b34f` | 2026-10-02 12:25:11 | Add pro and flash-thinking LLM pilot results (150 KuaiRand users each) and variant comparison |
| `1974316` | 2026-10-02 12:27:08 | Map X value-model heads to Kuaishou fields and tabulate user-side levers |
| `0db0bda` | 2026-10-02 12:39:22 | Add pro+thinking LLM pilot and full variant comparison to data-check report |
| `26fd0c4` | 2026-10-02 12:39:30 | Fix balance wording in data-check report |
| `f3db48e` | 2026-10-02 13:49:31 | Add working plan v1: reframe project around sampling/preference harms, mirror-buttons-cost questions, resource audit |
| `9b8ca6d` | 2026-10-02 14:02:40 | Working plan: add second-round sources (TikTok/YouTube control audits, relapse, Douyin mirror facts, MicroLens) and reframe Q2 |
| `4cba338` | 2026-10-02 15:17:04 | Working plan: add deep-research outcome (verified Q1 resources, unverified Q2/Q3 leads, gaps) |
| `64b14d4` | 2026-10-02 15:31:32 | Add execution plan v1: resource-grounded work packages, deviations from ideal, timeline, roles |

## 每次改动的文件

### a3cd594 — Initial commit

```text
A	README.md
```

### d2985e0 — Add Chinese summary of project and project-plan requirements

```text
A	docs/00_requirements_summary.md
```

### c3cae6d — Add research notes on regulation, platform anti-cocoon features, news and HK context

```text
A	docs/research/C_regulation_platforms_news_HK.md
```

### 060e6f7 — Add research notes on simulation models, datasets and existing anti-bubble tools

```text
A	docs/research/D_models_datasets_tools.md
```

### 9f5f813 — Add core filter-bubble / information-cocoon literature notes

```text
A	docs/research/A_core_literature.md
```

### 20f75c3 — Add topic candidates, research index/checklist, audit notes and Project Plan draft

```text
M	README.md
A	docs/01_topic_candidates.md
A	docs/project-plan/project_plan_draft.md
A	docs/research/B_audits_escape_metrics.md
A	docs/research/README.md
```

### c1b29fe — Add solution-side resource inventory (anti-cocoon algorithms, interventions, tools)

```text
A	docs/resources/solutions_anti_cocoon_methods.md
```

### f3c018c — Add second-round resource inventory, X code map, and KuaiRec quick-look script

```text
M	README.md
A	analysis/kuairec_quicklook.py
A	docs/resources/README.md
A	docs/resources/code_simulators_disclosures.md
A	docs/resources/datasets.md
A	docs/resources/personal_data_surveys_local_ethics.md
A	docs/resources/x_algorithm_code_map.md
A	docs/resources/x_algorithm_prior_analyses.md
```

### fc3f2c8 — Add notes on KuaiRec/KuaiRand origins and prior filter-bubble research using them

```text
A	docs/resources/kuai_citations.json
A	docs/resources/kuai_datasets_prior_research.md
```

### c9f658f — Add deep dive on Tsinghua information-cocoon research lineage

```text
A	docs/research/deep_dive/B_tsinghua_cocoon_lineage.md
```

### 465a2e8 — Add Kuaishou/USTC lineage deep dive and KuaiRand/KuaiEnv exploratory analyses

```text
A	analysis/deep_A_kuaienv/README.md
A	analysis/deep_A_kuaienv/kuaienv_trivial_results.csv
A	analysis/deep_A_kuaienv/kuaienv_trivial_results.txt
A	analysis/deep_A_kuaienv/kuaienv_trivial_results_len30.csv
A	analysis/deep_A_kuaienv/kuaienv_trivial_results_len30.txt
A	analysis/deep_A_kuaienv/run_kuaienv_trivial.py
A	analysis/deep_A_kuaienv/run_len30.py
A	analysis/deep_A_kuairand_kuairec/hate_followup.out
A	analysis/deep_A_kuairand_kuairec/hate_followup.py
A	analysis/deep_A_kuairand_kuairec/kuairand_concentration.out
A	analysis/deep_A_kuairand_kuairec/kuairand_concentration.py
A	analysis/deep_A_kuairand_kuairec/kuairand_pure_stats.out
A	analysis/deep_A_kuairand_kuairec/kuairand_pure_stats.py
A	analysis/deep_A_kuairand_kuairec/kuairec_stats.out
A	analysis/deep_A_kuairand_kuairec/kuairec_stats.py
A	docs/research/deep_dive/A_kuaishou_ustc_lineage.md
```

### 3823416 — Add simulation/audit deep dive with yaudit re-analysis, T-RECS and NDlib demos

```text
A	analysis/deep_D/ndlib_demo/abm.py
A	analysis/deep_D/ndlib_demo/out.txt
A	analysis/deep_D/trecs_demo/demo.py
A	analysis/deep_D/trecs_demo/demo_output.txt
A	analysis/deep_D/yaudit_reanalysis/S1_E1_E2_table.csv
A	analysis/deep_D/yaudit_reanalysis/bubble_curves.png
A	analysis/deep_D/yaudit_reanalysis/reanalyse.py
A	analysis/deep_D/yaudit_reanalysis/rec_top10_curve_manual_labels.csv
A	docs/research/deep_dive/D_simulation_models_audits.md
```

### 99bde6c — Add escape/user-control deep dive and cross-lineage gap synthesis

```text
A	docs/research/deep_dive/C_escape_user_control.md
A	docs/research/deep_dive/README.md
```

### 988ddfb — Add detection pilot on KuaiRec (screen-visible vs platform early-warning signals)

```text
A	analysis/pilot_detect/01_prep_kuairec.out
A	analysis/pilot_detect/01_prep_kuairec.py
A	analysis/pilot_detect/02_kuairec_userday.py
A	analysis/pilot_detect/03_describe.py
A	analysis/pilot_detect/03_describe_kuairec.out
A	analysis/pilot_detect/03_describe_kuairec_mw90.out
A	analysis/pilot_detect/05_eval_kuairec.out
A	analysis/pilot_detect/05_eval_kuairec_mw90.out
A	analysis/pilot_detect/05_evaluate.py
A	analysis/pilot_detect/06_extra.out
A	analysis/pilot_detect/06_extra.py
A	analysis/pilot_detect/07_figures.py
A	analysis/pilot_detect/cat_names.csv
A	analysis/pilot_detect/detect_lib.py
A	analysis/pilot_detect/fig1_auc_comparison.png
A	analysis/pilot_detect/fig2_lead_time.png
A	analysis/pilot_detect/fig3_events_by_day_and_example.png
A	analysis/pilot_detect/kuairec_eval_results.csv
A	analysis/pilot_detect/kuairec_eval_summary.json
A	analysis/pilot_detect/kuairec_info.json
A	analysis/pilot_detect/kuairec_mw90_eval_results.csv
A	analysis/pilot_detect/kuairec_mw90_eval_summary.json
A	analysis/pilot_detect/kuairec_mw90_info.json
A	analysis/pilot_detect/pilot_detect_report.md
```

### b155e52 — Add verified APA reference list for the Project Plan

```text
A	docs/project-plan/references_verified.md
```

### 1b09eb0 — Add X-like escape simulator pilot (code, results, figures)

```text
A	analysis/pilot_sim/fig1_seed_share_curves.png
A	analysis/pilot_sim/fig1b_ni_variants.png
A	analysis/pilot_sim/fig2_escape_cost.png
A	analysis/pilot_sim/fig3_ablation.png
A	analysis/pilot_sim/fig4_calibration.png
A	analysis/pilot_sim/pilot_sim_report.md
A	analysis/pilot_sim/results.json
A	analysis/pilot_sim/results.txt
A	analysis/pilot_sim/run_experiments.py
A	analysis/pilot_sim/sim.py
```

### fdece73 — Add complete Project Plan (Markdown, Word, PDF) for the detect-and-escape question

```text
M	README.md
A	docs/project-plan/Project_Plan.docx
A	docs/project-plan/Project_Plan.pdf
A	docs/project-plan/archive/project_plan_draft_v0_xiaohongshu.md
A	docs/project-plan/build_docx.js
A	docs/project-plan/project_plan.md
D	docs/project-plan/project_plan_draft.md
```

### 20cf0c9 — Add .gitignore for Python caches and derived parquet data

```text
A	.gitignore
```

### a1d39b7 — Update X code map and Project Plan to x-algorithm commit b79b947 (2026-10-01)

```text
M	docs/project-plan/Project_Plan.docx
M	docs/project-plan/Project_Plan.pdf
M	docs/project-plan/project_plan.md
M	docs/project-plan/references_verified.md
M	docs/resources/README.md
M	docs/resources/x_algorithm_code_map.md
```

### 2161da2 — Add data feasibility checks: ShortVideo profile, category alignment, embeddings, compute, off-interest acceptance, LLM benchmark

```text
A	analysis/data_check/00_download.sh
A	analysis/data_check/01_shortvideo_profile.out
A	analysis/data_check/01_shortvideo_profile.py
A	analysis/data_check/02_category_alignment.out
A	analysis/data_check/02_category_alignment.py
A	analysis/data_check/03_text_embeddings.out
A	analysis/data_check/03_text_embeddings.py
A	analysis/data_check/04_compute_bench.out
A	analysis/data_check/04_compute_bench.py
A	analysis/data_check/05_offinterest_acceptance.out
A	analysis/data_check/05_offinterest_acceptance.py
A	analysis/data_check/06_llm_benchmark_prep.out
A	analysis/data_check/06_llm_benchmark_prep.py
A	analysis/data_check/README.md
A	analysis/data_check/category_map_l1.csv
A	analysis/data_check/common.py
```

### 95153b7 — Add small LLM-user pilots (DeepSeek flash) on ShortVideo and KuaiRand random exposures

```text
M	analysis/data_check/06_llm_benchmark_prep.py
A	analysis/data_check/07_llm_pilot.out
A	analysis/data_check/07_llm_pilot.py
A	analysis/data_check/07_llm_pilot_per_user_gauc.csv
A	analysis/data_check/08_llm_pilot_kuairand.out
A	analysis/data_check/08_llm_pilot_kuairand.py
A	analysis/data_check/08_llm_pilot_kuairand_per_user_gauc.csv
M	analysis/data_check/README.md
```

### 061709e — Parameterise LLM pilot 2 by model and thinking mode; add variant comparison script

```text
M	analysis/data_check/08_llm_pilot_kuairand.out
M	analysis/data_check/08_llm_pilot_kuairand.py
D	analysis/data_check/08_llm_pilot_kuairand_per_user_gauc.csv
A	analysis/data_check/08_llm_pilot_kuairand_per_user_gauc_flash.csv
A	analysis/data_check/08_llm_pilot_kuairand_per_user_gauc_flash_think-high.csv
A	analysis/data_check/08_llm_pilot_kuairand_per_user_gauc_flash_think-low.csv
A	analysis/data_check/08_llm_pilot_kuairand_per_user_gauc_pro.csv
A	analysis/data_check/08_llm_pilot_kuairand_per_user_gauc_pro_think-high.csv
A	analysis/data_check/08_llm_pilot_kuairand_per_user_gauc_pro_think-low.csv
A	analysis/data_check/09_llm_variants_compare.py
```

### f53b34f — Add pro and flash-thinking LLM pilot results (150 KuaiRand users each) and variant comparison

```text
M	analysis/data_check/08_llm_pilot_kuairand_per_user_gauc_flash_think-low.csv
M	analysis/data_check/08_llm_pilot_kuairand_per_user_gauc_pro.csv
A	analysis/data_check/09_llm_variants_compare.out
A	analysis/data_check/09_llm_variants_per_user_gauc.csv
```

### 1974316 — Map X value-model heads to Kuaishou fields and tabulate user-side levers

```text
A	analysis/data_check/x_mapping_and_levers.md
```

### 0db0bda — Add pro+thinking LLM pilot and full variant comparison to data-check report

```text
M	analysis/data_check/08_llm_pilot_kuairand_per_user_gauc_pro_think-low.csv
A	analysis/data_check/08_llm_pilot_kuairand_pro_think-low.out
M	analysis/data_check/09_llm_variants_compare.out
M	analysis/data_check/09_llm_variants_per_user_gauc.csv
M	analysis/data_check/README.md
```

### 26fd0c4 — Fix balance wording in data-check report

```text
M	analysis/data_check/README.md
```

### f3db48e — Add working plan v1: reframe project around sampling/preference harms, mirror-buttons-cost questions, resource audit

```text
A	docs/project-plan/working_plan_v1.md
```

### 9b8ca6d — Working plan: add second-round sources (TikTok/YouTube control audits, relapse, Douyin mirror facts, MicroLens) and reframe Q2

```text
M	docs/project-plan/working_plan_v1.md
```

### 4cba338 — Working plan: add deep-research outcome (verified Q1 resources, unverified Q2/Q3 leads, gaps)

```text
M	docs/project-plan/working_plan_v1.md
```

### 64b14d4 — Add execution plan v1: resource-grounded work packages, deviations from ideal, timeline, roles

```text
A	docs/project-plan/execution_plan_v1.md
```
