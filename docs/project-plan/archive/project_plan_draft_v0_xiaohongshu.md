# Can You Tap Your Way Out? An Outside-In Audit of Xiaohongshu's Anti-Cocoon Controls

**COMP1110 Group Project — Project Plan (DRAFT v0.1, 2026-09-27)**

**Team members:** [Name 1, UID] · [Name 2, UID] · [Name 3, UID] · [Name 4, UID] · [Name 5, UID]

> Draft status: topic not yet confirmed by the team. Every reference must be opened and checked by a team member before submission (see `docs/research/README.md`). Target length: 4–6 pages.

---

## 1. Problem Statement

**Everyday context.** Most of us open Xiaohongshu (小红书, "RED") several times a day to find food, study tips, rental advice, or fitness routines. Many of us have also noticed that after a few days of looking at one kind of note, the home feed seems to show little else. This narrowing is what Sunstein (2006) called an *information cocoon* (信息茧房) and Pariser (2011) called a *filter bubble*.

**What changed recently.** Since March 2022, China's rules on algorithmic recommendation (Art. 17) require apps to offer a non-personalised option and ways to manage interest tags (CAC, 2022). In November 2024, a national "Qinglang" campaign named "homogeneous pushes that create information cocoons" as the first problem platforms must fix (CAC, 2024). By May 2025, the regulator reported that Xiaohongshu, Douyin, Kuaishou, Weibo, Bilibili and WeChat Channels had launched anti-cocoon tools such as "content preference adjustment" (内容偏好调节), "cocoon assessment" and "one-tap cocoon breaking" (CAC, 2025). But on **17 September 2026**, a commentary on People's Daily Online argued that these tools are hard to find, rarely used, and that feeds drift back to old interests soon after they are used (People's Daily Online, 2026). The only evidence so far comes from the platforms themselves or from users' self-reports. **We found no study that has measured these tools from the outside.**

**Research question.**

> *After a new Xiaohongshu account's home feed has been narrowed to a single lifestyle interest, do the platform's built-in anti-cocoon controls ("not interested", content-preference adjustment / "Explore More", and switching off personalised recommendation) restore feed diversity faster and for longer than doing nothing or simply engaging with other content?*

Put simply: **once you are in a cocoon, do the official "cocoon-breaking" buttons actually get you out, and do you stay out?**

**Sub-questions.**
1. *Falling in:* how many sessions of one-topic engagement does it take for the seed topic to dominate the feed?
2. *Getting out:* which escape strategy lowers the seed topic's share and raises feed diversity fastest?
3. *Staying out:* after the escape action, does the feed "relapse" to the old interest in the following days?
4. *Why:* can a simple recommender–user feedback-loop model reproduce the pattern we observe (e.g., fast to fall in, slow to get out)?

**In scope.** Xiaohongshu home ("Explore") feed on accounts registered in Hong Kong; one non-political lifestyle seed topic (proposed: weight-loss / body-shape content, [to be confirmed]); five escape strategies; a two-to-three-week audit window; a small simulation model.

**Out of scope.** Political or news content; effects on users' beliefs, attitudes or mental health; reverse-engineering Xiaohongshu's actual algorithm; claims about all users or all platforms; building a production app.

---

## 2. Computing and Data Science Connection

**Main project type: Hybrid** — *data analysis* (primary: an algorithm audit and its analysis) plus *simulation / modelling* (secondary: a feedback-loop model that explains the audit results).

| Concept / method | What it does in our project | How it helps answer the question |
|---|---|---|
| **Algorithm auditing with sock-puppet accounts** (Sandvig et al., 2014; Hosseinmardi et al., 2024) | Five fresh accounts follow a fixed, scripted protocol so that the only difference between them is the escape strategy. | Lets us study a black-box recommender from the outside, with a control condition. |
| **Experimental design** | Phases: baseline → induction → escape → follow-up; one control arm; all accounts run in parallel at the same times of day. | Separates the effect of each escape tool from time effects and algorithm updates. |
| **Structured data collection and content coding** | For each session we log the first 30 notes (position, title, category) into a shared spreadsheet using a fixed codebook of about 12–15 lifestyle categories. 10–20% of items are double-coded; agreement is checked with Cohen's κ. We may test an LLM classifier against our human labels to speed up coding, reporting its accuracy. | Turns screens into analysable data and shows the labels are reliable. |
| **Diversity metrics** (Kunaver & Požrl, 2017; Michiels et al., 2022) | Per session: seed-topic share; normalised Shannon entropy of the category distribution, *H* = −Σ *pᵢ* log *pᵢ* / log *K*; number of distinct categories; Jaccard similarity to the account's own baseline feed. We report at least two metrics because conclusions can depend on the metric (Mosnar et al., 2025). We also screenshot Xiaohongshu's own "content preference" pie chart and compare it with our measured distribution. | Gives a precise, comparable definition of "cocoon" and "diversity", and checks the platform's self-reported picture against ours. |
| **Time-series and comparative analysis** (Python: pandas, matplotlib) | Plot each metric over sessions; compute *time-to-cocoon* (sessions until seed share first exceeds 50%), *recovery half-life* (sessions to recover half of the lost entropy), and *relapse* (change in seed share after the escape action stops). The control account gives the "noise floor" of normal day-to-day change. Compare arms with descriptive statistics and simple non-parametric tests where sample sizes allow. | Directly answers sub-questions 1–3. |
| **Simulation of a recommender feedback loop** (Chaney et al., 2018; Jiang et al., 2019) | Agent-based Python model: *K* content categories; the recommender keeps an interest vector for the user, updated after each interaction by exponential smoothing; the feed samples categories in proportion to the vector plus an exploration rate ε. User actions: engage, "not interested" (negative update), preference adjustment (reset one weight), personalisation off (ε = 1). Outputs: the same metrics as the audit. Optionally, user preference distributions are drawn from the public KuaiRec short-video dataset (Gao et al., 2022). | Explains *why* the observed pattern happens; lets us test "what if" settings (e.g., how much exploration would stop rebound) that we cannot test on the real app. |
| **(Optional) Short anonymous survey of HKU students** | Awareness and use of anti-cocoon features; perceived feed diversity. | Adds everyday relevance: is the tool known and used at all? |

**Study design at a glance** (to be finalised after the pilot).

| Phase | Days | What every account does |
|---|---|---|
| 0. Baseline | 1–2 | Scroll the home feed without interacting |
| 1. Stain (induction) | 3–7 | Same scripted engagement with the seed topic only (search, open, like, save) |
| 2. Scrub (escape) | 8–12 | Each account uses **one** strategy: (a) control — stop engaging with the seed topic; (b) tap "not interested" on every seed-topic note; (c) lower the seed category in *content preference adjustment* / use "Explore More" (探索更多); (d) switch personalised recommendation off, then back on; (e) actively engage with other categories |
| 3. Relapse check | 13–16 | All accounts return to neutral scrolling |

Each session logs the first 30 notes; two sessions per day at fixed times → about 4,800 coded notes in total.

**Technical depth expected later.** The Final Report will contain the full audit protocol, the codebook and reliability results, the dataset (~4,800 logged notes), metric definitions with worked examples, figures comparing the five strategies, and the simulation's rules, parameters, calibration against our data, and scenario results.

---

## 3. Literature and Background Review

**Filter bubbles are real in exposure but contested in effect.** The concept comes from Sunstein (2006), who stressed users' own choices, and Pariser (2011), who blamed invisible personalisation. Large studies since then give a mixed picture. Bakshy et al. (2015) found that Facebook's ranking reduced cross-cutting news, but users' own choices reduced it more. The 2020 US-election collaborations with Meta found that removing the ranking algorithm or reducing like-minded content changed what people saw but not their attitudes (Guess et al., 2023; Nyhan et al., 2023). The Reuters Institute's review concludes that echo chambers are less widespread than feared and that evidence is heavily US-based (Ross Arguedas et al., 2022). We therefore do *not* try to prove that cocoons exist or are harmful. We adopt Michiels et al.'s (2022) testable definition — **personalisation causing a decrease in content diversity over time** — and ask a different question: can the decrease be reversed?

**Audits show how fast users fall in; far fewer study how they get out.** Sock-puppet audits (Sandvig et al., 2014; Metaxa et al., 2021) have measured "rabbit holes" on YouTube and TikTok, mostly for politics, misinformation or mental-health harm (Haroon et al., 2023; Hosseinmardi et al., 2024). Personalisation signals differ by platform and change over time: Boeker and Urman (2022) found following mattered most on TikTok, but a 2025 replication found watch time now dominates and that conclusions can flip with the choice of metric (Mosnar et al., 2025) — so we report more than one metric. Only a handful of studies measure *escaping*. On YouTube, watching debunking videos can partly "burst" misinformation bubbles (Tomlein et al., 2021), and a "stain → scrub" audit found that "not interested" removed most of a stained topic from the homepage (Liu et al., 2024), whereas Mozilla Foundation's (2022) study of about 22,000 real users found the same button prevented only about 11% of unwanted recommendations. On TikTok, Kaplan et al. (2026) found that "not interested" is the most effective control but is buried in the interface, and that feeds are often taken over by the unwanted topic again once users stop pressing it. These conflicting results show that escape tools must be measured on each platform, with a control, and *after* the escape action ends. **We adapt this stain → scrub → relapse design to a new setting.**

**Chinese platforms are studied mainly through surveys and interviews.** The only peer-reviewed sock-puppet audits of a Chinese platform we found are on Douyin, about health videos and news diversity (Shi & Li, 2024). A log study of a Chinese short-video platform found new users' consumption becoming more homogeneous over a year (Li et al., 2022). Interview and diary studies of Douyin and Xiaohongshu users report that users steer their feeds by searching, lingering or tapping "not interested", and that passive users are more cocooned (Li et al., 2025; 数字传播与新媒体学刊, 2026) — but this evidence is self-reported. **We found no controlled audit of Xiaohongshu, and no independent test of the official anti-cocoon controls launched in 2025 on any Chinese platform.**

**Regulation made anti-cocoon tools common, but their effect is unmeasured.** China's algorithm rules (CAC, 2022) and the 2024–25 campaign (CAC, 2024, 2025) led to the new features described above. Similar "algorithm opt-out" rules are spreading elsewhere: the EU Digital Services Act (Art. 38) requires a non-profiling feed option, and Australia proposed a "My Feed, My Way" opt-out on 8 September 2026. In Europe, courts and NGOs have argued that opt-outs which reset or are hard to reach are "dark patterns" (DSA Observatory, 2026). The most recent Chinese commentary claims the tools are rarely used and that feeds rebound (People's Daily Online, 2026), but offers no measurement. Our audit provides exactly that measurement for one platform.

