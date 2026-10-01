# CODE MAP: filter-bubble ("information cocoon") mechanisms in X's open-sourced For You algorithm

Repo: https://github.com/xai-org/x-algorithm, **commit `b79b947` (2026-10-01)**. `home-mixer/params/param.rs:1` says *"mirrored from config feature-switch defaults; last sync 2026-09-30T16:00:40Z"*. All paths are relative to the repo root, and **all file:line references point to commit `b79b947`**. I read the code but did not modify or run anything in the repo.

> **Update 2026-10-01.** This map was first written against commit `4c5cfe8` (2026-09-26, param sync 2026-09-25). It has been re-checked line by line against `b79b947`; every line reference was moved to the new commit and checked to point at the same code. What changed in between:
>
> | Commit date | Change | Effect on cocoons | Section |
> |---|---|---|---|
> | 09-29 | `NotInterestedWeight` −43.2 → **−47.52** (+10%) | negative feedback pushes harder | 1.1, 1.3, (b), (e) |
> | 09-29 | `ClickWeight` 0.4 → 0.3; `ContClickDwellTimeWeight` 0.0 → 0.4 | engagement mix shifts toward time spent after a click | 1.1, 1.3 |
> | 09-30 | `EnableColdStartThompsonSampling` false → **true** | random exploration among small creators is now on | 1.4, 5 |
> | 09-30 | Cold-start eligibility: follower cap 1,000 → 50,000; max post age 48 h → 2 h; impression threshold 1,000 → 200; position ratio 0.85 → 0.97 | lift goes to fresh, little-seen posts from a much wider set of authors | 1.4, (b) |
> | 09-30 | `PhoenixColdStartMaxResults` 0 → **200** | a cold-start retrieval path now adds up to 200 candidates | (a), 5 |
> | 09-30 | New `PhoenixRetrievalExcludeSeenPosts` (default false) | optional: retrieval skips already-seen posts | 5 |
> | 09-30 | MoE "arm gating" that zeroed some retrieved candidates (`author_policy_zeroed`) removed | those candidates now keep their scores | 1.4 |
> | 09-30 | `home-mixer/util/composition.rs` deleted; `Composition` now imported from an external library | the diversity-metric formulas are no longer visible in the repo | 5, (e) |
>
> Unchanged: DPP (θ = 0.65, pool 150), author-diversity decay 0.5 / floor 0.25, OON factor 0.75, mutual-follow reply boost +15, the 1024-action history, the 30-day feedback TTL, and the absence of a hard "not interested" filter. Earlier history: `vm-ranker/params.rs` (DPP, author diversity, OON) first appeared on 2026-09-23, `xai-value-model/scoring.rs` on 09-24, and the diversity-stats side effect on 09-15. Parameters are synced near-daily, so cite the commit.
>
> Also corrected in this pass: references to `home-mixer/params/config.rs` and `vm-ranker/main.rs` pointed to older versions of those files (both changed on 09-22/23) and are fixed below.

**Legend**
- **[V]**: verified in code. The file:line and a short quote are given.
- **[I]**: my interpretation or inference. It is not literally in the code.
- **[U]**: unknown or not in the repo. See section (f).

---

## (a) Pipeline diagram (For You request, default params)

```
                         FOR YOU REQUEST (viewer u)
                                   |
 1. QUERY HYDRATION  (home-mixer/candidate_pipeline/phoenix_candidate_pipeline.rs:231-280)
    - scoring_sequence  : last <=1024 user actions (UAS, "DENSE_WITH_LONG_DWELL")  -> Phoenix ranker input
    - retrieval_sequence: last <=1024 user actions                                  -> Phoenix retrieval input
    - followed / blocked / muted user ids, muted keywords, seen-post bloom filters,
      explicit+implicit engagement signals (<=15 most recent per type)             -> SimClusters seeds
                                   |
 2. CANDIDATE SOURCES (parallel; sources vec at phoenix_candidate_pipeline.rs:322-330)
    IN-NETWORK  Thunder:   newest posts of followees, <=1200 (param.rs:23-28), recency only
    OUT-OF-NET  Phoenix retrieval (two-tower ANN on user history), <=1000 (param.rs:4-9)
    OUT-OF-NET  SimClusters ANN: posts similar (cos>0.5) to recently engaged posts, <=800
    OUT-OF-NET  Phoenix cold-start retrieval: <=200 (param.rs:16-21; ON since 2026-09-30)
    (TweetMixer, PhoenixMOE, PhoenixTopics: OFF by default)
                                   |
 3. CANDIDATE HYDRATION: in_network flag, mutual-follow flag, text, author, counts, topics, SIDs
                                   |
 4. PRE-SCORING FILTERS (hard removals; :358-386)
    dup | core-data | age>48h | self | OON replies/RTs | OON NSFW simclusters | RT dedup |
    subscription | previously SEEN (x2) | previously SERVED | MUTED KEYWORD | BLOCK/MUTE author |
    Brazil election | video | TopicIds (topic/excluded-topic requests) | NewUserMinEngagement(off) |
    InventoryHoldout(off) | FavHoldout(off)
                                   |
 5. SCORING
    PhoenixScorer: transformer -> P(action) for ~25 actions per candidate (candidates isolated)
    VMRanker (home-mixer/scorers/vm_ranker.rs):
       local: weighted sum + new-author cold-start lift  (fallback if RPC fails)
       RPC -> vm-ranker service (vm-ranker/scoring/mod.rs:31-79):
           value model = weighted sum -> offset -> cold-start lift ->
                         x author-diversity decay (0.5^k, floor .25) x OON discount (0.75)
           DPP greedy MAP over top-150, theta=0.65, multimodal 1024-d post embeddings:
                         selected posts keep their score, everyone else -> score 0
                                   |
 6. SELECTION: TopKScoreSelector keeps top 50 by score (params/config.rs:17)
                                   |
 7. POST-SELECTION: visibility filtering (VFFilter, AncillaryVF), DedupConversation
    -> truncate to RESULT_SIZE = 35 posts (params/config.rs:18; candidate-pipeline/candidate_pipeline.rs:143-145)
                                   |
 8. BLENDING: ads, Who-to-Follow at slot 6 (config.rs:29), prompts ...
                                   |
 9. USER ACTS (like / dwell / "not interested" / mute ...) -> logged -> becomes next request's
    user action sequence (FEEDBACK LOOP: this is where a cocoon can form or dissolve)
```

---

## 1. Scoring: weights and the exact formula

### 1.1 Action weights (home-mixer/params/param.rs; identical defaults duplicated in vm-ranker/params.rs:3-126) [V]

| Action head | Param (param.rs line) | Weight |
|---|---|---|
| favorite | FavoriteWeight :302 | 0.5 |
| reply | ReplyWeight :303 | 5.0 |
| reply boost if mutual-follow original post | BidirectionalFollowReplyWeightBoost :304-309 | **+15.0** (so 20 total) |
| dwell boost if mutual-follow | BidirectionalFollowDwellWeightBoost :310-315 | 0.0 |
| retweet/repost | RetweetWeight :316 | 1.0 |
| photo expand | :317-322 | 0.05 |
| video open | :323-328 | 0.07 |
| click | ClickWeight :329 | **0.3** (was 0.4 until 09-29) |
| open link | :330 | 0.2 |
| profile click | :331-336 | 0.0 |
| video quality view (VQV) | VqvWeight :337 | 0.0 |
| share | :338 | 2.0 |
| share via DM | :339-344 | 5.0 |
| share via copy link | :345-350 | **20.0** |
| dwell (binary) | DwellWeight :351 | 0.05 |
| quote | :352 | 5.0 |
| quoted click | :353-358 | 0.05 |
| quoted VQV | :359-364 | 0.0 |
| follow author | FollowAuthorWeight :365-370 | 4.0 |
| post "unexplored" | PostUnexploredWeight :371-376 | 0.02 (in-network only) |
| continuous dwell time | ContDwellTimeWeight :377-382 | 0.004 (per unit of predicted dwell time) |
| continuous click-dwell time | ContClickDwellTimeWeight :383-388 | **0.4** (was 0.0 until 09-29; per unit of predicted dwell after a click) |
| **not interested** | NotInterestedWeight :390-395 | **-47.52** (was -43.2 until 09-29) |
| block author | :396-401 | -31.2 |
| mute author | :402-407 | -58.8 |
| report | ReportWeight :408 | -234.0 |
| not dwelled | :409-414 | -0.02 |

