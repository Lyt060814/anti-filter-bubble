# Research B: Algorithm audits, "bubble bursting", user controls, Chinese platforms, and diversity metrics

*For: HKU COMP1110 group project on filter bubbles / information cocoons (信息茧房). Compiled 27 Sep 2026.*

## How this was verified (please read)

- Every item below marked **Verified** had its title, authors/venue and URL/DOI appear in live web-search results during this session. The summaries use the abstracts and snippets returned by those searches.
- The sandbox **blocked direct page fetches** (arxiv.org, dl.acm.org, doi.org, mozillafoundation.org, ojs.aaai.org and others). So I could not open full PDFs. Where a detail (such as the exact number of agents) did not appear in a search result, I either left it out or tagged it **UNVERIFIED**.
- The search budget ran out before I could check a few classic metric papers. They are listed in Section 5b as **UNVERIFIED**, with DOIs from memory. Check them on Google Scholar before citing.

---

## 1. Sock-puppet audits of recommender feeds

### 1.1 YouTube

**[A1] Ribeiro, M. H., Ottoni, R., West, R., Almeida, V. A. F., & Meira Jr., W. (2020). Auditing radicalization pathways on YouTube. *Proc. FAT\* '20*, 131–141.** DOI: https://doi.org/10.1145/3351095.3372879 · preprint https://arxiv.org/abs/1908.08313 · code https://github.com/manoelhortaribeiro/radicalization_youtube. **Verified.**
- *Method and finding:* This is a large-scale data audit, not a logged-in sock-puppet audit. The authors analysed 330,925 videos from 349 channels, grouped as Media, Alt-lite, Intellectual Dark Web and Alt-right. They traced commenting users over time and simulated random walks on non-personalised recommendations. Users were found to migrate steadily from milder to more extreme communities. Alt-right channels were reachable through channel recommendations, though mostly not through video recommendations (the migration and random-walk detail is from memory, UNVERIFIED).
- *How we could use it:* It shows how to define content **categories** in advance and measure "pathways" between them. We could reuse the idea with lifestyle categories instead of political ones.

**[A2] Haroon, M., Wojcieszak, M., Chhabra, A., Liu, X., Mohapatra, P., & Shafiq, Z. (2023). Auditing YouTube's recommendation system for ideologically congenial, extreme, and problematic recommendations. *PNAS* 120(50), e2213020120.** DOI: https://doi.org/10.1073/pnas.2213020120 · PDF https://web.cs.ucdavis.edu/~zubair/files/haroon-pnas.pdf. **Verified.**
- *Method and finding:* 100,000 automated sock puppets were each trained on partisan content and then followed "up-next" recommendation trails. YouTube recommends mostly ideologically congenial content, and this grows deeper into the trail for right-leaning puppets. The share of problematic (extremist or conspiratorial) recommendations is low, at most 2.5%. Even so, 36.1% of puppets meet at least one, rising to about 40% for very-right puppets.
- *Debiasing "intervention":* An earlier preprint by the same team proposed a mitigation that injects counter-balancing videos into the watch history ("YouTube, The Great Radicalizer? Auditing and Mitigating Ideological Biases in YouTube Recommendations", arXiv 2022). **UNVERIFIED in this session**, because I did not see the URL.
- *How we could use it:* The **"depth in trail"** measure (the share of in-bubble items at step k) is a simple metric we can copy. The small-proportion-but-high-reach framing is also useful: "X% of our accounts met Y at least once".

**[A3] Tomlein, M., Pecher, B., Simko, J., Srba, I., Moro, R., Stefancova, E., Kompan, M., Hrckova, A., Podrouzek, J., & Bielikova, M. (2021). An audit of misinformation filter bubbles on YouTube: Bubble bursting and recent behavior changes. *RecSys '21*.** DOI: https://doi.org/10.1145/3460231.3474241 · arXiv https://arxiv.org/abs/2203.13769 · data and code https://github.com/kinit-sk/yaudit-recsys-2021. **Verified. Won Best Paper at RecSys 2021.**
- *Method and finding:* Pre-programmed agents first watched misinformation-promoting videos to "fall in". They then watched debunking videos to try to "burst" the bubble. Topics included 9/11, the moon landing, chemtrails, flat earth and vaccines (topic list from memory, UNVERIFIED). Bursting the bubble by watching debunking content **is possible, but the effect differs by topic**. The paper also compared its results with an earlier audit (Hussein et al. 2020) and found YouTube's behaviour had changed.
- *How we could use it:* This is the **closest template for our project**: a two-phase design (fall in, then escape). It measures both directions, not only how fast users fall in.

**[A4] Srba, I., Moro, R., Tomlein, M., Pecher, B., Simko, J., Stefancova, E., Kompan, M., Hrckova, A., Podrouzek, J., Gavornik, A., & Bielikova, M. (2023). Auditing YouTube's recommendation algorithm for misinformation filter bubbles. *ACM Transactions on Recommender Systems* 1(1), Article 6.** DOI: https://doi.org/10.1145/3568392 · arXiv https://arxiv.org/abs/2210.10085. **Verified.**
- *Method and finding:* The extended journal version of [A3]. It explicitly asks **how fast a user gets into a misinformation bubble** and **what it takes to burst it**, using the same fall-in-then-debunk agent design. It also annotates recommendations and search results for misinformation stance.
- *How we could use it:* It frames the two quantities we want to measure: time-to-bubble and time-to-burst. The annotation scheme (promoting, debunking or neutral) could be adapted to "in-niche vs out-of-niche".