**Models explain why narrowing happens, but have not been linked to real escape tools.** Chaney et al. (2018) and Jiang et al. (2019) showed in simulation that recommender feedback loops make consumption more homogeneous. We borrow their structure, but add the concrete user actions that the 2025 tools offer and calibrate the model with our own audit data.

**Existing anti-bubble products do not fit this setting.** Tools such as AllSides, Ground News's "Blindspot" and Balancer (Munson et al., 2013) target left/right political news in English. None measures lifestyle content, works on Chinese-language platforms, or tells users whether a platform's own controls work.

**Research gap.** Our study combines (1) a very recent, unmeasured claim (September 2026) about (2) regulator-mandated anti-cocoon tools, on (3) Xiaohongshu, a platform almost absent from the audit literature, with (4) non-political lifestyle content as the cocoon topic (earlier audits use lifestyle content only as a neutral control), from (5) the perspective of *escaping and relapsing* rather than *falling into* a cocoon. We do not claim the audit method is new; we claim the question, the tools tested and the setting are.

---

## 4. Feasibility, Limitations and Ethics

**Data and access.** We need only what any user sees: the first 30 notes of the home feed per session. Five members each run one fresh account on their own phone (HK mobile numbers). Manual audits of this size are an established practice: NGO audits of TikTok and Instagram used 3–8 hand-run accounts (Center for Countering Digital Hate, 2022; Amnesty International, 2025). We will record phone model, OS and app version, since device can affect recommendations (Shi & Li, 2024), and screen-record sessions so coding can be checked. Logging takes about 20–25 minutes per member per day for about 16 days (5 accounts × 16 days × 2 sessions × 30 notes ≈ 4,800 records). Tools: shared Google Sheet / CSV, Python (pandas, matplotlib, NumPy), optional KuaiRec dataset (public, CC BY-SA 4.0).

