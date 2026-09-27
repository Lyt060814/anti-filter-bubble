# Research C: Regulation, platform features, news and local (HK / mainland / student) context
COMP1110 group project on filter bubbles / information cocoons (信息茧房). Compiled 2026-09-27.

## How this was checked (please read)
- **WebFetch was blocked** by the sandbox's network egress proxy for every domain tried (cac.gov.cn, news.cn, qq.com, oeeee.com, cssn.cn, ithome.com, chinalawtranslate.com, wikipedia.org, reutersinstitute, cnbc.com, arxiv.org). I could not open any page in full.
- Every item below comes from **WebSearch results**: the title and URL were returned by the search engine, and the details come from the search engine's summary of those pages. Nothing is invented, but **none of it has been read on the original page**. Before citing anything in the report, open the URL and check the exact wording, figures and date.
- **UNVERIFIED** marks claims where the search summary was vague or possibly mixed up sources, or where I could not tie a date or number to a specific URL.
- The web-search budget (200 calls per session) ran out near the end, so the Hong Kong student section (5) is thinner than planned. See "Gaps" at the end.

---

## 1. China: CAC regulation of algorithmic recommendation

### 1.1 《互联网信息服务算法推荐管理规定》 (Provisions on the Administration of Algorithmic Recommendation for Internet Information Services)
- **Source:** CAC and three other ministries. Full text: https://www.cac.gov.cn/2022-01/04/c_1642894606364259.htm . Release notice: https://www.cac.gov.cn/2022-01/04/c_1642894606258238.htm . Mirror (Ministry of Public Security): https://www.mps.gov.cn/n6557558/c8304289/content.html . English translation: https://www.chinalawtranslate.com/algorithms/
- **Date:** published 4 Jan 2022; in force **1 Mar 2022**. The draft for comment was issued 27 Aug 2021: https://www.cac.gov.cn/2021-08/27/c_1631652502874117.htm
- **Summary:** **Art. 17** has three parts. (1) Providers must offer an option that is not based on the user's personal characteristics, or an easy way to switch algorithmic recommendation off, and must stop at once when the user switches it off. (2) Providers must let users choose or delete the user tags that are based on their personal characteristics. (3) Where an algorithm significantly affects a user's interests, the provider must explain it and take responsibility. Xinhua's explainer "五大看点" (five highlights): http://www.news.cn/politics/2022-01/06/c_1128238896.htm
- **Relevance:** This is the legal basis for the "turn off personalization" switch and tag management we can test on real apps. It has been in force for more than 4 years, but few evaluations exist.

### 1.2 "清朗·网络平台算法典型问题治理" special campaign (Qinglang campaign on typical problems in platform algorithms), explicitly targeting 信息茧房
- **Source:** Notice issued by CAC and three other departments. https://www.cac.gov.cn/2024-11/24/c_1734143936205514.htm ; also on gov.cn: https://www.gov.cn/zhengce/zhengceku/202411/content_6989143.htm ; news coverage: https://www.chinanews.com.cn/gn/2024/11-24/10324768.shtml , https://m.bjnews.com.cn/detail/1732433475129815.html
- **Date:** announced **24 Nov 2024**; the campaign ran until **14 Feb 2025**.
- **Summary:** It lists five focus areas. The first is homogeneous pushes that create information cocoons ("同质化推送营造'信息茧房'"). On cocoons, platforms must: build a cocoon-prevention mechanism and make pushed content more diverse; never push highly homogeneous content to induce addiction; never force users to pick interest tags; never record illegal or harmful content as a user tag; and set up "不感兴趣" (not interested) negative feedback properly. Beijing News quoted experts saying algorithm rules need external review: https://m.bjnews.com.cn/detail/1732456868129058.html
- **Relevance:** This is the first time a Chinese regulator named 信息茧房 as a problem to fix. It gives a clear policy hook ("did the fix work?").

### 1.3 CAC progress report: "中央网信办持续加强信息推荐算法治理" (CAC continues to strengthen governance of recommendation algorithms)
- **Source:** CAC, https://www.cac.gov.cn/2025-05/22/c_1749536203490537.htm ; syndicated at https://www.chinanews.com.cn/gn/2025/05-22/10419958.shtml and https://www.bbtnews.com.cn/2025/0522/557779.shtml
- **Date:** **22 May 2025**
- **Summary:** CAC says it directed Douyin, Xiaohongshu, Weibo, Kuaishou, WeChat Channels (视频号), Bilibili and others to optimize four areas: weighted recommendation of "positive energy" content, user choice, content diversity, and transparency. The platforms signed a "算法向善" (algorithms for good) Nanning declaration and published their algorithm rules. They launched features named **"茧房评估"** (cocoon assessment) and **"一键破茧"** (one-tap cocoon breaking). Douyin upgraded its **"使用管理助手"** (usage management assistant), which now visualizes the user's recent viewing. Xiaohongshu added **"内容偏好评估与调节"** (content-preference assessment and adjustment) and **"探索更多"** (explore more). CAC promised routine inspections and more "多样化破茧路径" (diverse ways to break the cocoon).
- **Relevance:** This is the official list of the anti-cocoon features. Our project could audit exactly these features.

