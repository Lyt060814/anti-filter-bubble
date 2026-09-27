# Research D: Simulation models, public datasets, and existing anti-bubble tools
*For the HKU COMP1110 group project on filter bubbles / information cocoons (信息茧房). Compiled 2026-09-27.*

**How sources were checked.** Every item below has a URL or DOI that came up in a live web search or page fetch during this review. The environment blocked direct fetches of arxiv.org, PLOS, PMC, cac.gov.cn, msnews.github.io, grouplens.org and huggingface.co. So for many papers the summaries rest on search-engine abstracts and snippets, not the full text. Two tags mark where extra care is needed:
- **[BG]**: a detail (a formula, a field name, an exact count) that comes from my background knowledge and was *not* confirmed on a fetched page. Check it in the source before you cite it.
- **UNVERIFIED**: I could not confirm the item itself, or its authors, date or link.

---

## Part 1: Simulation and modelling work

### 1.1 Bounded-confidence opinion models (the "classic" foundations)

**Deffuant, Neau, Amblard & Weisbuch (2000). "Mixing beliefs among interacting agents." *Advances in Complex Systems* 3, 87–98.** DOI: https://doi.org/10.1142/S0219525900000078
- **Summary:** Each agent holds an opinion x between 0 and 1. At each step two random agents meet. If their opinions differ by less than a threshold ε (the "confidence bound"), both move toward each other by a fraction μ. A high ε ends in consensus. A low ε ends in several separate opinion clusters that never talk to each other.
- **Variables and rules [BG for the exact update]:** `if |x_i − x_j| < ε: x_i += μ(x_j − x_i); x_j += μ(x_i − x_j)`.
- **Outputs:** the number of final clusters, the cluster sizes, and the time to converge.
- **How our project could use it:** This is the simplest model to code first (about 20 lines of Python). It is the baseline to which we add a "recommender" rule.

**Hegselmann & Krause (2002). "Opinion dynamics and bounded confidence models, analysis and simulation." *JASSS* 5(3).** https://www.jasss.org/5/3/2.html
- **Summary:** This is the synchronous version. At every step, *every* agent moves to the average opinion of all agents within distance ε. The paper studies when groups reach consensus, polarise, or fragment.
- **How our project could use it:** An alternative baseline. It is easier to vectorise with NumPy, and it gives cleaner plots of opinion over time.

**Sîrbu, Pedreschi, Giannotti & Kertész (2019). "Algorithmic bias amplifies opinion fragmentation and polarization: A bounded confidence model." *PLOS ONE* 14(3): e0213246.** https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0213246
- **Summary:** This paper takes the Deffuant model and changes *who meets whom*. A platform-like "algorithmic bias" parameter (γ) makes agents more likely to be paired with someone who already thinks like them. The result: society fragments even at ε values where the original model predicts consensus, and convergence slows dramatically.
- **Variables [BG]:** ε (confidence bound), μ (how far agents move toward each other), and γ (bias). A partner j is chosen with probability ∝ |x_i − x_j|^(−γ). γ = 0 is the original random mixing.
- **Outputs:** the number of clusters, the spread of opinions (polarisation), and the time to converge.
- **How our project could use it:** This is our **best core simulation**. It needs only a change to one line of the Deffuant code, and a "γ slider" makes a clear demo of the algorithm's effect.

**Perra & Rocha (2019). "Modelling opinion dynamics in the age of algorithmic personalisation." *Scientific Reports* 9, 7261.** https://www.nature.com/articles/s41598-019-43830-2
- **Summary:** Agents sit on a social network and adopt opinions based on what their friends post. A filtering algorithm decides which friends' posts each user sees: random, most recent first, or posts matching the user's current opinion. Personalised filtering distorts how people perceive opinions and changes the outcome.
- **How our project could use it:** Adds a network layer. The team can compare three feed rules (random / chronological / personalised) with the same agents, which is a direct analogue of the "turn off personalisation" switch that Chinese regulation requires (see 3.10).

**Geschke, Lorenz & Holtz (2019). "The triple-filter bubble: Using agent-based modelling to test a meta-theoretical framework for the emergence of filter bubbles and echo chambers." *British Journal of Social Psychology*.** https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/bjso.12286. Code (NetLogo, MIT licence): https://github.com/janlorenz/TripleFilterBubble
- **Summary:** Filtering happens on three levels: the **individual** (confirmation bias), the **social** (friends share things), and the **technological** (the recommender). The authors run 12 scenarios. A striking finding: echo chambers form *even with no social or technological filter*, from confirmation bias alone, when information comes through a central channel that reaches much of the population.
- **Variables [BG]:** agents have a 2-D attitude position and a memory of up to about 20 "info-bits". The chance of accepting an info-bit falls with its distance from the agent's attitude (a "latitude of acceptance" D and a "sharpness" δ). The agent's attitude is the mean of its memory.
- **Outputs:** attitude clusters and the diversity of each agent's memory.
- **How our project could use it:** The browser version (`TripleFilterBubble_Web.nlogo`) runs in NetLogoWeb, so the team can demo it with no install. It also reminds us to separate *self-selection* from *algorithm* effects.

