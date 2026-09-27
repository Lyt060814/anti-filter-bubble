# Resource inventory: open-source code, simulators and platform algorithm disclosures

**Project:** HKU COMP1110 group project on information cocoons / filter bubbles (信息茧房)
**Compiled:** 2026-09-27
**Excluded:** `xai-org/x-algorithm`, which another agent covers.

## How this was checked

- **GitHub metadata** (language, licence, `pushed_at` = last code push, archived flag) comes from the GitHub search API during this session.
- **Licences** were cross-checked by fetching each repo's `LICENSE` file from raw.githubusercontent.com.
- **Code facts** (metric names, weights, formulas) were read from raw source files and READMEs.
- **Non-GitHub pages** (TikTok, CAC, Meta, arXiv, Zenodo) were blocked by the network proxy. Facts about them come from search-result snippets. Anything not confirmed first-hand is marked **UNVERIFIED**.
- **"Last push"** is the date of the last commit push. **"Activity"** means the repo was only touched (for example, starred) recently, which says nothing about maintenance.
- **Difficulty** is for first-year students using laptops or Colab:
  - **Easy:** read it, or `pip install` and a notebook in under a day.
  - **Med:** a few days, some Python/pandas.
  - **Hard:** needs GPUs, a large codebase, or deep ML.

---

## 1. Real platform recommender code and disclosures

### 1a. Open-source production ranking code

