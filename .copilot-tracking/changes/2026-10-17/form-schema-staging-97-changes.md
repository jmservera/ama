---
title: Issue 97 implementation evidence
description: Fail-before, changes, validation and explicit acceptance limits
ms.date: 2026-10-17
---

## Scope and execution

Task 97 / form-schema-staging-97. Full P01-P03 plan scope, automatic parent continuation. Plan and details dated 2026-10-17; exactly one critique executed and PC-001 through PC-005 resolved before implementation. Status: P01-P03 complete; ready for one Review of the bounded engineering slice.

## Environment

Own pip venv in session files (`venv97`), Python 3.12.3. Installed existing editable src/core, src/agents and src/api before application use. Initial `python -m ruff --version` and `python -m mypy --version` failed with No module named ruff/mypy. Installed existing declared core/API dev extras with pip after that missing-tool evidence. No manifest dependencies added.

## P01-T01: Fail-before evidence

Before production edits, focused core discovery failed importing the absent `zava_forward.core.forms` contract (1 error). Separately started the existing real loopback HTTP harness and authenticated fixture staff; POST `/api/form-schemas` returned actual 404 `{"error":"Not found."}` and failed the expected 201 assertion. This is observed missing API behavior, not a missing installed distribution. Both commands exited 1. Service was stopped by cleanup.

After initial core implementation, 12 focused tests ran with one meaningful failure: `Store.detail` copied the new raw staging body into generic detail. Fixed the exact leak by removing `form_staging` from generic detail, leaving it accessible only through the dedicated current-rights endpoint. This tests the requirement rather than treating import success as behavior proof.

## P02: Implementation

Added one typed core `forms.py` module and two external test files. Registry versions remain immutable and unapproved; source authority is policy metadata only. Candidate staging preserves source ID/hash/version/date, exact raw values/locators, supplied parser/model/OCR lineage and separate observed verification. Unsupported inputs yield owned manual recovery; no AI/extraction/approval/review/pack workflow is activated.

Reused actual `ai_registry.digest`, Store document scan/hash helpers, current staff rights, SqlStore checked shared documents and case-row versions/audit. Added `form_schemas` to existing SQL DOCS; fixed missing checked-document sync cleanup so rolled-back first registry writes cannot remain as process-local ghost state. MssqlStore inherits this path; no new table or dialect implementation.

Dedicated authenticated API endpoints handle registry and case-bound batch reads/writes; generic detail strips raw staging entirely. All operations require the conservative existing rights intersection. SQL current actor is reread through existing `assistant_connection`, not the stale process staff cache. Errors are explicit and diagnostics exclude exception content/raw values.

Updated only core/API component docs plus one additive reference-index row and append-only log entry. No UI/web assets, private data or concurrent infrastructure/credential/sensor source changes.

## P03: Validation

Initial complete checks: core Ruff/format/mypy passed, then 549 core tests passed in 272.459s with one existing opt-in skip. API Ruff/format/mypy passed, then 565 API tests ran in 251.662s with one failure and 110 skips: the existing role endpoint inventory correctly rejected the new unlisted `/api/form-schemas` route. Added new registry/candidate GET/POST paths and dynamic action to that existing inventory, preserving all previous entries and tests. Classified as an immediately relevant integration amendment, no repeated critique.

Final focused checks after additional fault/source-policy coverage: 15 core form tests passed; two real loopback HTTP form tests passed with no skips. All core Ruff/format/mypy checks passed again (102 source files); all API static checks passed (48 source files). Valid-payload baseline exercise loaded the original `abaca788` server without changing checkout: a valid synthetic schema still returned 404 and failed expected 201, confirming exact missing behavior on the base.

Final complete reruns on the final source:

| Check | Command (own pip venv; component working directory unless noted) | Actual result |
| --- | --- | --- |
| Core focused | `python -m unittest discover -s tests -p test_form_staging.py -q` | 15 tests passed, zero skips, 8.095s |
| HTTP fixture (repository root) | `PYTHONPATH=src/api:src/core/tests:src/agents/tests python -m unittest discover -s src/api/tests -p test_form_staging_api.py -v` | 2 tests passed, zero skips, 2.274s; responsive loopback health/auth/registry/stage/read/denials; inference patched to fail |
| Core full | `python -m unittest discover -s tests -q` | 551 run, 550 passed, 1 existing opt-in skip, 257.634s |
| API full | `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q` | 565 run, 455 passed, 110 existing opt-in skips, 239.150s; endpoint inventory now passes |
| Core static | `python -m ruff check . && python -m ruff format --check . && python -m mypy` | Pass; 49 format targets, 102 mypy source files |
| API static | `python -m ruff check . && python -m ruff format --check . && python -m mypy` | Pass; 18 format targets, 48 mypy source files |
| Diff | `git diff --check` | Pass |

