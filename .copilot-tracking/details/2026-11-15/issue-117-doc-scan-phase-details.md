<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue 117 Document Malware Scan Quarantine Gate

## Metadata

* Task ID: issue-117-doc-scan
* Task slug: issue-117-doc-scan
* Related plan: .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-117-doc-scan-research.md, docs/adrs/0002-pilot-readiness-architecture.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md

## Phase Index

| Phase ID | Name                                                                                  | Status | Detail sections          |
|----------|---------------------------------------------------------------------------------------|--------|--------------------------|
| P01      | Canonical Malware Scan Verdict and Quarantine Gate (`doc_controls` & `document_rescan`) | ready  | P01, P01-T01, P01-T02    |
| P02      | Derivative-Use Quarantine Enforcement Across `src/core`                               | ready  | P02, P02-T01, P02-T02    |
| P03      | Focused Unit Tests and Tier Validation                                                | ready  | P03, P03-T01             |

<!-- rpi:phase id=P01 -->
## P01: Canonical Malware Scan Verdict and Quarantine Gate (`doc_controls` & `document_rescan`)

### Context

Research (`C2`, `C3`, `C4`, `C21`) showed that `doc_controls._scan_result` rejects `"failed"` with `RuntimeError`, `DefenderForStorageScanner.scan` misclassifies non-clean/non-malicious Defender error tags as `"pending"`, scanner failures lack a `"failed"` quarantine fallback, and `DocControlsMixin` / `DocumentRescanRunner` inspect only nested `doc["scan"]` while assuming it is a `dict`.

### Intent

Establish one canonical, fail-closed scan verdict and status resolution layer in `doc_controls.py` and `document_rescan.py` supporting `"clean"`, `"pending"`, `"infected"`, `"mismatch"`, and `"failed"`, plus missing, malformed, and dual `scan` / `scan_status` records.

### Boundaries

* Included: `src/core/src/zava_forward/core/doc_controls.py`, `src/core/src/zava_forward/core/document_rescan.py`.
* Excluded: HTTP route table in `src/api/src/zava_forward/api/server.py`; Bicep templates under `infra/`.

### Likely Targets

* `src/core/src/zava_forward/core/doc_controls.py`: Verdict constants, `DefenderForStorageScanner.scan`, canonical status/availability predicates, and `DocControlsMixin` scan/quarantine methods.
* `src/core/src/zava_forward/core/document_rescan.py`: Pending-scan detection in `DocumentRescanRunner.has_pending`.

### Dependencies

* None.

### Validation Expectations

* Unit tests verify `"failed"` verdict creation, Defender tag mapping (`None`/`""` -> `"pending"`, `"No threats found"` -> `"clean"`, `"Malicious"` -> `"infected"`, other tags -> `"failed"`), scanner exception fallback to `"failed"`, and `require_clean` / `ensure_scanned` behavior across `pending`, `infected`, `failed`, `mismatch`, missing, malformed, and conflicting `scan`/`scan_status`.

### Completion Evidence

* Updated `doc_controls.py` and `document_rescan.py` passing `mypy`, `ruff`, and unit tests.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add `"failed"` verdict, `SqlStore` rescan persistence, and canonical `scan_status` helpers in `doc_controls.py`

#### Context

`doc_controls.py` owns `LocalSignatureScanner`, `DefenderForStorageScanner`, `_scan_result`, and `DocControlsMixin` (`C2`, `C3`, `PC-001`, `PC-002`). Callers and projections may represent scan state via `doc["scan"] = {"status": ...}` and/or `doc["scan_status"]`. Legacy test `test_document_without_scan_field_is_scanned_on_first_use` (`C21`) deletes `"scan"` completely from an uploaded document (`generated=False`, neither `"scan"` nor `"scan_status"` present) and expects `ensure_scanned` to run `_scan_stored` once before `require_clean`, while `src/core/tests/test_document_rescan.py` (`#395`, `PC-001`) requires `_scan_result` to raise `RuntimeError` without coercing arbitrary objects on malformed/unsupported verdicts, requires `DefenderForStorageScanner.scan` to keep returning `"pending"` for `{}`, `DocumentStoreError`, `"Error"`, and `"Not scanned"`, and requires `scan_new_document`, `rescan_document`, and `rescan_pending` to propagate scanner/storage exceptions unchanged.

#### Intent

Make `doc_controls.py` fail closed on every non-clean, failed, missing, malformed, or conflicting scan state while preserving `#395` exception/retry semantics and `SqlStore` touch-tracking persistence.

