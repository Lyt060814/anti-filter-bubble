"""Schematic figures drawn as HTML and printed to vector PDF with headless Chromium.

Constructed for an idealised teaching report (see ../../README.md).
Shared HTML-to-PDF renderer used by teaser.py (Figure 1) and arch.py (Figure 2).
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


if __name__ == "__main__":
    print("schematics.py only provides render(); run teaser.py (Figure 1) and arch.py (Figure 2).")