`home-mixer/scorers/value_model.rs:50` also logs `active_secs_5m_residual_norm` with weight 0.0.

The code comment at param.rs:273-301 matters for interpretation [V]: *"Each weight multiplies the *predicted* probability of that action ... the weights do not multiply raw engagement counts"*, and *"the baseline probability of a Report is more than 1000x lower than a Like, so it's weighted more"*.

### 1.2 Weighted sum [V] `xai-value-model/scoring.rs:65-119`

```
S_raw = Σ_a  w_a(candidate) · P̂_a            (missing prediction -> 0; scoring.rs:57-59)
```

Special cases:
- `vqv` weight only if the video is long enough (`vqv_eligible`, min 10 s: param.rs:552-557). The weight is 0 anyway.
- **Reply weight** = 5 + 15 = 20 when `bidirectional_boost_eligible`: `!is_reply && !is_retweet && is_mutual_follow_author` (xai-value-model/inputs.rs:18-20; weights.rs:78-85). Mutual follow means the viewer follows the author *and* the author follows the viewer (home-mixer/candidate_hydrators/bidirectional_follow_hydrator.rs:60-61).
- **PostUnexplored** weight is applied **only to in-network candidates**: `let post_unexplored_weight = if candidate.in_network == Some(true) { weights.post_unexplored } else { 0.0 };` (scoring.rs:81-85).

**What does "unexplored" mean?** [V] It is a *training label* that Phoenix learns to predict. It is computed in `phoenix/xrex/data/recsys/recsys_batch.py:57-85`. A post counts as unexplored when all three hold:
- it is an original post (not a reply);
- it is at most 24 h old (`EXPLORATION_WINDOW_HOURS = 24.0`);
- `view_count < 0.03 · followers · (1 - e^{-λ·age}) / (1 - e^{-λ·24})`, where λ = ln2 / 8 h (`EXPLORATION_REACH_TARGET_FRACTION = 0.03`, `EXPLORATION_HALF_LIFE_HOURS = 8.0`).

So the post has reached fewer than about 3% of its author's followers compared with a saturating target curve. It is enabled for the prod ranking config (phoenix/xrex/configs/xrecsys.py:265, `_home_direct_packed_base`: `"compute_post_unexplored_label": True`) and disabled in the nano config (`"compute_post_unexplored_label": False` in `home_direct_packed_nano`).
[I] This is a small "help under-distributed posts from people you follow" term. It is a mild **widening within your own network**, not toward new topics. Its weight of 0.02 is tiny.

### 1.3 Offset and normalisation [V] `scoring.rs:121-130`, `weights.rs:4,45-76`

```
NEGATIVE_SCORES_OFFSET = 0.001
if S_raw >= 0:  S = S_raw + 0.001
else:           S = (S_raw + NegSum) / TotalSum · 0.001        # squashes negatives into [0, 0.001)
PosSum  = sum of the 18 positive "probability" weights = 43.24 (excludes cont_dwell_time,
          cont_click_dwell_time and the bidirectional boost; weights.rs:45-64)
NegSum  = 47.52+31.2+58.8+234+0.02 = 371.54   (weights.rs:66-72)
TotalSum = 414.78
(before 09-29: PosSum 43.34, NegSum 367.22, TotalSum 410.56)
```

[I] Every net-negative post lands below every net-positive post, and the order is preserved among negatives. There is no per-request normalisation such as softmax or dividing by the max. DPP later divides by the max score (section 2).

### 1.4 Post-fusion multipliers and where they really run

**The question: is author diversity disabled?** [V]
- **home-mixer local path**: `home-mixer/scorers/value_model.rs:40-44` sets `enable_author_diversity: false, author_diversity_decay: 1.0, author_diversity_floor: 1.0, oon_rescore_in_network_replies_retweets: false`. These weights are used only for `local_scores` (home-mixer/scorers/vm_ranker.rs:59-75): the per-candidate `weighted_score` plus the cold-start lift. The local scores are **served only as a fallback when the vm-ranker RPC fails** (vm_ranker.rs:107-113: `"VMRanker rank failed; serving local weighted scores"`). In that fallback there is **no author diversity and no OON discount**.
- **Normal path**: home-mixer sends `compute_value_model: true` and `value_model_id: "dpp"` (home-mixer/scorers/vm_ranker_request.rs:35-38). vm-ranker then builds weights from **its own** params (`vm-ranker/scoring/value_model.rs:61-104`):
  - `EnableAuthorDiversity = true` (vm-ranker/params.rs:139-144)
  - `AuthorDiversityDecay = 0.5` (:145-150)
  - `AuthorDiversityFloor = 0.25` (:151-156)
  - `EnableOonRescoreForInNetworkRepliesRetweets = true` (:157-162)
  - `MultiplierPreOffset = false` (:163-168)

  It calls `compute_value_scores` (vm-ranker/scoring/value_model.rs:150).

  **Conclusion: author diversity IS active in production-default config, but it is implemented in vm-ranker, not in home-mixer.**

The home-mixer value_model.rs values are a misleading red herring. Confidence is high, with one caveat: vm-ranker/params.rs has no "last sync" header like param.rs, so its defaults may be less authoritative (see (f)).

**Order of operations** (MultiplierPreOffset = false path) [V] `scoring.rs:242-282`:

```
weighted_i = offset(S_raw_i)                                  # 1.3
adjusted   = apply_cold_start_decisions(weighted)             # scoring.rs:223-240
             - one candidate may be lifted: max(score, sorted_weighted[rank])
             (the MoE arm-gating step that zeroed some candidates was removed on 09-30)
k_i        = number of candidates by the same author with a higher adjusted score, counted
             over the WHOLE candidate pool, not just the 35 served (author_pool_counts, :147-164)
author_mult_i = (1 - floor)·decay^k_i + floor = 0.75·0.5^k + 0.25          (:143-145)
               k=0:1.0  k=1:0.625  k=2:0.4375  k=3:0.344  k=4:0.297  ->0.25
oon_mult_i = effective_oon_weight if OON, or if in-network reply/retweet (flag true), else 1 (:166-175)
final_i    = adjusted_i · author_mult_i · oon_mult_i                         (:274-281)
```

**Out-of-network discount** [V] `vm-ranker/scoring/value_model.rs:106-130`:
- `effective_oon_weight = OonWeightFactor = 0.75` (params.rs:175-180);
- for topic requests it is `TopicOonWeightFactor = 0.5` (:169-174);
- for "new users" it would be `NewUserOonWeightFactor = 0.00001` (:187-192). That branch requires account age below `NewUserAgeThresholdSecs = 0` (:181-186) and at least 5 follows, so **it is effectively disabled**.

[I] 0.75 is a fixed 25% handicap on every post from outside your follow graph, and on in-network replies and reposts.

