---
title: Issue 82 capacity-at-booking plan and details supplement (2026-11-06)
ms.date: 2026-11-06
---

Supplements, leaving byte-identical, the d688 plan (sha256 00283261...) and details (46d237f7...). Admission: capacity-at-booking only; coupled authority and resident checks keep their order, types and text. Not acceptance of the authority family or any approved policy.

* [ ] Phase 1: shared `Flows` tests, RED first (JSON and SQLite; MssqlProcurement inherits, run only in a separately admitted full gate).
* [ ] Phase 2: `gates.CAPACITY_RULE` and `capacity_gate`; `CapacityGateError(ValueError)` carrying a result; classify the capacity sites; `require_booked_capacity` returns the pass result.
* [ ] Phase 3: light checks, Changes, canonical Review, local commit.

## Semantics

* Unknown (refuses): no single appointed order; missing, legacy, unreadable, stale or hash/scope/contract/home-mismatched capacity evidence; accepting manager no longer valid; recorded authority changed.
* Fail (refuses): work date outside evidenced period; committed capacity below existing orders.
* Pass: all existing checks succeed. Rule: gate "capacity", source PRD FR-008 and FR-016 with `procurement` evidenced capacity, effective date 2026-11-06 (implementation date), version "1", reviewer "Unreviewed exercise rule: named reviewer required before live use".
* Existing exception types and texts are unchanged (subclass of ValueError, same message). Authority/resident PermissionError and ValueError pass through untouched. Refusal happens before mutation, so no state, audit or snapshot change (asserted).

## Tests (fail before the change)

1. Booked valid case: `require_booked_capacity` returns outcome pass with the capacity rule and unreviewed reviewer; `advance` still books.
2. Known violation: evidenced period ends before the work date gives fail through `advance`, original ValueError text, `.result.outcome == "fail"`, no state change.
3. Corrupt stored capacity (persisted and reopened) gives unknown, refusal, no state change.
4. Control: authority and resident refusals keep their original exception types.

## Validation

* Now (LIGHT, own environment, exact-worktree imports, external caches, bytecode off): `test_gates`, `test_quality_procurement` (JsonFlows, SqlFlows), `test_consultation_controls`, `test_appointments*` if present, configured ruff check and format and mypy for `src/core`.
* Pending, FULL (SQL-backed authority and capacity): maintained gate with `test_mssqlstore.MssqlProcurement`, held by #185; independent exact-head assessment follows. No downgrade.
