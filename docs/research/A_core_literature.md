# Literature review A: core empirical and conceptual work on filter bubbles, echo chambers and information cocoons (信息茧房)

Prepared for HKU COMP1110 group project. Compiled 2026-09-27.

## How the sources were checked (please read)

- Every item below showed up in live web-search results, with its title, venue and URL/DOI visible in the results. The summaries come from the abstract or snippet text shown there.
- In this environment the direct page fetcher (WebFetch) was blocked for most academic domains (pnas.org, science.org, dl.acm.org, arxiv.org, sciencedirect, PMC, crossref), so I could not open full texts. Before quoting a number in the report, open the link and check it.
- Items marked **UNVERIFIED** (or with an UNVERIFIED field) have a detail I could not confirm, usually the author list. The source itself was still seen.
- Numbers in brackets like [A1] are IDs for cross-referencing inside the project.

---

## 1. Foundational concepts

### [A1] Pariser, E. (2011). *The Filter Bubble: What the Internet Is Hiding from You*. New York: Penguin Press.
- URL: https://www.penguinrandomhouse.com/books/309214/the-filter-bubble-by-eli-pariser/ (review: https://escholarship.org/uc/item/8w7105jp)
- Summary: This non-academic book coined the term "filter bubble". Pariser points to events such as Google personalising search results in 2009 and argues that personalisation algorithms quietly give each user a unique "information universe" that is invisible to them and that they did not choose. The book offers anecdotes and argument, not systematic data.
- Use in our project: Gives the original definition to open the introduction. Its three claims (the bubble is invisible, it is not chosen, and each person is alone in it) can become testable questions for our own data.

### [A2] Sunstein, C. R. (2006). *Infotopia: How Many Minds Produce Knowledge*. Oxford University Press. ISBN 9780195189285.
- URL: https://global.oup.com/academic/product/infotopia-9780195189285 ; https://academic.oup.com/book/50393
- Summary: This book is the source of the term "information cocoons", which Sunstein defines as "communication universes in which we hear only what we choose and only what comforts us and pleases us". It is a conceptual and legal-theory book about how groups pool information and when group deliberation fails (e.g., Columbia shuttle, Enron). In Sunstein's version, the cocoon is driven by **user choice**, not algorithms.
- Use in our project: The Chinese term 信息茧房 translates this concept, so cite it when defining terms. It also sets up the "self-selection vs algorithm" distinction that our project can test.

### [A3] Sunstein, C. R. (2017). *#Republic: Divided Democracy in the Age of Social Media*. Princeton University Press. DOI: 10.1515/9781400884711
- URL: https://www.degruyterbrill.com/document/doi/10.1515/9781400884711/html
- Summary: This book updates Sunstein's earlier *Republic.com* for the social-media era. It argues that personalised "Daily Me" feeds and group polarisation threaten democratic deliberation, and it calls for exposure to unchosen and shared experiences ("architecture of serendipity").
- Use in our project: The "architecture of serendipity" idea can justify any design intervention we propose, such as a feature that deliberately injects unexpected content.

---

## 2. Landmark empirical studies (mostly political news, US-centred)

