"""Regenerate prompt.md from prompt_md.in and the current prompt module so the two never drift.

Usage: python -I -X utf8 make_prompt_md.py
"""
import os

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
CURRENT = "prompt_v2.py"
ns = {}
exec(open(CURRENT, encoding="utf-8").read(), ns)
src = open("prompt_md.in", encoding="utf-8").read()
out = src.replace("SYSTEM_PLACEHOLDER", ns["SYSTEM"]).replace("TEMPLATE_PLACEHOLDER", ns["TEMPLATE"])
open("prompt.md", "w", encoding="utf-8", newline="\n").write(out)
print("wrote prompt.md")
