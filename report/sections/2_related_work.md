# 2 Related Work

<!-- D5 draft, Zhao Dingcheng, 2026-11-07. Every reference was checked against Crossref, arXiv or the publisher page; see report/ai_use_log.md. The list at the end will be merged into 9_references.md. -->

We group prior work into four lines. For each line we say what has been established and what is still missing. Section 2.5 states the gap this study addresses.

## 2.1 What an information cocoon is, and how it has been measured

The idea that personalised media can enclose people in a narrow set of views goes back to Sunstein's "information cocoons" (Sunstein, 2006, 2017) and Pariser's "filter bubble" (Pariser, 2011). The two terms are used loosely. Michiels et al. (2022) reviewed the conceptual and empirical literature, found that definitions often contradict one another, and proposed a testable one: a decrease in the diversity of what a user is recommended over time, caused by the choices of the user, the platform or other stakeholders.

Empirical studies have almost always measured diversity over **content categories**. On MovieLens, Nguyen et al. (2014) found that the content users consumed narrowed slightly over time, and that users who followed recommendations narrowed less than those who did not. On Kuaishou, Li et al. (2022) compared the category diversity of the videos that new users were shown with the videos they watched during their first year. Sukiennik et al. (2024) showed that narrowing also happens *inside* a broad interest, for example from sport to one club ("deep filter bubbles"). Anderson et al. (2020) linked algorithmic listening on Spotify to lower consumption diversity. Piao et al. (2023) explained the emergence of cocoons with a model in which similarity-based matching and positive or negative feedback interact.

*What is missing.* All of these measures treat a cocoon as concentration over topics or categories. They cannot tell a user who simply likes one topic from a user who, within that topic, keeps seeing one side of an argument. A user who watches many marriage videos may still see a balanced range of views; another user may watch few of them and see mostly one hostile narrative. Category measures score the first user as more "cocooned".

## 2.2 Viewpoint-level audits of platforms

A second line audits platforms at the level of stance or ideology, almost always on political or misinformation topics. Haroon et al. (2023) trained about 100,000 automated YouTube accounts on partisan content and found that "up-next" recommendations were mostly ideologically congenial, more so deeper into the trail for right-leaning accounts. Using counterfactual bots, Hosseinmardi et al. (2024) found that YouTube's sidebar "forgets" a partisan user's preference within about 30 videos once the user switches to moderate content. Tomlein et al. (2021) and Srba et al. (2023) showed that watching debunking videos can burst misinformation bubbles on YouTube, although search and recommendation respond differently. On TikTok, Pecher et al. (2026) audited polarising topics such as politics, climate change and vaccines, and found that the feed generally reinforced each account's existing stance.

*What is missing.* These audits treat the platform as a black box, so they cannot say whether a skew comes from what is available on the platform, from ranking that affects everyone, or from personalisation. They test few user strategies. They do not consider the everyday social issues that short-video users argue about, such as gender, marriage and appearance, and none studies Chinese platforms.

## 2.3 What user controls achieve

A third line asks whether users can steer their own feed. In a study of 22,722 YouTube users who donated data, Ricks and McCrosky (2022) found that "Not interested" prevented only about 11% of unwanted similar recommendations, and "Don't recommend channel" about 43%. Liu et al. (2024) found that "Not interested" removed on average 88% of homepage recommendations from the unwanted topic. On TikTok, Kaplan et al. (2026) found that "Not interested" was the most effective explicit signal, but that once accounts stopped using it, many feeds became dominated by the unwanted topic again. Vombatkere et al. (2024) proposed metrics for how much of a TikTok feed explores new content versus exploiting known interests. Recommender designs have also been proposed that let users ask for less of a category (Wang et al., 2022), or that counteract over-exposure inside the recommender itself (Gao et al., 2024).

*What is missing.* All of these controls, and the measures used to evaluate them, operate at the level of topics, channels or similar videos. They report how much unwanted content is removed, but not how much of the wanted topic is lost along with it. Nor do they ask whether a control changes the mix of viewpoints *within* a topic the user wants to keep, or whether the user could notice a viewpoint skew at all.

## 2.4 Simulation methods

The fourth line studies feedback loops in simulation. Theoretical models show that recommendation feedback can homogenise behaviour (Chaney et al., 2018), push user interests towards degenerate states (Jiang et al., 2019) and amplify preferences (Kalimeris et al., 2021). Dean et al. (2020) asked whether a user can make a given item recommended by changing their ratings ("reachability"). More recent work replaces rule-based users with LLM agents: Agent4Rec simulates users on movie data (Zhang et al., 2024); SimTok simulates filter bubbles on short-video data (Sukiennik et al., 2025, preprint); RecLoop compares generative and traditional recommenders in a closed loop (Yang et al., 2026, preprint). Feng et al. (2026) proposed Bubble Escape Potential, which compares how many categories are recommended to simulated users with positive and with negative behavioural tendencies.

