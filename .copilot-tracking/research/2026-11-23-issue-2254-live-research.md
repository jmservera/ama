# Research: issue 2254 safety tile vs list count (2026-11-23)

Disposition: executed. Planning Readiness: Ready.

Findings
* Tile (`insights.stats`), map (`insights.map_points/map_view`) and the in-memory list use `taskqueues.has_open_safety` on the case body. The HTTP list uses `SqlStore.page_cases`, which filters on the stored `cases.hazard` column.
* Cause of 23 vs 22: a stale column; `_repair_identity_columns` did not rebuild `hazard`. Fixed on main by a6c0910c97 (in HEAD). Regression test: `src/core/tests/test_sqlreads.py` (issue_2254).
* Reproduced on code: removing `hazard` from the repair makes the test fail, 3 != 4; restoring passes; module 18 OK.
* Live (revision 0000055): tile 23, markers 23, list "23 cases", API list 23, stats 23, same ids on map and list.

Evidence: docs/reference/research/issue-2254-live-r4-2026-11-23.md and issue-2254-live-2026-11-23/.
Unprovable: stale live row (SQL private); deployed image to commit mapping.
Follow-ups: none new; earlier notes already hold run 3 proof.
