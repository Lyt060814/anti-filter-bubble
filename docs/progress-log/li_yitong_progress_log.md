**Name:** Li Yitong (3036289377)

**Role:** Technical integration, research design, recommender experiments and data infrastructure

**Work completed**

- *Before the plan.* Reviewed prior work on information cocoons and user controls, and traced how "not interested" feedback works in X's open-source recommender. Ran data checks on ShortVideo and KuaiRand and small pilots with LLM-simulated users. Wrote the technical part of the project plan.
- *After the plan feedback.* The feedback said our question was vague and two key terms were undefined. I reworked the question into a measurable one: when a user says they do not want one viewpoint on an issue, how much does that viewpoint drop compared with other content on the same issue? I defined the issue corpus, viewpoint exposure and a selectivity score (1 if only the targeted viewpoint drops, 0 if the whole issue drops equally), and derived limits for three controls: topic tags give zero selectivity; classifier filters and embedding-based feedback are limited by how well they separate viewpoints.
- *This week.* Checked data and compute. Kuaishou's RecIF dataset has 162k users, 75.7M impressions and about 54k "not interested" events. I moved data and experiments to a GPU server.

**Difficulties encountered**

- Our earlier simulation cut a viewpoint's weight to 0.7 and the topic's to 0.97 after each "not interested", but these numbers had no source, and X's code cannot supply them. We will measure them on trained recommenders instead.
- Real logs are too sparse for a single issue: for marriage and gender, only 22 events can be compared before and after. The main measurement will therefore use controlled inputs to recommenders trained on all events, with logs as a topic-level check.
- Explicit claims are rare and mostly one-sided in the data, while framing that blames a whole gender recurs. I am proposing that we label framing alongside stance.

**In progress and next steps**

I am checking whether Kuaishou's OneRec model responds to "not interested" history as expected. Next, I will measure selectivity for the three controls on the group's labelled videos, work with Zhao Dingcheng on comparing strategies and the held-out issue, and with Xu Ruicong on evaluating simulated users with measured parameters. By 12 November I will write my sections of the report draft.
