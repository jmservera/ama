# Issue 233 criteria A and B audit (research)

Research disposition: executed. Planning Readiness: Ready. Tier: Focused.

## Evidence
* Criterion A (tensions shown where designs resolve them). `role-screens.js` renders the "Not shown for this role" panels (programme-queue, resident-choice, technical-queue, quality-queue) and the "Choice comes before offered capacity" panel on resident-choice; procurement-packages states the offer-is-not-a-promise rule (line ~1169). `checks/atlas_tensions_browser_check.py` rendered them in Chromium: exit 0, 370 PASS on 2026-11-13 at this head.
* Criterion B (same-home connected walk, no relabelling). `checks/connected_home_browser_check.py` walks one real Store-written home ZF-1 across five constructed logins and six screens with sibling ZF-2 as control; exit 0, 142 PASS, no write requests, no JS errors. It never calls ZF-1 EX-HOME-901 or any of the eight historical examples. `tests/test_connected_home_check.py` plus `test_atlas_tensions_checker.py`: 33 tests OK (3 skipped).
* Local run note: Playwright needed `libatomic.so.1` (extracted to /tmp, LD_LIBRARY_PATH) and chromium-headless-shell 1254.

## Gap found
* `docs/reference/research/ux/atlas-screen-trace.md` "Same-home walkthrough" says no fixture or screen for EX-HOME-901 exists and does not mention the executed ZF-1 connected walk, so the trace understates delivered evidence. No test pins that the checker keeps ZF-1 distinct from EX-HOME-901 / the eight separate examples.
* The checker itself still lists real deferrals (stage 1, aftercare, event order, AT, user validation): C4 full eight-stage walk, C5 and human acceptance stay unmet.

## Decision
No `role-screens.js` change needed. Add (1) a short unit guard in `test_connected_home_check.py` that the checker source does not relabel ZF-1 as EX-HOME-901 and keeps its deferral/not-acceptance statement; (2) a bounded trace paragraph and log entry recording the ZF-1 walk as engineering evidence, separate from EX-HOME-901. Do not tick criteria.
