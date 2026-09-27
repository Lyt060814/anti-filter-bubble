# Prior work on X's open-sourced For You algorithm: what already exists (research note, 2026-09-27)

For the HKU COMP1110 project on information cocoons and filter bubbles.

## How this was researched, and its limits

- **Sources used:** WebSearch result snippets, plus direct reads of github.com pages (the xai-org/x-algorithm README, `param.rs`, `vm-ranker/params.rs`, `vm-ranker/dpp.rs`, issues and PRs, and the commit list).
- **Blocked sites:** the network proxy blocked every other site, including arXiv, TechCrunch, Substack, 36kr, ppc.land, explainx.ai and dicemanorama.github.io.
- **Search budget:** the session-wide WebSearch budget (200 calls) ran out part-way through. As a result:
  - Section 3 (Chinese-language coverage) is thin.
  - Section 5 (other open algorithms: Bluesky, Mastodon, Reddit) could not be verified with URLs. Those items are listed only as **UNVERIFIED leads**.
- **What "verified" means here:** every item with a URL below was seen in a search result or fetched page. Details that came only from a search-engine summary are marked "(snippet)". Details read directly from GitHub are marked "(read on GitHub)".

---

## 1. History of the X/Twitter algorithm open-source releases

### 1.1 March 31, 2023: twitter/the-algorithm and twitter/the-algorithm-ml

- **Sources:**
  - README: https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md
  - Explainers:
    - Steven Tey, "How the Twitter Algorithm works in 2023": https://steventey.com/blog/twitter-algorithm
    - James Bachini: https://jamesbachini.com/twitter-algorithm/
    - InfoQ (Apr 2023): https://www.infoq.com/news/2023/04/twitter-algorithm/
    - TechCrunch (Mar 31, 2023): https://techcrunch.com/2023/03/31/twitter-reveals-some-of-its-source-code-including-its-recommendation-algorithm/amp
- **Summary:** Twitter released code for candidate sourcing, embeddings and the "Heavy Ranker" (a MaskNet neural ranker). The the-algorithm-ml README published the engagement weights as of Apr 5, 2023 (snippet):

  | Signal | Weight |
  |---|---|
  | fav (like) | 0.5 |
  | retweet | 1.0 |
  | reply | 13.5 |
  | good_profile_click | 12.0 |
  | reply_engaged_by_author | 75.0 |
  | negative_feedback_v2 | -74.0 |
  | report | -369.0 |

  The release did not include ad recommendations, trained production models or live tuning parameters.
- **Left open for us:** the 2023 weights give a baseline. The team can compare them with the 2026 weights, e.g. negative feedback -74 in 2023 vs "not interested" -43.2 in 2026, and reply 13.5 vs 5.0.

### 1.2 Criticism of the 2023 release as "transparency theatre"

- **Sources:**
  - Engadget, "What did Twitter's 'open source' algorithm actually reveal? Not a lot": https://www.engadget.com/what-did-twitters-open-source-algorithm-actually-reveal-not-a-lot-194652809.html
  - Fortune (Feb 22, 2023): https://fortune.com/2023/02/22/elon-musk-twitter-algorithm-transparency-open-source
  - NYU CSMaP, "What Can We Learn From Twitter's Open Source Algorithm?": https://csmapnyu.org/impact/news/what-can-we-learn-from-twitters-open-source-algorithm
  - Solomon Messing, "What can we learn from 'The Algorithm,' Twitter's partial open-sourcing": https://solomonmg.github.io/post/twitter-the-algorithm/
- **Summary (snippet):** critics said the release was incomplete, with no models, production endpoints or live parameters. They also said it did not explain why particular posts were up- or down-ranked. Around the same time, API price changes cut most researchers off from data needed to audit the system.
- **Left open for us:** the critique focused on *what was missing*. It did not ask what the published mechanisms imply for exposure diversity.

### 1.3 2025

- The only 2025 activity found was on the old repository. Issue #15985 on twitter/the-algorithm, "Remove out of network reply demotion" (erkinalp, Sep 10, 2025), was found via https://github.com/twitter/the-algorithm/issues?q=echo+chamber.
- **No 2025 code release by X was found.** This is UNVERIFIED: the search budget ran out before it could be checked thoroughly.

### 1.4 January 2026: xai-org/x-algorithm, first release

