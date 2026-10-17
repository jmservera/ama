<!-- markdownlint-disable-file -->
# RPI Changes: consultation-record-controls-92

Task ID: 92. Date: 2026-10-17. Declared scope: full approved P01/P02.
Execution: Complete P01/P01-T01/P02/P02-T01/P02-T02. Independent Review complete.
Plan and phase details dated 2026-10-17.
Original independent critique Revise retained; PC-001/PC-002 directly resolved.

## P01: Record and gate consultation

Completed P01/P01-T01: explicit unverified supplied-human records and unknown gate.
No Legal authority exists for contract consultation; no operational release path
will be invented. Shared edit declared: server.py one procurement route. No
Store/SQL/app.js/ops.js/generated-fixture edits planned.

## P02: Validation and Documentation

Completed P02-T01: 10 canonical core semantic methods and 3 canonical HTTP methods,
inherited by JSON/SQLite/opt-in MSSQL variants. No guard patches in new tests.
Explicit historical orders reach all five guards; all five individual in-memory
guard-removal mutants were killed by the reachable-seam test.

Initial test command failed with missing installed zava_forward. Created local
venv and installed editable src/core[dev,sql], src/agents, src/api[dev].
Core configured full Ruff and mypy pass (113 files); API Ruff/mypy pass
(54 files), targeted formatting passes. Initial new core mypy failures were
resolved with a typed dynamic test factory and lazy existing MSSQL harness import.
Initial SQL harness invocation missed the API test package path; corrected
PYTHONPATH includes src/api. Actual task-owned SQL Server 2022, loopback port
32796, database consultation92: all 10 new core methods pass with no skips,
including record/reload, source/actor/procurement writer conflicts and recovery.
No credentials appear in evidence.

Expanded regression run: 321 executions, 47 skipped, one legacy role-matrix setup
error caused by the intentional new consultation hold. Added an explicit
test-local consultation isolation patch to that single historical role test;
rerun passed: 321 executions, 47 skipped, no errors/failures. Skips are existing
opt-in MSSQL/browser checks and the JSON-only SQL transaction test.
Other legacy regression isolation changes are setup-only in
procurement, building, hazard and resident tests; no corresponding domain source
was edited. Existing #90 success tests cannot establish #92 acceptance.
No fixtures/dataset/hash manifests or shared Store/SQL files changed.

## Implementation-Time Plan and Detail Updates

PC-001/PC-002 direct dispositions applied before implementation; original
independent Revise verdict retained. Actual source/API routes and no UI edits
match approved scope. Additional role-matrix legacy setup isolation is an
immediately relevant test-target correction, not a new approval/bypass in runtime.
Canonical authored method counts remain within 18 core / 4 API maxima.

## Validation Record

* Targeted JSON/SQLite/API/independent-control run: 321 executions, 274 passes,
  47 explicitly skipped. Missing law-store warnings preserve unknown, not success.
* Actual task-owned SQL Server 2022: 70 passes, no skips. Includes 10 new core
  methods, 3 unpatched HTTP methods, existing MssqlProcurement/
  MssqlProcurementApi/MssqlStockDecisions/MssqlFinanceSignoffs.
* Five in-memory individual seam-guard removals: all detected by the new
  reachable-seam test as missing expected consultation refusal. No source mutation.
* Configured full core/API Ruff and mypy: pass (113/54 files); applicable changed
  files format checks pass. Diff whitespace check passes.
* Migration regression initially failed for missing python-pptx/Pillow;
  restored those plus PyYAML in the task-local venv, then 25/25 pass.
* Existing scenario manifest suite: 8/8 pass against actual unchanged combined
  public fixture hashes; provisional/proposed authority remains unchanged.
* Web/browser/accessibility, official legal-currentness, Azure and paid AI:
  not run, not required for backend-only record mechanics and not claimed.

## Pre-Review Reconciliation

Plan markers, details, evidence, source boundaries, partial acceptance and
handoff all current. No unfinished implementation markers. No new Legal role,
approval registry or let/renew route. Both exact criteria remain partial.
Ready for one independent Review; retain original outcome and route any findings.

## Independent Review and Publication Handoff

One independent Review executed, original outcome `Conformant with justified
divergence`, no implementation defects and no source correction requested.
Reviewer independently ran 35 executions: 34 passes, one explicit JSON SQL-check
skip. RV-001/RV-002 are accepted human-authority and genuine let/renew follow-ups,
not fabricated approvals or new active implementation markers. Original
critique and Review artifacts retained without replacement or a repeat pass.
Task-owned SQL container `ama-issue92-027d5c68-sql` and temporary credential file
were removed exactly; no shared resource was touched.
Continue normal commit/push/main PR with Refs #92; keep issue open and stop
per the explicit caller condition. Exact final head and PR receipt follow in state.

Publication: https://github.com/jmservera/ama/pull/389, target main, branch
feat/consultation-record-controls-92. Source/review commit:
`b86f930cbfa4b710a3445829332e3c44e50f2729`. Fresh authenticated GitHub identity
was resolved immediately before commit; repository-local noreply address used
for author and committer, with required Copilot trailer. Resume session:
`027d5c68-828d-47c9-8522-659504917170`. State records the explicit stop condition
and ranked residuals. A final tracking-only receipt commit records publication;
no source correction, review replacement, merge or issue closure occurred.

## Remaining Work and Acceptance Boundary

