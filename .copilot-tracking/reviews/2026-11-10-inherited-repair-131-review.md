---
title: Issue 131 inherited correction batch review
ms.date: 2026-11-10
task_id: 131-inherited-repair-1110
---

## Execution and outcome

* Review executed once, authored by the implementing worker. It is not independent. Root's independent exact-head assessment is still required before publication.
* Boundary: the dirty source set on top of merge `6ecb920` (`resident_decisions.py`, `test_resident_decisions.py`, `src/core/README.md`) plus the RPI records.
* Outcome: conformant for the two authorized Medium findings and the typing and format items, with open follow-ups routed to later work. No material finding remains open in the batch scope.

## Findings against the plan

| Item | Result |
| --- | --- |
| Corrupt stored inventory history reads as valid (D1 Medium 1) | Fixed. Every revision is validated; the view reads Malformed and the writer refuses without mutation or audit. Regression test covers 7 injected corruptions plus a valid control; it failed before the fix (red.exit 1) and passes on JSON and SQLite stores. |
| Ambiguous identity and Unknown route add no refusal reasons (D1 Medium 2) | Fixed with count-only reasons before the open-trigger reason. A canary check shows no reference, source, owner or digest leaks. |
| Three Core mypy errors | Fixed with real types, no casts to Any or suppressions. Configured mypy exit 0 over 288 files. |
| Format failure | Fixed by `ruff format` of the test file. Configured format check exit 0. |
| Hold safety | `TENURE_HOLD` stays last in every refusal; nothing releases or permits scope. Unmanaged legacy cases are unchanged by the existing tests. |
| Scope | Only the module, its direct tests and one README paragraph changed, plus an ordinary merge of `origin/main`. No schema, UI, endpoint, authority or roster change. |

## Routed follow-ups

* RV-001 (Low): add a stronger API-level `scope_record` assertion for the new reasons. Not done here to stay in the authorized batch.
* RV-002 (Low): the identity reason is permanent for linked reports because no action updates `identity_state`. A future approved process must define resolution.
* RV-003: MSSQL was not run and is not claimed. SQL-store cases ran only through the SQLite store.
* Budget: this batch consumed one cycle; the conservative proved minimum afterwards is 0. A further correction needs a new Root grant.
* Roster completeness, authority appointments, Legal and Finance handoffs, universal pre-offer integration and any hold release remain pending. This is not universal C1 or C2 compliance.