**New-author boost / "cold start"** [V] `home-mixer/scorers/author_cold_start.rs`. It is computed in home-mixer and passed to vm-ranker as `cold_start_lift_to_rank`.
- Eligible post (:176-181, :284-297), with values as of 2026-09-30 (previous values in brackets):
  - original post (not a reply or retweet);
  - `author_followers_count <= 50,000` (`ColdStartFollowerCap`, param.rs:477-482) [was 1,000];
  - post age at most **2 h** (`ColdStartMaxPostAgeSecs = 7200`, param.rs:483-488) [was 48 h];
  - post `view_count_on_home < 200` (`ColdStartImpressionThreshold`, param.rs:459-464) [was 1,000];
  - current position among non-zero scores `< 0.97·N` (`LowImpressionsMaxPositionRatio`, param.rs:490-495) [was 0.85].
  - [I] Net effect of the 09-30 change: the lift no longer targets only small accounts (≤1k followers) but almost any author's **very fresh, barely-seen** post, so it acts more like "new-post exploration" than "small-creator exposure".
- Target rank = `random_range(15..16)`, which is always 15. That means **at most one post per request** gets `score = max(score, 16th-best score)` (:204-214, :318-319; `ColdStartSlotMin/Max = 15/16`, param.rs:465-476).
- **Since 2026-09-30 the chosen post is picked by Thompson sampling** (`EnableColdStartThompsonSampling = true`, param.rs:503-508; was false). For every eligible post a reward is drawn from Beta(0.75 + favs, 49.25 + views − favs) (`ColdStartBetaAlpha0/Beta0`, param.rs:509-520); the `ColdStartTsTopK = 2` posts with the highest draws are kept, and of those the one with the higher model score is lifted (:231-271, :299-308). Before 09-30 it was simply the highest-scoring eligible post (`pick_by_score`).
- [I] This is the first **random exploration switched on by default** in the ranking path. It is small (at most one post per request) and works at the post level, not the topic level.
- [I] The lift happens *before* the OON ×0.75 and author-diversity multipliers, so a lifted OON post can slip below rank 16 again.

**Per-user weight perturbation** [V] `xai-value-model/weights.rs:96-104`: each weight is multiplied by `exp(±σ)`, with a per-user sign from md5. σ = `WeightPerturbationSigma = 0.0` (vm-ranker/params.rs:127-132), so it is **off**. [I] This is an exploration/AB hook.

---

## 2. vm-ranker DPP re-ranker (`vm-ranker/dpp.rs`, `vm-ranker/scoring/dpp_model.rs`, `vm-ranker/params.rs`)

### 2.1 Verified algorithm [V]

- **Pool**: sort candidates by value-model score and keep the top `max_selected_rank` (dpp_model.rs:70-78; dpp.rs:46-56). The param is `DppMaxSelectedRank = 150` (params.rs:206-211); the CLI default is 100 (args.rs:24-25).
- **Embeddings**: 1024-d multimodal post embeddings from `EmbeddingStore` (`get_mm_client(0, dim, false)`, embedding_store.rs:20; `--embedding-dim` default 1024, args.rs:27-28).
  - Retweets use the original post's embedding (dpp_model.rs:80-84).
  - **A post whose embedding is missing gets a random unit vector** (dpp_model.rs:23-37, :47).
  - [I] According to phoenix/reference/README.md:111-122 these "v5" MM embeddings come from a Qwen3-VL-Embedding model truncated to 1024-d, so they encode content and topic.
- **Quality**: `q_i = exp(α · s_i / s_max)` with `α = θ / (2(1-θ))` (dpp.rs:92-115). `θ = DppTheta = 0.65` (params.rs:205; CLI default 0.5, args.rs:21-22). At θ = 0.65, α = 0.929, so q ranges over [1, 2.53].
- **Kernel**: `L_ii = q_i²` and `L_ij = q_i · q_j · cos(e_i, e_j)` (dpp.rs:119-133). This is the quality × similarity form.
- **Greedy MAP inference** with incremental Cholesky (the fast greedy DPP MAP algorithm of Chen et al. 2018) (dpp.rs:223-314):
  - the first pick is argmax `L_ii`, i.e. the top-scored post;
  - each next pick is the i that maximises the conditional variance `cv_i = L_ii - Σ_j c_ji²`, which is the gain in log det;
  - it stops at `top_k` or when best `cv ≤ 1e-6` ("rank_exhausted").
- **top_k**: only set by the CLI flag `--dpp-top-k`, default 50 (args.rs:18-19). There is no feature-switch param for it.
- **Output**: DPP is a **filter, not a re-order**.
  - The selected posts are re-sorted by their *original* score (dpp.rs:154-171).
  - In dpp_model.rs:196-206 every candidate that was not selected, including everything below rank 150, gets **score 0.0**: `if selected_ids.contains(&c.tweet_id) { s.unwrap_or(0.0) } else { 0.0 }`.
  - A unit test is literally named `filter_only_preserves_original_scores` (dpp.rs:433-464).
- **Seed pinning**: an optional `seed_tweet_id` is pinned as the first element and suppresses near-duplicates of the seed, but it is never returned (dpp.rs:135-142; dpp_model.rs:102-125).
- **Enabling**: `DppEnabled = true` (params.rs:199-204), but the DPP context only exists if the service was started with `--dpp-enabled` (args.rs:15-16; main.rs:29-47). The CLI default is `false`, and the prod launch flags are not in the repo [U].

### 2.2 Plain language

Think of the top 150 posts as people applying for 50 seats.
- The first seat goes to the best-scoring post.
- For each next seat, every remaining post is judged on "how good am I" × "how different am I from the people already seated". Near-duplicates of seated posts, such as another post on the same news story, lose most of their "difference" credit.
- θ sets how much "good" counts compared with "different": θ = 1 means only score matters and θ = 0 means only novelty matters. **θ = 0.65 leans toward score, but not overwhelmingly.**
- The whole score range can only multiply a post's weight by at most e^{2α} = **6.4×**. Being almost a duplicate can shrink it by far more than that. So *similarity* can override quite large score gaps.

Winners keep their original order by score. Losers get score 0 and effectively never reach the 50-item selector or the 35 served posts.

Relevance/diversity balance as θ varies (my arithmetic from dpp.rs:95):

| θ | α | max quality ratio e^{2α} |
|---|---|---|
| 0.3 | 0.21 | 1.5 |
| 0.5 | 0.50 | 2.7 |
| **0.65** | **0.93** | **6.4** |
| 0.8 | 2.0 | 55 |
| 0.9 | 4.5 | 8103 |

### 2.3 Pseudo-code (a faithful Python port I checked against the Rust unit tests `identical_embeddings_select_top_scorer_only` and `orthogonal_embeddings_promote_diversity`)

```python
def dpp_filter(scores, embs, theta=0.65, top_k=50, max_rank=150, eps=1e-6):
    order = argsort(-scores)[:max_rank]                   # pool = top 150
    s, E = scores[order], normalize_rows(embs[order])     # cosine similarity
    alpha = theta / (2 * (1 - min(theta, 1 - eps)))
    q = exp(alpha * s / max(s[0], eps))                  # quality in [1, e^alpha]
    L = outer(q, q) * (E @ E.T); fill_diagonal(L, q**2)
    d = diag(L).copy(); sel = [argmax(d)]; C = [L[sel[0]] / sqrt(d[sel[0]])]
    while len(sel) < top_k:
        cv = d - sum(c**2 for c in C); cv[sel] = -inf    # conditional variance = marginal gain
        i = argmax(cv)
        if cv[i] <= eps: break                            # rank exhausted
        C.append((L[i] - sum(c * c[i] for c in C)) / sqrt(cv[i])); sel.append(i)
    keep = set(order[sel])
    return [scores[j] if j in keep else 0.0 for j in range(len(scores))]
```

