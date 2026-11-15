<!-- markdownlint-disable-file -->
# RPI Changes: Issue 117 Document Malware Scan Quarantine Gate

## Metadata

* Task ID: issue-117-doc-scan
* Related plan: .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-117-doc-scan-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02, P03, P03-T01
* All remaining active-plan markers: None
* Status basis: All planned phases and tasks (`P01` through `P03`) implemented and verified with Focused-tier unit tests, `ruff`, and `mypy` in `src/core` and `src/api`.

## Execution Summary

Implemented canonical fail-closed malware scan verdict normalization (`P01`), derivative-use quarantine enforcement across `src/core` (`P02`), and focused unit tests with full static and runtime validation across `src/core` and `src/api` (`P03`), leaving `server.py` HTTP routes untouched.

## Completed Work

### P01: Canonical Malware Scan Verdict and Quarantine Gate

* `P01-T01` (`src/core/src/zava_forward/core/doc_controls.py`): Added `"failed"` to `VERDICTS`, preserved strict tuple/type checks in `_scan_result`, added typed fail-closed helpers `scan_status`, `is_clean_document`, `is_clean_upload`, `is_available_case_document`, and `is_rescan_pending`, guarded `scan_new_document` and `_scan_stored` when `self.scanner is None`, updated `require_clean`, `ensure_scanned`, `rescan_pending`, and `rescan_document`, and added `SqlStore` `_touch(case_id)` plus top-level `scan_status` synchronization in `_scan_stored`.
* `P01-T02` (`src/core/src/zava_forward/core/document_rescan.py`): Updated `_pending(doc)` to delegate to `is_rescan_pending(doc)`.

### P02: Derivative-Use Quarantine Enforcement Across `src/core`

* `P02-T01` (`store.py`, `home_case.py`, `signoffs.py`, `forms.py`, `procurement.py`, `taskqueues.py`): Gated `Store.checklist` (preserving `(KeyError, TypeError)` behavior on malformed items), `Store.focus`, `home_case.links`, `home_case.view`, `signoffs._missing_evidence`, and `taskqueues.context` on `is_available_case_document`, and gated `forms.list_candidates` and `procurement._capacity_source` on `is_clean_upload`.
* `P02-T02` (`ai_tasks.py`, `data_protection.py`, `assistants.py`, `chat_case_answers.py`, `projection.py`, `resident_documents.py`, `resident_summary.py`): Enforced `store.require_clean(doc)` in `ai_tasks.run_document`, blocked non-clean uploads in `data_protection.document_model_hold` ahead of `actual_mode`, excluded quarantined uploads from `ai_tasks.source_labels`, `assistants.capture`, and `chat_case_answers.case_facts`, withheld quarantined document summaries in `projection.redact_staff_detail`, and updated resident document views/summaries to report `"failed"` and require `scan_status == "clean"` before treating a document request as provided.

### P03: Focused Unit Tests and Tier Validation

* `P03-T01` (`src/core/tests/test_technical_evidence_usability.py`, `src/core/tests/test_document_rescan.py`, `src/core/tests/test_resident_documents.py`, `src/api/tests/test_document_controls.py`): Added focused unit tests covering `clean`, `pending`, `infected`, `failed`, `mismatch`, missing/`None`, malformed, and conflicting (`scan` vs `scan_status`) states across download, `SqlStore` rescan persistence across reopen, and all derivative consumers (`Store.checklist`, `Store.focus`, `home_case.links` and `home_case.view`, `forms.list_candidates`, `procurement._capacity_source`, `signoffs`, `taskqueues.context`, `ai_tasks`, `data_protection.document_model_hold` under `ZF_DATA_MODE=actual`, `assistants.capture`, `chat_case_answers.case_facts`, `projection.redact_staff_detail`, `resident_documents`, and `resident_summary`).

## Implementation-Time Plan and Detail Updates

None.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `ruff check . && ruff format --check .` | `src/core` | Passed | `All checks passed! 289 files already formatted` |
| `mypy` | `src/core` | Passed | `Success: no issues found in 342 source files` |
| `ruff check . && ruff format --check .` | `src/api` | Passed | `All checks passed! 199 files already formatted` |
| `mypy` | `src/api` | Passed | `Success: no issues found in 283 source files` |
| `unittest` focused suite (26 modules) | `src/core/tests` | Passed | `Ran 537 tests in 296.257s — OK (skipped=20)` |
| `unittest` focused suite (15 modules incl. `test_document_controls`, `test_role_endpoint_inventory`) | `src/api/tests` | Passed | `Ran 452 tests in 614.740s — OK (skipped=61)` |
| `tools/rpi-checks.py` | repository gate | Skipped | Explicitly excluded by caller prompt (`Focused` validation tier; do NOT run `tools/rpi-checks.py`) |
| Post-rebase (`fa6f8d1dd` -> `e9c31f7fa`) `ruff` + `mypy` | `src/core` & `src/api` | Passed | `src/core` (293 formatted, 346 mypy files) & `src/api` (213 formatted, 297 mypy files) clean in isolated `PYTHONNOUSERSITE=1` worktree venv |
| Post-rebase (`fa6f8d1dd` -> `e9c31f7fa`) focused unit + rename suites | `src/core`, `src/api`, `tools/` | Passed | `src/core` 64 tests OK (`skipped=20`), `src/api` 44 tests OK (`test_document_controls`, `test_role_endpoint_inventory`), `tools/rename-zava-tests.py` 25 tests OK |

## Pre-Review Reconciliation

* Plan markers and phase details: reconciled (`P01`, `P02`, `P03` and all `P0x-T0x` checked)
* Completed-work evidence and handoff prose: reconciled
* Validation, blockers, remaining work, and follow-up items: reconciled
* Review readiness: ready for `rpi-review`

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-plan.md, `## Follow-Up Items`
* Provision live Azure Storage Defender malware scanning event/tag infrastructure in Bicep and deployment verification (outside this `src/core` + `src/api` code gate slice; tracked under ADR 0002 / cloud readiness backlog).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan (completed: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02, P03, P03-T01; remaining: None)
* Validation coverage: Focused tier complete (`src/core` ruff/mypy + 537 unit tests; `src/api` ruff/mypy + 452 unit tests including `test_document_controls` and `test_role_endpoint_inventory`)
* Blockers: None
* Current plan and detail updates: None
* Planning and critique state: ready (`PC-001` through `PC-006` resolved)
* Follow-up items: Azure Storage Defender infrastructure wiring
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (`confirmed automatic RPI Agent`)