- **Sources:**
  - X Engineering post: https://x.com/XEng/status/2013471689087086804 ("We have open-sourced our new 𝕏 algorithm, powered by the same transformer architecture as xAI's Grok model")
  - TechCrunch (Jan 20, 2026), "X open sources its algorithm while facing a transparency fine and Grok controversies": https://techcrunch.com/2026/01/20/x-open-sources-its-algorithm-while-facing-a-transparency-fine-and-grok-controversies/
  - Engadget, "X's 'open source' algorithm isn't a win for transparency, researchers say": https://www.engadget.com/social-media/xs-open-source-algorithm-isnt-a-win-for-transparency-researchers-say-181836233.html
  - ppc.land: https://ppc.land/xs-algorithm-source-code-drops-what-it-reveals-about-the-platforms-feed-mechanics/
  - Glitchwire: https://glitchwire.com/news/x-open-sources-its-algorithm-again-10-things-you-need-to-know-about-how-your-fee/
  - Phoenix README: https://github.com/xai-org/x-algorithm/blob/main/phoenix/README.md
- **Summary (snippet):**
  - Musk announced the release on Jan 10, 2026. Code went public on Jan 19–20 under Apache-2.0. Snippets differ on the exact date (Jan 19 vs Jan 20).
  - It was a rewrite in Rust and Python with four parts:
    - Home Mixer (orchestration)
    - Thunder (in-memory store of in-network posts)
    - Phoenix (retrieval and ranking with a Grok-1-derived transformer and candidate-isolation attention)
    - Candidate Pipeline framework
  - The handcrafted heuristics of 2023 were replaced by a learned model.
  - Researchers quoted by Engadget said the release did not provide useful transparency. It had no weights and could not be run.
- **Left open for us:** at this stage there were no real weight values to analyse.

### 1.5 May 15, 2026: runnable pipeline

- **Sources:**
  - Pasquale Pillitteri: https://pasqualepillitteri.it/en/news/2594/x-algorithm-open-source-may-2026
  - thedeepfeed.ai, "X algorithm 2026 open-source release, inspected" (2026-05-16): https://www.thedeepfeed.ai/posts/2026-05-16-x-algorithm-phoenix-release/
  - Commit list (commit 0bfc279, May 15): https://github.com/xai-org/x-algorithm/commits/main
- **Summary (snippet):**
  - Added `phoenix/run_pipeline.py`, an end-to-end inference pipeline.
  - Added a mini pre-trained Phoenix model via Git LFS.
  - Added ads blending with brand safety, six new hydrators, and the Grox content-understanding system.
  - Changed about 18k lines across 187 files.
  - thedeepfeed notes the release still does not let you run or audit *X's production* algorithm.
- **Left open for us:** the mini model plus the runnable pipeline make small-scale simulation possible. **No one was found using it to study exposure diversity or cocoons.**

### 1.6 August 13–14, 2026: production weights, filtering stack, "Under the Hood"

- **Sources:**
  - README "Notable Updates" (read on GitHub): https://github.com/xai-org/x-algorithm
  - TechCrunch (Aug 13, 2026), "X open sources its ranking algorithm, letting users see if they've been 'shadowbanned'": https://techcrunch.com/2026/08/13/x-open-sources-its-ranking-algorithm-letting-users-see-if-theyve-been-shadowbanned/
  - Engadget: https://www.engadget.com/2236672/x-is-testing-a-tool-that-will-let-users-see-if-their-posts-have-been-shadowbanned/
  - TechBriefly (Aug 14, 2026): https://techbriefly.com/2026/08/14/x-expands-open-source-codebase-adds-transparency-tool/
  - TechRound, "Real Transparency Or PR Theatre?": https://techround.co.uk/business/x-just-open-sourced-its-algorithm-and-added-a-shadowban-checker-real-transparency-or-pr-theatre/
  - ETV Bharat: https://www.etvbharat.com/en/technology/x-algorithm-open-source-shadowban-transparency-tool-x-elon-musk-enn26081404733
  - WeRSM: https://wersm.com/x-opens-for-you-algorithm-shadowban-signals/
  - Trending Topics: https://www.trendingtopics.eu/x-open-sources-its-algorithm-and-reveals-what-it-takes-to-go-viral/
  - Studio Global ("key parameters stay hidden"): https://www.studioglobal.ai/discover/answers/what-open-source-transparency-initiative-did-x-announce-6a7e886910551e202b129941
  - TechTimes (Aug 17, 2026), on the Brazil election filter: https://www.techtimes.com/articles/324704/20260817/x-published-brazils-election-censorship-filter-code-indias-secrecy-law-prevents-this.htm
