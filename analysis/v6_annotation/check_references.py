"""Cross-check in-text citations in report/sections against report/sections/9_references.md (issue #20).

Usage: python -I -X utf8 check_references.py
Prints citations with no matching entry, and entries never cited. Exit code 1 if either list is non-empty.
A citation is matched to an entry by first-author surname (or group author / pen name) and year.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SECTIONS = os.path.join(os.path.dirname(os.path.dirname(HERE)), "report", "sections")
GROUP = {"Secretariat of the Office of the Central Cyberspace Affairs Commission": "Secretariat"}
NAME = r"(?:[A-Z][A-Za-z\-'’]+|de [A-Z][a-z]+)"
CITE = re.compile(rf"(?:[A-Z]\. )?({NAME})(?: (?:et al\.|(?:&|and) {NAME}))?(?:,| \()\s?((?:19|20)\d\d)((?:, (?:19|20)\d\d)*)")


def entries():
    text = open(os.path.join(SECTIONS, "9_references.md"), encoding="utf-8").read()
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    out = {}
    for block in text.split("\n\n"):
        block = block.strip()
        if not block or block.startswith("#"):
            continue
        m = re.match(r"(.+?)\.? \(((?:19|20)\d\d)", block)
        first = m.group(1)
        for g, short in GROUP.items():
            if first.startswith(g):
                first = short
        out[(first.split(",")[0].split(" ")[0] if first != "Secretariat" else first, m.group(2))] = block[:70]
    return out


def citations():
    found = {}
    for f in sorted(glob.glob(os.path.join(SECTIONS, "*.md"))):
        if f.endswith("9_references.md"):
            continue
        s = open(f, encoding="utf-8").read()
        s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
        s = re.sub(r"```.*?```", "", s, flags=re.S)
        s = re.sub(r"\$[^$]*\$", "", s)
        for g, short in GROUP.items():
            for y in re.findall(re.escape(g) + r" et al\., ((?:19|20)\d\d)", s):
                found.setdefault((short, y), set()).add(os.path.basename(f))
            s = re.sub(re.escape(g) + r" et al\., (?:19|20)\d\d", "", s)
        for m in CITE.finditer(s):
            name, years = m.group(1), [m.group(2)] + re.findall(r"\d{4}", m.group(3) or "")
            if name in ("Section", "Table", "Figure", "Appendix", "Proposition", "In", "Since", "From", "By", "On", "The"):
                continue
            for y in years:
                found.setdefault((name, y), set()).add(os.path.basename(f))
        for y in re.findall(r"\(Shiqi, ((?:19|20)\d\d)\)", s):
            found.setdefault(("Shiqi.", y), set()).add(os.path.basename(f))
    return found


def main():
    ent, cit = entries(), citations()
    ent_keys = {(k[0].rstrip("."), k[1]) for k in ent}
    cit_keys = {(k[0].rstrip("."), k[1]) for k in cit}
    missing = sorted(cit_keys - ent_keys)
    uncited = sorted(ent_keys - cit_keys)
    print(f"{len(ent)} entries, {len(cit_keys)} distinct citations")
    for k in missing:
        print("CITED BUT NOT LISTED:", k, sorted(cit.get(k, cit.get((k[0] + ".", k[1]), []))))
    for k in uncited:
        print("LISTED BUT NOT CITED:", k)
    sys.exit(1 if missing or uncited else 0)


if __name__ == "__main__":
    main()
