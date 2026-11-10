---
title: Issue 131 case-local expected-household inventory primitive review
ms.date: 2026-11-10
task_id: 131-household-inventory-1110
---

## Review execution

* Execution: executed once after implementation. Authored by the implementing coordinator, not independent, because nested agents were prohibited. Independent exact-head assessment remains required before publication.
* Boundary assessed: the working-tree diff against base `fe59ef56a0084dd975fd7e5c342670bb8f788fb0` (5 modified files plus the dated RPI records), the plan, details, critique and changes records, and the focused validation logs.

## Outcome

Conformant with open follow-ups routed to later work. No blocking finding; no change was made after review.

## Scope and boundary checks

| Check | Result |
| --- | --- |
| Only `resident_decisions.py`, Core and API test files, Core and API READMEs, dated records changed | Pass |
| No store, sqlstore, server, projection, schema, endpoint, UI or role edits | Pass |
| Strict closed schema, no client digest or approval keys, empty/duplicate/over-100/mismatched/non-latest links rejected before mutation | Pass (tests) |
| Digest server-derived; report changes make links stale; no implicit supersession | Pass (tests) |
| Missing, Unknown, stale or malformed link refuses gate and `scope_record`, then keeps `TENURE_HOLD`; full current data releases nothing | Pass (tests) |
| Unmanaged legacy cases unchanged; reports-only cases keep exactly the existing hold text | Pass (tests) |
| Deletion removes new resident data and keeps `tenure_review_required` | Pass (tests) |
| Privacy: new fields in `INTAKE_FIELDS`, popped by existing projection and detail paths; gate text is count-only | Pass (core and served-handler canaries) |
| SQL writer-fence, competing writer, report-version race, committed-unconfirmed | Pass on SQLite SqlStore; MSSQL not run, not claimed |

## Findings

| ID | Severity | Finding | Routing |
| --- | --- | --- | --- |
| RV-001 | Low | The served-handler test asserts a non-200 for `scope_record` with a minimal body, which could pass for body-validation reasons alone. Core tests prove the inventory refusal reason directly. | Later Plan: strengthen the API assertion with a full valid scope body |
| RV-002 | Low | Managed detection now also treats a present-but-null inventory or non-list `tenure_reports` as managed. This is intended fail-closed behaviour, tested, but slightly widens the hold beyond truthy reports. | Later Research: confirm with the owner |
| RV-003 | Info | `ruff format` was not applied because base files are not format clean; only `ruff check` and `mypy` were run. | Later cleanup, separate task |
| RV-004 | Info | Roster completeness, identity, authority appointments, Legal and Finance handoffs, universal pre-offer integration and any hold release remain pending by design. | Separate owner decisions |

## Residual limits

* Caller-declared coverage is not proof of actual household completeness.
* Historical numeric corrective balance is UNKNOWN and no post-review grant is claimed.