- **What the Aug 13 release added:** configuration parameters, including the action-blending weights, plus the code that decides whether a post is filtered out of For You. The new systems were:
  - the visibility-filtering engine (about 54 rules, snippet)
  - SimClusters as an out-of-network (OON) candidate source
  - VM-Ranker, which re-ranks with a DPP (determinantal point process, explained in 1.7)
  - the account-labelling systems Agatha, BDSM and user-cred-v2
  - Under the Hood, a tool that shows users the visibility-limiting labels on their account and posts
- **What the Aug 14 README note said:**
  - It clarified that weights scale *predicted probabilities*, not raw engagement counts.
  - It added `Brazil2026ElectionFilter`. This removes posts from accounts reported to Brazil's Electoral Court, unless the viewer follows the account. TechTimes says the filter holds 665 account IDs (snippet).

### 1.7 The published parameter values (read on GitHub)

Values below were read from https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs and https://github.com/xai-org/x-algorithm/blob/main/vm-ranker/params.rs. The second file also lists the weight table.

**Positive action weights**

| Action | Weight |
|---|---|
| Favorite (like) | 0.5 |
| Reply | 5.0 |
| Retweet | 1.0 |
| Quote | 5.0 |
| Share | 2.0 |
| ShareViaDm | 5.0 |
| ShareViaCopyLink | 20.0 |
| FollowAuthor | 4.0 |
| Click | 0.4 |
| OpenLink | 0.2 |
| Dwell | 0.05 |
| ContDwellTime | 0.004 |
| ProfileClick | 0.0 |
| PostUnexplored | 0.02 |

**Negative action weights**

| Action | Weight |
|---|---|
| NotInterested | **-43.2** |
| BlockAuthor | -31.2 |
| MuteAuthor | -58.8 |
| Report | -234.0 |
| NotDwelled | -0.02 |

**Other parameters**

| Parameter | Value | Note |
|---|---|---|
| BidirectionalFollowReplyWeightBoost | 15.0 | |
| AuthorDiversityDecay | 0.5 | |
| AuthorDiversityFloor | 0.25 | Issue #202 gives the resulting multipliers: 2nd post by the same author 0.625, 3rd 0.4375 |
| OonWeightFactor | 0.75 | Out-of-network discount |
| TopicOonWeightFactor | 0.5 | |
| NewUserOonWeightFactor | 0.00001 | Applies to users younger than NewUserAgeThresholdSecs |
| NewUserAgeThresholdSecs | 0 | So the new-user factor appears inactive (our reading) |
| WeightPerturbationSigma | 0.0 | No exploration noise |
| **DppTheta** | **0.65** | |
| DppMaxSelectedRank | 150 | |
| DppEnabled | true | |
| EnableAuthorDiversity | true | |

**The DPP (determinantal point process) re-ranker**, read on GitHub at https://github.com/xai-org/x-algorithm/blob/main/vm-ranker/dpp.rs:

- It is a greedy, Cholesky-based MAP (maximum a posteriori) DPP, which picks the post set that best balances score and variety.
- Each post's quality term is `exp(alpha·q)`:
  - `q = score / max_score`
  - `alpha = theta / (2(1−theta))`
- The kernel is `qf_i · qf_j · cos(embedding_i, embedding_j)`. This matches the Chen et al. 2018 "Fast Greedy MAP Inference for DPP" formulation: https://arxiv.org/pdf/1709.05135
- **Our calculation:** with theta = 0.65, alpha ≈ 0.93. The quality factor therefore varies by at most about 2.5× across the top-150 candidates. That is a fairly mild relevance-versus-diversity trade-off.
- Posts with missing embeddings are counted as a metric, not excluded.

### 1.8 September 18, 2026 and afterwards