### 1.4 Follow-ups in 2026
- **(a) Draft revision of 《互联网信息服务管理办法》 (Measures on Internet Information Services), second round of public comment.** CAC notice: https://www.cac.gov.cn/2026-07/03/c_1784822399677167.htm ; Xinhua: https://www.news.cn/20260703/bb8af7abe671483dbc4603cd78175eff/c.html ; full text with the comment deadline: https://www.elawcn.com/rule/2026/0703/1862.html ; Southern Metropolis Daily (南都): https://m.mp.oeeee.com/a/BAAFRD0000202607031620435.html ; compliance commentary: https://www.secrss.com/articles/92409
  - **Dates:** published **3 Jul 2026**; comments closed **2 Aug 2026**.
  - **Summary:** The draft grows from 27 to 94 articles and adds a chapter on "智能信息服务" (intelligent information services). It bans forcing users to use AI or intelligent services, bans using algorithms to disrupt public opinion or evade supervision, and bans recording prohibited or harmful content as user interest points or tags. **UNVERIFIED:** whether the new text itself contains an explicit 信息茧房 or "turn off personalization" clause. The search summary only repeated the 2022 Art. 17 wording.
  - **Relevance:** Very recent (Jul–Aug 2026). It shows algorithm rules moving into a higher-level regulation.
- **(b) 《人工智能拟人化互动服务管理暂行办法》 (Interim Measures on AI Anthropomorphic Interactive Services).** Text: https://www.cac.gov.cn/2026-04/10/c_1777558395078289.htm ; CAC Q&A: https://www.cac.gov.cn/2026-04/10/c_1777558395284407.htm ; IT之家 (IT Home): https://www.ithome.com/0/938/006.htm
  - **Dates:** published **10 Apr 2026**; in force **15 Jul 2026**.
  - **Summary:** Regulates AI companion or "persona" chat services. The CAC lists the risks as emotional dependence, social alienation, cognitive manipulation and value steering, and it bans virtual partner or relative services for minors.
  - **Relevance:** A regulatory counterpart to "AI chatbot echo chambers". It links cocoons to generative AI.
- **(c) "清朗·整治AI应用乱象" campaign (Qinglang campaign on AI application misconduct).** https://www.cac.gov.cn/2026-04/30/c_1779289298718765.htm ; results of phase 1: https://www.chinanews.com.cn/gn/2026/07-06/10653724.shtml
  - **Dates:** launched **30 Apr 2026** (4 months, 2 phases); phase-1 results reported **6 Jul 2026**.
  - **Summary:** Targets AI-generated "数字泔水" (digital slop), fake information and similar abuses. In phase 1, more than 14,000 AI products were dealt with and more than 6 million items were removed.
  - **Relevance:** Shows that AI-generated content now floods recommendation feeds too.

---

## 2. Anti-cocoon features on Chinese platforms

| Platform | Feature (Chinese name) | Launch / report date | Source URL |
|---|---|---|---|
| Kuaishou 快手 | "信息茧房"自我评估 (self-assessment) and **"一键破茧"** (one-tap cocoon breaking). Path: top-left menu → 常用功能 (common functions) → **内容偏好** (content preferences). A pie chart shows the user's interest tags, and sliders set how strongly each tag is recommended. | Announced **20 May 2025** | https://finance.sina.com.cn/tech/digi/2025-05-20/doc-inexfkuz3668981.shtml ; https://news.zol.com.cn/985/9857452.html ; https://news.pconline.com.cn/1928/19284572.html |
| Douyin 抖音 | **使用管理助手 → 内容偏好** (usage management assistant → content preferences). Upgraded with 内容偏好评估 (preference assessment) and a visualization of recent viewing. CAC credits Douyin with "茧房评估" and "一键破茧". | Reported May 2025 | CAC link in 1.3; https://www.pai.com.cn/194577.html ; https://m.sohu.com/a/899094821_162758 |
| Xiaohongshu 小红书 | **我 → 设置 → 内容偏好调节** (Me → Settings → content-preference adjustment). A pie chart of the last 7 days or last day. Each category has 3 levels (减少推荐 / 默认 / 增加强度: less / default / more). Users can delete tags or add from dozens of others. Also **"探索更多"** (explore more). | Tested by Southern Metropolis Daily, Apr 2025 | https://www.nfnews.com/content/v3aZkY9D61.html ; https://epaper.oeeee.com/epaper/A/html/2025-04/29/content_4432.htm ; https://finance.eastmoney.com/a/202504243386299148.html |
| Weibo 微博 | **我的 → 设置 → 隐私设置 → 内容偏好管理** (Me → Settings → Privacy → content-preference management). Pie chart plus the same 3 levels. Also publishes its hot-search (热搜) rules. | Apr–May 2025 | same Southern Metropolis Daily sources; CAC 1.3 |
| Toutiao 今日头条 | Already lets users turn personalization on or off, change how often content outside their usual categories appears, and choose whether location, search history or follows are used. Pledged more algorithm transparency and anti-cocoon investment in 2025, and better "不感兴趣". | **6 Jan 2025** | https://news.qq.com/rain/a/20250106A0AVR100 ; https://www.ithome.com/0/822/680.htm |
| WeChat Channels 视频号 | Published 《一图读懂微信视频号算法推荐》 (WeChat Channels recommendation in one chart) and a 《算法破茧系列》 (cocoon-breaking series). Says recommendations run on two systems: a friends-based social one and an interest algorithm. Tencent said it would build a "破茧功能矩阵" (set of cocoon-breaking tools): easy switch-off, negative feedback, diversity assessment and custom categories. **UNVERIFIED:** the exact date and the exact source of the Tencent quote. | 2025 | https://cloud.tencent.com/developer/news/2377184 ; https://www.woshipm.com/share/6207300.html ; https://www.oschina.net/news/342428 |
| Bilibili 哔哩哔哩 | Added negative-feedback reasons "此类内容过多" (too much of this) and "推荐过" (already recommended). Joined the algorithm-disclosure effort by 20+ platforms (Shanghai government report, 9 Jan 2025). | Jan 2025 | https://www.shanghai.gov.cn/nw4411/20250109/7d6e3f8d9cf240769692a644fd90dde3.html |