**Warning for the simulator** [I, confirmed in my toy run]: the kernel rank is at most the embedding dimension. With 3-d topic vectors the DPP stops after 3 picks. Use embeddings with dimension ≥ 64 (the synthetic world uses 1024).

Toy illustration (my own run, **not** repo data): 150 posts, 5 topics, 64-d embeddings, scores favouring topic 0, top_k = 35.

| Setting | Topic counts | Normalised topic entropy |
|---|---|---|
| No DPP | [27, 5, 0, 1, 2] | — |
| θ = 0.3 | [11, 8, 5, 4, 7] | 0.96 |
| θ = 0.5 | [19, 5, 3, 3, 5] | 0.81 |
| θ = 0.65 | [24, 4, 2, 2, 3] | 0.65 |
| θ ≥ 0.8 | ≈ no-DPP | ≈ 0.5 |

---

## 3. Negative feedback: trace of "not interested" / "show fewer" / mute / block

### 3.1 What the client is offered [V] `home-mixer/util/urt/feedback.rs`

Each post gets a "Don't like" (`DONT_LIKE`, FROWN icon) menu (:203-237) with child actions:
- **"Show fewer from @author"**: `SEE_FEWER`, entity = the original author's UserId (:56-89).
- **"Show fewer retweets from @retweeter"** (:91-125).
- **"Not relevant"**: `NOT_RELEVANT`, entity = TweetId (:127-159).
- **"Not interested in topic X"**: entity = TopicId (:161-201). Its topic label is only attached when `EnableTopicFeedbackContext` is on (topic_feedback_context_hydrator.rs:117-118), and that is **false by default** (param.rs:836-841).

Every action carries `ttl_ms = FEEDBACK_TTL_MS = 30 days` (:12) and is POSTed to `/2/timeline/feedback.json` (:256-264).

### 3.2 What home-mixer does with it

**[V] Nothing in this repository reads a "see fewer / don't like / not relevant" store as a filter.** I searched all of home-mixer, visibility-filtering and filters. The only references are the URT marshalling code, score logging, and the weights. The handler for `/2/timeline/feedback.json` is not in the repo [U].

So, within this repo, "not interested" / "show fewer" is **not a hard filter** on the post, author or topic. It acts through the model, in three ways:
1. **As a prediction target.** Phoenix predicts `P(not_interested)`, which is multiplied by **-47.52** (-43.2 before 2026-09-29; mute by -58.8, block by -31.2) in the value model (section 1).
2. **As a possible input.** The ranker's history input is the full multi-hot action vector per history item (`phoenix/xrex/models/recsys_feature_prep.py:832-834`, `hist_action_emb` over the 64-action vocabulary). The action vocabulary includes `CLIENT_TWEET_NOT_INTERESTED_IN = 17`, `CLIENT_TWEET_SEE_FEWER = 19`, `CLIENT_TWEET_BLOCK_AUTHOR = 23` and `CLIENT_TWEET_MUTE_AUTHOR = 25` (phoenix/python/common/xai-proto/proto/recsys.proto:374-382); the label map is in phoenix/xrex/data/recsys/constants.py:50-61.
   - **But**: whether such events are *in the served sequence* depends on the UAS aggregation type. Production uses `DENSE_WITH_LONG_DWELL` (param.rs:151-162). The proto also defines separate `DENSE_WITH_NOT_INTERESTED_IN = 7` and `DENSE_WITH_NOT_INTERESTED_IN_64 = 21` (phoenix/python/common/xai-proto/proto/recsys.proto:1734, :1748; also `NON_DENSE_WITH_NOT_INTERESTED_IN = 17` at :1744).
   - [I] This hints that the default "dense" aggregation might *exclude* not-interested events. It cannot be verified: the aggregation service is not in the repo [U].
3. **As a training signal for retrieval.** The two-tower retrieval model treats REPORT, NOT_INTERESTED_IN, SEE_FEWER, UNFOLLOW, BLOCK, MUTE and NOT_RELEVANT as **hard negatives** (`phoenix/xrex/models/recsys_two_tower_model.py:1702-1712`). Its only positive is favorite (:1696-1700).

Also:
- The exact post that was marked is already gone because of `PreviouslySeenPostsFilter` (filters/previously_seen_posts_filter.rs:16-31).
- The index side counts `not_interested_in_count` per post (phoenix-rankall/src/processor/record.rs:60, phoenix-rankall-strato/lib/eventProcessing.strato:272-284). [I] That is a post-level aggregate, possibly used as a feature.

### 3.3 Hard negative controls (these are hard filters) [V]

| Control | Mechanism | Duration |
|---|---|---|
| Mute author / block author | `AuthorSocialgraphFilter` removes posts whose author is muted/blocked, or whose quoted/retweeted author is blocked, or where the author blocks the viewer (filters/author_socialgraph_filter.rs:15-55). Visibility filtering also reads blocks/mutes (README.md:74, :214). | Until the user undoes it; no TTL in code |
| Muted keywords | `ViewerMutedKeywordFilter` tokenises post text and removes matches (filters/viewer_muted_keyword_filter.rs:26-55) | As long as the keyword stays in `user_features.muted_keywords`; any expiry is client/server-side and not in the repo [U] |
| Excluded topics (request-supplied `excluded_topic_ids`) | `TopicIdsFilter` removes posts in the excluded topics **and also removes posts with no topic label at all** (`_ => false`, filters/topic_ids_filter.rs:82-102) | Per request |

**Time decay** [V/I]:
- The only explicit TTL is the 30-day `ttl_ms` in feedback metadata (feedback.rs:12). Its enforcement is outside the repo.
- Model-mediated negative feedback lasts as long as the event stays inside the last ≤1024 actions of the user action sequence (param.rs:771-782). [I] That is a count-based FIFO window rather than a time decay. Active users push it out faster.
- The trained model also generalises, so the effect is "soft" and not guaranteed. The only "decay" is that the model sees each history item's age and position (post-age feature, right-anchored RoPE, see section 4).

---

## 4. Phoenix model inputs (how fast can a feed narrow or recover?)

**Sequence** [V]:
- `MaxSeqLengthScoring = 1024` and `MaxSeqLengthRetrieval = 1024` (param.rs:771-782).
- The model's `history_seq_len = 1022` plus 64 candidates (phoenix/xrex/configs/xrecsys.py `_home_direct_packed_base`; phoenix/README.md:405-406).
- Fetched from the User Action Aggregation Service with `window_time_ms = UAS_WINDOW_TIME_MS = 300_000` (5 min; params/config.rs:34; scoring_sequence_query_hydrator.rs:47-59).
  - [U] The meaning of the 5-min window is not in the repo. [I] It is probably an aggregation/dedup window, not "last 5 minutes of history", because the sequence length is up to 1024.
  - The aggregation type is `DENSE_WITH_LONG_DWELL` and the source is `NEW_UUA_ARROW` (param.rs:151-162, :764-770).

**Per history item** [V] (phoenix/README.md:182-191; recsys_feature_prep.py):
- hashed post id + author id;
- 64-way multi-hot **action** vector (what the user did);
- semantic IDs (6 levels × 256 codes, a topic-like code of the post);
- context: surface, post age, hour of day, timezone;
- dwell time;
- flags for whether the viewer follows the author and the author follows the viewer (feature_prep: `enable_is_author_followed_by_viewer`, `enable_is_author_following_viewer`);
- engagement counts.

A user-prefix token carries country, language, location, gender, age bracket and installed apps.

**Candidates** attend only to user + history, never to each other: "candidate isolation" (phoenix/README.md:131-235). [I] The model itself has **no notion of slate diversity**. Every candidate is scored as if it were alone, so ten near-identical posts on your favourite topic can all score high. Diversity only enters afterwards, through the author decay and the DPP.