- **Sources:** README (read on GitHub): https://github.com/xai-org/x-algorithm; Streamlinefeed: https://streamlinefeed.co.ke/news/x-under-the-hood-transparency-update-government-shadowban-2026
- **Summary:** Under the Hood reports now say whether an account or its posts were visibility-limited to comply with law.
- **Commit pattern:** after Aug 13 the commits are near-daily automated "Open-source X Recommendation Algorithm" syncs by a CI agent. The last one is on Sep 26 (4c5cfe8). One community PR was merged: #88, "Deduplicate in_network_ids before VF lookup" (Sep 2–3). This means **the parameters can drift from day to day**.
- The open issue #203, "Publish a plain-language changelog for param.rs changes", asks for exactly this to be documented.
- Commit list: https://github.com/xai-org/x-algorithm/commits/main

### 1.9 Other secondary histories and technical explainers (not individually verified)

- **Release histories:**
  - Keywords Everywhere, "every release of the xai-org/x-algorithm repo, dated and explained": https://keywordseverywhere.com/news/social-algorithm-updates/x-algorithm-open-source/
  - explainx.ai: https://explainx.ai/blog/x-algorithm-open-source-github-elon-musk-2026
- **Technical explainers:**
  - RankSaga, "From MaskNet to Grok · A Technical Read of xai-org/x-algorithm (2026)": https://ranksaga.com/blog/x-algorithm-2026/
  - Ajit Singh, system-design explainer: https://singhajit.com/system-design/x-twitter-for-you-algorithm/
  - dicemanorama, "X For You Algorithm — Deep Dive" (describes the DPP): https://dicemanorama.github.io/X-Algorithm-Explained/

---

## 2. Academic work

### 2.1 Directly about X's ranking and amplification

1. **Milli, Carroll, Wang, Pandey, Zhao & Dragan (Dragan is UNVERIFIED as an author), "Engagement, user satisfaction, and the amplification of divisive content on social media."** PNAS Nexus 4(3) pgaf062, March 2025. Preprint arXiv:2305.16941.
   - Links: https://academic.oup.com/pnasnexus/article/4/3/pgaf062/8052060 and https://arxiv.org/pdf/2305.16941
   - **What it found:** a preregistered audit comparing Twitter's engagement-ranked feed with a chronological baseline. The algorithm amplified emotionally charged, out-group-hostile political content, and users said they did not prefer these posts. A ranking based on users' *stated* preferences reduced this amplification.
   - **Left open for us:** it studied the 2023-era black-box feed. It did not use the published 2026 weights or the DPP, and it did not model feed dynamics over time (cocoon formation).

2. **Gauthier, Hodler, Widmer & Zhuravskaya, "The political effects of X's feed algorithm."** Nature, 2026, doi:10.1038/s41586-026-10098-2.
   - Links: https://www.nature.com/articles/s41586-026-10098-2 and CEPR summary https://cepr.org/voxeu/columns/how-xs-algorithm-shifts-political-attitudes
   - **What it found:** a field experiment in 2023 with 4,965 US users randomised to the algorithmic or chronological feed for about 7 weeks. Moving to the algorithmic feed raised engagement and shifted opinions in a conservative direction. For example, users were 4.7 percentage points more likely to prioritise Republican issues. Moving the other way (algorithmic to chronological) had no comparable effect.
   - Press coverage: The Conversation / phys.org, Feb 2026: https://theconversation.com/a-few-weeks-of-xs-algorithm-can-make-you-more-right-wing-and-it-doesnt-wear-off-quickly-276153
   - **Left open for us:** it treats the algorithm as a black box. It does not identify which code mechanism (OON discount, engagement weights, SimClusters) causes the effect.

3. **Ye, Luceri & Ferrara, "Auditing Political Exposure Bias: Algorithmic Amplification on Twitter/X During the 2024 U.S. Presidential Election."** FAccT '25.
   - Links: https://dl.acm.org/doi/10.1145/3715275.3732159 and https://arxiv.org/abs/2411.01852
   - **What it found:** 120 sock-puppet accounts (left, right, balanced, neutral) collected more than 9M tweets over six weeks. About 50% of timeline posts were out-of-network. Exposure was concentrated on a few high-popularity accounts. Both left- and right-leaning users saw more aligned content and less opposing content, which is **direct evidence of cocoon-like exposure on X**. Right-leaning users had the highest exposure inequality.
   - **Left open for us:** it is purely observational, from before the 2026 code. It has no link to parameters such as OonWeightFactor = 0.75 or the DPP.

