## R5 post-merge integration polish (#16 review)

Address the two requested editorial items without changing any numerical results:

- Align feedback with Proposition 1, filtering with Proposition 3 and detection with Proposition 6. First use of V_sup explicitly maps to Section 3.2's total skew rather than personal V.
- Shorten the main discussion, keep a six-row parameter table, and lead each subsection with its result. Detailed parameters, calibration conventions, eleven-arm definitions, filtering normalization, censoring, detection formula and reproduction move to Appendix B.

Appendix B's source is saved in analysis/v6_simulation/appendix_b.md and linked from the subsection, respecting the originally authorized paths. It is ready for inclusion as Appendix B during final export. No edits to other authors' report files. The simulation block is marked, and headings reserve 5.1 for Li Yitong's forthcoming OneRec measurements; our text is 5.2/5.3.

All four figure links, screenshot/log hashes and numerical-evidence checks still pass. Old #7 is confirmed closed after merged #16. This is prose/organization only; it does not rerun or change the agreed simulations.
