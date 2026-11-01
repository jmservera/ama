---
title: "Plan: issue #232 round 2"
ms.date: 2026-11-01
---
<!-- markdownlint-disable-file -->
* [x] Phase 1: restore valid JavaScript in role-screens.js (add missing `  }` and `});` for data-operator, contractor-job-pack, resident-choice, hazard-triage); verify with `node --check`.
* [x] Phase 2: add `summarise`/`summary` to the resident-choice screen and render it in the no-home-selected state of `roleScreensView`.
* [x] Phase 3: add node-vm unit test `test_queue_summary_is_read_only_and_marks_unavailable_homes`.
* [x] Phase 4: focused validation (api unit tests, ruff check, ruff format --check, mypy).

Plan critique (single pass, self): compatible. Keep per-page fetch bounded at 20; failures show Unknown, never an empty success; no writes. Rejected: core list projection change (out of tight scope).

## Correction cycle

* [x] Merge origin/main, node --check the JS.
* [x] Add `choiceStoppedSummary` (stop state via `choiceStopVersion`, binding, review need) for the queue column.
* [x] Show `current <status>; latest recorded vN <status> (binding)` in the queue measure column.
* [x] Extend queue tests with the stale-scope and stop-then-waiting fixtures.
