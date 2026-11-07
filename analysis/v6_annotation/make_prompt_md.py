"""Regenerate prompt.md section 4 from prompt_v1.py so the two never drift. Usage: python -I make_prompt_md.py"""
import os

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
ns = {}
exec(open("prompt_v1.py", encoding="utf-8").read(), ns)
src = open("prompt_md.in", encoding="utf-8").read()
out = src.replace("SYSTEM_PLACEHOLDER", ns["SYSTEM"]).replace("TEMPLATE_PLACEHOLDER", ns["TEMPLATE"])
open("prompt.md", "w", encoding="utf-8", newline="\n").write(out)
print("wrote prompt.md")