**[A5] Mozilla Foundation (2022, 20 Sept). *Does This Button Work? Investigating YouTube's ineffective user controls.*** Report: https://www.mozillafoundation.org/en/research/library/user-controls/report/ · PDF https://assets.mofoprod.net/network/documents/Mozilla-Report-YouTube-User-Controls.pdf · press summary https://techcrunch.com/2022/09/20/youtubes-dislike-and-not-interested-options-dont-do-much-for-your-recommendations-study-says/. **Verified.**
- *Method and finding:* 22,722 volunteers used the RegretsReporter browser extension, generating data on more than 567 million video recommendations. The study was a randomised experiment (with Thoughtworks) plus a user survey. Compared with a control group, **"Don't recommend channel" prevented about 43% of unwanted recommendations, "Dislike" 12% and "Not interested" 11%**. In the survey, 39.3% felt the controls did not change their recommendations at all.
- *How we could use it:* It is a direct precedent for testing **escape buttons** such as 不感兴趣. Its metric is "% of unwanted recommendations prevented compared with a control". It also shows why we need a **control account that does nothing**.

**[A6] Liu, A., Wu, S., & Resnick, P. (2024). How to train your YouTube recommender to avoid unwanted videos. *Proc. ICWSM* 18(1), 930–942.** https://ojs.aaai.org/index.php/ICWSM/article/view/31363 · arXiv https://arxiv.org/abs/2307.14551. **Verified.**
- *Method and finding:* Sock-puppet agents ran a **"stain phase"** (watching many videos on one topic) followed by a **"scrub phase"** (using disinterest tools). Staining clearly increased the topic's share on the homepage. In the scrub phase, **"Not interested" worked best, removing on average 88% of the topic's homepage recommendations**. Neither phase had much effect on the recommendations beside a video. In a survey of 300 people, 44% did not know the "Not interested" button existed.
- *How we could use it:* **The stain-then-scrub design is exactly our research question.** Its results also conflict with Mozilla's [A5] (11% vs 88% for "Not interested"). That shows the **measurement surface matters**: homepage vs up-next, and bots vs real users.

**[A7] Hosseinmardi, H., Ghasemian, A., Rivera-Lanas, M., Horta Ribeiro, M., West, R., & Watts, D. J. (2024). Causally estimating the effect of YouTube's recommender system using counterfactual bots. *PNAS* 121(8), e2313377121.** DOI: https://doi.org/10.1073/pnas.2313377121. **Verified** (title, venue, first authors and main finding; the co-author list after Horta Ribeiro is from memory).
- *Method and finding:* "Counterfactual bots" first replay a real user's history. Then one bot keeps following the user's choices while its twin follows only the algorithm's recommendations. On average, **recommendations pushed bots toward more moderate content than the users chose themselves**, so user preference dominates. The paper also estimates a "forgetting time": how many videos it takes for the sidebar to stop reflecting partisan history after the bot switches to moderate viewing (**UNVERIFIED detail**, from memory).
- *How we could use it:* It is one of the few papers that quantifies **how fast the algorithm "forgets"**, which is our escape-speed question. It also argues for a **paired, twin-account design**.

**[A8] Brown, M. A., Bisbee, J., Lai, A., Bonneau, R., Nagler, J., & Tucker, J. A. (2022). Echo chambers, rabbit holes, and ideological bias: How YouTube recommends content to real users.** Brookings: https://www.brookings.edu/articles/echo-chambers-rabbit-holes-and-ideological-bias-how-youtube-recommends-content-to-real-users/ · SSRN https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4114905. **Verified.**
- *Method and finding:* Real users followed prescribed recommendation paths from their own accounts, a "real-user audit" (method detail from memory, UNVERIFIED). The algorithm **does not send most users down extremist rabbit holes**. It does narrow the ideological range, which the authors call a "(very) mild ideological echo chamber".
- *How we could use it:* It is a model for a **human-driven (manual) audit**, which is what our team would actually do.

### 1.2 TikTok

**[A9] Wall Street Journal (2021, July). *Inside TikTok's algorithm / How TikTok's algorithm figures you out* (video investigation).** Video: https://www.youtube.com/watch?v=nfczi2cI6Cs · summaries https://kottke.org/21/07/how-tiktoks-algorithm-figures-you-out and https://tidbits.com/2021/08/02/wall-street-journal-video-explores-tiktoks-troubling-algorithm/. **Verified** through secondary summaries; I did not see the wsj.com article URL.
- *Method and finding:* More than 100 bot accounts were each given secret interests, expressed only by **re-watching or pausing** on related videos. TikTok learned the interests in **under 2 hours, sometimes about 40 minutes**. Watch time was the key signal, and some bots drifted into rabbit holes such as depression content.
- *How we could use it:* It justifies a **"time-to-bubble" metric in minutes**. It also shows that **dwell time alone**, with no likes or follows, can be the only manipulated variable. That is easy for humans to do.