*What is missing.* In the theoretical models, user behaviour and the effect of each action are set by hand. Agent-based simulations replace these assumptions with LLM behaviour that is hard to validate. Most simulations use movie, book or product data and recommenders that were not trained on a real platform's logs. Their outcome measures are again category diversity, and reachability concerns single items rather than "reduce one kind of content while keeping the rest of the topic".

## 2.5 The gap

Taken together, prior work measures cocoons over categories, audits viewpoints only on political topics and only from outside the platform, evaluates user controls at the topic level, and simulates feedback loops with hand-set or LLM-generated users. No study separates **viewpoint skew within an everyday issue** from **interest in that issue**, and then asks, on a recommender trained on real short-video logs, how the skew forms, whether a user can detect it, and what each available action costs in lost content. This study addresses that gap for opposing narratives, such as negative group labels, in gender and marriage videos on Kuaishou.

## References used in this section

Anderson, A., Maystre, L., Anderson, I., Mehrotra, R., & Lalmas, M. (2020). Algorithmic effects on the diversity of consumption on Spotify. In *Proceedings of The Web Conference 2020* (pp. 2155–2165). ACM. https://doi.org/10.1145/3366423.3380281

Chaney, A. J. B., Stewart, B. M., & Engelhardt, B. E. (2018). How algorithmic confounding in recommendation systems increases homogeneity and decreases utility. In *Proceedings of the 12th ACM Conference on Recommender Systems* (pp. 224–232). ACM. https://doi.org/10.1145/3240323.3240370

Dean, S., Rich, S., & Recht, B. (2020). Recommendations and user agency: The reachability of collaboratively-filtered information. In *Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency* (pp. 436–445). ACM. https://doi.org/10.1145/3351095.3372866

Feng, D., Xu, Q., Wang, Z., Hua, C., Yang, Z., & Huang, Q. (2026). Quantifying the potential to escape filter bubbles: A behavior-aware measure via contrastive simulation. *Proceedings of the AAAI Conference on Artificial Intelligence, 40*(17), 14729–14737. https://doi.org/10.1609/aaai.v40i17.38492

Gao, C., Wang, S., Li, S., Chen, J., He, X., Lei, W., Li, B., Zhang, Y., & Jiang, P. (2024). CIRS: Bursting filter bubbles by counterfactual interactive recommender system. *ACM Transactions on Information Systems, 42*(1), 1–27. https://doi.org/10.1145/3594871

Haroon, M., Wojcieszak, M., Chhabra, A., Liu, X., Mohapatra, P., & Shafiq, Z. (2023). Auditing YouTube's recommendation system for ideologically congenial, extreme, and problematic recommendations. *Proceedings of the National Academy of Sciences, 120*(50), Article e2213020120. https://doi.org/10.1073/pnas.2213020120

Hosseinmardi, H., Ghasemian, A., Rivera-Lanas, M., Horta Ribeiro, M., West, R., & Watts, D. J. (2024). Causally estimating the effect of YouTube's recommender system using counterfactual bots. *Proceedings of the National Academy of Sciences, 121*(8), Article e2313377121. https://doi.org/10.1073/pnas.2313377121

Jiang, R., Chiappa, S., Lattimore, T., György, A., & Kohli, P. (2019). Degenerate feedback loops in recommender systems. In *Proceedings of the 2019 AAAI/ACM Conference on AI, Ethics, and Society* (pp. 383–390). ACM. https://doi.org/10.1145/3306618.3314288

Kalimeris, D., Bhagat, S., Kalyanaraman, S., & Weinsberg, U. (2021). Preference amplification in recommender systems. In *Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining* (pp. 805–815). ACM. https://doi.org/10.1145/3447548.3467298

Kaplan, L., Patel, D., Gerzon, N., Mislove, A., & Sapiezynski, P. (2026). When 'For You' isn't for you: Measuring user agency in TikTok's algorithmic feed. *Proceedings of the International AAAI Conference on Web and Social Media, 20*(1), 1175–1189. https://doi.org/10.1609/icwsm.v20i1.42688

Li, N., Gao, C., Piao, J., Huang, X., Yue, A., Zhou, L., Liao, Q., & Li, Y. (2022). An exploratory study of information cocoon on short-form video platform. In *Proceedings of the 31st ACM International Conference on Information & Knowledge Management* (pp. 4178–4182). ACM. https://doi.org/10.1145/3511808.3557548

