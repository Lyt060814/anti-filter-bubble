# 1 Introduction

<!-- L6 draft, Li Yitong, 2026-11-07. Findings in the last paragraph will be finalised after Sections 4 and 5 are complete. -->

As university students, we spend a good part of each day on short-video feeds, and many of the videos are about issues our generation argues over: whether a partner who earns less is worth marrying, whether a bride price is a sign of respect or a transaction, whether staying in a stable job is wise or cowardly, what a "normal" body looks like. Watching such videos is not a problem in itself. The worry is subtler: a feed can keep showing us a topic we chose while, within that topic, tilting towards one kind of story, for example videos that describe a whole gender as greedy or untrustworthy. We would not notice, because we never see what other people are shown, and the buttons we can press, such as "not interested", may not do what we hope.

This worry has a name, the *information cocoon* (Sunstein, 2006) or *filter bubble* (Pariser, 2011), and Chinese regulators have taken it up: a 2024 campaign by the Cyberspace Administration of China listed "homogeneous recommendation that creates information cocoons" as a target, and in 2025 major short-video platforms launched features to "assess" and "break" a user's cocoon. Yet both the research literature and these features mostly measure cocoons as a narrowing of *topics* or *content categories* (Section 2). That conflates two different things. Watching a lot of marriage videos is an interest. Being shown, within those videos, mostly one hostile narrative is what the original idea of a cocoon was about.

This report studies the second kind of cocoon from the user's side. Our main question is:

> **On everyday social issues in short-video feeds, can recommendation push a user towards one opposing narrative while keeping the topic, can the user notice it, and what does it cost the user to get out?**

We break this into three research questions.

- **RQ1 (distribution).** Across the social issues that appear in users' feeds, how common are opposing narratives, and of what kinds?
- **RQ2 (formation and detection).** For a user who engages more with one narrative, how quickly does the within-issue mix tilt, compared with how their interest in the topic changes? How many videos would the user need to see to notice?
- **RQ3 (escape).** How far do the actions available to a user ("not interested", watching other content, deleting history, blocking, switching off personalisation) reduce the tilt, what do they cost in lost content, and how long does the effect last?

We answer these with three kinds of evidence, each labelled in the text: measurements on a large public log of a real Chinese short-video platform (Kuaishou's RecIF data, about 160,000 users and 75 million impressions); experiments on OneRec, a recommender trained by Kuaishou on that data; and simulations of a transparent recommender whose scale is calibrated to OneRec's measured responses. Video content is labelled by large language models, whose reliability we check by comparing models rather than by hand. Gender and relationships is our case study, because it is the largest social issue in what users are shown and its most harmful narrative, a negative label on a whole gender, can be defined precisely.

Our contributions are:

1. a definition of a viewpoint cocoon that separates it from topic interest, with an exact split of a user's skew into a platform layer and a personal layer (Section 3);
2. a set of propositions showing that the property that lets a recommender build a cocoon is the same one that lets a user take it apart, and what each kind of control can and cannot reach (Section 3);
3. a data-driven map of where opposing narratives appear in a real feed, and evidence that an open-source model greatly overstates them (Section 4);
4. experiments showing that a recommender trained only on logs can respond to "not interested" in the wrong direction, and simulations comparing the cost and persistence of user strategies (Section 5); and
5. design implications for a user-side "viewpoint exposure report" (Section 6).

The rest of the report is organised accordingly; Section 7 discusses limitations and ethics.
