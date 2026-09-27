# Resource Inventory 2 — SOLUTIONS to information cocoons / filter bubbles (信息茧房)

HKU COMP1110 group project. Compiled 2026-09-27.

**How this was compiled.** Every item below has a URL that appeared in a live web search result during this session. Most direct page fetches (arxiv.org, Chinese news sites) were blocked by the network, so summaries come from search-result snippets and abstracts. Anything I could not confirm from a snippet is marked **UNVERIFIED**. No repositories were cloned. The "Difficulty" rating is my estimate for first-year students with basic Python (numpy/pandas): Easy / Medium / Hard.

Legend: **Paper** = paper link, **Code** = code link (only when a code URL was actually seen), **Evidence** = what is known about effectiveness.

---

## Part 1 — Platform-side algorithms (re-ranking, exploration, control)

### 1.1 Maximal Marginal Relevance (MMR): Carbonell & Goldstein, SIGIR 1998
- **Paper:** https://aclanthology.org/X98-1025.pdf ; Semantic Scholar: https://www.semanticscholar.org/paper/The-Use-of-MMR-and-Diversity-Based-Reranking-in-and-Carbonell-Goldstein/fb27d922754a8bfb8dee582f0231f55174fd50e3
- **Tutorial (recsys framing):** https://medium.com/data-science-collective/diversity-in-recommendations-maximal-marginal-relevance-mmr-0e7840c9399e
- **Summary:** MMR builds a list greedily. At each step it picks the item that maximises λ·relevance − (1−λ)·(max similarity to the items already chosen), so it trades relevance against redundancy. It was originally made for search and summarisation, and it is now the standard baseline for diversity re-ranking in recommenders (and in RAG).
- **Evidence:** The original paper reports "some benefits" for diversity ranking in preliminary results. Its value is that it is simple, not that it has strong recsys A/B evidence.
- **Difficulty:** **Easy.** About 15 lines of numpy with a cosine-similarity matrix.
- **How we could use it:** It is our main baseline re-ranker. Sweep λ from 0 to 1 to trace a diversity–engagement trade-off curve in the simulator.

### 1.2 DPP greedy MAP re-ranking: Chen, Zhang & Zhou (Hulu), NeurIPS 2018
- **Paper:** https://arxiv.org/abs/1709.05135 ; NeurIPS: https://proceedings.neurips.cc/paper/2018/hash/dbbf603ff0e99629dda5d75b6f75f966-Abstract.html
- **Code (official, Python):** https://github.com/laming-chen/fast-map-dpp (file `dpp.py`: https://github.com/laming-chen/fast-map-dpp/blob/master/dpp.py)
- **Related code:** a MATLAB version is in https://github.com/insuhan/dppmapmips/blob/main/greedy_exact.m, and a follow-up paper ("Lazy and Fast Greedy MAP") is at https://github.com/Alnusjaponica/DPP-MAP-Inference
- **Chinese explainer:** https://guyuecanhui.github.io/2020/07/29/paper-2018-hulu-dpp_map/
- **Summary:** A determinantal point process (DPP) scores a set of items with the determinant of a kernel L = diag(q)·S·diag(q), where q is item quality/relevance and S is item similarity. Sets of relevant, mutually dissimilar items get high scores. Exact MAP inference is NP-hard. The paper gives a fast incremental-Cholesky greedy algorithm that is practical for real-time recommendation.
- **Evidence:** The paper reports a better relevance–diversity trade-off than competing methods at much lower run time. The details of any Hulu online A/B test are **UNVERIFIED**.
- **Difficulty:** **Medium.** `dpp.py` is short and can be called almost as-is. Understanding *why* the determinant measures diversity needs basic linear algebra (the determinant is the volume spanned by the item vectors).
- **How we could use it:** It is the second re-ranker. Compare it with MMR at matched relevance loss. Hypothesis: DPP diversifies the whole set, while MMR only penalises the most similar neighbour.

### 1.3 DPP at YouTube: Wilhelm et al., CIKM 2018
- **Paper:** https://dl.acm.org/doi/10.1145/3269206.3272018 ; IR Anthology: https://ir.webis.de/anthology/2018.cikm_conference-2018.292/ ; Semantic Scholar: https://www.semanticscholar.org/paper/Practical-Diversified-Recommendations-on-YouTube-Wilhelm-Ramanathan/c09b090a664674ba528957a28330ba07d1004dcc
- **Summary:** This is Google/YouTube's production DPP diversification of the mobile home feed. It learns the DPP kernel parameters from user feedback and re-ranks the feed in windows.
- **Evidence:** The abstract says it "yields substantial short- and long-term increases in user engagement" in live experiments. This is one of the strongest pieces of industrial evidence that **diversity need not cost engagement**. The exact percentage figures are **UNVERIFIED** (the PDF was not accessible).
- **Difficulty:** Hard to reproduce as described (learned kernel). The idea can be reproduced with item 1.2's code.
- **How we could use it:** Cite it as real-world evidence in the report ("YouTube found diversity *raised* long-term engagement"). Then test whether our simulator reproduces the effect. It should, if we give simulated users satiation or boredom.

### 1.4 Calibrated Recommendations: Steck (Netflix), RecSys 2018
- **Paper:** https://dl.acm.org/doi/10.1145/3240323.3240372 (PDF: https://dl.acm.org/doi/pdf/10.1145/3240323.3240372)
- **Code:** https://github.com/karlhigley/calibrator (third-party). Notebook walkthrough: http://ethen8181.github.io/machine-learning/recsys/calibration/calibrated_reco.html
- **Summary:** Accuracy-trained recommenders over-serve a user's main interest and crowd out their minor interests. Calibration re-ranks so the genre distribution of the list matches the user's history; for example, 70% romance and 30% action in → 70/30 out. Divergence is measured with a KL divergence, and the method uses a greedy re-rank with a trade-off λ. (That the metric is a KL divergence comes from my knowledge of the paper; the snippet only says "metrics for quantifying the degree of calibration".)
- **Evidence:** Nominated for best paper at RecSys 2018. The paper reports offline results on MovieLens; Netflix online results are **UNVERIFIED**.
- **Difficulty:** **Easy–Medium.**
- **How we could use it:** Calibration is a *different* goal from diversity. It protects minority interests from disappearing, which is exactly the "narrowing over time" mechanism of a cocoon. It makes a good contrast with MMR/DPP, which push *beyond* the user's history.

