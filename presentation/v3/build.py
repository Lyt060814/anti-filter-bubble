"""Assemble presentation/slides_v3.html from the v2 deck's fonts, styles and engine plus new slides."""
import json, sys
from pathlib import Path

HERE = Path(__file__).parent
REPO = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parents[1]
src = (REPO / "presentation/slides.html").read_text(encoding="utf-8")

head = src[: src.index("</style></head>")]
head = head.replace("<title>Viewpoint Cocoons — COMP1110 Presentation</title>", "<title>Viewpoint Cocoons — COMP1110 Presentation (v3)</title>")
engine = src[src.index("const STATIC="): src.index("/* ---------- per-slide initialisers ---------- */")]
nav = src[src.index("/* ---------- navigation ---------- */"):]
nav = nav.replace("$('#hud-name').textContent=s.dataset.speaker;",
                  "$('#hud-name').textContent=s.dataset.speaker;updRQ(s);")
assert "updRQ(s)" in nav

css = """
/* v3 additions */
#hud-rq{position:absolute;left:680px;bottom:40px;font:400 17px var(--mono);letter-spacing:3px;color:rgba(141,136,125,.5);z-index:20;white-space:nowrap}
#hud-rq span{margin-right:26px}#hud-rq span.on{color:var(--rose)}
body.paper #hud-rq{color:#9a9384}body.paper #hud-rq span.on{color:#b0213f}
.trow{display:grid;grid-template-columns:260px 1fr;align-items:baseline;border-bottom:1px solid rgba(236,229,211,.18);padding:22px 0 20px;font:600 34px/1.2 var(--serif)}
.trow .ty{font-size:28px;line-height:1.35;color:var(--sepia)}.trow .ty.rose{color:var(--rose)}
.tk{font:600 34px/1.22 var(--serif);margin-top:22px;padding-left:34px;position:relative}
.tk::before{content:'—';position:absolute;left:0;color:var(--ash)}
svg text[font-family="PM"]{font-family:var(--mono)}svg text[font-family="CG"]{font-family:var(--serif)}
"""

notes = {
 1: "Hello everyone. We are Fu Yitong, Wang Junbo, Zhao Dingcheng, Li Yitong and Xu Ruicong. Our project asks what happens inside the topics your short-video feed shows you.",
 2: "Here are two feeds. In both, about thirty percent of the videos are about marriage. Short-video apps now offer a cocoon check, and it would give these two feeds the same score. Now look inside the topic. The red squares are videos that pin a negative label on a whole gender, like 'women today only look at the bride price'. Feed A meets one in sixteen. Feed B meets one in eight: twice the odds. Both rates come from the viewing logs. Feed B has kept the topic and narrowed the view. That is what we call a viewpoint cocoon.",
 3: "Today's tools cannot see this. Cocoon checks and most research count how narrow your topics are. Studies of viewpoints look at politics, from outside the app. Studies of buttons ask what a button removes, not what it costs you. So we ask four questions: how common such videos are, how a cocoon forms, whether a user can notice it, and what getting out costs. Wang Junbo will show how we make this measurable.",
 4: "A feed has two separate dials. Interest is how much of your feed is the topic. Skew is how much more often one view shows up than it actually exists. A topic fan with high interest and normal skew is fine. A cocoon is high skew, whatever the interest. Feeds A and B have the same interest, so a cocoon check, which reads only this axis, cannot tell them apart.",
 5: "Where does the skew come from? Picture a stage that is tilted for everyone, and a person who leans further on their own. Among the marriage videos on offer, about one in twenty-four carries a gender label. Ranking shows them to everyone at one in sixteen: that is the platform layer, the tilted stage. For the most skewed tenth of heavy viewers, their own history pushes it to one in eight: the personal layer. Everything a user can press, like, skip or 'not interested', reaches only the inner ring.",
 6: "We cannot open Kuaishou's app, so we found four ways in. Its public logs, a hundred and sixty thousand users, show what people were shown. OneRec, a recommender trained on those logs, lets us edit a history and watch the response. A simulation runs that response forward for months. And a counting bound tells us what a user could notice. Zhao Dingcheng starts with the first question.",
 7: "First we need to find these videos among millions. An open model reads each video description and answers a fixed list of questions. Videos take sides in four ways; the group label is the sharpest. To check the model, two stronger models relabelled twelve hundred videos. Our model agrees with them well, kappa 0.78 on group labels, and we correct every share for the errors it still makes. We count labels against either gender, and we take no side on marriage.",
 8: "So how common are they? Social issues are about eight percent of everything shown, and within them about one video in five takes a side. These videos get more reactions, nearly twice the comments. But they are also marked 'not interested' more often, so the attention is not approval. And ranking shows them more often than they exist, in every issue area. For gender labels, 4.1 percent of the videos on offer become 6.2 percent of what is shown. That is the platform layer, for everyone. What does a user's own history add? Li Yitong.",
 9: "To see how the recommender reacts, we ran a controlled experiment on OneRec. We took a real user's history, swapped in ten new videos, and computed exactly what the model would recommend next, for two hundred users. Ten issue videos raise the topic strongly. Ten group-label videos raise the narrative two-thirds as much, while a random split stays at zero: the model really does tell this narrative apart, so it can amplify it. One more result to remember: if the same ten videos are marked 'not interested', the narrative still goes up. The button is read as interest.",
 10: "One edit is one step. To follow weeks of use, we built a simulation whose recommender responds as the probe measured. Take a topic fan who tends to finish group-label videos. After about three weeks the skew is half-way, and by three months the odds of meeting the label have doubled. The topic share, the dashed line, sits flat at thirty percent the whole time, so a cocoon check sees nothing. A casual viewer with the same taste barely moves. Could this fan notice? Xu Ruicong.",
 11: "Noticing means telling a real tilt from bad luck, like telling a loaded coin from a fair one. Ten flips are not enough, and you also need a fair coin to compare with. To see a doubling, a user needs about four hundred and ninety labelled issue videos from their own feed, and as many from a feed without personalisation. Their own feed gives that in nine days. The reference takes about four months. If the platform published the reference, six days would do.",
 12: "Now suppose the fan wants out, but wants to keep the topic. We tried eleven ways out for seventeen days. Up is skew removed; right is topic kept. Turning personalisation off, or 'show less of this topic', removes the skew by removing the topic. Scrolling past the label keeps the topic and works. Pressing 'not interested' on the same videos works worse than scrolling past: remember, each press is read as interest. A filter goes furthest and needs no help from the recommender.",
 13: "And when the user stops, every curve climbs back. Half of the gain is gone in about a week. Escape is a habit, not a button. Fu Yitong will close.",
 14: "So what does this mean? A user can lower their own layer: change what they finish, use a filter, and keep doing it. But only the platform can measure the view inside each topic, publish the reference that makes skew visible, make 'not interested' mean not interested, and decide how much ranking amplifies what provokes. Our evidence comes from logs, an open model and simulation; we measure what people see, not what they believe. Next time a check calls your feed diverse, look inside the topic. Thank you.",
}
dur = [15, 50, 35, 35, 45, 30, 40, 55, 55, 45, 45, 55, 25, 40]
cum = [0]
for d in dur:
    cum.append(cum[-1] + d)