#### Boundaries

* Included:
  * Add `VERDICTS = ("clean", "pending", "infected", "mismatch", "failed")` and allow `"failed"` in `_scan_result` while keeping exact tuple/str type checks (never stringifying malformed values) and raising `RuntimeError` on unsupported verdicts such as `"unknown"`.
  * Keep `DefenderForStorageScanner.scan` returning `("pending", ...)` for `DocumentStoreError`, missing tags, and non-clean/non-malicious tags (`"Error"`, `"Not scanned"`), preserving `#395` retry sweeps (`PC-001`).
  * Add canonical helpers:
    * `scan_status(doc)`: returns `None` if `not isinstance(doc, Mapping)`. Inspects `"scan"` (valid only when `isinstance(doc["scan"], Mapping)` and `isinstance(doc["scan"].get("status"), str)` and non-empty and in `VERDICTS`) and `"scan_status"` (valid only when `isinstance(doc["scan_status"], str)` and non-empty and in `VERDICTS`). If neither key is present, returns `None`. If `"scan"` is present and malformed/unsupported, returns `None`. If `"scan_status"` is present and invalid/unsupported, returns `None`. If both keys are present and disagree, returns the non-`"clean"` status if one is `"clean"`, else `None` (never `"clean"`). Otherwise returns the resolved status string.
    * `is_clean_document(doc)`: `isinstance(doc, Mapping) and (doc.get("generated") is True or scan_status(doc) == "clean")`.
    * `is_clean_upload(doc)`: `isinstance(doc, Mapping) and not doc.get("generated") and scan_status(doc) == "clean"`.
    * `is_available_case_document(doc)`: returns `False` if `not isinstance(doc, Mapping)`; `True` if `doc.get("generated") is True`; `scan_status(doc) == "clean"` whenever `doc.get("generated") is False or "scan" in doc or "scan_status" in doc`; `True` otherwise (preserving synthetic metadata-only unit-test dicts that carry none of `generated`, `scan`, or `scan_status`).
    * `is_rescan_pending(doc)`: `isinstance(doc, Mapping) and not doc.get("generated") and (scan_status(doc) == "pending" or ("scan" not in doc and "scan_status" not in doc))`.
  * In `scan_new_document` and `_scan_stored`: if `self.scanner is None`, raise `RuntimeError("No content scanner is configured; the document remains unavailable.")`; let scanner/storage exceptions and `_scan_result` `RuntimeError`s propagate unchanged (`PC-001`). When the scanner returns `("failed", detail)`, persist `status="failed"` without deleting bytes so the upload remains quarantined and blocked everywhere.
  * In `_scan_stored`: call `if hasattr(self, "_touch"): self._touch(case_id)` before `self.save()` so `SqlStore` persists case document updates during `rescan_pending` / `ensure_scanned`, and synchronize `if "scan_status" in doc: doc["scan_status"] = verdict` (`PC-002`).
  * In `require_clean(doc)`: if `not is_clean_document(doc)`, raise `DocumentUnavailable("This document is not available until it has passed the content scan.")`.
  * In `ensure_scanned(case_id, doc, who)`: return early if `not is_rescan_pending(doc)`. Never auto-rescan `"infected"`, `"failed"`, `"mismatch"`, `"clean"`, or explicitly malformed/null `scan` / `scan_status` fields.
  * In `rescan_pending(who)`: iterate using `is_rescan_pending(d)`; increment `out["clean"]` for `"clean"`, `out["pending"]` for `"pending"`, and `out["blocked"] = out.get("blocked", 0) + 1` (not `out["pending"]`) when `"failed"` or non-removed non-clean is returned (`PC-002`).
  * In `rescan_document` (and `Store.replace_document`): use `not d.get("generated")` rather than `not d["generated"]` (`PC-002`).
* Excluded: Changing document JSON schema fields emitted by `Store.add_document`.

#### Likely Targets

* `src/core/src/zava_forward/core/doc_controls.py`: Verdict model, canonical predicates, and `DocControlsMixin`.
* `src/core/src/zava_forward/core/store.py`: `not d.get("generated")` in `replace_document`.

#### Dependencies

* None.

#### Validation Expectations

* `src/core/tests/test_document_rescan.py` and `src/api/tests/test_document_controls.py` pass for all 5 verdicts, `SqlStore` reopen persistence, `#395` malformed/outage contracts, and missing/malformed/conflicting `scan` and `scan_status`.

#### Completion Evidence

