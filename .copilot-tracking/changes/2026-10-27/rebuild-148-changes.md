<!-- markdownlint-disable-file -->
# RPI Changes: rebuild-148

## Metadata

* Task ID: 148
* Implementation date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/rebuild-148-plan.md
* Details: .copilot-tracking/details/2026-10-27/rebuild-148-phase-details.md

## Execution Status

Complete for full authoring plan P01/P01-T01/P01-T02; no active plan markers remain.
No live Azure adapter, private data/secret access, deployment or teardown.

## Execution Summary

Approved boundary: one orchestrator module, one external test module and two
component/runbook documentation updates. All issue criteria remain partial.

## Implementation-Time Plan and Detail Updates

PC-001/002 applied before implementation. PC-003 rejected because the alleged
system-temp prohibition is not in this parent execution context. Original
Revise critique retained. No second critique, no new user decision.

## Validation Record

Initial interpreter import failed: ModuleNotFoundError zava_forward. Created
external /tmp/ama-148-venv and pip-installed editable core/orchestrator without
dependency resolution plus existing pinned Ruff 0.17.1 and mypy 2.4.0.
No manifest/pin change or uv use.

## Blockers

None for authoring. Real resource/retention/preservation/tenant authority and
disposable Azure acceptance remain outside scope.

## Completed Work

### Checked sequencing and bounded inventory (P01-T01)

New src/orchestrator/src/zava_forward/orchestrator/rebuild.py implements
17 fixed stage/check contracts, separate generic/budget inventories, explicit
subscription/ama scope, known-type/dependency ordering and exact remaining
inventory readback. Locks, retained data, absent boolean safety metadata,
unknown types and inventories above 1,000 records fail closed. No shell,
subprocess, Azure adapter, credential handler or data path option exists.
The CLI permits dry-run or a fresh synthetic-local rehearsal only.

### Disposable SQL and failure evidence (P01-T01)

New src/orchestrator/tests/test_rebuild.py has 22 tests with subtests for every
operation/check failure. It covers fixed trace, scope/types/duplicates,
missing/changed protection, budget drift, unexplained disappearance, lingering
deletes, operation failure, zero-inventory recheck, SQL seed/staff/audit tamper
through new connections, repeat fresh runs, exclusive file creation, private
environment non-use, argument rejection and sanitized CLI errors.

The local adapter generates its own SQLite control-plane fixture schema, not
the application core Store. This is an ordinary implementation clarification:
local schema checks are real SQL readbacks, but not application integration.
Seed/staff/workload-sql/restart are labelled local-sql-verified; remaining stages
are simulated-not-live. Temporary workspace contains only generated fixtures;
no private stock, actual staff, profile or environment file is opened.

### Runbooks and execution (P01-T02)

infra/README.md and src/orchestrator/README.md document exact commands, no-Azure
boundary, result classifications, failure semantics and retained-data/tenant/
lineage residual gates. Historical 2026-10-12 observed results are unchanged.
No knowledge-base source changed, no workflow or check name changed.

## Validation Results

| Check | Result | Evidence |
| --- | --- | --- |
| First focused unittest attempt | Failed | 19 tests; 3 tamper subtests had uncommitted changes invisible to independent readers; fixed fixture to commit before verifying, not production isolation |
| Initial Ruff | Failed | formatting/line length and test default construction; corrected with existing formatter and optional default |
| Initial full orchestrator discovery | Passed with skip | 66 tests, 1 SQL-driver skip before driver restoration |
| Initial mypy | Failed | mssql_python missing in existing worker/tests; installed existing core sql extra pin mssql-python==1.15.0 via pip |
| Full orchestrator discovery after installation | Passed | 68 tests, zero skips; PYTHONPATH=../core/tests /tmp/ama-148-venv/bin/python -m unittest discover -s tests -q |
| Ruff check and format | Passed | full src/orchestrator project |
| mypy | Passed | strict project config, 14 source files |
| Installed CLI dry-run | Passed | 17 stage contracts; no backend/workspace operations |
| Installed CLI synthetic-local | Passed | 17 stages, 10 modeled deletions, zero generic and budget inventories; scope explicitly synthetic/local |
| git diff --check | Passed | no whitespace errors |
| Azure/deployment/private data/real models | Not run | expressly excluded; no cloud fallback |
| Heavy local gate | Not run | bounded source-only tool; owner disallows --all and permits --changed only for large changes |

CLI output artifacts remain external in the session files directory:
rebuild-148-dry-run.json and rebuild-148-local.json.

## Acceptance Evidence

| #148 criterion | Status | Evidence and missing boundary |
| --- | --- | --- |
| Checked scripted rebuild; no secrets on argv | Partial | Fixed local stage/check engine and CLI tests; real helper integration is not implemented |
| Dependency teardown, budgets, empty inventory | Partial | Synthetic inventory ordering/readback tests and local roundtrip; no Azure teardown |
| Synthetic seed and staff reconciliation | Partial | Generated local fixture rows survive reopen; no real store/tenant reconciliation or continuing lineage restore |
| Dry-run and disposable environment test | Partial | Zero-backend-I/O dry-run plus disposable local SQLite exercise; no disposable Azure exercise |

No issue checkbox is ticked and the PR must use Refs #148.

## Pre-Review Reconciliation

Plan markers/details, completed source/docs, validation and partial-acceptance
language reconciled. No active authoring task remains. One independent Review
is next; human/live approval is not supplied by local checks.

## Remaining Work

No active implementation markers. Single independent Review and draft publication.

## Follow-Up Items

Authorized cloud integration, preservation/retention approvals and actual
disposable Azure test; see canonical plan Follow-Up Items.
