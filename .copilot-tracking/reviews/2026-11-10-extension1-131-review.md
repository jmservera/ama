---
title: Issue 131 E1 missing households key (review)
ms.date: 2026-11-10
task_id: 131-extension1-1110
---

## Execution and outcome

* Review executed once, authored by the implementing worker; not independent. The independent exact-head assessment by reviewer 8f078 is required before publication.
* Boundary: dirty source on merge `356dc58` (`resident_decisions.py`, `test_resident_decisions.py`) plus the RPI records.
* Outcome: conformant for the single authorized residual (missing `households` key). No material finding open in scope.

## Findings against the plan

| Item | Result |
| --- | --- |
| Missing `households` key accepted as null and extendable | Fixed: key presence is required for every revision in the shared validator used by the view and the writer. Regression failed before (4 failures, JSON and SQLite) and passes after. |
| Legitimate Unknown and stale history not rejected | Explicit null control reads Unknown and accepts the next revision; the earlier stale-digest control still passes. |
| Hold safety | `TENURE_HOLD` stays last; nothing releases or permits scope; refusal paths unchanged. |
| Scope | Two source files only plus ordinary merge of main. No README, schema, UI, API, field or permission change. |
| Checks | Core 149 skipped OK, API OK, ruff check, format check and mypy (296 files) all 0; the first mypy failure was a missing dev dependency introduced by main, restored in the owned venv and recorded. |

## Routed follow-ups

* RV-001 (Low, carried): stronger API `scope_record` assertion for the refusal reasons.
* RV-002 (carried): approved process to resolve identity; the identity reason stays for linked reports.
* RV-003: MSSQL not run and not claimed.
* Accounting: E1 used, four extension corrections remain subject to Root; no automatic E2; previous minimum 0 preserved.
* Roster completeness, authority appointments, Legal and Finance handoffs, universal pre-offer integration and any hold release remain pending. Not universal C1 or C2 compliance.
