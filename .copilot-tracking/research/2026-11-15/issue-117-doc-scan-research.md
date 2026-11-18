<!-- markdownlint-disable-file -->

# Task Research: issue-117-doc-scan

| Field              | Value                                                               |
|--------------------|---------------------------------------------------------------------|
| Date               | 2026-11-15                                                          |
| Researcher / agent | rpi-research (under confirmed automatic RPI Agent)                  |
| Status             | Complete                                                            |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-117-doc-scan-research.md |

## Research Brief

* What to research: Existing document store, blob upload, quarantine, malware scan status recording, download availability, and derivative-use surfaces across `src/core` and `src/api` (and any consumers such as `src/agents` or chat grounding) for Issue #117 (`Uploads are scanned before availability`).
* Why it matters: Unscanned, pending, infected, failed, or scan-missing document uploads must fail closed across download and derivative-use paths so unsafe content cannot be read by users or models before `scan_status == "clean"` is recorded.
* Audience or intended use: Downstream `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` phases within the confirmed automatic RPI session for Issue #117.
* Scope: `src/core`, `src/api`, related consumer paths (such as `src/agents` or grounding/evidence consumers), existing unit tests, and ADR 0002 / PRD DH-003 traceability.
* Non-goals: Live Azure Defender for Storage deployment, DPO/Legal approval of final retention schedules, new HTTP routes in `server.py` (unless preserving `test_role_endpoint_inventory.py`), running `tools/rpi-checks.py`, or pushing commits to remote.
* Criteria: Identify every code path where uploaded documents are stored, scanned, listed, read/downloaded, or consumed by downstream helpers/grounding/exports; determine whether any path fails open or lacks explicit `scan_status == "clean"` enforcement on `pending`, `infected`, `failed`, or missing `scan_status`; select a complete, minimal convergence recommendation with focused unit test coverage.
* Requested outputs: Complete dated research artifact with three-wave cycle log, `C#` codebase evidence table, convergence recommendation, alternatives, and Planning Readiness assessment.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                  |
|----------------------------------|--------------------------------------------------------------------------------------------------------|
| Research question(s)             | How are document uploads, scan verdicts, quarantine states, downloads, and derivative document uses implemented and gated across `src/core` and `src/api` (plus adjacent consumers), and where if anywhere can non-`clean` documents be accessed or used? |
| Codebase scope                   | `src/core`, `src/api`, `src/agents`, `docs/adrs/0002-pilot-readiness-architecture.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md` |
| External scope                   | none                                                                                                   |
| Initial internal candidate areas | `src/core/` document store / scanner modules, `src/api/` server and document handlers, `src/api/tests/test_role_endpoint_inventory.py`, chat/agent grounding paths |
| Initial external candidate areas | none                                                                                                   |
| Research posture                 | focused                                                                                                |
| Posture provenance               | caller-specified (bounded internal task with named targets `src/core`, `src/api`, and focused validation tier) |
| Explicit limits / deadline       | Single-run automatic RPI loop; focused validation tier (`src/core` and `src/api` unit tests, `ruff`, `mypy`); no `tools/rpi-checks.py`; no git push |
| Posture-specific completion basis | focused scope and materiality: all upload, scan, download, and derivative-use surfaces in scope inspected and backed by `path:line` evidence |
| Edits allowed during research?   | no, research-only                                                                                      |
| Resolved evidence root           | `.copilot-tracking/`                                                                                   |
| Known constraints / excluded sources | Do not add new HTTP routes in `server.py` unless `test_role_endpoint_inventory.py` is preserved; do not place `.copilot-tracking/` paths in production code, comments, docstrings, or commit messages |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                                   | Scoped authority or output contract                        | Selected / skipped reason                                                       |
|---------------------|---------------------------------------|--------------------------------------------------------|------------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`     | `applyTo: "**"` matches repository inputs and outputs  | Adds repository structure, testing, regulatory, and style rules | Selected: mandatory repository instructions                                     |
| Skill               | `rpi-research`                        | Explicit caller phase request                          | Read-only three-wave research artifact contract            | Selected: active RPI phase skill                                                |
| Skill               | `python-foundational` / `owasp-top-10`| Domain match to Python security gate                   | Reference conventions only                                 | Skipped: bounded internal Python inspection needs direct codebase evidence first |
| Research specialist | `hve-core-all:rpi-researcher`         | Registered subagent for independent research lanes     | Lane artifact under `.copilot-tracking/research/subagents/` | Skipped (inline): tightly coupled codebase trace across `src/core` and `src/api` fits fast inline inspection |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                 | Answers / unanswered | Resulting decision or selected further research                                  |
|------------------|-------------------------------------------------------------------------------------------------------|----------------------|----------------------------------------------------------------------------------|
| Intake           | Caller supplied explicit target, branch, validation tier, fail-closed scan gate rules, and non-interactive continuous RPI instruction | Not needed           | Proceed in `focused` posture and `convergence` output mode without pausing       |
| Direction change | None required during single complete three-wave cycle                                                 | None                 | Keep bounded scope across `src/core` and `src/api` with zero new HTTP routes     |
| Convergence      | Evidence converges on unified `doc_controls` fail-closed helpers across download and derivative paths | Not needed           | Select unified fail-closed scan status gate and advance to `rpi-plan`            |

## Scope and Success Criteria

* Scope: Document store implementations, malware scanners / tag readers, document metadata models, upload/download HTTP handlers, case/evidence/chat/export/agent derivative readers in `src/core`, `src/api`, and `src/agents`, plus unit tests in `src/core/tests` and `src/api/tests`.
* Assumptions:
  * ADR 0002 notes that some scan-before-availability scaffolding may already exist in `src/core` or `src/api`; must verify exact runtime behavior for `pending`, `infected`, `failed`, and missing `scan_status` across all read AND derivative-use surfaces.
  * Stacked parent branch `feat/demo-164-chat-grounding-provenance-0900` may have added chat grounding or provenance readers that read case documents—must verify whether chat grounding or any other derivative consumer inspects `scan_status`!
* Success criteria:
  * Every research question is answered with `path:line` evidence.
  * Findings, decisions, and readiness claims cite Evidence Log IDs (`C#`).
  * Alternatives are compared with trade-offs and one convergence recommendation is selected.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  * Inspect existing document store / blob upload / quarantine / malware scan gate in `src/core` and `src/api` for Issue #117 (`Uploads are scanned before availability`).
  * Determine what is needed so document uploads remain quarantined / unavailable for download or derivative use until `scan_status == "clean"` is recorded, failing closed on `pending`, `infected`, `failed`, or missing scan status, with focused unit tests proving the gate.
  * Preserve `test_role_endpoint_inventory.py` (do not add new HTTP routes unless preserved).