### 1.5 Contextual bandits / exploration: LinUCB, Li, Chu, Langford & Schapire, WWW 2010 (Yahoo!)
- **Paper:** https://arxiv.org/pdf/1003.0146 ; IR Anthology: https://ir.webis.de/anthology/2010.wwwconf_conference-2010.67/
- **Code (student-level reimplementation):** https://github.com/Michael-Yi-Rong/Contextual-Bandits
- **Offline evaluation companion paper:** "Unbiased Offline Evaluation of Contextual-bandit-based News Article Recommendation Algorithms" https://arxiv.org/pdf/1003.5956
- **Summary:** Recommendation is framed as an explore/exploit problem. LinUCB picks the item with the highest upper confidence bound, so uncertain items get tried. This is the canonical paper on exploration in recommendation. Simpler relatives are ε-greedy (with probability ε, show a random item) and Thompson sampling (sample from a posterior).
- **Evidence:** The paper reports a click lift over context-free bandits on Yahoo! Front Page traffic. The often-quoted "12.5%" figure is **UNVERIFIED** in this session.
- **Difficulty:** ε-greedy is **Easy**; Thompson sampling (Beta-Bernoulli) is **Easy–Medium**; LinUCB is **Medium**.
- **How we could use it:** Implement ε-greedy and Thompson sampling as "exploration" solutions and compare them with re-ranking solutions. The key question is whether exploration only diversifies *exposure*, or whether it also *changes the learned user model* so the cocoon index stays lower over time.

### 1.6 "Values of User Exploration in Recommender Systems": Chen et al. (Google), RecSys 2021
- **Paper:** https://dl.acm.org/doi/10.1145/3460231.3474236 ; Google Research page: https://research.google/pubs/values-of-exploration-in-recommender-systems/
- **Summary:** Argues that exploration is not just a short-term cost for reducing model uncertainty. It improves recommendation quality aspects (such as novelty and diversity) that affect *long-term* user experience.
- **Evidence:** Live experiments on a large platform (Google; presumably YouTube). The specific metrics are **UNVERIFIED**.
- **Difficulty:** Conceptual only.
- **How we could use it:** It justifies measuring *long-horizon* engagement (for example, the last 20% of simulation steps) and not only immediate clicks.

