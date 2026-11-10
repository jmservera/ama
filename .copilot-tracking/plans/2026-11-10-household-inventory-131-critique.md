---
title: Issue 131 case-local expected-household inventory primitive critique
ms.date: 2026-11-10
task_id: 131-household-inventory-1110
---

## Execution

Single final-candidate critique of the plan and details, executed once on 2026-11-10 before implementation. Nested agents were prohibited by the brief, so this is an authored self-critique by the implementing agent, not an independent review. It does not satisfy the independent exact-head assessment that remains required before publication.

Verdict: Proceed with five compatible findings applied directly to the details. No finding conflicts with a confirmed Root decision and none needs a user decision.

## Findings and dispositions

| ID | Finding | Disposition |
| --- | --- | --- |
| PC-001 | The view runs on a detached copy in `Store.detail` but is also called by the gate on the live case. It must not use `setdefault` or any write, or a read could mutate stored data. | Applied: the view only reads with `.get`, and a test compares the case and audit before and after reads. |
| PC-002 | Existing tests assert `resident_gate == [TENURE_HOLD]` for cases with reports and no inventory. Adding a missing-inventory reason there would change existing behaviour. | Applied (decision D1): inventory reasons only when the inventory field is present; the hold still refuses managed cases without inventory and the view reports the gap. |
| PC-003 | Gate reasons are visible to many roles. Household references, sources, owners or digests in them would leak. | Applied (D3): counts only; canary test on the gate text and on withheld-role detail. |
| PC-004 | A malformed persisted field must fail closed but must not break unrelated manual or hazard routes. | Applied: malformed handling lives only in the view and the two consumers; test hazard and decision recording on a corrupted case. |
| PC-005 | `RESIDENT_FIELDS` is also used by retention listing and role copying. Adding the raw field must still keep `tenure_review_required` after deletion. | Applied: the flag is not in the tuple; deletion test asserts it remains and scope stays held. |

## Residual risks accepted

* Declared coverage is caller supplied; the primitive cannot prove it is the actual household list.
* Cases with reports but no inventory keep the previous message; the gap appears only in the view.
* SQLite and JSON only; MSSQL is not run and not claimed.
