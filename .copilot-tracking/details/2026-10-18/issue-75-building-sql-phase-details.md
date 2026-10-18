<!-- markdownlint-disable-file -->
---
title: Issue 75 building SQL phase details
description: Task-level evidence and completion requirements
ms.date: 2026-10-18
---

## Metadata

Task 75 / issue-75-building-sql. Related plan:
`.copilot-tracking/plans/2026-10-18/issue-75-building-sql-plan.md`.
Research C2-C6 establishes fixture/store/HTTP test contracts.
Status: Ready after original Revise critique; PC-001 through PC-004 directly
disposed in plan and incorporated below before implementation.

## Phase Index

| Phase | Direction | Initial status |
| --- | --- | --- |
| P01 | Focused test-only conformance | Complete |
| P02 | Local constructed evidence | Complete; adverse attempts preserved |
| P03 | Single original Review and draft publication | Review ready |

<!-- rpi:phase id=P01 -->
## P01: Add focused conformance evidence

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add MSSQL semantics and HTTP replay

Context: core tests loop JSON/SQLite and API tests instantiate reusable fixture.
The existing MSSQL module has wipe/factory, runs in CI and exempts migrated
untyped harness style from configured strictness; do not add exemptions.
Include only `test_mssqlstore.py` and focused README text. No removals.

Use a scoped unittest.mock patch of `building_fixture.SqlStore` to a bounded
wrapper of existing `factory`, then call unchanged `open_store(folder, True, data)`.
Register db.close immediately after construction before fallible contract/capacity
setup. Each test wipes only the explicitly disposable database. Existing wipe
closes its short-lived connection in finally; no table-list changes.

Planned focused semantic cases:

* Persist a nonempty dependency and full building record plus separate home
  evidence/allocation. Save, close, unlink constructed seed, reopen through
  existing factory and assert record/home payload equality.
* Open two distinct raw sessions, commit hold on one, read synchronized view
  on the other. Under first local lock retain stale snapshot, second commits
  a version/label winner, first attempts conflicting hold erasure/version.
  Require ConflictError and a third connection's exact winner comparison.
* Issue matching order before hold. Persist hold, independently reopen/read;
  refuse target advance, matching issue/reissue with unchanged cases/orders.
  Every issue/reissue, including expected failures, supplies valid explicit
  resident_bindings=[{"measure": "Loft insulation", "context_revision": 1}].
  Assert Building SYN-B1 and HOLD-1's label in each refusal, not resident-scope
  or duplicate-order refusal. ZF-2/PKG-SHARED refuses; ZF-2/PKG-OTHER issues and
  reissues; ZF-3/PKG-SHARED issues/books/advances using
  `supplied_appointment_fixture`. Assert exact resulting stage and retained hold.
* Separately construct missing resident/funding/technical prerequisites with
  clear building and accepted sibling. Assert GateError and exact unchanged
  cases/documents/quality after building read and advance refusal. Assert the
  exact corresponding resident/funding/technical reason, not merely GateError.
* Construct submitted target QA and accepted/closed sibling; reject target
  handover with the exact unaccepted-QA transition reason and retain both states
  after independent SQL reopen.

HTTP class inherits existing BuildingHttpTests unchanged, patches fixture
constructor only during parent setUp and wipes database first. All three
HTTP tests execute unchanged on SQL. Subclass cleanups own partial/successful
setup: register connection closure inside factory; use a patch context manager;
always register partial HTTP cleanup even if parent setUp fails. Shutdown/join
only a started live thread, then close server/tmp. Override successful parent
tearDown so resources are not doubly closed; cleanups run in reverse acquisition
order. Record a contained fault probe without increasing committed test count.
No real AI invocation: assistant test only reads registry.

Completion evidence: scoped diff, explicit test names and exact assertions.
No unresolved choice; real failures may require descriptive amendment, not
speculative production edits. Material intent/authority issue stops affected task.

<!-- rpi:phase id=P02 -->
## P02: Execute local validation and reconcile evidence

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run focused regressions and actual owned SQL

Depends on P01. Install source distributions only after already observed missing
dependency failure. Isolated task virtualenv, pip; no PYTHONPATH=mvp.
Select core `test_buildings`, `test_quality_procurement`; API
`test_buildings`, `test_procurement_api`, `test_role_matrix`,
`test_mssqlstore.SharedSqlIsPortableTests` using src test paths.
Run opt-in-off new class selection and report skips as Not run separately.

Actual SQL: create UUID task-named SQL2022 container bound 127.0.0.1 to an
ephemeral port, generated ephemeral password only in subprocess environment,
no mounts. Inspect responsiveness before testing. Create UUID task database;
configure all ZF_SQL_* explicitly, never source .env or inherit configured
dataset. Select only new building classes using existing module infrastructure.
All validations use an allowlisted subprocess environment, retaining only local
tool lookup/home/locale settings, never ambient ZF_* or Azure/model credentials.
Force verified selectors ZF_DOC_STORE=local, ZF_SCANNER=local,
ZF_AUTH=password, ZF_ENV=test,
workspace task-owned TMPDIR, ZF_DOC_DIR and ZF_DIGEST_DIR. Verify actual selector
names before invocation; do not print or inspect previous environment values.
Only known explicitly constructed input paths are passed. Workspace scratch
is `.copilot-tracking/.issue75-scratch/` and is removed after exact-path cleanup.
Capture full test output, SQL version/database and cleanup by exact container ID.
Finally remove exact owned container, verify absence; its database disappears
with container. No new committed tooling/service for this operation.

Also `python3 tools/rename-zava-tests.py`, API `ruff check .`,
`ruff format --check .`, `mypy` using its configured exclusions.
Run smallest targeted checks first. No changed image inputs means image,
nonroot and browser/a11y reruns are not applicable, not implicitly passing.
All errors and SQL skips remain evidence. No completed human review checkbox.

<!-- rpi:phase id=P03 -->
## P03: One original Review and publication

<!-- rpi:task id=P03-T01 -->
### P03-T01: Review once, freeze evidence and publish draft

Depends on P02 reconciliation. Original Review assesses exact test/source diff,
acceptance mapping, adverse evidence and production boundary; one execution
only, retain unfavorable verdict. Independent plan critique is not this Review.
Commit all issue RPI artifacts plus executable/docs change together; no private
data, credentials, generated logs with secrets or unrelated changes.
Use authenticated gh user ID/login noreply for author/committer. Include
Conventional Commit and required Copilot trailer. Push only supplied topic,
draft PR targeting main, Refs #75 only, no issue closure verbs or checkbox ticks.
Publication metadata may need one evidence-only follow-up commit; do not
change assessed source after Review. Do not self-merge or rewrite/rebase.
Completion: frozen SHA/base, draft URL, path inventory, actual SQL results,
cleanup and explicit operational/human/live gates. No child task automatically.