* Canonical functions implemented and exported in `doc_controls.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Align `document_rescan._pending` with canonical `is_rescan_pending`

#### Context

`document_rescan._pending` (`C4`, `PC-004`) inspects `(doc.get("scan") or {}).get("status", "pending") == "pending"`, which raises `AttributeError` if `doc["scan"]` is a non-dict scalar and misinterprets records carrying top-level `scan_status`.

#### Intent

Delegate pending-rescan detection in `document_rescan._pending` to `doc_controls.is_rescan_pending(doc)`.

#### Boundaries

* Included: `src/core/src/zava_forward/core/document_rescan.py` (`_pending`).
* Excluded: Changing rescan runner keyset paging, `_attempt` rollback semantics, or worker reporting keys.

#### Likely Targets

* `src/core/src/zava_forward/core/document_rescan.py`: `_pending`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* `src/core/tests/test_document_rescan.py` passes and non-pending (`failed`, `infected`, `mismatch`, `clean`, malformed `scan`) records do not trigger spurious rescans or `AttributeError`.

#### Completion Evidence

* `document_rescan.py` updated and `src/core/tests/test_document_rescan.py` green.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Derivative-Use Quarantine Enforcement Across `src/core`

### Context

Research (`C6`–`C18`) found that while `Store.get_document`, `Store.read_document`, `forms.stage_candidates`, and `form_review._source_document` call `require_clean`, multiple case-level and direct-helper derivative paths fail open or ignore `scan_status` when an upload is `pending`, `infected`, `failed`, `mismatch`, or missing scan status.

### Intent

Enforce canonical quarantine predicates across every derivative document consumer in `src/core`.

### Boundaries

* Included: `store.py`, `signoffs.py`, `forms.py`, `procurement.py`, `taskqueues.py`, `data_protection.py`, `ai_tasks.py`, `assistants.py`, `chat_case_answers.py`, `resident_documents.py`, `resident_summary.py`.
* Excluded: `src/api/src/zava_forward/api/server.py` route registrations.

### Likely Targets

* `src/core/src/zava_forward/core/store.py`: `Store.focus` and `Store.checklist`.
* `src/core/src/zava_forward/core/signoffs.py`: `_usable_document`.
* `src/core/src/zava_forward/core/forms.py`: `list_candidates`.
* `src/core/src/zava_forward/core/procurement.py`: `_capacity_source`.
* `src/core/src/zava_forward/core/taskqueues.py`: `context` EPC/Survey freshness lookup.
* `src/core/src/zava_forward/core/data_protection.py`: `document_model_hold`.
* `src/core/src/zava_forward/core/ai_tasks.py`: `source_labels` and `run_document`.
* `src/core/src/zava_forward/core/assistants.py`: `capture`.
* `src/core/src/zava_forward/core/chat_case_answers.py`: `case_facts`.
* `src/core/src/zava_forward/core/resident_documents.py`: `SCAN_TEXT` and `document_answer`.
* `src/core/src/zava_forward/core/resident_summary.py`: `_request_state` and `needed_from_you`.

### Dependencies

* P01.

### Validation Expectations

* Quarantined uploads (`pending`, `infected`, `failed`, `mismatch`, missing/malformed scan status) are blocked/excluded across all 11 derivative modules while all existing unit tests in `src/core/tests` and `src/api/tests` pass.

### Completion Evidence

* Updated `src/core` modules passing unit tests, `ruff`, and `mypy`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Gate case checklists, focus, `home_case`, sign-offs, forms, procurement, and task queues on clean uploads

#### Context

Quarantined uploads currently count toward `Store.checklist` (`funding_step("approve")`, `require_booking_gates`, `funding_draft`) and `Store.focus` (`C6`), appear as clean documents/frozen IDs in `home_case.links` and `home_case.view` (`PC-003`), clear EPC/Survey staleness in `taskqueues.context` (`C16`), and encounter raw `d.get("scan")` dict assumptions in `signoffs._missing_evidence` (`C15`, `PC-004`), `forms.list_candidates` (`C12`, `PC-003`), and `procurement._capacity_source` (`C14`, `PC-004`). In addition, `Store._evidence_missing` relies on `Store.checklist` raising `(KeyError, TypeError)` on malformed items like `[{}]` or `[None]` (`PC-005`).

#### Intent

Use `is_available_case_document` for case evidence, `home_case`, and freshness queries (preserving `KeyError`/`TypeError` on malformed `Store.checklist` items) and `is_clean_upload` for form candidate listing and procurement capacity source validation.

#### Boundaries

* Included:
  * `store.py`: in `Store.checklist`, compute `have = {k for d in c["documents"] for k in (d["kind"],) if is_available_case_document(d)}` so `[None]` and `[{}]` still raise `TypeError` and `KeyError` (`PC-005`); in `Store.focus`, filter `c["documents"]` with `is_available_case_document(d)`.
  * `home_case.py`: filter `case.get("documents", [])` with `is_available_case_document(d)` in both `links` and `view` (`PC-003`).
  * `signoffs.py`: in `_missing_evidence(c, usable_only=False)`, preserve the `usable_only: bool = False` signature (`PC-004`) and filter `c["documents"]` with `is_available_case_document(d)` when `usable_only` is `True` (while `Store.checklist` enforces `is_available_case_document` across all callers).
  * `forms.py`: in `list_candidates`, compute `clean_ids = {d["id"] for d in case["documents"] if is_clean_upload(d)}` (`PC-003`).
  * `procurement.py`: in `_capacity_source`, validate `is_clean_upload(doc)` instead of `(doc.get("scan") or {}).get("status") == "clean"` (`PC-004`).
  * `taskqueues.py`: in `context`, filter `case.get("documents", [])` with `is_available_case_document(d)` before computing `EPC` and `Survey` freshness.
* Excluded: Altering `c["documents"]` stored list.

#### Likely Targets

* `src/core/src/zava_forward/core/store.py`: `focus`, `checklist`, `replace_document`.
* `src/core/src/zava_forward/core/home_case.py`: `links`, `view`.
* `src/core/src/zava_forward/core/signoffs.py`: `_missing_evidence`.
* `src/core/src/zava_forward/core/forms.py`: `list_candidates` (with `form_review._document` already calling `store.require_clean`).
* `src/core/src/zava_forward/core/procurement.py`: `_capacity_source`.
* `src/core/src/zava_forward/core/taskqueues.py`: `context`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* `test_gates.py`, `test_home_case.py`, `test_technical_evidence_usability.py`, `test_form_staging.py`, `test_form_held_download_api.py`, `test_quality_procurement.py`, `test_procurement_api.py`, and `test_taskqueues.py` all pass, and quarantined uploads cannot satisfy any checklist, funding, booking, technical sign-off, `home_case` snapshot, form candidate listing, procurement commitment, or freshness check.

#### Completion Evidence

* All six modules updated to use canonical `doc_controls` predicates.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Gate AI document inspection, structured assistants, employee case chat facts, projection summaries, and resident document views

#### Context

Quarantined uploads must never enter model prompts, structured assistant contexts, employee chat case summaries, projected staff document summaries, or satisfy resident document requests (`C7`–`C11`, `C17`, `C18`, `PC-003`). Ordering invariants:
1. `ai_tasks.run_document` must run `export_fields.scalars(doc, ("name", "mime"))` before calling `store.require_clean(doc)` (`test_sensor_privacy.py`), and enforce `store.require_clean(doc)` whenever `doc.get("generated") is False or "scan" in doc or "scan_status" in doc` (`test_assistant_release.py`).
2. `data_protection.document_model_hold` must reject any non-generated document that carries `"scan"` or `"scan_status"` when `scan_status(doc_map) != "clean"` **before** `if is_actual:` (`PC-003`), so `ZF_DATA_MODE=actual` calls with `derivative="reviewed_redacted"` (including direct `Ai.look_at(..., doc=doc)` calls) cannot bypass the scan hold, while preserving synthetic `{"id": "D-UP-1", "generated": False}` without scan keys in `test_data_protection.py`.

#### Intent

Block uncleaned uploads across AI document tasks, model holds, structured assistants, employee chat facts, projected summaries, and resident document request/summary views.

#### Boundaries

* Included:
  * `ai_tasks.py`: filter `c.get("documents", [])` in `source_labels` using `is_available_case_document(d)`; in `run_document`, after `export_fields.scalars(doc, ("name", "mime"))`, call `store.require_clean(doc)` whenever `isinstance(doc, Mapping) and (doc.get("generated") is False or "scan" in doc or "scan_status" in doc)`.
  * `data_protection.py`: in `document_model_hold`, **before** `if is_actual:`, if `isinstance(doc, Mapping)` and `not doc.get("generated")` and (`"scan" in doc` or `"scan_status" in doc`) and `scan_status(doc) != "clean"`, return `"Document has not passed the content scan and cannot be sent to a model. " + MANUAL_PATH` (`PC-003`).
  * `assistants.py`: in `capture`, filter `c.get("documents", [])` with `is_available_case_document(d)`.
  * `chat_case_answers.py`: in `case_facts`, filter `_rows(detail.get("documents"))` with `is_available_case_document(d)`.
  * `projection.py`: in `redact_staff_detail`, withhold `doc["summary"] = NOTE_HELD` whenever `not is_available_case_document(doc)` so a quarantined upload's prior/injected summary text is not exposed as clean summary prose.
  * `resident_documents.py`: add `"failed": "Error: the recorded file check failed and could not clear this file. Ask staff for help."` to `SCAN_TEXT`; in `document_answer`, mark a request `"A presented document is recorded. Staff still need to check it."` only when `any(d.kind == request.kind and not d.generated and d.scan_status == "clean" for d in facts.documents)`.
  * `resident_summary.py`: in `_request_state`, return `"provided"` only when `any(d.kind == kind and not d.generated and d.scan_status == "clean" for d in facts.documents)`; in `needed_from_you`, check `if not document.get("generated") and document["scan_status"] != "clean":` so `"pending"`, `"infected"`, `"mismatch"`, `"failed"`, and `"unknown"` presented uploads are all surfaced (`PC-003`).
* Excluded: Changing resident upload prohibition or web frontend JS.

#### Likely Targets

* `src/core/src/zava_forward/core/ai_tasks.py`: `source_labels`, `run_document`.
* `src/core/src/zava_forward/core/data_protection.py`: `document_model_hold`.
* `src/core/src/zava_forward/core/assistants.py`: `capture`.
* `src/core/src/zava_forward/core/chat_case_answers.py`: `case_facts`.
* `src/core/src/zava_forward/core/projection.py`: `redact_staff_detail`.
* `src/core/src/zava_forward/core/resident_documents.py`: `SCAN_TEXT`, `document_answer`.
* `src/core/src/zava_forward/core/resident_summary.py`: `_request_state`, `needed_from_you`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* `test_data_protection.py`, `test_sensor_privacy.py`, `test_assistant_release.py`, `test_assistants.py`, `test_ai_provider_payload_spy.py`, `test_chat_panel.py`, `test_resident_documents.py`, and `test_resident_summary.py` all pass, and new assertions confirm fail-closed blocking on `pending`, `infected`, `failed`, `mismatch`, and missing scan status (including `ZF_DATA_MODE=actual` in `document_model_hold`).

#### Completion Evidence

* All seven modules updated and verified by unit tests.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Unit Tests and Tier Validation

### Context

Issue #117 and the caller specification require focused unit tests proving uploads remain quarantined and unavailable for download or derivative use until `scan_status == "clean"`, failing closed on `pending`, `infected`, `failed`, or missing scan status, validated via per-project `src/core` and `src/api` unit tests, `ruff`, and `mypy` without running `tools/rpi-checks.py` (`PC-006`).

### Intent

Lock semantic and regression test coverage in existing test suites and execute the complete per-project Focused validation tier.

### Boundaries

* Included:
  * Test ownership and target files:
    * `src/api/tests/test_document_controls.py` (canonical API + `Store` upload/download/derivative quarantine test suite; removals: `none`; max additions: 6 focused test methods; preserve formatting exclusions on legacy file per `PC-006`).
    * `src/core/tests/test_technical_evidence_usability.py` (canonical core evidence/checklist/home_case/assistant/chat/taskqueue/model-hold quarantine test suite; removals: `none`; max additions: 4 focused strictly-typed test methods).
    * `src/core/tests/test_document_rescan.py` (canonical `SqlStore` rescan persistence + `"failed"` verdict + `scan_status` sync test suite; removals: `none`; max additions: 2 focused strictly-typed test methods).
    * `src/core/tests/test_resident_documents.py` (canonical resident document scan-state, `needed_from_you`, & request-satisfaction test suite; removals: `none`; max additions: 2 focused strictly-typed test methods).
  * Generated test targets: `none`.
  * Semantic vs regression coverage:
    * Semantic coverage: download (`GET /api/cases/{cid}/documents/{did}` / `Store.get_document`), `SqlStore` `rescan_pending` reopen persistence & `scan_status` synchronization, and derivative uses (`POST /api/cases/{cid}/read-doc` including `reviewed_redacted` derivative and `necessity_exception`, `ai_tasks.run_document`, `document_model_hold` including `ZF_DATA_MODE=actual` with `reviewed_redacted`, `forms.stage_candidates` & `forms.list_candidates`, `form_export.draft_export`, `procurement._capacity_source`, `home_case.links` & `home_case.view`, `projection.redact_staff_detail`, `Store.checklist` including `[None]` `TypeError` preservation / `funding_step("approve")` / `require_booking_gates`, `assistants.capture` / `eligible`, `chat_case_answers.case_facts`, `taskqueues.context` freshness, and `resident_documents` / `resident_summary.needed_from_you`) all fail closed across `pending`, `infected`, `failed`, `mismatch`, missing (`None` / `{}` / absent scanner), and conflicting (`scan` vs `scan_status`) states, and succeed once `scan_status == "clean"` is recorded.
    * Regression coverage: existing `src/core` unittest suite, existing `src/api` unittest suite (including `test_role_endpoint_inventory.py`, `src/core/tests/test_document_rescan.py`, `test_data_protection.py`, `test_sensor_privacy.py`, `test_assistant_release.py`), and per-project `ruff check .`, `ruff format --check .`, and `mypy`.
* Excluded: Running `tools/rpi-checks.py`; browser E2E suites; modifying unrelated tests.

### Likely Targets

* `src/api/tests/test_document_controls.py`: Add focused tests for `"failed"` scan verdict quarantine, missing-scanner refusal, conflicting/malformed/missing `scan` & `scan_status`, download 409/403 refusal, `read-doc` derivative refusal, forms staging/listing/export quarantine, and checklist/funding/procurement quarantine until clean rescan.
* `src/core/tests/test_technical_evidence_usability.py`: Add strictly-typed focused tests proving `pending`, `infected`, `failed`, `mismatch`, and missing/conflicting scan status uploads are excluded from `Store.checklist` (while `[None]` raises `TypeError`), `home_case`, `projection`, `assistants.capture`, `ai_tasks.source_labels`, `chat_case_answers.case_facts`, `taskqueues.context`, and blocked in `data_protection.document_model_hold` (both synthetic and `actual` modes).
* `src/core/tests/test_document_rescan.py`: Add strictly-typed focused tests proving explicit `"failed"` verdicts quarantine without deletion and `SqlStore` `rescan_pending` persists across reopen while synchronizing `scan_status`.
* `src/core/tests/test_resident_documents.py`: Add strictly-typed focused tests proving `"failed"` scan text and proving `pending`, `infected`, `failed`, `mismatch`, and `None` uploads do not satisfy resident document requests and appear in `resident_summary.needed_from_you`.

### Dependencies

* P01, P02.

### Validation Expectations

* Inside `src/core`: `python3 -m unittest discover -s tests -q && ruff check . && ruff format --check . && mypy` exits 0.
* Inside `src/api`: `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q && ruff check . && ruff format --check . && mypy` exits 0.

### Completion Evidence

* Recorded command exit codes and test counts in `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add focused unit tests in `src/core/tests` and `src/api/tests` and run per-project Focused validation suite

