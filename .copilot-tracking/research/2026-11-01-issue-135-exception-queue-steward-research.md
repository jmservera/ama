# Research: issue 135 data steward and digital operator exception queue

Date: 2026-11-01. Disposition: executed. Planning Readiness: Ready.

## Evidence

* PRD FR-012 and AC-040 (conflict exposes both values, source ids, dates/versions, validation state, resolution owner; authority and eligibility stay Unknown). FR-029 and AC-031 (row-level import disposition, source workbook unchanged).
* Existing core pattern: store-independent, injected-input registers with their own tests, for example `src/core/src/zava_forward/core/challenges.py` (#220) and `cohort_eval.py`. Each has a README section and a `tests/test_*.py`.
* Existing partial coverage: `ai_tasks.py` (AI records and quarantine), `continuity.py` (incident and continuity records), `taskqueues.py` (read-only work queues, never assignment), `recovery.py` (erasure register). None provides an owned exception queue with controlled recovery.
* No store, API or UI exposes an exception queue; no `exception` module exists.

## Decisions for the slice

* New pure module `zava_forward.core.exception_queue` with injected clock; no store, API, UI or importer coupling (dependency rule: core imports no workload).
* Two named roles, `data_steward` and `digital_operator`, routed by exception kind. Role names are engineering placeholders; the open item (named operator and steward roles) stays open for the owner.
* Recovery is a recorded, human-actor request only. The module never replays, releases or corrects; it keeps the original source and unresolved eligibility.
* Outage state shown honestly: unknown or stale checks are reported as Unknown, never healthy.

## Not delivered (out of tight scope)

Persistence in JSON/SQL/MSSQL stores, API and UI wiring, importer/AI-run producers, named role approval, runbook owner sign-off.