**Pilot first.** In week 1 we will check that the Hong Kong version of Xiaohongshu offers the content-preference and personalisation-off controls. If a control is missing, we will replace that arm (e.g., with a second "not interested" intensity) or run the same arm on Bilibili/Douyin as a comparison.

**Methods next.** Finalise the codebook and protocol after a two-day pilot; run the audit; code and check reliability; compute metrics; build and calibrate the simulation.

**Limitations and what we will not claim.**
- One account per strategy is a very small sample, so results are exploratory case evidence, not general laws. If phone numbers allow, we will add a second account for key arms.
- Fresh accounts behave differently from real users with long histories.
- Audit findings are a snapshot: platforms change, and earlier TikTok audits did not replicate a few years later (Mosnar et al., 2025).
- Xiaohongshu may change its algorithm during the study; running all accounts in parallel reduces but does not remove this risk.
- Location, device and time of day can affect recommendations; we will fix what we can and record the rest.
- We will not claim anything about users' beliefs or well-being, or about how Xiaohongshu's algorithm works internally.

**Ethics.**
- *No real users are studied.* Sock-puppet accounts will not post, comment, message or follow ordinary users; they only view, like and save. We record note titles and categories only, never usernames or images of people.
- *Platform terms.* Accounts are created manually, used at human speed, and with no scraping or automation; we will review Xiaohongshu's terms and minimise any burden on the platform.
- *Researcher well-being.* Weight-loss content can be harmful; members may swap topics, and we will stop exposure at any sign of discomfort.
- *Survey (optional).* Anonymous, voluntary, with informed consent and no personal identifiers; we will ask the teaching team whether ethics approval is needed before running it.
- *Data.* Stored in the team's private repository; the published dataset contains categories and anonymised titles only.