4. **Efstratiou, Duskin, Starbird & Spiro, "Rabble-Rousers in the New King's Court: Algorithmic Effects on Account Visibility in Pre-X Twitter."** ICWSM 2026. arXiv:2512.06129.
   - Links: https://arxiv.org/abs/2512.06129 and https://ojs.aaai.org/index.php/ICWSM/article/view/42661
   - **What it found:** it replicates the finding that right-leaning accounts get more exposure in the algorithmic feed. The advantage appears to come from *behaviour the algorithm rewards* (agitating content, platform attention) rather than party. Legacy-verified accounts got less exposure.
   - **Left open for us:** the "behaviour rewarded" explanation could be tested against the 2026 weights. For example, reply 5.0 and quote 5.0 reward conversational or agitating posts.

5. **Graham & Andrejevic (QUT/Monash), 2024 working paper** on possible algorithmic boosts to Musk's account and Republican-leaning accounts after about July 13, 2024.
   - Links: TechPolicy.Press https://www.techpolicy.press/new-research-points-to-possible-algorithmic-bias-on-x/ and The Register https://www.theregister.com/2024/11/20/x_marks_the_spot_for
   - **Left open for us:** it is based on engagement metrics only, with no code-level explanation.

6. **Piccardi et al., "Reranking partisan animosity in algorithmic social media feeds alters affective polarization."** Science, Nov 2025.
   - Links: https://www.science.org/doi/10.1126/science.adu5584 and arXiv https://arxiv.org/abs/2411.14652v2
   - Companion Perspective, "Platform-independent experiments on social media": https://www.science.org/doi/10.1126/science.aec7388
   - **What it found:** a browser extension used an LLM to re-rank real X feeds for 1,256 users over 10 days before the 2024 election. Reducing or increasing antidemocratic attitudes and partisan animosity (AAPA) content shifted out-party animosity by more than 2 points on a 100-point scale.
   - **Left open for us:** it shows that re-ranking changes attitudes. It does not test X's *own* DPP or diversity knobs.

7. **"The Prosocial Ranking Challenge: Reducing Polarization on Social Media without Sacrificing Engagement."** arXiv:2603.19626, 2026. Authors UNVERIFIED.
   - Link: https://arxiv.org/pdf/2603.19626
   - **What it is:** alternative-ranker competition work. Details not read.
   - **Left open for us:** it offers comparison baselines for "anti-cocoon" rankers.

8. **"Revealing The Secret Power: How Algorithms Can Influence Content Visibility on Twitter/X."** arXiv:2410.17390. Authors UNVERIFIED.
   - Link: https://awesomepapers.io/recommender-systems/papers/2410.17390
   - **Status:** content not read. It is **UNVERIFIED** whether it uses the open-source code.

9. **Background on DPP diversity:**
   - Chen et al., "Fast Greedy MAP Inference for DPP to Improve Recommendation Diversity" (NeurIPS 2018): https://arxiv.org/pdf/1709.05135. This is the method X's dpp.rs appears to follow.
   - "Representation Online Matters" (Pinterest diversification, 2023): https://arxiv.org/pdf/2305.15534
   - "Diversity on the Go! Streaming DPPs" (WWW 2021): https://cs.stanford.edu/people/paulliu/files/www-2021-mic.pdf

### 2.2 Academic analyses *of the code itself*

- **None found.** No arXiv, ACM or SSRN paper was found that analyses the 2026 xai-org/x-algorithm code, or the Aug–Sep 2026 parameters, from any angle.
- For the 2023 release, the analyses found were blog-style pieces by academics, not peer-reviewed code audits:
  - NYU CSMaP
  - Solomon Messing
- Caveat: the search budget ran out before searching Google Scholar for "the-algorithm" code audits. Treat "none found" as **likely but UNVERIFIED**.

---

## 3. Blogs, practitioner analyses, GitHub discussion

### 3.1 Practitioner and "growth" blogs (Aug–Sep 2026)

These are almost all creator-growth oriented. None takes a cocoon or diversity angle.

