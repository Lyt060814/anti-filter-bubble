# 3 Concepts and Theory

<!-- L6 draft, Li Yitong, 2026-11-07. Definitions and propositions adapted from research_plan_v5.md section 4 and research_plan_v6.md section 3. Numbers in the worked examples are illustrative unless a source is given. -->

This section defines what we mean by a viewpoint cocoon, separates it from ordinary interest in a topic, and derives how different user actions can or cannot change it. The definitions are used throughout Sections 4 and 5; the propositions give testable predictions that the simulations in Section 5 check.

## 3.1 A cocoon is a relation, not a kind of content

A cocoon is not a property of any single video. It describes how the mix of videos a person is shown differs from some reference mix. Defining it therefore needs three things: an issue and an attribute within it, the person's exposure, and a reference.

Let $\mathcal I$ be all videos and $I_k \subseteq \mathcal I$ the videos about issue $k$ (here, gender and relationships). Within the issue, an attribute $s$ splits videos into a **target set** $A$ (for example, videos that attach a negative label to a whole gender) and a **retained set** $B$ (other videos on the issue, which the user wants to keep seeing). Videos whose attribute cannot be judged are reported separately.

For user $u$ at time $t$, let $\pi_{u,t}(i)$ be the probability that the next video shown is $i$, and write $\pi(G)=\sum_{i\in G}\pi(i)$ for a set of videos $G$. We describe the user's state with two numbers:

$$m_{u,t}=\pi_{u,t}(I_k), \qquad p_{u,t}=\frac{\pi_{u,t}(A)}{\pi_{u,t}(A\cup B)} .$$

The **topic share** $m$ measures interest: how much of the feed is about the issue. The **within-issue share** $p$ measures what the user sees once they are on the issue. A user with high $m$ and an ordinary $p$ simply likes the topic. A user whose $p$ is far above a reference is in a viewpoint cocoon, whatever their $m$. Category-diversity measures used in earlier work (Section 2.1) capture only $m$.

## 3.2 Three references and a decomposition of skew

"Far above" needs a reference. We use three:

- the **supply share** $p^{\mathrm{sup}}$: the share of $A$ among the issue videos available on the platform;
- the **platform share** $\bar p=\bar\pi(A)/\bar\pi(A\cup B)$, where $\bar\pi$ is the exposure averaged over all users, so it is what the platform shows on average;
- the share $p^{\mathrm{np}}$ a user would see with personalisation switched off, a setting that Chinese regulation requires platforms to offer.

On the log-odds scale, $\operatorname{logit}p=\log\frac{p}{1-p}$, the total skew a user experiences splits exactly into two parts:

$$\underbrace{\operatorname{logit}p_u-\operatorname{logit}p^{\mathrm{sup}}}_{\text{total skew}}
=\underbrace{\operatorname{logit}\bar p-\operatorname{logit}p^{\mathrm{sup}}}_{\text{platform layer}}
+\underbrace{\operatorname{logit}p_u-\operatorname{logit}\bar p}_{\text{personal layer, } V_u} .$$

The **platform layer** is shared by everyone: ranking that favours a narrative raises it for all users. The **personal layer** $V_u$ is the part created by personalisation, and it is what we call the user's viewpoint skew. Supply itself is only described, not judged: calling the supply "skewed" would require an external standard, such as how views are distributed in society, which we do not have and do not assume.

*Worked example (illustrative numbers).* Suppose 1.0% of the available marriage videos carry a gender group label, the platform shows them in 1.4% of its marriage-video impressions on average, and one user sees them in 2.8%. The user's total skew is $\operatorname{logit}0.028-\operatorname{logit}0.010=1.05$. Of this, $0.34$ is the platform layer and $V_u=0.71$ is personal: the odds that this user meets the narrative are about twice the platform average ($e^{0.71}\approx2.0$). Reporting only $V_u$ would hide the platform layer; reporting only the total would hide that personalisation doubled it.

In the simulations of Section 5 there is no separate platform population, so the reported skew is the total skew relative to supply.

## 3.3 How a feedback action moves the state

To see how a user's actions change $(m,V)$, consider the standard dot-product recommender with softmax exposure: each video has a vector $v_i$, the user has a vector $u$, and

$$\pi(i)\propto\exp\!\left(\langle u,v_i\rangle/\tau\right).$$

When the user gives feedback on video $j$ (completing it, liking it, or marking it "not interested"), the user vector moves to $u+\eta v_j$, with $\eta>0$ for positive and $\eta<0$ for negative feedback. Let $s_j(i)=\langle v_j,v_i\rangle$ be the similarity of video $i$ to $j$, and $\bar s_j(G)$ its exposure-weighted average over a set $G$.

**Proposition 1 (first-order effect of feedback).** For small $\eta$,

$$\Delta V\approx\frac{\eta}{\tau}\big[\bar s_j(A)-\bar s_j(B)\big]=\frac{\eta}{\tau}\,c_j,
\qquad
\Delta\log m\approx\frac{\eta}{\tau}\big[\bar s_j(I_k)-\bar s_j(\mathcal I)\big]=\frac{\eta}{\tau}\,t_j .$$

*Reason.* After the update, $\log\pi(i)$ changes by $\frac{\eta}{\tau}s_j(i)$ minus a normalising constant that is the same for every video. Summing over a set and taking a first-order expansion gives $\Delta\log\pi(G)\approx\frac{\eta}{\tau}[\bar s_j(G)-\bar s_j(\mathcal I)]$. $V$ is $\log\pi(A)-\log\pi(B)$ minus a constant, so the normalising terms cancel.