---

## 5. Timeline and Team Roles

**Milestones** (dates in 2026; adjust once the course calendar is confirmed).

| Week | Dates | Milestone | Lead |
|---|---|---|---|
| 1 | 28 Sep – 4 Oct | Confirm topic; verify all references; submit **Project Plan (4 Oct)** | [Name 1] |
| 2 | 5 – 9 Oct | Register accounts; two-day pilot; confirm which controls exist in HK; finalise protocol and codebook v1; simulation v0 | [Name 2], [Name 3], [Name 5] |
| 2–4 | 10 – 25 Oct | Run audit (16 days): baseline (2 d) → induction (5 d) → escape (5 d) → follow-up (4 d); daily logging; weekly reliability check | All (one account each); [Name 2] coordinates |
| 4 | 20 – 24 Oct | **Interim progress meeting** with TA: show pilot data and early plots | [Name 1] |
| 5 | 26 Oct – 1 Nov | Finish coding; Cohen's κ; compute all metrics; first figures; calibrate simulation | [Name 3], [Name 4], [Name 5] |
| 6 | 2 – 8 Nov | Simulation scenarios; (optional) survey; results write-up; **Interim progress log (4 Nov, individual)** | [Name 4], [Name 5]; all |
| 7 | 9 – 15 Nov | Integrate and edit **Final Report (15 Nov)**; individual self-reflections | [Name 1] (editor); all |
| 8–9 | 16 – 26 Nov | Slides and rehearsal; **Group presentation (17/19/24/26 Nov)** | [Name 4] (slides); all present |

**Roles** (each member also runs one audit account every day).