### [A4] Bakshy, E., Messing, S., & Adamic, L. A. (2015). Exposure to ideologically diverse news and opinion on Facebook. *Science*, 348(6239), 1130–1132.
- DOI: https://doi.org/10.1126/science.aaa1160
- Summary: Facebook researchers used de-identified data on 10.1 million US users who self-reported their ideology. They split exposure to "cross-cutting" news into three stages: what friends share, what the News Feed ranking shows, and what users click. Algorithmic ranking cut cross-cutting exposure by roughly 15% (in the paper's terms), but users' own choices (friend networks and clicks) reduced it more than the algorithm did.
- Use in our project: Its **three-stage funnel (potential exposure → exposure → selection)** is a clean framework we can copy for any platform, including a Douyin/Xiaohongshu feed. Critics note it was written by Facebook's own researchers.

### [A5] Flaxman, S., Goel, S., & Rao, J. M. (2016). Filter bubbles, echo chambers, and online news consumption. *Public Opinion Quarterly*, 80(S1), 298–320.
- URL: https://academic.oup.com/poq/article/80/S1/298/2223402 (preprint: https://5harad.com/papers/bubbles.pdf)
- Summary: The authors analysed web-browsing histories of 50,000 US users who regularly read news. They found that news reached through social media and search engines is linked to **greater** ideological distance between individuals. The same channels are also linked to **more** exposure to the reader's less-preferred side. So segregation and diversity rise together.
- Use in our project: Measuring ideological or topical "slant" from **browsing or viewing logs** is a method we can borrow on a small scale, for example students exporting their own watch history. The paradoxical result is a good talking point.

### [A6] Cinelli, M., De Francisci Morales, G., Galeazzi, A., Quattrociocchi, W., & Starnini, M. (2021). The echo chamber effect on social media. *PNAS*, 118(9), e2023301118.
- DOI: https://doi.org/10.1073/pnas.2023301118
- Summary: The authors compared more than 100 million pieces of content on controversial topics (gun control, vaccination, abortion) across Gab, Facebook, Reddit and Twitter. They measured echo chambers with two ingredients: homophily in the interaction network, and bias in how information spreads toward like-minded peers. Homophilic clusters dominate on Facebook and Twitter. The paper also reports weaker segregation on Reddit and Gab and attributes the difference partly to feed algorithms; that part comes from my prior knowledge of the paper, not the search snippet, so check it.
- Use in our project: The **two-ingredient operationalisation** (network homophily plus diffusion bias) is a ready-made metric. The cross-platform comparison design also fits a "compare apps" project.

### [A7] Huszár, F., Ktena, S. I., O'Brien, C., Belli, L., Schlaikjer, A., & Hardt, M. (2022). Algorithmic amplification of politics on Twitter. *PNAS*, 119(1), e2025334119.
- DOI: https://doi.org/10.1073/pnas.2025334119
- Summary: Twitter ran a long-term randomised experiment in which a control group kept a reverse-chronological timeline. The authors used it to measure how much the ranking algorithm amplified tweets from elected politicians in seven countries and from US news outlets. In six of seven countries the mainstream political right was amplified more than the left. However, far-left and far-right groups were **not** amplified more than moderate ones.
- Use in our project: It defines an **"amplification ratio"** (algorithmic reach divided by chronological reach), which is easy to explain in a COMP1110 context. It shows why a no-algorithm baseline is essential.

### [A8] Guess, A. M., Malhotra, N., Pan, J., Barberá, P., Allcott, H., … Tucker, J. A. (2023). How do social media feed algorithms affect attitudes and behavior in an election campaign? *Science*, 381(6656), 398–404.
- DOI: https://doi.org/10.1126/science.abp9364
- Summary: This is part of the US 2020 Facebook and Instagram Election Study. Consenting users were randomly moved from the algorithmic feed to a reverse-chronological feed for about three months. They spent much less time on the platforms and saw more political and untrustworthy content. However, polarisation, political knowledge and attitudes showed **no significant change**. The authors conclude that "algorithms shape what people see but not what they believe". *Science* later published an eLetter and an erratum debating whether Meta's changes to its algorithm during the study weakened it (https://www.eurekalert.org/news-releases/1058833 ; https://www.science.org/doi/10.1126/science.adu8261).
- Use in our project: This is the gold-standard causal design. The feed-swap idea can be copied at student scale, for example a one-week "chronological / following-only feed" self-experiment. The eLetter debate shows that platform-controlled research has limits.

### [A9] Nyhan, B., Settle, J., Thorson, E., Wojcieszak, M., Barberá, P., Chen, A. Y., … Tucker, J. A. (2023). Like-minded sources on Facebook are prevalent but not polarizing. *Nature*, 620(7972), 137–144.
- DOI: https://doi.org/10.1038/s41586-023-06297-w
- Summary: Across all active US adult Facebook users in 2020, most content came from like-minded sources, but political news was only a small share of it. A field experiment with 23,377 users cut like-minded-source exposure by about one-third. This raised cross-cutting exposure and reduced uncivil content, but had **no measurable effect** on eight pre-registered attitudes, including affective polarisation.
- Use in our project: It is evidence that **most of what people see is not political**. That supports a project on lifestyle and entertainment bubbles. The "reduce like-minded content by one-third" design is also an intervention template.

### [A10] González-Bailón, S., Lazer, D., … Tucker, J. A. (2023). Asymmetric ideological segregation in exposure to political news on Facebook. *Science*, 381(6656), 392–398.
- DOI: https://doi.org/10.1126/science.ade7138
- Summary: This study used aggregated data on 208 million US Facebook users. It compared three things: all political news users *could* have seen, what they *did* see after algorithmic curation, and what they *engaged* with. Ideological segregation was high and rose along that funnel. It was asymmetric, with a large, homogeneously conservative corner where most misinformation sat. (Author list abbreviated; copy the full list from the Science page.)
- Use in our project: This is the same funnel logic as [A4] at population scale, and a clear diagram idea for our slides. It also shows that segregation can be measured at the level of **domains/URLs** rather than individuals.

### [A11] Hosseinmardi, H., Ghasemian, A., Rivera-Lanas, M., Horta Ribeiro, M., West, R., & Watts, D. J. (2024). Causally estimating the effect of YouTube's recommender system using counterfactual bots. *PNAS*, 121(8), e2313377121.
- DOI: https://doi.org/10.1073/pnas.2313377121 (preprint: https://arxiv.org/abs/2308.10398)
- Summary: Bots first replayed real users' watch histories and then followed **only** recommendations. The researchers then compared bot trajectories with what the real users actually watched next. Relying on recommendations alone led, on average, to **more moderate** content than users' own choices. This suggests user preference, not the algorithm, drives consumption of hyper-partisan content.
- Use in our project: The **"counterfactual bot" or sock-puppet** method is feasible for students. For example, we could create fresh accounts on Douyin/TikTok/Xiaohongshu, train them on a topic, then let them follow recommendations only.

### [A12] Haroon, M., Wojcieszak, M., Chhabra, A., Liu, X., Mohapatra, P., & Shafiq, Z. (2023). Auditing YouTube's recommendation system for ideologically congenial, extreme, and problematic recommendations. *PNAS*, 120(50), e2213020120.
- DOI: https://doi.org/10.1073/pnas.2213020120
- Summary: This audit used 100,000 sock-puppet accounts. YouTube recommended ideologically congenial content to partisan puppets, and deeper in the "up-next" trail a growing share came from extremist or conspiratorial channels, especially for right-leaning puppets. The paper sits in tension with [A11] and shows how method choices shape conclusions.
- Use in our project: The sock-puppet protocol is a model to follow (train, then record the recommendation trail at depth 1..N). Contrasting [A11] with [A12] is a good way to show the debate.

---

## 3. Reviews and the "do bubbles really exist?" debate

### [A13] Bruns, A. (2019). *Are Filter Bubbles Real?* Cambridge: Polity (Digital Futures series). ISBN 9781509536443.
- URL: https://www.wiley.com/en-us/Are+Filter+Bubbles+Real%3F-p-9781509536443 ; open version: https://eprints.qut.edu.au/131674/ ; LSE review: https://blogs.lse.ac.uk/lsereviewofbooks/2020/01/17/book-review-are-filter-bubbles-real-by-axel-bruns/
- Summary: This book-length critique argues that the influence of echo chambers and filter bubbles has been badly overstated as part of a "moral panic". Bruns says blaming algorithms distracts from deeper problems: hyperpartisanship, populism, and people who **do** see opposing views but reject them.
- Use in our project: It is the main sceptical voice for a balanced literature review. It also suggests our project should measure **how people react** to diverse content, not only whether they are exposed to it.

### [A14] Ross Arguedas, A., Robertson, C. T., Fletcher, R., & Nielsen, R. K. (2022). *Echo chambers, filter bubbles, and polarisation: a literature review*. Reuters Institute for the Study of Journalism / Royal Society.
- URL: https://reutersinstitute.politics.ox.ac.uk/echo-chambers-filter-bubbles-and-polarisation-literature-review ; PDF: https://reutersinstitute.politics.ox.ac.uk/sites/default/files/2022-01/Echo_Chambers_Filter_Bubbles_and_Polarisation_A_Literature_Review.pdf
- Summary: This is a policy-oriented review. It concludes that echo chambers are **much less widespread than commonly assumed**, with most people having fairly diverse news diets and only a minority of partisans in echo chambers. It finds **no support for the filter bubble hypothesis** (algorithms often *increase* diversity) and a mixed picture on polarisation. It notes that evidence outside the US is very limited.
- Use in our project: It is the best single citation for "the evidence is mixed". Its point that research is US-heavy directly supports our gap claim about Hong Kong and mainland China.

### [A15] Michiels, L., Leysen, J., Smets, A., & Goethals, B. (2022). What are filter bubbles really? A review of the conceptual and empirical work. *Adjunct Proceedings of the 30th ACM Conference on User Modeling, Adaptation and Personalization (UMAP '22 Adjunct)*, 274–279.
- DOI: https://doi.org/10.1145/3511047.3538028 ; PDF: https://adrem.uantwerpen.be/bibrem/pubs/bubbles.pdf
- Summary: The authors argue that contradictory findings come from the vagueness of Pariser's thesis. They propose a precise, testable definition: a filter bubble exists when a personalisation algorithm causes a **decrease in diversity** of what a user sees over time, compared to a non-personalised baseline. They then re-interpret previous empirical studies against that definition.
- Use in our project: **Adopt this definition as our operational definition.** It tells us exactly what to measure: diversity, over time, compared with a baseline, with the algorithm as the cause.

### [A16] Hartmann, D., et al. (2025). A systematic review of echo chamber research: comparative analysis of conceptualizations, operationalizations, and varying outcomes. *Journal of Computational Social Science*. **Authors UNVERIFIED** (the author names come from memory; the title, journal and URL were seen).
- URL: https://link.springer.com/article/10.1007/s42001-025-00381-z (preprint: https://arxiv.org/pdf/2407.06631)
- Summary: This review covers 129 studies. It finds that disagreement comes from measurement choices and from regional, political, cultural and platform biases. Homophily-based and computational social-science studies tend to **support** echo chambers, while exposure-based studies and those looking at the wider media environment tend to **challenge** them.
- Use in our project: It explains *why* studies disagree. We should state clearly which kind of measure (network vs exposure) we use.

### [A17] "Echo Chambers and Filter Bubbles Reconsidered: Unpacking Scholarly, Industrial, and Media Perspectives on Their Existence and Causes" (2026). Book chapter, Springer Nature (ISBN prefix 978-981-95-0880-8). **Authors and book title UNVERIFIED.**
- URL: https://link.springer.com/chapter/10.1007/978-981-95-0880-8_2
- Summary (from search snippet): This systematic review covers 391 peer-reviewed articles and 131 Google News articles. It finds that conclusions about whether echo chambers and filter bubbles exist depend strongly on the discipline, platform and method. Claims about their causes track methodological choices and the authors' institutional position (academic vs industry vs media).
- Use in our project: It is very recent (2026) evidence that the media narrative and the academic evidence differ. That is useful for a "public perception vs evidence" angle.

### [A18] "Filter Bubbles in Recommender Systems: Fact or Fallacy — A Systematic Review" (2023). arXiv:2307.01221. **Authors UNVERIFIED** (not seen in results).
- URL: https://arxiv.org/pdf/2307.01221
- Summary: This is a systematic review of filter-bubble research from the recommender-systems (computer science) side. It covers how bubbles are defined and measured and which mitigation techniques exist, such as diversity-aware re-ranking. (Summary based on the title only; I could not open the full text.)
- Use in our project: A CS-side counterpart to [A14]. Check its mitigation-technique taxonomy before proposing our own solution.

---

## 4. Beyond politics: entertainment, music, short video, consumption

### [A19] Nguyen, T. T., Hui, P.-M., Harper, F. M., Terveen, L., & Konstan, J. A. (2014). Exploring the filter bubble: the effect of using recommender systems on content diversity. *Proceedings of WWW '14*, 677–686.
- DOI: https://doi.org/10.1145/2566486.2568012
- Summary: This longitudinal study of MovieLens (movie recommendations) users measured the content diversity of movies consumed over time. Diversity narrowed slightly for everyone, but users who **followed** recommendations narrowed *less* than those who ignored them. (This finding is from my prior knowledge; the search snippet only confirmed the study's aim, so check the abstract.) It is one of the first non-political filter-bubble studies.
- Use in our project: Shows filter bubbles apply to **entertainment tastes**. Its "diversity over time, followers vs non-followers" design is simple to reproduce with personal viewing logs.

### [A20] Anderson, A., Maystre, L., Anderson, I., Mehrotra, R., & Lalmas, M. (2020). Algorithmic effects on the diversity of consumption on Spotify. *Proceedings of The Web Conference 2020 (WWW '20)*.
- DOI: https://doi.org/10.1145/3366423.3380281 ; Spotify page: https://research.atspotify.com/algorithmic-effects-on-the-diversity-of-consumption-on-spotify/
- Summary: This study of Spotify listening data found that algorithm-driven listening is associated with **lower** diversity. Users who become more diverse over time do so by moving toward **organic** (self-directed) listening. A randomised experiment showed that recommendations work best for low-diversity users. The paper frames the tension between short-term satisfaction and long-term diversity.
- Use in our project: The paper's embedding-based **"generalist–specialist" diversity score** is a metric worth borrowing (metric name from prior knowledge; check it). It is also direct evidence of a music or lifestyle bubble.

### [A21] Chaney, A. J. B., Stewart, B. M., & Engelhardt, B. E. (2018). How algorithmic confounding in recommendation systems increases homogeneity and decreases utility. *Proceedings of RecSys '18*, 224–232.
- DOI: https://doi.org/10.1145/3240323.3240370 ; preprint: https://arxiv.org/pdf/1710.11214
- Summary: Simulations show a feedback loop: recommenders are retrained on data produced by users who were already shown recommendations. Over time this **homogenises** user behaviour across users without making anyone better off.
- Use in our project: It explains the feedback loop mechanism in computing terms, which suits COMP1110. A small Python simulation of this loop could be a project deliverable.

### [A22] Li, N., Gao, C., Piao, J., Huang, X., Yue, A., Zhou, L., Liao, Q., & Li, Y. (2022). An exploratory study of information cocoon on short-form video platform. *Proceedings of CIKM '22*.
- DOI: https://doi.org/10.1145/3511808.3557548 ; PDF: https://fi.ee.tsinghua.edu.cn/~gaochen/papers/CIKM2022-FilterBubble.pdf
- Summary: A Tsinghua team with an industry partner analysed **one year of behavioural records of new users** on a top Chinese short-video platform. They measured how the diversity of each user's consumption, their "information cocoon", changed over time. They found consumption becoming more homogeneous and linked cocoons to both video content and how users interact with the algorithm.
- Use in our project: This is the closest large-scale study to "short video + Chinese platform + entertainment (non-political) content". Its cocoon metrics, such as category entropy over time, can be reused on our own data.

### [A23] Hou, L., Pan, X., Liu, K., Yang, Z., Liu, J., & Zhou, T. (2022/2023). Information cocoons in online navigation. *iScience* (online Dec 2022; Jan 2023 issue; volume and article number: check on the journal page).
- URL: https://www.cell.com/iscience/fulltext/S2589-0042(22)02166-6 ; PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC9840977/
- Summary: The authors analysed real recommendation networks (Science, PNAS and Amazon "related items"). They showed that similarity-based recommendation creates information cocoons that reduce how navigable the whole system is by **hundreds of times**. They give a formal definition of a cocoon and propose a more flexible recommendation strategy.
- Use in our project: A network-science definition of cocoons for **consumption (Amazon) and academic** content, not politics. The navigability metric is a novel alternative to diversity.

### [A24] Boeker, M., & Urman, A. (2022). An empirical investigation of personalization factors on TikTok. *Proceedings of the ACM Web Conference 2022 (WWW '22)*.
- DOI: https://doi.org/10.1145/3485447.3512102 ; preprint: https://arxiv.org/pdf/2201.12271
- Summary: A sock-puppet audit of TikTok's For You feed tested language, location, following, liking and watch time. All of these factors affected recommendations: following had the strongest influence, then liking, then video view rate (watch time).
- Use in our project: Directly relevant to Douyin, TikTok's sister app. It tells us **which user actions to manipulate** in an escape experiment, for example whether follow/unfollow or deliberate watch time is the strongest lever.

### [A25] Amnesty International (2023). *Driven into Darkness: How TikTok's 'For You' Feed Encourages Self-Harm and Suicidal Ideation* (POL 40/7350/2023). Follow-up (Oct 2025): *Dragged into the rabbit hole: new evidence of TikTok's risks to children's mental health* (France).
- URLs: https://www.amnesty.org/en/documents/pol40/7350/2023/en/ ; https://www.amnesty.org/en/latest/news/2025/10/tiktok-steering-children-towards-depressive-and-suicidal-content/
- Summary: These NGO reports (grey literature) used automated accounts posing as teenagers. Accounts that signalled interest in mental health were quickly pulled into "rabbit holes" of depressive and self-harm content. The 2025 follow-up says this was still happening.
- Use in our project: Evidence that **non-political "wellbeing" bubbles** harm young people. The method is simple and replicable, but cite it as advocacy research, not peer-reviewed.

---

## 5. Users trying to escape: agency, controls and literacy

### [A26] Sheng, M., & Zhang, P. (2024). "How I Form and Escape Information Cocoons": An interview study of users on short video apps. In *iConference 2024 Proceedings*, LNCS 14596, Springer.
- DOI: https://doi.org/10.1007/978-3-031-57850-2_10
- Summary: The authors ran semi-structured interviews with 22 short-video app users and used thematic analysis. Users **form cocoons on purpose** (for comfort and relevance) but sometimes make deliberate efforts to escape them for diversity and serendipity. Their tactics include following or unfollowing accounts, "training" the algorithm, and exploring hashtags or categories. Cocoon phases differ by topic: exploration, filtering, opinion consolidation and self-verification.
- Use in our project: This is **the key paper for our "escape" angle**. The interview protocol and the list of escape tactics can become our survey items. Its small sample (n=22) leaves room for a quantitative follow-up with HKU students.

### [A27] Mozilla Foundation (Ricks, B., & McCrosky, J.) (2022). *Does This Button Work? Investigating YouTube's Ineffective User Controls*. **Author names UNVERIFIED** (the report itself was seen).
- URL: https://www.mozillafoundation.org/en/research/library/user-controls/
- Summary: This crowdsourced study used about 20,000 volunteers running the RegretsReporter browser extension. "Not interested" prevented only about 11% of unwanted recommendations, and even "Don't recommend channel" prevented only about 43%. A companion survey found users confused and frustrated by the controls.
- Use in our project: It gives **effect sizes for escape tools**. We could test whether Douyin's or Xiaohongshu's "不感兴趣" button, or the new "content preference adjustment" features, actually work.

### [A28] Swart, J. (2021). Experiencing algorithms: How young people understand, feel about, and engage with algorithmic news selection on social media. *Social Media + Society*, 7(2).
- DOI: https://doi.org/10.1177/20563051211008828
- Summary: In-depth interviews with 22 Dutch young people aged 16–26. Their sense-making about algorithms was triggered by expectation violations and personalisation cues. Knowing about algorithms did **not** automatically lead them to act against algorithmic decisions.
- Use in our project: It supports a "knowledge–action gap" hypothesis for students: awareness does not equal escape. That is testable with a survey.

### [A29] Jylhä, V., Hirvonen, N., & Haider, J. (2025). Algorithmic recommendations in the everyday life of young people: imaginaries of agency and resources. *Information, Communication & Society*.
- DOI: https://doi.org/10.1080/1369118X.2025.2470227 ; open PDF: https://www.diva-portal.org/smash/get/diva2:1940382/FULLTEXT01.pdf
- Summary: Thematic interviews with 20 young Finns, analysed with Giddens's concept of resources. Recommender systems limit young people's agency, for example in self-expression and in control over their data. Yet young people still find ways to use the systems for their own ends.
- Use in our project: A recent theoretical frame ("agency" and "resources") for interpreting student escape behaviour.

### [A30] Blakston, Chambers, & Notley (2025). Young people, algorithms and news: exploring the relationship between algorithmic literacy and news literacy. *Journal of Youth Studies*. **First names UNVERIFIED.**
- DOI: https://doi.org/10.1080/13676261.2025.2571491
- Summary: A survey of Australians aged 12–16 looked at awareness of algorithms in news and at which demographic and media habits predict it. It found a link between algorithmic literacy and news literacy and recommends teaching both together in schools.
- Use in our project: Offers **algorithmic-literacy survey measures** we could adapt for university students.

### [A31] Kim, D. W., Buntain, C., & Ciampaglia, G. L. (2026). Understanding the gap between stated and revealed preferences in news curation: A study of young adult social media users. arXiv:2604.11517 (April 2026 preprint).
- URL: https://arxiv.org/abs/2604.11517
- Summary: A mixed-methods study (surveys, interviews and a feed-curation task) with young adults. Participants often engaged with low-quality content they did not endorse. When asked to curate an "ideal" feed, they put accuracy and diversity first. This reveals a gap between **stated** and **revealed** preferences.
- Use in our project: A very recent study on **young adults**. The feed-curation task ("design your ideal feed") is a cheap, engaging activity we can run with classmates.

### [A32] He, Y., Tang, Z., & Chen, H. (2026). Content fuzzing for escaping information cocoons on digital social media. *Findings of ACL 2026*. arXiv:2604.05461.
- URL: https://aclanthology.org/2026.findings-acl.547/ ; code: https://github.com/EYH0602/ContentFuzz
- Summary: This paper takes the **creator's** perspective. ContentFuzz uses an LLM to rewrite posts so their meaning is kept but machine stance classifiers label them differently. That lets content cross affinity clusters. It was tested on four stance detectors, three datasets and two languages.
- Use in our project: A 2026 technical example of "escaping" from the supply side. It also raises an ethical question (is this manipulation?) that is worth discussing.

---

## 6. Chinese platforms and Chinese-language scholarship (信息茧房)

### [A33] 朱红涛, 李姝熹 (Zhu Hongtao & Li Shuxi) (2021). 信息茧房研究综述 [A review of information cocoon research]. 《图书情报工作》 *Library and Information Service*, 65(18), 141–149.
- DOI: https://doi.org/10.13266/j.issn.0252-3116.2021.18.015 ; URL: https://www.lis.ac.cn/CN/10.13266/j.issn.0252-3116.2021.18.015 ; ChinaXiv: https://chinaxiv.org/abs/202304.00484
- Summary: A content-analysis review of Chinese and international work along five dimensions: how the concept evolved, empirical evidence, effects, formation mechanisms, and countermeasures ("breaking the cocoon").
- Use in our project: A good starting map of the Chinese literature. Its five-dimension structure could organise our own review section.

### [A34] 彭兰 (Peng Lan) (2020). 导致信息茧房的多重因素及"破茧"路径 [Multiple factors leading to information cocoons and paths to "breaking the cocoon"]. 《新闻界》 *Journalism and Mass Communication*, 2020(1), 30–38.
- URL: http://new.oversea.cnki.net/kcms/detail/detail.aspx?filename=NEWS202001005&dbcode=CJFQ&dbname=CJFDTEMP&v=
- Summary: A highly cited conceptual paper. It argues that cocoons are an old phenomenon (selective exposure), now reinforced by social networks, platforms and algorithms together. Breaking them needs better algorithms and platforms, a better supply of information, **and** better individual media literacy.
- Use in our project: The standard Chinese framing of "multiple causes, multiple exits". It is useful for structuring the solutions section.

### [A35] 杨洸 (Yang Guang) et al. (2020). 新闻算法推荐的信息可见性、用户主动性与信息茧房效应：算法与用户互动的视角 [Information visibility, user initiative and the information-cocoon effect of algorithmic news recommendation]. 《新闻大学》 *Journalism Research*, 2020(2). **Co-author(s) UNVERIFIED** (only Yang Guang was confirmed).
- URL: http://dianda.cqvip.com/Qikan/Article/Detail?id=7101655025&from=Qikan_Article_Detail
- Summary: A questionnaire survey of **Jinri Toutiao (今日头条)** users. Algorithmic recommendation did **not** produce a cocoon effect. Instead it widened the range of news users encountered, and users and the algorithm "respond to and develop with each other".
- Use in our project: Chinese evidence against the cocoon hypothesis on the platform most associated with it in public debate. Pairs well with [A14].

### [A36] 施颖婕, 桂勇, 黄荣贵, 郑雯 (Shi Yingjie, Gui Yong, Huang Ronggui & Zheng Wen) (2022). 网络媒介"茧房效应"的类型化、机制及其影响——基于"中国大学生社会心态调查（2020）"的中介分析 [Typology, mechanisms and effects of the "cocoon effect" of online media: a mediation analysis based on the 2020 Chinese University Students' Social Attitudes Survey]. 《新闻与传播研究》 *Journalism & Communication*, 2022(5).
- Evidence URLs: https://www.jwview.com/jingwei/html/01-16/522779.shtml (interview with Zheng Wen); award list: http://xinwen.cass.cn/bsdt/202402/t20240228_5735484.shtml. **The direct journal-article URL was not found, so locate it on CNKI.**
- Summary: This study uses a **national survey of Chinese university students** to compare ten kinds of online media. Cocoons are **not** an automatic result of recommendation algorithms. What matters is transmission structure (horizontal vs vertical) and whether user connections are open or closed. Acquaintance-based social media (WeChat) tends to "build cocoons", public-discussion media (Weibo) tends to "break" them, and vertical-transmission media such as short-video apps did neither.
- Use in our project: **The most relevant single Chinese source for us: university students, many platforms, and a counter-intuitive finding about short video.** We could replicate a mini version with HKU students.

### [A37] "News Diversity Under Algorithms: The Effects of Pre-Selected and Self-Selected Personalization on Chinese TikTok (Douyin)" (2025). *Digital Journalism*, 13(7), 1190–1208. **Authors UNVERIFIED** (the paper appears on Li Jinhui's publications page, https://lijinhuihust.wixsite.com/lijh/publications, but the full author list was not seen).
- DOI: https://doi.org/10.1080/21670811.2025.2450312
- Summary: This study ran **agent-based testing** (virtual agents imitating users) on Douyin. Algorithmic personalised news was **more diverse** in categories than random chance, and algorithmic decisions did more than human choices to promote diverse topics. The authors also modelled whether users can reach a more balanced diet by widening their interests and engaging with unmatched content. Chinese media covered it as "短视频算法显著提升推荐内容多样性" (e.g., https://www.sohu.com/a/853045612_123753).
- Use in our project: A Douyin-specific **agent or sock-puppet method** we can copy. The "engage with unmatched content" simulation is essentially an **escape strategy test**.

### [A38] 渠润泽, 徐敬宏 (Qu Runze & Xu Jinghong) (2026). 解构"信息茧房"：算法、用户偏好与信息生态的动态交互 [Deconstructing information cocoons: dynamic interaction of algorithms, user preferences and information ecology]. 《新闻与传播研究》 *Journalism & Communication*, 2026(3).
- PDF: https://sjc.bnu.edu.cn/docs/2026-05/a83991a68bec4b19a7a357bf5bb6138b.pdf
- Summary: A survey analysed with SEM plus fsQCA (fuzzy-set qualitative comparative analysis). Perceived algorithmic personalisation and cognitive biases reinforce each other and deepen cocoons. **Perceived algorithmic transparency** reduces cocoons directly, and also indirectly by encouraging active information seeking and more diverse information and social-network interaction.
- Use in our project: A very recent Chinese study with **ready-made survey constructs**: perceived personalisation, perceived transparency, active seeking, information diversity, and social-network diversity. It points to transparency as a design lever.

### [A39] 算法推荐与"信息茧房"的再审视——基于抖音、小红书用户使用行为的实证调查 [Re-examining algorithmic recommendation and information cocoons: an empirical investigation of Douyin and Xiaohongshu user behaviour]. 《数字传播与新媒体学刊》. **Authors and year UNVERIFIED.**
- URL: https://onlinejandl.com/index.php/COMU/article/view/213
- Summary: A mixed-methods study combining interviews with 20 users and 7-day usage logs. Exposure diversity did **not** fall for everyone, and some users discovered new interests through the algorithm. Cocoons were more common among **passive, low-intervention** users. Douyin's strong-recommendation model and Xiaohongshu's search-plus-recommendation model showed different cocoon strength. Active actions ("不感兴趣", searching) noticeably reduced homogeneity.
- Use in our project: Very close to our likely design: **Douyin vs Xiaohongshu, usage logs, active intervention**. Its 7-day log method is feasible for a student group.

### [A40] Tsinghua CIKM study [A22] is also a Chinese-platform study; see above.

### [A41] Studies of Chinese college students and older adults on short-video cocoons (English-language)
- (a) "The Research on Chinese College Students' View on the Information Cocoons on Douyin". Atlantis Press conference proceedings. **Authors and year UNVERIFIED.** PDF: https://www.atlantis-press.com/article/125976917.pdf. A survey in which 97.92% of respondents knew Douyin personalises by algorithm and 83.33% believed algorithms can trap people in an information cocoon. *Use:* baseline perception numbers to compare with HKU students; the source is low-tier, so cite it cautiously.
- (b) "The Relationship Between Social Media Information Sharing Characteristics and Problem Behaviors Among Chinese College Students Under Recommendation Algorithms". *Psychology Research and Behavior Management* (2024). **Authors UNVERIFIED.** DOI: https://doi.org/10.2147/PRBM.S466398. An online survey of **34,752 Chinese college students** on recommendation algorithms, information sharing and behaviour problems. *Use:* shows large student samples are possible, and links bubbles to wellbeing rather than politics.
- (c) "Information Cocoons on Short Video Platforms and Its Influence on Depression Among the Elderly: A Moderated Mediation Model". *Psychology Research and Behavior Management* (2023). **Authors UNVERIFIED.** DOI: https://doi.org/10.2147/PRBM.S415832. A survey of 400 older Chinese adults: information cocoons predicted depression through loneliness, and family emotional support moderated the effect. *Use:* an existing **"information cocoon" self-report scale** that could be adapted for students.
- (d) "The Dark Side of Recommendation Algorithms in Chinese Mass Short Video Apps: Effect of Perceived Over-Recommendation on Users' Cognitive Dissonance and Discontinuance Intention". *International Journal of Human–Computer Interaction* (2024). **Authors UNVERIFIED.** DOI: https://doi.org/10.1080/10447318.2024.2383038. 322 survey responses from Douyin-type app users: perceived "information narrowing", redundancy, overload and privacy invasion raised cognitive dissonance, which led to intention to quit. *Use:* "information narrowing" as a measurable construct; quitting as an extreme form of escape.
- (e) "Adolescents' Algorithmic Resistance to Short Video APP's Recommendation: The Dual Mediating Role of Resistance Willingness and Resistance Intention". *Frontiers in Psychology* (2022). **Authors UNVERIFIED.** DOI: https://doi.org/10.3389/fpsyg.2022.859597. A survey on Chinese adolescents' "algorithmic resistance". *Use:* a scale for **resistance/escape intention**.

### [A42] 国内信息茧房研究的热点与趋势 [Hotspots and trends of information-cocoon research in China] (2025). **Authors and journal UNVERIFIED** (DOI prefix suggests a Chinese science-communication journal).
- DOI: https://doi.org/10.19483/j.cnki.11-4653/n.2025.04.006 ; URL: http://www.scimedia.cn/cn/article/doi/10.19483/j.cnki.11-4653/n.2025.04.006
- Summary: A CiteSpace bibliometric analysis of Chinese cocoon research. It finds the field centres on "technology" and "people", with a narrow perspective and little theory built for the Chinese context. It calls for moving beyond technological determinism.
- Use in our project: A citable statement that **Chinese research is itself calling for user-centred, non-deterministic work**. That is exactly our gap.

---

## 7. Other recent items (2025–2026), including Aug–Sep 2026

- **[A43] Brown, É. (2026). Recommended selves: authenticity and algorithmic filtering.** *Journal of the American Philosophical Association*, 12(1), 15–34. DOI: https://doi.org/10.1017/apa.2025.10009 ; arXiv posted **August 2026**: https://arxiv.org/abs/2608.14602. A philosophical argument: recommenders frustrate users' "second-order desires" (what they *want to want*) because they rely on thin behavioural signals, but they can also prompt self-understanding. The paper argues for controllable, explainable recommenders. *Use:* gives a normative reason why letting students steer their own feed matters, i.e., why escaping is worthwhile.
- **[A44] "Do Generative Recommenders Deepen the Information Cocoon? A Closed-Loop Simulation with LLM-powered User Simulators" (June 2026).** arXiv:2606.17707, https://arxiv.org/abs/2606.17707. **Authors UNVERIFIED.** Search snippet: generative (LLM-based) recommenders were generally *less* prone to exposure-level cocoons than traditional baselines, but cocoon severity depended on tokenisation and model scale. *Use:* shows the next generation of recommenders is an open question, and simulations with LLM "users" are a cheap way in.
- **[A45] "Understanding the Information Cocoon: A Multidimensional Assessment and Analysis of News Recommendation Systems" (Sept 2025).** arXiv:2509.11139, https://arxiv.org/abs/2509.11139. **Authors UNVERIFIED.** It distinguishes a "selection cocoon" (driven by the user) from a "recommendation cocoon" (driven by the algorithm) and defines a cocoon as a loss of information diversity. *Use:* this vocabulary is useful for separating user choice from algorithm effect in our write-up.
- **[A46] "Breaking Information Cocoons: A Hyperbolic Framework for Balancing Exploration and Exploitation in Recommender Systems" (HERec).** arXiv:2411.13865, https://arxiv.org/abs/2411.13865. **Authors UNVERIFIED.** Reports about 11% higher diversity with a small gain in utility. *Use:* an example of an algorithmic (platform-side) fix.
- **[A47] Science eLetter and erratum on Guess et al. 2023** (published 2024–2025): https://www.eurekalert.org/news-releases/1058833 and https://www.science.org/doi/10.1126/science.adu8261. Critics argued that Meta changed its news-feed algorithm during the experiment, which weakens the study's conclusions. *Use:* shows the limits of research that depends on platform cooperation.
- **Grey literature and policy context (China, 2025–2026):** Tencent Research Institute's report 《算法破茧》 (https://tisi.org/32160/). In 2025, Chinese regulators ran a campaign on "algorithm problems", and platforms (Douyin, Xiaohongshu and others) launched "content preference adjustment" (内容偏好调节) features to help users break cocoons; see news coverage such as https://m.thepaper.cn/newsDetail_forward_30250322 and https://www.thecover.cn/news/bFnLy22llAeH90qSdq8Jkw== . *Use:* these new **user-facing escape features** have almost no independent evaluation yet, which is a timely gap to test.
- Note on Aug–Sep 2026: my searches turned up very few peer-reviewed empirical papers published specifically in Aug–Sep 2026. The one confirmed August 2026 item is the arXiv posting of Brown [A43]. A PressReader entry dated 2026-08-28 with a Chinese magazine feature on "算法生态" appeared (https://www.pressreader.com/china/media-5898/20260828/282136413312902), but I could not open it (**UNVERIFIED** content). The search budget ran out before I could check further, so a final manual search on Google Scholar with a "since 2026" filter is recommended.

---

## Synthesis: what is crowded vs where the gaps are (~300 words)

**Crowded areas.** Research on filter bubbles and echo chambers is dominated by **political news in the US**, mostly on Facebook, Twitter/X and YouTube [A4–A12]. The strongest evidence, including the 2023 Meta election experiments [A8–A10], counterfactual bots [A11] and the Twitter amplification experiment [A7], points to the same conclusion. Algorithms clearly shape *what people see*: segregation is real and asymmetric, and like-minded content is common. But the effects on *what people believe* are small, and user self-selection often matters more than the algorithm [A4, A11]. Reviews [A13–A17] agree that the classic "filter bubble" is overstated. They also say that results depend heavily on the definition and metric used. Michiels et al. [A15] give the cleanest testable definition: a decrease in diversity over time, caused by personalisation, compared with a non-personalised baseline.

**Under-studied areas (possible gaps for our project):**
1. **Non-political content.** Nyhan et al. [A9] show that political news is a small share of what people see, yet only a few studies look at entertainment, lifestyle or consumption bubbles: movies [A19], music [A20], short video [A22], and mental-health rabbit holes [A25]. Lifestyle cocoons (food, beauty, study tips, "Xiaohongshu aesthetics") are almost unmeasured.
2. **Chinese platforms.** Chinese scholarship is large but mostly conceptual or survey-based [A33–A35, A42]. The few behavioural or experimental studies of Douyin and Toutiao [A22, A35–A37, A39] give **mixed** results, sometimes finding that algorithms *increase* diversity. Xiaohongshu is barely studied, and Hong Kong users are absent altogether.
3. **Active escape.** Most studies treat users as passive. Only small qualitative studies [A26, A39] and Mozilla's control-button audit [A27] look at deliberate escape tactics. Nobody has evaluated the new "content preference adjustment" features that Chinese platforms launched in 2025.
4. **University students.** Youth studies focus on news literacy [A28–A31]. Shi et al. [A36] is the only multi-platform study of university students, and it uses 2020 data.

**Suggested niche:** a small, mixed-method study of **HKU students' non-political (lifestyle/entertainment) cocoons on Douyin/Xiaohongshu**. It could combine a survey (constructs from [A38, A41]) with a short sock-puppet or self-log experiment testing whether escape actions (following, "not interested", search, preference settings) measurably raise diversity (category entropy, per [A15, A22]).
