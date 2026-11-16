"""Study-design figure (Figure 3): data -> labelling -> four kinds of evidence -> questions.

Run:  python3 arch.py          # writes ../fig_overview.pdf
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np

import model as M
from schematics import render

SRC = Path(__file__).resolve().parent
R = json.loads((SRC / "results.json").read_text())

INK, MUTE, HAIR = "#1A1A1A", "#6B7280", "#DDE1E6"
ROSE, BLUE, TEAL, GOLD, VIOLET = "#C0502E", "#2B5C8A", "#23797A", "#9A7217", "#7B6BB0"
RQC = {1: BLUE, 2: ROSE, 3: VIOLET, 4: TEAL}
KS = "#FF4906"  # Kuaishou orange


def logo(name, size=22, color=None):
    s = (SRC / "logos" / f"{name}.svg").read_text()
    s = re.sub(r'<title>.*?</title>', '', s)
    s = re.sub(r'\s(height|width)="[^"]*"', '', s, count=2)
    s = s.replace('style="flex:none;line-height:1"', '')
    s = s.replace("<svg", f"<svg width='{size}' height='{size}' style='vertical-align:middle'", 1)
    if color:
        s = s.replace('fill="currentColor"', f'fill="{color}"')
        if 'fill=' not in s.split('>')[0]:
            s = s.replace("<svg", f"<svg fill='{color}'", 1)
    return s


def pill(rq):
    return f"<span class='rq' style='background:{RQC[rq]}'>RQ{rq}</span>"


# --------------------------------------------------------------------------- mini visuals (SVG)
def svg_log_table():
    rows = [("u·0193", "婚礼vlog", [1, 1, 0, 0, 0]), ("u·0193", "女人只看彩礼", [1, 0, 1, 0, 0]),
            ("u·7731", "三分钟早餐", [0, 0, 0, 0, 1]), ("u·7731", "相亲实录", [1, 1, 0, 1, 0])]
    icons = ["▶", "♥", "✎", "↗", "⊘"]
    out = ["<svg viewBox='0 0 206 104' style='width:100%;height:auto'>",
           "<text x='4' y='12' class='th'>user</text><text x='50' y='12' class='th'>description</text>"]
    for j, ic in enumerate(icons):
        out.append(f"<text x='{146+j*13}' y='12' class='th' text-anchor='middle'>{ic}</text>")
    for i, (u, d, fb) in enumerate(rows):
        y = 32 + i * 20
        out.append(f"<line x1='0' x2='206' y1='{y-14}' y2='{y-14}' stroke='{HAIR}'/>")
        out.append(f"<text x='4' y='{y}' class='td'>{u}</text><text x='50' y='{y}' class='tdc'>{d}</text>")
        for j, v in enumerate(fb):
            col = (ROSE if j == 4 else BLUE) if v else "#D5D9DF"
            out.append(f"<circle cx='{146+j*13}' cy='{y-4}' r='{4.2 if v else 3}' fill='{col}'/>")
    out.append("</svg>")
    return "".join(out)


def svg_tokens():
    cols = ["#E3ECF5", "#E3ECF5", "#FBE3D9", "#E3ECF5", "#E3ECF5"]
    out = ["<svg viewBox='0 0 206 30' style='width:100%;height:auto'>"]
    for i in range(5):
        x = 2 + i * 41
        out.append(f"<rect x='{x}' y='4' width='37' height='22' rx='5' fill='{cols[i]}' stroke='#C9D4E1'/>"
                   f"<text x='{x+18.5}' y='19.5' class='tok' text-anchor='middle'>{'⟨a,b,c⟩' if i != 2 else '⟨d,e,f⟩'}</text>")
    out.append("</svg>")
    return "".join(out)


def svg_funnel():
    st = [("75.3 M", "all impressions", 1.0, "#C9D6E3"),
          ("9.6 M", "screened candidates", 0.86, "#B7CBDC"),
          ("5.9 M", "issue corpus", 0.73, "#9DBCD3"),
          ("1.77 M", "case corpus", 0.62, ROSE)]
    W, h, gap = 262, 28, 6
    out = [f"<svg viewBox='0 0 {W} {4*(h+gap)-gap}' style='width:100%;height:auto'>"]
    for i, (n, lab, w, c) in enumerate(st):
        bw = 112 * w
        y = i * (h + gap)
        out.append(f"<rect x='{(112-bw)/2:.1f}' y='{y}' width='{bw:.1f}' height='{h}' rx='5' fill='{c}'/>"
                   f"<text x='56' y='{y+19}' class='fn' text-anchor='middle' fill='{'#fff' if i == 3 else INK}'>{n}</text>"
                   f"<text x='120' y='{y+19}' class='fl'>{lab}</text>")
    out.append("</svg>")
    return "".join(out)


def svg_layers():
    ax = lambda p: 14 + (np.log(p / (1 - p)) - np.log(.03 / .97)) / (np.log(.16 / .84) - np.log(.03 / .97)) * 232  # noqa: E731
    pts = [(M.P_SUP, "supply", "4.1%", "#8C96A3", "end", 5), (M.P_BAR, "platform", "6.2%", BLUE, "start", -5), (0.127, "one user", "12.7%", ROSE, "middle", 0)]
    out = ["<svg viewBox='0 0 260 96' style='width:100%;height:auto'>",
           f"<line x1='10' x2='250' y1='58' y2='58' stroke='{MUTE}' stroke-width='1.4'/>"]
    xs = []
    for p, lab, v, c, anc, dx in pts:
        x = ax(p)
        xs.append(x)
        out.append(f"<circle cx='{x:.1f}' cy='58' r='6.5' fill='{c}' stroke='#fff' stroke-width='1.5'/>"
                   f"<text x='{x+dx:.1f}' y='43' class='vb' text-anchor='{anc}' fill='{c}'>{v}</text>"
                   f"<text x='{x+dx:.1f}' y='26' class='vl' text-anchor='{anc}' fill='{c}'>{lab}</text>")
    for a, b, lab, c, tx, anc in ((xs[0], xs[1], "platform layer", BLUE, xs[1] - 4, "end"),
                                  (xs[1], xs[2], "personal layer V", ROSE, xs[1] + 8, "start")):
        out.append(f"<path d='M{a+2:.1f},70 v6 H{b-2:.1f} v-6' fill='none' stroke='{c}' stroke-width='1.6'/>"
                   f"<text x='{tx:.1f}' y='93' class='vl' text-anchor='{anc}' fill='{c}'>{lab}</text>")
    out.append("</svg>")
    return "".join(out)


def svg_probe():
    """History tokens grouped by field -> OneRec -> scores over candidates."""
    out = ["<svg viewBox='0 0 330 112' style='width:100%;height:auto'>"]
    fields = [("watched", ["#DCE6F0"] * 4 + [ROSE] * 2), ("liked", ["#DCE6F0"] * 3), ("not interested", ["#DCE6F0"] * 2)]
    y = 10
    for name, cs in fields:
        out.append(f"<text x='0' y='{y+11}' class='fl2'>{name}</text>")
        for i, c in enumerate(cs):
            out.append(f"<rect x='{92+i*12}' y='{y+1}' width='10' height='13' rx='2.5' fill='{c}'/>")
        y += 22
    out.append(f"<text x='92' y='{y+12}' class='fl2' fill='{ROSE}'>+k injected</text>")
    # model block
    out.append(f"<path d='M172,{50} h14' stroke='{MUTE}' stroke-width='1.6' marker-end='url(#ah)'/>")
    out.append(f"<rect x='190' y='14' width='54' height='76' rx='9' fill='#fff' stroke='{INK}' stroke-width='1.6'/>")
    for i in range(4):
        out.append(f"<rect x='198' y='{24+i*14}' width='38' height='9' rx='2' fill='{['#EADFD8','#E3ECF5','#EADFD8','#E3ECF5'][i]}'/>")
    out.append(f"<text x='217' y='106' class='fl2' text-anchor='middle'>OneRec</text>")
    out.append(f"<path d='M246,50 h12' stroke='{MUTE}' stroke-width='1.6' marker-end='url(#ah)'/>")
    # candidate scores
    vals = [(0.55, "#9DBCD3"), (0.42, "#9DBCD3"), (0.86, ROSE), (0.33, "#9DBCD3"), (0.78, ROSE), (0.25, "#C9CED6")]
    for i, (v, c) in enumerate(vals):
        out.append(f"<rect x='{266+i*10}' y='{86-v*64:.1f}' width='7' height='{v*64:.1f}' rx='1.5' fill='{c}'/>")
    out.append(f"<line x1='264' x2='328' y1='86.5' y2='86.5' stroke='{MUTE}'/>"
               f"<text x='296' y='106' class='fl2' text-anchor='middle'>scores</text>")
    out.append("<defs><marker id='ah' markerWidth='7' markerHeight='7' refX='5' refY='3.5' orient='auto'>"
               f"<path d='M0,0 L7,3.5 L0,7 z' fill='{MUTE}'/></marker></defs></svg>")
    return "".join(out)


def svg_loop():
    """User -> finish/skip -> profile -> recommender -> feed -> user."""
    out = ["<svg viewBox='0 0 300 130' style='width:100%;height:auto'>",
           "<defs><marker id='ah2' markerWidth='7' markerHeight='7' refX='5' refY='3.5' orient='auto'>"
           f"<path d='M0,0 L7,3.5 L0,7 z' fill='{TEAL}'/></marker></defs>"]
    nodes = [(52, 24, "user", "likes φ, θ"), (248, 24, "profile", "200 finished"),
             (248, 104, "recommender", "from probes"), (52, 104, "feed", "180 a day")]
    for i, (x, y, t, sub) in enumerate(nodes):
        out.append(f"<rect x='{x-50}' y='{y-18}' width='100' height='36' rx='9' fill='#fff' stroke='{TEAL}' stroke-width='1.6'/>"
                   f"<text x='{x}' y='{y-1}' class='nd' text-anchor='middle'>{t}</text>"
                   f"<text x='{x}' y='{y+11}' class='ns' text-anchor='middle'>{sub}</text>")
    arr = [("M104,24 H194", "finish / skip", 150, 15), ("M248,44 V84", "", 0, 0), ("M196,104 H106", "softmax", 150, 96), ("M52,84 V44", "", 0, 0)]
    for d, lab, lx, ly in arr:
        out.append(f"<path d='{d}' stroke='{TEAL}' stroke-width='1.6' fill='none' marker-end='url(#ah2)'/>")
        if lab:
            out.append(f"<text x='{lx}' y='{ly}' class='ns' text-anchor='middle' fill='{TEAL}'>{lab}</text>")
    out.append(f"<text x='150' y='70' class='ns' text-anchor='middle' fill='{TEAL}'>repeat for 128 days</text>")
    out.append("</svg>")
    return "".join(out)


def svg_bound():
    """Two samples and their overlapping sampling distributions."""
    out = ["<svg viewBox='0 0 290 112' style='width:100%;height:auto'>"]
    xs = np.linspace(0, 1, 120)
    for mu, c, lab, dx, anc in ((0.30, "#8C96A3", "reference", -6, "end"), (0.52, VIOLET, "your feed", 6, "start")):
        y = np.exp(-0.5 * ((xs - mu) / 0.09) ** 2)
        pts = " ".join(f"{20+x*250:.1f},{88-v*62:.1f}" for x, v in zip(xs, y))
        out.append(f"<polyline points='{pts}' fill='none' stroke='{c}' stroke-width='2'/>"
                   f"<text x='{20+mu*250+dx:.1f}' y='22' class='ns' text-anchor='{anc}' fill='{c}'>{lab}</text>")
    out.append(f"<text x='272' y='46' class='nd' text-anchor='end' fill='{VIOLET}'>n ≈ 490</text><text x='272' y='60' class='ns' text-anchor='end'>per sample</text>")
    out.append(f"<line x1='14' x2='276' y1='88.5' y2='88.5' stroke='{MUTE}'/>"
               f"<text x='145' y='108' class='ns' text-anchor='middle'>observed share of group labels</text>")
    out.append("</svg>")
    return "".join(out)


def svg_crosscheck():
    """Two reference models label the same videos; agreement grid."""
    a = [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
    b = [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0]
    out = ["<svg viewBox='0 0 236 70' style='width:100%;height:auto'>"]
    for r, (row, y) in enumerate(((a, 8), (b, 36))):
        for i, v in enumerate(row):
            out.append(f"<rect x='{40+i*16}' y='{y}' width='13' height='13' rx='2.5' fill='{ROSE if v else '#DCE3EA'}'/>")
    out.append(f"<rect x='{40+5*16-2}' y='4' width='17' height='49' rx='4' fill='none' stroke='{INK}' stroke-width='1.3' stroke-dasharray='3 2'/>")
    out.append(f"<text x='{40+5*16+6.5}' y='66' class='ns' text-anchor='middle'>disagree</text>")
    out.append("</svg>")
    return "".join(out)


def rq_icon(k, col):
    p = {1: "<circle cx='12' cy='12' r='8'/><path d='M12 4v8l6 5'/>",
         2: "<path d='M3 18l6-6 4 4 8-9'/><path d='M15 7h6v6'/>",
         3: "<circle cx='10.5' cy='10.5' r='6'/><path d='M15 15l6 6'/>",
         4: "<path d='M10 4H5v16h5'/><path d='M14 8l4 4-4 4M18 12H9'/>"}[k]
    return (f"<svg width='26' height='26' viewBox='0 0 24 24' fill='none' stroke='{col}' stroke-width='2' "
            f"stroke-linecap='round' stroke-linejoin='round'>{p}</svg>")


# --------------------------------------------------------------------------- figure
def arch():
    css = f"""
    @font-face {{ font-family: NotoSC; font-weight: 400; src: url(fonts/cache/NotoSerifSC-Regular.ttf); }}
    body {{ font-family: PagellaFig, NotoSC, serif; color: {INK}; }}
    .wrap {{ display: grid; grid-template-columns: 236px 290px 1fr 196px; column-gap: 14px; padding: 2px; align-items: stretch; }}
    .stage {{ border-radius: 14px; padding: 10px 11px 11px 11px; position: relative; }}
    .s1 {{ background: #EEF3F8; }} .s2 {{ background: #EEF5F0; }} .s3 {{ background: #FBF5EF; }} .s4 {{ background: #F5F6F8; }}
    .sh {{ font-size: 17px; letter-spacing: .18em; text-transform: uppercase; color: {MUTE}; margin: 0 0 7px 2px; }}
    .sh b {{ color: {INK}; letter-spacing: .1em; }}
    .box {{ background: #fff; border: 1.3px solid {HAIR}; border-radius: 10px; padding: 8px 9px; margin-bottom: 9px; }}
    .box:last-child {{ margin-bottom: 0; }}
    .bt {{ font-size: 21px; font-weight: 700; display: flex; align-items: center; gap: 7px; line-height: 1.1; }}
    .bs {{ font-size: 17.5px; color: #3A4048; line-height: 1.22; margin-top: 3px; }}
    .num {{ font-weight: 700; }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 4px; margin-top: 6px; }}
    .chip {{ font-size: 15.5px; padding: 1px 7px; border-radius: 6px; border: 1.2px solid; background: #fff; }}
    .ev {{ display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 9px; height: calc(100% - 26px); }}
    .ec {{ background: #fff; border: 1.3px solid {HAIR}; border-radius: 10px; padding: 8px 10px 6px 10px; display: flex; flex-direction: column; }}
    .tag {{ font-size: 14px; letter-spacing: .14em; text-transform: uppercase; font-weight: 700; }}
    .et {{ font-size: 21.5px; font-weight: 700; line-height: 1.1; margin: 1px 0 1px 0; display: flex; align-items: center; gap: 6px; }}
    .es {{ font-size: 17px; color: #3A4048; line-height: 1.2; }}
    .vis {{ flex: 1; display: flex; align-items: center; justify-content: center; padding: 4px 6px; }}
    .foot {{ display: flex; justify-content: space-between; align-items: center; font-size: 15.5px; color: {MUTE}; }}
    .rq {{ color: #fff; font-size: 14px; padding: 1px 6px; border-radius: 5px; margin-left: 3px; font-weight: 700; letter-spacing: .04em; }}
    .q {{ border-left: 5px solid; background: #fff; border-radius: 8px; padding: 9px 9px; margin-bottom: 10px; display: flex; gap: 9px; align-items: center; }}
    .q small {{ display: block; font-size: 15px; color: #3A4048; line-height: 1.15; }}
    .big2 {{ font-size: 17.5px; }} .mini {{ font-size: 15px; color: #3A4048; margin-top: 4px; line-height: 1.15; }}
    .lrow {{ display: flex; align-items: center; gap: 5px; }} .arw {{ color: #9AA1AB; font-size: 20px; }}
    .thumb {{ width: 42px; height: 56px; object-fit: cover; border-radius: 6px; outline: 2.5px solid {ROSE}; }}
    .checks div {{ font-size: 14.5px; border: 1.3px solid {BLUE}; color: {BLUE}; border-radius: 5px; padding: 0 6px; margin: 2px 0; white-space: nowrap; }}
    .checks div.r {{ border-color: {ROSE}; color: {ROSE}; }} .checks div.ck {{ border: none; color: #3A4048; font-size: 13.5px; padding: 0 2px; line-height: 1.2; }}
    .q:last-child {{ margin-bottom: 0; }}
    .q h4 {{ font-size: 15px; margin: 0; letter-spacing: .12em; color: #6B7280; }}
    .q p {{ font-size: 20px; font-weight: 700; color: #1A1A1A; color: #3A4048; line-height: 1.2; margin: 0; }}
    .arr {{ position: absolute; top: 50%; right: -15px; width: 16px; height: 26px; margin-top: -13px; z-index: 3; }}
    svg text {{ font-family: PagellaFig, serif; }}
    .th {{ font-size: 13px; fill: {MUTE}; }} .td {{ font-size: 13px; fill: {MUTE}; }} .tdc {{ font-size: 13.5px; font-family: NotoSC, serif; fill: {INK}; }}
    .tok {{ font-size: 12.5px; fill: #3A4048; }}
    .fn {{ font-size: 17px; font-weight: 700; }} .fl {{ font-size: 16px; fill: #3A4048; }}
    .vb {{ font-size: 16px; font-weight: 700; }} .vl {{ font-size: 15.5px; }}
    .fl2 {{ font-size: 12.5px; fill: #3A4048; }}
    .nd {{ font-size: 14px; font-weight: 700; fill: {INK}; }} .ns {{ font-size: 12.5px; fill: #3A4048; }}
    """
    chev = ("<svg class='arr' viewBox='0 0 16 26'><path d='M3 3l10 10-10 10' fill='none' stroke='#9AA1AB' "
            "stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'/></svg>")
    stack = "".join(
        f"<img src='covers/{n}.jpg' style='position:absolute;left:{x}px;top:{y}px;width:62px;height:83px;object-fit:cover;"
        f"border-radius:7px;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.18);transform:rotate({r}deg);"
        f"{'outline:2.5px solid ' + ROSE + ';' if n == 'vlog_man' else ''}'>"
        for n, x, y, r in (("breakfast", 4, 6, -7), ("wedding", 52, 0, 2), ("vlog_man", 102, 8, 8), ("football", 150, 2, -3)))
    data = f"""<div class='stage s1'>{chev}<div class='sh'>① <b>Data</b></div>
      <div class='box'><div class='bt'>{logo('kuaishou', 22, KS)} RecIF logs</div>
        <div style='position:relative;height:96px;margin:6px 0 2px 0'>{stack}</div>
        <div class='big2'><b>160k</b> users · <b>75M</b> views</div>
        <div style='margin-top:4px'>{svg_log_table()}</div></div>
      <div class='box'><div class='bt'>{logo('kuaishou', 22, KS)} OneRec-1.7B</div>
        <div style='margin-top:6px'>{svg_tokens()}</div>
        <div class='mini'>history as semantic IDs → scores for any video</div></div></div>"""
    lab = f"""<div class='stage s2'>{chev}<div class='sh'>② <b>Labelling</b></div>
      <div class='box'>{svg_funnel()}</div>
      <div class='box'><div class='lrow'><img src='covers/vlog_man.jpg' class='thumb'>
          <span class='arw'>→</span>{logo('qwen', 34)}<span class='arw'>→</span>
          <div class='checks'><div>marriage</div><div class='r'>group label</div>
          <div class='ck'>target ✓ trait ✓<br>scope ✓ voice ✓</div></div></div></div>
      <div class='box'><div class='lrow' style='gap:8px'>{logo('deepseek', 28)}{logo('openai', 25, '#111')}
          <div style='flex:1'>{svg_crosscheck()}</div></div>
        <div class='mini' style='text-align:center'>1,200 relabelled · κ = 0.78 · recall 0.79</div></div></div>"""
    ev = f"""<div class='stage s3'>{chev}<div class='sh'>③ <b>Four kinds of evidence</b></div><div class='ev'>
      <div class='ec'><div class='tag' style='color:{BLUE}'>Observational</div><div class='et'>Logs</div>
        <div class='vis'>{svg_layers()}</div>
        <div class='foot'><span>§4.3, §5.1</span><span>{pill(1)}{pill(2)}</span></div></div>
      <div class='ec'><div class='tag' style='color:{ROSE}'>Interventional</div><div class='et'>Recommender probes {logo('kuaishou', 18, KS)}</div>
        <div class='vis'>{svg_probe()}</div>
        <div class='foot'><span>§5.2</span><span>{pill(2)}{pill(4)}</span></div></div>
      <div class='ec'><div class='tag' style='color:{TEAL}'>Mechanistic</div><div class='et'>Transparent simulation</div>
        <div class='vis'>{svg_loop()}</div>
        <div class='foot'><span>§5.3, §7</span><span>{pill(2)}{pill(4)}</span></div></div>
      <div class='ec'><div class='tag' style='color:{GOLD}'>Analytic</div><div class='et'>Detection bound</div>
        <div class='vis'>{svg_bound()}</div>
        <div class='foot'><span>§3.4, §6</span><span>{pill(3)}</span></div></div></div></div>"""
    qs = f"""<div class='stage s4'><div class='sh'>④ <b>Questions</b></div>""" + "".join(
        f"<div class='q' style='border-color:{RQC[k]}'>{rq_icon(k, RQC[k])}<div><h4>RQ{k}</h4><p>{t}</p><small>{d}</small></div></div>"
        for k, t, d in ((1, "Prevalence", "how common, how amplified"), (2, "Formation", "how much, how fast"),
                        (3, "Detection", "can a user notice"), (4, "Escape", "what it costs"))) + "</div>"
    html = f"<style>{css}</style><div class='wrap'>{data}{lab}{ev}{qs}</div>"
    render("overview", html, 1360)


if __name__ == "__main__":
    arch()
