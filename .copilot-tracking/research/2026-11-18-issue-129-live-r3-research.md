# Research: issue #129 live re-verification, third pass (2026-11-18)

Disposition: executed (extends the r1 and r2 notes in docs/reference/research). Scope: synthetic demo, desktop only; owner decisions 2026-11-18 apply.

Open criterion on the issue: "Atlas owner confirms bundle to opportunity mapping". Ticked: bundles; O10 and O18 to O20 out of scope.

Known evidence: issue comments 2026-11-03, 11-05, 11-10 (CLI via PR #1374 is partial); r2 note records the mapping as unproven.

Questions for this pass:
1. Do the core and api suites and the PR #1374 stdin CLI still pass on current main (b6b08475c)?
2. Does the live demo (revision 0000031 or newer) still expose any bundle screen or route, and is an Atlas-owner confirmation recorded anywhere (issue comments, ADR, protocol)?

Planning Readiness: Ready. Live action limited to read-only sign-in and GETs; no Azure resource created.