**Outputs** are the P(action) heads listed in section 1 (64-action taxonomy plus 8 continuous dwell slots; phoenix/README.md:414-415).

**Retrieval** [V]:
- A two-tower model. The user tower is a transformer over the same history and has **no learned per-user ID embedding** (`use_user_embedding=False`, phoenix/README.md:101-108): "the user is represented by what they interacted with".
- Candidates are represented by semantic IDs + author.
- Training uses **favorites as positives** and negative-feedback actions as hard negatives (recsys_two_tower_model.py:1696-1718).

[I] Implications for speed:
- The feed state *is* the last ~1024 interactions. Narrowing speed depends on how many of those are same-topic engagements.
- Recovery requires new, different engagements to displace old ones, or the model to weight recent items more heavily (RoPE is right-anchored: `"right_anchored_rope": True`, phoenix/xrex/configs/xrecsys.py:267).
- A heavy user with 300 actions a day refreshes the whole window in about 3 days. A light user may carry months of history.
- For the retrieval tower, only likes count as "positive". A user who only reads but never likes gives it little signal apart from the dwell and action features in the history.

---

## 5. Candidate sources, exploration and diversity experiments

| Source | Limit / rule | File:line | Effect |
|---|---|---|---|
| Thunder (in-network) | newest posts of followees, at most 1200 (`ThunderMaxResults`); ≤50 originals and ≤30 replies per author; **sorted purely by recency** (`score_recent` sorts by `created_at`) | param.rs:23-28; thunder/config.rs:1-12; thunder/thunder_service.rs:297, :322-326 | neutral: mirrors the follow graph |
| Phoenix retrieval (OON) | at most 1000; nearest neighbours of the user-history embedding. New (09-30): optional exclusion of already seen/served posts (`PhoenixRetrievalExcludeSeenPosts`, default **false**; param.rs:244-249; sources/phoenix_source.rs:65-93) | param.rs:4-9; sources/phoenix_source.rs:97-144 | narrows: "more like your history" |
| SimClusters (OON) | seeds = up to 15 most recent posts per engagement type (fav, RT, reply, bookmark, share, own post, photo expand, VQV, immersive VQV) (param.rs:592-597; models/engagement_signals.rs:42-51); ANN cosine > 0.5 (`POST_ANN_MIN_SCORE`), ≤200 per seed, round-robin interleave, cap 800 | sources/simclusters_source.rs:24-34, :96-147, :150-184, :209-231 | narrows strongly and fast: seeds are only your last few engagements |
| Phoenix cold-start retrieval | `PhoenixColdStartMaxResults = 200` (was 0 until 2026-09-30); passed to the same retrieval call as the main Phoenix source | param.rs:16-21; sources/phoenix_source.rs:117-136 | **new extra candidates since 09-30**; what the cold-start path returns is not in the repo [U] |
| MoE / TweetMixer | `EnablePhoenixMOESource = false`, `PhoenixMOEMaxResults = 0`, `EnableTweetMixerSource = false` | param.rs:47-52, :164-169, :188-193 | off |

- **Proportions** [V/I]: there is no fixed in-network/OON quota anywhere in selectors or blenders. My grep for `in_network` in selectors/ads/blending found none. The mix emerges from scores. The fixed 0.75 OON multiplier plus the mutual-follow reply boost tilt it toward in-network.
- **Randomness / exploration** [V]:
  - the cold-start slot (random rank in [15,16), i.e. deterministic 15);
  - **Thompson sampling among cold-start candidates (ON since 2026-09-30**; section 1.4);
  - a cold-start retrieval source of up to 200 candidates (`PhoenixColdStartMaxResults`, ON since 2026-09-30);
  - weight perturbation (σ = 0, off);
  - random unit embeddings for embedding-less posts in DPP. [I] This is accidental exploration, because random 1024-d vectors are nearly orthogonal to everything and so are favoured by DPP.
  - Otherwise the pipeline is **deterministic given the user history**. There is no ε-greedy.
- **NewUserMinEngagementFilter** [V] (filters/new_user_min_engagement_filter.rs:31-72): for accounts younger than 30 min or resurrected less than 30 min ago, it drops OON posts whose fav/engagement/view metric is below a threshold. **Disabled** (`EnableNewUserMinEngagementFilter = false`, threshold 0.0; param.rs:659-694). [I] If enabled it would push new users toward already-popular content, which is a popularity bias.
- **TopicIdsFilter** [V] (filters/topic_ids_filter.rs:14-106): active only for topic requests or when `excluded_topic_ids` is non-empty (query.rs:238-248).
  - Topic requests keep only posts tagged with the requested (expanded) topics.
  - Exclusions drop tagged posts **and untagged posts**.
  - [I] A user-chosen hard narrowing (topic tab) or a user-chosen hard exclusion.
- **InventoryHoldoutFilter** [V] (filters/inventory_holdout_filter.rs:31-79): drops a deterministic hash(post, viewer) percentage of originals/replies/retweets. **Disabled**, 0% (param.rs:797-820). [I] A measurement holdout, not diversity. **FavHoldoutFilter** (filters/fav_holdout_filter.rs:10-47) is similar: 2-15% by fav count, disabled (param.rs:822-827).
- **ResponseDiversityStats experiment** [V] (side_effects/response_diversity_stats_side_effect.rs):
  - **Measurement only**; it changes nothing.
  - Logged for 5% of requests (`DEFAULT_SAMPLING_RATE = 0.05`, :14) or for all requests in `EnableResponseDiversityStatsExperimentBucket` experiment buckets (param.rs:121-126, default false).
  - It records, for the final list, the top 10, and the "pre-heuristic" top-K by `weighted_score`, i.e. **before** author decay, OON and DPP (:85-95):
    - author `UniqueAuthors`, `UniqueAuthorRatio`, `MaxAuthorShare`, `AuthorHhi`, `AuthorEntropyNorm`;
    - source entropy;
    - `InNetworkShare`;
    - semantic-ID level-1/level-2 unique counts, max share and entropy (:112-185).
  - Definitions (`Composition`, now imported from the external `xai_candidate_pipeline::component_library::utils`, so **no longer visible in the repo since 2026-09-30**; last visible in `home-mixer/util/composition.rs:22-46` at commit `4c5cfe8`): `hhi = Σp²`, `entropy_norm = (-Σ p ln p) / ln(n_items)`.
  - [I] These are **per-request (single-slate) statistics on 5% of requests**. Nothing in the repo tracks a viewer's diversity over time or shows it to the viewer.
  - [I] **This is exactly the metric set a student simulator should report.** It also shows X measures diversity before versus after the heuristics.
- Other widening-ish features [V]:
  - Who-to-Follow module at position 6 with 30 h fatigue (config.rs:29; param.rs:890-901);
  - `PreviouslySeen`/`PreviouslyServed` filters guarantee novelty of *items* but not of *topics*.

---

## 6. docs/BIDIRECTIONAL_BOOST_CHANGE.md: params over time [V]

It is a worked example of how a single parameter evolves:
- **July 10, 2026**: A/B test assigns small random user groups a mutual-follow reply boost of 5, 10, 15 or 20. Most users have 0. A dwell boost was tested too but not shipped. (doc lines 5-9)
- **July 13, 2026**: "initial broad launch". The diff adds `bidirectional_follow_hydrator.rs`, the params (`BidirectionalFollowReplyWeightBoost` default **20.0**, dwell boost 0.0) and `reply_weight_for` / `dwell_weight_for` in the then-existing `home-mixer/scorers/ranking_scorer.rs`. Only *original* posts from *mutual* follows are eligible. The unit tests show replies and retweets are excluded. (doc lines 14-476)
- **July 24, 2026**: the value is lowered from 20 to **15**. The stated reason is user feedback that during the World Cup people saw too little discussion from accounts they don't follow. (doc lines 478-495)