| Member | Main responsibility | Deliverable contribution |
|---|---|---|
| [Name 1] | Project lead; literature, regulation and news review; final report editor | Sections on background and related work; overall consistency |
| [Name 2] | Audit protocol and account operations; pilot; daily schedule | Methods section (audit design); protocol appendix |
| [Name 3] | Data collection template, codebook, labelling quality (κ); optional LLM-assisted coding test | Dataset; data and reliability section |
| [Name 4] | Data analysis and visualisation (metrics, statistics, figures); presentation slides | Results section; figures |
| [Name 5] | Simulation model: design, implementation, calibration, scenarios | Modelling section; simulation appendix |

---

## References

> APA 7th. **All entries must be checked against the original source before submission.**

- Amnesty International. (2025). *Dragged into the rabbit hole: New evidence of TikTok's risks to children's mental health*. https://www.amnesty.org/en/latest/news/2025/10/tiktok-steering-children-towards-depressive-and-suicidal-content/
- Bakshy, E., Messing, S., & Adamic, L. A. (2015). Exposure to ideologically diverse news and opinion on Facebook. *Science, 348*(6239), 1130–1132. https://doi.org/10.1126/science.aaa1160
- Boeker, M., & Urman, A. (2022). An empirical investigation of personalization factors on TikTok. In *Proceedings of the ACM Web Conference 2022* (pp. 2298–2309). https://doi.org/10.1145/3485447.3512102
- Center for Countering Digital Hate. (2022). *Deadly by design*. https://counterhate.com/research/deadly-by-design/
- Chaney, A. J. B., Stewart, B. M., & Engelhardt, B. E. (2018). How algorithmic confounding in recommendation systems increases homogeneity and decreases utility. In *Proceedings of RecSys '18* (pp. 224–232). https://doi.org/10.1145/3240323.3240370
- Cyberspace Administration of China [CAC]. (2022, January 4). 互联网信息服务算法推荐管理规定 [Provisions on the administration of algorithmic recommendation in internet information services]. https://www.cac.gov.cn/2022-01/04/c_1642894606364259.htm
- Cyberspace Administration of China [CAC]. (2024, November 24). 关于开展"清朗·网络平台算法典型问题治理"专项行动的通知. https://www.cac.gov.cn/2024-11/24/c_1734143936205514.htm
- Cyberspace Administration of China [CAC]. (2025, May 22). [Progress report on the algorithm governance campaign]. https://www.cac.gov.cn/2025-05/22/c_1749536203490537.htm
- DSA Observatory. (2026, July 30). [Analysis of Bits of Freedom v. Meta, "Ineffective by design"]. [URL to verify]
- Gao, C., Li, S., Lei, W., Chen, J., Li, B., Jiang, P., He, X., Mao, J., & Chua, T.-S. (2022). KuaiRec: A fully-observed dataset and insights for evaluating recommender systems. In *Proceedings of CIKM '22*. https://doi.org/10.1145/3511808.3557220
- Guess, A. M., et al. (2023). How do social media feed algorithms affect attitudes and behavior in an election campaign? *Science, 381*(6656), 398–404. https://doi.org/10.1126/science.abp9364
- Haroon, M., et al. (2023). Auditing YouTube's recommendation system for ideologically congenial, extreme, and problematic recommendations. *PNAS, 120*(50). https://doi.org/10.1073/pnas.2213020120
- Hosseinmardi, H., et al. (2024). Causally estimating the effect of YouTube's recommender system using counterfactual bots. *PNAS, 121*(8). https://doi.org/10.1073/pnas.2313377121
- Jiang, R., Chiappa, S., Lattimore, T., György, A., & Kohli, P. (2019). Degenerate feedback loops in recommender systems. In *Proceedings of AIES '19*. https://doi.org/10.1145/3306618.3314288
- Kaplan, L., Patel, D., Gerzon, N., Mislove, A., & Sapiezynski, P. (2026). When 'For You' isn't for you: Measuring user agency in TikTok's algorithmic feed. *Proceedings of ICWSM, 20*(1), 1175–1189. https://ojs.aaai.org/index.php/ICWSM/article/view/42688
- Kunaver, M., & Požrl, T. (2017). Diversity in recommender systems – A survey. *Knowledge-Based Systems, 123*, 154–162. https://doi.org/10.1016/j.knosys.2017.02.009
- Li, N., Gao, C., Piao, J., Huang, X., Yue, A., Zhou, L., Liao, Q., & Li, Y. (2022). An exploratory study of information cocoon on short-form video platform. In *Proceedings of CIKM '22*. https://doi.org/10.1145/3511808.3557548
- Li, W., Kuo, J.-C., Sheng, M., Zhang, P., & Wu, Q. (2025). Beyond explicit and implicit: How users provide feedback to shape personalized recommendation content. In *Proceedings of CHI '25*. https://doi.org/10.1145/3706598.3713241
- Liu, A., Wu, S., & Resnick, P. (2024). How to train your YouTube recommender to avoid unwanted videos. *Proceedings of ICWSM, 18*(1), 930–942. https://ojs.aaai.org/index.php/ICWSM/article/view/31363
- Metaxa, D., Park, J. S., Robertson, R. E., Karahalios, K., Wilson, C., Hancock, J., & Sandvig, C. (2021). Auditing algorithms: Understanding algorithmic systems from the outside in. *Foundations and Trends in Human–Computer Interaction, 14*(4), 272–344. https://doi.org/10.1561/1100000083
- Michiels, L., Leysen, J., Smets, A., & Goethals, B. (2022). What are filter bubbles really? A review of the conceptual and empirical work. In *UMAP '22 Adjunct* (pp. 274–279). https://doi.org/10.1145/3511047.3538028
- Mosnar, M., Skurla, A., Pecher, B., Tibensky, M., Jakubcik, J., Bindas, A., Sakalik, P., & Srba, I. (2025). Revisiting algorithmic audits of TikTok: Poor reproducibility and short-term validity of findings. In *Proceedings of SIGIR '25*. https://doi.org/10.1145/3726302.3730293
- Mozilla Foundation. (2022). *Does this button work? Investigating YouTube's ineffective user controls*. https://www.mozillafoundation.org/en/research/library/user-controls/
- Munson, S. A., Lee, S. Y., & Resnick, P. (2013). Encouraging reading of diverse political viewpoints with a browser widget. In *Proceedings of ICWSM 2013*.
- Nyhan, B., et al. (2023). Like-minded sources on Facebook are prevalent but not polarizing. *Nature, 620*, 137–144. https://doi.org/10.1038/s41586-023-06297-w
- Pariser, E. (2011). *The filter bubble: What the Internet is hiding from you*. Penguin Press.
- People's Daily Online. (2026, September 17). "破茧"功能，何以真正破除"信息茧房". http://theory.people.com.cn/n1/2026/0917/c40531-40800283.html
- Ross Arguedas, A., Robertson, C. T., Fletcher, R., & Nielsen, R. K. (2022). *Echo chambers, filter bubbles, and polarisation: A literature review*. Reuters Institute for the Study of Journalism. https://reutersinstitute.politics.ox.ac.uk/echo-chambers-filter-bubbles-and-polarisation-literature-review
- Sandvig, C., Hamilton, K., Karahalios, K., & Langbort, C. (2014). Auditing algorithms: Research methods for detecting discrimination on internet platforms. Paper presented at *Data and Discrimination: Converting Critical Concerns into Productive Inquiry*, ICA preconference.
- Shi, W., & Li, J. (2024). New digital divide shaped by algorithm? Evidence from agent-based testing on Douyin's health-related video recommendation. *Communication Research, 51*(7), 867–890. https://doi.org/10.1177/00936502241262056
- Sunstein, C. R. (2006). *Infotopia: How many minds produce knowledge*. Oxford University Press.
- Tomlein, M., Pecher, B., Simko, J., Srba, I., Moro, R., Stefancova, E., Kompan, M., Hrckova, A., Podrouzek, J., & Bielikova, M. (2021). An audit of misinformation filter bubbles on YouTube: Bubble bursting and recent behavior changes. In *Proceedings of RecSys '21* (pp. 1–11). https://doi.org/10.1145/3460231.3474241
- 数字传播与新媒体学刊. (2026). 算法推荐与"信息茧房"的再审视——基于抖音、小红书用户使用行为的实证调查 [Authors to be added]. https://onlinejandl.com/index.php/COMU/article/view/213
