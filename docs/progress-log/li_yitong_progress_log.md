**Name:** Li Yitong (3036289377)

**Role:** Technical integration, recommendation simulation and intervention experiments

**Work completed**

- Refined the research question with Fu Yitong and Wang Junbo: helping users see fewer unwanted claims while keeping useful content on the same topic. I wrote formal definitions of the issue corpus, viewpoint exposure and a selectivity score, which compares how much a control reduces the unwanted viewpoint with how much it reduces the rest of the issue.
- With Xu Ruicong, built a simple recommendation simulator comparing five actions, including negative feedback, topic filtering and selective filtering with extra content.
- Checked larger data and compute for the experiments: Kuaishou's RecIF dataset (162k users, about 54k "not interested" records) and a GPU server.

**Difficulties encountered**

- The simulator's feedback parameters, such as how much one "not interested" lowers a viewpoint compared with its topic, were set by hand, and no public source gives them. I am replacing them with values measured on a trained recommender (Kuaishou's OneRec).
- Real "not interested" records on a single issue are too few for a direct before-and-after comparison, so we test the trained model with controlled inputs and use the logs as a check.

**In progress and next steps**

I am improving the simulator with measured feedback, classification errors and stopping interventions (with Xu Ruicong). By 8 November I will compare the five strategies under different assumptions and on the new issue (with Zhao Dingcheng and Xu Ruicong), then write my section of the report draft by 12 November.
