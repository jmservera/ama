<!-- markdownlint-disable-file -->
# Review: Issue 117 Document Malware Scan Quarantine Gate

## Scope and Evidence

* Task ID: issue-117-doc-scan
* Review date: 2026-11-15
* Review scope: full task (`P01`, `P02`, `P03`)
* Assessed boundary: Fail-closed malware scan verdict normalization (`clean`, `pending`, `infected`, `mismatch`, `failed`, missing/malformed/conflicting `scan` vs `scan_status`), `SqlStore` rescan touch/persistence, download and derivative-use quarantine across `src/core` without adding HTTP routes in `server.py`, and Focused-tier unit test + static check validation across `src/core` and `src/api`.
* Plan: .copilot-tracking/plans/2026-11-15/issue-117-doc-scan-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-117-doc-scan-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/issue-117-doc-scan-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/issue-117-doc-scan-research.md; independent code-review lens over `git diff` across 19 modified `src/core` and `src/api` files.

## Opening Review State

* Interpreted review goal: Verify that the completed implementation of Issue #117 (`Uploads are scanned before availability`) satisfies all functional and non-functional requirements, acceptance criteria, critique dispositions (`PC-001` through `PC-006`), route-inventory constraints, and Focused-tier validation gates without regressions or residual defects.
* Review scope: full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; plan, phase details, plan critique, research, and reconciled changes record are complete and aligned.
* Acceptance basis: User Decisions and Requirements, Functional and Non-Functional Requirements, Acceptance Criteria, and `PC-001`–`PC-006` Critique Dispositions in `.copilot-tracking/plans/2026-11-15/issue-117-doc-scan-plan.md`.
* First comparison boundary: Reconcile `P01`, `P02`, and `P03` markers and code diff against planned quarantine gates and Focused-tier test/lint/type evidence, excluding live Azure Storage Defender Bicep provisioning (tracked as distinct follow-up).
* Active read-only boundaries: Read-only comparison over source, tests, and prior RPI artifacts; write authority restricted exclusively to `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-review.md`.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass post-implementation review on 2026-11-15 across `.copilot-tracking/plans/2026-11-15/issue-117-doc-scan-plan.md`, `.copilot-tracking/details/2026-11-15/issue-117-doc-scan-phase-details.md`, `.copilot-tracking/reviews/2026-11-15/issue-117-doc-scan-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/issue-117-doc-scan-changes.md`, and the 19-file working-tree diff (`src/core` and `src/api/tests/test_document_controls.py`), corroborated by an independent `code-review` subagent verification.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `P01: Canonical Malware Scan Verdict and Quarantine Gate` | Reconciled | `VERDICTS`, canonical helpers, scanner `None` guard, `#395` exception preservation, `SqlStore` `_touch` + `scan_status` sync, and `document_rescan._pending` match plan and details. |
| `P02` (`P02-T01`, `P02-T02`) | `P02: Derivative-Use Quarantine Enforcement Across src/core` | Reconciled | All 13 consumer modules enforce fail-closed quarantine (`is_clean_document`, `is_clean_upload`, `is_available_case_document`, and pre-`actual_mode` `document_model_hold`). |
| `P03` (`P03-T01`) | `P03: Focused Unit Tests and Tier Validation` | Reconciled | Focused unit tests added across 4 test modules; `ruff`, `mypy`, 537 `src/core` tests, and 452 `src/api` tests passed with zero `server.py` route edits. |
| `## Follow-Up Items` | `Follow-Up Items` (Azure Storage Defender Bicep wiring) | Reconciled | Retained outside active `P01`–`P03` completion scope in both plan and changes record. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/doc_controls.py` | Added `"failed"` verdict, strict `_scan_result` check, `scan_status` / `is_clean_document` / `is_clean_upload` / `is_available_case_document` / `is_rescan_pending`, `self.scanner is None` `RuntimeError`, and `SqlStore` `_touch` + `scan_status` sync | Diff + unit tests in `test_document_rescan.py` and `test_document_controls.py` | `src/core` & `src/api` `ruff`, `mypy`, `unittest` passed | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/document_rescan.py` | Delegated `_pending(doc)` to `is_rescan_pending(doc)` | Diff + `test_document_rescan.py` | `src/core` `ruff`, `mypy`, `unittest` passed | Reconciled |
| `P02-T01` | `src/core/src/zava_forward/core/{store,home_case,signoffs,forms,procurement,taskqueues}.py` | Gated checklists, focus, `home_case` links/views, sign-offs, form candidate listing, procurement capacity commitments, and task-queue freshness on clean uploads | Diff + `test_technical_evidence_usability.py` & `test_document_controls.py` | `src/core` & `src/api` `ruff`, `mypy`, `unittest` passed | Reconciled |
| `P02-T02` | `src/core/src/zava_forward/core/{ai_tasks,data_protection,assistants,chat_case_answers,projection,resident_documents,resident_summary}.py` | Enforced `require_clean` in `ai_tasks.run_document`, pre-`actual_mode` hold in `document_model_hold`, filtered `source_labels`/`assistants.capture`/`chat_case_answers.case_facts`, held quarantined summaries in `projection.redact_staff_detail`, and gated resident document request/summary views | Diff + `test_resident_documents.py` & `test_document_controls.py` | `src/core` & `src/api` `ruff`, `mypy`, `unittest` passed | Reconciled |
| `P03-T01` | `src/core/tests/{test_technical_evidence_usability,test_document_rescan,test_resident_documents}.py`, `src/api/tests/test_document_controls.py` | Added focused unit tests proving download and derivative quarantine across `Store` and `SqlStore`; verified route inventory intact | Test execution logs (`537` `src/core` tests + `452` `src/api` tests) | All Focused-tier checks exited `0` (`RV-001` notes minor optional test-depth addition for `rescan_pending`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| None | No implementation-time plan or phase-detail revisions were needed; implementation matched finalized post-critique plan | None | Plan markers and changes record reconciled | Finalized post-critique (`PC-001`–`PC-006` resolved) | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All six plan-critique findings (`PC-001` through `PC-006`) were directly resolved in planning and verified in code (`#395` exception/retry preservation, `SqlStore` `_touch` + `scan_status` sync, `home_case` / `projection` / `forms.list_candidates` / pre-`actual_mode` `document_model_hold` / `resident_summary.needed_from_you`, `Store.checklist` `(KeyError, TypeError)` preservation, and per-project `ruff`/`mypy` compliance).
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No pause was needed; `P01` -> `P02` -> `P03` executed in strict dependency order.
* Justification assessment: Supported by codebase evidence and Focused-tier test runs.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Provision live Azure Storage Defender malware scanning event/tag infrastructure in Bicep and deployment verification | Issue #117 slice scoped by caller to `src/core` and `src/api` code/test quarantine gate under Focused validation | Infrastructure / cloud readiness workstream (`infra/`) | Open; distinct follow-up route |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Direct unit-test assertion for `SqlStore.rescan_pending()` reopen persistence and `blocked` counter

* Related scope: `P03-T01`
* Evidence: `src/core/src/zava_forward/core/doc_controls.py` (`_scan_stored` `self._touch(case_id)` and `rescan_pending` `blocked` counter) vs `src/core/tests/test_document_rescan.py` and `src/api/tests/test_document_controls.py`
* Impact: Production behavior in `DocControlsMixin._scan_stored` and `DocControlsMixin.rescan_pending` is implemented accurately, and `SqlStore` reopen persistence is verified via `rescan_document(...)`, but adding a dedicated `SqlStore` unit test calling `rescan_pending()` directly across reopen (for both `("failed", ...)` -> `out["blocked"] == 1` and `("clean", ...)` -> `scan_status == "clean"`) would guard against future regressions in batch rescan sweeps if `_touch` were ever moved out of `_scan_stored`.
* Destination: follow-up
* Smallest useful next action: Add a focused `SqlStore` test case in `src/core/tests/test_document_rescan.py` exercising `store.rescan_pending()` with `("failed", ...)` and `("clean", ...)` verdicts across `open_store()`.

## Defects

* None (zero production defects across `src/core` and `src/api`; `server.py` route inventory unchanged).

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | follow-up | Add direct `SqlStore.rescan_pending()` reopen & `blocked` counter assertions in `src/core/tests/test_document_rescan.py` | Non-blocking test-hardening residual item; production implementation is complete and conformant |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001` (`src/core/tests/test_document_rescan.py`): Direct unit-test assertion for `SqlStore.rescan_pending()` across store reopen and `out["blocked"] == 1` counter when batch-rescanning `"pending"` -> `"failed"` / `"clean"`.
* Plan follow-up (`infra/`): Live Azure Storage Defender malware-scanning tag provisioning in Bicep and deployment verification per ADR 0002.

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None (`P01`, `P02`, and `P03` complete)

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `ruff check . && ruff format --check .` | `src/core` | Passed | `All checks passed! 289 files already formatted` |
| `mypy` | `src/core` | Passed | `Success: no issues found in 342 source files` |
| `ruff check . && ruff format --check .` | `src/api` | Passed | `All checks passed! 199 files already formatted` |
| `mypy` | `src/api` | Passed | `Success: no issues found in 283 source files` |
| `python -m unittest -q ...` (26 modules) | `src/core/tests` | Passed | `Ran 537 tests in 296.257s — OK (skipped=20)` |
| `python -m unittest -q ...` (15 modules incl. `test_document_controls`, `test_role_endpoint_inventory`) | `src/api/tests` | Passed | `Ran 452 tests in 614.740s — OK (skipped=61)` |
| `git --no-pager diff -- src/api/src/zava_forward/api/server.py` | `src/api` route inventory | Passed | Empty diff; zero HTTP routes added or modified |
| `tools/rpi-checks.py` | full repository gate | Skipped | Explicitly excluded by caller instructions (`Validation Tier: Focused`; do NOT run `tools/rpi-checks.py`) |

## Outcome

* Outcome: Residual work
* Outcome rationale: All planned phases (`P01`–`P03`), functional/non-functional requirements, critique dispositions (`PC-001`–`PC-006`), and Focused-tier checks are complete with zero production code defects and unchanged HTTP route inventory; one low-severity, non-blocking test-depth item (`RV-001`) and the pre-declared infrastructure follow-up are routed as distinct follow-up work.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | `RV-001` (`SqlStore.rescan_pending()` direct reopen/counter test in `test_document_rescan.py`); Azure Storage Defender Bicep wiring (`infra/`) |

* Execution status: Complete
* Outcome: Residual work
* Validation coverage: Focused tier complete (`src/core` and `src/api` `ruff`, `mypy`, 537 `src/core` unit tests, 452 `src/api` unit tests including `test_document_controls` and `test_role_endpoint_inventory`; `tools/rpi-checks.py` skipped per caller instruction)
* Blockers: None

## Post-Rebase Reconciliation (`fa6f8d1dd`)

* Child RPI continuation task `issue-117-doc-scan-rebase-fa6f8d1dd` rebased candidate commit `4d91dae33` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`fa6f8d1dd`) as `e9c31f7fa051d5fd58795aa7feae7e404760433b`, resolving the single `Store.focus` adjacency conflict in `src/core/src/zava_forward/core/store.py` (`self._open_safety_items` + `is_available_case_document`) and passing worktree-isolated `ruff check .`, `ruff format --check .`, `mypy`, `#117` quarantine suites, `#76` `Store.focus` suite, `test_role_endpoint_inventory`, and `tools/rename-zava-tests.py`.
* Original parent `#117` Review outcome (`Outcome: Residual work` with routed follow-up `RV-001` and Azure Storage Defender infrastructure wiring) is preserved unchanged; see `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-rebase-fa6f8d1dd-review.md` for the rebase-continuation Review record.

## Post-Rebase and CI Test-Fixture Reconciliation (`0358b9ad5` / `ad005cd5f`)

* Child RPI continuation task `issue-117-doc-scan-fix-rebase-0358b9ad5` rebased `feat/demo-117-doc-scan` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`ad005cd5f` atop `0358b9ad5`, replaying `#117` implementation as `058fcc3e8`) and committed `3efbe346a7b8cb066a94b157271b6ac7ec39edd7` adding clean synthetic scan metadata (`scan=dict(status="clean", scanner="Synthetic metadata fixture")`) to the pre-gate `Store.EVIDENCE` setup stubs in `src/core/tests/test_resident_decisions.py` (`test_resident_acceptance_never_clears_technical_or_hazard_gates`) without weakening `is_available_case_document` fail-closed missing-scan quarantine.
* Re-verified `src/core` (focused 484 tests OK + full 3,660 tests OK, `ruff` 298 files, `mypy` 351 files), `src/api` (`test_document_controls` + `test_role_endpoint_inventory` 44 tests OK, `ruff` 213 files, `mypy` 297 files), and `tools/rename-zava-tests.py` (25 tests OK). Original parent `#117` Review outcome (`Outcome: Residual work`, `RV-001`) remains preserved unchanged; see `.copilot-tracking/reviews/logs/2026-11-15/issue-117-doc-scan-fix-rebase-0358b9ad5-review.md`.