We call $c_j$ the **attribute contrast** (how much more similar $j$ is to $A$ than to $B$) and $t_j$ the **topic contrast** (how much more similar $j$ is to the issue than to the rest of the feed). Three consequences follow.

1. *Formation and escape depend on the same quantity.* If a user completes more $A$ than $B$ videos, $V$ grows at a rate proportional to $c$. If $c\approx0$, the user's preferences cannot create a personal viewpoint skew, and the user's own feedback cannot remove one either. Whatever lets a recommender build a cocoon is also what lets a user take it apart.
2. *The exchange rate of "not interested".* Marking an $A$ video as not interested lowers $V$ by $\frac{|\eta|}{\tau}c_a$ but lowers $\log m$ by $\frac{|\eta|}{\tau}t_a$. Each unit of viewpoint skew removed costs $t_a/c_a$ units of topic share. When the recommender's representation is organised mainly by topic ($t\gg c$), the user loses much of the issue to remove a little of the narrative.
3. *Engaging with the retained content.* Positive feedback on a $B$ video lowers $V$ while raising $m$, so in principle it avoids topic loss. How much it lowers $V$ depends on $\bar s_b(B)-\bar s_b(A)$; Section 5 shows that this can be very small when $A$ is rare.

The sign and size of $\eta$ for "not interested" are set by how a platform implements the button, not by the user. A recommender that only learns from logs may give it the wrong sign: in our test of OneRec, putting videos in the "not interested" field increased, rather than decreased, recommendations of similar videos (Section 5).

## 3.4 What other controls can and cannot do

**Proposition 2 (topic and tag controls).** If an action multiplies the exposure of every video in a tag or topic by the same factor, $\Delta V$ depends only on how the attribute is distributed across tags; if every tag contains $A$ in the same proportion, $\Delta V=0$. Switching off the whole issue sets $m$ to zero, at which point $V$ is undefined. Likewise, any "cocoon check" that summarises the feed by content categories, such as the self-assessment features launched by Chinese platforms in 2025, cannot see $V$.

**Proposition 3 (filters).** If an external filter removes every video it classifies as $A$, with exposure-weighted recall $\mathrm{TPR}$ and false-positive rate $\mathrm{FPR}$, and the removed slots are not refilled,

$$\Delta V=\log\frac{1-\mathrm{TPR}}{1-\mathrm{FPR}},\qquad \Delta\log m=\log\big(1-p\,\mathrm{TPR}-(1-p)\,\mathrm{FPR}\big).$$

Keyword blocking, author blocking and LLM-based filtering are all of this kind; they differ only in their recall and false-positive rate. A filter changes what is shown but not the recommender's state, so its effect stops as soon as it is switched off.

**Proposition 4 (strong feedback).** Repeated "not interested" on $A$ videos tilts exposure to $\pi^\kappa(i)\propto\pi(i)e^{-\kappa s_j(i)}$ with growing $\kappa$. The within-issue share $p$ falls as long as $A$ remains more similar to $j$ than $B$; but if some off-issue content is less similar to $j$ than every issue video, the topic share $m$ goes to zero as $\kappa\to\infty$. Pushed far enough, the button improves the mix within the issue by removing the issue.

**Proposition 5 (what users can reach).** Actions that change the recommender's state (feedback, deleting history, resetting) act on the user vector, so they can remove the personal layer $V_u$ but not the platform layer, which is fixed by supply and global ranking. Switching personalisation off sets $V_u$ to zero and leaves the user with the platform layer. Only filters, or leaving the platform, act on the platform layer.

## 3.5 Can a user notice a cocoon?

A user sees only their own feed. To tell whether the narrative is over-represented, they, or a tool on their side, must count it in what they see and compare it with a reference sample, for example from the personalisation-free feed. Both counts rely on a classifier with recall $\alpha$ and false-positive rate $\beta$, so the observed share is $q=\beta+(\alpha-\beta)p$.

**Proposition 6 (sample size for detection).** With $n$ issue videos from the user's feed and $n$ from the reference, a one-sided test at level $a$ with power $1-\gamma$ that the user's share exceeds the reference needs approximately

$$n\approx\frac{(z_a+z_\gamma)^2\,[q_u(1-q_u)+q_0(1-q_0)]}{(\alpha-\beta)^2\,(p_u-p_0)^2}$$

issue videos in each sample (standard two-sample test with a misclassification correction; Rogan & Gladen, 1978).

*Worked example.* Take the reference share $p_0=1.0\%$ (the rate at which the reference model labels marriage videos as carrying a gender group label, Section 4.3), a user who sees the narrative at twice the odds ($p_u=1.98\%$), $a=0.05$ and power $0.8$. With a good classifier ($\alpha=0.8$, $\beta=0.02$), the user needs about 6,500 issue videos in each sample. At the median share of issue videos in RecIF histories (1.6% of all impressions), that is about 400,000 impressions, roughly 800 times the median length of a user history in the data. With a four-fold skew the requirement falls to about 900 issue videos. With an open model as the classifier ($\beta=0.125$, Section 4.3), even the four-fold case needs about 4,000. A user cannot notice a rare narrative from their own feed; a platform, which knows $\pi_u$ directly, can compute $V_u$ without sampling.
