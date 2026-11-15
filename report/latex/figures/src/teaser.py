"""Page-1 overview figure: one user's 128 days across the four research questions.

Run:  python3 teaser.py          # writes ../fig_teaser.pdf
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import model as M
from schematics import render, BASE_CSS  # noqa: F401  (render prints HTML to PDF)

SRC = Path(__file__).resolve().parent
R = json.loads((SRC / "results.json").read_text())

INK, MUTE, HAIR = "#1A1A1A", "#6B7280", "#D9DDE3"
ROSE, BLUE, VIOLET, TEAL, GOLD, SLATE = "#C0502E", "#2B5C8A", "#7B6BB0", "#23797A", "#B8892B", "#5F7A99"
RQ = {1: ("#2B5C8A", "Prevalence"), 2: ("#C0502E", "Formation"), 3: ("#7B6BB0", "Detection"), 4: ("#23797A", "Escape")}

# --------------------------------------------------------------------------- small pictograms (24x24 line icons)
ICON = {
    "rings": '<circle cx="9" cy="13" r="5.5"/><circle cx="15" cy="13" r="5.5"/><path d="M7 6.5l2-2.5 2 2.5"/>',
    "couple": '<circle cx="8.5" cy="7" r="2.6"/><circle cx="15.5" cy="7" r="2.6"/><path d="M4 20c0-4 2-7 4.5-7s4.5 3 4.5 7M11 20c0-4 2-7 4.5-7S20 16 20 20"/>',
    "coin": '<circle cx="12" cy="12" r="7.5"/><path d="M9 9l3 3 3-3M12 12v5M9.5 13.5h5"/>',
    "talk": '<path d="M4 6h11v7H9l-3 3v-3H4z"/><path d="M15 9h5v7h-2v3l-3-3h-3v-2"/>',
    "bowl": '<path d="M3 12h18a9 6 0 0 1-18 0z"/><path d="M8 9c0-2 1-2 1-4M12 9c0-2 1-2 1-4M16 9c0-2 1-2 1-4"/>',
    "ball": '<circle cx="12" cy="12" r="8"/><path d="M12 7l3.8 2.8-1.4 4.4H9.6L8.2 9.8z"/>',
    "plane": '<path d="M3 13l18-6-6 13-3-5z"/><path d="M12 15l3-8"/>',
    "cat": '<path d="M5 9V4l4 3h6l4-3v5a7 7 0 0 1-14 0z"/><circle cx="9.5" cy="11" r=".9"/><circle cx="14.5" cy="11" r=".9"/>',
    "book": '<path d="M4 5h7v14H4zM13 5h7v14h-7z"/>',
    "baby": '<circle cx="12" cy="9" r="4.5"/><path d="M6 21c0-4 3-6 6-6s6 2 6 6"/>',
}


def icon(name, col, size=26):
    return (f"<svg viewBox='0 0 24 24' width='{size}' height='{size}' fill='none' stroke='{col}' stroke-width='1.6' "
            f"stroke-linecap='round' stroke-linejoin='round'>{ICON[name]}</svg>")


KIND = {  # cover gradient, icon colour, overlay text colour
    "other": ("linear-gradient(160deg,#EEF0F2,#D9DEE4)", "#8C96A3", "#5B6573"),
    "food": ("linear-gradient(160deg,#F6EEE3,#E8D7C2)", "#B38A5C", "#7A5A36"),
    "sport": ("linear-gradient(160deg,#E7F0EA,#CFE0D5)", "#5E8F70", "#3F6B50"),
    "issue": ("linear-gradient(160deg,#E6EEF6,#C9D9EA)", "#4D7AA6", "#24496E"),
    "label": ("linear-gradient(160deg,#FBEDE7,#F2D3C6)", "#C0502E", "#8F3519"),
}


def card(kind, cn, en, photo, likes="1.2w"):
    """A feed card with a photographic 3:4 cover (generated, see covers/) and Kuaishou-style title overlay."""
    ring = f"box-shadow:0 0 0 2.6px {ROSE};" if kind == "label" else ""
    return (f"<div class='card' style='{ring}'><div class='cov' style=\"background-image:url(covers/{photo}.jpg)\">"
            f"<div class='ov'>{cn}<span class='lk'>♥ {likes}</span></div></div>"
            f"<div class='cap'>{en}</div></div>")


def phone(inner, foot=""):
    return (f"<div class='phone'><div class='notch'></div><div class='sb'><span>9:41</span><span class='sbr'>"
            f"<i></i><i></i><i></i></span></div><div class='tabs'><span>Following</span><b>For You</b><span>Nearby</span></div>"
            f"<div class='scr'>{inner}</div>{foot}</div>")


def grid(cards):
    return "<div class='grid'>" + "".join(cards) + "</div>"


def badge(n, rq):
    return f"<span class='bdg' style='background:{RQ[rq][0]}'>{n}</span>"


def note(n, rq, big, html, ev):
    return (f"<div class='note'>{badge(n, rq)}<div><div class='big' style='color:{RQ[rq][0]}'>{big}</div><div class='nt'>{html}</div>"
            f"<div class='ev' style='color:{RQ[rq][0]};border-color:{RQ[rq][0]}'>{ev}</div></div></div>")


# --------------------------------------------------------------------------- right panel: one user's trajectory (SVG)
def chart(W=430, H=640):
    F = R["formation"]["users"]["fan_strong"]
    E = R["escape"]["strategies"]
    d0 = R["formation"]["n_form"] / M.VIDEOS_PER_DAY
    share = lambda v: 100 * M.expit(M.logit(M.P_BAR) + np.asarray(v))  # noqa: E731
    x0, x1, xmax = 60, W - 18, 130.0
    yA0, yA1, ymax = 40, 330, 16.0          # share panel (top, bottom)
    yB0, yB1, mmax = 384, 470, 34.0         # topic panel
    X = lambda d: x0 + (x1 - x0) * np.asarray(d) / xmax  # noqa: E731
    YA = lambda p: yA1 - (yA1 - yA0) * np.asarray(p) / ymax  # noqa: E731
    YB = lambda p: yB1 - (yB1 - yB0) * np.asarray(p) / mmax  # noqa: E731

    def path(xs, ys):
        return "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in zip(xs, ys))

    def smooth(v, k=7):
        v = np.asarray(v, float)
        out = np.convolve(v, np.ones(k) / k, mode="same")
        out[: k // 2], out[-(k // 2):] = v[: k // 2], v[-(k // 2):]
        return out

    s = []
    act0, act1 = d0, d0 + R["escape"]["n_act"] / M.VIDEOS_PER_DAY
    s.append(f"<rect x='{X(act0):.1f}' y='{yA0-14}' width='{X(act1)-X(act0):.1f}' height='{yB1-yA0+14}' fill='#F2F0EB'/>")
    s.append(f"<text x='{X(act0)-4:.1f}' y='{yA0-20}' class='ax' text-anchor='end'>acting</text>")
    s.append(f"<text x='{X(act1)+4:.1f}' y='{yA0-20}' class='ax'>stopped</text>")
    # grid and axes
    for p in (0, 4, 8, 12, 16):
        s.append(f"<line x1='{x0}' x2='{x1}' y1='{YA(p):.1f}' y2='{YA(p):.1f}' class='gl'/>"
                 f"<text x='{x0-8}' y='{YA(p)+5:.1f}' class='ax' text-anchor='end'>{p}%</text>")
    for m in (0, 15, 30):
        s.append(f"<line x1='{x0}' x2='{x1}' y1='{YB(m):.1f}' y2='{YB(m):.1f}' class='gl'/>"
                 f"<text x='{x0-8}' y='{YB(m)+5:.1f}' class='ax' text-anchor='end'>{m}%</text>")
    for d in (0, 30, 60, 90, 120):
        s.append(f"<text x='{X(d):.1f}' y='{yB1+22}' class='ax' text-anchor='middle'>{d}</text>")
    s.append(f"<text x='{(x0+x1)/2:.1f}' y='{yB1+46}' class='axl' text-anchor='middle'>days of use</text>")
    s.append(f"<text transform='translate(14,{(yA0+yA1)/2:.0f}) rotate(-90)' class='axl' text-anchor='middle'>group labels among issue videos</text>")
    s.append(f"<text transform='translate(14,{(yB0+yB1)/2:.0f}) rotate(-90)' class='axl' text-anchor='middle'>topic share</text>")
    # reference lines
    for p, lab, col in ((100 * M.P_BAR, "platform average 6.2%", BLUE), (100 * M.P_SUP, "supply 4.1%", "#8C96A3")):
        s.append(f"<line x1='{x0}' x2='{x1}' y1='{YA(p):.1f}' y2='{YA(p):.1f}' stroke='{col}' stroke-width='1.6' stroke-dasharray='5 4'/>")
    s.append(f"<text x='{X(1.5):.1f}' y='{YA(100*M.P_BAR)+20:.1f}' class='ref' fill='{BLUE}'>platform 6.2%</text>")
    s.append(f"<text x='{X(1.5):.1f}' y='{YA(100*M.P_SUP)+20:.1f}' class='ref' fill='#7C8796'>supply 4.1%</text>")
    # formation
    tf = np.array(F["t"]) / M.VIDEOS_PER_DAY
    sf = share(F["V"])
    # one simulated user (thin): formation, then carrying on
    one = M.simulate(0.8, 2.0, n_form=R["formation"]["n_form"], n_act=R["escape"]["n_act"], n_after=R["escape"]["n_after"],
                     strategy="S0", seeds=1, rng_seed=14, record_every=100)
    t1 = np.array(one["t"]) / M.VIDEOS_PER_DAY
    s.append(f"<path d='{path(X(t1), YA(share(one['V'][:, 0])))}' fill='none' stroke='{ROSE}' stroke-width='1.2' stroke-opacity='.55' stroke-linejoin='round'/>")
    s.append(f"<path d='{path(X(t1), YB(100 * one['m'][:, 0]))}' fill='none' stroke='{ROSE}' stroke-width='1.1' stroke-opacity='.5'/>")
    s.append(f"<path d='{path(X(tf), YA(sf))}' fill='none' stroke='{ROSE}' stroke-width='3.2' stroke-linejoin='round'/>")
    mf = 100 * np.array(F["m"])
    s.append(f"<path d='{path(X(tf), YB(mf))}' fill='none' stroke='{ROSE}' stroke-width='3' />")
    # layer braces at the branching point
    bx = X(d0) - 16
    for lo, hi, lab, col, dy in ((100 * M.P_SUP, 100 * M.P_BAR, "platform layer", BLUE, 0),
                                 (100 * M.P_BAR, float(sf[-8:].mean()), "personal layer", ROSE, 0)):
        a, b = YA(lo) - 1.5, YA(hi) + 1.5
        s.append(f"<path d='M{bx+7:.1f},{a:.1f} H{bx:.1f} V{b:.1f} H{bx+7:.1f}' fill='none' stroke='{col}' stroke-width='1.6'/>")
        s.append(f"<text x='{bx-6:.1f}' y='{(a+b)/2+5:.1f}' class='brc' fill='{col}' text-anchor='end'>{lab}</text>")
    # strategies after the branch
    lines = [("S0", "carry on", ROSE, ""), ("S2", "“not interested”", GOLD, "6 4"), ("S1", "scroll past", TEAL, ""),
             ("S11", "classifier filter", VIOLET, ""), ("S8", "personalisation off", SLATE, "2 3")]
    ends = {}
    for key, lab, col, dash in lines:
        e = E[key]
        t = d0 + np.array(e["t"]) / M.VIDEOS_PER_DAY
        sel = t >= d0 - 0.01
        v = np.array(e["V"])[sel]
        tt = t[sel]
        sh = share(v)
        w = 3.2 if key == "S0" else 2.6
        s.append(f"<path d='{path(X(tt), YA(sh))}' fill='none' stroke='{col}' stroke-width='{w}' stroke-dasharray='{dash}' stroke-linejoin='round'/>")
        mm = 100 * np.array(e["m"])[sel]
        s.append(f"<path d='{path(X(tt), YB(mm))}' fill='none' stroke='{col}' stroke-width='2.2' stroke-dasharray='{dash}'/>")
        ends[key] = (float(sh[-1]), lab, col)
    # end labels, spread so they do not collide
    order = sorted(ends.items(), key=lambda kv: -kv[1][0])
    ys, last = [], -1e9
    for key, (p, lab, col) in order:
        y = max(YA(p) + 5, last + 21)
        ys.append((y, lab, col))
        last = y
    # legend under the chart, two columns
    for i, (key, lab, col, dash) in enumerate(lines):
        lx, ly = x0 + (i % 2) * 190, yB1 + 74 + (i // 2) * 26
        s.append(f"<line x1='{lx}' x2='{lx+30}' y1='{ly-5}' y2='{ly-5}' stroke='{col}' stroke-width='3' stroke-dasharray='{dash}'/>"
                 f"<text x='{lx+38}' y='{ly}' class='lbl'>{lab}</text>")
    s.append(f"<text x='{X(87):.1f}' y='{YB(6)+5:.1f}' class='ann' fill='{SLATE}' text-anchor='end'>topic gone →</text>")
    # formation annotation
    s.append(f"<text x='{X(3):.1f}' y='{YA(14.6):.1f}' class='ann' fill='{ROSE}'>fans who finish</text>"
             f"<text x='{X(3):.1f}' y='{YA(14.6)+20:.1f}' class='ann' fill='{ROSE}'>group-label videos</text>")
    s.append(f"<text x='{x0}' y='{yB1+154}' class='lbl' fill='{MUTE}'>thick: mean of 400 fans · thin: one fan</text>")
    return (f"<svg width='{W}' height='{H}' viewBox='0 0 {W} {H}' xmlns='http://www.w3.org/2000/svg'>"
            + "".join(s) + "</svg>")


# --------------------------------------------------------------------------- figure
def teaser():
    F = R["formation"]["users"]["fan_strong"]
    pl = R["case"]["platform_layer"]
    css = f"""
    @font-face {{ font-family: NotoSC; font-weight: 400; src: url(fonts/cache/NotoSerifSC-Regular.ttf); }}
    @font-face {{ font-family: NotoSC; font-weight: 700; src: url(fonts/cache/NotoSerifSC-Bold.ttf); }}
    body {{ font-family: PagellaFig, NotoSC, serif; color: {INK}; }}
    .wrap {{ display: grid; grid-template-columns: 1fr 430px; column-gap: 24px; padding: 4px 6px 2px 4px; }}
    .lt {{ display: grid; grid-template-columns: repeat(4, 1fr); column-gap: 20px; position: relative; }}
    .pz {{ zoom: 0.722; width: 256px; position: relative; }}
    .kick {{ font-size: 15.5px; letter-spacing: .22em; text-transform: uppercase; color: {MUTE}; }}
    .hd {{ font-style: italic; font-size: 25px; line-height: 1.1; margin: 1px 0 9px 0; white-space: nowrap; }}
    .phone {{ position: relative; width: 100%; aspect-ratio: 9/18.2; border: 2.6px solid #24272C; border-radius: 30px;
             background: #fff; overflow: hidden; box-shadow: 0 1px 0 #24272C; }}
    .notch {{ position: absolute; top: 7px; left: 50%; width: 56px; height: 15px; margin-left: -28px; border-radius: 9px; background: #24272C; }}
    .sb {{ display: flex; justify-content: space-between; padding: 8px 20px 0 22px; font-size: 13px; font-weight: 700; height: 26px; }}
    .sbr i {{ display: inline-block; width: 4px; margin-left: 2px; background: #24272C; border-radius: 1px; }}
    .sbr i:nth-child(1) {{ height: 6px; }} .sbr i:nth-child(2) {{ height: 8px; }} .sbr i:nth-child(3) {{ height: 10px; }}
    .tabs {{ display: flex; justify-content: center; gap: 16px; font-size: 13.5px; color: #9AA1AB; padding: 6px 0 8px 0;
             border-bottom: 1px solid #EEF0F2; }}
    .tabs b {{ color: {INK}; font-weight: 700; border-bottom: 2px solid {INK}; padding-bottom: 1px; }}
    .scr {{ padding: 9px 9px; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 9px; }}
    .card {{ border-radius: 9px; overflow: hidden; background: #fff; border: 1px solid #ECEEF1; }}
    .cov {{ position: relative; aspect-ratio: 3/4; background-size: cover; background-position: center; display: flex; align-items: flex-end; }}
    .ico {{ opacity: .95; }}
    .ov {{ width: 100%; font-family: NotoSC, serif; font-weight: 700; font-size: 14px; line-height: 1.15; color: #fff; padding: 22px 7px 5px 7px; white-space: nowrap; overflow: hidden;
            background: linear-gradient(to top, rgba(0,0,0,.62), rgba(0,0,0,0)); text-shadow: 0 1px 2px rgba(0,0,0,.5); }}
    .ctag {{ position: absolute; top: 7px; right: 7px; color: #fff; font-size: 11.5px; padding: 1px 6px; border-radius: 7px; letter-spacing: .04em; }}
    .cap {{ font-size: 11.5px; line-height: 1.16; padding: 4px 6px 4px 6px; color: #3A4048; height: 48px; overflow: hidden; position: relative; }}
    .lk {{ display: block; font-family: PagellaFig, serif; font-weight: 400; font-size: 10.5px; opacity: .9; margin-top: 1px; }}
    .note {{ display: grid; grid-template-columns: 24px 1fr; column-gap: 7px; margin-top: 12px; }}
    .bdg {{ width: 22px; height: 22px; border-radius: 50%; color: #fff; font-size: 14.5px; font-weight: 700;
            display: inline-flex; align-items: center; justify-content: center; margin-top: 1px; }}
    .big {{ font-size: 30px; line-height: 1; font-weight: 700; letter-spacing: -.01em; }}
    .nt {{ font-size: 17.5px; line-height: 1.18; margin-top: 2px; color: #2A2F36; }}
    .nt b {{ font-weight: 700; }}
    .ev {{ display: inline-block; margin-top: 4px; font-size: 12px; letter-spacing: .14em; text-transform: uppercase;
           border: 1.3px solid; border-radius: 4px; padding: 0 6px; }}
    .arrow {{ position: absolute; top: 205px; width: 22px; height: 22px; }}
    .pin {{ position: absolute; width: 30px; height: 30px; border-radius: 50%; color: #fff; font-size: 19px; font-weight: 700;
            display: flex; align-items: center; justify-content: center; box-shadow: 0 0 0 2.5px #fff; z-index: 3; }}
    .check {{ padding: 6px 12px; }}
    .check h5 {{ font-size: 15px; letter-spacing: .12em; text-transform: uppercase; color: {MUTE}; font-weight: 400; }}
    .donut {{ display: flex; justify-content: center; margin: 12px 0 6px 0; }}
    .ok {{ text-align: center; font-size: 20px; font-weight: 700; color: #2F7D4F; line-height: 1.1; }}
    .ok small {{ display: block; font-family: NotoSC, serif; font-size: 14px; font-weight: 400; color: #2F7D4F; margin-top: 2px; }}
    .rows {{ margin-top: 12px; font-size: 13.5px; color: #3A4048; }}
    .rows div {{ display: flex; justify-content: space-between; border-top: 1px solid #EEF0F2; padding: 4px 0; }}
    .hidden {{ margin-top: 12px; border: 1.6px dashed {VIOLET}; border-radius: 9px; padding: 7px 8px; font-size: 13.5px; line-height: 1.25; color: {VIOLET}; }}
    .sheet {{ position: absolute; left: 0; right: 0; bottom: 0; background: #fff; border-top-left-radius: 18px; border-top-right-radius: 18px;
             box-shadow: 0 -8px 22px rgba(0,0,0,.18); padding: 10px 14px 16px 14px; }}
    .sheet .hb {{ width: 38px; height: 4px; border-radius: 3px; background: #D5D9DF; margin: 0 auto 8px auto; }}
    .sheet div.it {{ font-size: 14.5px; padding: 7px 2px; border-top: 1px solid #F0F1F3; display: flex; justify-content: space-between; }}
    .sheet div.it span {{ font-family: NotoSC, serif; color: {MUTE}; font-size: 13px; }}
    .sheet div.hl {{ color: {GOLD}; font-weight: 700; }}
    .dim {{ position: absolute; inset: 0; background: rgba(20,22,26,.30); }}
    .tap {{ position: absolute; width: 34px; height: 34px; border-radius: 50%; border: 3px solid #fff; background: rgba(255,255,255,.35); box-shadow: 0 0 0 6px rgba(255,255,255,.25); }}
    .rt {{ border-left: 1px solid {HAIR}; padding-left: 22px; }}
    .rt .hd {{ margin-bottom: 0; }}
    svg text {{ font-family: PagellaFig, serif; }}
    .ax {{ font-size: 17px; fill: {MUTE}; }} .axl {{ font-size: 17px; fill: {MUTE}; }}
    .gl {{ stroke: #EEF0F2; stroke-width: 1.2; }}
    .ref {{ font-size: 16.5px; }} .brc {{ font-size: 17px; font-style: italic; }} .lbl {{ font-size: 17px; fill: #3A4048; }} .ann {{ font-size: 17px; font-style: italic; }}
    .legend {{ grid-column: 1 / span 2; display: flex; gap: 16px; align-items: center; margin-top: 14px; padding-top: 9px; border-top: 1px solid {HAIR}; font-size: 15.5px; color: #3A4048; white-space: nowrap; }}
    .legend .sw {{ display: inline-block; width: 15px; height: 15px; border-radius: 4px; margin-right: 6px; vertical-align: -2px; }}
    .legend .k {{ letter-spacing: .14em; text-transform: uppercase; font-size: 13px; color: {MUTE}; margin-right: -8px; }}
    """
    # phones
    p1 = phone(grid([
        card("other", "三分钟早餐", "Breakfast in 3 minutes", "breakfast", "3.4w"),
        card("label", "女人只看彩礼", "“Women only want the bride price”", "vlog_man", "8.9w"),
        card("other", "绝杀！", "Last-second winner", "football", "2.1w"),
        card("issue", "婚礼vlog", "Our wedding day", "wedding", "1.6w"),
        card("issue", "相亲实录", "A first date", "blind_date"),
        card("issue", "婚后第一年", "Our first married year", "married_home"),
    ]))
    p2 = phone(grid([
        card("label", "男人婚后都变了", "“Men change after the wedding”", "vlog_woman", "12w"),
        card("issue", "彩礼怎么谈", "Two families, one bride price", "families", "2.3w"),
        card("label", "男人靠不住", "“Men cannot be trusted”", "vlog_car", "9.6w"),
        card("issue", "婚后第一年", "Our first married year", "married_home", "1.8w"),
        card("label", "女人只看彩礼", "“Women only want the bride price”", "vlog_man"),
        card("issue", "婚礼vlog", "Our wedding day", "wedding"),
    ]))
    donut = ("<svg width='110' height='110' viewBox='0 0 42 42'>"
             "<circle cx='21' cy='21' r='15.9' fill='none' stroke='#EEF0F2' stroke-width='6'/>"
             + "".join(f"<circle cx='21' cy='21' r='15.9' fill='none' stroke='{c}' stroke-width='6' "
                       f"stroke-dasharray='{a} {100-a}' stroke-dashoffset='{25-o}'/>"
                       for a, o, c in ((30, 0, "#7FA3C6"), (22, 30, "#E4C9A6"), (18, 52, "#A9CDB5"), (16, 70, "#C9CED6"), (14, 86, "#E0D8EE")))
             + "<text x='21' y='23.4' text-anchor='middle' font-size='6.4' fill='#3A4048' font-family='PagellaFig'>5 topics</text></svg>")
    p3 = phone(f"""<div class='check'><h5>Cocoon self-check</h5>
        <div class='donut'>{donut}</div>
        <div class='ok'>Your feed is diverse ✓<small>你的内容很丰富</small></div>
        <div class='rows'><div><span>Marriage &amp; family</span><span>30%</span></div><div><span>Food</span><span>22%</span></div>
        <div><span>Sport</span><span>18%</span></div><div><span>Travel</span><span>16%</span></div></div>
        <div class='hidden'>Not shown: within marriage, group labels are <b>13%</b> here and 6% on average.</div></div>""")
    p4 = phone(grid([
        card("label", "女人只看彩礼", "“Women only want the bride price”", "vlog_man", "8.9w"),
        card("issue", "相亲实录", "A first date", "blind_date", "1.1w"),
        card("label", "男人靠不住", "“Men cannot be trusted”", "vlog_car", "9.6w"),
        card("issue", "婚礼vlog", "Our wedding day", "wedding"),
    ]) + "<div class='dim'></div><div class='tap' style='left:60px;top:150px'></div>",
        foot="""<div class='sheet'><div class='hb'></div>
        <div class='it hl'>Not interested <span>不感兴趣</span></div><div class='it'>Show less of this topic <span>减少此类</span></div>
        <div class='it'>Report <span>举报</span></div></div>""")

    def col(kick, hd, ph, notes, pins=""):
        return f"<div><div class='kick'>{kick}</div><div class='hd'>{hd}</div><div class='pz'>{ph}{pins}</div>{notes}</div>"

    pin = lambda n, rq, x, y: f"<div class='pin' style='left:{x}px;top:{y}px;background:{RQ[rq][0]}'>{n}</div>"  # noqa: E731
    c1 = col("Day 0", "A new user", p1,
             note(1, 1, f"{R['landscape']['total_opp']*100//R['landscape']['total_issue']}%", "of issue videos take a side; they draw ~2× the comments", "RQ1 · logs")
             + note(2, 1, "1.55×", "ranking boost for group labels, the same for every user", "RQ1 · logs"),
             pin(1, 1, 236, 82))
    c2 = col("Day 89", "A topic fan", p2,
             note(3, 2, "odds ×2", "for group labels, while topic share stays at 30%", "RQ2 · simulation")
             + note(8, 2, "⅔", "OneRec separates the narrative ⅔ as sharply as the topic", "RQ2 · probe"),
             pin(3, 2, -12, 82))
    c3 = col("The check", "What the app says", p3,
             note(4, 3, "“diverse”", "a category check cannot see the skew", "RQ3 · theory")
             + note(5, 3, "4 months", f"to notice it alone: {int(round(M.detection_n(np.log(2), alpha=.79, beta=.01), -1))} labelled videos per sample", "RQ3 · bound"),
             pin(4, 3, 228, 196) + pin(5, 3, -12, 440))
    c4 = col("Day 90 on", "Trying to get out", p4,
             note(6, 4, "worse", "“not interested” is read as interest; scrolling past does better", "RQ4 · probe + sim.")
             + note(7, 4, "1 week", "after stopping, half the gain is gone", "RQ4 · simulation"),
             pin(6, 4, -12, 405))
    arrows = "".join(
        f"<svg class='arrow' style='left:calc({p}% - 11px)' viewBox='0 0 22 22'><path d='M4 11h13M12 6l5 5-5 5' fill='none' stroke='#9AA1AB' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'/></svg>"
        for p in (25, 50, 75))
    legend = ("<div class='legend'><span class='k'>Feed</span>"
              f"<span><i class='sw' style='background:#D9DEE4;box-shadow:0 0 0 2px {ROSE}'></i>video with a gender group label</span>"
              "<span style='color:#6B7280'>covers and titles are illustrative</span>"
              "<span style='flex:1'></span><span class='k'>Findings</span>"
              + "".join(f"<span><i class='sw' style='background:{c};border-radius:50%'></i>RQ{k} {n.lower()}</span>" for k, (c, n) in RQ.items())
              + "</div>")
    html = f"""<style>{css}</style><div class='wrap'>
      <div class='lt'>{c1}{c2}{c3}{c4}{arrows}</div>
      <div class='rt'><div class='kick'>Simulated topic fans, 128 days</div><div class='hd'>Same topic, narrower view</div>{chart()}</div>
      {legend}</div>"""
    render("teaser", html, 1290)


if __name__ == "__main__":
    teaser()