**[A10] Boeker, M., & Urman, A. (2022). An empirical investigation of personalization factors on TikTok. *Proc. ACM Web Conference 2022 (WWW '22)*.** DOI: https://doi.org/10.1145/3485447.3512102. **Verified.**
- *Method and finding:* Automated sock puppets varied one factor at a time. **Following had the strongest influence** on the For You feed, followed by liking and then video view rate. The factors also included location and language (detail from memory, UNVERIFIED).
- *How we could use it:* It gives a **one-factor-at-a-time design** for deciding which user action (like, follow, watch to the end) builds a bubble fastest.

**[A11] Vombatkere, K., Mousavi, S., Zannettou, S., Roesner, F., & Gummadi, K. P. (2024). TikTok and the art of personalization: Investigating exploration and exploitation on social media feeds. *Proc. ACM Web Conference 2024 (WWW '24)*.** DOI: https://doi.org/10.1145/3589334.3645600 · arXiv https://arxiv.org/abs/2403.12410. **Verified.**
- *Method and finding:* The authors treat a feed as a timeline and label each item as either **"exploitation"** (matching the user's known interests) or **"exploration"** (new). They propose metrics for how personalised a timeline is, and validate them against bot accounts and a random baseline on real TikTok data. They also measure how viewing duration, liking and following drive personalisation.
- *How we could use it:* The **exploration-vs-exploitation labels are a ready-made coding scheme** for our logged feeds, for example "% exploration items per session".

**[A12] Mosnar, M., Skurla, A., Pecher, B., Tibensky, M., Jakubcik, J., Bindas, A., Sakalik, P., & Srba, I. (2025). Revisiting algorithmic audits of TikTok: Poor reproducibility and short-term validity of findings. *SIGIR '25*.** DOI: https://doi.org/10.1145/3726302.3730293 · arXiv https://arxiv.org/abs/2504.18140 · data https://zenodo.org/records/16792218. **Verified.**
- *Method and finding:* The authors re-ran earlier TikTok sock-puppet audits in early 2025. The **earlier findings did not reproduce**. **Watching is now the strongest personalisation signal**, stronger than liking or following, and grows with watch duration, which contradicts [A10]. **Conclusions also flipped depending on which metric was chosen.**
- *How we could use it:* It is an important **limitation to cite**: our results are a snapshot. We should **report more than one metric**, for example entropy and top-category share.

**[A13] Ibrahim, H., Jang, H. D., Aldahoul, N., Kaufman, A. R., Rahwan, T., & Zaki, Y. (2025). TikTok's recommendations skewed towards Republican content during the 2024 U.S. presidential race.** arXiv preprint https://arxiv.org/abs/2501.17831. **Verified** as a preprint; peer-reviewed venue unknown.
- *Method and finding:* 323 sock-puppet experiments ran in Texas, New York and Georgia, with accounts seeded with partisan content. About 394,000 videos were viewed and labelled between 30 April and 11 November 2024. The algorithm showed an **asymmetric** skew toward Republican-leaning content.
- *How we could use it:* It shows how **many accounts** a large team needs (hundreds) against the **effect sizes** found (about 10%), which helps us calibrate what a small team can and cannot detect.

**[A14] (UMAP 2026) Algorithmic audit of personalisation drift in polarising topics on TikTok. *Proc. 34th ACM UMAP*.** DOI: https://doi.org/10.1145/3774935.3806161 · arXiv https://arxiv.org/abs/2603.20723 · dataset https://zenodo.org/records/19144520. **Verified** (title, venue, DOI and findings). Authors: **UNVERIFIED** (likely the KInIT group).
- *Method and finding:* Sock puppets on TikTok's web interface covered 5 topics (flat earth, US politics, vaccination, climate change, and a **neutral control topic: cooking**), each with supporting or opposing stances. Drift toward users' preferences was strong. There was a **neutralising effect for misinformation topics** and reinforcement for US politics.
- *How we could use it:* It is **one of the few audits with a non-political "lifestyle" topic (cooking)** as a baseline, which directly supports auditing lifestyle niches.

**[A15] Kaplan, L., Patel, D., Gerzon, N., Mislove, A., & Sapiezynski, P. (2026). When 'For You' isn't for you: Measuring user agency in TikTok's algorithmic feed. *Proc. ICWSM* 20(1), 1175–1189.** https://ojs.aaai.org/index.php/ICWSM/article/view/42688 · arXiv https://arxiv.org/abs/2605.10690. **Verified.**
- *Method and finding:* The team audited the TikTok **mobile app** through emulator control, app modification and network-traffic interception. They could replicate an account's history to ask "what if" questions. The feed responds to explicit and implicit signals. However, **"Not Interested" is the most effective explicit signal and is buried in the interface**. When accounts **stop signalling disinterest, many feeds are dominated by the unwanted topic again**.
- *How we could use it:* **This is the single most relevant "escape" paper.** It shows that escape can be **temporary**, so we should keep measuring after the scrub phase ends: a relapse metric.

**[A16] Center for Countering Digital Hate (2022, Dec). *Deadly by Design.*** https://counterhate.com/research/deadly-by-design/ · PDF https://counterhate.com/wp-content/uploads/2022/12/CCDH-Deadly-by-Design_120922.pdf. **Verified.**
- *Method and finding:* This was a **manual** audit. There were 8 new accounts: 2 per country in the US, UK, Canada and Australia, all registered as 13-year-olds, one per pair with "loseweight" in the username. The accounts paused on and liked body-image and mental-health videos. Suicide content appeared **within 2.6 minutes** and eating-disorder content **within 8 minutes**. The "loseweight" accounts received 12 times more self-harm content. The session length (about 30 minutes per account) is from memory, UNVERIFIED.
- *How we could use it:* **This is the feasibility benchmark: 8 accounts, hand-run, in short sessions.** It reports "minutes until first X" as its time-to-bubble metric.

**[A17] Amnesty International (2023, Nov). *Driven into the Darkness: How TikTok's 'For You' feed encourages self-harm and suicidal ideation.*** PDF https://cdn.amnesty.at/media/11311/amnesty-report_driven_into_the_darkness_how-tiktoks-for-you-feed-encourages-self-harm-and-suicidal-ideation_november-2023.pdf · news https://www.amnesty.org/en/latest/news/2023/11/tiktok-risks-pushing-children-towards-harmful-content/. **Verified.**
- *Method and finding:* The automated part used more than 30 bot accounts posing as 13-year-olds in Kenya and the US, supported by AI Forensics. After 5–6 hours, **nearly 1 in 2 videos** were mental-health related, about 10 times the control. The manual part used 1 account each in Kenya, the Philippines and the US. Within **3–20 minutes of manual re-watching**, more than half of the feed was mental-health content.
- *How we could use it:* It shows **manual accounts reach a bubble faster than bots**, which is encouraging for a student team. The 3-country design is a model for comparing locations, such as an HK vs mainland SIM, if relevant.

**[A18] Amnesty International (2025, Oct). *Dragged into the rabbit hole: New evidence of TikTok's risks to children's mental health* (France).** PDF https://www.amnesty.org/en/wp-content/uploads/2025/10/POL4003602025ENGLISH.pdf · news https://www.amnesty.org/en/latest/news/2025/10/tiktok-steering-children-towards-depressive-and-suicidal-content/. **Verified.**
- *Method and finding:* **3 hand-run accounts** posed as 13-year-olds: two girls and one boy. Within 5 minutes, before any signal, "sad/depressive" content appeared. **By 15–20 minutes feeds were almost entirely mental-health content**. Within 3–4 hours, videos romanticising suicide appeared.
- *How we could use it:* It shows that **3 accounts over a few hours** is publishable NGO-grade evidence. It is a replication two years after [A17], after the TikTok "refresh" feature launched ([C6]).

### 1.3 Instagram / Reels

**[A19] Accountable Tech & Design It For Us (2025, May). *Scary Feeds: The Reality of Teen Accounts.*** https://accountabletech.org/research/scary-feeds-the-reality-of-teen-accounts/. **Verified.**
- *Method and finding:* 5 new Instagram Teen Accounts were run by young adult participants (it is unclear from the search summary how long testing lasted). **All 5 were shown "sensitive content"**, and 4 of 5 participants reported distressing experiences.
- *How we could use it:* A **5-person, 5-account** study, the same size as our team, so a direct feasibility precedent.

**[A20] 5Rights Foundation (2025, Apr). *Is Instagram now safe for teens? Instagram Teen Accounts case study.*** PDF https://5rightsfoundation.com/wp-content/uploads/2025/04/TeenAccounts_Case-Study_Final.pdf. **Verified** (URL and headline findings seen; the finding may partly come from the Accountable Tech report, so it is attributed with caution).
- *Summary:* 100% of teen test accounts got "sensitive" images or Reels, 80% got potentially harmful health content, and failures were concentrated in Reels.
- *How we could use it:* It supports treating **Reels-style short video** as the highest-risk surface.

> **Gap:** I found **no peer-reviewed sock-puppet audit of Instagram Reels specifically about filter bubbles or diversity**. Existing work is NGO child-safety testing.

---

## 2. Chinese platforms (Douyin, Xiaohongshu, Kuaishou, Bilibili, Toutiao, Weibo)

**[B1] Shi, W., & Li, J. (2024). New digital divide shaped by algorithm? Evidence from agent-based testing on Douyin's health-related video recommendation. *Communication Research* 51(7), 867–890.** DOI: https://doi.org/10.1177/00936502241262056. **Verified. Won an ICA 2024 Top Paper award.**
- *Method and finding:* The authors used automated "agent-based testing" on Douyin. Virtual users on **different phone models**, standing in for socioeconomic status, watched health videos. **Cheaper phones received a smaller share of authenticated (credible) health videos**, which suggests an algorithmic "new digital divide".
- *How we could use it:* **This is the main peer-reviewed sock-puppet audit of Douyin.** It shows that **device/account attributes** are a variable worth controlling for; our team should use similar phones.

**[B2] Jinan University team (2025). News diversity under algorithms: The effects of pre-selected and self-selected personalization on Chinese TikTok (Douyin). *Digital Journalism* 13(7), 1190–1208.** DOI: https://doi.org/10.1080/21670811.2025.2450312. **Verified** (title, journal, pages). Authors **UNVERIFIED**, likely Shi, W., Li, J. and colleagues. Chinese coverage: https://www.nfnews.com/content/p3ZO0wmk6l.html.
- *Method and finding:* Agent-based testing compared three conditions: **pure random exposure**, **algorithmic (pre-selected) personalisation only**, and **algorithmic plus user (self-selected) choice**. **Personalised news on Douyin was *more* diverse in news categories than chance**, and algorithmic decisions contributed more to diversity than human choices did. The authors also tested whether widening interest scope or engaging with unmatched content increases balance.
- *How we could use it:* It supplies a **three-condition design** with a random baseline, and it is **evidence against a simple "cocoon" story on Douyin** for our literature review.

**[B3] Cai, Y., & Wang, F. (2024). Exploring the behavior of users "training" Douyin's personalized recommendation algorithm system in China. In *HCII 2024: Human Interface and the Management of Information*, LNCS, Springer.** https://link.springer.com/chapter/10.1007/978-3-031-60114-9_14. **Verified** (title and authors). Method details were not visible (**UNVERIFIED**; likely an interview/qualitative study).
- *How we could use it:* It is the Chinese counterpart to the "training the algorithm" folk-theory literature ([C1]–[C4]).

**[B4] Li, W., Kuo, J.-C., Sheng, M., Zhang, P., & Wu, Q. (2025). Beyond explicit and implicit: How users provide feedback to shape personalized recommendation content. *CHI '25*.** DOI: https://doi.org/10.1145/3706598.3713241 · arXiv https://arxiv.org/abs/2502.09869. **Verified.**
- *Method and finding:* 34 semi-structured interviews in Mandarin (Dec 2022–Apr 2023) with users of **Xiaohongshu, Douyin** and similar apps. The paper introduces **"intentional implicit feedback"**: deliberately lingering, searching or skipping to steer the feed. Users used it especially to **increase diversity**.
- *How we could use it:* It tells us which **realistic escape strategies** Chinese users actually use (search, deliberate dwell, 不感兴趣), so our scrub conditions can mirror them.

**[B5] 《算法推荐与"信息茧房"的再审视——基于抖音、小红书用户使用行为的实证调查》, *数字传播与新媒体学刊* (Journal of Digital Communication and New Media), 2026-03-12.** https://onlinejandl.com/index.php/COMU/article/view/213. **Verified** (title, journal, findings). Authors **UNVERIFIED**.
- *Method and finding:* Semi-structured interviews with 20 users plus **7-day usage logs** on Douyin and Xiaohongshu. Cocoons were more likely among **passive, low-intervention users**. Douyin's stronger push-recommendation mode showed stronger cocoon effects than Xiaohongshu's search-plus-recommendation mode. **Active interventions (不感兴趣, searching) noticeably reduced homogeneity.**
- *How we could use it:* It is the **closest Chinese-language precedent** in scale (20 people, 7 days of logs). Its claim about 不感兴趣 is **self-reported and log-based, not a controlled audit**: that is our gap.

**[B6] 杨洸, 佘佳玲 (2020). 新闻算法推荐的信息可见性、用户主动性与信息茧房效应：算法与用户互动的视角. *新闻大学* 2020(2).** https://jil.nju.edu.cn/xgyj/2021zq/20210121/i186471.html · CQVIP http://dianda.cqvip.com/Qikan/Article/Detail?id=7101655025. **Verified.**
- *Method and finding:* A questionnaire survey of **Toutiao (今日头条)** users. Algorithmic news recommendation **did not create a simple cocoon effect** and could widen exposure. Users and algorithms shape each other.
- *How we could use it:* It is a counter-evidence citation from a Chinese platform, though survey-based, not an audit.

**[B7] 渠润泽, 徐敬宏 (2026). 解构"信息茧房"：算法、用户偏好与信息生态的动态交互. *新闻与传播研究* 2026(3).** PDF https://sjc.bnu.edu.cn/docs/2026-05/a83991a68bec4b19a7a357bf5bb6138b.pdf. **Partly verified**: the title, authors and SEM method appeared in the search snippet; I have **not read the findings (UNVERIFIED)**.
- *How we could use it:* A recent top Chinese journal paper for the literature review; check its findings before citing.

### 2.1 Regulation and platform "escape tools" in mainland China (context for our audit)

**[B8] 国家网信办等四部门 (2021/2022). 《互联网信息服务算法推荐管理规定》 (in force 1 Mar 2022), Art. 17.** https://www.cac.gov.cn/2022-01/04/c_1642894606364259.htm · English translation https://www.chinalawtranslate.com/algorithms/. **Verified.**
- Article 17 requires providers to offer **an option not targeted at personal characteristics, or a convenient way to switch off algorithmic recommendation**, and to stop immediately when the user switches it off.
- *How we could use it:* The **"关闭个性化推荐" switch is legally mandated**. Whether switching it off actually yields a diverse, non-personalised feed is an **auditable claim**.

**[B9] 中央网信办等四部门 (2024-11). 关于开展"清朗·网络平台算法典型问题治理"专项行动的通知.** https://www.cac.gov.cn/2024-11/24/c_1734143936205514.htm · https://www.gov.cn/zhengce/zhengceku/202411/content_6989143.htm. **Verified.**
- The campaign's first target is **信息茧房 caused by homogeneous recommendation**. It requires user-editable interest tags and better transparency. It ran from 12 Nov 2024 to 14 Feb 2025.

**[B10] Yicai Global (2025). Douyin, Xiaohongshu, other platforms tweak algorithms as China cracks down on info bubbles.** https://www.yicaiglobal.com/news/douyin-xiaohongshu-other-platforms-tweak-algorithms-as-china-cracks-down-on-info-bubbles · see also ECNS 2025-05-22 https://www.ecns.cn/news/sci-tech/2025-05-22/detail-ihersmuc8113570.shtml. **Verified.**
- Douyin added a **content-preference review/adjust** feature. Xiaohongshu added an **"Explore More" (one-tap bubble-breaking)** button. Douyin, Xiaohongshu, Weibo, Kuaishou, WeChat Channels and Bilibili all announced diversity and transparency measures.

**[B11] 南方都市报 (2025-04-23). 多平台上线"内容偏好调节"功能，能破除信息茧房吗？实测.** https://m.mp.oeeee.com/a/BAAFRD0000202504231074797.html · https://www.nfnews.com/content/v3aZkY9D61.html. **Verified.**
- This is a journalistic hands-on test. **Xiaohongshu** shows a pie chart of the past 1 or 7 days of browsing categories, lets users delete tags and add dozens more. **Weibo** has a similar "内容偏好管理" with three settings (decrease, default, increase). At the time, **Douyin and Kuaishou had no equally fine-grained control**.
- *How we could use it:* These tools **show a diversity measure (the category pie chart) to the user**. We can **screenshot it as a platform-reported "ground truth"** and compare it with our own coded entropy.

**[B12] 21世纪经济报道, 肖潇 & 袁清渠 (2025-01-21). 测评六大社交平台：推荐算法大起底.** https://www.21jingji.com/article/20250121/herald/c6607c75d2df5a75335e911f61437055.html. **Verified.**
- A journalistic evaluation of the recommendation transparency and controls of WeChat, Weibo, Douyin, Kuaishou, Xiaohongshu and Bilibili. It documents where the **个性化推荐 switch and 不感兴趣** are located on each app.
- *How we could use it:* A **practical map of where each escape tool sits** in each app, for our protocol.

**[B13] Xinhua (2025-04-16). 揭秘算法如何帮助用户打破"信息茧房"：抖音开放日公开算法原理.** http://www.news.cn/tech/20250416/cb30d07cc64f497b938b82f551204e05/c.html. **Verified.**
- Douyin's **own claim** that its multi-objective algorithm actively breaks cocoons.
- *How we could use it:* It states the claim our independent audit could test.

**[B14] 腾讯研究院 (2025-07). 算法破茧：从信息茧房到信息蜂房 (industry report).** https://tisi.org/32160/. **Verified** (URL and title). Content not read (**UNVERIFIED**).
- *How we could use it:* An industry perspective; treat it as grey literature.

> **Bilibili note:** One search summary said Bilibili added "此类内容过多" and "推荐过" as feedback reasons in its 不感兴趣 panel. It was attributed to a 2025 news round-up (https://www.xhby.net/content/s682fb82fe4b00b861f0b01da.html), but I could not open it, so this is **UNVERIFIED**.
>
> **Gap:** I found **no peer-reviewed sock-puppet audit of Xiaohongshu, Kuaishou, Bilibili or Weibo**, and **no controlled audit of any Chinese platform's escape tools** (不感兴趣, 关闭个性化推荐, 内容偏好调节, Xiaohongshu's "Explore More"). The Douyin audits ([B1], [B2]) study health and news, not lifestyle content, and not escaping.

---

## 3. User controls, user agency and "algorithmic folk theories"

**[C1] Karizat, N., Delmonaco, D., Eslami, M., & Andalibi, N. (2021). Algorithmic folk theories and identity: How TikTok users co-produce knowledge of identity and engage in algorithmic resistance. *Proc. ACM HCI* 5(CSCW2), 1–44.** DOI: https://doi.org/10.1145/3476046. **Verified.**
- *Method and finding:* 15 semi-structured interviews with US TikTok users. Users hold "folk theories" that the For You feed reflects, and suppresses, identities. They practise **algorithmic resistance**: deliberately liking, commenting or re-watching to "correct" the feed.
- *How we could use it:* Its **user strategies** can be operationalised as our scrub actions, and it gives us a vocabulary for our survey or interview questions.

**[C2] Simpson, E., & Semaan, B. (2021). For You, or For "You"? Everyday LGBTQ+ encounters with TikTok. *Proc. ACM HCI* 4(CSCW3), Article 252.** (The issue is dated Dec 2020; the paper is usually cited as 2021.) DOI: https://doi.org/10.1145/3432951. **Verified.**
- *Method and finding:* 16 interviews. The feed both affirms and violates identity, a pattern the authors call **"algorithmic exclusion"**. Users build self-organised practices to cope.
- *How we could use it:* Background on why users want to reshape their feed.

**[C3] Simpson, E., Hamann, A., & Semaan, B. (2022). How to tame "your" algorithm: LGBTQ+ users' domestication of TikTok. *Proc. ACM HCI* 6(GROUP), Article 22.** DOI: https://doi.org/10.1145/3492841. **Verified.**
- *Finding:* Users "domesticate" and **tame** the algorithm through deliberate interaction.
- *How we could use it:* It provides the "taming" concept for our framing: can a user deliberately tame the feed back to diversity?

**[C4] Siles, I., Valerio-Alfaro, L., & Meléndez-Moran, A. (2024; online 2022). Learning to like TikTok . . . and not: Algorithm awareness as process. *New Media & Society* 26(10), 5702–5718.** DOI: https://doi.org/10.1177/14614448221138973. **Verified.**
- *Method and finding:* **43 Costa Rican new users kept a diary for one month**, plus 7 focus groups. It identifies five activities, including **"training" the app** and **coping with oscillating relevance**.
- *How we could use it:* A **diary method over 1 month with new users** that 5 students could copy on themselves, as an autoethnographic complement to the audit.

**[C5] Vera, J. A., & Ghosh, S. (2025). "They've over-emphasized that one search": Controlling unwanted content on TikTok's For You page. *CHI '25*.** DOI: https://doi.org/10.1145/3706598.3713666 · arXiv https://arxiv.org/abs/2504.13895. **Verified.**
- *Method and finding:* 14 interviews. Users are frustrated that **a single search or interaction over-shapes the feed**. They make many attempts to remove unwanted content, with mixed success.
- *How we could use it:* Motivation for measuring the effect of **one "contaminating" action** (for example one search) and how long it persists.

**[C6] TikTok Newsroom (2023, 16 Mar). Introducing a way to refresh your For You feed on TikTok.** https://newsroom.tiktok.com/en-us/introducing-a-way-to-refresh-your-for-you-feed-on-tiktok-us · TechCrunch https://techcrunch.com/2023/03/16/tiktoks-new-feature-lets-you-refresh-your-for-you-feed-and-retrain-your-algorithm/. **Verified.**
- Settings → Content preferences → "Refresh your For You feed" makes recommendations behave as if the user had just signed up.
- *How we could use it:* It defines a **"reset" condition**. I found **no independent audit of whether the reset actually works** (gap), and Douyin's equivalent is unverified.

*(See also [A5] Mozilla, [A6] Liu et al., [A15] Kaplan et al. and [B4] Li et al. above, which are the empirical studies of controls.)*

---

## 4. Methodological guides for audits

**[D1] Sandvig, C., Hamilton, K., Karahalios, K., & Langbort, C. (2014). Auditing algorithms: Research methods for detecting discrimination on internet platforms.** Paper for the *Data and Discrimination* preconference at the 64th Annual Meeting of the International Communication Association, Seattle. PDF https://websites.umich.edu/~csandvig/research/Auditing%20Algorithms%20--%20Sandvig%20--%20ICA%202014%20Data%20and%20Discrimination%20Preconference.pdf. **Verified.**
- *Content:* It defines five audit designs: code audit, non-invasive user audit, scraping audit, **sock-puppet audit** and **crowdsourced/collaborative audit**, each with legal and ethical trade-offs (typology from memory of the paper; the PDF itself was not opened).
- *How we could use it:* Our method section can say: **"a manual sock-puppet audit (Sandvig et al., 2014)"**. Its ToS/ethics discussion should also be cited.

**[D2] Metaxa, D., Park, J. S., Robertson, R. E., Karahalios, K., Wilson, C., Hancock, J., & Sandvig, C. (2021). Auditing algorithms: Understanding algorithmic systems from the outside in. *Foundations and Trends in Human-Computer Interaction* 14(4), 272–344.** DOI: https://doi.org/10.1561/1100000083 · free PDF https://hci.stanford.edu/publications/2021/FnT_AuditingAlgorithms.pdf. **Verified.**
- *Content:* A book-length guide to how audits are designed: choosing inputs, controls, measurement and noise, ethics, and the gap between sock puppets and real users.
- *How we could use it:* **The main "how-to" to read before designing the protocol**, especially the sections on noise and controls. Its advice on running control accounts in parallel, because feeds change on their own, is from memory and UNVERIFIED.

**[D3] Mosnar et al. (2025)**, see [A12]: a **reproducibility checklist** in practice (publish your video IDs, your code and your metric choice).

---

## 5. Diversity and bubble metrics

### 5a. Verified sources on metrics

**[E1] Kunaver, M., & Požrl, T. (2017). Diversity in recommender systems – A survey. *Knowledge-Based Systems* 123, 154–162.** DOI: https://doi.org/10.1016/j.knosys.2017.02.009. **Verified.**
- *Summary:* A survey of diversity definitions, metrics and diversification algorithms since 2001, covering intra-list diversity, coverage, novelty and the accuracy–diversity trade-off.
- *How we could use it:* The **standard citation for defining diversity** in our report.

**[E2] Castells, P., Hurley, N., & Vargas, S. (2022). Novelty and diversity in recommender systems. In F. Ricci, L. Rokach & B. Shapira (Eds.), *Recommender Systems Handbook* (3rd ed.). Springer.** DOI: https://doi.org/10.1007/978-1-0716-2197-4_16 (2015 edition: https://doi.org/10.1007/978-1-4899-7637-6_26). **Verified.**
- *Summary:* The formal definitions of **intra-list diversity (ILD)**, novelty, **aggregate diversity/coverage**, **Gini** and **entropy-based** concentration metrics, and how to evaluate them.
- *How we could use it:* The **formula source** for our metrics section.

### 5b. UNVERIFIED classics (from memory; search budget exhausted; check before citing)

- Ziegler, C.-N., McNee, S. M., Konstan, J. A., & Lausen, G. (2005). Improving recommendation lists through topic diversification. *WWW '05*. DOI 10.1145/1060745.1060754. It is the origin of **intra-list similarity/diversity**. **UNVERIFIED.**
- Nguyen, T. T., Hui, P.-M., Harper, F. M., Terveen, L., & Konstan, J. A. (2014). Exploring the filter bubble: The effect of using recommender systems on content diversity. *WWW '14*. DOI 10.1145/2566486.2568012. It measures **diversity over time** for users who do and do not follow recommendations. **UNVERIFIED.**
- Hannak, A., Sapiezynski, P., Molavi Kakhki, A., Krishnamurthy, B., Lazer, D., Mislove, A., & Wilson, C. (2013). Measuring personalization of web search. *WWW '13*. DOI 10.1145/2488388.2488435. It is the canonical use of **Jaccard overlap between paired accounts plus a same-time control account to estimate noise**. **UNVERIFIED.**
- Helberger, N., Karppinen, K., & D'Acunto, L. (2018). Exposure diversity as a design principle for recommender systems. *Information, Communication & Society* 21(2). DOI 10.1080/1369118X.2016.1271900. It defines **"exposure diversity"**. **UNVERIFIED.**
- Vrijenhoek, S., et al. (2021). Recommenders with a mission: Assessing diversity in news recommendations. *CHIIR '21*. DOI 10.1145/3406522.3446019. It proposes normative diversity metrics. **UNVERIFIED.**

### 5c. Metric cookbook for our project

For a feed log in which each item is coded into one of K topic categories:

| Metric | Formula / definition | Used or motivated by | Interpretation |
|---|---|---|---|
| **Shannon entropy** (normalised) | H = −Σ pᵢ log pᵢ ; H_norm = H / log K | [E1], [E2]; Douyin diversity work [B2] | 1 = perfectly spread, 0 = single topic (full bubble) |
| **Top-category share / concentration** | max pᵢ | [A2] (share at trail depth), [A6] (topic fraction on homepage) | The easiest to explain; "bubble" can be defined as >50% |
| **Gini coefficient** over category counts | Standard Gini on sorted counts | [E2] | 0 = equal, 1 = concentrated |
| **Intra-list diversity (ILD)** | Mean pairwise dissimilarity (1 − same-category, or tag Jaccard distance) within a session's N items | [E2]; Ziegler 2005 (UNVERIFIED) | Works with tags/hashtags instead of fixed categories |
| **Coverage** | # distinct categories (or creators) seen / K | [E1] | Simple count |
| **Exploration rate** | % items not matching the seeded interest | [A11] Vombatkere | Directly measures "outside the bubble" |
| **Jaccard overlap between accounts** | \|A∩B\| / \|A∪B\| on creators/hashtags | Hannak 2013 (UNVERIFIED); cross-account comparison | Treatment vs control divergence; control vs control gives the noise floor |
| **Time-to-bubble** | Minutes, or number of items, until top-category share first exceeds a threshold (e.g. 50%) | [A9] WSJ (40 min–2 h), [A16] CCDH (2.6 / 8 min), [A17]/[A18] Amnesty (3–20 min) | "How fast do you fall in" |
| **Time-to-escape / % removed** | Items or sessions of the scrub action until share drops below baseline; or (share_before − share_after)/share_before | [A6] (88% removed), [A5] (43/12/11% prevented), [A3]/[A4] (bursting), [A7] (forgetting) | "How fast can you get out" |
| **Relapse** | Share of the unwanted topic N sessions **after** scrubbing stops | [A15] Kaplan | Whether escape lasts |

**Tip:** [A12] shows conclusions can flip with metric choice, so report **at least two** (for example top-category share and normalised entropy).

---

## 6. Synthesis (~300 words)

**What is well audited.** YouTube is the best-studied platform by far: radicalisation pathways [A1], ideological congeniality at scale [A2], misinformation bubbles *and bursting* [A3]/[A4], counterfactual "forgetting" [A7], and user-control efficacy [A5]/[A6]. TikTok has become the second hub. Researchers have studied which signals personalise the feed [A10]/[A12], exploration vs exploitation [A11], elections [A13], topic drift [A14], user agency [A15], and many NGO child-safety "rabbit-hole" audits [A16]–[A18]. Most audits concern **politics, misinformation or mental-health harm**. Non-political lifestyle content appears mainly as a *neutral control* (cooking in [A14]).

**What is NOT well audited.**
1. **Chinese platforms.** Only Douyin has peer-reviewed agent-based audits, and those study health divides [B1] and news diversity [B2]. I found **no sock-puppet audit of Xiaohongshu, Bilibili, Kuaishou or Weibo**. Evidence there comes from interviews/logs ([B4], [B5]), surveys ([B6]) or journalism ([B11], [B12]).
2. **Escape tools on Chinese apps.** 不感兴趣, 关闭个性化推荐 (legally required by Art. 17 [B8]), Xiaohongshu's 内容偏好调节 pie chart and "Explore More" button, and Weibo's preference slider were **introduced in 2024–25 under the 清朗 campaign [B9]/[B10] but never independently audited**. The platforms' own claims ([B13]) are untested.
3. **Escaping vs falling in.** Many studies report time-to-bubble in minutes ([A9], [A16]–[A18]). Only a handful measure escape: [A3]/[A4], [A6], [A7], [A15], and [A5] with real users. Two findings matter here: results conflict (Mozilla's 11% vs Liu et al.'s 88% for "Not interested"), and escape can be **temporary** ([A15]). **Reset features** (TikTok's "refresh" [C6]) have not been independently tested, as far as I found.
4. **Lifestyle niches** (beauty, food, fitness, travel on 小红书) as the bubble topic itself are almost unaudited.

**A clear gap our project can fill:** a small, manual **stain → scrub → relapse** audit of Xiaohongshu (and Douyin or Bilibili) on lifestyle topics. It would compare 不感兴趣, preference adjustment, and switching off personalisation against a do-nothing control, measuring entropy, top-category share, time-to-bubble and time-to-escape.

---

## 7. Feasibility: how small teams ran manual audits

| Study | Accounts | Duration | Items logged | Manual? |
|---|---|---|---|---|
| CCDH *Deadly by Design* [A16] | 8 (2 per country × 4) | Short first sessions (reported ~30 min each; exact length UNVERIFIED) | Every video in session | Yes |
| Amnesty 2025 France [A18] | 3 | Bubble reached in 15–20 min; ran 3–4+ h | All FYP videos coded | Yes |
| Amnesty 2023 manual part [A17] | 3 (Kenya, Philippines, US) | 3–20 min to >50% mental-health content; about 1 h | All FYP videos coded | Yes (plus 30+ bots) |
| Accountable Tech [A19] | 5 teen accounts | Not stated in the summary (UNVERIFIED) | Screenshots and notes | Yes (5 young people) |
| 数字传播与新媒体学刊 [B5] | 20 real users | 7 days of logs | Usage logs plus interviews | Yes (real users) |
| Siles et al. [C4] | 43 new users | 1 month of diaries | Diary entries | Yes (real users) |
| Tomlein/Srba [A3]/[A4]; Liu et al. [A6] | Tens of scripted agents (exact number UNVERIFIED) | Days to weeks | Thousands of recommendations | No (bots) |
| Haroon [A2] / Ibrahim [A13] | 100,000 / 323 runs | Months | ~394k videos in [A13] | No (bots) |

**Implications for 5 first-year students:**
- A **manual audit of 5–10 fresh accounts** (one or two per student) is well within NGO precedent ([A16]–[A19]). Include **at least one do-nothing control account** per platform ([A5], [D2]).
- Suggested scale: **7–10 days × one 15–20 min session per day × first 30–50 feed items logged per session**. That gives about 10 accounts × 10 sessions × 40 items ≈ **4,000 coded items**. Code each item into roughly 8–12 topic categories in a shared spreadsheet, and use **screen recording** so coding can be checked.
- Phases: **baseline (day 1) → stain (days 2–4: dwell/like one lifestyle niche) → scrub (days 5–7: one escape tool per account: 不感兴趣 / 内容偏好调节 / 关闭个性化推荐 / "Explore More" / nothing) → relapse check (days 8–10: normal neutral scrolling)**. This mirrors [A6] and [A15].
- **Control for noise:** use the same phone model and OS ([B1] shows device matters), the same time of day, a fresh SIM/phone number per account if possible, and log out or clear the app between accounts.
- **Threats to validity to acknowledge:** results are a short-term snapshot ([A12]); category coding needs two coders and an agreement check; account creation may breach platform terms, so discuss ethics and keep the study non-commercial ([D1], [D2]).

---

## 8. Further leads (title and URL seen in searches, content NOT checked; UNVERIFIED)

- *Auditing Algorithmic Personalization in TikTok Comment Sections*, ICWSM 2026. https://ojs.aaai.org/index.php/ICWSM/article/view/42769
- *How Audit Methodologies Can Impact Our Understanding of YouTube's Recommendation Systems*, ICWSM 2024. https://ojs.aaai.org/index.php/ICWSM/article/download/31311/33471/35367 (arXiv 2303.03445)
- *Dynamics of Algorithmic Content Amplification on TikTok*, arXiv 2503.20231. https://arxiv.org/pdf/2503.20231
- *Auditing Exposure to Harmful Content on TikTok using Multimodal Language Models: A Cross-National, Age-Stratified Study*, arXiv 2608.17583. https://arxiv.org/pdf/2608.17583
- *Why am I seeing this: Democratizing End User Auditing for Online Content Recommendations*, arXiv 2410.04917. https://arxiv.org/pdf/2410.04917
- *Counting How the Seconds Count: Understanding Algorithm-User Interplay in TikTok via ML-driven Analysis of Video Content*, arXiv 2503.20030. https://arxiv.org/pdf/2503.20030
- *Everyday algorithm auditing* (Shen et al. 2021), arXiv 2105.02980. https://arxiv.org/pdf/2105.02980
- *The Research on Chinese College Students' View on the Information Cocoons on Douyin* (SEAA 2022, Atlantis Press). https://www.atlantis-press.com/proceedings/seaa-22/125976917
- *Measuring Users' Awareness of Content Recommendation Algorithm: A Survey on Douyin Users in Rural China* (iConference 2023, LNCS). https://dl.acm.org/doi/10.1007/978-3-031-28035-1_15
- *PILOT: Control Surfaces for Authoring Social Media Feeds*, arXiv 2509.19615. https://arxiv.org/pdf/2509.19615
