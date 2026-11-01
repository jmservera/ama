# Plan: issue 135 exception queue slice

Date: 2026-11-01. Research: ../research/2026-11-01-issue-135-exception-queue-steward-research.md

## Phases

* [ ] P1 Add `src/core/src/zava_forward/core/exception_queue.py` (ExceptionQueue: raise, conflict view, scoped queue view, controlled recovery request, audit log, outage banner).
* [ ] P2 Add `src/core/tests/test_exception_queue.py` covering each acceptance criterion.
* [ ] P3 Add README section in `src/core/README.md`.
* [ ] P4 Run pytest/unittest, ruff check, ruff format --check, mypy in `src/core`.

## Acceptance mapping

1. Conflict values with source, date, version and named resolution owner: `raise_conflict`, `conflict_view`.
2. Failed imports, model calls, stranded tasks in an owned queue: `raise_failure`, `queue`.
3. Recovery controlled and audited; no replay or release: `request_recovery` records only, flags replayed/released False.
4. Original source and unresolved eligibility preserved: deep-copied immutable `original_source`, `eligibility` remains Unknown.
5. Scoped, visible access and honest outage: `access_report`, `queue(actor)`, `outage_banner`.

## Critique (single pass, verdict proceed)

* Risk: a recovery call could be read as an automatic replay. Mitigation: only named human actors in the owning role, mandatory reason, status `recovery_requested`, no callback or executor exists.
* Risk: resolving a conflict could hide the other value. Mitigation: resolution records a chosen value and evidence but both values and original source remain; eligibility is never changed.
* Direct dispositions: both applied in the plan. No user decision needed.