- **"个性化推荐" on/off switches across apps (Weibo, WeChat, Bilibili, Douyin, Xiaohongshu).** These appeared around March, apparently in 2022 when the rules took effect. **UNVERIFIED:** the search summary was ambiguous about the year.

### 2.1 Douyin's public explanation of its algorithm
- **Title:** 抖音安全与信任中心 (Douyin Safety and Trust Center) website launch, then an open day
- **Sources:** 人民论坛网 (People's Tribune), https://www.rmlt.com.cn/2025/0331/726642.shtml ; 财联社 (CLS), https://www.cls.cn/detail/1988109 ; 新华网 (Xinhua), http://www.news.cn/tech/20250417/9b2e3622d8764c408c2b667bf73d1d29/c.html ; 经济参考报 (Economic Information Daily), http://jjckb.xinhuanet.com/20250415/47885102bbc5465db63398ae7b574049/c.html
- **Dates:** site (95152.douyin.com) announced **30 Mar 2025** at the 2025 China Internet Media Forum; open day **15 Apr 2025**.
- **Summary:** Douyin disclosed the principles of its recommender for the first time. The model predicts the probability of user actions and uses multi-objective modelling. Douyin says it balances **"100+ objectives"** (for example "收藏", saves), so the system does not keep pushing similar content, and it presents multi-objective optimization as a way to break cocoons.
- **Relevance:** This is the platform's own claim that it diversifies feeds. Our project can test the claim.

### 2.2 Evidence on use and effectiveness
- **Southern Metropolis Daily hands-on test, "多平台上线'内容偏好调节'功能，能破除信息茧房吗？实测"** ("Several platforms launch content-preference adjustment. Can it break cocoons? We tested it"). 23–29 Apr 2025. https://www.nfnews.com/content/v3aZkY9D61.html ; print edition "用户自选内容推荐强度 能破'信息茧房'?" ("Can letting users choose recommendation strength break cocoons?"), https://epaper.oeeee.com/epaper/A/html/2025-04/29/content_4432.htm . Journalists (南都·隐私护卫队, the paper's privacy team) walked through the Xiaohongshu and Weibo features. **UNVERIFIED:** whether they measured any change in feed diversity afterwards. The summary only describes the features.
  - **Relevance:** A journalistic walkthrough, not a systematic audit. That leaves a gap we can fill.
- **"'破茧'功能，何以真正破除'信息茧房'"** ("How can cocoon-breaking features actually break information cocoons?"). Theory page of 人民网 (People's Daily Online), http://theory.people.com.cn/n1/2026/0917/c40531-40800283.html ; also 科学网 (ScienceNet), https://news.sciencenet.cn/htmlnews/2026/9/571625.shtm , and Sina, https://finance.sina.com.cn/tech/discovery/2026-09-17/doc-inisayaf4206569.shtml . **17 Sep 2026.**
  - **Summary:** Argues that the features ("茧房评估", "一键破茧", "使用管理助手", "内容偏好评估与调节", "探索更多") have not changed the core logic of recommendation. The features sit deep inside Settings and are almost never promoted, so **usage is "极低" (very low)**. It also says that even after a user taps them, **the algorithm narrows back to old interests quickly** unless the user engages strongly with the new content. Proposals: interface-design guidelines that put these features in prominent places; yearly splash-screen or pop-up prompts; and "knowledge exploration" or "opinion balancer" modes. **UNVERIFIED:** the author, and whether "使用率极低" rests on any data.
  - **Relevance:** **10 days old at the time of writing.** It states our hypothesis ("the features are hard to find and their effect fades quickly") as an untested claim. This is ideal for a timely project.
- **Shenzhen University report 《短视频用户的算法实践与"破茧"报告》** ("Short-video users' algorithm practices and cocoon breaking"), by the 深圳大学深圳城市传播创新研究中心 (Shenzhen University centre for urban communication innovation). Released 7 Nov 2025; covered 11 Nov 2025. https://edu.cnr.cn/gc/20251111/t20251111_527426500.shtml ; https://finance.sina.com.cn/jjxw/2025-11-11/doc-infwzezw1963177.shtml ; https://news.mydrivers.com/1/1085/1085809.htm
  - **Summary:** Used simulated accounts on Douyin, Kuaishou, Bilibili, Xiaohongshu and WeChat Channels, a survey of 1,215 users and 20+ interviews. 77.8% of users say they see "unexpected but interesting" content. 73.9% say the algorithm helped them find new interests. More than 75% believe they can "tame" the algorithm. More than 65% use "不感兴趣" well. More than 60% actively try to break the cocoon. The report suggests cocoons may be "overstated". **UNVERIFIED:** the funder. Coverage appeared on Tencent's news site, and the Tencent Research Institute (腾讯研究院) published a related pro-algorithm report: "算法破茧｜腾讯研究院三万字报告" (a 30,000-character report on algorithms and cocoon breaking), https://tisi.org/32160/ , 10 Jul 2025 per https://news.qq.com/rain/a/20250710A06X7J00 .
  - **Relevance:** A counterpoint. It relies on self-reported perceptions, and our group could compare perception with measured diversity.
- **渠润泽 (Qu Runze) & 徐敬宏 (Xu Jinghong), "解构'信息茧房'：算法、用户偏好与信息生态的动态交互"** ("Deconstructing the information cocoon: dynamic interaction among algorithms, user preferences and the information ecosystem"). 《新闻与传播研究》 (Journalism & Communication), 2026 No. 3. PDF: https://sjc.bnu.edu.cn/docs/2026-05/a83991a68bec4b19a7a357bf5bb6138b.pdf
  - **Summary:** Uses structural equation modelling (SEM) and fsQCA (fuzzy-set qualitative comparative analysis). Perceived personalization combined with the user's own cognitive bias deepens the cocoon. Perceived transparency encourages active information seeking, which raises diversity and eases the cocoon. The authors propose a combined strategy: "透明度优化 × 多样性提升 × 主动寻求激励" (better transparency × more diversity × incentives for active seeking).
  - **Relevance:** A recent academic model. Its "transparency to active seeking" link is what features like 茧房评估 are supposed to trigger.
- **Other:** 央视网 (CCTV online), "算法推荐带来'信息茧房' 视野受限、认知固化 如何'破茧'？" ("Recommendation algorithms create cocoons: narrow views, fixed thinking. How to break out?"), 25 May 2025. https://news.cctv.cn/2025/05/25/ARTILGTQQwv1LNobO1aKtQER250525.shtml . 观察者网 (Guancha), "老外的中国'信息茧房'，被算法打碎了" ("Foreigners' 'information cocoon' about China was shattered by algorithms"), 4 Jun 2026. https://www.guancha.cn/economy/2026_06_04_819387.shtml . This one frames Xiaohongshu or Douyin algorithms as having broken Western users' cocoon about China; it was not read in full.

---

## 3. EU, US and other laws

### 3.1 EU Digital Services Act, Art. 38
- **Sources:** Article text, https://streamlex.eu/articles/dsa-en-art-38/ ; DSA Observatory analysis, https://dsa-observatory.eu/2024/11/22/the-regulation-of-recommender-systems-under-the-dsa-a-transition-from-default-to-multiple-and-dynamic-controls/ ; TechCrunch, "Coming soon to TikTok in Europe: A 'For You' feed without the TikTok algorithm", **4 Aug 2023**, https://techcrunch.com/2023/08/04/tiktok-algorithm-dsa/
- **Summary:** Very large online platforms (VLOPs) must offer **at least one recommender option that is not based on profiling** (as defined in the GDPR). From Aug 2023, TikTok EU users could turn personalization off, so For You and LIVE show popular videos from where they live and around the world. Analysts found platforms favour "transparency" over real "controllability". **UNVERIFIED:** Instagram and Facebook's own Aug 2023 non-personalized options. I did not reach a primary source for them.
- **Evaluations:** I found **no quantitative study of how many users take up the non-profiling option.** The search summary said so explicitly, and it is itself a research gap. Related pieces: DSA Observatory, "Making Recommender Systems Work for People" (19 May 2025), https://dsa-observatory.eu/2025/05/19/making-recommender-systems-work-for-people/ ; EU DisinfoLab, "Malicious semi-compliance", https://www.disinfo.eu/malicious-semi-compliance-as-platform-approach-to-eu-regulation/ ; ISD's TikTok recommender research before the 2025 German election, https://www.isdglobal.org/digital_dispatches/towards-transparent-recommender-systems-lessons-from-tiktok-research-ahead-of-the-2025-german-federal-election/ ; arXiv 2603.05653, "The DSA's Blind Spot: Algorithmic Audit of Advertising and Minor Profiling on TikTok", https://arxiv.org/pdf/2603.05653 (Mar 2026; sock-puppet audit method).
- **Relevance:** The EU equivalent of Art. 17. It suggests an East–West comparison, "an opt-out exists, but is it usable?"

### 3.2 Bits of Freedom v. Meta (Netherlands)
- **Sources:** NL Times, 26 Jan 2026, https://nltimes.nl/2026/01/26/meta-drops-appeal-court-ruling-requiring-non-algorithmic-social-media-timelines ; EDRi, https://edri.org/our-work/court-again-rules-in-favour-of-bits-of-freedom-freedom-of-choice-for-instagram-and-facebook-users-remains-intact/ ; the Platform Law Blog, 9 Oct 2025, https://the-platform-law.com/2025/10/09/the-bits-of-freedom-ruling-the-first-step-in-private-dsa-enforcement/ ; **DSA Observatory, "Ineffective by design: Bits of Freedom vs Meta…", 30 Jul 2026**, https://dsa-observatory.eu/2026/07/30/ineffective-by-design-bits-of-freedom-vs-meta-at-the-forefront-of-enforcing-user-control-for-recommender-systems-under-the-dsa/
- **Timeline:**
  - Suit filed 8 Sep 2025.
  - 2 Oct 2025: the court ruled that switching back to the profiled feed every time the app opens is a prohibited **dark pattern**, and that the user's choice must persist.
  - Meta changed its apps around 1 Jan 2026.
  - 26 Jan 2026: Meta dropped its appeal.
- **Relevance:** A legal finding that an opt-out which does not persist is ineffective by design. This matches the Chinese claim that the algorithm "narrows back" after a user taps 破茧.

### 3.3 EDRi complaint against YouTube
- **Sources:** https://edri.org/our-work/edri-files-dsa-complaint-against-youtube-for-undermining-user-autonomy/ ; complaint PDF, https://edri.org/wp-content/uploads/2026/03/EDRi-DSA-complaint-Youtube.pdf ; MLex, https://www.mlex.com/mlex/articles/2450279/google-facing-complaint-over-access-to-non-profiling-feed-on-youtube-in-eu
- **Date:** early **Mar 2026** (mentioned in EDRi-gram 18 Mar 2026).
- **Summary:** Complaint to the Belgian Digital Services Coordinator. Choosing YouTube's non-profiling option is hidden behind several settings screens, leaves a **blank homepage and deletes the watch history**, while switching back takes one click. EDRi alleges this breaches DSA Arts. 38, 27(3) and 25.
- **Relevance:** A concrete example of friction or "sludge" in opt-out design, which we can compare with Chinese apps.

### 3.4 EU Commission preliminary findings against TikTok
- **Sources:** 6 Feb 2026, addictive design, https://digital-strategy.ec.europa.eu/en/news/commission-preliminarily-finds-tiktoks-addictive-design-breach-digital-services-act ; **24 Jul 2026**, minors' accounts, https://ec.europa.eu/commission/presscorner/detail/en/ip_26_1679
- **Summary:** In February, the Commission found that TikTok had not assessed risks from infinite scroll, autoplay, push notifications and its **highly personalized recommender**. It suggested adapting the recommender, among other remedies. In July, it said minors' accounts should be private by default and minors' content should not be recommended in For You.
- **Relevance:** Personalized feeds are now treated as a systemic risk in EU enforcement (Jul 2026).

### 3.5 US: New York SAFE for Kids Act
- **Sources:** NY Attorney General press release (2026), https://ag.ny.gov/press-release/2026/attorney-general-james-and-governor-hochul-release-final-safe-kids-act-rules ; Governor's office, https://www.governor.ny.gov/news/governor-hochul-and-attorney-general-james-announce-final-safe-kids-act-rules-protect-children ; WBNG, **28 Jul 2026**, https://www.wbng.com/2026/07/28/hochul-letitia-james-issue-final-rules-new-york-safe-kids-act/ ; Covington's Inside Privacy, https://www.insideprivacy.com/childrens-privacy/new-york-publishes-final-safe-for-kids-act-rules/
- **Summary:**
  - Final rules released **28 Jul 2026**; in force **25 Jan 2027**.
  - Users under 18 cannot get an algorithmic **"addictive feed"** (or night-time notifications) without verifiable parental consent.
  - Rules cover age assurance, including at least one method besides government ID.
  - Penalties up to US$5,000 per violation.
- **Relevance:** Law that defaults young users to non-algorithmic (following or chronological) feeds.

### 3.6 Australia: "My Feed, My Way" (algorithm opt-out)
- **Sources:** Prime Minister's media release, https://www.pm.gov.au/media/my-feed-my-way ; **CNBC, 8 Sep 2026**, https://www.cnbc.com/2026/09/08/australia-social-media-algorithm-opt-out.html ; Newcastle Herald op-ed by Albanese, "Opt-out algorithm laws are a world first", https://www.newcastleherald.com.au/story/9346432/anthony-albanese-opt-out-algorithm-laws-are-a-world-first/
- **Summary:** Proposed under a draft Digital Duty of Care law. Platforms must notify new and existing users over 16 and let them choose an algorithmic or a follow-only feed. The choice must be respected each time the app opens. Fines up to A$109.2m (reported).
- **Relevance:** **Very recent (Sep 2026).** Western governments are now copying the approach China took in 2022, which makes a comparison with China timely.

### 3.7 Instagram "Your Algorithm"
- **Sources:** https://about.instagram.com/blog/announcements/reels-algorithm-control ; https://www.newsx.com/tech-and-auto/instagram-introduces-your-algorithm-allows-users-to-control-topics-across-feed-reels-and-explore-233084/ ; UNILAD Tech, 11 Sep 2026, https://www.uniladtech.com/social-media/instagram-opt-out-algorithm-button-to-change-feed-735531-20260911
- **Summary:** Launched **Dec 2025** for Reels in the US. It shows the topics Instagram thinks the user likes and lets them add, remove or mute topics. A 2026 roundup says it has since expanded to Feed, Reels and Explore for all English-language users. **UNVERIFIED:** the exact date of that expansion.
- **Relevance:** Close to 小红书/快手's "内容偏好" pie chart. Instagram is widely used by HK students, so it allows a cross-platform comparison on the same phones.

---

## 4. Recent news, 2026 (especially Jul–Sep)

| Date | Item | URL |
|---|---|---|
| 17 Sep 2026 | People's Daily Online theory piece "'破茧'功能，何以真正破除'信息茧房'": the features are buried, rarely used, and their effect fades. | http://theory.people.com.cn/n1/2026/0917/c40531-40800283.html |
| 11 Sep 2026 | UNILAD Tech: "Instagram actually has a button that lets you opt out of the algorithm" | https://www.uniladtech.com/social-media/instagram-opt-out-algorithm-button-to-change-feed-735531-20260911 |
| 8 Sep 2026 | Australia "My Feed, My Way" algorithm opt-out proposal | https://www.cnbc.com/2026/09/08/australia-social-media-algorithm-opt-out.html |
| 2 Sep 2026 | The Scholarly Kitchen: "When Your AI Knows You Too Well: Personalization, Sycophancy, and the Risk of an Intellectual Echo Chamber in AI-assisted Research". Argues that memory and personalization in chatbots plus sycophancy can create an echo chamber for one person. | https://scholarlykitchen.sspnet.org/2026/09/02/when-your-ai-knows-you-too-well-personalization-sycophancy-and-the-risk-of-an-intellectual-echo-chamber-in-ai-assisted-research/ |
| Sep 2026 (arXiv 2609.xxxxx) | "Delusions and Harms Associated with AI Chatbot Use: Early Evidence from 185 Real-World Reports" (UNVERIFIED: authors and exact date) | https://arxiv.org/pdf/2609.08027 |
| Aug 2026 (arXiv 2608.xxxxx) | "An Echo Chamber of One: Should AI Psychosis Be a Distinct Clinical Entity?" Covered by The Decoder: "Chatbots built an 'echo chamber of one'…" (UNVERIFIED: authors and exact date) | https://arxiv.org/pdf/2608.23937 ; https://the-decoder.com/chatbots-built-an-echo-chamber-of-one-and-now-psychiatry-has-to-decide-if-ai-psychosis-exists/ |
| 28 Aug 2026 | 《传媒》 (Media) magazine issue with the theme "算法生态" (algorithm ecosystem); articles on AI and algorithm-driven cultural communication | https://www.pressreader.com/china/media-5898/20260828/282136413312902 |
| 2 Aug 2026 | Comments close on the CAC draft 互联网信息服务管理办法 (section 1.4a) | https://www.elawcn.com/rule/2026/0703/1862.html |
| 30 Jul 2026 | DSA Observatory, "Ineffective by design: Bits of Freedom vs Meta" | https://dsa-observatory.eu/2026/07/30/ineffective-by-design-bits-of-freedom-vs-meta-at-the-forefront-of-enforcing-user-control-for-recommender-systems-under-the-dsa/ |
| 28 Jul 2026 | NY SAFE for Kids Act final rules | https://www.wbng.com/2026/07/28/hochul-letitia-james-issue-final-rules-new-york-safe-kids-act/ |
| 24 Jul 2026 | EU preliminary findings: TikTok minors' accounts and For You recommendation | https://ec.europa.eu/commission/presscorner/detail/en/ip_26_1679 |
| 15 Jul 2026 | China's AI anthropomorphic-interaction measures take effect | https://www.cac.gov.cn/2026-04/10/c_1777558395078289.htm |
| 6 Jul 2026 | CAC reports phase-1 results of the "清朗·整治AI应用乱象" campaign | https://www.chinanews.com.cn/gn/2026/07-06/10653724.shtml |
| 3 Jul 2026 | CAC second draft of 互联网信息服务管理办法 (94 articles, new chapter on intelligent services) | https://www.cac.gov.cn/2026-07/03/c_1784822399677167.htm |
| 19 Jun 2026 | HKFP on the Reuters DNR 2026 Hong Kong page (section 5) | https://hongkongfp.com/2026/06/19/reuters-institute-report-says-hong-kong-media-facing-intimidation-financial-crisis-political-pressure-and-tax-audits/ |
| 18 Jun 2026 | 橙新聞 (Orange News, HK): more than 60% of respondents back laws limiting teenagers' social-media use; 75% say platforms carry a lot of harmful content. UNVERIFIED: who ran the survey and the exact date (the date comes from the search summary). | https://www.orangenews.hk/hongkong/VMsSZ1d/ |

**AI sycophancy background (spring 2026):** UNU C3 blog "The Echo Chamber in Your Pocket", https://c3.unu.edu/blog/the-echo-chamber-in-your-pocket , mentions an MIT formal proof and a preregistered Stanford study in *Science* on sycophantic AI, both from spring 2026. Related: "Sycophantic AI decreases prosocial intentions and promotes dependence", https://www.researchgate.net/publication/403189902 . **UNVERIFIED:** the exact citations of the MIT and *Science* papers. Find them before citing.

---

## 5. Hong Kong and university-student context

- **Reuters Institute Digital News Report 2026, Hong Kong page.** https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/hong-kong ; HKFP coverage, 19 Jun 2026, https://hongkongfp.com/2026/06/19/reuters-institute-report-says-hong-kong-media-facing-intimidation-financial-crisis-political-pressure-and-tax-audits/ ; CUHK local partner page, https://ccpos.com.cuhk.edu.hk/reuters-institute-digital-news-report-hong-kong/
  - **Summary:** Written by Alex Zhi-Xiong Koo, Francis Lee and Hsuan-Ting Chen (CUHK), from a survey of 2,004 HK residents. Weekly offline reach: TVB News 55%, Now/ViuTV 24%, RTHK 19%, Lion Rock Daily 7%. Online: TVB Online 34%, HK01 33%, then Yahoo; SCMP 8%. The report also notes growing self-censorship among journalists. **UNVERIFIED:** social-media-for-news shares and figures by age. I could not open the page.
  - **Relevance:** The authoritative baseline on HK news habits. Pull the under-35 data and the platform list from the page.
- **DNR 2025, Hong Kong (CUHK C-Centre).** https://ccpos.com.cuhk.edu.hk/digital-news-report-2025-hong-kong/ ; https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2025/hong-kong
  - **Summary:** 86% get news online. TV is still slightly ahead of social media. Facebook and YouTube are the main social platforms for news. RTHK is the most trusted brand.
- **Digital 2026: Hong Kong (DataReportal), as summarized by MORE Digital, 5 Mar 2026.** https://moredigital.com.hk/2026/03/05/hong-kong-social-media-2026/ ; full report link given there: https://datareportal.com/reports/digital-2026-hong-kong
  - **Summary:**
    - 6.24m active social-media users (84.4% of the population), on 6.6 platforms each, about 10h49m a week.
    - Top platforms: WhatsApp, Facebook, Instagram, TikTok, WeChat. Xiaohongshu is 6th; Threads rose to 8th with 24.8% (above X).
    - MORE Digital estimates 1.55–1.7m Xiaohongshu users; the report itself does not give a figure.
- **Survey of 709 HK students (遵理潮指數, the "Tutors Index"), Jun 2023.** https://www.media-outreach.com/news/hong-kong/2023/07/31/236833/ ; HK01: https://www.hk01.com/%E7%A0%94%E6%95%B8%E6%89%80/925417/ ; Sing Tao: https://stheadline.com/society/3258952/
  - **Summary:**
    - Platform use: Instagram 93%, Facebook 48%, Xiaohongshu 33%, TikTok 19%.
    - More than half have stopped using Facebook (94% used it in 2013).
    - 46% had posted nothing in the past month; mostly they browse.
  - **Relevance:** Shows HK students live on recommendation-driven feeds (IG, 小红书). The data is from 2023, so it needs updating, which our own survey could do.
- **Mainland students in HK and "two echo chambers".** SCMP letter "Making Hong Kong home for mainland Chinese students a work in progress", https://www.scmp.com/opinion/letters/article/3353628/making-hong-kong-home-mainland-chinese-students-work-progress . **UNVERIFIED:** the date (likely 2026, judging by the article ID) and the author.
  - **Summary:** Says mainland students rely on Xiaohongshu and WeChat, local students on WhatsApp, IG, Facebook and YouTube. It describes this as "two echo chambers" that deepen segregation.
  - **Relevance:** Direct support for a "dual information environment" angle at HKU. It is an opinion letter, not data.
- **Xiaohongshu in Hong Kong.**
  - HKFP, 9 Jun 2025: Xiaohongshu sets up a Hong Kong office. https://hongkongfp.com/2025/06/09/social-media-e-commerce-platform-xiaohongshu-or-rednote-in-english-sets-up-office-in-hong-kong/
  - Wisers, "XiaoHongShu Hong Kong Report 2025": https://www.wisers.com/blog/58346/xiaohongshu-hong-kong-report-2025/
  - Marketing-Interactive: 39% of HK users research brands on Xiaohongshu. https://www.marketing-interactive.com/survey-39-hk-users-research-brands-or-products-on-xhs
  - 遠見 (Global Views): "當臉書在香港不再流行，「小紅書治港」盛行中" ("As Facebook fades in HK, Xiaohongshu takes over"). https://www.gvm.com.tw/article/121448
- **Mainland studies of university students and cocoons.** Example: Hans Publishers paper "智能算法推荐背景下信息茧房现象对大学生的负面影响" ("Negative effects of the information-cocoon phenomenon on university students under intelligent algorithmic recommendation"), https://www.hanspub.org/journal/paperinformation?paperid=70107 . This is a low-tier journal, and I found no comparable HK study (search budget exhausted).

---

## 6. Synthesis: most promising angles for an original research question (~300 words)

The strongest opening is a **gap between mandate and evidence**. China has required an "off switch" and tag management since March 2022 (Art. 17). The Nov 2024 Qinglang campaign made 信息茧房 an explicit target. By May 2025, CAC was presenting named features as the result: Kuaishou's "一键破茧" (20 May 2025), Douyin's 使用管理助手/内容偏好, Xiaohongshu's 内容偏好调节 and 探索更多. Almost all public evidence about these features is either **platform self-description**, such as Douyin's "100+ objectives", or **self-reported perception surveys**. The Shenzhen University report (Nov 2025) says about 78% of users feel their feeds are diverse. Then on **17 Sep 2026**, a People's Daily Online theory piece claimed the opposite: the features are buried, rarely used, and the feed "narrows back" soon after use. Nobody seems to have measured this. The EU shows the same pattern: Dutch courts (Oct 2025 to Jan 2026) and EDRi's YouTube complaint (Mar 2026) called non-persistent or friction-heavy opt-outs "dark patterns", and Australia (8 Sep 2026) and New York (28 Jul 2026) are now writing opt-out and default rules of their own.

**Candidate questions (narrow, local, feasible in one semester):**
1. **Audit (strongest):** "Does Xiaohongshu's 内容偏好调节 or 探索更多 (or Kuaishou's 一键破茧) measurably diversify the feed of a new HK-registered account, and how long does the effect last?" Method: sock-puppet accounts. Log the categories of the first N posts, use the feature, then re-log after 1, 3 and 7 days. Measure with Shannon entropy or category counts. This directly tests the 17 Sep 2026 "narrow-back" claim.
2. **Discoverability or friction:** Count the taps needed to reach the anti-cocoon or non-personalized setting on Xiaohongshu, Douyin, Instagram ("Your Algorithm") and YouTube. Compare with the EU "dark pattern" standard.
3. **Awareness survey at HKU:** What share of HKU students (local vs mainland) know these features exist, and have used them? How does perceived diversity compare with measured diversity? This tests the "usage is very low" claim and the "two echo chambers" claim at our own university.

Angle 1 plus a small version of angle 3 gives a timely, original and data-driven project that fits COMP1110's data-science focus.

---

## Gaps and things to check before citing
- Open every URL above. I could not read any page in full because of proxy blocks.
- Find the author and data basis of the 17 Sep 2026 People's Daily Online piece.
- Get DNR 2026 Hong Kong figures on social media for news, by age.
- Look for any quantitative uptake data for the Chinese 破茧 features or the EU Art. 38 options. None was found.
- Confirm the date and author of the SCMP letter on mainland students.
- Search further for HK surveys from 2025–2026 (HKFYG, HKU POP / PORI, CUHK) on youth information diets. My search budget ran out before I could do this.
