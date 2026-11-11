---
title: Staff intake 132 C4 changes
ms.date: 2026-11-09
---

Corrective cycle C4 of five total (cycles 1 to 3 spent, one remains). Parent task `staff-intake-132`.

## Changes

| Finding | Change | Evidence |
| --- | --- | --- |
| 1 High: no resident binding | `_binding` reads the work order's bound scope revision, checks it is still current, passes `context_revision` to `submit_quality`; 409 if missing or changed; no waiver. View shows a blocker for legacy unbound receipts. | `test_recorder_is_denied_and_independent_qa_accepts`, corrector, acknowledger, worker replacement, unbound tests |
| 2 High: corrections not in item | `correct` updates the matching `rec["items"]` evidence inside the same operation; originals and history kept; survives restart. | `test_correction_updates_current_quality_item_and_survives_restart`, `test_correction_failure_leaves_item_and_history_unchanged` |
| 3 High: digest default | New evidence needs an explicit 64 hex digest (400), stale compare (409); replay of a stored `capture_ref` matched on the stored receipt before pack checks. | `test_explicit_valid_digest_is_required_for_new_evidence`, offline and lost-response tests |
| 4 Medium: JS duplicate error | Duplicate is a reconciliation: receipt refreshed, polite status notice, no error. | `test_lost_response_retry_reconciles_without_error_or_second_record` |

Files: `staff_intake.py`, `staff-intake.js`, `test_staff_intake_api.py`, `test_staff_intake_browser.py`, both READMEs.

## Validation (focused tier)

* `test_staff_intake_api` 23 OK on SQLite; same 23 on MSSQL (disposable loopback container) exit 0.
* Browser plus axe, 5 states, 2 tests OK under nonqueued `flock -n`.
* Impacted API suites 178 OK (23 skipped opt-in); core `test_job_pack`, `test_quality_procurement` 146 OK.
* ruff format and check clean; strict mypy clean on `staff_intake.py`.
* Red first: 8 of 23 failed on the old source.

## Limits

* Cross-process stale check and commit race remains (needs a shared persistence hook, out of owned scope; PC-005).
* Evidence recorded before C4 has no binding and is blocked, not repaired.
* AC5 escalation write path stays a gap. No QA, legal, live or assistive technology acceptance; axe is not a WCAG claim.