| # | Name | URL | Language | Licence | Status | Difficulty | How our project could use it |
|---|---|---|---|---|---|---|---|
| 1 | **twitter/the-algorithm** (2023 X/Twitter "For You" release) | https://github.com/twitter/the-algorithm | Scala (plus Java, Python, Rust) | AGPL-3.0 | Not archived. Last push 2025-09-08. Created 2023-03-27. About 74k stars. | Hard to run, Easy/Med to read | Read the README component map (SimClusters, real-graph, light ranker, home-mixer, visibility-filters) to explain the pipeline: candidate generation → ranking → filtering. **Compare the 2023 structure with the 2026 x-algorithm.** |
| 2 | **twitter/the-algorithm-ml** (heavy ranker and TwHIN) | https://github.com/twitter/the-algorithm-ml ; weights table at https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md | Python (PyTorch) | AGPL-3.0 | Last push 2024-07-10 (inactive) | Easy (weights table) / Hard (model) | See the weights table below. **Use it as the baseline for "2023 vs 2026 X ranking weights"** and to discuss how much a "not interested" signal counts. |
| 3 | **igorbrigadir/awesome-twitter-algo** (annotated guide to the 2023 release) | https://github.com/igorbrigadir/awesome-twitter-algo | Markdown | Not checked | Created 2023-04 (last push not checked) | Easy | A beginner-friendly map of the 2023 code. Saves hours of reading Scala. |
| 4 | **X Community Notes**: open-source bridging algorithm, docs and research paper | Code: https://github.com/twitter/communitynotes (scoring in `/scoring/src`, paper `birdwatch_paper_2022_10_27.pdf`). Docs: https://communitynotes.x.com/guide/en/under-the-hood/note-ranking-code | Python | Apache-2.0 | **Active: last push 2026-09-21.** About 1.9k stars. | Med | Canonical example of **bridging-based ranking**. Matrix factorisation separates a "viewpoint" factor from a note's helpfulness intercept, so only notes rated helpful across viewpoints are shown. **Use it as an anti-polarisation example.** A simplified version runs on a sample of the data. |
| 5 | **Community Notes public data** (notes, ratings, status history as TSV) | https://communitynotes.x.com/guide/en/under-the-hood/download-data (download page: https://x.com/i/communitynotes/download-data) | TSV | Data is public (terms UNVERIFIED) | Updated continuously | Med (files are large) | README-documented workflow: put the TSVs next to the code and run `python main.py` to reproduce production note scores. **Measure how often notes reach "helpful" across viewpoints.** A helper R package: https://github.com/colin-fraser/communitynotes |
| 6 | **Reddit "hot" ranking** (historical open-source reddit) | https://github.com/reddit-archive/reddit/blob/master/r2/r2/lib/db/_sorts.pyx | Python/Cython | CPAL-1.0 | Archived | Easy | Verified formula: `sign*log10(max(|ups-downs|,1)) + (date-1134028003)/45000`. A **non-personalised popularity + recency** ranker to contrast with personalised feeds. It is what "everyone sees the same front page" looks like. |
| 7 | **Hacker News ranking** (Arc `news.arc`) | Analyses: http://www.righto.com/2009/06/how-does-newsyc-ranking-work.html and https://www.righto.com/2013/11/how-hacker-news-ranking-really-works.html. Alternative open ranker: https://github.com/social-protocols/quality-news | Arc (Lisp) | Arc source licence not checked | Formula from 2009; penalties since then are partly hidden | Easy | `score = (P-1)/(T+2)^1.8`. A second non-personalised baseline; the 1.8 "gravity" is easy to tweak in a simulation. |
| 8 | **ByteDance Monolith** (TikTok's real-time training infrastructure) | Code: https://github.com/bytedance/monolith. Paper: https://arxiv.org/abs/2209.07663 (ORSUM@RecSys 2022) | Python (plus C++) | "Other" (non-standard) | **Archived.** Last push 2025-10-13. About 9.3k stars. | Hard | It is **infrastructure** (collisionless embedding tables, online training), **not TikTok's ranking policy**. Use it only to explain *why* TikTok adapts within minutes: real-time training on fresh feedback makes cocoons form fast. Do not claim it is "TikTok's algorithm". |
| 9 | **Bluesky feed-generator** (official AT Protocol custom-feed starter kit) | https://github.com/bluesky-social/feed-generator | TypeScript | MIT | **Active: last push 2026-09-25.** About 2.1k stars. | Med | Shows **"algorithmic choice"**: anyone can publish a feed and users pick one. Use it as an example of a structural anti-cocoon solution. |
| 10 | **MarshalX/bluesky-feed-generator** (Python version of 9) | https://github.com/MarshalX/bluesky-feed-generator | Python | MIT | Last push not checked | Med | A Python route if the team wants to deploy a toy "diverse feed" on Bluesky. Optional stretch goal. |
| 11 | **spacecowboy's "For You" Bluesky feed**: write-up of a real personalised third-party feed | https://atproto.com/blog/serving-the-for-you-feed ; https://simonwillison.net/2026/Apr/24/serving-the-for-you-feed/ | Go + SQLite (per the write-up) | Code release **UNVERIFIED** (no public repo found) | Write-up from April 2026 | Easy (reading) | A simple collaborative-filtering logic: "people who liked what you liked also liked…". About 72k users, served from one home PC. **A clean, explainable example of how a cocoon can form.** |
| 12 | **Mastodon** (chronological home timeline; trends module) | https://github.com/mastodon/mastodon (trends code at `app/models/trends/statuses.rb`, confirmed to exist) | Ruby | AGPL-3.0 | Active | Med (reading Ruby) | A contrast case: no engagement-ranked home feed. Only the "trending" surfaces are algorithmic. Useful for a "chronological vs algorithmic" comparison. |
| 13 | **Kuaishou OneRec / OneRec-V2 / OpenOneRec** | Papers: https://arxiv.org/abs/2506.13695 , https://arxiv.org/abs/2508.20900 , https://arxiv.org/abs/2512.24762. Code/data: https://github.com/Kuaishou-OneRec/OpenOneRec | Python | Apache-2.0 per README badge (no root LICENSE file found: **UNVERIFIED**) | 2025–2026 | Hard (1.7B/8B models) | Shows the 2025 industry shift to **end-to-end generative recommenders** optimised for "App Stay Time". OneRec reports +0.54% / +1.24% stay time. **Use it to discuss what the objective function rewards.** |
| 14 | **Xiaohongshu (RedNote) industrial paper**: "Towards Large-scale Generative Ranking" | https://arxiv.org/html/2505.04180v2 | Paper only | n/a | 2025 | Hard | Search snippets say it has online A/B tests on the Xiaohongshu Explore feed. The Xiaohongshu authorship claim is **UNVERIFIED** beyond those snippets. User-side study: https://arxiv.org/abs/2501.18210 (CHI 2025, hashtag re-appropriation to steer the RedNote algorithm). |
| 15 | **YouTube published recommender work** | Blog: https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/ (Goodrow, 2021-09-15). Paper: https://research.google/pubs/recommending-what-video-to-watch-next-a-multitask-ranking-system/ (RecSys 2019, MMoE multi-objective ranking) | Prose / paper | n/a | 2019–2021 | Easy (blog) / Med (paper) | The blog discusses filter bubbles and "authoritative" boosting. The paper shows multi-objective ranking (engagement + satisfaction). Covington et al. 2016, "Deep Neural Networks for YouTube Recommendations", is the classic, but its URL was not verified in this session. |

**X 2023 heavy-ranker weights**, verbatim from the-algorithm-ml README, dated April 5, 2023:

| Signal | Weight |
|---|---|
| fav | 0.5 |
| retweet | 1.0 |
| reply | 13.5 |
| good_profile_click | 12.0 |
| video_playback50 | 0.005 |
| reply_engaged_by_author | 75.0 |
| good_click | 11.0 |
| good_click_v2 | 10.0 |
| **negative_feedback_v2** | **-74.0** |
| report | -369.0 |

The README says the weights were set so that each weighted engagement probability contributes "a near-equal amount" to the score, and have been "periodically adjusted to optimize for platform metrics".

### 1b. Platform disclosures (prose, no code)

| # | Name | URL | Type | Status | Difficulty | How our project could use it |
|---|---|---|---|---|---|---|
| 16 | **Meta AI system cards** (22 cards: 14 Facebook, 8 Instagram) and "Explaining ranking" | https://ai.meta.com/tools/system-cards/ ; https://transparency.meta.com/features/explaining-ranking/ ; FB Feed card: https://transparency.meta.com/features/explaining-ranking/fb-feed/ ; announcement: https://ai.meta.com/blog/how-ai-powers-experiences-facebook-instagram-system-cards/ | Web pages | June 2023, updated since (UNVERIFIED) | Easy | Lists the prediction signals (probability of like, comment, share, etc.) and user controls. Pair it with the critique https://www.mozillafoundation.org/en/blog/this-is-not-a-system-card-scrutinising-metas-transparency-announcements/ ("disclosure ≠ accountability"). |
| 17 | **Instagram "Your Algorithm"** (Dec 2025): AI summary of your interest topics, which you can boost, mute or add to | https://about.instagram.com/blog/announcements/reels-algorithm-control ; https://techcrunch.com/2025/12/10/instagrams-new-your-algorithm-tool-gives-you-more-control-over-the-reels-you-see | Product feature | Launched 2025-12-10 in the US; extended to Explore/Feed later (per announcements) | Easy | The newest mainstream **"anti-cocoon control"** to evaluate. Compare it with "Not interested" (see audit #44). A small self-test is possible: log Reels topics before and after changing the settings. |
| 18 | **TikTok "Introduction to the TikTok recommendation system"** | https://www.tiktok.com/transparency/en-us/recommendation-system/ ; https://www.tiktok.com/creator-academy/article/guidelines-recommendation-system-intro | Web pages | Current (page not fetchable here) | Easy | Per search snippets, TikTok states that if consecutive videos are too similar, some are replaced to add variety. **That is a claimed anti-cocoon diversity rule you could simulate.** |
| 19 | **TikTok EU DSA measures**: non-personalised FYP (Aug 2023) and DSA Risk Assessment Report 2025 | https://newsroom.tiktok.com/en-eu/fulfilling-commitments-dsa-update ; report PDF: https://sf16-va.tiktokcdn.com/obj/eden-va2/zayvwlY_fjulyhwzuhy%5B/ljhwZthlaukjlkulzlp/DSA/DSARiskAssessmentReport-TikTokTechnologyLimited-2025.pdf | PDF / web | 2025 report (dated 28 Aug 2025 per snippet) | Med (long PDF) | The report discusses recommender-system risks ("rabbit hole"). **Compare the EU non-personalised option with the controls in HK/China.** Analysis: https://kgi.georgetown.edu/research-and-commentary/measuring-risk-what-eu-risk-assessments-and-us-litigation-reveal-about-meta-and-tiktok/ |
| 20 | **X DSA Systemic Risk Assessment 2025** (summary) | https://transparency.x.com/content/dam/transparency-twitter/dsa/2025-x-dsa-sra-summary-report.pdf | PDF | 2025 | Med | Cross-check what X tells the EU against its open-source code (#1, #2, and x-algorithm). |
| 21 | **EU DSA Transparency Database** (statements of reasons for moderation decisions) plus its source code | Data: https://transparency.dsa.ec.europa.eu/data-download ; search: https://transparency.dsa.ec.europa.eu/statement-search ; code: https://github.com/digital-services-act/transparency-database | Daily CSV/Parquet; PHP app | Active. Snippets mention a Python helper `dsa-tdb` and a Research API. | Med | Covers **moderation, not ranking**, but gives real volumes of "visibility restriction/demotion" decisions per platform. Could support a "demotion as hidden ranking" slide. Article 27 text (recommender "main parameters" plus the option to change them): https://dsa-library.com/article/27/ |
| 22 | **Douyin 安全与信任中心** (Safety & Trust Center, launched 2025-03-30), which publishes recommendation-algorithm principles | Site 95152.douyin.com (per news; not fetched). News: https://www.guancha.cn/economy/2025_03_31_770341.shtml ; https://cn.wicinternet.org/2025-03/31/content_37940458.htm ; follow-up conference (2026-01): http://www.news.cn/tech/20260122/04c02add69f94669bef9b6d80392a66c/c.html | Web (Chinese) | Launched 2025, still active in 2026 | Easy | Douyin describes neural nets estimating the probability of each action (like, follow, share, comment…) with multi-objective modelling, plus diversity mechanisms. **The best Chinese-platform primary source; compare it with the X weights.** |
| 23 | **China CAC algorithm filing (互联网信息服务算法备案)** | First batch announcement (2022-08-12, 30 algorithms): https://www.cac.gov.cn/2022-08/12/c_1661927474338504.htm ; query system https://beian.cac.gov.cn (blocked here). English list: https://www.chinalawtranslate.com/algorith-listing/ ; secondary summaries: https://www.secrss.com/articles/45815 , https://tech.p2hp.com/archives/342 | Government lists | Batches from 2022 onward | Easy/Med | See the note below this table. |

**What the CAC filing lists contain.** The published *清单* are tables of platform, algorithm name, service and filing number. Per secondary sources, each algorithm's public entry in the filing system (公示内容) carries a short description of its basic principle and operating mechanism (算法基本原理/运行机制); this is **UNVERIFIED**, because the query system could not be opened here. A secondary summary quotes Douyin's filed recommendation algorithm as having an **"兴趣探索" (interest exploration)** mechanism:

- each recommendation includes some share of categories the user rarely watches, and
- one random item is added per request "to ensure diversity".

**UNVERIFIED primary text.** The descriptions are short and non-quantitative. Search snippets also mention Xiaohongshu features such as "内容偏好评估和调整" and "探索更多" (source attribution **UNVERIFIED**). **Use:** turn "X% out-of-profile + 1 random item" into a policy in your simulator, and test whether it actually breaks the cocoon.

---

## 2. Recommender simulation and evaluation frameworks

| # | Name | URL | Language | Licence | Status | Difficulty | How our project could use it |
|---|---|---|---|---|---|---|---|
| 24 | **T-RECS** (Tool for RecSys Simulation; Princeton) | https://github.com/elucherini/t-recs ; docs https://elucherini.github.io/t-recs/ | Python | MIT | Last push 2024-11-24 (low activity) | **Easy–Med** | Built for sociotechnical studies. Has built-in measurements: `InteractionSimilarity`, `RecSimilarity`, `InteractionSpread`, `StructuralVirality`, `AverageFeatureScoreRange`. **Run a 100-user cocoon simulation and plot homogenisation over time.** The team's best starting simulator. |
| 25 | **Google RecSim** | https://github.com/google-research/recsim | Python (TensorFlow 1-era) | Apache-2.0 | **Archived.** Last push 2022-01-03. | Hard (old TF, RL) | Has an `interest_evolution` environment (user interests drift with consumption). Cite it as the classic; the old dependencies make it hard on Colab. |
| 26 | **Google RecSim NG** | https://github.com/google-research/recsim_ng | Python / Jupyter (TF Probability) | Apache-2.0 | **Archived.** Last push 2022-04-26. | Hard | Multi-agent "ecosystem" simulation (users + creators). Mention only. |
| 27 | **KuaiSim** (Kuaishou-data user simulator, "KRLBenchmark") | https://github.com/Applied-Machine-Learning-Lab/KuaiSim | Python / PyTorch notebooks | Apache-2.0 | Last push 2024-09-10 | Med–Hard | The user-response model is trained on KuaiRand (click, like, "is_hate", long_view…). Shows **how industry simulates short-video users**; probably too heavy to extend. |
| 28 | **KuaiRec** (fully-observed Kuaishou dataset) | https://github.com/chongminggao/KuaiRec (homepage https://kuairec.com) | Data + notebooks | CC-BY-SA-4.0 | Last push 2026-01-06 | **Easy–Med** | A dense user×video watch-ratio matrix, so a recommender's picks can be scored against "true" preferences. **Use it as ground truth for a cocoon simulation on real short-video data.** |
| 29 | **KuaiRand** (randomly exposed videos) | https://github.com/chongminggao/KuaiRand | Data | CC-BY-SA-4.0 | Activity 2026 (last push not checked) | Easy–Med | Includes randomly inserted videos, the real-world analogue of Douyin's "random item". **Measure how users react to out-of-bubble content**, including negative "hate" feedback. |
| 30 | **CIRS** ("Bursting Filter Bubbles by Counterfactual Interactive Recommender System"; includes a KuaishouEnv) | https://github.com/chongminggao/CIRS-codes ; paper https://arxiv.org/pdf/2204.01266.pdf | Python / PyTorch | MIT | Last push 2024-01-02 | Hard | Its environment penalises filter bubbles (users leave when bored of repetition). **Borrow the idea "boredom → user leaves" for your own simulator.** |
| 31 | **UCRS** ("User-controllable Recommendation Against Filter Bubbles", SIGIR 2022) | https://github.com/WenjieWWJ/UCRS | Python | No licence file | Last push 2022-05-04 | Hard | Academic model of **user controls** (like "show me less of X") and why naive controls fail. Background for the "does 'not interested' work?" question. |
| 32 | **RecAgent / YuLan-Rec** (LLM-agent user simulation) | https://github.com/RUC-GSAI/YuLan-Rec | Python | MIT | Last push 2025-04-01 | Hard (needs LLM API credits) | The README says it simulates **(1) information cocoons and (2) user conformity**. Cite it as evidence; a mini-version is possible with a few LLM agents. |
| 33 | **SimTok** (LLM-agent simulation of short-video filter bubbles) | Paper: https://arxiv.org/abs/2504.08742 | n/a | **Public code not found (UNVERIFIED)** | 2025 | n/a (paper) | Paper findings: demographics and category attraction worsen homogenisation. Tested interventions: cold-start and feedback weighting. Related: PersonaAct (https://arxiv.org/html/2601.22547) for counterfactual filter-bubble auditing, and the BEP metric (AAAI 2026) with code at https://github.com/fengdifu24/bepmetric |
| 34 | **Microsoft Recommenders** | https://github.com/recommenders-team/recommenders | Python | MIT | **Active: last push 2026-09-25.** About 22k stars. | **Easy–Med** | Many Colab-ready notebooks. `recommenders/evaluation/python_evaluation.py` defines `diversity`, `user_diversity`, `novelty`, `historical_item_novelty`, `serendipity`, `user_serendipity`, `catalog_coverage`, `distributional_coverage` (verified). **Ready-made beyond-accuracy metrics.** |
| 35 | **RecBole** | https://github.com/RUCAIBox/RecBole (docs https://recbole.io/) | Python / PyTorch | MIT | Last push 2025-02-24 | Med | 90+ models in one config. Metric classes include `ItemCoverage`, `AveragePopularity`, `ShannonEntropy`, `GiniIndex`, `TailPercentage` (verified in `metrics.py`). |
| 36 | **Elliot** | https://github.com/sisinflab/elliot | Python | Apache-2.0 | Active: last push 2026-09-22 | Med | Config-file driven. The README advertises "accuracy to beyond-accuracy, bias, and fairness" metrics. |
| 37 | **Cornac** | https://github.com/PreferredAI/cornac (https://cornac.preferred.ai) | Python | Apache-2.0 | Active: last push 2026-09-14 | Easy–Med | Simple API. **Main Cornac has only accuracy and ranking metrics** (verified in `metrics/__init__.py`); diversity metrics live in the Informfully fork (#42). |
| 38 | **LensKit (lkpy)** | https://github.com/lenskit/lkpy (https://lenskit.org) | Python | MIT-style (Boise State / Drexel) | Active: last push 2026-09-23 | Med | A teaching-oriented toolkit (used in university recsys courses). An alternative to MS Recommenders. |
| 39 | **Mesa** (agent-based modelling) | https://github.com/mesa/mesa (docs https://mesa.readthedocs.io) | Python | Apache-2.0 | **Active: last push 2026-09-23** | **Easy–Med** | Build the team's own ABM: agents with interest vectors, a feed ranker, and a "not interested" action. Has built-in data collection and browser visualisation. |
| 40 | **NDlib** (network diffusion and opinion dynamics) | https://github.com/GiulioRossetti/ndlib (docs http://ndlib.readthedocs.io/) | Python | BSD-2-Clause | Last push 2026-07-31 | **Easy** | Includes **`AlgorithmicBiasModel` and `AlgorithmicBiasMediaModel`** (verified): opinion dynamics where an "algorithm" preferentially shows like-minded peers or media. **One parameter controls cocoon strength.** A great five-minute demo. |
| 41 | **Triple-Filter-Bubble model** (Geschke, Lorenz & Holtz 2019, BJSP) | https://github.com/janlorenz/TripleFilterBubble (Zenodo DOI 10.5281/zenodo.1407733). Paper: https://bpspsychub.onlinelibrary.wiley.com/doi/abs/10.1111/bjso.12286 | NetLogo | MIT | Last push 2019-04-14 (stable) | **Easy** (NetLogo Web runs in the browser) | 12 ready scenarios separating individual, social and technological filters. **Live in-class demo; replicate one scenario.** |

### Anti-cocoon ranking experiments and alternative platforms

| # | Name | URL | Language | Licence | Status | Difficulty | How our project could use it |
|---|---|---|---|---|---|---|---|
| 42 | **Informfully Recommenders** (norm-aware Cornac extension, University of Zurich) | https://github.com/Informfully/Recommenders (plus /Experiments, /Datasets) | Python | Apache-2.0 | Repos created 2024–25 (last push not checked) | Med | **One package with MMR, PM-2, Greedy-KL (calibration) and Dynamic Attribute Penalization re-rankers, RADio / Gini / ILD metrics, and rank- and preference-based user simulators.** Supports the MIND, EB-NeRD and NeMig news datasets. |
| 43 | **Prosocial Ranking Challenge** (Berkeley CHAI, 2024) | Code: https://github.com/HumanCompatibleAI/ranking-challenge. Results paper: https://arxiv.org/abs/2603.19626. About: https://humancompatible.ai/news/2024/01/18/the-prosocial-ranking-challenge-60000-in-prizes-for-better-social-media-algorithms/ | Python (example rankers, API spec, sample data) | **No licence file** | Last push 2025-03-26 | Med | Field experiment: 9,386 users, 5 alternative rankers vs control, Facebook/Reddit/X via browser extension, Aug 2024 – Feb 2025. The paper's title reports reduced polarisation "without sacrificing engagement". **The best real evidence that re-ranking can work.** The sample-ranker API is a template for a "bridging re-ranker". Perspective-API ranker: https://github.com/HumanCompatibleAI/ranking-challenge-perspective |
| 44 | **Tournesol** (open, collaborative YouTube recommender, EPFL-linked) | https://github.com/tournesol-app/tournesol ; https://tournesol.app ; dataset paper https://openreview.net/pdf/7a278281b2bae45d690e6e3d157320620769a0f6.pdf | Python (Django) + React | Code AGPL-3.0+; public data ODC-BY-1.0 (per FAQ) | **Active: last push 2026-09-25** | Easy (data) / Hard (platform) | Pairwise comparisons ("more reliable", "more important") → Bradley-Terry scores. **An alternative objective to engagement.** The public dataset (updated weekly) is small enough for pandas. |
| 45 | **Polis** plus **red-dwarf** (Python re-implementation of the Polis pipeline) | https://github.com/compdemocracy/polis ; https://github.com/polis-community/red-dwarf | Polis: Python/Clojure/TS. red-dwarf: Python. | Polis AGPL-3.0; red-dwarf MPL-2.0 | Both active (Polis last push 2026-09-27) | Med | PCA + clustering of opinion groups and "group-informed consensus". **The bridging idea in a deliberation tool.** red-dwarf lets students run it in Python. |
| 46 | **Gobo** (MIT Center for Civic Media: aggregator with user-controlled filters that shows what was filtered out) | https://github.com/mitmedialab/gobo | JavaScript + Python (Flask) | MIT | Created 2017. Old CI suggests low maintenance (UNVERIFIED). | Med | A design reference for **transparent, user-controlled filters**. Screenshots for the "solutions" section. |
| 47 | **Filter-bubble demo repos** (student / explorable level) | https://github.com/ncase/crowds (Nicky Case's network explorable) ; https://github.com/Liebestraum09/echobreak (2026 notebook: bubble plus a structural fix) ; https://github.com/Vitinholiv/Bubble ; https://github.com/malshehriai11/NRSim (news filter bubbles) ; https://github.com/kasnder/IdentiSwap (YouTube extension to "swap" bubbles) | Mixed | Varies / unchecked | Small, 0–450 stars | Easy | Inspiration for the **interactive demo**. Nicky Case's "Wisdom and/or Madness of Crowds" explorable is the design benchmark. The others are tiny, so verify before reusing code. |

---

## 3. Diversity and beyond-accuracy metric and re-ranking libraries

| # | Name | URL | Language | Licence | Status | Difficulty | How our project could use it |
|---|---|---|---|---|---|---|---|
| 48 | **RADio** (Vrijenhoek et al., RecSys 2022: rank-aware divergence metrics for normative news diversity) | https://github.com/svrijenhoek/RADio (simplified: https://github.com/svrijenhoek/RADio- ; follow-up: https://github.com/svrijenhoek/normative-diversity) | Jupyter / Python | **No licence file** | Last activity 2024 | Med | Five metrics: Calibration, Fragmentation, Activation, Representation, Alternative Voices. Rank-aware JS-divergence is a principled **"cocoon distance"**. The Informfully (#42) implementation is easier to use. |
| 49 | **RecList** (behavioural "black-box" tests for recommenders) | https://github.com/RecList/reclist (https://reclist.io) | Python | MIT | Last push 2023-08-09 (inactive) | Med | Write "cocoon unit tests", e.g. "after 20 cooking likes, ≥30% of recommendations are non-cooking". |
| 50 | **RecTools** (MTS) | https://github.com/MTSWebServices/RecTools | Python | Apache-2.0 | Active: last push 2026-09-09 | Easy–Med | Verified metrics: `IntraListDiversity`, `Serendipity`, `MeanInvUserFreq` (novelty), `AvgRecPopularity`, `CatalogCoverage`, plus debiasing utilities. A clean API. |
| 51 | **Fast greedy MAP inference for DPP** (Chen, Zhang & Zhou, NeurIPS 2018; from Hulu) | https://github.com/laming-chen/fast-map-dpp ; paper http://papers.nips.cc/paper/7805-fast-greedy-map-inference-for-determinantal-point-process-to-improve-recommendation-diversity | Python (numpy, a single short file) | Apache-2.0 | Last push 2020-05-11 (stable) | **Easy** | Drop-in **DPP diversity re-ranker**: build the kernel `L = diag(q)·S·diag(q)` from relevance and similarity. DPP-style re-ranking is widely reported in industry (UNVERIFIED for any specific platform). **Our main "technical fix" candidate.** |
| 52 | **Calibrated Recommendations** (Steck, RecSys 2018) | https://github.com/karlhigley/calibrator (Scala) ; Python via Informfully's Greedy-KL re-ranker (#42) | Scala / Python | MIT (calibrator) | Last push 2022 | Easy to re-implement (about 30 lines) | Makes the recommended genre mix match the user's history mix. Shows that **"calibration ≠ diversity"**: it can preserve a cocoon. No official Steck code was found. |
| 53 | **Beyond-accuracy metrics already in the frameworks** | See #34 (MS Recommenders), #35 (RecBole), #36 (Elliot), #50 (RecTools), #42 (Informfully), #24 (T-RECS) | Python | See above | See above | Easy | **Pick one metric set and use it consistently**: recommended trio = category entropy / Gini, intra-list diversity, coverage. |

---

## 4. Audit tooling, audit datasets and data donation

| # | Name | URL | Language | Licence | Status | Difficulty | How our project could use it |
|---|---|---|---|---|---|---|---|
| 54 | **KInIT YouTube misinformation filter-bubble audit** (RecSys 2021; extended in ACM TORS) | https://github.com/kinit-sk/yaudit-recsys-2021 | Python (Selenium bots) + notebooks + CSV | **No licence file** | Repo touched 2026 (last push not checked) | **Easy (data) / Hard (bots)** | Sock puppets first "enter" a bubble by watching misinformation, then try to **"burst" it by watching debunking videos**. The repo includes the bots, `recommendations.csv` / `search_results.csv`, and about 2.9k manual annotations. **Re-analyse the bubble-bursting curves; this is directly "how to break a cocoon".** |
| 55 | **TikTok audit reproducibility study** (Mosnar et al., SIGIR 2025) | https://arxiv.org/abs/2504.18140 ; Zenodo record https://zenodo.org/records/16792218 (contents **UNVERIFIED**, blocked here) | Paper (+ probably code/data) | Unknown | 2025 | Easy (paper) | Key finding: TikTok audits reproduce poorly and findings go stale within months. This is an important caveat for any claim about "the" TikTok algorithm. |
| 56 | **"When 'For You' Isn't For You: Measuring User Agency in TikTok's Algorithmic Feed"** (Kaplan et al., 2026) | https://arxiv.org/abs/2605.10690 ; press: https://news.northeastern.edu/2026/06/09/tiktok-not-interested-algorithm-control/ | Paper | Code release **UNVERIFIED** | 2026 | Easy (paper) | Directly answers **"does 'Not interested' work?"**: sock puppets on the mobile app, 200+ videos per topic (cooking, fitness, sports betting). "Not interested" beat swiping in 3/5 runs (cooking, fitness) and 4/5 runs (betting), but long-term effectiveness varied by topic. **Replicate the design in the simulator.** |
| 57 | **Other 2025–26 TikTok audits** | Personalisation drift on polarising topics: https://arxiv.org/pdf/2603.20723 ; ads and minors: https://arxiv.org/html/2603.05653 ; amplification dynamics: https://arxiv.org/pdf/2503.20231 ; AutoLike (automated interaction audits): https://arxiv.org/pdf/2502.08933 ; WhichTok (compares three TikTok data-acquisition tools): https://arxiv.org/pdf/2608.09917 | Papers | Unknown | 2025–26 | Easy–Med | Literature evidence. WhichTok helps choose a data-collection method. |
| 58 | **Student-scale TikTok sock-puppet pipelines** | https://github.com/ferjozsot23/tiktok-fyp-auditor (Playwright + Whisper, MSc 2026) ; https://github.com/raye22/tiktok_personalization | Python | Unchecked | Small, 2026 | Hard (and ToS/ethics issues) | Shows what an automated audit looks like. **Not recommended to run** (account bans, ethics). Cite it as the method. |
| 59 | **Mozilla RegretsReporter** (YouTube extension for reporting regrettable recommendations; data behind Mozilla's "Does this button work?" study) | https://github.com/mozilla-extensions/regrets-reporter | Python (analysis) + JS/TS (extension) | **No licence detected** | Last push 2023-11-28 (inactive) | Med | Classic crowdsourced audit of **whether YouTube's "Don't recommend" / "Not interested" buttons work.** The extension and analysis code are a model for a small team survey. |
| 60 | **Zeeschuimer** (browser extension that captures the items your TikTok/Instagram/X feed actually loads, exported as NDJSON; feeds 4CAT) | https://github.com/digitalmethodsinitiative/zeeschuimer ; converter https://github.com/PublicDataLab/zeehaven ; example analysis https://github.com/jobreu/tiktok-analysis | JavaScript | MPL-2.0 | **Active: last push 2026-09-10** | **Easy–Med** | **Lowest-effort real-feed data.** Team members browse normally, then export what their feed showed and measure topic entropy before and after using "Not interested" or Instagram's "Your Algorithm". No automation, so fewer ToS issues. |
| 61 | **Port / Feldspar** (Eyra data-donation frontend; data processed locally in the browser) | https://github.com/eyra/port (deprecated; README points to https://github.com/eyra/feldspar). JOSS paper DOI 10.21105/joss.05596 | TypeScript + Python (Pyodide) | AGPL-3.0 | Port deprecated 2024; Feldspar is the successor | Med–Hard | The privacy-respecting way to analyse **Takeout / "Download your data" exports** (TikTok, YouTube, Instagram). A light version: write a local pandas script over each member's own export. |
| 62 | **OSD2F** (Open Source Data Donation Framework, University of Amsterdam) | https://github.com/uvacw/osd2f | Python | AGPL-3.0 | **Archived.** README points to https://datadonation.eu | Med | Background on data-donation methods only. |

---

## (a) Top 10 for five first-year students (6 weeks, laptops/Colab)

| Rank | Resource | Why | Suggested owner |
|---|---|---|---|
| 1 | **X 2023 heavy-ranker weights** (#2) + awesome-twitter-algo (#3) | The only real, published, numeric ranking formula. Reply = 13.5, author-engaged reply = 75, negative feedback = -74, report = -369. Pairs directly with the team's x-algorithm (2026) work. | Member A (algorithm analysis) |
| 2 | **KuaiRec + KuaiRand** (#28, #29) | Real short-video data (Douyin's sibling ecosystem, Kuaishou) small enough for Colab. Fully-observed preferences make "true" cocoon measurement possible. Random exposures mimic "兴趣探索". | Member B (data) |
| 3 | **T-RECS** (#24) | `pip`-installable simulator with built-in homogenisation metrics. The fastest route to a credible cocoon-over-time plot. | Member C (simulation) |
| 4 | **NDlib `AlgorithmicBiasModel`** (#40) | Five-minute opinion-polarisation demo; one parameter models algorithm strength. | Member C |
| 5 | **fast-map-dpp** (#51) + **Informfully MMR / Greedy-KL re-rankers** (#42) | Ready diversity re-rankers: the "solution" half of the project. | Member D (solutions) |
| 6 | **Microsoft Recommenders `python_evaluation`** (#34) (or RecTools #50) | Verified diversity, novelty, serendipity and coverage functions. No need to invent metrics. | Member B/D |
| 7 | **Community Notes bridging algorithm** (#4, #5) | Real-world anti-polarisation algorithm, open-source and still maintained (2026). A small matrix-factorisation re-implementation is feasible. | Member D |
| 8 | **Triple-Filter-Bubble NetLogo Web** (#41) | Zero-install browser demo for the presentation. It separates individual, social and algorithmic causes (a "not only the algorithm" nuance). | Member E (presentation) |
| 9 | **Prosocial Ranking Challenge** (#43) | Real field-experiment evidence (9,386 users) that alternative rankers reduce polarisation. Its sample-ranker API gives a template. | Member D/E |
| 10 | **Audit evidence bundle**: Kaplan 2026 "Not interested" (#56) + KInIT YouTube bubble-bursting data (#54) + Zeeschuimer self-audit (#60) | Answers the core question ("do anti-cocoon controls work?") with real data plus a small ethical self-audit. | Member E + all |

---

## (b) Ideas for combining them

1. **"X-score inside a cocoon simulator".**
   - Implement the 2023 weighted score `Σ w_i · P(engagement_i)` in a roughly 100-line numpy or Mesa/T-RECS simulation. Use 100 users with topic-interest vectors; the P(·) values come from interest similarity.
   - Vary `negative_feedback_v2` from 0 to -74 to -300 and plot category entropy over 50 rounds. This answers whether a stronger "not interested" penalty breaks the cocoon or only removes one topic.
   - Swap in the 2026 x-algorithm weights from the other agent to compare.
2. **"Douyin 兴趣探索 vs DPP vs greedy on real data".**
   - Use KuaiRec's fully-observed matrix as ground truth.
   - Compare four policies:
     - (i) greedy top-k by predicted watch ratio;
     - (ii) the Douyin-style filed policy: X% rarely-watched categories + 1 random item;
     - (iii) DPP re-ranking (fast-map-dpp);
     - (iv) MMR (Informfully).
   - Report watch-ratio (satisfaction), category Gini/entropy (Recommenders/RecTools), and coverage.
   - The expected finding is a satisfaction–diversity trade-off curve. KuaiRand's random exposures give a real-world check on how users react to exploration.
3. **"Not-interested replication in silico".**
   - Recreate Kaplan 2026's sock-puppet protocol in the simulator: 200 videos, topic seeding, then "Not interested" vs swipe-away.
   - Model the button as either a (a) video-level, (b) creator-level or (c) topic-level penalty, with decay.
   - Show which modelling choice reproduces their "works short-term, varies long-term" result.
4. **"Bridging as a cure".**
   - Re-implement Community Notes' matrix factorisation on a tiny synthetic ratings matrix (two opinion camps) to show how bridging scores differ from raw likes.
   - Use the bridging score as a feed re-ranker inside NDlib-style opinion dynamics, or in the T-RECS simulation.
   - Compare polarisation (opinion variance) under engagement ranking vs bridging ranking. This echoes the Prosocial Ranking Challenge finding.
5. **"Chronological vs popularity vs personalised".**
   - Implement Mastodon-style chronological, Reddit hot, HN gravity and personalised collaborative filtering (spacecowboy style) in the same simulation.
   - Measure what each does to diversity. Non-personalised rankers make a good control condition.
6. **"Disclosure vs code" table.**
   - For X (2023 code, 2026 code, DSA SRA 2025), TikTok (transparency page, DSA 2025 report), Meta (system cards), Douyin (95152 site, CAC filing) and Kuaishou (OneRec papers), tabulate:
     - what they disclose (signals, objectives, weights, diversity rules, user controls);
     - what is verifiable in code.
   - Result: a transparency scorecard for the report.
7. **"Self-audit with real feeds".**
   - Each member uses Zeeschuimer (or their platform's data export) for one week: three days of baseline, then an "intervention" (heavy use of "Not interested", Instagram "Your Algorithm", or TikTok's refresh/non-personalised feed where available).
   - Compute topic entropy per day. The sample is tiny (n=5), so frame it as a case study and follow ethics guidance.
8. **Re-analyse KInIT YouTube data.** Plot the "bubble bursting" curve (share of misinformation recommendations vs number of debunking videos watched). That gives empirical support to the "active counter-consumption" strategy in the "how to break cocoons" advice.

---

## (c) Gaps and caveats

- **No open production ranker for TikTok, Douyin, Xiaohongshu, Kuaishou or Bilibili.**
  - Monolith is archived infrastructure, not ranking logic.
  - OneRec/OpenOneRec are research releases; production weights and objectives are not public.
  - Nothing verifiable was found for **Bilibili**'s recommender (no search budget left to look further).
- **CAC algorithm filing text** could not be accessed. beian.cac.gov.cn and cac.gov.cn were blocked, and the Douyin "兴趣探索 + 1 random item" wording comes from a secondary source (**UNVERIFIED**). Someone on the team should open https://beian.cac.gov.cn from Hong Kong or the mainland and screenshot the Douyin and Xiaohongshu entries.
- **The TikTok DSA Article 27 "main parameters" page** and the Douyin 95152 site were not fetchable here. Their content is from search snippets only.
- **Bluesky's default "Discover" algorithm is not open-source.** Only the feed-generator framework and third-party feeds are; spacecowboy's "For You" code release is unconfirmed.
- **No public code was found for SimTok (2025) or Kaplan 2026.** The Mosnar 2025 Zenodo contents are unverified.
- **Simulator dependency rot.** RecSim and RecSim NG are archived (TF1-era) and T-RECS has been quiet since 2024. On Colab, prefer T-RECS, Mesa, NDlib or a hand-written numpy simulation.
- **No standard "information cocoon index".** Metrics are scattered (entropy, Gini, ILD, RADio JS-divergence, coverage). The team must define and justify one. RADio is news-specific.
- **Calibration (Steck 2018)** has no official code; only a Scala port and Informfully's Greedy-KL exist. It is easy to hand-code.
- **Missing licences:** the Prosocial Ranking Challenge repo, RADio, KInIT yaudit, UCRS and RegretsReporter have no licence file. They are fine for reading and citing, but reuse rights are unclear.
- **Platform audits go stale fast** (Mosnar 2025). Any claim about "the algorithm" should carry a date. Automated sock-puppet scraping risks ToS violations and account bans; prefer simulation, public datasets and voluntary self-exports.
- **Search budget:** the session's web-search quota ran out mid-task. Covington et al. 2016 (YouTube DNN), the Mastodon trends docs and Chinese tech blogs (Kuaishou, Xiaohongshu, Bilibili engineering blogs) were not searched in depth.
