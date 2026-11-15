"""Schematic figures drawn as HTML and printed to vector PDF with headless Chromium.

Constructed for an idealised teaching report (see ../../README.md).
Run:  python3 schematics.py [concept|overview|mockup]     # writes ../fig_<name>.pdf
"""
from __future__ import annotations

import json
import random
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

import model as M

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
R = json.loads((SRC / "results.json").read_text())
CHROME = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")

C_A, C_B, C_O = "#D1603D", "#2B5C8A", "#D5DAE1"
INK, TICK, LINE, PANEL = "#1A1A1A", "#5F6670", "#DFE3E8", "#F6F7F9"

BASE_CSS = f"""
@font-face {{ font-family: Inter; font-weight: 400; src: url(fonts/Inter-Regular.ttf); }}
@font-face {{ font-family: Inter; font-weight: 600; src: url(fonts/Inter-SemiBold.ttf); }}
@font-face {{ font-family: Inter; font-weight: 700; src: url(fonts/Inter-Bold.ttf); }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #fff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: Inter, sans-serif; color: {INK}; font-size: 18px; line-height: 1.3; }}
b, .b {{ font-weight: 700; }} .sb {{ font-weight: 600; }}
.mute {{ color: {TICK}; }} .a {{ color: {C_A}; }} .bl {{ color: {C_B}; }}
"""


def render(name: str, html: str, width: int, height: int):
    page = f"<!doctype html><html><head><meta charset='utf-8'><style>@page {{ size: {width}px {height}px; margin: 0; }}{BASE_CSS}" \
           f"body {{ width: {width}px; height: {height}px; overflow: hidden; }}</style></head><body>{html}</body></html>"
    src = SRC / f".{name}.html"
    src.write_text(page)
    out = OUT / f"fig_{name}.pdf"
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--run-all-compositor-stages-before-draw",
                    "--virtual-time-budget=4000", "--no-pdf-header-footer", f"--print-to-pdf={out}", f"file://{src}"],
                   check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    info = subprocess.run(["pdfinfo", str(out)], capture_output=True, text=True).stdout
    pages = [l for l in info.splitlines() if l.startswith("Pages")]
    print("wrote", out.name, pages)


# ------------------------------------------------------------------------------------- concept
def concept():
    rnd = random.Random(7)

    def grid(n_issue, n_a):
        cells = ["o"] * 100
        idx = rnd.sample(range(100), n_issue)
        for i in idx:
            cells[i] = "b"
        for i in rnd.sample(idx, n_a):
            cells[i] = "a"
        return "".join(f"<i class='t {c}'></i>" for c in cells)

    v = R["formation"]["users"]["fan_strong"]["V_end"]
    css = f"""
    .wrap {{ padding: 6px 10px 0 10px; }}
    .cols {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 28px; }}
    .who {{ font-size: 20px; font-weight: 700; margin-bottom: 1px; }}
    .sub {{ font-size: 16px; color: {TICK}; margin-bottom: 7px; }}
    .phone {{ background: {PANEL}; border: 1.5px solid {LINE}; border-radius: 18px; padding: 12px; }}
    .g {{ display: grid; grid-template-columns: repeat(10, 1fr); gap: 3.5px; }}
    .t {{ display: block; aspect-ratio: 1; border-radius: 4px; background: {C_O}; }}
    .t.b {{ background: {C_B}; }} .t.a {{ background: {C_A}; box-shadow: 0 0 0 2px #fff, 0 0 0 3.6px {C_A}; }}
    .legend {{ display: flex; justify-content: center; gap: 16px; margin: 10px 0 9px 0; font-size: 15.5px; color: {TICK}; white-space: nowrap; }}
    .legend i {{ display: inline-block; width: 13px; height: 13px; border-radius: 3px; margin-right: 5px; vertical-align: -1px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 17px; }}
    td {{ padding: 7px 5px; border-top: 1.5px solid {LINE}; vertical-align: middle; }}
    td.k {{ width: 50%; }} td.n {{ width: 12%; text-align: center; font-size: 22px; font-weight: 700; }}
    td.r {{ text-align: right; font-weight: 600; }}
    .small {{ font-size: 14.5px; color: {TICK}; display: block; margin-top: 1px; }}
    .pill {{ display: inline-block; padding: 3px 9px; border-radius: 999px; font-size: 15px; font-weight: 700; white-space: nowrap; }}
    .pill.g1 {{ background: #E9EDF2; color: {TICK}; }} .pill.g2 {{ background: #FBE9E2; color: {C_A}; }}
    """
    html = f"""<style>{css}</style><div class='wrap'>
    <div class='cols'>
      <div><div class='who bl'>User 1</div><div class='sub'>follows the topic</div><div class='phone'><div class='g'>{grid(30, 2)}</div></div></div>
      <div><div class='who a'>User 2</div><div class='sub'>same topic, narrower view</div><div class='phone'><div class='g'>{grid(30, 4)}</div></div></div>
    </div>
    <div class='legend'><span><i style='background:{C_O}'></i>other videos</span><span><i style='background:{C_B}'></i>gender &amp; marriage</span>
      <span><i style='background:{C_A}'></i>… with a gender group label</span></div>
    <table>
      <tr><td class='k'><b>Topic share</b><span class='small'>what category-level “cocoon checks” see</span></td>
          <td class='n bl'>30%</td><td class='n a'>30%</td><td class='r'><span class='pill g1'>no difference</span></td></tr>
      <tr><td class='k'><b>Group-label share in the topic</b><span class='small'>what this study measures: skew <i>V</i></span></td>
          <td class='n bl'>6%</td><td class='n a'>13%</td><td class='r'><span class='pill g2'>odds ×{np.exp(v):.1f}</span></td></tr>
    </table></div>"""
    render("concept", html, 620, 512)