No active implementation markers remain. Actual named Legal consultation
authority and dedicated let/renew workflow are external gaps. Both exact issue
criteria remain partial; keep issue open.

## Coordinator-Authorized Main Integration (2026-10-17)

The coordinator explicitly authorized rebasing only this topic and publishing
with an explicit expected-old-SHA lease. Before the operation the worktree was
clean, on feat/consultation-record-controls-92, and both local/remote old head
were `5411f0d41fc4425a5ab3cc9592f175a2f293bd82`. Freshly fetched main was
`1a05dfb8a4c4d9992d72a57228ce15123e9bcf2c`, containing hazard PR #388.
Replayed source commit `b86f930c` as `0282b7ff` and receipt commit `5411f0d4`
as `2e5732cf`; no main/other-worktree/PR #387 write or extra Review.

### Conflict intent and source-boundary evidence

Only manual conflict: docs/reference/log.md. Retained all upstream hazard
correction/adverse-Review/integration entries, then appended the complete own
consultation entry. Verified upstream log bytes are the exact prefix, with own
old suffix intact. Component READMEs, KB index/synthesis and hazard test setup
auto-merged; inspected their actual combined intent, not blind side selection.
All upstream inspection routes and own #92 route remain present.

Entire own src runtime/test/README added/removed bytes match before/after the
rebase. SHA-256 of the ordered path plus added/removed line stream:
`246a5f1a055c53bdf042ae188aa9db83b38144bfc40346f18071f7171cc0a128`.
`git range-diff` shows only the KB log context changed in the source commit;
the receipt commit is patch-identical. Original Review bytes retained:
`e4a7543ac73f1e0fdaee61ca8c093acdb1cc4f6b9b2c433b69fcb7384391a59f`;
original critique bytes retained:
`dc6c9bca23f55e9f80cfc9ed231547ae668b0e72cee5b538ab5b6f25ec24ce17`.

Own procurement/controller/new-test bytes are exact old-head matches.
Upstream hazard, workflows, shared SQL, Store, finance, grants, signoffs, MSSQL
harness, dataset/building fixture and scenario manifest bytes are exact new-base
matches. Thus current-actor/scoped-hold/recovery hooks and prior-pending versus
committed-audit semantics were not rewritten. The sole own hazard test delta
remains the explicitly disclosed consultation-only legacy setup isolation.

### Actual integration validation

Existing local venv still imports editable src/core and src/api in this worktree.
No dependency install or PYTHONPATH=mvp workaround was used.

The first combined command omitted `src/api` from test-package search, so the
new upstream test_hazard_api import failed (`tests.test_mvp` unavailable).
Corrected command, not source:

```bash
PYTHONPATH=src/api:src/core/tests:src/api/tests:src/agents/tests \
  .venv/bin/python -m unittest test_consultation_controls test_quality_procurement \
  test_procurement_api test_buildings test_hazard_referral test_hazard_api \
  test_resident_decisions test_stock_reconciliation test_finance_match_controls \
  test_grant_lifecycle_controls test_finance_signoffs test_role_matrix \
  test_scenario_manifest -q
```

Actual result: 348 executions, 300 passed, 48 explicit skips, no errors/failures.
This includes actual SQLite and JSON consultation/hazard authority, rollback,
recovery, shared stock/finance/grant/provider and HTTP checks. Missing-law-store
warnings remain unknown, not successful legal validation. Opt-in backend/browser
skips were not promoted to passes.

Configured full core and API Ruff check/format/mypy passed: core 61 formatted
files and 114 typed files, API 22 formatted files and 54 typed files.
Six added relative documentation links/anchors and diff whitespace checked.
Scenario manifest validated against the actual unchanged combined fixture hash;
no provisional/proposed authority was promoted.

No source/shared-persistence conflict or source adjustment occurred. For this
documentation-only manual resolution, exact source parity plus combined
SQLite/JSON/API smoke and static checks satisfy the coordinator's stated
integration requirement. No new MSSQL container/run was required or claimed.
The earlier 70 actual local SQL Server passes remain original-phase historical
evidence, not new integration parity. No cloud, paid AI, browser or operational
legal validation was performed.

### Exact criteria and bounded coordinator follow-up

Criterion 1 remains partial: a source/version-bound supplied-human decision
recording seam exists and works fail-closed, but its registered manager recorder
is not a verified authorized Legal decision-maker. No actual authorized Legal
decision, contract-consultation capability or delegation is fabricated.

Criterion 2 remains partial for an independent engineering reason: there is no
genuine contract/framework/call-off let/renew transition or authoritative
integration seam in this module. Ordinary work-order confirmation is not letting
or renewal. Absence of a human approval is not the reason that software seam is
absent and does not prohibit building isolated fail-closed mechanics.

Bounded follow-up for the coordinator: separately plan a real package-linked
contract let/renew transition or integration with the authoritative procurement
operation, bind its explicit consultation guard to the exact contract/scope/source
and current authorized human decision, and prove unknown/stale/unauthorized
denials on fictional stores before any operational activation. Keep default deny
while authority is unavailable; no new financial purchase API, real contract or
portal. This is proposed remaining engineering, not secretly added current scope.

Original full RPI phase artifacts and independent outcome remain intact.
Coordinator final-head independent review is pending. PR #389 remains Refs #92
with empty closingIssuesReferences; checks may be absent and are not declared
green. Publish only this branch using expected old remote SHA
`5411f0d41fc4425a5ab3cc9592f175a2f293bd82`; no merge or issue closure.