[I] Takeaways for the project:
1. The weights are **policy knobs tuned by A/B tests** and they change within weeks.
2. The company itself recognised a narrowing side-effect: a friends-only boost crowded out out-of-network event content, and it partially reversed the change.
3. The diff references `ranking_scorer.rs` and shows a test asserting `oon_score == in_network_score * 0.75`, but the scoring has since been refactored into `xai-value-model/` + `vm-ranker/`. The code evolves, so the team should cite commit dates.

---

## 7. Runnability of Phoenix nano + synthetic data

**Requirements** [V] (phoenix/QUICKSTART.md:10-24; phoenix/README.md:293-354; phoenix/pyproject.toml):
- Linux + **NVIDIA GPU + CUDA 12**, Python ≥ 3.11, `uv`, a Rust toolchain and `protoc` ≥ 3.15.
- apt packages: build-essential, cmake, libibverbs-dev, libnl, libclang, libnuma.
- `uv sync --extra engine` builds the Rust serving engine. QUICKSTART says it is "required for training and serving".
- JAX pinned to `jax[cuda12]==0.8.1` (pyproject.toml:12).
- The validated environment is a GB300. The code detects A100/H100/H200/GB200/GB300 and **raises "Unknown GPU architecture" for anything else** unless `MACHINE_TYPE` is set (phoenix/xrex/utils/gpu.py:28-40, :103-113).
- Seqpack training requires `pallas_ranker_varlen_attn` or `cutedsl` kernels, which have Hopper/Blackwell tunings (xrex/models/recsys_model.py:3192-3201; xrex/pallas/ranker_attention_varlen.py:69-72).

**Colab** [I]:
- Free Colab (T4, sm75, no native bf16) is **very unlikely** to work: unknown architecture, Pallas GPU kernels, and a heavy Rust + ibverbs build.
- Colab Pro with an **A100** is *plausibly* workable. It is detected as A100, apt and root are available, and a nano run is "minutes on one GPU". Expect friction building the engine and kernels, and budget a day of debugging.
- CPU-only training of the ranker is not a supported path.
- **Recommendation: do not make the project depend on running Phoenix.**

**Synthetic data generator** [V] (phoenix/reference/world.py):
- Pure NumPy and CPU-friendly. Runs in any Colab.
- The world has 16 topics (:12-29), users with 2-4 preferred topics and Gamma(1.5)-weighted preferences (:485-505), authors with primary/secondary topic + quality, and posts with topic, quality and Zipf popularity (:535-570).
- **Engagement model**:
  - `affinity = pref[user, post_topic] · author_quality · post_quality` (:302-305);
  - `gate = sigmoid(14·(affinity - 0.10))` (:308-309);
  - `P(action) = base_rate · gate`, with base rates fav 0.14, click 0.10, video 0.08, repost 0.045, reply 0.035, bookmark 0.02, quote 0.015, share 0.012 (:54-63, :311-312);
  - dwell is log-normal (:335-339).
- **Candidates are 70% from the user's topics and 30% from random topics** (:383-396).
- Post MM embeddings: `topic_anchor + 0.35·author_style + 0.15·jitter`, normalised, so same-topic cosine is clearly higher (:417-429, check :650-655).
- `dump_gen.py` builds histories of 26-1022 items (LENGTH_BUCKETS, :29-41) and candidates of 8-64.

**Can it make toy users with controlled interests?** [I] Yes, easily. `generate_world(...)` (world.py:456-583) is a plain function returning arrays. You can overwrite `user_pref_matrix`, `user_topic_ids` and `user_topic_w` for chosen users, for example a one-topic "cocoon" user and a uniform "omnivore". Then reuse `sample_candidate_posts`, `sample_engagement` and `mm_vector` as the "true user" and "content" model.

Limitations:
- Preferences are **static**; there is no drift.
- There are **no negative actions** such as not-interested, mute or block. Only `not_dwelled` exists.
- Users have **no follow graph**.

You would add these yourselves. The world is also what `dump_gen.py` writes as training data, so if you ever do get a GPU, a nano Phoenix can be trained on your custom world.

---

## (b) Mechanism table

| # | Mechanism | file:line | Effect on diversity | Key parameter values | Confidence |
|---|---|---|---|---|---|
| 1 | Engagement-weighted value model (predicted P(action) × weights) | xai-value-model/scoring.rs:65-119; param.rs:302-414 | **narrows**: ranks by what you already engage with | fav 0.5, reply 5, RT 1, share 2, DM 5, copy-link 20, quote 5, follow 4, dwell 0.05, cont-dwell 0.004 | high |
| 2 | Negative-action heads | same; param.rs:390-414 | **widens** (lets the user push content away), but only via the model | not-interested **-47.52** (was -43.2 until 09-29), block -31.2, mute -58.8, report -234, not-dwelled -0.02 | high (weights); medium (efficacy) |
| 3 | Offset/squash of negative scores | scoring.rs:121-130; weights.rs:4 | neutral: all negatives go below all positives | offset 0.001; PosSum 43.24, NegSum 371.54 (was 43.34 / 367.22) | high |
| 4 | Candidate isolation in Phoenix (no slate awareness) | phoenix/README.md:131-235 | **narrows**: no built-in redundancy penalty | — | high |
| 5 | User action sequence as the only "user profile" | param.rs:771-782; phoenix/README.md:101-108 | **narrows** (feedback loop), but recovers via FIFO | 1024 actions; no user-ID embedding in retrieval | high (length); medium (dynamics) |
| 6 | Phoenix two-tower retrieval (fav-positive) | sources/phoenix_source.rs; recsys_two_tower_model.py:1696-1718 | **narrows**: nearest neighbours of history | ≤1000 candidates; positives = fav only | high |
| 7 | SimClusters seeded by recent engagements | sources/simclusters_source.rs:24-34, :150-184 | **narrows** fast, recency-driven | 15 seeds per type, cos > 0.5, ≤800 | high |
| 8 | Thunder recency (in-network) | thunder/thunder_service.rs:322-326; thunder/config.rs | neutral (mirrors follow graph) | ≤1200; ≤50 originals/author | high |
| 9 | OON discount | vm-ranker/params.rs:175-180; scoring.rs:166-175 | **narrows** toward the follow graph | ×0.75 (topic requests ×0.5; new-user ×0.00001 disabled) | high (value); medium (prod value, see f) |
| 10 | Mutual-follow reply boost | param.rs:304-309; weights.rs:78-85; inputs.rs:18-20 | **narrows** toward close friends / social cocoon | +15 on reply weight (5 → 20); originals only | high |
| 11 | Author diversity decay | scoring.rs:143-164, :177-211; vm-ranker/params.rs:139-156 | **widens** (author level only, not topic) | 0.75·0.5^k + 0.25; enabled in vm-ranker; **disabled** in home-mixer local fallback (value_model.rs:40-44) | high |
| 12 | DPP re-ranker (quality × cosine similarity) | vm-ranker/dpp.rs:35-314; dpp_model.rs:54-206; params.rs:199-211 | **widens** (content/topic level) | θ = 0.65 (α = 0.93), pool 150, top_k 50 (CLI), 1024-d MM embeddings; non-selected → 0 | high (algorithm); medium (deployment flags) |
| 13 | Random embedding for embedding-less posts | dpp_model.rs:23-37, :47 | **widens** (accidental) | random unit vector | high (code); low (magnitude) |
| 14 | Cold-start lift (fresh, little-seen posts) | home-mixer/scorers/author_cold_start.rs:176-326; param.rs:459-538 | **widens** (exposure for fresh, little-seen posts, ≤1 post/request) | since 09-30: followers ≤50,000, views <200, age ≤2 h, Thompson sampling ON (top-2), lift to rank 15 [before: ≤1,000 / <1,000 / ≤48 h / TS off] | high |
| 15 | PostUnexplored head | scoring.rs:81-85; recsys_batch.py:57-85 | widens slightly (within network) | weight 0.02; target 3% of followers in 24 h | high |
| 16 | Weight perturbation per user | weights.rs:96-104; vm-ranker/params.rs:127-138 | would widen (exploration) | σ = 0 → **off** | high |
| 17 | Previously seen/served filters | filters/previously_seen_posts_filter.rs; param.rs:905-916 | widens (item novelty only) | bloom filters; served exclusion 10 min / 100 ids | high |
| 18 | Mute/block author (hard) | filters/author_socialgraph_filter.rs:15-55 | narrows by the user's choice (removes an author permanently) | no TTL | high |
| 19 | Muted keywords (hard) | filters/viewer_muted_keyword_filter.rs:26-55 | narrows by the user's choice | — | high |
| 20 | Topic / excluded-topic filter | filters/topic_ids_filter.rs:14-106 | **narrows** hard (topic tab); exclusion also drops untagged posts | only when topic_ids / excluded_topic_ids given | high |
| 21 | "Show fewer / not interested / not relevant" menu | util/urt/feedback.rs:12-237 | widens (via model/labels); **no hard filter in repo** | TTL 30 days (metadata); topic option off | medium |
| 22 | NewUserMinEngagementFilter | filters/new_user_min_engagement_filter.rs; param.rs:659-694 | would narrow toward popular content | **off**; window 30 min | high |
| 23 | Inventory / Fav holdouts | filters/inventory_holdout_filter.rs; fav_holdout_filter.rs | neutral (measurement) | **off** (0%) | high |
| 24 | Response diversity stats | side_effects/response_diversity_stats_side_effect.rs (formulas moved out of repo 09-30) | neutral (measurement) | 5% sampling; HHI, entropy_norm, SID L1/L2 | high |
| 25 | Who-to-Follow slot | params/config.rs:29; param.rs:890-901 | could widen the follow graph (or narrow if WTF is similarity-based) | position 6; fatigue 30 h | low (WTF logic not examined) |
| 26 | Final truncation | params/config.rs:17-18 | neutral | top 50 selected → 35 served | high |

