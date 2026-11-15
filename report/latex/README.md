# Final report (LaTeX)

> **Disclaimer.** The report in this folder describes an *idealised project* written for teaching purposes in COMP1110.
> **All data, experiments, figures, tables and results in it are constructed. None of them was measured**, and none is
> evidence about any dataset, model, platform, company or group of people it names. Only the cited literature, the
> descriptions of other authors' published work, the team contribution table and the declaration of generative AI use
> are real. Do not cite it or use it as a basis for research, product or policy decisions.

- `main.tex`, `report.sty`, `sections/`, `references.bib`: the report.
- `figures/src/model.py`: the scenario model; `study.py` builds every number (`results.json`, `generated/*.tex`);
  `plots.py` draws the charts; `schematics.py` renders the HTML diagrams to PDF with headless Chromium.
- Build: `bash report/latex/build.sh` (XeLaTeX; add `--data` to regenerate numbers and figures first, about three minutes).
  On Overleaf, set the compiler to XeLaTeX.
- Fonts: text, mathematics and every figure use TeX Gyre Pagella (Pagella Math for formulas). The figure scripts convert
  the TeX Live copies to TrueType in `figures/src/fonts/cache/` (`fonts/pagella.py`, git-ignored).

The earlier Markdown version of the report (based on the experiments actually run) is in `report/sections/`,
last built at commit `f99bf77`.
