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