- **ppc.land, "X gives copy-link shares a feed weight of 20, against 0.5 for likes":** https://ppc.land/x-gives-copy-link-shares-a-feed-weight-of-20-against-0-5-for-likes/ (lists the -43.2 / -31.2 / -58.8 / -234 negatives)
- **explainx.ai, "X Discloses Ranking Weights: A Report Costs 468 Likes":** https://explainx.ai/blog/x-algorithm-for-you-timeline-open-source-ranking-weights-august-2026 (the "equivalence" framing that the Aug 14 README warns against)
- **Substack, "Decoding the X Algorithm - the August 2026 Update":** https://profitandpurpose247.substack.com/p/decoding-the-x-algorithm-the-august
- **FrameOS, "How the X (Twitter) Algorithm Works in 2026, From the Code":** https://frameos.studio/blog/twitter-algorithm
- **Bhavik Sarkhedi, "X's Real Algorithm Weights: What the Source Code Says":** https://bhaviksarkhedi.com/guides/i-read-x-source-code/
- **OpenTweet:** https://opentweet.io/blog/x-algorithm-open-source-github-2026
- **Publora:** https://publora.com/blog/x-algorithm-open-source
- **Joe Youngblood:** https://www.joeyoungblood.com/social-media/x-com-open-sourced-its-for-you-algorithm-heres-what-creators-and-marketers-need-to-know/
- **Furkan Gözükara (Medium), "X's Algorithm Update Is Bigger Than It Looks":** https://medium.com/@furkangozukara/xs-algorithm-update-is-bigger-than-it-looks-a-deep-dive-into-the-latest-x-algorithm-commit-6bbdab3bb7db
- **Slím Boulahouech (Medium):** https://medium.com/@slim.boulahouech/they-just-open-sourced-the-x-algorithm-here-are-the-new-rules-for-viral-growth-aefbcfc84e76
- **unfair.so:** https://unfair.so/x-algorithm
- **Japanese note.com posts:**
  - Tomono: https://note.com/ztx_tomono/n/nb2c833798ee4?hl=en
  - Ogura: https://note.com/ogulinks/n/nf9650ef93883?hl=en
- **Growth-hacking repos that treat the code as a "how to go viral" manual:**
  - ceoguy/x-algorithm-skill: https://github.com/ceoguy/x-algorithm-skill
  - tang-vu/x-algorithm-playbook: https://github.com/tang-vu/x-algorithm-playbook
- **"Transparency Theater of X" (Trilogy AI Substack):** https://trilogyai.substack.com/p/the-transparency-theater-of-x. Date and author UNVERIFIED. It argues transparency progressed on one dimension while others stayed opaque or regressed (snippet).
- **Left open for us:** these pieces read the weights **from a creator's perspective** ("how do I get reach"), not a viewer's ("what range of content do I end up seeing").

### 3.2 Chinese-language coverage

- **36Kr (English edition), "Elon Musk Shocks with X's Open-Sourced Recommendation Algorithm: 1,600 GitHub Stars in Six Hours":** https://eu.36kr.com/en/p/3647519956717442. Covers the January 2026 release. Content not read.
- **Not reached:** 虎嗅 (Huxiu), 机器之心 (Synced), 知乎 (Zhihu) and CSDN analyses of the 2026 code were **not reached** (the proxy blocked them and the search budget ran out). This is an **UNVERIFIED gap in this note**. A team member with normal internet access should search 知乎/CSDN for "X 推荐算法 开源 2026 解读", "x-algorithm 信息茧房" and "DPP 多样性 X 推荐".

### 3.3 GitHub issues and PRs on xai-org/x-algorithm about diversity (read on GitHub)

The repo has about 33.4k stars and 5.4k forks.

**Key finding:** searches of the repo's issues for "bubble" and "echo chamber" returned **zero results**. Diversity is discussed only as *repetition* or *creator fairness*, never as *viewpoint or topic cocoons*.

**Issue #202, "Author diversity resets on every For You request, so the same author repeats across consecutive loads"** (aunysillyme, Sep 15, 2026). https://github.com/xai-org/x-algorithm/issues/202
- Author-diversity counts only exist within one request.
- Decay is 0.5 with a floor of 0.25, giving multipliers of 0.625 and 0.4375.
- It proposes seeding the counts with time-decayed history.
- **Left open for us:** it covers author repetition only, not topic or viewpoint repetition.

**PR #212, "Fix/202 cross request author diversity"** (Junyi-Zheng, Sep 20, 2026, open, no reviews). https://github.com/xai-org/x-algorithm/pull/212
- Adds `EnableCrossRequestAuthorDiversity` (off by default).
- Settings: 300 s window, 60 s half-life, weight 0.25, max count 5.
- Includes 37 tests.

