# Research: issue 2254 run 5 (2026-11-23)

Disposition: executed (opening record; findings appended below).

Scope: find the first criterion that code or tests can still satisfy. Prior runs (r1 to r4) proved the live counts and the under-count regression (stale stored hazard 0 while body has an open hazard). The issue body lists no ticked criteria; its expectations are: one definition across tile, map and list; reproducible cause; regression test.

Findings
* Live, revision ca-cutover-test-demo-api--0000056 (2026-11-23): tile 23, 23 map markers, list heading "23 cases", API list 23, stats hazards 23, no id difference either way (probe-r5.json, screens overview-r5.png and list-safety-r5.png under docs/reference/research/issue-2254-live-2026-11-23/). No Azure change; no throwaway resource.
* Gap on code: the existing regression covers only the under-count (stored hazard 0, body has an open hazard). The over-count (stored hazard 1, hazard released or case closed) is not tested, and it is the direction that makes the list longer than the tile.
* The repair already covers both directions (compares all columns); the test is the missing evidence. Planning Readiness: Ready.