Existing opt-in skips include SQL Server/Azure and browser integration gates; no skipped live check is claimed passed. Existing safety tests emit the explicit expected unavailable-law-store diagnostic; that is not a model call or successful law evaluation. Core suite also emitted pre-existing unclosed-file ResourceWarnings in sensor fixture tests; those unrelated sources were not changed.

The loopback fixture runs only temporary constructed data and stops its server/thread on cleanup. Source/registry restart tests reopen temporary SQLite without reading a seed. No private dataset, real SQL Server/Azure, billable inference, Docker execution, remote checks, actual approval or external submission was used.

## Reconciliation and discoveries

All P01-P03 tasks now have completion evidence, details match the implemented contract and docs, and no active implementation blocker remains. Ordinary local corrections: actual digest helper, generic-detail exclusion, current SQL staff read and rollback of missing shared-document state. Immediately relevant integration amendment: existing role inventory extended after actual full-suite failure. No significant scope divergence or repeated critique.

Review must distinguish bounded code conformity from unmet approved-schema/full-PRD acceptance. Follow-ups remain actual template authority/binding, #98 workflow and any future task-specific AI release; none is activated here.

## Acceptance and remaining boundaries

No actual approved template or form authority supplied. No fixture is approval. Unapproved collection does not satisfy approved preparation or full AC-046/047/053. No live extraction/model, SQL Server/Azure, human review, #98 workflow or submission.

## Authorized integration continuation 2026-10-17

Continued the same #97 / PR #377 loop at the caller's explicit request, not a
new research/plan/implementation/review cycle. Starting topic was clean at
`c021a3fd84636d255450959eef2089749f712d44`. Fetched and rebased the two run-owned
commits onto `origin/main` at
`0bdcb2f0e55aedf28445bac1fc6f1bbae5b68134`, including #373, #374 and #376.
The resulting source/handoff commits are `1e59021` / `81c9922`.

Only conflicts were additive `docs/reference/README.md` and `log.md`. Kept
all upstream credential and queue index rows and log entries, the upstream
sensor entry, and the topic's form entry. Verified the current log begins
with the entire upstream log byte-for-byte and every upstream index table
row remains. No credential, sensor or web implementation was edited.

`git range-diff abaca788..c021a3f origin/main..HEAD` showed only conflict-context
changes, the already-upstream API README date and the preserved sensor-test
typing override context; the handoff patch was identical. All five topic
runtime files (forms, server, store, sqlstore, projection), both staging tests
and the endpoint inventory remain byte-identical to the independently reviewed
`c021a3f` content. Queue/store/permission tests were selected because upstream
queue assets consume the existing server/store boundary; no browser behavior
was rewritten. Existing editable pip environment was reused; no install needed.

| Integration gate | Exact command (existing venv Python; component directory) | Actual result |
| --- | --- | --- |
| Core staging/permissions/store/queue | `PYTHONPATH=tests python -m unittest test_form_staging test_documents test_sqlstore test_sqlreads test_taskqueues test_sqlqueues test_queue_benchmark -q` | 84 tests passed, zero skips, 106.460s; includes all 15 form tests and synthetic 60,000-case queue checks |
| API staging/permissions/auth/documents/queue | `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_form_staging_api test_role_endpoint_inventory test_role_matrix test_auth test_document_controls test_task_queue_api -q` | 80 tests passed, zero skips, 32.391s; includes both loopback form tests |
| Core gates | `python -m ruff check . && python -m ruff format --check . && python -m mypy` | Passed; 51 format targets, 104 mypy files |
| API gates | `python -m ruff check . && python -m ruff format --check . && python -m mypy` | Passed; 18 format targets, 48 mypy files |
| Upstream JS parse | `node --check src/zava_forward/api/web/app.js` | Passed; no web edits |
| Whitespace and preservation | `git diff --check`; upstream prefix/row and original runtime-byte comparisons | Passed |