---

## (c) Plain-language explanation (for first-year students)

1. **Collect.** Every time you open For You, X gathers a few thousand candidate posts:
   - the newest posts from accounts you follow (Thunder);
   - posts a neural network thinks match "what you've been doing lately" (Phoenix retrieval);
   - posts similar to the handful of posts you most recently liked or reposted (SimClusters).

   The last two sources learn only from **your own recent history**, so they already favour what you liked before.
2. **Predict.** A big transformer (Phoenix) reads your last ~1000 actions and predicts, for each candidate, the chance you would like it, reply, share, block it, say "not interested", and so on. It judges each post alone, so it never notices "these ten posts are all about the same thing".
3. **Score.** These chances are combined into one number with fixed weights: sharing via copy-link is worth 20, replying 5, liking 0.5; "not interested" is about -48 (raised from -43 on 29 Sep 2026), muting -59, reporting -234. Then:
   - posts from people you *don't* follow are multiplied by 0.75;
   - original posts from people who follow you back get a big bonus on the reply term (reply weight 5 → 20).

   Both nudge you toward your existing social circle.
4. **Two brakes on sameness:**
   - **Author brake.** The 2nd post from the same author is worth 62.5%, the 3rd 44%, and so on, never below 25%.
   - **Content brake (DPP).** Among the top 150 posts, the system picks about 50 that are both high-scoring *and* different from each other, measured with content embeddings. θ = 0.65 means "mostly score, but diversity matters". Posts that look like something already picked are dropped.
5. **Newcomer lift.** Once per refresh, one very fresh (≤2 h), little-seen post may be lifted to about position 16. Since 30 Sep 2026 the candidate is partly chosen at random (Thompson sampling), which is the first random exploration switched on by default.
6. **Feedback.**
   - Muting or blocking an account, or muting a word, removes that content for good.
   - "Show fewer" or "not interested" is **not** a delete button in this code. It becomes data that teaches the model to predict you won't like similar posts, and a -47.52 weight (-43.2 before 29 Sep 2026) then pushes such posts down.
7. **The loop.** What you engage with becomes your next ~1000-action history, and that history decides what you see next. That is the loop that can create a cocoon, and the brakes are what fight it.

---

## (d) Research questions this code enables

1. **Narrowing speed.** With these weights and a 1024-action FIFO history, how many sessions until a simulated user's served-feed topic entropy falls below 0.5? How does that depend on true-preference concentration (1-topic vs 4-topic users)?
2. **θ sweep.** How much does DPP θ (0.3 / 0.5 / 0.65 / 0.8 / 1.0 = off) change topic entropy, unique topics, and SID-L1 entropy of the 35 served posts, and how much predicted engagement does it cost? Trace the engagement-diversity Pareto frontier.
3. **DPP vs author decay.** Which brake matters more for *topic* diversity? Author decay only sees author IDs. Try a world where one topic has many authors against one where it has few.
4. **OON factor.** How does in-network share, and topic entropy, change as OonWeightFactor goes 1.0 → 0.75 → 0.5? Is a follow graph that is topically narrow a stronger cocoon than the algorithm?
5. **Mutual-follow boost (0 / 5 / 15 / 20).** Does raising it create a "friends cocoon" (high in-network share) and crowd out event or OON content, reproducing the July 2026 World Cup complaint in simulation?
6. **Negative feedback power.** If a user clicks "not interested" on every post from topic X, how many requests until topic-X share falls below 5%, when:
   - (a) it is a hard filter;
   - (b) it is a model input with weight -47.52 (-43.2 before 09-29) and a FIFO history of 1024;
   - (c) it is excluded from the sequence (the DENSE aggregation uncertainty)?
7. **Recovery (un-cocooning).** After a user's true interests shift (drift), how many interactions until the feed reflects the new mix? How does this scale with history length L (128 / 512 / 1024) and user activity?
8. **SimClusters seed recency.** With seeds = the last 15 engagements per type, does one binge session (e.g. 30 likes on one topic) dominate OON retrieval for the next day?
9. **Cold-start lift.** Does lifting one fresh, little-seen post per request measurably raise author diversity or topic diversity? How much did switching Thompson sampling on (2026-09-30) change this?
10. **Popularity bias.** If NewUserMinEngagementFilter were enabled, how concentrated (Gini/HHI over authors) would new users' feeds become?
11. **Pre- vs post-heuristic diversity.** Replicate X's own `ResponseDiversity` metrics (AuthorHhi, AuthorEntropyNorm, SidL1EntropyNorm, InNetworkShare) at the pre-heuristic and final stages. How much diversity do the heuristics add?
12. **Weight perturbation as exploration.** Does per-user σ > 0 (weights × e^{±σ}) slow narrowing, and what is the engagement cost?

---

## (e) Minimal faithful Python re-implementation spec

**World** (reuse or adapt `phoenix/reference/world.py`):
- `T` topics (16) with unit anchors `a_t` in R^D, D ≥ 64 (so DPP is not rank-limited).
- Authors: primary/secondary topic, quality `q_a ~ Beta(2,2)`, style vector, followers count.
- Posts: author, topic (80% primary, 20% secondary), quality `~Beta(2,2)`, created time, views, favs, embedding `e_p = norm(a_t + 0.35·style_a + 0.15·noise)` (world.py:426).

