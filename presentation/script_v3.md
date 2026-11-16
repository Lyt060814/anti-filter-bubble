---
title: "COMP1110 演讲稿 v3（英文，约 1,300 词，9:30）"
subtitle: "配合 slides_v3.html；幻灯片里按 N 看到的讲稿由本文件生成"
---

括号里的提示是动作，不用念出来。数字都和报告一致。修改讲稿后运行 `python3 presentation/v3/build.py`，幻灯片里的讲稿会同步更新。

---

## Fu Yitong（第 1–4 页，约 2:20）

**Slide 1 · 0:22**
> You just wanted to relax. Then: "No internship by sophomore summer? You are lagging behind." *(停一拍)* Thanks, I was about to have a nice evening. *(停一拍)* Videos like this, and a feed that keeps serving them to you, are what our project studies: the information cocoon. How common it is, how it forms, and how to get out.

**Slide 2 · 0:22**
> Everyone has heard of the information cocoon: your feed shows you more of what you already like. You may think, bro, that's cliché. But we have something special. Most research defines a cocoon by topic: by that definition, you are in a cocoon if your feed is stuck on a few topics, like football or relationships. But this can be misleading.

**Slide 3 · 0:46**
> *(翻页)* Look, here are two users, and each square is a video. *(指图例)* Dark squares are everything else in the feed. Light squares are marriage videos. Red squares are marriage videos with a very one-sided message, like "Not married by thirty? You are gonna die alone." A topic check can only count the light squares. Both users have thirty percent, so by that definition they are in exactly the same level of cocoon. But it cannot see the red ones, and User 2 meets red twice as often. Her feed kept the topic and narrowed the view. That is what we call a **viewpoint cocoon**.

**Slide 4 · 0:50**
> That is our first vital difference from existing work: we measure the viewpoint inside a topic. And it means a user does not have to give up a topic they like just to escape the skew.
>
> Our second vital difference: we look from the inside. Most audits look from the outside: they create fake accounts and see what gets recommended. But then you cannot separate the causes of a one-sided feed. Is it because many creators simply post this view? Because the platform loves promoting it? Or because you just keep watching it? With public Kuaishou logs and an open recommender, we can separate the three. Wang Junbo will show how we make this measurable.

---

## Wang Junbo（第 5–6 页，约 1:20）

**Slide 5 · 0:40**
> Fu asked: is it the creators, the platform, or you? First we need one number, skew: how often a view is shown, compared with how often it actually exists. *(逐层指)* Start with what creators post: that is the baseline. Then what the platform shows everyone: anything above the baseline is the **platform layer**, and everyone gets it. Then what your own feed shows you: anything above that is your **personal layer**, built by your own watching. *(指左边圆圈)* Think of a stage tilted for everyone, and one person leaning further. And anything you can press, whether like, skip or "not interested", reaches only your own lean.

**Slide 6 · 0:40**
> So we ask four questions, and each needs its own evidence. *(逐列指)* How common are these videos, and how big is the platform layer? We read the logs: 160,000 users, every video labelled by language models. How does a personal layer form? We probe OneRec, a recommender trained on these logs, then simulate months of use. Can a user notice it? We count how many videos it takes. And what does each way out cost? We simulate every option. Zhao Dingcheng starts with the first question.

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
