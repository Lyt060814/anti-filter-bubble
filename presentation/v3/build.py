"""Assemble presentation/slides_v3.html from the v2 deck's fonts, styles and engine plus new slides."""
import json, re, sys
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

def read_script(path):
    """Speaker notes per slide from script_v3.md: the quoted lines under each '**Slide N' heading."""
    notes, cur = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\*\*Slide (\d+)", line)
        if m:
            cur = int(m.group(1)); notes[cur] = []
        elif line.startswith("## "):
            cur = None
        elif cur and line.startswith(">"):
            t = line[1:].strip()
            if t:
                notes[cur].append(t)
    out = {}
    for k, ps in notes.items():
        t = " ".join(ps)
        t = re.sub(r"\*\(([^)]*)\)\*", r"[\1]", t)   # stage cues
        t = t.replace("**", "").replace("*", "")
        out[k] = t
    return out


notes = read_script(REPO / "presentation/script_v3.md")
dur = [15, 50, 35, 35, 45, 30, 45, 50, 55, 45, 45, 55, 25, 40]
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
