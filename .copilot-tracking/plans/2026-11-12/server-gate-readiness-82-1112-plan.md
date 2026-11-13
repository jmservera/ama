---
title: Issue 82 funding readiness fail-closed plan
ms.date: 2026-11-12
task_id: server-gate-readiness-82-1112
---

## Objective

Make the server-side readiness pre-check (`Store.gate_reasons`) use the same fail-closed definition of funding as the existing booking gate: only an explicit `True` is confirmed. An absent or non-boolean `funding_ok` then yields the existing funding reason (HTTP 409) instead of a `KeyError` (HTTP 404 "Case not found.") or a false "ready". Research: [research](../../research/2026-11-12/server-gate-readiness-82-1112-research.md). Details: [details](../../details/2026-11-12/server-gate-readiness-82-1112-details.md). Refs #82 only.

## Phases

* [x] Phase 1: one independent critique of the final candidate plan, recorded in [critique](server-gate-readiness-82-1112-critique.md); apply compatible findings.
* [x] Phase 2: add failing-first regressions (store level and HTTP level), record the failing output, then apply the one-line change.
* [x] Phase 3: focused validation: new tests, `test_gates`, impacted store/API tests, ruff check, ruff format --check on touched files, mypy where configured.
* [ ] Phase 4: changes record, one original Review, local commit with repository-local privacy-safe identity.

## Boundaries and stop rules

* No new rule, policy, gate family, finance gate, reviewer or approval; rule records and "unreviewed exercise rule" reviewer stay unchanged.
* Denials stay denials; unknown never passes; no consent, safety hold or independent-review logic changes; `taskqueues.py`, `gates.py` and the server mapping are not edited.
* No push, PR, merge, issue edit, tick or closure; no correction allowance created; no full gate, SQL, live or model execution.
* One candidate only; Review findings become later work.
