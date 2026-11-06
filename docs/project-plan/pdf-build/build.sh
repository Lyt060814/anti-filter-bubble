#!/usr/bin/env bash
# Build a PDF from a Markdown plan: pandoc -> standalone HTML (MathJax SVG formulas) -> headless Chromium.
# Usage (from the repository root): bash docs/project-plan/pdf-build/build.sh docs/project-plan/research_plan_v5.md
# Needs pandoc, npm (MathJax is installed into pdf-build/node_modules on first run) and Chromium.
# Relative links to repository files are rewritten to GitHub URLs so they work inside the PDF.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "$here/../../.." && pwd)"
src="$(realpath "$1")"
name="$(basename "$src" .md)"
rel_dir="$(realpath --relative-to="$repo" "$(dirname "$src")")"
out_pdf="$(dirname "$src")/$name.pdf"
mkdir -p "$here/out"
[ -f "$here/node_modules/mathjax/es5/tex-svg-full.js" ] || npm install --silent --no-audit --no-fund --prefix "$here" mathjax@3.2.2
html="$here/out/$name.html"
title="$(grep -m1 '^# ' "$src" | sed 's/^# //')"
pandoc "$src" -f markdown -t html5 -s \
  --mathjax="../node_modules/mathjax/es5/tex-svg-full.js" \
  --include-in-header="$here/mathjax-config.html" \
  --css="../style.css" -V document-css=false \
  --lua-filter="$here/filters.lua" -M source-dir="$rel_dir" \
  -M pagetitle="$title" -o "$html"
chromium="${CHROMIUM:-$(command -v chromium || command -v chromium-browser || command -v google-chrome)}"
rm -f "$out_pdf"
"$chromium" --headless=new --no-sandbox --disable-gpu --run-all-compositor-stages-before-draw \
  --virtual-time-budget=30000 --no-pdf-header-footer \
  --print-to-pdf="$out_pdf" "file://$html" >/dev/null 2>&1 || true
[ -s "$out_pdf" ] || { echo "PDF was not produced" >&2; exit 1; }
echo "$out_pdf"
