# Research: issue 2254 run 5 (2026-11-23)

Disposition: executed (opening record; findings appended below).

Scope: find the first criterion that code or tests can still satisfy. Prior runs (r1 to r4) proved the live counts and the under-count regression (stale stored hazard 0 while body has an open hazard). The issue body lists no ticked criteria; its expectations are: one definition across tile, map and list; reproducible cause; regression test.

Findings
* Live, revision ca-cutover-test-demo-api--0000056 (2026-11-23): tile 23, 23 map markers, list heading "23 cases", API list 23, stats hazards 23, no id difference either way (probe-r5.json, screens overview-r5.png and list-safety-r5.png under docs/reference/research/issue-2254-live-2026-11-23/). No Azure change; no throwaway resource.
* Gap on code: the existing regression covers only the under-count (stored hazard 0, body has an open hazard). The over-count (stored hazard 1, hazard released or case closed) is not tested, and it is the direction that makes the list longer than the tile.
* The repair already covers both directions (compares all columns); the test is the missing evidence. Planning Readiness: Ready.
# Research: issue 2254 run 5, sibling stale filter columns (2026-11-23)

Disposition: executed. Planning Readiness: Ready.

Earlier runs (r1 to r4, see docs/reference/research/issue-2254-live-r4-2026-11-23.md) proved the 23 vs 22 defect repaired on main (a6c0910c97) by adding `hazard` to `SqlStore._repair_identity_columns`. This run takes a new code angle.

Findings
* The HTTP list filters on stored columns: `FLAG_SQL` in `src/core/src/zava_forward/core/sqlstore.py` reads `hazard`, `support`, `days`, `decision` and `fstatus`.
* `_repair_identity_columns` rebuilds only `stage, area, wave, owner_code, closed, hazard, contractor`. The columns `support`, `days`, `decision` and `fstatus` are derived from the case body by `_row` but never reconciled, so a body edited without its columns leaves the Show only filters `support`, `long`, `nodecision`, `fundingprog` and `funding` disagreeing with the body-derived tiles, the same defect class as 2254.
* `nodecision` falls back to the in-memory path in `page_cases`, so it is body-correct already; the others are SQL-answered.
* Acceptance expectation "one definition of safety issue open across tile, map and list" is already proven live (r4). The remaining code-satisfiable gap is the sibling columns.

Plan: extend the repair column list with `support`, `days`, `fstatus`, `decision`; add a regression test that stales them and compares SQL totals to body counts.
Unprovable for the demo: the original stale live row (SQL is private); image-to-commit mapping.
