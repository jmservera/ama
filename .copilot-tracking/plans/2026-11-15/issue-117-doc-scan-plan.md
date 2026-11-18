<!-- markdownlint-disable-file -->
# RPI Plan: Issue 117 Document Malware Scan Quarantine Gate

## Task Metadata

* Task ID: issue-117-doc-scan
* Task slug: issue-117-doc-scan
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-117-doc-scan-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/issue-117-doc-scan-plan-critique.md

## Executive Summary

This plan closes the fail-open gaps in document malware scanning and quarantine enforcement for Issue #117 (`Uploads are scanned before availability`). It establishes canonical scan-verdict helpers and a first-class `"failed"` verdict in `zava_forward.core.doc_controls` (while preserving `#395` exception propagation, Defender pending-retry semantics, and `SqlStore` touch-tracking persistence), then wires fail-closed `scan_status == "clean"` checks across document download, AI document reading and redaction derivatives, structured assistants, employee case chat facts, staff projection summaries, versioned home-case views and link snapshots, form staging/listing/review/export, procurement commitment checks, case checklist/funding/booking/technical sign-off gates, task queue freshness, and resident-facing document request/summary views, backed by focused unit tests in `src/core/tests` and `src/api/tests`.

### User Decisions and Requirements Highlights

* ✅ Uploads must remain quarantined and unavailable for download or derivative use until `scan_status == "clean"` is recorded, failing closed on `pending`, `infected`, `failed`, or missing scan status (Issue #117).
* ✅ Do not add new HTTP routes in `src/api/src/zava_forward/api/server.py` so `test_role_endpoint_inventory.py` remains intact.
* ✅ Run Focused validation tier checks only (`src/core` unit tests, `src/api` unit tests, `ruff check`, `ruff format --check`, and `mypy`); do not run `tools/rpi-checks.py`, and commit locally with `Refs #117` without pushing.

### What You May Not Know

* Document records in the codebase can carry nested `doc["scan"]["status"]`, top-level `doc["scan_status"]`, or both; resolving them through one canonical `scan_status(doc)` function prevents split-brain bypasses where one field says `"clean"` while the other is `"infected"`, `"failed"`, or malformed.
* Legacy unit tests for unrelated capabilities construct synthetic metadata-only case document dicts without `Store.add_document` (omitting `generated`, `scan`, and `scan_status`), whereas every uploaded document sets `generated=False` and/or carries `scan`/`scan_status`. Using strict `is_clean_document` on byte/content/staging paths and `is_available_case_document` on case-collection consumers keeps every upload fail-closed on missing scan status without breaking synthetic metadata-only fixtures.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Ensure document uploads remain quarantined and unavailable for download or derivative use until a clean malware scan verdict (`scan_status == "clean"`) is recorded, failing closed on `pending`, `infected`, `failed`, or missing scan status (Issue #117; `.copilot-tracking/research/2026-11-15/issue-117-doc-scan-research.md`).
* Prove the fail-closed scan gate across download and derivative-use surfaces with focused unit tests in `src/core` and `src/api` (Caller prompt).
* Do not add new HTTP routes in `src/api/src/zava_forward/api/server.py` unless `test_role_endpoint_inventory.py` is preserved; zero new HTTP routes will be added (Caller prompt; C24).
* Execute Focused validation tier checks (`src/core` unit tests, `src/api` unit tests, `mypy`, `ruff check`, `ruff format --check`) without running `tools/rpi-checks.py` (Caller prompt).
* Commit all code, test, and `.copilot-tracking/` artifacts locally on `feat/demo-117-doc-scan` with `Refs #117` and the Copilot trailer without pushing (Caller prompt).

## Goals

* Introduce first-class `"failed"` scan verdict support and canonical fail-closed scan-status helpers in `zava_forward.core.doc_controls`.
* Block document download and every derivative document consumer whenever an uploaded document's resolved scan status is `pending`, `infected`, `failed`, `mismatch`, missing, malformed, or conflicting.
* Prove fail-closed quarantine behavior across download and derivative consumers with focused unit tests while keeping existing `src/core` and `src/api` test suites, `mypy`, and `ruff` clean.

## Scope and Non-Goals

### In Scope

* Canonical scan verdict normalization (`"clean"`, `"pending"`, `"infected"`, `"mismatch"`, `"failed"`), missing-scanner `RuntimeError` guard while preserving `#395` scanner/storage exception propagation and Defender retryable `"pending"` tag semantics, `SqlStore` `_touch(case_id)` persistence and `scan_status` synchronization in `_scan_stored`, and unified `scan_status`, `is_clean_document`, `is_clean_upload`, `is_available_case_document`, and `is_rescan_pending` helpers in `src/core/src/zava_forward/core/doc_controls.py` and `document_rescan.py`.
* Fail-closed upload availability enforcement across `store.py`, `home_case.py`, `projection.py`, `data_protection.py`, `ai_tasks.py`, `assistants.py`, `chat_case_answers.py`, `forms.py`, `procurement.py`, `signoffs.py`, `taskqueues.py`, `resident_documents.py`, and `resident_summary.py`.
* Focused unit tests in `src/core/tests/` and `src/api/tests/` covering `clean`, `pending`, `infected`, `failed`, `mismatch`, and missing/malformed/conflicting scan status across download, `SqlStore` rescan persistence, and derivative uses.

### Non-Goals

* Adding or modifying HTTP routes in `src/api/src/zava_forward/api/server.py`.
* Live Azure Storage Defender infrastructure provisioning in Bicep or DPO/Legal sign-off on retention schedules.
* Running `tools/rpi-checks.py` or pushing commits to `origin`.

## Functional Requirements

* Support `"failed"` as a valid persisted malware scan verdict in `_scan_result` alongside `("clean", "pending", "infected", "mismatch")`, raise `RuntimeError` if `self.scanner is None` or a malformed/unsupported verdict is returned without coercing arbitrary objects, preserve retryable `"pending"` semantics in `DefenderForStorageScanner.scan` (`#395`), touch the case (`_touch(case_id)`) and synchronize `doc["scan_status"]` in `_scan_stored` so `SqlStore` persists rescan updates across reopen, and keep explicit `"failed"` verdicts quarantined until rescanned clean.
  * Observable acceptance criteria: `_scan_result` accepts `"failed"` and rejects malformed/unsupported verdicts with `RuntimeError`; `DefenderForStorageScanner.scan` preserves `#395` retryable `"pending"` behavior; `_scan_stored` persists updates in `SqlStore` across reopen and synchronizes `doc["scan_status"]` when present.
* Resolve nested `doc["scan"]["status"]` and top-level `doc["scan_status"]` through one fail-closed `scan_status(doc)` helper and guard `DocControlsMixin.require_clean`, `ensure_scanned`, `rescan_pending`, `rescan_document`, and `document_rescan._pending`.
  * Observable acceptance criteria: `require_clean` raises `DocumentUnavailable` whenever resolved status is `pending`, `infected`, `failed`, `mismatch`, missing/`None`, malformed `scan`, or disagreed between `scan` and `scan_status`; `ensure_scanned` auto-scans on first use only when `scan_status(doc) == "pending"` or neither `scan` nor `scan_status` is present on an ungenerated document, and never overwrites `infected`, `failed`, `mismatch`, or malformed scan markers.
* Prevent quarantined uploads from being used in any derivative workflow (`Store.read_document` including `reviewed_redacted`/`necessity_exception`, `ai_tasks.run_document`, `data_protection.document_model_hold` prior to `is_actual`, `ai_tasks.source_labels`, `assistants.capture`, `chat_case_answers.case_facts`, `projection.redact_staff_detail` document summaries, `home_case.links` and `home_case.view`, `forms.list_candidates`, `procurement._capacity_source`, `Store.checklist` preserving `(KeyError, TypeError)` on malformed items, `Store.focus`, `signoffs._missing_evidence`, `taskqueues.context`, `resident_documents`, and `resident_summary`).
  * Observable acceptance criteria: Non-clean uploads (`pending`, `infected`, `failed`, `mismatch`, missing/malformed scan status) cannot be downloaded, summarized/extracted by AI (including under `ZF_DATA_MODE=actual` with `reviewed_redacted`), staged/listed/exported in forms, used as procurement capacity commitments, frozen into `home_case` links/views, counted as present evidence in checklists/funding/booking/technical gates or freshness windows, cited in assistants or employee chat facts, or treated as satisfying a resident document request, while resident views surface `"failed"` and `"unknown"` non-clean uploads in `SCAN_TEXT` and `needed_from_you`.

## Non-Functional Requirements

* Backwards compatibility with existing route inventory and synthetic metadata-only unit test fixtures.
  * Objective threshold or evaluation condition: Zero new HTTP routes in `server.py`; 100% pass rate across existing and added `src/core` and `src/api` unit test suites.
  * Operating condition or verification approach, if needed: Run `unittest discover` inside `src/core` and `src/api` (including `test_role_endpoint_inventory.py` and `src/core/tests/test_document_rescan.py`).
  * Observable acceptance criteria: All `src/core` and `src/api` unit tests pass with zero regressions.
* Static type safety and formatting compliance.
  * Objective threshold or evaluation condition: Zero errors from per-project `mypy`, `ruff check .`, and `ruff format --check .` in `src/core` and `src/api`.
  * Operating condition or verification approach, if needed: Run `ruff check . && ruff format --check . && mypy` inside `src/core` and inside `src/api` per `src/README.md`, using strict PEP 484 typing on `src/core` tests and preserving formatting exclusions on legacy `src/api/tests/test_document_controls.py`.
  * Observable acceptance criteria: Per-project `ruff` and `mypy` exit with code `0`.

## Acceptance Criteria

* Document uploads with `scan_status` / `scan.status` equal to `pending`, `infected`, `failed`, `mismatch`, missing/`None`, malformed, or conflicting (`scan` vs `scan_status`) are rejected with `DocumentUnavailable` on download and AI document read, and remain unavailable across derivative case, `home_case`, projection, AI, assistant, chat, form, procurement, sign-off, task-queue, and resident-request surfaces until `scan_status == "clean"` is recorded.
* Explicit `"failed"` scan verdicts are persisted, synchronized across `scan` and `scan_status` (including `SqlStore` reopen after rescan), and remain quarantined while preserving `#395` exception/retry contracts in `src/core/tests/test_document_rescan.py`.
* No HTTP routes are added or removed in `src/api/src/zava_forward/api/server.py`, and `test_role_endpoint_inventory.py` passes.
* Per-project `unittest`, `ruff check .`, `ruff format --check .`, and `mypy` in `src/core` and `src/api` all pass.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-plan.md                                                                            |
| Phase details                    | .copilot-tracking/details/2026-11-15/issue-117-doc-scan-phase-details.md                                                                 |
| Latest critique                  | .copilot-tracking/reviews/2026-11-15/issue-117-doc-scan-plan-critique.md with Revise verdict; PC-001 through PC-006 directly resolved    |
| Relevant research                | .copilot-tracking/research/2026-11-15/issue-117-doc-scan-research.md                                                                     |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md is created by implementation as its evidence record                   |
| Planning execution and readiness | Complete and Ready for `rpi-implement`                                                                                                   |
| Continuation context             | Parent return to confirmed automatic RPI Agent (`Plan` -> `Implement` -> `Review`)                                                       |

## Sources

* `.copilot-tracking/research/2026-11-15/issue-117-doc-scan-research.md`: Codebase evidence `C1`–`C24` across `src/core` and `src/api` upload, scan, download, derivative-use, and test contracts.
* `docs/adrs/0002-pilot-readiness-architecture.md`: Document store and Defender malware scan tag architecture for Issue #117.
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: DH-003 and AC-115 quarantine requirements for unsafe or unvalidated uploads across residents, staff readers, and models.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Canonical Malware Scan Verdict and Quarantine Gate (`doc_controls` & `document_rescan`)

* Intent: Add `"failed"` scan verdict support, fail-closed scanner error handling, and canonical `scan_status` / availability helpers in `doc_controls.py` and `document_rescan.py`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add `"failed"` verdict, `SqlStore` rescan persistence, and canonical `scan_status` helpers in `doc_controls.py`

* Requirement and evidence: Support `"failed"`, missing, malformed, and dual `scan`/`scan_status` document records fail-closed while preserving `#395` exception/retry semantics (`C2`, `C3`, `C21`, `PC-001`, `PC-002`).
* Expected result: `doc_controls.py` exports `VERDICTS` including `"failed"`, `scan_status`, `is_clean_document`, `is_clean_upload`, `is_available_case_document`, and `is_rescan_pending`; `scan_new_document` and `_scan_stored` raise `RuntimeError` if `self.scanner is None` and preserve `#395` exception propagation; `_scan_stored` calls `self._touch(case_id)` and synchronizes `doc["scan_status"]`; `require_clean`, `ensure_scanned`, `rescan_pending`, and `rescan_document` enforce canonical fail-closed semantics.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-117-doc-scan-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Align `document_rescan._pending` with canonical `is_rescan_pending`

* Requirement and evidence: Prevent `AttributeError` on malformed `scan` and honor top-level `scan_status` in `document_rescan._pending` (`C4`, `PC-004`).
* Expected result: `document_rescan._pending` uses `doc_controls.is_rescan_pending(doc)` safely without misclassifying `failed`, `infected`, `mismatch`, `clean`, or malformed records.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/issue-117-doc-scan-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Derivative-Use Quarantine Enforcement Across `src/core`

* Intent: Ensure non-clean uploads (`pending`, `infected`, `failed`, `mismatch`, missing/malformed/conflicting scan status) cannot be consumed by AI model dispatch, assistants, employee chat, staff projections, `home_case` views/snapshots, checklists/gates, forms, procurement, task queues, or resident request satisfaction.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Gate case checklists, focus, `home_case`, sign-offs, forms, procurement, and task queues on clean uploads

* Requirement and evidence: Close derivative workflow gates in `store.py`, `home_case.py`, `signoffs.py`, `forms.py`, `procurement.py`, and `taskqueues.py` (`C6`, `C12`, `C14`, `C15`, `C16`, `C20`, `PC-003`, `PC-004`, `PC-005`).
* Expected result: `Store.checklist` evaluates `d["kind"]` before `is_available_case_document(d)` (preserving `(KeyError, TypeError)` for `_evidence_missing`); `Store.focus`, `home_case.links`, `home_case.view`, `signoffs._missing_evidence` (preserving `usable_only: bool = False`), and `taskqueues.context` filter via `is_available_case_document`; `forms.list_candidates` and `procurement._capacity_source` filter via `is_clean_upload`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-117-doc-scan-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Gate AI document inspection, structured assistants, employee case chat facts, projection summaries, and resident document views

* Requirement and evidence: Prevent model/assistant/chat/projection/resident derivative use of uncleaned uploads in `data_protection.py`, `ai_tasks.py`, `assistants.py`, `chat_case_answers.py`, `projection.py`, `resident_documents.py`, and `resident_summary.py` (`C7`–`C11`, `C17`, `C18`, `C22`, `C23`, `PC-003`).
* Expected result: `ai_tasks.run_document` enforces `store.require_clean(doc)` after scalar validation; `data_protection.document_model_hold` blocks any scan-tagged non-clean document **before** `if is_actual:`; `ai_tasks.source_labels`, `assistants.capture`, `chat_case_answers.case_facts`, and `projection.redact_staff_detail` document summaries exclude/withhold quarantined uploads via `is_available_case_document`; `resident_documents` and `resident_summary` add `"failed"` to `SCAN_TEXT`, require `d.scan_status == "clean"` before marking a request recorded/provided, and surface non-clean (`!= "clean"`) non-generated presented uploads in `needed_from_you`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/issue-117-doc-scan-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Unit Tests and Tier Validation

* Intent: Prove fail-closed quarantine behavior across download, `SqlStore` rescan reopen, and all derivative uses for `clean`, `pending`, `infected`, `failed`, `mismatch`, and missing/malformed/conflicting scan status, and pass per-project `unittest`, `ruff`, and `mypy`.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add focused unit tests in `src/core/tests` and `src/api/tests` and run per-project Focused validation suite

* Requirement and evidence: Prove download and derivative-use quarantine gates without adding HTTP routes (`C20`–`C24`, `PC-001`–`PC-006`).
* Expected result: Extended unit tests in `src/core/tests/test_technical_evidence_usability.py`, `src/core/tests/test_resident_documents.py`, `src/core/tests/test_document_rescan.py`, and `src/api/tests/test_document_controls.py` pass alongside full `src/core` and `src/api` unittest suites (including `test_role_endpoint_inventory.py`), per-project `ruff check .`, `ruff format --check .`, and `mypy`.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/issue-117-doc-scan-phase-details.md

## Dependencies

* `zava_forward.core` editable/installed package in worktree Python environment: Required so `src/core` and `src/api` unit tests, `mypy`, and `ruff` import updated `doc_controls` helpers cleanly.
* `src/api/tests/test_role_endpoint_inventory.py`: Enforces unchanged route inventory on `src/api/src/zava_forward/api/server.py`.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [Critical]: Scanner exception and Defender tag coercion breaks `#395` rescan contracts | resolved | Updated `P01-T01` to support explicit `"failed"` verdicts while preserving `_scan_result` `RuntimeError` propagation, `DefenderForStorageScanner` retryable `"pending"` tags (`"Error"`, `"Not scanned"`), and raising `RuntimeError` when `self.scanner is None`. |
| `PC-002` [High]: `SqlStore` drops `_scan_stored` persistence when untouched and leaves `scan_status` unsynchronized | resolved | Updated `P01-T01` and `P03-T01` so `_scan_stored` calls `self._touch(case_id)` and syncs `doc["scan_status"]`, `rescan_document`/`replace_document` use `d.get("generated")`, `rescan_pending` does not miscount `"failed"` as `"pending"`, and `SqlStore` reopen persistence is unit-tested. |
| `PC-003` [High]: Four derivative/projection paths remain fail-open (`home_case`, `forms.list_candidates`, pre-`is_actual` `document_model_hold`, `resident_summary.needed_from_you`) | resolved | Added `home_case.py` (`links`, `view`), `projection.py` summary hold, `forms.list_candidates` `is_clean_upload`, pre-`is_actual` scan check in `document_model_hold`, and `not document.get("generated") and document["scan_status"] != "clean"` in `resident_summary.needed_from_you` across `P02-T01`, `P02-T02`, and `P03-T01`. |
| `PC-004` [High]: Nonexistent symbol and test-file targets in `P01-T02`, `P02-T01`, and `P03` | resolved | Replaced anchors with exact repository targets: `document_rescan._pending`, `src/core/tests/test_document_rescan.py`, `signoffs._missing_evidence` (retaining `usable_only: bool = False`), `form_review._document`, `procurement._capacity_source`, and `src/core/tests/test_quality_procurement.py` / `src/api/tests/test_procurement_api.py`. |
| `PC-005` [Medium]: `Store.checklist` filtering must preserve `KeyError` and `TypeError` on malformed items | resolved | Updated `P02-T01` so `Store.checklist` evaluates `d["kind"]` before `is_available_case_document(d)`, preserving `(KeyError, TypeError)` for `Store._evidence_missing` (`test_gates.py`). |
| `PC-006` [Medium]: Per-project `ruff` and `mypy` execution and strict typing / legacy format-exclude rules | resolved | Updated `P03-T01` to run `ruff check . && ruff format --check . && mypy` per project inside `src/core` and `src/api`, enforce strict PEP 484 typing in `src/core/tests`, and avoid reformatting excluded legacy `src/api/tests/test_document_controls.py`. |

## Follow-Up Items

* Provision live Azure Storage Defender malware scanning event/tag infrastructure in Bicep and deployment verification (outside this `src/core` + `src/api` code gate slice; tracked under ADR 0002 / cloud readiness backlog).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md
* Ready phase or task: P01 (P01-T01)
* Remaining provisional question or blocker: None