API tests emitted expected unavailable-law-store and explicit authentication
denial diagnostics; no failed test or skipped check. Previous complete-suite
counts above belong to the pre-integration source, not fresh full-suite runs.
No live/private/cloud checks, browser run, infra test or approval was claimed.
Reviewer `97fdbce9` is independently reviewing `c021a3f`; final exact-head
delta follow-up remains required. Review outcome stays Residual work; real
approved-template authority/binding remains unmet and #97 must stay open.

After publishing integration head `a5a8018`, attempted direct same-task handoff
to the caller-supplied reviewer ID `97fdbce9`. The agent tool returned
`No agent found`; that reviewer is not addressable from this session. No
replacement or new review loop was launched. Final exact-head follow-up must
be routed through PR #377/coordinator; it remains a real unresolved review
handoff, not a claimed reviewer approval.

## Correction cycle ONE: first-use scan persistence, 2026-10-17

Caller relayed independent reviewer `97fdbce9` verdict **REVISE** on `c021a3f`:
first-use scanning of pending/missing scan metadata saves the SQL case, clearing
its touched set before staging appends the batch. The success audit could
persist without the candidate body. Rebase was already complete at correction
baseline `387747a`; the defective runtime was unchanged by integration.

Added regressions before touching production. Actual fail-before commands
(existing venv, component directory):

* Core: `PYTHONPATH=tests python -m unittest test_form_staging.FormStaging.test_rescanned_sources_retain_full_batch_after_reads_and_sql_reopen test_form_staging.FormStaging.test_rescan_final_save_failure_and_conflict_do_not_commit_batch_or_success_audit -v`.
  Exit 1: two missing-batch errors (pending and absent scan), failed rollback
  assertion and missing expected cross-process ConflictError; 2 methods, 0.817s.
* API: `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_form_staging_api.FormApi.test_rescanned_sql_sources_persist_after_repeated_http_reads_and_reopen -v`.
  Exit 1: both pending/absent scan returned authenticated POST 201, then failed
  full-batch lookup during repeated actual GET/detail reads; 1 method, 1.106s.

Root correction: immediately before append, reacquire the current case via
existing `store._case(case_id)` after scanning/validation have finished. This
reenlists the current case in SQL optimistic save/discard tracking, with no
new transaction helper, permission bypass or source authority change.
Regression assertions compare the entire saved batch (raw value, locator,
source/hash/version and supplied processing lineage) across repeated reads,
generic detail and a new SQLite store. Fault regression fails the final save
after successful scan; cross-process mutation tests the current case version.
Both verify no retained candidate or success audit on refusal. The independently
durable scan is not falsely rolled back or counted as staging success.

| Correction validation | Exact command (component directory, owned venv Python) | Actual result |
| --- | --- | --- |
| Focused core | `PYTHONPATH=tests python -m unittest test_form_staging -q` | 17 passed, zero skips, 5.466s |
| Core relevant suite | `PYTHONPATH=tests python -m unittest test_form_staging test_documents test_sqlstore test_sqlreads test_taskqueues test_sqlqueues -q` | 85 passed, zero skips, 55.996s |
| API relevant suite | `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_form_staging_api test_role_endpoint_inventory test_role_matrix test_auth test_document_controls test_task_queue_api -q` | 81 passed, zero skips, 27.996s; includes 3 real HTTP form methods |
| Core static | `python -m ruff check . && python -m ruff format --check . && python -m mypy` | Passed, 51 format targets / 104 mypy files |
| API static | `python -m ruff check . && python -m ruff format --check . && python -m mypy` | Passed, 18 format targets / 48 mypy files |

Initial correction lint found two test closure loop bindings; explicitly bound
the callback defaults and reran core suite/gates successfully. Existing expected
law-store/auth refusal diagnostics remain in API tests. No full-suite rerun,
live SQL Server/cloud/private/paid inference or actual approval claimed.
Independent **REVISE** is not superseded: reviewer must reverify correction on
the final pushed head. Actual approved-template authority remains RV-001
unmet; registry prerequisite exists, #98 remains undelivered. Same loop, one
correction cycle, no scope expansion or issue closure.
