"""Make TrueType copies of TeX Gyre Pagella, the report's body font, for the figure scripts.

matplotlib (pdf.fonttype 42) and Chromium both embed TrueType fonts as real fonts, whereas the
CFF-based .otf files that TeX Live ships end up as Type 3 or fail. This converts the four .otf
files once into ./cache (git-ignored), under the family name "PagellaFig" so that it never clashes
with the system's own copy. Outlines are unchanged apart from the cubic-to-quadratic conversion.

TeX Gyre Pagella: (c) GUST e-foundry, GUST Font License. The converted files are not distributed.
"""
from __future__ import annotations

from pathlib import Path

from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, newTable

FAMILY = "PagellaFig"
HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
SEARCH = [Path("/usr/share/texmf/fonts/opentype/public/tex-gyre"),
          Path("/usr/share/texlive/texmf-dist/fonts/opentype/public/tex-gyre")]
STYLES = {"regular": "Regular", "italic": "Italic", "bold": "Bold", "bolditalic": "Bold Italic"}


def _find(style: str) -> Path:
    for d in SEARCH:
        p = d / f"texgyrepagella-{style}.otf"
        if p.exists():
            return p
    import subprocess
    out = subprocess.run(["kpsewhich", f"texgyrepagella-{style}.otf"], capture_output=True, text=True).stdout.strip()
    if out:
        return Path(out)
    raise FileNotFoundError(f"texgyrepagella-{style}.otf not found; install TeX Gyre (tex-gyre package)")


def _convert(src: Path, dst: Path, style: str) -> None:
    font = TTFont(str(src))
    order = font.getGlyphOrder()
    gs = font.getGlyphSet()
    glyphs = {}
    for name in gs.keys():
        pen = TTGlyphPen(gs)
        gs[name].draw(Cu2QuPen(pen, 1.0, reverse_direction=True))
        glyphs[name] = pen.glyph()
    font["loca"] = newTable("loca")
    font["glyf"] = glyf = newTable("glyf")
    glyf.glyphOrder = order
    glyf.glyphs = glyphs
    del font["CFF "]
    for t in ("VORG",):
        if t in font:
            del font[t]
    glyf.compile(font)
    hmtx = font["hmtx"]
    for name, g in glyf.glyphs.items():
        if hasattr(g, "xMin"):
            hmtx[name] = (hmtx[name][0], g.xMin)
    font["maxp"] = maxp = newTable("maxp")
    maxp.tableVersion = 0x00010000
    for attr in ("maxZones",):
        setattr(maxp, attr, 1)
    for attr in ("maxTwilightPoints", "maxStorage", "maxFunctionDefs", "maxInstructionDefs",
                 "maxStackElements", "maxSizeOfInstructions"):
        setattr(maxp, attr, 0)
    maxp.maxComponentElements = max((len(getattr(g, "components", []) or []) for g in glyf.glyphs.values()), default=0)
    maxp.compile(font)
    post = font["post"]
    post.formatType, post.extraNames, post.mapping, post.glyphOrder = 2.0, [], {}, order
    try:
        post.compile(font)
    except OverflowError:
        post.formatType = 3
    sub = STYLES[style]
    names = font["name"]
    for rec in list(names.names):
        if rec.nameID in (16, 17, 21, 22):
            names.removeNames(nameID=rec.nameID)
    for pid, eid, lid in ((3, 1, 0x409), (1, 0, 0)):
        names.setName(FAMILY, 1, pid, eid, lid)
        names.setName(sub, 2, pid, eid, lid)
        names.setName(f"{FAMILY} {sub}", 4, pid, eid, lid)
        names.setName(f"{FAMILY}-{sub.replace(' ', '')}", 6, pid, eid, lid)
    font.sfntVersion = "\000\001\000\000"
    dst.parent.mkdir(exist_ok=True)
    font.save(str(dst))


def ensure() -> dict[str, Path]:
    """Return {style: path to TrueType file}, converting on first use."""
    out = {}
    for style in STYLES:
        dst = CACHE / f"{FAMILY}-{style}.ttf"
        if not dst.exists():
            _convert(_find(style), dst, style)
        out[style] = dst
    return out


if __name__ == "__main__":
    for k, v in ensure().items():
        print(k, v)
