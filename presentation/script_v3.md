---
title: "COMP1110 演讲稿 v3（英文，约 1,300 词，9:30）"
subtitle: "配合 slides_v3.html；幻灯片里按 N 看到的讲稿由本文件生成"
---

括号里的提示是动作，不用念出来。数字都和报告一致。修改讲稿后运行 `python3 presentation/v3/build.py`，幻灯片里的讲稿会同步更新。

---

## Fu Yitong（第 1–3 页，约 1:40）

**Slide 1 · 0:15**
> Hello everyone. We are Fu Yitong, Wang Junbo, Zhao Dingcheng, Li Yitong and Xu Ruicong. Our project is about what happens *inside* the topics your short-video feed shows you.

**Slide 2 · 0:50**
> Here are two feeds. *(指两组方格)* Each square is a video, and the pale ones are about marriage. In both feeds, that is thirty percent. Chinese apps now offer a "cocoon check", and it would give these two feeds exactly the same score.
>
> Now look inside the topic. The red squares are videos that pin a negative trait on a whole gender, like *(指右边)* "Women today only look at the bride price." Feed A meets one of these in every sixteen marriage videos. Feed B meets one in every eight: twice the odds.
>
> Feed B has kept the topic, but narrowed the view. We call this a **viewpoint cocoon**.

**Slide 3 · 0:35**
> Today's tools cannot see this. *(左边逐条)* Cocoon checks, and most research, count how narrow your *topics* are. Studies of viewpoints focus on politics, and look at the platform from outside. Studies of buttons ask what a button removes, not what it costs you.
>
> *(指底部)* So we ask four questions. How common are such videos? How does a cocoon form? Can a user notice it? And can they get out? Wang Junbo will show how we make this measurable.

---

## Wang Junbo（第 4–6 页，约 1:50）

**Slide 4 · 0:35**
> A feed has two separate dials. *(横轴)* Interest: how much of your feed is the topic. *(纵轴)* Skew: inside the topic, how much more often one view shows up than it actually exists.
>
> A topic fan who sees all sides is fine. A cocoon is high skew, whatever the interest. Feeds A and B sit at the same interest, one above the other. A cocoon check reads only this bottom axis, so it cannot tell them apart.

**Slide 5 · 0:45**
> Where does the skew come from? Picture a stage that is tilted for everyone, and one person who leans further on their own.
>
> *(逐级指数字)* Among the marriage videos on offer, about one in twenty-four carries a gender label. Ranking shows them to everyone at one in sixteen. That is the **platform layer**: the tilted stage. For the most skewed tenth of heavy viewers, their own history pushes it to one in eight. That is the **personal layer**.
>
> And everything a user can press, whether like, skip or "not interested", reaches only the inner ring.

**Slide 6 · 0:30**
> We cannot open Kuaishou's app, so we found four ways in. Its public logs from 160,000 users tell us what people were actually shown. OneRec, a recommender trained on those logs, lets us change a history and watch how it reacts. A simulation runs that reaction forward for months. And a counting bound tells us what a user could notice. Zhao Dingcheng starts with the first question.

---

## Zhao Dingcheng（第 7–8 页，约 1:35）

**Slide 7 · 0:45**
> An open model reads every video description. *(指左边)* Videos take sides in four ways; the sharpest is the group label. *(指下方)* It counts only if all four hold: a whole gender, a negative trait, all or most of them, and in the video's own voice. Quoting it to rebut it does not count.
>
> *(指右边)* Two stronger models, DeepSeek and GPT, relabelled 1,200 videos. Our model agrees with them well, a kappa of 0.78, and we correct every share for the errors it still makes. We count labels against *either* gender, and take no side on marriage.

**Slide 8 · 0:50**
> So how common are they? *(点阵)* Social issues are about eight percent of everything shown, and within them about one video in five takes a side.
>
> *(中间)* These videos draw more reactions: nearly twice the comments. But they are also marked "not interested" more often: these are associations, and the attention is not simply approval.
>
> *(右边)* And ranking shows them more often than they exist, in every issue area, by up to one and a half times the odds. For gender labels, that is the one in sixteen you saw a moment ago: the platform layer, and everyone gets it.
>
> But what does a user's *own* history add? Li Yitong.

---

## Li Yitong（第 9–10 页，约 1:40）

**Slide 9 · 0:55**
> To see how the recommender reacts, we ran a controlled experiment on OneRec. *(左边)* We take a real user's history, swap in ten new videos, and compute exactly what the model would recommend next, for two hundred users.
>
> *(右边)* Ten issue videos raise the topic strongly. Ten group-label videos raise the narrative two-thirds as much, while a random split stays at zero. So the model really does tell this narrative apart, and that means it can amplify it.
>
> *(指红框，放慢)* And remember this one: if the same ten videos are marked "not interested", the narrative still goes **up**. The button is read as interest.

**Slide 10 · 0:45**
> One edit is one step. To follow months of use, we built a simulation whose recommender responds the way the probe measured. Take a topic fan who tends to finish group-label videos. *(沿红线)* After about three weeks the skew is half-way, and by three months the odds of meeting the label have doubled.
>
> *(指虚线)* Meanwhile the topic share sits flat at thirty percent, so a cocoon check sees nothing. A casual viewer with the same taste barely moves.
>
> Could this fan notice? Xu Ruicong.

---

## Xu Ruicong（第 11–13 页，约 2:05）

**Slide 11 · 0:45**
> Noticing means telling a real tilt from bad luck. It is like checking whether a coin is loaded: ten flips are not enough, and you need a fair coin to compare with.
>
> To see a doubling, a user needs about 490 labelled issue videos from their own feed, and as many again from a feed without personalisation. *(指条形)* Their own feed fills up in nine days. The reference takes about four months. If the platform published a reference, six days would be enough.

**Slide 12 · 0:55**
> Now suppose the fan wants out but wants to keep the topic. We tried eleven ways out, each for seventeen days. *(说明坐标)* Up means skew removed; right means more of the topic kept.
>
> *(左下)* Turning personalisation off, or "show less of this topic", removes the skew by removing the topic. *(右边)* Scrolling past the labels keeps the topic and works. Pressing "not interested" on the same videos works *worse* than scrolling past, because, as Li Yitong said, each press is read as interest. *(顶部)* A filter goes furthest, and it needs no help from the recommender.

**Slide 13 · 0:25**
> And when the user stops, *(沿曲线回升)* every curve climbs back. Half the gain is gone in about a week. Escape is a habit, not a button.
>
> Fu Yitong will close.

---

## Fu Yitong（第 14 页，约 0:40）

**Slide 14 · 0:40**
> So what does this mean? *(左)* A user can lower their own layer: change what they finish, use a filter, and keep doing it.
>
> *(右)* But only the platform can measure the view inside each topic, publish the reference that makes skew visible, make "not interested" mean not interested, and decide how much ranking amplifies what provokes.
>
> Our evidence comes from logs, an open model and simulation, and we measure what people see, not what they believe.
>
> Next time a check calls your feed diverse, look inside the topic. Thank you.

---

## 排练提示

- **说数字后停半秒。** 比例统一说 "one in sixteen"，不念百分比。
- **三处伏笔都要讲出来：** 第 9 页 "remember this"，第 12 页 "as Li Yitong said"，第 14 页 "make 'not interested' mean not interested"。
- **超时先砍：** 第 7 页的四类例句（不念），然后第 11 页最后一句（平台公布参照只需 6 天）。
