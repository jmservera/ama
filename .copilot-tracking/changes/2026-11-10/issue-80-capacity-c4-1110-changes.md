---
title: Issue 80 capacity C4 changes
description: Prospective and final change record for C4
ms.date: 2026-11-10
---

## Prospective (before implement-start)

* Planned source change: `src/api/checks/capacity_browser_check.py` only, per the [details](../../details/2026-11-10/issue-80-capacity-c4-1110-details.md): the C3 branch of `hold_capacity_read` calls `inject(route)` so the retry request is registered in `expected_failures` before the same 503 is served.
* No whole browser run is planned (line-571 cause unknown). No app, API, core, auth, UI or `ops.js` change.
* Not yet done: edit, validation, review.

## Final (2026-11-10)

* Changed `src/api/checks/capacity_browser_check.py` only (1 line, raw diff `phase80-capacity-c4-evidence-1110/impl.diff`): the C3 branch of `hold_capacity_read` now calls `inject(route)` instead of `route.fulfill(status=503, body="Unavailable")`, so the retry request is registered in `expected_failures` first (C3-R1). Same status and body; flag, exact-endpoint match, held sibling, 401 release, assertions and timeout unchanged.

| Check | Exit | Result |
| --- | --- | --- |
| Ruff check, format check (checker) | 0, 0 | Pass |
| `node --check ops.js` (unchanged) | 0 | Pass |
| `test_list_export_api` | 0 | 11 OK |
| Related static (5 modules) | 0 | 60 OK |
| Diagnostic observation 1 (`obs1.*`) | 0 | Stage works as designed; snapshot defect disclosed |
| Diagnostic observation 2 (`obs2.*`) | 0 | 6 of 6 stage runs showed the alert in about 5.2 s |
| Whole `capacity_browser_check --axe` | not run | Line-571 cause unknown; a run would be blind (Root excluded it) |

* Skipped by design: whole browser run. The C3-R1 fix and the C3 stage correction are unexercised at runtime; the delayed-401 iterations and the empty-capacity assertion remain unobserved. The C3 line-571 failure is neither explained nor corrected.
* Cleanup: disposable drivers live only as evidence copies; no helper or `/tmp/ama-c4diag*` scratch left.
