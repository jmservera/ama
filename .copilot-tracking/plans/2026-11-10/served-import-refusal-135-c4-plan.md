---
title: Plan, served import refusal correction (#135 C4/5)
ms.date: 2026-11-10
---

Planned 2026-11-10 after research and before any source edit. One coherent correction batch; one correction (C5) remains afterwards. Details: [details](../../details/2026-11-10/served-import-refusal-135-c4-details.md). Critique: [critique](../../reviews/plans/2026-11-10/served-import-refusal-135-c4-plan-critique.md).

## Phases

* [x] Phase 1: Open the changes record, then Core store-owned persistence (`import_refusals.py` mixin hook, `sqlstore.py` override). Findings 1.
* [x] Phase 2: Importer CLI error contract (`__main__.py`). Finding 2.
* [x] Phase 3: Register source status from one snapshot with stored/shown counts (`exception_register.py`). Finding 3.
* [x] Phase 4: Load web skills and fetch current web-design-guidelines, then one copy correction in `role-screens.js` and screen test coverage. Finding 4.
* [x] Phase 5: Focused regressions that fail on 67ad4680 (Core persistence, importer CLI, API scoped source text, screen). Re-run external red probes.
* [x] Phase 6: Targeted validation: importer, Core, API suites, ruff, format, mypy, actual local JSON and SQLite served story, served browser render with scoped empty states, actual disposable MSSQL persistence, reload, idempotency and rollback evidence.
* [x] Phase 7: One Review, state, handoff, local commit (no push).

## Success criteria

* A failed save leaves no in-memory projection, no success audit, no durable change, and a same-instance retry persists once (JSON, SQLite, MSSQL).
* Committed-but-refresh-failed and partially recorded outcomes are reported distinctly, never as "nothing recorded".
* CLI exits 2 with a truthful diagnostic and no traceback for ConflictError, driver errors and the committed-uncertain outcomes.
* Source text states stored count and shown count from the same snapshot as the queue and never says items are shown when scope hides them.
* The screen empty text no longer claims failed imports are unconnected when connected.
* No new roles, permissions, producer, replay, rejected-batch feature or model call.

## Blockers recorded in advance

* C3 process order adverse stays a publication blocker.
* MSSQL and browser proof are required; if the disposable container, driver or browser cannot run, record blocked, not success.