**User state** (per user u):
- `p_u` — true topic preferences (simplex). Static, or drifting: `p_u ← (1-η)p_u + η·shock`.
- `F_u` — followed authors; `M_u ⊆ F_u` — mutual follows.
- `H_u` — `deque(maxlen=L)`, L = 1024 (or scaled down), of events `(post, topic, author, actions:set, t)`.
- `muted_authors`, `blocked_authors`, `muted_topics` (hard lists); `seen` (set).

**Model stand-in for Phoenix** (the simulator's weakest link; keep it simple and state it):
- Interest estimate:
  `ĥ_u[t] = (ε + Σ_{e∈H_u, e.topic=t} (Σ_{a∈e.actions} c_a)) / normaliser`,
  with c_fav = 1, c_reply = 2, c_share = 2, c_dwell = 0.5, c_not_interested = −3, c_not_dwelled = −0.2.
  Optionally apply a recency weight `γ^{age_rank}`, γ ≈ 0.998.
- Predicted affinity: `x̂ = ĥ_u[topic_p] · q_author · q_post` (mirrors world.py:302-305).
- Predicted probabilities: `P̂_a = base_a · σ(14(x̂ − 0.1))` for positive actions, with base rates from world.py:54-63.
- Negatives: `P̂_notint = b_ni · (1 − σ(...)) · (1 + κ·n_notint_on_topic_or_author_in_H)`, with b_ni ≈ 0.002, b_block ≈ 0.0005, b_mute ≈ 0.0005, b_report ≈ 0.0001. These are assumptions, since negative feedback is rare (param.rs:285-287).

**Candidate generation per request:**
- In-network: newest ≤ N_in posts from `F_u` (≤ 50 per author), age ≤ 48 h, recency-sorted.
- Two-tower: top N_ret posts by `ĥ_u · onehot(topic)` (or `u_emb · e_p`, with `u_emb = mean of e_p over fav'd posts in H`).
- SimClusters: for the most recent 15 engaged posts (per type), take posts with `cos(e_seed, e_p) > 0.5`; round-robin; cap N_sc.
- Scaled sizes, e.g. N_in = 120, N_ret = 100, N_sc = 80 (prod: 1200/1000/800).

**Filters:** age > 48 h; seen; author in muted/blocked; topic in muted_topics (keyword stand-in); OON replies (if you model replies).

**Scoring** (verbatim from the code):
```
S_raw = Σ w_a P̂_a    # weights from param.rs table; reply weight 20 if mutual & original;
                     # post_unexplored only if in-network
S     = S_raw + 0.001 if S_raw >= 0 else (S_raw + 371.54)/414.78 * 0.001
cold start: among eligible (followers<=50000, views<200, original, age<=2h,
            position<0.97N) draw r ~ Beta(0.75+favs, 49.25+views-favs),
            keep the 2 highest r, pick the higher-scoring one; S = max(S, sorted(S)[15])
k     = # same-author candidates with higher S (whole pool)
S    *= 0.75*0.5**k + 0.25
S    *= 0.75 if out_of_network (or in-network reply/RT) else 1
```

**DPP:** `dpp_filter(S, E, theta=0.65, top_k=50, max_rank=150)` (section 2.3). Then take the top 50 by S, then the first 35 as the feed.

**User response** (true model, not the recommender's estimate):
- For each shown post, `x = p_u[topic]·q_a·q_p`.
- Sample positive actions with `P = base·σ(14(x − 0.1))`; dwell log-normal (world.py:311-339).
- With probability `β·(1 − σ(14(x − 0.1)))` choose "not interested", β ≈ 0.02 (tunable); mute/block with much smaller probability.
- Record `not_dwelled` if no action. Follow the author with probability `base_follow·σ(...)`; this updates `F_u`.
- Append all events to `H_u` (FIFO) and add the posts to `seen`.

**Variants to toggle** (the experiments of section d):

| Variant | Settings |
|---|---|
| θ | 0.3–1.0 (1.0 = no DPP) |
| Author decay | on/off, decay/floor |
| OON factor | 0.5–1.0 |
| Bidirectional boost | 0–20 |
| Negative-feedback mode | {hard filter for 30 days, model-only with the above c_notint, excluded from history} |
| History length | L |
| Cold start | on/off; Thompson sampling |
| Weight perturbation | σ |

**Metrics per request** (copy X's `Composition` definitions; last visible in `home-mixer/util/composition.rs:22-46` at commit `4c5cfe8`):
- over topics, authors and sources of the 35 served posts: `entropy_norm = −Σp ln p / ln(n_items)`, `HHI = Σp²`, `unique`, `max_share`;
- `InNetworkShare`;
- divergence between the served topic distribution and the true `p_u` (KL or total variation);
- "cocoon index" = served-topic entropy ÷ entropy of `p_u`;
- engagement per request (a sum of sampled actions weighted by the same weights), to show the trade-off.

Report both **pre-heuristic** (top-35 by weighted score) and **final** metrics, as X does.

---

## (f) Open uncertainties

1. **Production values in vm-ranker.** vm-ranker/params.rs holds author-diversity, OON and DPP defaults without the "mirrored from config ... last sync" header that param.rs has. Real production values come from config-sync (vm-ranker/main.rs:61-84; the log line says the feature-switch engine re-reads the synced files every 30 s) and may differ. Specifically:
   - `--dpp-enabled` (CLI default false) and `--dpp-top-k` (CLI default 50, no param) are deployment flags not in the repo.
   - Whether DPP runs in production is implied by README.md:282 and `DppEnabled = true`, but not provable.
2. **Is "not interested" in the model's input sequence?** The aggregation type is `DENSE_WITH_LONG_DWELL`. The existence of separate `DENSE_WITH_NOT_INTERESTED_IN` types suggests it may not be. The User Action Aggregation Service is not in the repo.
3. **Server-side handling of `/2/timeline/feedback.json`** (30-day TTL): whether "show fewer from @X" becomes a hard filter or down-rank elsewhere (e.g. in candidate stores or UAS) is not visible.
4. **Meaning of `window_time_ms = 300_000`** in the UAS request (5 min): an aggregation window, not a history horizon (inferred).
5. **Phoenix predictions are learned.** We cannot know from code how strongly past "not interested" or topic history changes P̂. Any simulator's P̂ model is an assumption. Without production checkpoints, "how fast" questions can only be answered for the simulated model.
6. **Embeddings used by DPP** come from `xai_recsys_mm_server` (not in the repo). I identified them as the 1024-d "v5" multimodal embeddings from the phoenix reference README. The missing-embedding rate in production is unknown; it is logged by `DPP_EMBEDDING_MISS_RATIO`.
7. **Other stages** (visibility-filtering labels, ads blending, Who-to-Follow, the `quality_factor::apply` load scaling of source sizes) were not examined in depth. Their diversity effects are unassessed.
8. **Experiments** (feature-switch buckets) can override any default for part of the traffic. The README says experiments at ≥10% traffic should be visible, which means smaller ones may not be.
9. **Colab feasibility** is inferred from the requirements, not tested. I did not run Phoenix. The only thing I executed was a small NumPy port of the DPP in my scratchpad, for validation.
10. **Code history.** BIDIRECTIONAL_BOOST_CHANGE.md references `home-mixer/scorers/ranking_scorer.rs`, which no longer exists. Scoring was refactored into `xai-value-model/`. Cite the commit (`b79b947`, 2026-10-01) when writing up; parameters are re-synced almost daily (e.g. the 09-29/09-30 changes in the update table at the top).
