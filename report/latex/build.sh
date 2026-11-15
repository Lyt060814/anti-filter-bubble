#!/usr/bin/env bash
# Build the report PDF. Usage: bash report/latex/build.sh [--data]
#   --data  also regenerate the constructed data, charts and schematics (needs python3 with numpy, scipy, matplotlib; Chromium)
set -euo pipefail
cd "$(dirname "$0")"
if [ "${1:-}" = "--data" ]; then
  (cd figures/src && python3 study.py && python3 plots.py && python3 schematics.py)
fi
latexmk -xelatex -interaction=nonstopmode -halt-on-error -quiet main.tex
echo "built $(pwd)/main.pdf ($(pdfinfo main.pdf | awk '/Pages/{print $2}') pages)"