### 1.7 Popularity-bias mitigation: Abdollahpouri, Burke & Mobasher, FLAIRS 2019 (xQuAD re-ranking)
- **Paper:** https://arxiv.org/abs/1901.07555 (AAAI-hosted PDF: https://cdn.aaai.org/ocs/18199/18199-78818-1-PB.pdf)
- **Related:** "The Unfairness of Popularity Bias in Recommendation" https://arxiv.org/pdf/1907.13286 ; calibration for popularity bias https://arxiv.org/pdf/2007.12230 ; causal approach "Causal Intervention for Leveraging Popularity Bias" https://arxiv.org/pdf/2105.06067
- **Summary:** Adapts xQuAD (a search-diversification method) into a personalised re-ranker that raises the share of long-tail (less popular) items. "Smooth xQuAD" gives the best accuracy/diversity balance.
- **Evidence:** Offline, on MovieLens and Epinions: better long-tail coverage with maintained ranking quality.
- **Difficulty:** **Easy–Medium.** Label items head/tail, then run a greedy re-rank.
- **How we could use it:** Popularity bias gives the *society-level* cocoon (everyone converges on the same hits). Measure cross-user homogenisation (for example, mean Jaccard overlap between users' lists) and catalogue coverage/Gini.

### 1.8 Serendipity-oriented recommendation: Kotkov, Wang & Veijalainen, Knowledge-Based Systems 2016 (survey)
- **Paper:** https://dl.acm.org/doi/10.1016/j.knosys.2016.08.014 ; Semantic Scholar: https://www.semanticscholar.org/paper/A-survey-of-serendipity-in-recommender-systems-Kotkov-Wang/cf9c0846c6b1c97b89fb27d5acef6db18fe04039
- **Also:** systematic review (JCST 2020) https://link.springer.com/article/10.1007/s11390-020-0135-9 ; interview study "What Is Serendipity?" https://arxiv.org/pdf/2505.15440 ; LLM knowledge-graph serendipity https://arxiv.org/pdf/2508.04032
- **Summary:** Defines serendipitous items as *relevant + novel + unexpected* (significantly different from what the user has rated). It classifies algorithms (re-ranking, modified CF, clustering) and evaluation methods.
- **Evidence:** Mostly offline metrics and user studies. There is little public A/B evidence.
- **Difficulty:** Easy to implement a simple version: a score of relevance × distance from the user's history centroid.
- **How we could use it:** Add a "serendipity" metric to the evaluation (a hit that is far from history) and possibly a serendipity re-ranker.

### 1.9 Bridging-based ranking: Ovadya & Thorburn, 2023
- **Paper:** https://arxiv.org/abs/2301.09976 ; Knight Institute version: https://knightcolumbia.org/content/bridging-systems ; Harvard Ash Center: https://ash.harvard.edu/resources/bridging-systems-open-problems-for-countering-destructive-divisiveness-across-ranking-recommenders-and-governance/
- **Design-library entry:** https://www.prosocialdesign.org/library/bridging-based-ranking
- **Summary:** Proposes "bridging systems" that rank content by whether it earns approval *across* divided groups, rather than by raw engagement. The domains covered are recommenders, collective-response systems and deliberation. This reframes the goal from "more diversity" to "more mutual understanding".
- **Evidence:** Conceptual. Field evidence comes from items 1.10–1.11 (small or mixed).
- **Difficulty:** **Medium** in a simulator, because simulated users need group labels.
- **How we could use it:** Give simulated users two opinion groups and score items by min(approval in group A, approval in group B). Compare this with engagement ranking on polarisation-style metrics.

### 1.10 X/Twitter Community Notes open-source matrix-factorisation ("bridging") algorithm
- **Code + docs:** https://github.com/twitter/communitynotes/blob/main/documentation/under-the-hood/ranking-notes.md
- **Summary:** Ratings are modelled as rating ≈ μ + rater_intercept + note_intercept + rater_factor · note_factor. The factor term absorbs "viewpoint" agreement, so a note is shown as "Helpful" only if its *intercept* (helpfulness that viewpoint does not explain) exceeds 0.40. In practice, a note has to be rated helpful by people who usually disagree.
- **Related research:** Supernotes https://arxiv.org/html/2411.06116 ; manipulation risks: https://arxiv.org/pdf/2511.02615 and https://arxiv.org/html/2607.01824 ; quality-sensitive MF https://arxiv.org/html/2604.11224 ; stability https://arxiv.org/pdf/2601.14002
- **Evidence:** Deployed at scale and open source. Later papers (2025–26) show vulnerability to rater bias and coordinated manipulation.
- **Difficulty:** **Medium.** A 1-D matrix factorisation fitted with numpy gradient descent is about 40 lines; the official repo is too big to use directly.
- **How we could use it:** It is the most concrete "bridging" algorithm to re-implement as a toy. It could also be the core of an app concept (Part 5).

### 1.11 Prosocial Ranking Challenge: field experiment 2024–25 (preprint 2026)
- **Paper:** https://arxiv.org/abs/2603.19626 (HTML: https://arxiv.org/html/2603.19626v1)
- **Blog:** https://rankingchallenge.substack.com/p/its-possible-to-reduce-polarization ; commentary: https://tomstafford.substack.com/p/another-algorithm-is-possible
- **Background:** https://humancompatible.ai/news/2024/01/18/the-prosocial-ranking-challenge-60000-in-prizes-for-better-social-media-algorithms/ ; registry: https://www.socialscienceregistry.org/trials/14274 ; finalist example: https://research.qut.edu.au/genailab/2024/05/08/genai-lab-a-finalist-in-the-prosocial-ranking-challenge/
- **Summary:** A browser extension re-ranked real Facebook, Reddit and X feeds for 9,386 desktop users (Aug 2024 – Feb 2025, around the US election). Users were randomised to control or one of five alternative algorithms. The algorithms used LLM classifiers to up-rank or add "prosocial" content: informative, constructive, pro-democracy, or divide-bridging.
- **Evidence:** Pooled, the algorithms cut affective polarisation by **0.03 SD** (p < 0.05), a 1.5-point drop in the in-party/out-party thermometer gap. Engagement changes were tiny: −0.37 min/day on Facebook, −0.2 on Reddit, +0.32 on X. So there was **a small benefit at almost no engagement cost**. Which of the five algorithms performed best is **UNVERIFIED** (full PDF not read).
- **Difficulty:** Not reproducible; cite it as evidence.
- **How we could use it:** It is the best 2026 evidence that re-ranking for social goals is *possible without killing engagement*, and also that the effects are *small*. Good for an honest "limitations" section.

### 1.12 User-Controllable Recommendation Against Filter Bubbles (UCRS): Wang, Feng, Nie & Chua, SIGIR 2022
- **Paper:** https://arxiv.org/abs/2204.13844 ; ACM: https://dl.acm.org/doi/10.1145/3477495.3532075
- **Code (PyTorch):** https://github.com/WenjieWWJ/UCRS ; reproducibility archive: https://zenodo.org/records/7590874
- **Summary:** Users issue *controls* at inference time, for example "fewer items like my past" or "more of category X". A causality-based User-Controllable Inference (UCI) framework, using counterfactual inference, removes the influence of out-of-date user representations. It supports user-feature controls and item-feature controls, including a simple re-ranking variant.
- **Evidence:** Offline experiments on three datasets (included in the repo) show reduced filter-bubble measures with controllable accuracy loss.
- **Difficulty:** Running the repo is **Medium–Hard**. Re-implementing the *idea* is **Easy**: a user slider sets a target share for a category, then re-rank.
- **How we could use it:** It is the academic backbone for a "user slider" solution. In the simulator, model a user who moves the slider after noticing the cocoon.

### 1.13 Human–AI adaptive dynamics and information cocoons: Piao et al. (Tsinghua FIB lab), Nature Machine Intelligence 2023
- **Paper:** https://www.nature.com/articles/s42256-023-00731-4 ; news summary: https://techxplore.com/news/2023-10-humanai-interaction-scenarios-cocoons.html
- **Summary:** An adaptive information-dynamics model of how user feedback and AI recommendation co-evolve. It is tested on two large real-world datasets. It identifies two scenarios that lead to cocoons and proposes strategies to prevent them.
- **Evidence:** Model plus empirical validation (NMI 5:1214–1224). The specific prevention strategies are **UNVERIFIED**. (My recollection is that they involve balancing positive/negative feedback and adding randomness or exploration; check the paper.)
- **Difficulty:** Reading is Medium. The *model structure* is a good template for our simulator.
- **How we could use it:** Cite it as the theoretical justification for a feedback-loop simulator. Mirror its "adaptive" user (preferences drift toward what is consumed).

### 1.14 Short-video cocoons (Tsinghua): Li, Gao & Li, CIKM 2022; Sukiennik et al., WWW 2024
- **Papers:** "An Exploratory Study of Information Cocoon on Short-form Video Platform" https://fi.ee.tsinghua.edu.cn/~gaochen/papers/CIKM2022-FilterBubble.pdf ; "Uncovering the Deep Filter Bubble: Narrow Exposure in Short-Video Recommendation" https://dl.acm.org/doi/10.1145/3589334.3648159
- **Group page:** https://fi.ee.tsinghua.edu.cn/~gaochen/
- **Summary:** Empirical studies on short-video platform data. The finding seen in the snippet is that users with homogeneous preferences are more likely to be trapped in severe cocoons. The WWW 2024 paper introduces a "deep" filter bubble: narrowing *within* a topic, not only across topics.
- **Also from the same group (URL not seen, so UNVERIFIED):** "Breaking Filter Bubble: A Reinforcement Learning Framework of Controllable Recommender System" (Li et al., 2023) and "Simulating Filter Bubble on Short-Video Recommender System with LLM Agents" (Sukiennik et al., 2025).
- **Difficulty:** Reading only.
- **How we could use it:** The "deep filter bubble" argues for measuring diversity at *two levels* (topic and sub-topic) in our metrics. It is directly relevant to Douyin/Kuaishou-style feeds.

### 1.15 Kuaishou industrial diversity papers
- **Contextual Distillation Model for Diversified Recommendation** (KDD 2024?; venue UNVERIFIED): https://arxiv.org/pdf/2406.09021. Diversity at inference time is achieved through a linear combination of model scores, with offline tests and an **online A/B test on Kuaishou**.
- **Feature-aware Diversified Re-ranking with Disentangled Representations:** https://arxiv.org/pdf/2206.05020. Deployed on Kuaishou's "more relevant videos" feature. It reports watch time, video plays **and** "watched video tags" (a diversity metric) together.
- **Learning and Optimization of Implicit Negative Feedback:** https://arxiv.org/pdf/2308.13249. Six months deployed on Kuaishou. It analyses the *correlation between diversity and users' negative feedback*, which relates to how "not interested" signals interact with diversity.
- **Real-time Short Video Recommendation on Mobile Devices:** https://arxiv.org/pdf/2208.09577 (on-device re-ranking).
- **Evidence:** Online A/B tests are reported. Exact lift numbers are **UNVERIFIED**.
- **Difficulty:** Hard to reproduce. Useful as "industry does this" evidence and for metric ideas (watch-time + tag coverage).

### 1.16 LLM / generative recommenders and cocoons (2024–2026)
- **"Do Generative Recommenders Deepen the Information Cocoon?" (2026):** https://arxiv.org/abs/2606.17707. The RecLoop closed-loop simulator uses LLM user agents on Amazon data. Generative (Semantic-ID) recommenders were *less* prone to exposure-level cocoons than sequential baselines. However, feedback loops still concentrated the "code space", giving a new "structural cocoon" metric.
- **"Quantifying the Potential to Escape Filter Bubbles: A Behavior-Aware Measure via Contrastive Simulation"** (AAAI; year UNVERIFIED): https://arxiv.org/pdf/2512.03067. Uses LLM user simulators to measure *escapability*, not just current diversity.
- **"Generative Echo Chamber? Effects of LLM-Powered Search Systems on Diverse Information Seeking"** (CHI 2024; venue UNVERIFIED): https://arxiv.org/html/2402.05880v2. Examines whether conversational LLM search creates echo chambers.
- **"Mitigating Filter Bubble from the Perspective of Community Detection: A Universal Framework"** (2025): https://arxiv.org/pdf/2508.11239. A plug-in mitigation framework; details UNVERIFIED.
- **"Understanding the Information Cocoon: A Multidimensional Assessment... of News Recommendation Systems"** (2025): https://arxiv.org/pdf/2509.11139. Useful for metric design.
- **"Content Fuzzing for Escaping Information Cocoons on Digital Social Media"** (2026): https://arxiv.org/pdf/2604.05461. Method details are **UNVERIFIED** (only the title was seen).
- **"A Simulation Framework for Studying Systemic Effects of Feedback Loops in Recommender Systems"** (2025): https://arxiv.org/pdf/2510.14857
- **"Decoding Echo Chambers: LLM-Powered Simulations..."** (COLING 2025): https://aclanthology.org/2025.coling-main.264.pdf
- **Other:** "An Exploratory Study on Information Cocoon in Recommender Systems" (Data Science & Engineering, Springer 2025): https://link.springer.com/article/10.1007/s41019-025-00288-9
- **How we could use it:** Optional stretch goal: replace our rule-based simulated user with an LLM agent. Also cite 2606.17707 as evidence that recommender *architecture* matters.

---

## Part 2 — Evidence on user-side and policy interventions

### 2.1 Chronological feed on Facebook/Instagram: Guess et al., Science 2023
- **Paper:** https://www.science.org/doi/10.1126/science.abp9364 ; summary: https://csmapnyu.org/research/academic-research/how-do-social-media-feed-algorithms-affect-attitudes-and-behavior-in-an-election-campaign
- **Summary:** Randomised users to a reverse-chronological feed for three months during the 2020 US election.
- **Evidence:** Time spent and activity dropped a lot. Users saw *more* political and untrustworthy content, *less* uncivil content, and more content from moderate or ideologically mixed sources (Facebook). There was **no significant change** in issue polarisation, affective polarisation or attitudes.
- **Lesson:** "Just turn off the algorithm" is not a clean fix. It changes exposure but not attitudes, and it reduces use.

### 2.2 X "For You" vs chronological: Nature 2026
- **Paper:** https://www.nature.com/articles/s41586-026-10098-2 ; PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC13061628/ ; news & views: https://www.nature.com/articles/d41586-026-00486-z ; CEPR column: https://cepr.org/voxeu/columns/how-xs-algorithm-shifts-political-attitudes
- **Summary:** A 2023 field experiment randomised US X users to an algorithmic or a chronological feed for 7 weeks.
- **Evidence:** Switching the algorithm **on** increased engagement and shifted policy opinions in a conservative direction; the algorithm showed more conservative and activist posts and demoted news outlets. Switching it **off** had *no comparable effect*: the asymmetry suggests exposure effects persist. Neither direction changed affective polarisation.
- **Lesson:** This is key for our "reset" argument. Once a cocoon forms, simply switching the feed off may not undo it, which argues for *prevention* (diversity by design) over *cure*.

### 2.3 Reducing like-minded exposure: Nyhan et al., Nature 2023
- **Paper:** https://www.nature.com/articles/s41586-023-06297-w
- **Evidence:** Cutting like-minded-source content by about 1/3 for 23,377 Facebook users increased cross-cutting exposure and reduced incivility. It had **no measurable effect** on 8 preregistered attitude measures.
- **Lesson:** Diversifying exposure ≠ changing minds, at least over short periods. Our project should define success as *exposure diversity and user agency*, and not promise depolarisation.

### 2.4 Nudging users to subscribe to counter-attitudinal outlets: Levy, AER 2021
- **Paper:** https://www.aeaweb.org/articles?id=10.1257%2Faer.20191777 ; Yale ISPS: https://isps.yale.edu/research/publications/isps21-08
- **Data + code:** https://www.openicpsr.org/openicpsr/project/121922/version/V1/view?path=/openicpsr/121922/fcr:versions/V1/Datasets/Likes&type=folder
- **Evidence:** Randomly offering subscriptions to counter-attitudinal news pages **reduced negative attitudes toward the other party** without changing opinions. Facebook's algorithm was *less likely to show* posts from counter-attitudinal outlets even after users subscribed.
- **Lesson:** This is strong evidence that a *user-side* action works and that the platform algorithm partly undoes it. A good argument for combining user-side and platform-side solutions.

### 2.5 Diversity nudges: Mattis, Masur, Möller & van Atteveldt, New Media & Society (online 2022; issue 2024)
- **Paper:** https://journals.sagepub.com/doi/full/10.1177/14614448221104413 ; open repository: https://research.vu.nl/en/publications/nudging-towards-news-diversity-a-theoretical-framework-for-facili ; project: https://www.nwo.nl/en/projects/406di19073
- **Summary:** A theoretical framework for *personalised* diversity nudges in news recommenders. Nudges are designed for different users: those who seek diversity but cannot find it, versus those who need serendipity to break feedback loops.
- **Related empirical work:** "Nudges for news recommenders: prominent article positioning increases selection, engagement, and recall of environmental news, but reducing complexity does not" (Journal of Communication 2025): https://doi.org/10.1093/joc/jqaf019. **Position nudges work; simplification nudges did not.** Also Shin & Zhou 2024, "Value and Diversity-Aware News Recommendation": https://journals.sagepub.com/doi/abs/10.1177/10776990241246680 ; a bachelor thesis review of digital nudging: https://recsys-lab.at/wp-content/uploads/2024/09/BA_Modre-Laura_Digital-Nudging_S2023.pdf
- **How we could use it:** Model a "position nudge" in the simulator, putting one diverse item at rank 1 versus rank 10. Position bias makes rank 1 much more powerful.

### 2.6 Do "Not interested" / "Dislike" controls work? Mozilla "Does This Button Work?" (2022)
- **Report:** https://www.mozillafoundation.org/en/youtube/user-controls/ ; press release: https://www.mozillafoundation.org/en/blog/mozilla-investigation-youtubes-dislike-button-other-user-controls-largely-fail-to-stop-unwanted-recommendations/
- **Evidence:** About 23,000 volunteers and about 568M recommended videos (via the RegretsReporter extension). Compared with not using controls, "Don't recommend channel" prevented only **43%** of unwanted recommendations, "Remove from history" **29%**, "Dislike" **12%** and "Not interested" **11%**. A survey of 2,700+ users found they feel *not in control*.
- **Lesson:** This is direct evidence that existing user-side controls are weak. It motivates *independent measurement* of whether controls work (app concept, Part 5).

### 2.7 Bottom-up "de-biasing" of YouTube without platform help: Haroon et al., PNAS 2023
- **Paper:** https://www.pnas.org/doi/10.1073/pnas.2213020120 ; arXiv: https://arxiv.org/abs/2203.10666 ; PDF: https://web.cs.ucdavis.edu/~zubair/files/haroon-pnas.pdf
- **Summary:** 100,000 sock-puppet accounts watched about 9.9M videos. The audit found ideologically congenial recommendations, increasingly extreme ones deeper in the trail, and more problematic channels. The team also **designed a bottom-up intervention**: the user's watch history is steered by injecting counter-balancing videos, which reduced ideological bias in recommendations *without YouTube's cooperation*.
- **Evidence:** Tested on sock puppets, **not** real users. The exact effect size is UNVERIFIED.
- **Difficulty:** The idea is simple to simulate: inject k "balancing" interactions into history.
- **How we could use it:** It is a strong candidate for a *user-side algorithmic* solution in our simulator ("history injection"). It is also an app concept.

### 2.8 Middleware / feed choice: Fukuyama et al., Stanford Working Group on Platform Scale (2020–21)
- **Report:** https://fsi.stanford.edu/publication/report-working-group-platform-scale ; Journal of Democracy article: https://www.journalofdemocracy.org/articles/the-future-of-big-tech-solving-for-a-moving-target/ ; explainer: https://stanforddaily.com/2021/11/10/want-to-limit-digital-platform-power-use-middleware-stanford-professors-say/ ; Georgetown overview: https://mdi.georgetown.edu/featured-research/diresta_middleware/
- **Summary:** Proposes third-party "middleware" companies that sit between users and platforms and let users choose their own ranking and filtering.
- **Evidence:** A policy proposal. The first large real-world instance is Bluesky (2.9).

### 2.9 Bluesky custom feeds: middleware in practice
- **Code (official starter kit, TypeScript):** https://github.com/bluesky-social/feed-generator ; docs: https://docs.bsky.app/docs/starter-templates/custom-feeds ; community examples: https://github.com/ealmuina/bsky-feed , https://github.com/mackuba/bluesky-feeds-rb
- **Research:** Zhou, Wang & Zhang (UW), "Middleware for Feed Recommendation in Practice" (2026): https://arxiv.org/abs/2609.12958. Interviews with 26 feed creators plus analysis of 88,302 custom feeds. Middleware works at scale, but creators lack interaction data and feedback, and are unpaid hobbyists. "Whose Posts Get Ranked: Identical-Text Exposure Gaps in Bluesky Custom Feeds" (2026): https://arxiv.org/pdf/2608.13879. Custom feeds can create their *own* biases. "Paper Skygest" (academic recs on Bluesky): https://arxiv.org/pdf/2601.04253
- **Difficulty:** Deploying a real feed is **Medium** (Node/TypeScript server plus hosting). It is within reach if one teammate knows JS.
- **How we could use it:** A real deployment path for a "diverse" or "bridging" feed. It is also evidence that feed choice alone does not guarantee diversity.

### 2.10 Algorithm literacy interventions
- **Review:** Gagrčin, Naab & Grub, "Algorithmic media use and algorithm literacy: An integrative literature review" (New Media & Society): https://journals.sagepub.com/doi/10.1177/14614448241291137
- **Young adults:** "When knowing more means doing less: Algorithmic knowledge and digital (dis)engagement among young adults" (HKS Misinformation Review, 2025): https://misinforeview.hks.harvard.edu/article/when-knowing-more-means-doing-less-algorithmic-knowledge-and-digital-disengagement-among-young-adults/. Knowing more about algorithms can lead to *disengagement* rather than critical action.
- **Awareness and attitudes:** Frontiers in Psychology 2025, "Resistance or compliance? The impact of algorithmic awareness on people's attitudes toward online information browsing": https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1563592/full ; JCMC, "Attitudinal and behavioral correlates of algorithmic awareness among German and U.S. social media users": https://academic.oup.com/jcmc/article/28/5/zmad035/7257707 ; "Resilience and disempowerment in algorithmic systems" (2026): https://doi.org/10.1177/14614448261446591 ; IJoC 2025: https://ijoc.org/index.php/ijoc/article/download/23508/4934/89234
- **Evidence (from snippets):** In a 2024 experiment, participants browsed under a diversity-maintaining algorithm and an adaptive algorithm (order randomised). The adaptive algorithm reduced diverse choices, especially when it came second. An 11-session after-school programme increased students' algorithm understanding and agency. Which of the above sources reports these two findings is not certain (**UNVERIFIED** attribution; likely the Gagrčin review).
- **How we could use it:** It supports an "explain + show" design (the tool shows your bubble) rather than pure education. It also warns that awareness alone can cause disengagement.

### 2.11 Friction and time-limit features
- **TikTok "Control your scroll" features:** https://newsroom.tiktok.com/tiktoks-new-features-to-help-you-control-your-scroll?lang=en-AU
- **Evidence:** In this session I found no rigorous public evaluation of platform time-limit features. The self-nudge-app study (Grüning et al., PNAS 2023, "one sec") was not confirmed (search budget exhausted), so it is **UNVERIFIED — no URL**. Friction mainly reduces *quantity* of use; its effect on *diversity* is untested. That is an evidence gap.

### 2.12 China: CAC "清朗·网络平台算法典型问题治理" campaign and platform responses (2024-11 → 2025)
- **Official (CAC, 2025-05-22):** https://www.cac.gov.cn/2025-05/22/c_1749536203490537.htm
- **Coverage:** https://www.nbd.com.cn/articles/2025-05-22/3883838.html ; https://www.stcn.com/article/detail/1841060.html ; https://news.qq.com/rain/a/20250523A009VJ00 ; editorial: https://news.bjd.com.cn/2025/05/22/11172602.shtml ; January 2025 platform measures: https://m.21jingji.com/article/20250106/herald/453104874790c3a9cb7ed74fab464ab0.html and https://finance.sina.com.cn/stock/relnews/us/2025-01-08/doc-ineehmtv3872000.shtml
- **Summary:** Under CAC guidance, platforms added "茧房评估" (cocoon assessment) and "一键破茧" (one-click cocoon-breaking) on Douyin, and "内容偏好调节" (content-preference adjustment) on Xiaohongshu and others. Xiaohongshu lets users view, edit, delete and add interest tags, and switch personalisation off. Weibo added "explanation labels" to the top-50 hot-search terms.
- **Independent test (journalism):** Nandu (南都) "多平台上线'内容偏好调节'功能，能破除信息茧房吗？实测" (2025-04): https://m.mp.oeeee.com/a/BAAFRD0000202504231074797.html ; print version: https://ipaper.oeeee.com/ipaper/A/html/2025-04/29/content_4432.htm. The page was **not accessible**, so its findings are UNVERIFIED.
- **Think-tank:** Tencent Research Institute, "算法破茧" (about 30,000 characters): https://tisi.org/32160/. Identifies engagement-maximising objectives, positive feedback loops and data dependency as cocoon mechanisms.
- **Evidence gap:** There is **no peer-reviewed evaluation** of whether 一键破茧 / 内容偏好调节 actually increase diversity over time. This is a clear gap our project can point to.

---

## Part 3 — Existing tools, apps and extensions (beyond AllSides / Ground News / Balancer)

| # | Tool | URL(s) | What it does | Evidence / notes | Use for us |
|---|------|--------|--------------|------------------|------------|
| 3.1 | **Unhook** (browser extension) | https://unhookextension.com/ ; https://chromewebstore.google.com/detail/unhook-remove-youtube-rec/khncfooichmfjbepaaaebmommgaepoid | Hides YouTube recommendations, Shorts, comments, autoplay | 500k+ users (per the store page snippet). No diversity evaluation. | Shows the "remove the algorithm" approach. It does not *diversify*. |
| 3.2 | **News Feed Eradicator** | https://github.com/jordwest/news-feed-eradicator ; https://addons.mozilla.org/en-US/firefox/addon/news-feed-eradicator/ | Replaces FB/IG/YT/LinkedIn feeds with a quote | Open source (WebExtension). No diversity evidence. | Code reference for building an extension that modifies feeds. |
| 3.3 | **Tournesol** | https://tournesol.app/ ; code: https://github.com/tournesol-app/tournesol ; paper: https://arxiv.org/abs/2211.01179v2 ; https://arxiv.org/abs/2107.07334 | Community-governed YouTube recommender. Contributors make pairwise comparisons, which are turned into scores (generalised Bradley-Terry, trust propagation, secure aggregation, "Solidago" pipeline). | Deployed, open source, security guarantees. | Example of "collective" rather than engagement-based ranking. The pairwise-comparison idea is easy to reuse. |
| 3.4 | **Gobo** (MIT Media Lab 2017; Gobo 2.0 at UMass 2022) | https://github.com/mitmedialab/gobo ; https://medium.com/mit-media-lab/who-filters-your-news-why-we-built-gobo-social-bfa6748b5944 ; https://www.media.mit.edu/publications/gobo-a-system-for-exploring-user-control-of-invisible-algorithms-in-social-media/ ; https://publicinfrastructure.org/2022/11/09/gobo-2-0-all-your-social-media-in-one-place/ | Aggregator with user sliders (seriousness, rudeness, virality, gender, brands). The politics slider runs from "my perspective" to "lots of perspectives". Shows *why* each post was included and what was filtered out. | Research prototype, open source. | **Best design precedent for a transparent slider UI.** |
| 3.5 | **Bluesky custom feeds** | see 2.9 | Users pick or subscribe to third-party ranking algorithms | Large-scale middleware (88k feeds) | Deployment path. |
| 3.6 | **Instagram "Your Algorithm"** (announced 2025-12-10) | https://about.instagram.com/blog/announcements/reels-algorithm-control | Shows the topics IG thinks you like (Reels/Explore); add or remove topics, preview example reels, reset | No public effectiveness data | The platform's own "transparency + control" pattern. |
| 3.7 | **TikTok "Manage Topics"** (2024) plus an AI-content slider (Nov 2025) | https://techcrunch.com/2024/08/30/tiktoks-new-manage-topics-tool-gives-you-more-control-over-your-for-you-feed-heres-how-to-use-it ; https://www.socialmediatoday.com/news/tiktok-adds-option-to-limit-ai-content-in-your-for-you-feed/805952/ ; https://www.macrumors.com/2025/11/19/tiktok-ai-content-limits/ ; https://newsroom.tiktok.com/more-ways-to-discover-new-content-and-creators-you-love?lang=en | Sliders for about 10+ broad topics (Creative Arts, Travel, Nature, Sports…) | No public effectiveness data. Coarse topics only. | Coarse topic slider = UCRS-style control (1.12). |
| 3.8 | **YouTube "Your custom feed"** (test from Nov 2025) | https://9to5google.com/2025/11/26/youtube-testing-new-home-page-with-more-control-over-suggested-content/ ; https://www.ghacks.net/2025/11/26/youtube-is-testing-your-custom-feed-a-way-to-let-users-personalize-their-home-feed/ ; https://betanews.com/2025/11/25/youtube-starts-testing-your-custom-feed-feature/ | Natural-language prompt to re-tune the Home feed | Experimental, limited users; no data | Natural-language control is the 2025–26 trend. Our tool could do a prompt-based version. |
| 3.9 | **Douyin 茧房评估 / 一键破茧**, **Xiaohongshu 内容偏好调节**, **Weibo 热搜解释标签** | see 2.12 | Self-assessment of cocoon plus one-click diversification; tag editing; ranking explanations | No independent evaluation | Direct comparison point for a HK/China-focused project. |
| 3.10 | **Bobble** (research browser extension, PAM 2014) | https://cseweb.ucsd.edu/~snoeren/papers/bobble-pam14.pdf ; https://link.springer.com/chapter/10.1007/978-3-319-04918-2_13 | Re-runs your Google query from many vantage points to show personalisation differences | Found that 98% of Google results showed some inconsistency, mostly due to location | Precedent for "show me what others see", i.e. a *comparison* view of your bubble. |
| 3.11 | **Filter-bubble visualisation**: Nagulendra & Vassileva, Hypertext 2014 | https://dl.acm.org/doi/10.1145/2631775.2631811 ; https://www.academia.edu/47959692/Understanding_and_controlling_the_filter_bubble_through_interactive_visualization | Interactive visualisation of what a social network's filter hides, with controls to let it through | Small user study (details UNVERIFIED) | Classic design precedent for a "bubble map" UI. |
| 3.12 | **Algorithmic Mirror** (2025 research prototype) | https://arxiv.org/pdf/2504.16615 | Interactive tool for self-reflection on YouTube recommendations | Details **UNVERIFIED** (title only) | Closest existing research prototype to our potential app; read before designing. |
| 3.13 | **Cyclops** (UMAP 2023 adjunct) | https://dl.acm.org/doi/10.1145/3563359.3597398 | "Looking beyond the single perspective in information access systems" | Details UNVERIFIED | Design precedent for multi-perspective views. |
| 3.14 | **WatchLens** (2026) | https://arxiv.org/pdf/2608.04807 | Configurable platform for online video-recommendation experiments | Details UNVERIFIED | Possible research infrastructure for user studies. |
| 3.15 | **Prosocial Design Network library** | https://www.prosocialdesign.org/library/bridging-based-ranking | Catalogue of evidence-rated prosocial design patterns (for example bridging-based ranking) | Curated evidence ratings | **Design-pattern collection for user agency.** Cite it for the app-design section. |
| 3.16 | **Spotify**: research on algorithmic vs organic diversity | https://research.atspotify.com/algorithmic-effects-on-the-diversity-of-consumption-on-spotify/ | (research, see 4.3) | — | Evidence on music cocoons. |

---

## Part 4 — Evaluation methodology

### 4.1 Simulation-based evaluation (feedback loops)
- **Chaney, Stewart & Engelhardt, RecSys 2018**, "How Algorithmic Confounding in Recommendation Systems Increases Homogeneity and Decreases Utility": https://arxiv.org/pdf/1710.11214 ; ACM: https://dl.acm.org/doi/10.1145/3240323.3240370. Simulates six recommenders (popularity, MF, random, ideal, content, social) in a feedback loop. Training on recommender-confounded data **homogenises users without increasing utility**. No code URL was seen. **This is the template for our simulator design** (random and "ideal" recommenders as bounds).
- **T-RECS** (Princeton, Lucherini, Sun, Winecoff & Narayanan): https://github.com/elucherini/t-recs ; quick-start notebook: https://github.com/elucherini/t-recs/blob/main/examples/quick-start.ipynb ; paper: https://arxiv.org/abs/2107.08959 ; blog: https://blog.citp.princeton.edu/2021/08/04/studying-the-societal-impact-of-recommender-systems-using-simulation/. A pip-installable Python simulator built for filter-bubble and polarisation studies. **Difficulty: Easy–Medium. The best off-the-shelf option for first-years.**
- **RecSim / RecSim NG** (Google): https://github.com/google-research/recsim ; https://github.com/google-research/recsim_ng ; https://arxiv.org/pdf/2103.08057. More powerful but TensorFlow-heavy. **Hard**; not recommended for 2 weeks.
- **Survey:** "Synthetic Data-Based Simulators for Recommender Systems: A Survey": https://arxiv.org/pdf/2206.11338
- **LLM-agent simulators:** RecLoop (1.16), feedback-loop framework https://arxiv.org/pdf/2510.14857

### 4.2 Offline metrics (for diversity–accuracy trade-off curves)
Standard metrics to implement (definitions are standard; no single URL needed):
- **Accuracy / engagement:** precision@k or hit-rate, or in simulation the expected click/watch probability (sum of the user's true utility over shown items).
- **Intra-list diversity (ILD):** mean pairwise (1 − cosine similarity) within a list.
- **Category entropy per user:** Shannon entropy of the categories consumed over a window. Plot it over time; a falling line is a cocoon forming.
- **Calibration (KL divergence):** 1.4.
- **Coverage and Gini:** fraction of the catalogue ever recommended; Gini of item exposure (popularity bias, 1.7).
- **Cross-user homogenisation:** mean Jaccard overlap between users' recommendation lists (Chaney 2018).
- **Serendipity:** relevant ∩ far from the history centroid (1.8).
- **Two-level "deep bubble" diversity:** topic and sub-topic entropy (1.14).
- **Escapability:** how many steps of exploration are needed to restore entropy (inspired by https://arxiv.org/pdf/2512.03067).
- Present results as **Pareto curves**: x = engagement, y = diversity, one curve per method, each point one value of λ or ε.

### 4.3 Published online / field evidence
- **YouTube DPP** (1.3): diversity → *higher* short- and long-term engagement.
- **Google exploration** (1.6): exploration improves long-term user experience.
- **Kuaishou** (1.15): online A/B tests of diversity re-rankers that report watch time *and* tag coverage.
- **Spotify, Anderson et al., WWW 2020**, https://dl.acm.org/doi/10.1145/3366423.3380281 ; Spotify Research page https://research.atspotify.com/algorithmic-effects-on-the-diversity-of-consumption-on-spotify/. **Algorithmic listening is associated with lower diversity**. Users who became more diverse did so by moving to *organic* listening. Recommendations work best for low-diversity users.
- **MovieLens, Nguyen et al., WWW 2014**: https://dl.acm.org/doi/10.1145/2566486.2568012 ; GroupLens blog: https://grouplens.org/blog/taking-recommendations-improves-consumption-diversity-a-surprise-result-from-exploring-the-filter-bubble-and-movielens/. Recommendations narrowed over time for everyone, but users who *followed* recommendations narrowed *less* than those who ignored them. **This is a counter-intuitive, important result.**
- **Facebook/Instagram 2020 election studies** (2.1, 2.3) and **X, Nature 2026** (2.2): field RCTs of feed changes.
- **Prosocial Ranking Challenge** (1.11): multi-platform RCT of alternative rankers.
- **Mozilla RegretsReporter** (2.6): crowd-sourced measurement of user controls.
- **Sock-puppet audits:** Haroon et al. (2.7). TikTok personalisation-drift audit (2026): https://arxiv.org/pdf/2603.20723

### 4.4 Key evaluation lessons for our report
1. Diversity and engagement are **not always in conflict** (YouTube DPP, Google exploration, PRC). Show this with Pareto curves, where some solutions might dominate the baseline.
2. **Exposure diversity ≠ attitude change** (Guess, Nyhan). Define success in terms of exposure and agency.
3. **Asymmetry/persistence** (X, Nature 2026) means prevention matters more than reset. Test "reset" in the simulator: does entropy recover after the cocoon forms?
4. **User controls are often weak** (Mozilla), and platform-side algorithms can counteract user choices (Levy). So test *combined* user + platform solutions.

---

## Part 5 — Recommendations

### (a) Shortlist: 3–5 solution approaches to implement and compare in a Python simulator (~2 weeks)

**Common setup (week 1):**
- Items: about 500–2,000 items with a category label plus an embedding vector. Use synthetic Gaussian clusters, or MovieLens genres (GroupLens; https://grouplens.org/datasets/movielens/, URL not re-checked this session).
- Users: about 200 users with true preference vectors. **Adaptive drift** (Piao et al. 2023 style): after consuming an item, the preference moves a little toward it. Clicks follow a logistic function of utility plus a position bias.
- Base recommender: score = learned user vector · item vector, retrained on observed clicks every T steps (the feedback loop; Chaney 2018). Alternatively use T-RECS (https://github.com/elucherini/t-recs) to save time.
- Bounds: **random** and **oracle ("ideal")** recommenders.
- Metrics: category entropy over time, ILD, coverage/Gini, cross-user Jaccard, cumulative clicks (engagement), and final distance between true and initial preferences (how much the user was "moved").

**Approaches to compare (pick 4):**
1. **MMR re-ranking** (1.1). Easy; sweep λ.
2. **DPP greedy re-ranking** (1.2). Wrap `laming-chen/fast-map-dpp/dpp.py`; sweep the relevance weight.
3. **Calibrated re-ranking** (1.4). Protects minority interests; compare "keep my 70/30" with "push me out" (MMR/DPP).
4. **Exploration: ε-greedy vs Thompson sampling** (1.5). Tests whether exploration also fixes the *learned model*, not just the current list.
5. **User-side: "history injection" or user slider** (2.7 / 1.12). The user (or a tool acting for them) adds k diverse interactions per week, or sets a target category share. This lets us compare **user-side vs platform-side** in one framework. That comparison is our most original angle.

**Suggested experiments:**
- Diversity–engagement Pareto curves for 1–4.
- A "cocoon then reset" test: run the baseline for 200 steps, then switch on each solution, and measure how fast entropy recovers. This tests the X/Nature 2026 asymmetry.
- Heterogeneous users: are diverse-by-nature users helped or harmed? (Spotify and MovieLens findings.)
- An optional bridging variant (1.9/1.10): two opinion groups, rank by minimum cross-group approval.

**Suggested 2-week plan:** Days 1–3 simulator plus baseline plus metrics. Days 4–7 MMR, calibration, ε-greedy (simple). Days 8–10 DPP, Thompson sampling, history injection. Days 11–14 experiments, plots, write-up.

### (b) App / tool design concepts not already done by existing products

**Concept 1: "Does this button work?" personal control-effectiveness tracker (破茧验证器)**
- **What:** A browser extension or mobile companion that logs your feed (YouTube / Bilibili web / Xiaohongshu web) before and after you use a platform control ("Not interested", Douyin 一键破茧, Xiaohongshu 内容偏好调节, TikTok Manage Topics). It shows a before/after topic-entropy chart and says whether the control actually changed the feed. With consent, results are pooled across users.
- **Why new:** Mozilla's 2022 study (2.6) did this once for YouTube and is now 4 years old. The Chinese platform controls (2.12) and IG "Your Algorithm" / YouTube "Your custom feed" (3.6, 3.8) have **no independent evaluation**; only one journalistic "实测" was found.
- **Evidence gap filled:** Do the 2024–26 generation of user controls actually diversify feeds, and for how long?

**Concept 2: "Exploration budget" autopilot (探索预算)**
- **What:** The user sets a weekly exploration budget, for example "20% of my feed from outside my top-3 topics". The tool (a) visualises the current share, (b) suggests or queues diverse items from curated sources, and (c) optionally performs Haroon-style **history injection** (2.7) by opening or watching selected videos in a background tab so the platform's model is nudged. It ends with a weekly "cocoon report".
- **Why new:** Unhook and News Feed Eradicator *remove* feeds (3.1–3.2). TikTok, IG and Douyin sliders are coarse, platform-controlled and not goal-based. Haroon's intervention was only tested on sock puppets.
- **Evidence gap filled:** Does user-driven, budgeted exploration change real users' feeds and self-reported diversity over weeks? (No real-user test was found.) Our simulator (shortlist item 5) gives a first *simulated* answer.

**Concept 3: Campus "bridging feed" for HKU (a Bluesky custom feed or course-forum plugin)**
- **What:** A feed that ranks posts or comments by **cross-group approval** (Community Notes-style matrix factorisation, 1.10), plus DPP diversity. Groups can be faculties, local vs non-local, or languages (粤/普/Eng). It is built on the Bluesky feed-generator starter kit (2.9) or as a plugin for a class discussion board.
- **Why new:** Bridging ranking has been tested in the US political context (PRC 1.11, Community Notes) but, as far as found, **not** in HK/Chinese-language or multilingual student communities. Bluesky's feed ecosystem lacks bridging feeds with published evaluation (2.9 notes creators lack feedback data).
- **Evidence gap filled:** Does bridging-based ranking increase cross-group exposure and perceived mutual understanding in a small, non-US, multilingual community? It can be run as a small class study.

---

## Items needing verification before citing (search budget ran out)
- LinUCB "12.5%" click lift (1.5); YouTube DPP numeric gains (1.3); Hulu online A/B (1.2).
- Piao et al. 2023 specific prevention strategies (1.13).
- Which Prosocial Ranking Challenge algorithm was most effective (1.11).
- Details of Algorithmic Mirror (3.12), Content Fuzzing (1.16), community-detection mitigation (1.16), and Cyclops (3.13).
- Nandu 实测 findings on 内容偏好调节 (2.12).
- One-sec / friction evidence (2.11): no URL found.
- "Breaking Filter Bubble: RL Framework of Controllable Recommender System" (Li et al. 2023) and Sukiennik 2025 LLM-agent short-video simulation (1.14): titles from a search snippet; no URL seen.
