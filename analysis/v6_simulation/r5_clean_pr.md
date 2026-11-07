## R5, rewritten from new main after merged R2/R3/R4

Replace the obsolete draft with the English simulation/detectability subsection only, based on the merged calibrated package (#3) and v2 detection results (#15). Other authors' sections are preserved; the file's simulation scope is explicitly marked.

Includes a self-contained model description, evidence-labelled parameter table, four existing PNG/PDF figures, actual numerical conclusions and limitations. Explains why S3 does not reverse skew: ordinary B has only -c²s local contrast versus A's c²(1-s), so at 2% supply its per-update attribute signal is about 1/49. The negative local sign in Proposition 2 does not imply large cumulative escape while natural A feedback continues.

Discusses calibration identifiability (eta*t²/tau and eta*c²/tau only), uncertain Qwen-labelled pilot targets, assumed coordinate caps/memory/heavy-user priors, supply rather than personal reference, unequal effort, idealized deletion and right censoring. No new platform or belief claim.

Adds a small v2 filtering supplement: the main fitted group case with the cross-check FPR .12525 gives delta skew -1.6551 and delta log topic exposure -.1453, versus -1.7833/-.0476 for the benchmark assumed classifier. This is a two-main-case sensitivity, not a full-grid rerun. Static direct-filter predictions are retained for all 262 x four theta x twenty seed endpoints; their frame is explicitly separated from dynamic endpoints. Source rates are cross-model agreement estimates, not human gold-standard accuracy, and their uncertainty is not propagated.

Detection now uses DeepSeek v2 1.0% as main reference. At twice the odds and topic rate 1.6%, the Qwen cross-check error profile requires 33,070 same-topic videos or 2,066,875 total exposures per arm. False positives overwhelm rare-target signal in this tested scenario; this does not prove universal impossibility of open-source classification.

Includes a genuine screenshot of calibrated_audit.py stdout displayed in Notepad, the exact source log and SHA256 metadata. Added AI log and Xu contribution entries. Focused checks verify all figure links, screenshot/log hashes, all new seed records, and that baseline dynamic values match merged R3. The analysis directory remains below 60 MB. Required shared-file exceptions are the figure, AI and contribution logs plus screenshot evidence.

This clean PR supersedes old #7. After this PR is merged, close #7; do not merge its obsolete model results. No automatic merge and no direct main push.