# ------------------------------------------------------------------------------------- overview
def overview():
    css = f"""
    .wrap {{ display: grid; grid-template-columns: 250px 34px 262px 34px 1fr 34px 236px; align-items: stretch; padding: 4px; height: 100%; }}
    .col {{ display: flex; flex-direction: column; gap: 12px; }}
    .hd {{ font-size: 16px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: {TICK}; margin-bottom: 0; }}
    .box {{ background: {PANEL}; border: 1.5px solid {LINE}; border-radius: 14px; padding: 13px 15px; flex: 1; }}
    .box h4 {{ font-size: 19.5px; font-weight: 700; margin-bottom: 5px; }}
    .box p {{ font-size: 17px; color: #3A4048; line-height: 1.32; }}
    .box p + p {{ margin-top: 5px; }}
    .num {{ font-weight: 700; color: {INK}; }}
    .arrow {{ display: flex; align-items: center; justify-content: center; }}
    .arrow svg {{ width: 22px; height: 30px; }}
    .ev {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; flex: 1; }}
    .ev .box {{ padding: 12px 14px; }}
    .tag {{ display: inline-block; font-size: 14.5px; font-weight: 700; padding: 2px 9px; border-radius: 999px; margin-bottom: 6px; }}
    .t1 {{ background: #E3ECF5; color: {C_B}; }} .t2 {{ background: #FBE9E2; color: {C_A}; }}
    .t3 {{ background: #E3F1F1; color: #23797A; }} .t4 {{ background: #F5EDD9; color: #9A7217; }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }}
    .chip {{ font-size: 15px; font-weight: 600; padding: 3px 9px; border-radius: 7px; background: #fff; border: 1.5px solid {LINE}; }}
    .rq {{ border-left: 5px solid {C_B}; }} .rq.r2 {{ border-left-color: {C_A}; }} .rq.r3 {{ border-left-color: #23797A; }}
    .rq.d {{ border-left-color: #9A7217; background: #FCF8EE; }}
    .rq h4 {{ font-size: 18.5px; }} .rq p {{ font-size: 16.5px; }}
    """
    arrow = "<div class='arrow'><svg viewBox='0 0 22 30'><path d='M3 4 L16 15 L3 26' fill='none' stroke='#AEB5BF' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'/></svg></div>"
    html = f"""<style>{css}</style><div class='wrap'>
    <div class='col'><div class='hd'>Data</div>
      <div class='box'><h4>Kuaishou RecIF logs</h4><p><span class='num'>160,412</span> users<br><span class='num'>75.3 M</span> impressions<br>
        each with a text description of the video and the user's feedback</p></div>
      <div class='box'><h4>OneRec-1.7B</h4><p>open generative recommender trained on the same logs</p></div>
    </div>{arrow}
    <div class='col'><div class='hd'>Labelling</div>
      <div class='box'><h4>Issue and narrative labels</h4><p>an open language model reads every candidate description</p>
        <div class='chips'><span class='chip'>one right way</span><span class='chip'>binary opposition</span><span class='chip'>anxiety appeal</span><span class='chip'>group label</span></div></div>
      <div class='box'><h4>Cross-check</h4><p>two stronger models relabel <span class='num'>1,200</span> videos; prevalence is corrected for the measured error rates</p></div>
    </div>{arrow}
    <div class='col'><div class='hd'>Four kinds of evidence</div>
      <div class='ev'>
        <div class='box'><span class='tag t1'>observational</span><h4>Logs</h4><p>prevalence, engagement, and the three-layer split of each user's exposure</p></div>
        <div class='box'><span class='tag t2'>interventional</span><h4>Recommender probing</h4><p>edit a history, read the exact change in what OneRec would recommend</p></div>
        <div class='box'><span class='tag t3'>mechanistic</span><h4>Transparent simulation</h4><p>a small model fitted to the probe: formation, 11 escape strategies, rebound</p></div>
        <div class='box'><span class='tag t4'>analytic</span><h4>Detection bound</h4><p>how many videos a user must count before a skew can be told from chance</p></div>
      </div>
    </div>{arrow}
    <div class='col'><div class='hd'>Questions</div>
      <div class='box rq'><h4>RQ1 · Prevalence</h4><p>How common are opposing narratives?</p></div>
      <div class='box rq r2'><h4>RQ2 · Formation</h4><p>Does the feed tilt? Can users notice?</p></div>
      <div class='box rq r3'><h4>RQ3 · Escape</h4><p>What does each action cost?</p></div>
      <div class='box rq d'><h4>Design</h4><p>Viewpoint exposure report</p></div>
    </div></div>"""
    render("overview", html, 1360, 500)