### 1.2 Recommender-system feedback-loop simulations

**Chaney, Stewart & Engelhardt (2018). "How algorithmic confounding in recommendation systems increases homogeneity and decreases utility." *RecSys '18*.** DOI: https://doi.org/10.1145/3240323.3240370 · arXiv: https://arxiv.org/abs/1710.11214
- **Summary:** When a recommender is retrained on data produced by users who were already following its recommendations, a feedback loop forms. The simulations show that this "confounded" training makes users' behaviour more alike (homogenisation) *without* making them better off (no gain in utility).
- **Variables and rules [BG]:** users and items have hidden "true preference" vectors. At each step a user picks from a recommended list, mostly by true utility. The recommender (popularity, content-based, matrix factorisation, social, random, or "ideal") is retrained on these choices.
- **Output metric [BG]:** mean **Jaccard similarity** between pairs of users' consumed item sets, relative to an ideal recommender. Also mean user utility.
- **How our project could use it:** Pairwise Jaccard similarity is a **simple, explainable "bubble" metric** that we can compute on simulated data *and* on KuaiRec.

**Jiang, Chiappa, Lattimore, György & Kohli (2019). "Degenerate feedback loops in recommender systems." *AIES '19*.** https://arxiv.org/abs/1902.10730
- **Summary:** A theoretical model of how a user's interest drifts as the system keeps showing them what they already like. It separates two effects. An **echo chamber** is the user's interests being reinforced. A **filter bubble** is the pool of candidate items shrinking. Both can make the system "degenerate", and continuous random exploration and a growing candidate pool slow this down.
- **How our project could use it:** Gives clean vocabulary for the report, and a justification for testing ε-greedy exploration in our simulation.