**PR #83, "docs: propose cross-request semantic fatigue experiment"** (pranay0703, Aug 30, 2026, draft). https://github.com/xai-org/x-algorithm/pull/83
- An RFC to measure whether repeated exposure to *semantically similar* content across requests reduces engagement. It is positioned as complementary to the within-slate DPP.
- **This is the closest thing found to a "cocoon" analysis.** However, its goal is engagement fatigue, not information diversity, and it contains no data.

**PR #37, "Add experimental slate-level diversity reranking"** (therufet721, Aug 14, 2026, open). https://github.com/xai-org/x-algorithm/pull/37
- Adds hard caps: max 2 posts per author in a 20-post window.
- Adds semantic-adjacency constraints.
- Off by default.

**Issue #200, "Gate out-of-network reach on follower engagement RATE, not raw in-network volume"** (Sep 14, 2026). https://github.com/xai-org/x-algorithm/issues/200
- Cites: OON factor 0.75 (topics 0.5), about 1,200 in-network candidates for 35 slots, a cold-start threshold below 1k followers, and an "Aug 26 cold-start change".
- The angle is creator reach, not viewer diversity.

**Issue #201, "ProfileClickWeight is 0.0"** and **issue #203, "Publish a plain-language changelog for param.rs changes"** (both Sep 15, 2026). Listed at https://github.com/xai-org/x-algorithm/issues

**Issue #210, "Expose static account-level SimCluster affinities in under-the-hood exports"** (Sep 19, 2026). Listed at https://github.com/xai-org/x-algorithm/issues
- **Relevant for us:** SimCluster affinities are a measurable "cocoon coordinate".

**Tracking issue #45** (cmdr-chara, Aug 14, 2026). https://github.com/xai-org/x-algorithm/issues/45
- Indexes three ranking proposals:
  - #19: a verification-neutral UserCred prior
  - #22: cold-start smoothing
  - #44: "gated dwell-regret" default objective, https://github.com/xai-org/x-algorithm/pull/44 (the PR itself says it does not claim to optimise long-term outcomes)
- Also PRs #21 ("Make missing DPP embeddings deterministic") and #27 ("Bound VM Ranker DPP work by the server pool limit"). These are engineering fixes, not analyses of theta.

**Issues #79 and #80** (Aug 26, 2026) are about out-of-network discovery for adult-labelled creators. Not directly relevant.

**Old repo, twitter/the-algorithm (2023):**
- Issue #1760, "Echo chamber balancing" (Apr 10, 2023). https://github.com/twitter/the-algorithm/issues/1760
  - Proposes a 50/50 mix of agreeing and opposing posts, selected with NLP.
  - Got no responses.
- Issue #538 (need for a "Not Helpful" option)
- Issue #1496 (producers presenting to more than one community)
- Issue #15985 (Sep 2025, "Remove out of network reply demotion")
- All found via https://github.com/twitter/the-algorithm/issues?q=echo+chamber

---

## 4. Work linking X's algorithm to echo chambers and polarisation, or examining its diversity mechanisms

- **Empirical evidence of cocoon-like or polarising effects on X:**
  - Ye et al. (FAccT 2025): users see more aligned and less opposing out-of-network content
  - Gauthier et al. (Nature 2026): the algorithmic feed shifts attitudes
  - Milli et al. (PNAS Nexus 2025): amplifies divisive content
  - Piccardi et al. (Science 2025): re-ranking alters polarisation
  - Efstratiou et al. (ICWSM 2026): rewarded behaviours drive visibility
- **Mechanism-level examination of X's diversity code:** only the GitHub items above (#202, #212, #37, #83), plus a one-line description of the DPP in explainer blogs (dicemanorama, README).
- **Nobody found** has:
  - discussed whether DppTheta = 0.65 is "a lot" or "a little" diversity
  - noticed that the DPP operates on *Phoenix embeddings of posts*, which cluster by topic and style, so it diversifies within a slate but not across sessions
  - asked how the 0.75 OON discount interacts with SimClusters retrieval, which is community-based (and therefore cocoon-prone)
