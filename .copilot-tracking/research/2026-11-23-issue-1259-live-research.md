---
title: Research, issue 1259 live run 7
ms.date: 2026-11-23
---

Disposition: executed. Scope: unticked AC4 (regressions plus failing-first) and AC5 (process gate). Fix and regressions are on main (head 342fad401d).

Findings:

* Red at `cd687abadd^` with current tests: 6 tests, 7 failures. Green on main: 110 tests OK.
* Live: `ca-cutover-test-demo-api` active revision 0000054 and `ca-resident-demo` 0000026 are image-based apps; no `rankingPublish` job exists among the Container Apps jobs (load, audit, orch, live-simulator, live-receiver). The ranking runner is an operator CLI, so no live behaviour can prove or disprove the criteria; local filesystem tests are the right mechanism.

Planning Readiness: Ready.