**Mansoury, Abdollahpouri, Pechenizkiy, Mobasher & Burke (2020). "Feedback loop and bias amplification in recommender systems." *CIKM '20*.** DOI: https://doi.org/10.1145/3340531.3412152
- **Summary:** Simulates many rounds of "recommend → user consumes → retrain" on real rating data. Popularity bias grows over the rounds: a few popular items dominate. It also shows that minority user groups get recommendations that drift further from their real tastes [BG: the paper's example is female users in MovieLens].
- **How our project could use it:** A template for a **MovieLens- or KuaiRec-based loop**: train a simple recommender, feed its top-k back in as new "clicks", and plot the Gini coefficient of item popularity over the rounds.

**Kalimeris, Bhagat, Kalyanaraman & Weinsberg (2021). "Preference amplification in recommender systems." *KDD '21*.** DOI: https://doi.org/10.1145/3447548.3467298 · Meta blog summary: https://research.facebook.com/blog/2021/08/when-do-recommender-systems-amplify-user-preferences-a-theoretical-framework-and-mitigation-strategies/
- **Summary:** A theoretical model where each time a user interacts with a recommended item, their preference narrows toward it. The paper shows when this "preference amplification" happens and proposes mitigation strategies.
- **How our project could use it:** Supports the claim that a user's taste itself changes, not just what they are shown. This justifies a user model in which preferences update after each video.

**Piao, Liu, Zhang, Su & Li (2023). "Human–AI adaptive dynamics drives the emergence of information cocoons." *Nature Machine Intelligence* 5, 1214–1224.** DOI: https://doi.org/10.1038/s42256-023-00731-4 · News: https://techxplore.com/news/2023-10-humanai-interaction-scenarios-cocoons.html
- **Summary:** A Tsinghua (Yong Li's lab) model that explicitly uses the term **"information cocoon"** (信息茧房). Cocoons emerge from the feedback loop between human choices and AI recommendations. The findings were tested on two large real-world datasets, and the paper sets out two scenarios that lead to cocoons plus strategies to prevent them.
- **How our project could use it:** The most directly relevant high-profile paper. It uses the Chinese framing, so it anchors our problem statement.

**Burghardt & Lerman (2022). "Emergent instabilities in algorithmic feedback loops." arXiv:2201.07203.** https://arxiv.org/pdf/2201.07203 (authors from memory: **UNVERIFIED**)
- **Summary (from search snippet):** In simulation, a *greedy* recommender ends up recommending a small set of items: item-popularity Gini is high and prediction error is higher. **ε-greedy** exploration gives a lower Gini and a lower Brier score (more accurate).
- **How our project could use it:** Evidence that **exploration is an antidote that need not cost accuracy**. This is a nice hypothesis for us to replicate.

**Kaminskas & Bridge (2016). "Diversity, serendipity, novelty, and coverage: A survey and empirical analysis of beyond-accuracy objectives in recommender systems." *ACM TiiS* 7(1).** https://research.ucc.ie/en/publications/diversity-serendipity-novelty-and-coverage-a-survey-and-empirical/
- **Summary:** The standard reference for how to *measure* what accuracy metrics miss. It covers diversity (e.g., intra-list distance), serendipity (relevant *and* unexpected), novelty, and catalogue coverage.
- **How our project could use it:** Our **metric dictionary**. Pick two or three of these metrics and define them precisely in the report.

**T-RECS (Lucherini et al.).** Python library for agent-based simulation of recommender systems. `pip install trecs`, MIT licence. https://github.com/elucherini/t-recs
- **Summary:** A ready-made Python framework for simulating users, items and recommenders over time, with pluggable metrics through `get_measurements()`. The accompanying paper was *not* confirmed on the page (**UNVERIFIED** citation).
- **How our project could use it:** A fallback if coding the loop from scratch takes too long. It is probably overkill for first-years, but its tutorial notebooks are good references.

### 1.3 LLM-agent simulations (2023–2026)

**Wang et al. RecAgent, "User Behavior Simulation with Large Language Model-based Agents." arXiv 2306.02552 (2023); *ACM TOIS* (2024/25).** https://arxiv.org/pdf/2306.02552 · DOI: https://doi.org/10.1145/3708985 · Code: https://github.com/RUC-GSAI/YuLan-Rec
- **Summary:** Each simulated user is an LLM agent with a profile, a memory (sensory, short-term and long-term) and actions: watch movies, chat with other agents, post. The repo lists **information cocoons** and conformity among its case studies. It uses MovieLens-1M items and needs an OpenAI-compatible API key.
- **How our project could use it:** Too heavy to reproduce. Cite it as the "state of the art". A cheap version is possible: 10–20 LLM "personas" choosing from a feed, run for a few rounds.

**Sukiennik, Wang et al. (2025). "Simulating Filter Bubble on Short-video Recommender System with Large Language Model Agents" (SimTok).** arXiv: https://arxiv.org/abs/2504.08742 · Semantic Scholar: https://www.semanticscholar.org/paper/Simulating-Filter-Bubble-on-Short-video-Recommender-Sukiennik-Wang/a5be5e3b13a889106f97973d41e59db15efc1e56 (full author list UNVERIFIED)
- **Summary:** Runs LLM agents, with profiles covering age, gender, city tier, personality and interests, against a recommender trained on real **short-video** data. It finds that demographic features and "category attraction" speed up homogenisation. The group is Tsinghua FIB-Lab.
- **How our project could use it:** The closest match to our **short-video / Douyin** angle. Its list of drivers (demographics, category attraction) can become toggles in our own simple model.

**Törnberg, Valeeva, Uitermark & Bail (2023). "Simulating social media using large language models to evaluate alternative news feed algorithms." arXiv:2310.05984.** https://arxiv.org/abs/2310.05984
- **Summary:** LLM personas built from American National Election Study data read news, post, like and comment on three simulated platforms with different feed algorithms. A "bridging" feed, which boosts posts liked across party lines, produced less toxic and more cross-party conversation [BG: finding from memory, check the abstract].
- **How our project could use it:** Shows that the team could compare **feed rules**, not only user behaviour.

**Larooij & Törnberg (2025). "Can We Fix Social Media? Testing Prosocial Interventions using Generative Social Simulation." arXiv:2508.03385.** https://arxiv.org/abs/2508.03385
- **Summary:** An LLM + agent-based model platform, with no engagement-ranking algorithm, still reproduced echo chambers, concentrated influence and amplified polarised voices. Six interventions, from chronological feeds to bridging algorithms, gave only modest gains and sometimes made things worse.
- **How our project could use it:** An important **counter-point for the report**: "just change the algorithm" may not be enough. User-side awareness tools are a complementary route.

**Yang et al. (2026). "Do Generative Recommenders Deepen the Information Cocoon? A Closed-Loop Simulation with LLM-powered User Simulators" (RecLoop).** https://arxiv.org/abs/2606.17707 (full author list UNVERIFIED; Shandong University per the search snippet)
- **Summary:** Newer "generative" recommenders keep broader item-level diversity than classic ID-based ones. But concentration still grows *inside* their semantic-code space, depending on how items are tokenised and on model size.
- **How our project could use it:** A single-sentence "future directions" point: cocoons persist across recommender generations.

**Feng et al. (2026). "Quantifying the Potential to Escape Filter Bubbles: A Behavior-Aware Measure via Contrastive Simulation." *AAAI-26* 40(17).** https://ojs.aaai.org/index.php/AAAI/article/view/38492 · Code: https://github.com/fengdifu24/bepmetric
- **Summary:** Proposes **Bubble Escape Potential (BEP)**. The same recommender is run with simulated users who lean "positive" and users who lean "negative", and their exposure is compared. This separates true confinement from good preference modelling. The repo reports that **mild random recommendations were ineffective** at relieving bubbles.
- **How our project could use it:** A simplified "contrastive" test: a user who clicks *everything* versus a user who skips a category. Does the system let them escape? Also, a small amount of randomness may not be enough.

**Other 2025–26 items seen in search results only (titles and links confirmed, contents not read):**
- PersonaAct: "Simulating Short-Video Users with Personalized Agents for Counterfactual Filter Bubble Auditing." https://arxiv.org/html/2601.22547
- "A Simulation Framework for Studying Systemic Effects of Feedback Loops in Recommender Systems." https://arxiv.org/pdf/2510.14857
- "Filter Bubbles in Recommender Systems: Fact or Fallacy – A Systematic Review." https://arxiv.org/pdf/2307.01221 (a useful review for the literature section; authors UNVERIFIED)

### 1.4 Plain-language explanation and a first-year implementation

**The common skeleton behind all of the models above:**

| Piece | Simple version for us |
|---|---|
| **Users** | N = 200–1000 agents. Each has an interest vector over K = 10 content categories (e.g., food, games, beauty, news, sport…), or a single opinion x ∈ [0, 1]. |
| **Items** | M = 2000 videos, each with one category (or an opinion position). |
| **Recommender** | Choose one: (a) random; (b) popularity; (c) "personalised", which shows categories in proportion to the user's past clicks; (d) personalised + ε-greedy, where with probability ε a random category is shown. |
| **User choice** | Click with probability = interest[category] (optionally with a confirmation-bias sharpness). |
| **Feedback / drift** | After a click, interest[category] += α (then renormalise). This is the preference amplification described by Kalimeris et al. |
| **Loop** | Repeat for T = 200 rounds. |
| **Metrics** | (1) **Shannon entropy** of each user's recent category mix (low = cocoon). (2) **Gini** of item or category exposure. (3) **Mean pairwise Jaccard** between users' consumed sets (homogenisation, as in Chaney et al.). (4) Total clicks = "engagement", to show the engagement–diversity trade-off. For opinion models: number of clusters and variance. |

**Minimal Python sketch** (NumPy + Matplotlib, about 40 lines; students can extend it):
```python
import numpy as np
rng = np.random.default_rng(0)
N, K, T, alpha = 500, 10, 200, 0.05

def run(eps):                      # eps = exploration rate (0 = pure personalisation)
    interest = rng.dirichlet(np.ones(K), N)        # true tastes
    history  = np.ones((N, K))                     # system's click counts (prior)
    ent = []
    for t in range(T):
        p_rec = history / history.sum(1, keepdims=True)
        explore = rng.random(N) < eps
        cat = np.where(explore, rng.integers(0, K, N),
                       [rng.choice(K, p=p) for p in p_rec])
        click = rng.random(N) < interest[np.arange(N), cat]
        history[np.arange(N)[click], cat[click]] += 1          # system learns
        interest[np.arange(N)[click], cat[click]] += alpha     # user drifts
        interest /= interest.sum(1, keepdims=True)
        share = history / history.sum(1, keepdims=True)
        ent.append((-(share * np.log(share)).sum(1)).mean())   # diversity
    return ent
# plot run(0.0), run(0.1), run(0.3) -> entropy vs. time
```
**Experiments one week of coding can support:** vary ε (exploration), α (how malleable users are), and the recommender type. Report the entropy over time, the final click-through (engagement), and the trade-off curve. As an extension, use Sîrbu's γ-biased Deffuant model for the "opinion" version and show the number of clusters against γ.

---

## Part 2: Public datasets

| Dataset | Size | Key fields | Licence / access | Bubble / diversity use |
|---|---|---|---|---|
| **KuaiRec** (Kuaishou) | small matrix 1,411 users × 3,327 videos, 4.68 M interactions, **99.6 % dense**; big matrix 7,176 × 10,728, 12.5 M interactions, 16.3 % dense | user_id, video_id, play_duration, video_duration, timestamp, **watch_ratio**; item_categories; caption + 3-level categories; social_network; user_features | CC BY-SA 4.0, via Zenodo | See below |
| **KuaiRand** (Kuaishou) | Pure: 27,285 users, 7,583 videos, 1.44 M rows (~184 MB); 1K: 1,000 users, 11.7 M rows; 27K: 322 M rows (~23 GB) | 12 feedback signals (click, like, follow, view time…), **`is_rand` flag for randomly exposed videos**, user and video features | CC BY-SA 4.0, Zenodo | See below |
| **MIND** (Microsoft News) | ~1 M users, >160 k English articles; MIND-small ~50 k users [BG] | behaviors.tsv (user, time, click history, impressions with click labels); news.tsv (category, subcategory, title, abstract, entities) [BG] | Free for research under Microsoft Research License Terms | See below |
| **MovieLens** (GroupLens) | 100K: 100,000 ratings, 943 users, 1,682 movies; ml-latest-small ~100 k ratings [BG]; up to 20M/32M | userId, movieId, rating, timestamp; genres; tags | Research/education use, no redistribution [BG, check README] | See below |
| **Tenrec** (Tencent) | ~5 M users, 140 M interactions, 4 scenarios (QK/QB video/article) | user, item, click, like, share, follow, **video category**, watching times, gender, age | Access terms UNVERIFIED (I believe an application form is needed) | See below |
| **MicroLens** (short-video platform, not named) | Full: 34 M users, 1 M videos, 1 B interactions; **MicroLens-100K**: 100 k users, 19,738 videos, ~719 k interactions | user–video (comment-based) interactions, raw titles, covers, audio, video | Download via recsys.westlake.edu.cn; no redistribution of modified copies; licence not stated | See below |
| **NineRec** | Bilibili source domain + 9 target sets, including Bili_Food/Dance/Movie/Cartoon/Music, **KU (Kuaishou), DY (Douyin)**, QB, TN | item text + cover image, user–item interactions | TPAMI 2025; licence UNVERIFIED | See below |
| **Qilin** (Xiaohongshu 小红书 + Tsinghua) | 15,482 users; recommendation 83 k train / 11 k test samples; search 44 k / 6 k; 2.2 M images, 6.9 M text notes | image-text and video notes, user history, clicks, app-level context | **MIT licence**, Hugging Face `THUIR/Qilin` | See below |

**Notes and "how our project could use it":**

- **KuaiRec** (Gao et al., CIKM '22). DOI: https://doi.org/10.1145/3511808.3557220 · https://kuairec.com · https://github.com/chongminggao/KuaiRec
  - **Why it matters:** the small matrix is *fully observed*, so we know how much every user would have liked every video. We can therefore simulate any recommender and measure the result honestly, with no "missing data" problem.
  - **How our project could use it:** Build our feedback-loop simulation on real Kuaishou data. Compare "personalised top-k" against "ε-greedy" on category entropy *and* on true watch_ratio, which makes the diversity–satisfaction trade-off measurable. **This is our top dataset pick.**
- **KuaiRand** (Gao et al., CIKM '22). DOI: https://doi.org/10.1145/3511808.3557624 · https://github.com/chongminggao/KuaiRand
  - **How our project could use it:** Compare how users react to *randomly inserted* videos versus algorithm-chosen ones. That is real-world evidence of whether "serendipity" injections get watched. KuaiRand-Pure (184 MB) is laptop-sized.
- **MIND** (Wu et al., ACL 2020). https://aclanthology.org/2020.acl-main.331/ · https://msnews.github.io
  - **How our project could use it:** Measure category entropy in users' click histories, and whether clicks shrink toward a few categories over time. This is the news-domain complement to the short-video data.
- **MovieLens** (Harper & Konstan 2015, *TiiS* 5(4)). DOI: https://doi.org/10.1145/2827872
  - **How our project could use it:** The easiest data for replicating Mansoury et al.'s popularity-bias loop. Tiny, clean, with genres, and it has endless tutorials.
- **Tenrec** (Yuan et al., NeurIPS 2022 Datasets & Benchmarks; first-author name UNVERIFIED). https://papers.nips.cc/paper_files/paper/2022/hash/4ad4fc1528374422dd7a69dea9e72948-Abstract-Datasets_and_Benchmarks.html · https://tenrec0.github.io/
  - **How our project could use it:** Chinese-platform video/article data with categories and true negatives. Probably more than we need; a backup option.
- **MicroLens** (Ni et al., CIKM '25; authors UNVERIFIED). DOI: https://doi.org/10.1145/3746252.3761655 · https://github.com/westlake-repl/MicroLens/
  - **How our project could use it:** Has raw titles and covers. With a free multilingual embedding model, content similarity could be measured instead of relying only on category labels.
- **NineRec** (TPAMI). DOI: https://doi.org/10.1109/tpami.2024.3373868 · https://arxiv.org/html/2309.07705
  - **How our project could use it:** The only public research set we found with **Bilibili and Douyin-sourced** interactions. Useful to show "the same analysis works on Chinese platforms".
- **Qilin** (Chen et al., SIGIR '25). DOI: https://doi.org/10.1145/3726302.3730279 · https://github.com/RED-Search/Qilin
  - **How our project could use it:** The only *Xiaohongshu* public dataset found. It covers lifestyle content (not politics), so it fits a "lifestyle bubble" angle, though the dataset is built around search.
- **Douyin via the ICME 2019 Short Video Understanding Challenge** (ByteDance). https://www.biendata.xyz/competition/icmechallenge2019/
  - Current downloadability is **UNVERIFIED**, so do not rely on it.
- **Bilibili**: no official interaction dataset beyond NineRec. VideoIC (danmaku comments, 4,951 videos, 5 M comments; https://dl.acm.org/doi/10.1145/3394171.3413890) is about comments, not recommendation.

### 2.1 Personal data exports ("analyse your OWN information diet")

**Google Takeout: YouTube `watch-history.json`.**
- **Fields:** each entry has `title` ("Watched …"), `titleUrl` (video URL), `subtitles` (channel name and URL) and `time` (ISO timestamp). **There is no watch duration and no category.** Categories and tags can be added through YouTube Data API v3 `videos.list` (snippet.categoryId) [BG].
- **Sources:** field guide https://playbackstats.com/guides/youtube-watch-history-json · parser https://github.com/seanbreckenridge/google_takeout_parser · example visualiser https://github.com/FabioMai/google-takeout-viz
- **How our project could use it:** Each team member exports their history and computes weekly channel/category entropy and "top-5 channel share". Plot the "cocoon index" over months. This gives a real, personal, ethically simple dataset (self-donated, with consent inside the team).

**TikTok "Download your data"** (Settings → Account → Download your data; JSON or TXT). The browsing history has entries like `{Date, VideoLink}`, plus likes, searches, and ad-interest categories. Guide: https://www.scrolldecoded.com/blog/tiktok-data-export-guide/
- **Caveat [BG]:** TikTok withdrew from Hong Kong in 2020, so HK students are more likely to have Douyin, YouTube, Instagram, Bilibili or Xiaohongshu accounts.

**Douyin 抖音**: 我 → ≡ → 设置 → 个人信息管理 → 申请个人信息下载. Watch history is visible in the app under 观看历史. Source: Douyin privacy policy https://sf3-cdn-tos.douyinstatic.com/obj/ies-hotsoon-draft/douyin_agreement/privacy.html (as summarised by search).
- Whether the downloaded copy *includes a machine-readable watch history* is **UNVERIFIED**. Test it early (week 1), because approval may take days.
- **How our project could use it:** If the export works, it is the first "own-data" analysis on a Chinese short-video platform we are aware of. If it does not, manual logging (screenshots or labelling 100 feed items per day) is the fallback.

**Data-donation research that uses these exports:**
- **Zannettou, Nemes-Nemeth, Ayalon, Goetzen, Gummadi, Redmiles & Roesner (2024). "Analyzing User Engagement with TikTok's Short Format Video Recommendations using Data Donations." *CHI '24*.** DOI: https://doi.org/10.1145/3613904.3642433 · PDF: https://homes.cs.washington.edu/~franzi/pdf/zannettou-tiktok-chi24.pdf
  - **Summary:** 347 users donated 9.2 M recommended videos. The median user watched 90 videos per day, about 27 min per day, and attention was stable at about 45 %. Daily time grew over each user's lifetime.
  - **How our project could use it:** Its method (download → strip identifiers → compute metrics) is a template for our own-data analysis.
- **Vombatkere, Mousavi, Zannettou, Roesner & Gummadi (2024). "TikTok and the Art of Personalization: Investigating Exploration and Exploitation on Social Media Feeds." *WWW '24*.** DOI: https://doi.org/10.1145/3589334.3645600 · https://arxiv.org/abs/2403.12410
  - **Summary:** Labels each feed item as *exploration* (new interest) or *exploitation* (existing interest). "Follow" was the strongest driver of personalisation, then "like", then watch time. Broad categories such as Food and Beauty got increasingly reinforced, and no rabbit-hole evidence was found for niche topics.
  - **How our project could use it:** The **explore/exploit labelling** is doable on our own YouTube or Douyin histories: "is this video's category/channel new to me in the last 7 days?"
- **"Wei et al."** A TikTok data-donation study with a first author named Wei was **not found (UNVERIFIED)**. Related items that were found: "Counting How the Seconds Count: Understanding Algorithm-User Interplay in TikTok via ML-driven Analysis of Video Content" (https://arxiv.org/pdf/2503.20030) and "Dynamics of algorithmic content amplification on TikTok", *EPJ Data Science* 2026 (https://link.springer.com/article/10.1140/epjds/s13688-026-00629-2). Authors of both are UNVERIFIED.
- **Data-donation tools:** OSD2F, Araujo et al., *Computational Communication Research* 2022 (https://github.com/uvacw/osd2f), and Port, Boeschoten et al., *JOSS* 2023 (https://pure.uva.nl/ws/files/142777920/Port.pdf). Both process the export locally, so only aggregates leave the device.
  - **How our project could use it:** A privacy-by-design pattern to copy: our tool computes metrics in the browser or notebook, and raw history never leaves the user's device.

---

## Part 3: Existing anti-bubble tools and products

| # | Tool | What it does | Evidence of effectiveness |
|---|---|---|---|
| 3.1 | **AllSides** https://www.allsides.com/media-bias/ratings · methods: https://www.allsides.com/about/media-bias-rating-methods | Rates the political bias of outlets (blind surveys, editorial panels, >100 k user ratings). Shows top stories from Left / Centre / Right side by side; the feed is ⅓ from each. | No peer-reviewed effect study found. Bias charts themselves are debated (Poynter: https://www.poynter.org/fact-checking/media-literacy/2021/should-you-trust-media-bias-charts/). |
| 3.2 | **Ground News "Blindspot"** https://ground.news/blindspot · https://ground.news/rating-system | Aggregates coverage of each story and shows its left/centre/right split. The Blindspot feed lists stories covered mainly by one side. A **personal "My News Bias" dashboard** shows the user's own diet (paid tier). | No independent evaluation found. Ratings are averaged from AllSides, Ad Fontes and MBFC. |
| 3.3 | **BuzzFeed "Outside Your Bubble"** (2017) https://www.buzzfeed.com/bensmith/helping-you-see-outside-your-bubble · Nieman Lab: https://www.niemanlab.org/reading/buzzfeed-tries-to-break-readers-out-of-their-social-media-bubbles/ | A human-curated module under widely shared articles summarising what people on Twitter, Facebook, Reddit and the web were saying. Later moved into a Facebook group. | No outcome evaluation; critics questioned it (https://thenextweb.com/opinion/2017/02/25/buzzfeeds-new-outside-bubble-disaster-making/). |
| 3.4 | **Balancer**, Munson, Lee & Resnick, *ICWSM 2013* https://ojs.aaai.org/index.php/ICWSM/article/view/14429 | A browser extension showing a tightrope-walker who tips over when the user's weekly political reading is unbalanced. | **Field experiment with a control group:** a modest shift toward balance (≈1–2 more weekly visits to opposing sites, or 5–10 to centrist sites). *The key evidence that self-monitoring feedback works a little.* |
| 3.5 | **Escape Your Bubble** (Chrome extension, ~2016–17) https://www.facebook.com/EscapeYourBubble/ | Injects friendly, positive articles about the opposing political side into the Facebook News Feed. | No evaluation found. It is probably defunct, since Facebook has changed. |
| 3.6 | **Read Across the Aisle** (Nick Lum, 2017) https://www.niemanlab.org/2017/03/a-news-app-aims-to-burst-filter-bubbles-by-nudging-readers-toward-a-more-balanced-media-diet/ · https://apps.apple.com/us/app/read-across-the-aisle/id1189851891 | An iOS/Chrome news app that tracks time spent on ~20 outlets across the spectrum; a slider shows your lean and nudges you to "read across". | No published evaluation found. Current availability is UNVERIFIED. |
| 3.7 | **Bobble**, Xing, Meng, Doozan, Feamster, Lee & Snoeren, *PAM 2014* https://link.springer.com/chapter/10.1007/978-3-319-04918-2_13 · PDF: https://cseweb.ucsd.edu/~snoeren/papers/bobble-pam14.pdf | A browser extension that re-runs your Google search from many vantage points and profiles, and shows how *your* results differ. | Measurement tool: it documented inconsistency and personalisation in results. It is not a behaviour-change trial. |
| 3.8 | **NewsCube**, Park, Kang, Chung & Song, *CHI 2009* https://dl.acm.org/doi/10.1145/1518701.1518772 | Automatically clusters articles on one event into different "aspects" or viewpoints and shows them together. | A user study reported that readers engaged with more varied aspects [BG: details in paper]. |
| 3.9 | **Nudges for news diversity** | **3bij3** by Loecherbach & Trilling (2020), *CCR* 2(1) (https://doi.org/10.5117/CCR2020.1.003.LOEC), is an open-source 3×3-grid news app for field experiments on recommender logics. **Mattis, Masur, Möller & van Atteveldt (2024)**, *New Media & Society* (https://journals.sagepub.com/doi/10.1177/14614448221104413), is a nudge taxonomy: gatekeeper, clickworthiness and model-citizen nudges. **"Nudges for news recommenders…"**, *Journal of Communication* 2025 (https://doi.org/10.1093/joc/jqaf019), is an experiment: prominent positioning **increased** selection, engagement and recall of environmental news, while reducing complexity did not. | Mixed but real effects. **Placement and prominence work; simplification alone doesn't.** |
| 3.10 | **Chinese platform features (2025)**, driven by CAC regulation | **Regulation:** 《互联网信息服务算法推荐管理规定》 Art. 17 (in force 2022-03-01) requires a non-personalised option or an easy switch-off (https://www.cac.gov.cn/2022-01/04/c_1642894606364259.htm). The 2024–25 "清朗·网络平台算法典型问题治理" campaign explicitly targets **"信息茧房"** (https://www.gov.cn/zhengce/zhengceku/202411/content_6989143.htm). **Resulting features:** Kuaishou **"信息茧房自我评估" + "一键破茧"**, which shows an interest portrait from feed content types, preferences and recommendation strength, then rebalances tags and frequency with one tap (https://finance.sina.com.cn/tech/roll/2025-05-21/doc-inexfvks0991614.shtml). Douyin's upgraded **"使用管理助手"** with a **内容偏好评估** visual of recent viewing. Xiaohongshu's **"内容偏好评估与调节" + "探索更多"**, showing category shares with per-category sliders (减少 / 默认 / 增加). WeChat Channels, Bilibili and Weibo also made adjustments (https://www.nbd.com.cn/articles/2025-05-22/3883838.html; https://news.qq.com/rain/a/20250226A095HX00). | **No independent evaluation found.** Only press and government reports. A Nandu (南方都市报) piece asks "用户自选内容推荐强度 能破信息茧房?" (https://ipaper.oeeee.com/ipaper/A/html/2025-04/29/content_4432.htm); its content was not read. |
| 3.11 | **Research prototypes for user awareness** | **Nagulendra & Vassileva (2014)**, *HT '14* (https://dl.acm.org/doi/10.1145/2631775.2631811): an interactive "bubble" visualisation of what a social feed filtered out, with controls; the user study reported better awareness. Also seen as titles only: "Algorithmic Mirror: Designing an Interactive Tool to Promote Self-Reflection for YouTube Recommendations" (https://arxiv.org/pdf/2504.16615) and "Compass: Continuously Aligning Social Media Feeds via In-Situ Reflections" (https://arxiv.org/pdf/2608.04274). | Small user studies. |
| 3.12 | **Evidence from outside the tools** | **Levy (2021)**, *AER* 111(3) (https://doi.org/10.1257/aer.20191777): randomly nudging Facebook users to subscribe to counter-attitudinal outlets **reduced negative feelings toward the other party**, but did not change opinions. Facebook's algorithm was *less likely* to show posts from those outlets even after users subscribed. **Larooij & Törnberg (2025)** (see 1.3): algorithm tweaks alone gave modest gains. | Supports "exposure helps attitudes a bit, but platforms work against it". |

**How our project could use Part 3:**
- The Balancer and Levy results give us a **hypothesis with evidence behind it**: showing people their own diet plus easy counter-exposure yields small but real shifts.
- The Chinese "茧房评估 / 一键破茧" features are a **perfect case study**. They exist and are mandated, but they are unevaluated, platform-controlled, and each works on only one app. Our project could design or test an independent, cross-platform version.

**What is missing:**
1. **Politics-only focus.** Almost all Western tools (3.1–3.9) are about US left/right news. Nothing addresses **lifestyle or entertainment short-video cocoons** (food, beauty, gaming, "study-with-me"), which is where Vombatkere et al. found the strongest reinforcement.
2. **No independent tools for Chinese-language platforms.** The only tools are the platforms' own self-assessments, which are opaque and run by the party that benefits from engagement.
3. **No cross-platform measurement.** Nobody combines YouTube + Douyin + Xiaohongshu into one "information diet" view.
4. **Weak or no measurement feedback over time.** Balancer did this in 2013. Current consumer tools (Ground News aside) do not show a *trend* ("your diversity fell 30 % this month").
5. **Almost no rigorous evaluation**, especially of the 2025 Chinese features.
6. **The "mild randomness is ineffective" finding** from the BEP paper and Larooij & Törnberg suggest naive "inject random content" is not enough. The *design* of exposure matters: prominence, relevance, and user agency.

---

## Synthesis: gaps and feasible technical cores (~300 words)

The modelling literature agrees on a single mechanism. A **feedback loop** runs from recommender to user choice to retraining, and users' own preferences drift along the way (Chaney; Jiang; Mansoury; Kalimeris; Piao). That loop homogenises consumption and shrinks diversity, often without raising real satisfaction. Exploration or randomness helps, but the newest work (BEP, AAAI-26; Larooij & Törnberg 2025) warns that *mild* randomness or single algorithm tweaks do little.

Empirically, fully observed and randomised-exposure data now exist for a Chinese short-video platform (**KuaiRec / KuaiRand, CC BY-SA**). That makes honest, laptop-scale simulation possible. On the product side, anti-bubble tools are overwhelmingly US-political, mostly unevaluated, and absent for lifestyle short-video and Chinese platforms. The 2025 platform features ("一键破茧") are opaque, single-platform and unevaluated. Balancer (2013) remains the rare tool with a controlled trial showing that **self-monitoring feedback** shifts behaviour a little.

**Feasible cores for 5 first-years in about 6 weeks** (pick one as the main core and one as support):

1. **Simulation core ("Cocoon Lab").** Build the Python loop in §1.4, then calibrate it on **KuaiRec's small matrix**. Compare personalised, ε-greedy and "category-quota" recommenders on category entropy, Jaccard homogenisation and true watch_ratio. Deliverable: trade-off curves plus an interactive slider demo (Streamlit or a Jupyter widget). *Weeks: 1 = learn the data; 2–3 = code; 4 = experiments; 5–6 = report.*
2. **Own-data analysis core ("Diet Mirror").** Each member exports their YouTube Takeout history (and Douyin if the export works). Compute weekly entropy, top-channel share and an explore/exploit ratio (following Vombatkere et al.), then visualise a personal "cocoon index" trend. Run a one-week self-experiment: baseline week vs. a week using the platform's 破茧/preference settings. Process everything locally, following the Port/OSD2F privacy pattern.
3. **Design core ("Bubble Meter" prototype).** A mock-up or simple web app that turns (2) into a Balancer-style feedback visual for *lifestyle* short video. It shows cross-platform diversity, and offers "one relevant-but-new" suggestions rather than random ones. Evaluate it with a small within-team or classmate usability test.

**Recommended combination:** use 1 or 2 as the technical core, with 3 as the user-facing output. This directly fills the gaps in Chinese short-video coverage, lifestyle content, and measurement feedback.