# ------------------------------------------------------------------------------------- mock-up
def mockup():
    E = R["escape"]["strategies"]
    v = R["formation"]["users"]["fan_strong"]["V_end"]
    p_user = 100 * float(M.expit(M.logit(M.P_BAR) + v))
    n_need = int(round(float(M.detection_n(np.log(2), alpha=0.79, beta=0.01)), -1))

    def eff(s):
        return f"{'+' if E[s]['dV_late'] >= 0 else '−'}{abs(E[s]['dV_late']):.1f}"

    def kept(s):
        return f"{100*E[s]['topic_kept']:.0f}%"

    def bar(label, val, vmax, col, bold=False):
        w = 100 * val / vmax
        return (f"<div class='row'><div class='lab{' b' if bold else ''}'>{label}</div><div class='track'><div class='fill' style='width:{w:.1f}%;background:{col}'></div></div>"
                f"<div class='val{' b' if bold else ''}'>{val:.1f}%</div></div>")

    acts = [("Scroll past these videos", "S1", "while you keep it up", "ok"),
            ("Press “not interested” on them", "S2", "weaker than scrolling past", "warn"),
            ("Filter them with a classifier", "S11", "only while the filter is on", "ok"),
            ("Clear your watch history", "S7", "returns within two weeks", "warn"),
            ("“Show less of this topic”", "S9", "removes the topic, not the tilt", "bad")]
    rows = "".join(f"<tr><td>{n}</td><td class='c b'>{eff(s)}</td><td class='c'>{kept(s)}</td><td class='note {cls}'>{note}</td></tr>" for n, s, note, cls in acts)
    css = f"""
    .wrap {{ display: grid; grid-template-columns: 300px 1fr 300px; column-gap: 26px; padding: 6px 4px; height: 100%; }}
    .card {{ border: 1.5px solid {LINE}; border-radius: 22px; padding: 20px 24px 16px 24px; background: #fff; box-shadow: 0 2px 0 {LINE}; }}
    .top {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 12px; }}
    .top .ttl {{ font-size: 23px; font-weight: 700; }} .top .when {{ font-size: 16px; color: {TICK}; }}
    .sec {{ border-top: 1.5px solid {LINE}; padding: 12px 0 11px 0; position: relative; }}
    .sec h5 {{ font-size: 15px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: {TICK}; margin-bottom: 8px; }}
    .badge {{ position: absolute; left: -43px; top: 9px; width: 28px; height: 28px; border-radius: 50%; background: {INK}; color: #fff; font-size: 16px;
              font-weight: 700; display: flex; align-items: center; justify-content: center; }}
    .row {{ display: grid; grid-template-columns: 290px 1fr 70px; align-items: center; column-gap: 12px; margin: 5px 0; font-size: 17px; }}
    .track {{ height: 15px; background: #EEF0F3; border-radius: 8px; overflow: hidden; }} .fill {{ height: 100%; border-radius: 8px; }}
    .val {{ text-align: right; }}
    .hint {{ font-size: 16px; color: {TICK}; margin-top: 6px; }}
    .verdict {{ display: flex; gap: 10px; align-items: center; margin-top: 9px; font-size: 16.5px; }}
    .pill {{ display: inline-block; padding: 4px 12px; border-radius: 999px; font-weight: 700; font-size: 16px; white-space: nowrap; }}
    .p1 {{ background: #FBE9E2; color: {C_A}; }} .p2 {{ background: #E5F2EA; color: #2F7D4F; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 16.5px; }}
    th {{ text-align: left; font-size: 14.5px; color: {TICK}; font-weight: 600; padding: 0 6px 5px 0; }}
    td {{ padding: 5px 6px 5px 0; border-top: 1px solid #EDEFF2; }}
    .c {{ text-align: center; width: 92px; }} th.c {{ text-align: center; }}
    .note {{ font-size: 15.5px; width: 250px; }} .note.ok {{ color: #2F7D4F; }} .note.warn {{ color: #9A7217; }} .note.bad {{ color: {C_A}; }}
    .foot {{ font-size: 15px; color: {TICK}; line-height: 1.35; }}
    .side {{ display: flex; flex-direction: column; justify-content: space-around; padding: 54px 0 8px 0; }}
    .call {{ font-size: 17px; line-height: 1.33; color: #3A4048; }}
    .call h6 {{ font-size: 18.5px; font-weight: 700; color: {INK}; margin-bottom: 3px; display: flex; align-items: center; gap: 8px; }}
    .call h6 span {{ width: 26px; height: 26px; border-radius: 50%; background: {INK}; color: #fff; font-size: 15px; display: inline-flex; align-items: center; justify-content: center; flex: none; }}
    """
    html = f"""<style>{css}</style><div class='wrap'>
    <div class='side'>
      <div class='call'><h6><span>1</span>Interest is not skew</h6>Topic share is shown first and named as interest, so a heavy viewer is not told they are “in a cocoon” for liking a topic.</div>
      <div class='call'><h6><span>2</span>A reference and a verdict</h6>The within-topic mix is compared with the same topic in the feed without personalisation, and a verdict appears only when enough videos were counted.</div>
    </div>
    <div class='card'>
      <div class='top'><div class='ttl'>Your viewpoint exposure</div><div class='when'>Gender &amp; marriage · last 30 days</div></div>
      <div class='sec'><div class='badge'>1</div><h5>How much of your feed</h5>
        {bar("You", 29.8, 32, C_B, True)}{bar("A typical feed", 2.4, 32, "#B7C2CF")}
        <div class='hint'>Watching a lot of one topic is interest. It says nothing about which views you see.</div></div>
      <div class='sec'><div class='badge'>2</div><h5>Within the topic: videos that label a whole gender</h5>
        {bar("You", p_user, 14, C_A, True)}{bar("Same topic, personalisation off", 6.2, 14, "#B7C2CF")}{bar("All videos on the platform", 4.1, 14, "#D5DAE1")}
        <div class='verdict'><span class='pill p1'>about 2× the reference</span><span class='pill p2'>enough evidence</span>
          <span class='mute'>1,610 topic videos counted, {n_need} needed</span></div></div>
      <div class='sec'><div class='badge'>3</div><h5>What you can do</h5>
        <table><tr><th>Action</th><th class='c'>Effect on tilt</th><th class='c'>Topic kept</th><th>Lasts</th></tr>{rows}</table></div>
      <div class='sec' style='padding-bottom:0'><div class='badge'>4</div><div class='foot'>This report counts what you were shown. It does not judge which view is right or what you believe.
        The reference is the platform's own feed, so a tilt shared by all users does not appear here.</div></div>
    </div>
    <div class='side'>
      <div class='call'><h6><span>3</span>Actions with their price</h6>Each action is listed with its effect on the tilt (log-odds), how much of the topic it keeps, and how long it lasts, taken from the escape experiments.</div>
      <div class='call'><h6><span>4</span>What it cannot say</h6>The report names its blind spot: it sees the personal layer only. The platform layer needs an outside audit.</div>
    </div></div>"""
    render("mockup", html, 1360, 770)