Liu, A., Wu, S., & Resnick, P. (2024). How to train your YouTube recommender to avoid unwanted videos. *Proceedings of the International AAAI Conference on Web and Social Media, 18*, 930–942. https://doi.org/10.1609/icwsm.v18i1.31363

Michiels, L., Leysen, J., Smets, A., & Goethals, B. (2022). What are filter bubbles really? A review of the conceptual and empirical work. In *Adjunct Proceedings of the 30th ACM Conference on User Modeling, Adaptation and Personalization* (pp. 274–279). ACM. https://doi.org/10.1145/3511047.3538028

Nguyen, T. T., Hui, P.-M., Harper, F. M., Terveen, L., & Konstan, J. A. (2014). Exploring the filter bubble: The effect of using recommender systems on content diversity. In *Proceedings of the 23rd International Conference on World Wide Web* (pp. 677–686). ACM. https://doi.org/10.1145/2566486.2568012

Pariser, E. (2011). *The filter bubble: What the Internet is hiding from you*. Penguin Press.

Pecher, B., Bindas, A., Jakubcik, J., Tuna, M., Tibensky, M., Liska, S., Sakalik, P., Suty, A., Mosnar, M., Hossner, F., & Srba, I. (2026). Algorithmic audit of personalisation drift in polarising topics on TikTok. In *Proceedings of the 34th ACM Conference on User Modeling, Adaptation and Personalization* (pp. 1–10). ACM. https://doi.org/10.1145/3774935.3806161

Piao, J., Liu, J., Zhang, F., Su, J., & Li, Y. (2023). Human–AI adaptive dynamics drives the emergence of information cocoons. *Nature Machine Intelligence, 5*(11), 1214–1224. https://doi.org/10.1038/s42256-023-00731-4

Ricks, B., & McCrosky, J. (2022). *Does this button work? Investigating YouTube's ineffective user controls*. Mozilla Foundation. https://assets.mofoprod.net/network/documents/Mozilla-Report-YouTube-User-Controls.pdf

Srba, I., Moro, R., Tomlein, M., Pecher, B., Simko, J., Stefancova, E., Kompan, M., Hrckova, A., Podrouzek, J., Gavornik, A., & Bielikova, M. (2023). Auditing YouTube's recommendation algorithm for misinformation filter bubbles. *ACM Transactions on Recommender Systems, 1*(1), 1–33. https://doi.org/10.1145/3568392

Sukiennik, N., Gao, C., & Li, N. (2024). Uncovering the deep filter bubble: Narrow exposure in short-video recommendation. In *Proceedings of the ACM Web Conference 2024* (pp. 4727–4735). ACM. https://doi.org/10.1145/3589334.3648159

Sukiennik, N., Wang, H., Zeng, Z., Gao, C., & Li, Y. (2025). *Simulating filter bubble on short-video recommender system with large language model agents* (arXiv:2504.08742). arXiv. https://arxiv.org/abs/2504.08742

Sunstein, C. R. (2006). *Infotopia: How many minds produce knowledge*. Oxford University Press.

Sunstein, C. R. (2017). *#Republic: Divided democracy in the age of social media*. Princeton University Press.

Tomlein, M., Pecher, B., Simko, J., Srba, I., Moro, R., Stefancova, E., Kompan, M., Hrckova, A., Podrouzek, J., & Bielikova, M. (2021). An audit of misinformation filter bubbles on YouTube: Bubble bursting and recent behavior changes. In *Proceedings of the 15th ACM Conference on Recommender Systems* (pp. 1–11). ACM. https://doi.org/10.1145/3460231.3474241

Vombatkere, K., Mousavi, S., Zannettou, S., Roesner, F., & Gummadi, K. P. (2024). TikTok and the art of personalization: Investigating exploration and exploitation on social media feeds. In *Proceedings of the ACM Web Conference 2024* (pp. 3789–3797). ACM. https://doi.org/10.1145/3589334.3645600

Wang, W., Feng, F., Nie, L., & Chua, T.-S. (2022). User-controllable recommendation against filter bubbles. In *Proceedings of the 45th International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 1251–1261). ACM. https://doi.org/10.1145/3477495.3532075

Yang, J., Sun, G., Zhang, M., Wang, L., Li, Y., Cui, H., Xin, X., & Ren, P. (2026). *Do generative recommenders deepen the information cocoon? A closed-loop simulation with LLM-powered user simulators* (arXiv:2606.17707). arXiv. https://arxiv.org/abs/2606.17707

Zhang, A., Chen, Y., Sheng, L., Wang, X., & Chua, T.-S. (2024). On generative agents in recommendation. In *Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 1807–1817). ACM. https://doi.org/10.1145/3626772.3657844