- Also found: a GitHub agent-based model of algorithmic bias in echo-chamber formation on Twitter, InPhyT/Algorithmic_Bias_in_Echo_Chamber_Formation (2023, generic opinion dynamics, not X's code): https://github.com/InPhyT/Algorithmic_Bias_in_Echo_Chamber_Formation. It is a method precedent for simulation.

---

## 5. "Read the code or intervene in the feed" precedents on other platforms

Verified with URLs:

- **Piccardi et al. (Science 2025) and the Science Perspective on "platform-independent experiments"** (links in 2.1). A method precedent for studying feeds without platform cooperation.
- **Twitter 2023 code readings** by NYU CSMaP and Solomon Messing (links in 1.2). Academics reading ranking code to reason about political effects.
- **Pinterest "Representation Online Matters"** (https://arxiv.org/pdf/2305.15534). An industry paper describing a production diversification system, including DPP-style approaches. A precedent for reasoning about diversity re-rankers.

**UNVERIFIED leads** (not confirmed with a URL this session; verify before citing):

- Huszár et al., "Algorithmic amplification of politics on Twitter", PNAS 2022 (Twitter's internal study).
- Bluesky: open "custom feed" generators (AT Protocol feed-generator starter kit) and academic studies of Bluesky feed diversity (2024–2025).
- Mastodon: reverse-chronological, no algorithmic ranking (a design contrast rather than code to analyse).
- Reddit: the old open-sourced "hot" ranking formula, often explained in blogs (e.g. Amir Salihefendic's 2010-era write-up).
- Meta 2023 US 2020 election studies in Science/Nature (Guess et al., Nyhan et al.) on chronological feeds and reducing like-minded sources.
- Twitter/X Community Notes studies (e.g. its bridging-based ranking; Wojcik et al. 2022). The team asked about these, but they were not verified here.

---

## 6. Gap analysis (about 300 words)

**Has anyone analysed the Aug–Sep 2026 X code from an information-cocoon perspective?** As far as this search could see, **no**.

- **Coverage of the Aug 13 release was of three kinds:**
  - news (TechCrunch, Engadget, TechRound), focused on shadowban transparency
  - creator-growth blogs, focused on "copy-link = 20", "report = -234" and so on
  - GitHub contributors, focused on author repetition (#202, #212), slate caps (#37), creator reach (#200) and engagement fatigue (#83)
- **The peer-reviewed evidence on X and polarisation** (Milli 2025, Ye 2025, Piccardi 2025, Gauthier 2026, Efstratiou 2026) all treats the algorithm as a **black box**. None of it maps its findings onto the now-public parameters.
- **No paper, blog or issue was found that:**
  - simulates cocoon formation using X's *actual* weights and DPP settings
  - separates the cocoon-producing mechanisms from the anti-cocoon ones
- The cocoon-producing mechanisms are the engagement-weighted blend (reply 5, quote 5, share-via-copy-link 20, bidirectional-follow reply boost 15), the 0.75 out-of-network discount, SimClusters retrieval, and WeightPerturbationSigma = 0 (no exploration noise).
- The anti-cocoon mechanisms are the DPP with theta = 0.65 over the top 150 candidates, author decay of 0.5 with a 0.25 floor, the new-author boost, PostUnexplored = 0.02, and the negative weights.

**Specific open questions a first-year team could tackle:**

1. **Simulating cocoons with X's real weights.** Build a toy agent model or a small `run_pipeline.py` experiment. Track topic entropy and SimCluster concentration over many sessions. Compare the production parameters against ablations: DPP off, OON factor = 1.0, author diversity off.
2. **Sweeping DPP theta.** alpha = theta/(2(1−theta)), so theta = 0.65 gives alpha ≈ 0.93 and at most a ~2.5× quality spread. Sweep theta from 0 to 0.95 and measure within-slate diversity versus across-session diversity. This tests whether a per-request DPP can counter a cocoon at all. PR #83 argues it cannot, but gives no data.
3. **How "not interested" propagates.** -43.2 multiplies a *predicted* probability. Does one "not interested" click suppress the whole topic or cluster (a cocoon *narrowing*), or only that author? The code shows no explicit topic-level suppression beyond the Phoenix model's learned history. Compare how block and mute act as hard filters.
4. **Cross-request memory.** Quantify how much the #212-style history window would reduce repetition. Then propose a *topic*-level version.
5. **Parameter drift.** With near-daily CI syncs, track how `param.rs` changes over time. This responds to issue #203.
