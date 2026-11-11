#!/usr/bin/env bash
# Assemble report/sections/*.md in numeric order into report/build/report.md and build report/build/report.pdf.
# Usage (from the repository root): bash report/build_report.sh
# Image paths are made absolute so the headless browser can load them; HTML comments are dropped.
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)"
out="$repo/report/build"; mkdir -p "$out"
# Image URLs must use the browser's native path form: file:///D:/... on Windows (Git Bash), file:///home/... elsewhere.
if command -v cygpath >/dev/null 2>&1; then repo_url="file:///$(cygpath -m "$repo")"; else repo_url="file://$repo"; fi
{
  echo "# Viewpoint Cocoons in Chinese Short-Video Feeds"
  echo
  echo "COMP1110 Final Report · Fu Yitong, Li Yitong, Wang Junbo, Xu Ruicong, Zhao Dingcheng"
  echo
  # Report-only layout: figures centred and capped in height so a figure never fills a page.
  echo '<style>img{display:block;margin:4pt auto;max-width:100%;max-height:8.5cm;object-fit:contain}'
  echo 'img[src*="exposure_report_mockup"]{max-height:15cm} h2{break-before:auto} p{margin:0 0 5pt}</style>'
  echo
  for f in $(ls "$repo"/report/sections/*.md | sort -t/ -k1 -V); do
    perl -0pe 's/<!--.*?-->\n?//gs' "$f" | sed -E 's/^# /## /; s/^## ([0-9]+\.[0-9])/### \1/; s/^### ([^0-9])/#### \1/' \
      | sed -E "s#\]\(\.\./\.\./([^)]+\.(png|jpg|svg))\)#]($repo_url/\1)#g; s#\]\(\.\./(screenshots/[^)]+)\)#]($repo_url/report/\1)#g"
    echo
  done
} > "$out/report.md"
bash "$repo/docs/project-plan/pdf-build/build.sh" "$out/report.md"
