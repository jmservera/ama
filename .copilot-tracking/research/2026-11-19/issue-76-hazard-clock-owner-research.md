# Issue 76 research: hazard and safeguarding clock and named owner

Disposition: executed. Planning Readiness: Ready (no source change needed).

Only unticked criterion: "Hazard and safeguarding items show a clock and named owner". Demo is synthetic, desktop only (owner decision 2026-11-18).

Findings:
* Code exists: `taskqueues.project_safety_clock_and_owner`, `safeguarding_clocks`, renderer in `src/api/.../web/app.js`; tests `test_hazard_safeguarding_clock_owner_76.py`, `test_taskqueues` (31 tests OK on this checkout).
* Earlier passes (r1 to r3, 2026-11-18) found 0 of 16 safeguarding items live.
* Fresh live probe 2026-11-19, revision 33: 1 safeguarding clock (ZF-2025-0148, owner named, 39 h, due 2026-10-17T09:00:00Z) and 1 hazard clock (ZF-2025-0331, owner named, times Unknown).
* No safeguarding write path exists in the API; adding one would touch a safety authority boundary (FULL tier), and is no longer needed to prove the demo.

Evidence: docs/reference/research/issue-76-live-r4-2026-11-19.md and its folder.