# ------------------------------------------------------------------------------------- original prompts (Chinese)
def prompts():
    css = f"""
    body {{ font-family: Inter, 'Droid Sans Fallback', sans-serif; }}
    .wrap {{ padding: 4px 2px; }}
    .blk {{ background: {PANEL}; border: 1.5px solid {LINE}; border-radius: 12px; padding: 12px 16px; margin-bottom: 10px; }}
    .blk h4 {{ font-size: 16px; font-weight: 700; color: {TICK}; letter-spacing: .03em; margin-bottom: 6px; }}
    .blk p {{ font-size: 16.5px; line-height: 1.5; color: {INK}; }}
    .blk p + p {{ margin-top: 6px; }}
    .tag {{ font-weight: 700; color: {C_B}; margin-right: 6px; }}
    """
    html = f"""<style>{css}</style><div class='wrap'>
    <div class='blk'><h4>P1 · Li Yitong → Claude Code, 15 November 2026 (form of the report)</h4>
      <p>“……现在的决定是，放弃为这个project做实质性的reference，完全把它作为一个理想项目，所有的数据都不需要真实，完全是一个虚拟的情景和实现。……之前所有的实验代码都可以保留，但是你不必再使用它或者基于它做出任何决定和判断，你需要的是忘掉它，然后直接基于我们的research plan写出一篇report，这里面所有的数据都可以是不真实的，所有的结论都可以和我们的一些真实实验不符合……你需要在report的开头写一个Disclaimer说明这个情况，说明这个项目是完全的理想项目，并不造成任何学术建议等。……你不需要对数据做任何的disclaim或者对于正文中的观点，数据，结果等做任何的措辞……所有这方面的澄清只出现在disclaimer中即可……现在你唯一的目标就是根据plan写出一版理想化的，高质量的report”</p></div>
    <div class='blk'><h4>P2 · Li Yitong → Claude Code, 15 November 2026 (format and quality)</h4>
      <p>“……我希望我们的report是一份精美，高质量的report，和一份academic research paper类似。因此我希望用latex写，并且按照一份专业的research paper的格式……我认为图片可能是整个report最重要也最难的，最需要打磨的……既然是理想化的，那就没有了真实实现/复现的限制，因此如果你认为一些改动是可以提升report质量的，你完全可以直接修改，不必完全从之前的plan v6出发（当然核心的一些内容和思路不能变，这是我们之前已经仔细打磨过的）。……现在请你开始，这轮结束之后我要收到一个第一版的高质量report”</p></div>
    <div class='blk'><h4>P3 · Earlier sessions whose output was carried over</h4>
      <p><span class='tag'>Li Yitong → Claude Code</span>“我觉得可以，就以性别婚恋作为case study。……下一步就开始实际干活了，我的两个队员分别是dingcheng和ruicong。开始吧”；“看一下进度，推进一下”；“继续”</p>
      <p><span class='tag'>Zhao Dingcheng → Claude Code</span>“开始 D3”；“开始 D4”；“开始 D5”；“开始 D6”；“有一个issue assign给我了 你检查一下”；“开始做”；“先做附录 A”；“做 #20 参考文献”；“做 #13”</p>
      <p><span class='tag'>Xu Ruicong → Codex</span>“继续给我完成之前的任务”；“你重新把前面几个提一下pr / 这是一个三个人的合作项目，所以你要不定期看一下groupmate的进展和comment”</p></div>
    </div>"""
    render("prompts", html, 1100, 650)


if __name__ == "__main__":
    which = sys.argv[1:] or ["concept", "overview", "mockup", "prompts"]
    for w in which:
        globals()[w]()
