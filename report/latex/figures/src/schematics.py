"""Schematic figures drawn as HTML and printed to vector PDF with headless Chromium.

Constructed for an idealised teaching report (see ../../README.md).
Run:  python3 schematics.py [concept|overview]     # writes ../fig_<name>.pdf
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

sys.path.insert(0, str(Path(__file__).resolve().parent / "fonts"))
from pagella import ensure  # noqa: E402

ensure()

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
R = json.loads((SRC / "results.json").read_text())
CHROME = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")

C_A, C_B, C_O = "#D1603D", "#2B5C8A", "#D5DAE1"
INK, TICK, LINE, PANEL = "#1A1A1A", "#5F6670", "#DFE3E8", "#F6F7F9"

BASE_CSS = f"""
@font-face {{ font-family: PagellaFig; font-weight: 400; font-style: normal; src: url(fonts/cache/PagellaFig-regular.ttf); }}
@font-face {{ font-family: PagellaFig; font-weight: 400; font-style: italic; src: url(fonts/cache/PagellaFig-italic.ttf); }}
@font-face {{ font-family: PagellaFig; font-weight: 700; font-style: normal; src: url(fonts/cache/PagellaFig-bold.ttf); }}
@font-face {{ font-family: PagellaFig; font-weight: 700; font-style: italic; src: url(fonts/cache/PagellaFig-bolditalic.ttf); }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #fff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: PagellaFig, serif; color: {INK}; font-size: 21.5px; line-height: 1.3; }}
b, .b {{ font-weight: 700; }} .sb {{ font-weight: 600; }}
.mute {{ color: {TICK}; }} .a {{ color: {C_A}; }} .bl {{ color: {C_B}; }}
"""


def _chrome(args):
    return subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--run-all-compositor-stages-before-draw",
                           "--virtual-time-budget=4000", *args], capture_output=True, text=True, check=False)


def render(name: str, html: str, width: int, height: int = 0):
    """Print `html` to a one-page vector PDF `width` CSS px wide. Pass 1 measures the content height
    (at least `height`); pass 2 prints with a page of exactly that height."""
    def page(h):
        size = f"@page {{ size: {width}px {h}px; margin: 0; }}" if h else ""
        body = f"body {{ width: {width}px; min-height: {height}px; overflow: hidden; }}" if h else \
               f"body {{ width: {width}px; min-height: {height}px; }}"
        probe = "" if h else ("<script>window.addEventListener('load',()=>document.fonts.ready.then(()=>"
                              "document.title='H='+Math.ceil(document.body.getBoundingClientRect().height)));</script>")
        return (f"<!doctype html><html><head><meta charset='utf-8'><title></title><style>{size}{BASE_CSS}{body}</style>{probe}</head>"
                f"<body>{html}</body></html>")
    src = SRC / f".{name}.html"
    src.write_text(page(0))
    dom = _chrome(["--dump-dom", f"file://{src}"]).stdout
    import re
    m = re.search(r"<title>H=(\d+)</title>", dom)
    h = int(m.group(1)) + 2 if m else (height or 800)
    src.write_text(page(h))
    out = OUT / f"fig_{name}.pdf"
    _chrome(["--no-pdf-header-footer", f"--print-to-pdf={out}", f"file://{src}"])
    info = subprocess.run(["pdfinfo", str(out)], capture_output=True, text=True).stdout
    pages = [l.split()[-1] for l in info.splitlines() if l.startswith("Pages")]
    print("wrote", out.name, f"{width}x{h}px", "pages", pages)


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
    .who {{ font-size: 24px; font-weight: 700; margin-bottom: 1px; }}
    .sub {{ font-size: 19px; color: {TICK}; margin-bottom: 7px; }}
    .phone {{ background: {PANEL}; border: 1.5px solid {LINE}; border-radius: 18px; padding: 12px; }}
    .g {{ display: grid; grid-template-columns: repeat(10, 1fr); gap: 3.5px; }}
    .t {{ display: block; aspect-ratio: 1; border-radius: 4px; background: {C_O}; }}
    .t.b {{ background: {C_B}; }} .t.a {{ background: {C_A}; box-shadow: 0 0 0 2px #fff, 0 0 0 3.6px {C_A}; }}
    .legend {{ display: flex; justify-content: center; gap: 16px; margin: 10px 0 9px 0; font-size: 18.5px; color: {TICK}; white-space: nowrap; }}
    .legend i {{ display: inline-block; width: 13px; height: 13px; border-radius: 3px; margin-right: 5px; vertical-align: -1px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 20.5px; }}
    td {{ padding: 7px 5px; border-top: 1.5px solid {LINE}; vertical-align: middle; }}
    td.k {{ width: 50%; }} td.n {{ width: 12%; text-align: center; font-size: 26.5px; font-weight: 700; }}
    td.r {{ text-align: right; font-weight: 600; }}
    .small {{ font-size: 17.5px; color: {TICK}; display: block; margin-top: 1px; }}
    .pill {{ display: inline-block; padding: 3px 9px; border-radius: 999px; font-size: 18px; font-weight: 700; white-space: nowrap; }}
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
      <tr><td class='k'><b>Topic share</b><span class='small'>what topic-level checks see</span></td>
          <td class='n bl'>30%</td><td class='n a'>30%</td><td class='r'><span class='pill g1'>no difference</span></td></tr>
      <tr><td class='k'><b>Group-label share in the topic</b><span class='small'>what this study measures: skew <i>V</i></span></td>
          <td class='n bl'>6%</td><td class='n a'>13%</td><td class='r'><span class='pill g2'>odds ×{np.exp(v):.1f}</span></td></tr>
    </table></div>"""
    render("concept", html, 620)


# ------------------------------------------------------------------------------------- overview
def overview():
    css = f"""
    .wrap {{ display: grid; grid-template-columns: 250px 34px 262px 34px 1fr 34px 236px; align-items: stretch; padding: 4px; height: 100%; }}
    .col {{ display: flex; flex-direction: column; gap: 12px; }}
    .hd {{ font-size: 19px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: {TICK}; margin-bottom: 0; }}
    .box {{ background: {PANEL}; border: 1.5px solid {LINE}; border-radius: 14px; padding: 13px 15px; flex: 1; }}
    .box h4 {{ font-size: 23.5px; font-weight: 700; margin-bottom: 5px; }}
    .box p {{ font-size: 20.5px; color: #3A4048; line-height: 1.32; }}
    .box p + p {{ margin-top: 5px; }}
    .num {{ font-weight: 700; color: {INK}; }}
    .arrow {{ display: flex; align-items: center; justify-content: center; }}
    .arrow svg {{ width: 22px; height: 30px; }}
    .ev {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; flex: 1; }}
    .ev .box {{ padding: 12px 14px; }}
    .tag {{ display: inline-block; font-size: 17.5px; font-weight: 700; padding: 2px 9px; border-radius: 999px; margin-bottom: 6px; }}
    .t1 {{ background: #E3ECF5; color: {C_B}; }} .t2 {{ background: #FBE9E2; color: {C_A}; }}
    .t3 {{ background: #E3F1F1; color: #23797A; }} .t4 {{ background: #F5EDD9; color: #9A7217; }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }}
    .chip {{ font-size: 18px; font-weight: 600; padding: 3px 9px; border-radius: 7px; background: #fff; border: 1.5px solid {LINE}; }}
    .rq {{ border-left: 5px solid {C_B}; }} .rq.r2 {{ border-left-color: {C_A}; }} .rq.r3 {{ border-left-color: #7B6BB0; }} .rq.r4 {{ border-left-color: #23797A; }}
        .rq h4 {{ font-size: 22px; }} .rq p {{ font-size: 20px; }}
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
      <div class='box rq r2'><h4>RQ2 · Formation</h4><p>How much does personalisation add?</p></div>
      <div class='box rq r3'><h4>RQ3 · Detection</h4><p>Can a user notice it?</p></div>
      <div class='box rq r4'><h4>RQ4 · Escape</h4><p>What does each action cost?</p></div>
    </div></div>"""
    render("overview", html, 1360)


if __name__ == "__main__":
    which = sys.argv[1:] or ["concept", "overview"]
    for w in which:
        globals()[w]()