data = json.loads((HERE / "data.json").read_text())
sections = (HERE / "sections.html").read_text(encoding="utf-8")
enters = (HERE / "enters.js").read_text(encoding="utf-8")
assert sections.count('<section class="slide"') == len(dur) == len(notes)

hud = """
<div id="hud-sp"><small>SPEAKER</small><b id="hud-name"></b></div>
<div id="hud-pj">VIEWPOINT COCOONS · COMP1110</div>
<div id="hud-rq"><span data-q="1">RQ1 HOW COMMON</span><span data-q="2">RQ2 FORMATION</span><span data-q="3">RQ3 NOTICING</span><span data-q="4">RQ4 ESCAPE</span></div>
<div id="hud-pg"></div>
<div id="grain"></div><div id="vig"></div>
<div id="timer"></div>
<div id="notes"><div class="meta"></div><div class="txt"></div></div>
</div>
"""
consts = (
    "const NOTES=" + json.dumps({str(k): v for k, v in notes.items()}, ensure_ascii=False) + ";\n"
    + "const CUM=" + json.dumps(cum) + "; // cumulative end times (s)\n"
    + "// Simulation series and escape results from report/latex/figures/src/results.json\n"
    + "const FORM=" + json.dumps(data["FORM"], separators=(",", ":")) + ";\n"
    + "const ESC=" + json.dumps(data["ESC"], separators=(",", ":")) + ";\n"
    + "const TRAJ=" + json.dumps(data["TRAJ"], separators=(",", ":")) + ";\n"
)
rq = "function updRQ(s){const q=s.dataset.rq;$('#hud-rq').style.visibility=s.id==='s1'?'hidden':'visible';$$('#hud-rq span').forEach(e=>e.classList.toggle('on',e.dataset.q===q))}\n"

out = (head + css + "</style></head>\n<body>\n<div id=\"stage\">\n<canvas id=\"bg\"></canvas>\n\n"
       + sections + hud + "\n<script>\n" + consts + engine + enters + rq + nav)
(REPO / "presentation/slides_v3.html").write_text(out, encoding="utf-8")
print("ok", len(out), "total", cum[-1], "s")