#### Context

All new behavior introduced in P01 and P02 needs concise, parameterized `subTest` checks in existing test files with strict PEP 484 annotations in `src/core/tests` (`PC-006`) and surgical edits in `src/api/tests/test_document_controls.py`.

#### Intent

Add focused unit tests in the four existing test modules and verify 100% pass across per-project unit tests, `ruff`, and `mypy`.

#### Boundaries

* Included: `src/api/tests/test_document_controls.py`, `src/core/tests/test_technical_evidence_usability.py`, `src/core/tests/test_document_rescan.py`, `src/core/tests/test_resident_documents.py`, plus running per-project Focused validation commands.
* Excluded: `tools/rpi-checks.py`, new test files.

#### Likely Targets

* `src/api/tests/test_document_controls.py`: API and `Store` scan/download/derivative tests.
* `src/core/tests/test_technical_evidence_usability.py`: Core derivative availability, `home_case`, `checklist` `TypeError`, and model-hold tests.
* `src/core/tests/test_document_rescan.py`: `SqlStore` reopen persistence, `"failed"` verdict quarantine, and `scan_status` sync tests.
* `src/core/tests/test_resident_documents.py`: Resident scan status, `needed_from_you`, and request satisfaction tests.

#### Dependencies

* P01-T01, P01-T02, P02-T01, P02-T02.

#### Validation Expectations

* Per-project `unittest`, `ruff check .`, `ruff format --check .`, and `mypy` in `src/core` and `src/api` pass with exit code 0.

#### Completion Evidence

* Passing test output and static check output recorded in implementation changes artifact.

#### Unresolved Items

* None.