* Inferred research questions:
  * Q1: Where are `DocumentStore`, upload intake, scan status transitions, and quarantine controls implemented in `src/core`?
  * Q2: How does `src/api` expose document upload, metadata listing, download/content retrieval, and scan updates, and how does each behave when `scan_status` is `pending`, `infected`, `failed`, `None`/missing, or unknown?
  * Q3: What derivative-use paths exist in `src/core`, `src/api`, or `src/agents` (such as chat grounding/provenance from stacked PR #1641, evidence packs, PAS 2035 assessments, grant bids, quality acceptance, exports, or retention) that read document bytes or treat uploaded documents as available/valid evidence before `scan_status == "clean"`?
  * Q4: What unit tests and endpoint inventory checks currently cover document scanning, quarantine, and derivative document access in `src/core/tests` and `src/api/tests`?
* Caller constraints and non-goals: Focused validation tier only; no `tools/rpi-checks.py`; no git push; continuous RPI execution without pausing.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Focus on `Uploads are scanned before availability` fail-closed gate across download and derivative use  | Caller intake       | Scopes research to `scan_status == "clean"` enforcement and tests                  |
| exclude                                                  | Do not add HTTP routes in `server.py` unless `test_role_endpoint_inventory.py` is preserved             | Caller intake       | Constrains convergence design away from unnecessary route additions                |
| exclude                                                  | Do not run `tools/rpi-checks.py` or push to remote                                                      | Caller intake       | Scopes validation planning to focused unit tests, `mypy`, and `ruff`               |

## Research Questions

|  # | Sub-question                                                                                                                                   | Type            | Priority | Status   |
|---:|------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | How do `src/core` document stores and scanners store uploads, assign initial `scan_status`, Quarantine blobs/files, and record scan verdicts?  | depth           | H        | answered |
| Q2 | How do `src/api` download and document-read endpoints gate access on `scan_status` (`clean`, `pending`, `infected`, `failed`, missing/other)?  | depth           | H        | answered |
| Q3 | Which derivative-use paths (chat grounding, agent helpers, evidence verification, exports, case views) consume documents, and do they fail closed when `scan_status != "clean"`? | breadth | H | answered |
| Q4 | What existing tests and contracts (`test_role_endpoint_inventory.py`, `src/core/tests`, `src/api/tests`) govern changes and prove the gate?    | straightforward | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, GitHub Issue #117.
* Reused (verified) findings: Issue #117 has two checkboxes: `- [ ] Uploads are scanned before availability` (open) and `- [x] Retention job lists records past trigger and needs owner approval; legal hold blocks deletion` (already checked). ADR 0002 notes partial delivery of `DocumentStore` with synthetic local scanner and Defender tag reader, which must now be verified directly in source code rather than assumed complete.
* Superseded / stale: Issue #117 label mentions `mvp/`, which was retired at cut-over in favor of `src/`.

## Cycle 1 Execution Log

### Wave 1: Wider

* Executed inline across `src/core/src/zava_forward/core/`, `src/api/src/zava_forward/api/`, and `src/agents/` (tightly coupled codebase trace; `hve-core-all:rpi-researcher` skipped inline as recorded in Extension Registry).
* Mapped every document storage, scan, HTTP endpoint, and downstream consumer surface:
  * Storage & scanning: `documents.py` (`LocalFileDocumentStore`, `AzureBlobDocumentStore`), `doc_controls.py` (`LocalSignatureScanner`, `DefenderForStorageScanner`, `DocControlsMixin`), `document_rescan.py` (`DocumentRescanRunner`).
  * Core intake, download & AI document read: `store.py` (`add_document`, `get_document`, `read_document`, `checklist`, `focus`), `server.py` (`/api/cases/{cid}/documents`, `/api/cases/{cid}/documents/{did}`, `/api/cases/{cid}/read-doc`, `/api/admin/documents/rescan`).
  * Downstream / derivative consumers: `data_protection.py` (`document_model_hold`), `ai.py` (`look_at`), `ai_tasks.py` (`source_labels`, `run_document`), `assistants.py` (`capture`, `eligible`), `chat_case_answers.py` (`case_facts`), `chat_isolation.py` / `export_fields.py` (`chat_case`), `forms.py` (`_document`, `stage_candidates`, `list_candidates`), `form_review.py` (`_source_document`), `form_export.py` (`draft_export`, `export_freshness`), `procurement.py` (`_capacity_source`), `signoffs.py` (`_usable_document`, `technical_gate`), `taskqueues.py` (`context` freshness), `resident_documents.py` (`SCAN_TEXT`, `document_answer`), and `resident_summary.py` (`_request_state`, `documents_view`, `needed_from_you`).

### Wave 2: Deeper

* Inspected exact implementation lines for every surface discovered in Wave 1 (`C1`–`C20`):
  * Verdict model & scanner gap (`C1`, `C2`, `C3`): `doc_controls._scan_result` only accepts `("clean", "pending", "infected", "mismatch")` and raises `RuntimeError` on `"failed"`. `DefenderForStorageScanner.scan` treats `None`/empty tag as `"pending"` (`"scan result not yet written"`), `"No threats found"` as `"clean"`, `"Malicious"` as `"infected"`, and **any other tag** (e.g. `"Scan failed"`, `"Error"`, corrupted/unexpected tag) as `"pending"` instead of `"failed"`. In addition, if `self.scanner` is `None` or raises during `scan_new_document` or `_scan_stored`, there is no fail-closed `"failed"` verdict path.
  * Dual `scan` / `scan_status` representation & malformed-record gaps (`C3`, `C4`, `C5`, `C12`, `C15`, `C16`): Core stores `doc["scan"] = {"status": ..., ...}`, whereas callers/projections/fixtures may set or carry `doc["scan_status"]` (or malformed `scan=None`, `scan={}`, `scan="clean"`, or conflicting `scan={"status": "clean"}` alongside `scan_status="infected"`). `DocControlsMixin.require_clean`, `ensure_scanned`, `rescan_pending`, `document_rescan.has_pending`, `forms.list_candidates`, and `procurement._capacity_source` read `doc.get("scan")` inconsistently (`d.get("scan", {}).get("status")` even raises `AttributeError` when `d["scan"] is None`!) and ignore `doc["scan_status"]`, meaning `ensure_scanned` would treat `{"generated": False, "scan_status": "infected"}` or `"failed"` as `"pending"` and overwrite it via `LocalSignatureScanner`!
  * Derivative-use fail-open gaps (`C6`–`C18`):
    1. `Store.checklist(c)` (`store.py:1132`) and `Store.focus(c, ...)` (`store.py:640`) check `{d["kind"] for d in c["documents"]}` without filtering out quarantined uploads (`pending`, `infected`, `failed`, `mismatch`, or missing scan status on `generated=False`), allowing quarantined uploads to satisfy checklist completion, `funding_step(..., "approve")`, `require_booking_gates`, and `funding_draft` missing-document checks!
    2. `ai_tasks.source_labels(c, ...)` (`ai_tasks.py:86`) includes `Document: {d['name']}` for quarantined uploads in AI prompt source labels for `summary`, `message`, `briefing`, and `funding_draft`.
    3. `ai_tasks.run_document` (`ai_tasks.py:451`) and `data_protection.document_model_hold` (`data_protection.py:478`) rely solely on `Store.read_document` having checked `require_clean` upstream; calling `run_document` or `document_model_hold` / `Ai.look_at` directly on a document record with non-clean `scan` or `scan_status` (even with `derivative="reviewed_redacted"` or `necessity_exception`) does not enforce `scan_status == "clean"`.
    4. `assistants.capture(...)` (`assistants.py:265`) passes all `c.get("documents", [])` into `source["documents"]`, letting quarantined uploads satisfy `eligible(...)` (`{"Survey", "Design"}` / `"Funding evidence"`) and enter structured assistant model prompts!
    5. `chat_case_answers.case_facts(detail, ...)` (`chat_case_answers.py:187`) lists quarantined upload `kind`s in employee chat `documents` facts.
    6. `taskqueues.context(...)` (`taskqueues.py:333`) uses quarantined `"EPC"` / `"Survey"` uploads to compute `"Within review window"` freshness!
    7. `resident_documents.py` (`SCAN_TEXT` at line 106, `document_answer` at line 124) and `resident_summary.py` (`_request_state` at line 85, `needed_from_you` at line 157) lack a plain-language `"failed"` scan message, mark document requests `"provided"` even when `d.scan_status` is `"pending"`, `"infected"`, `"failed"`, `"mismatch"`, or `None` (violating PRD AC-115 *"rejected attempts do not satisfy the request"*), and omit `"failed"` / `"unknown"` uploads from `needed_from_you`!

### Wave 3: Contrarian

* Tested the candidate fail-closed rule against all 50 unit test modules in `src/core/tests` and `src/api/tests` (`C19`–`C24`) to ensure tightening upload quarantine does not break legitimate legacy synthetic fixtures or existing contract tests:
  * Counter-evidence 1 (`C20`): Legacy unit tests for unrelated capabilities (`test_gates.py:119` `{"kind": "EPC"}`, `test_assistants.py:102` `dict(id="SURVEY-1", kind="Survey", ...)`, `test_ai_provider_payload_spy.py:228` `FIRST_DOC`, `building_fixture.py`) construct metadata-only case document dicts **without** `Store.add_document`, omitting `"generated"`, `"scan"`, and `"scan_status"`. Meanwhile, **every** uploaded document created via `Store.add_document` (`store.py:1211`) or upload test fixtures (`test_technical_evidence_usability.py:24`, `test_document_controls.py`, `test_document_rescan.py`) sets `"generated": False` (matching the existing `data_protection.py:517` convention `doc.get("generated") is False`) and/or carries `"scan"` / `"scan_status"`.
    * Resolution: Distinguish strict byte/content/staging gates (`require_clean(doc)`: requires `doc.get("generated") is True` or `scan_status(doc) == "clean"`, failing closed on any missing/non-clean status) from case-collection projection helper `is_available_case_document(doc)` (returns `True` for `generated is True`; requires `scan_status(doc) == "clean"` whenever `doc.get("generated") is False` or `"scan" in doc` or `"scan_status" in doc` — failing closed on `pending`, `infected`, `failed`, `mismatch`, and missing/`None` scan status for every upload — while preserving synthetic metadata-only dicts that have none of `generated`, `scan`, or `scan_status`).
  * Counter-evidence 2 (`C21`): `test_document_controls.py:86` (`test_document_without_scan_field_is_scanned_on_first_use`) explicitly pops `"scan"` from a stored upload (`{"generated": False}` with neither `"scan"` nor `"scan_status"`) and expects `get_document` -> `ensure_scanned` to run `_scan_stored` once before `require_clean`; if the scanner is `DefenderForStorageScanner` with no clean tag (`test_document_controls.py:67`), `_scan_stored` records `"pending"` and `require_clean` raises `DocumentUnavailable` (HTTP 403). However, if `"scan"` or `"scan_status"` IS present with `None`, `{}`, `""`, `"failed"`, `"infected"`, `"mismatch"`, or conflicting values, `ensure_scanned` must **not** auto-rescan/overwrite it with a clean verdict — it must fail closed immediately in `require_clean`!
  * Counter-evidence 3 (`C22`, `C23`): `test_sensor_privacy.py:216` passes a malicious `doc["name"] = PACKET` (`generated=False`, no `scan`) into `ai_tasks.run_document` with `patch.object(store, "require_clean")` and expects `export_fields.scalars(doc, ("name", "mime"))` to raise `ValueError` first; `test_data_protection.py:332` calls `dp.document_model_hold({"id": "D-UP-1", "generated": False}, ..., derivative="reviewed_redacted")` directly without `"scan"`/`"scan_status"` to unit-test consent/redaction flags. Running `store.require_clean(doc)` right after `export_fields.scalars(...)` in `ai_tasks.run_document` AND checking scan status in `data_protection.document_model_hold` whenever `"scan" in doc_map or "scan_status" in doc_map` satisfies both contracts while closing direct bypasses!
  * Counter-evidence 4 (`C24`): `test_role_endpoint_inventory.py` enforces exact route parity with `server.py`. Zero new HTTP routes are needed because all upload, download, read-doc, forms, chat, assistant, and rescan gates operate inside `src/core` under existing endpoints.

## Evidence Log

| ID  | Source (`path:line`)                                                     | Summary                                                                                                                      |
|-----|--------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| C1  | `src/core/src/zava_forward/core/documents.py:36-215`                     | `LocalFileDocumentStore` and `AzureBlobDocumentStore` store/read raw bytes and blob index tags (`Malware Scanning scan result`). |
| C2  | `src/core/src/zava_forward/core/doc_controls.py:36-94`                   | `_scan_result` omits `"failed"`; `DefenderForStorageScanner.scan` maps unexpected/error tags to `"pending"` instead of `"failed"`. |
| C3  | `src/core/src/zava_forward/core/doc_controls.py:137-205`                 | `DocControlsMixin.scan_new_document`, `require_clean`, `_scan_stored`, `ensure_scanned`, `rescan_pending`, `rescan_document` ignore `scan_status`, mishandle non-dict `scan`, and lack scanner-error `"failed"` fallback. |
| C4  | `src/core/src/zava_forward/core/document_rescan.py:42-53`                | `DocumentRescanRunner.has_pending` assumes `doc.get("scan")` is a dict or `None` and ignores `scan_status`.                  |
| C5  | `src/core/src/zava_forward/core/store.py:1175-1335`                      | `Store.add_document` sets `"generated": False` and runs `scan_new_document`; `read_document` and `get_document` call `ensure_scanned` + `require_clean`. |
| C6  | `src/core/src/zava_forward/core/store.py:640,1132`                       | `Store.focus` and `Store.checklist` count all `c["documents"]` regardless of scan status, letting quarantined uploads satisfy gates. |
| C7  | `src/core/src/zava_forward/core/data_protection.py:478-538`              | `document_model_hold` treats `doc.get("generated") is False` as uploaded, but allows `reviewed_redacted` / `necessity_exception` without checking `scan` / `scan_status`. |
| C8  | `src/core/src/zava_forward/core/ai.py:315-336`                           | `Ai.look_at` gates model vision/text inspection on `document_model_hold(doc, ...)`.                                          |
| C9  | `src/core/src/zava_forward/core/ai_tasks.py:86,451-470`                  | `source_labels` exposes quarantined upload names to AI prompts; `run_document` lacks its own `store.require_clean(doc)` guard when called directly. |
| C10 | `src/core/src/zava_forward/core/assistants.py:265-305`                   | `assistants.capture` includes quarantined uploads in `source["documents"]` and eligibility checks (`Survey`, `Design`, `Funding evidence`). |
| C11 | `src/core/src/zava_forward/core/chat_case_answers.py:187`                | `case_facts` includes quarantined uploads in employee chat `documents` summary.                                              |
| C12 | `src/core/src/zava_forward/core/forms.py:139-151,182-193`                | `forms._document` calls `ensure_scanned` + `require_clean`; `forms.list_candidates` uses `d.get("scan", {}).get("status") == "clean"` (crashes if `scan=None`, ignores `scan_status`). |
| C13 | `src/core/src/zava_forward/core/form_review.py:66-79`                    | `form_review._source_document` calls `store.require_clean(doc)` so `form_export` blocks non-clean sources via `DocumentUnavailable`. |
| C14 | `src/core/src/zava_forward/core/procurement.py:85-95`                    | `procurement._capacity_source` checks `(doc.get("scan") or {}).get("status") == "clean"` without checking conflicting `scan_status`. |
| C15 | `src/core/src/zava_forward/core/signoffs.py:21-41`                       | `signoffs._usable_document` filters `usable_only=True`, while `_missing_evidence` delegates to `Store.checklist`.            |
| C16 | `src/core/src/zava_forward/core/taskqueues.py:332-347`                   | `taskqueues.context` computes `EPC` and `Survey` freshness from `case.get("documents", [])` without excluding quarantined uploads. |
| C17 | `src/core/src/zava_forward/core/resident_documents.py:106-135`           | `SCAN_TEXT` lacks `"failed"`; `document_answer` marks requests `"A presented document is recorded"` even when `scan_status != "clean"`. |
| C18 | `src/core/src/zava_forward/core/resident_summary.py:82-90,156-165`       | `_request_state` marks requests `"provided"` for non-clean uploads, and `needed_from_you` omits `"failed"` / `"unknown"` scan states. |
| C19 | `src/api/src/zava_forward/api/server.py:591-606,812-835`                 | `GET /api/cases/{cid}/documents/{did}` and `POST /api/cases/{cid}/read-doc` translate `DocumentUnavailable` to HTTP 403.     |
| C20 | `src/core/tests/test_technical_evidence_usability.py:18-55`              | Confirms uploaded test documents set `generated=False`, whereas metadata-only fixtures (`test_gates.py:119`, `test_assistants.py:102`) omit `generated`/`scan`. |
| C21 | `src/api/tests/test_document_controls.py:42-98`                          | Tests EICAR (`infected`), MIME mismatch (`mismatch`), Defender pending (`pending`), and legacy missing-`scan` rescan on first use. |
| C22 | `src/api/tests/test_sensor_privacy.py:212-235`                           | Patches `store.require_clean` and asserts `export_fields.scalars` rejects malformed `doc["name"]` first in `ai_tasks.run_document`. |
| C23 | `src/core/tests/test_data_protection.py:328-360`                         | Unit-tests `document_model_hold` consent/redaction rules using `{"id": "D-UP-1", "generated": False}` with no `scan` key.     |
| C24 | `src/api/tests/test_role_endpoint_inventory.py:1-120`                    | Asserts exact route inventory parity against `server.py`; adding no routes preserves inventory 100%.                         |

## Synthesized Findings

1. **Q1 (Scan Verdicts & Storage Intake)**: `Store.add_document` writes uploaded bytes to `DocumentStore` with `"generated": False` and immediately invokes `DocControlsMixin.scan_new_document` (`C1`, `C3`, `C5`). However, `doc_controls` lacks a first-class `"failed"` verdict: `DefenderForStorageScanner.scan` misclassifies non-clean/non-malicious Defender error tags as `"pending"`, `_scan_result` rejects `"failed"` with `RuntimeError`, and scanner exceptions/absence lack a fail-closed `"failed"` quarantine record (`C2`, `C3`).
2. **Q2 (Download & Direct Read Gate)**: `GET /api/cases/{cid}/documents/{did}` (`Store.get_document`) and `POST /api/cases/{cid}/read-doc` (`Store.read_document`) gate access through `ensure_scanned` + `require_clean`, returning HTTP 403 via `DocumentUnavailable` (`C3`, `C5`, `C19`). However, `require_clean` and `ensure_scanned` only inspect nested `doc["scan"]["status"]`, crash on non-dict `doc["scan"]`, ignore top-level `doc["scan_status"]` (or `scan` vs `scan_status` conflicts), and risk re-scanning an already `"failed"`/`"infected"` top-level `scan_status` record as if it were `"pending"` (`C3`, `C4`).
3. **Q3 (Derivative-Use Gates)**: While `forms.stage_candidates`, `form_review`, and `form_export` already call `require_clean` (`C12`, `C13`), multiple derivative-use paths fail open or inconsistently inspect scan state when `scan_status` is `pending`, `infected`, `failed`, `mismatch`, or missing: `Store.checklist` / `Store.focus` (`C6`), `ai_tasks.source_labels` / direct `ai_tasks.run_document` (`C9`), `data_protection.document_model_hold` (`C7`, `C8`), `assistants.capture` (`C10`), `chat_case_answers.case_facts` (`C11`), `forms.list_candidates` (`C12`), `procurement._capacity_source` (`C14`), `signoffs._usable_document` (`C15`), `taskqueues.context` (`C16`), and `resident_documents` / `resident_summary` (`C17`, `C18`).
4. **Q4 (Test & Route Contracts)**: Existing tests in `test_document_controls.py` and `test_technical_evidence_usability.py` cover `infected`, `mismatch`, and `pending` on basic download, but do not test `failed`, malformed/conflicting `scan` vs `scan_status`, missing scan status when scanner cannot clear, or derivative quarantine across checklist/funding/booking gates, AI `read_document` (`reviewed_redacted` / `necessity_exception`), structured assistants, employee case chat, forms, procurement, task queues, and resident views (`C20`–`C24`). Zero HTTP routes need to be added (`C24`).

## Alternatives Considered

| Option | Summary | Pros | Cons | Disposition |
|--------|---------|------|------|-------------|
| Option A: Canonical `doc_controls` fail-closed helpers wired across all read & derivative surfaces | Add `"failed"` verdict + canonical `scan_status(doc)`, `is_clean_document(doc)`, `is_clean_upload(doc)`, and `is_available_case_document(doc)` in `doc_controls.py`; enforce across `DocControlsMixin`, `document_rescan`, `Store`, `forms`, `procurement`, `signoffs`, `ai_tasks`, `data_protection`, `assistants`, `chat_case_answers`, `taskqueues`, `resident_documents`, and `resident_summary`. | Single source of truth; fails closed on `pending`, `infected`, `failed`, `mismatch`, missing, malformed, or conflicting `scan`/`scan_status`; preserves legacy metadata-only unit test fixtures and `test_role_endpoint_inventory.py`. | Touches ~12 focused modules in `src/core`. | **Selected** |
| Option B: Gate only `Store.get_document` and `Store.read_document` | Add `"failed"` verdict in `doc_controls.py` without updating case checklist, assistants, chat facts, forms, taskqueues, or resident views. | Smaller diff (2 files). | Leaves quarantined uploads able to satisfy funding/booking checklists, enter assistant/chat grounding, clear taskqueue staleness, and mark resident document requests provided. | Rejected (`C6`–`C18`) |
| Option C: Drop uncleaned uploads from `Store.detail` / `c["documents"]` entirely | Filter non-clean uploads out of `c["documents"]` on read. | Hides quarantined uploads from downstream readers automatically. | Breaks quarantine visibility, admin rescan (`rescan_document`), auditability, and resident plain-language scan warnings (`SCAN_TEXT`) that intentionally show pending/failed/infected status without granting content or evidence availability. | Rejected (`C3`, `C17`, `C21`) |

## Selected Recommendation

Adopt **Option A**:
1. Extend `doc_controls.py` with `"failed"` in supported scan verdicts, update `DefenderForStorageScanner.scan` so unrecognized/error Defender tags return `("failed", ...)` while only `None`/`""` returns `("pending", ...)`, and wrap scanner execution in `scan_new_document` / `_scan_stored` so missing or raising scanners record `("failed", ...)` and keep the upload quarantined (`C2`, `C3`).
2. Introduce canonical helpers in `doc_controls.py` (`C3`, `C20`–`C23`):
   * `scan_status(doc)`: reads nested `doc["scan"]["status"]` and top-level `doc["scan_status"]`; returns `"clean"` **only** when at least one valid status is `"clean"` and neither key is malformed or non-`"clean"` (if both keys exist and disagree, or `scan` is malformed/empty, fails closed to the non-clean status or `None`).
   * `is_clean_document(doc)`: `True` iff `doc` is a `Mapping` and (`doc.get("generated") is True` or `scan_status(doc) == "clean"`). Used by `DocControlsMixin.require_clean`.
   * `is_clean_upload(doc)`: `True` iff `doc` is a `Mapping`, `not doc.get("generated")`, and `scan_status(doc) == "clean"`. Used by `forms.list_candidates` and `procurement._capacity_source`.
   * `is_available_case_document(doc)`: `True` for `doc.get("generated") is True`; requires `scan_status(doc) == "clean"` whenever `doc.get("generated") is False` or `"scan" in doc` or `"scan_status" in doc` (failing closed on `pending`, `infected`, `failed`, `mismatch`, or missing/`None` scan status); `True` only for legacy synthetic metadata-only dicts lacking all three keys.
3. Update `ensure_scanned`, `rescan_pending`, and `document_rescan.has_pending` so auto-scan on first use runs only when `"scan" not in doc and "scan_status" not in doc`, and pending rescan runs only when `scan_status(doc) == "pending"` — never overwriting `"infected"`, `"failed"`, `"mismatch"`, or malformed scan fields (`C3`, `C4`, `C21`).
4. Enforce `is_available_case_document` / `is_clean_upload` / `require_clean` / `scan_status` across all derivative consumers: `Store.checklist` & `Store.focus` (`C6`), `data_protection.document_model_hold` (`C7`), `ai_tasks.source_labels` & `ai_tasks.run_document` (`C9`), `assistants.capture` (`C10`), `chat_case_answers.case_facts` (`C11`), `forms.list_candidates` (`C12`), `procurement._capacity_source` (`C14`), `signoffs._usable_document` (`C15`), `taskqueues.context` (`C16`), and `resident_documents` / `resident_summary` (`C17`, `C18`).
5. Add focused unit tests in `src/core/tests/test_technical_evidence_usability.py`, `src/core/tests/test_resident_documents.py`, and `src/api/tests/test_document_controls.py` proving fail-closed behavior for `pending`, `infected`, `failed`, `mismatch`, and missing/conflicting `scan_status` across download and all derivative uses, without adding any HTTP routes (`C21`, `C24`).

## Decisions, Risks, and Further Research

* Current confirmed decisions:
  * D1: Canonicalize scan status resolution in `doc_controls.py` (`scan_status`, `is_clean_document`, `is_clean_upload`, `is_available_case_document`) and add first-class `"failed"` verdict (`C2`, `C3`).
  * D2: Fail closed across both byte-reading paths (`get_document`, `read_document`, `ai_tasks.run_document`, `document_model_hold`, `forms.stage_candidates`) and case-level derivative paths (`checklist`, `focus`, `source_labels`, `assistants.capture`, `chat_case_answers`, `forms.list_candidates`, `procurement`, `signoffs`, `taskqueues`, `resident_documents`, `resident_summary`) (`C5`–`C18`).
  * D3: Add zero HTTP routes in `server.py`, preserving `test_role_endpoint_inventory.py` (`C24`).
* Unresolved decisions / blockers: None.
* Residual risks:
  * Live Azure Defender for Storage deployment infrastructure and DPO/Legal sign-off on retention schedules remain separate work outside this slice, as noted in ADR 0002 and Issue #117 scope.
* Potential further research: None needed for this slice; re-entry is not warranted because all internal code paths and contrarian test fixtures have been verified (`C1`–`C24`).

## Readiness and Handoff

* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`
* **Research-only check**: Confirmed — zero source or test files were modified during `rpi-research`.
* **Self-Check**:
  * [x] Brief, posture (`focused`), and extension provenance recorded.
  * [x] Cycle 1 completed Wider, Deeper, and Contrarian waves in order.
  * [x] Q1–Q4 answered with stable `C1`–`C24` `path:line` evidence IDs.
  * [x] Alternatives compared and Option A selected with evidence-based rejection rationale.
  * [x] Continuation owned by confirmed automatic RPI Agent (`Research` -> `Plan`).

