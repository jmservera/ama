<!-- markdownlint-disable-file -->
# RPI Phase Details: consultation-record-controls-92

Task ID: 92. Date: 2026-10-17.
Plan: .copilot-tracking/plans/2026-10-17/consultation-record-controls-92-plan.md.
Research: .copilot-tracking/research/2026-10-17/consultation-record-controls-92-research.md.

<!-- rpi:phase id=P01 -->
## P01: Record and gate consultation

Context: procurement packages are versioned contract references, not awards.
The existing manager authority is not Legal authority (research C3-C8).
Boundary: source stays in src/core; one API route in shared server.py, no shared
Store/SQL or UI edits. All supplied statuses remain unverified.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add record-only procurement mechanics and authenticated route

Require a registered manager recorder, named human decision maker supplied by the
caller, exact status/reason and source document coordinates. Require expected
consultation record version and store contract/scope/source hash and UTC server
provenance in append-only-by-application history. Validate original source bytes
using existing capacity-source mechanics; register the case rowversion with the
existing SQL validation context. Use a consultation action in `_proc_operation`
that authenticates the recorder without pretending it is contract/Legal authority.

Expose supplied status plus effective unknown and explicit unverified authority
in package lists. No positive record may satisfy the gate; missing/malformed or
mutated records remain unknown. Add guard calls at issue/reissue/correct/Booked
and require_booked_capacity, before successful side effects. Preserve negative
appointments, factual completion and withdrawal.

Completion: unmocked denial tests for all relevant seams; source records round-trip;
HTTP permission, input and conflict behavior; no automatic legal decisions.

<!-- rpi:phase id=P02 -->
## P02: Validate and document

Depends on P01. No hidden test success from fabricated approvals.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add exact semantic, mutation and transaction tests

Exercise four statuses, unknown defaults, no authority from user fields, forged
actor, stale record version, invalid/missing/generated source, byte/version change,
scope/contract version, rollback before commit, restart persistence and safe
non-binding operations. No guard substitution in #92 semantic tests. Existing
other-domain success tests may explicitly isolate this guard, documenting that
their pass does not establish consultation acceptance. No test deletions.
PC-001: seed test-local historical order snapshots in the exact required states
with valid #90 prerequisites, never patching consultation during #92 setup or
execution. Check specific consultation errors, state/version/audit invariance,
and individually remove each seam guard in focused in-memory mutation validation.
Use a separate unpatched API class; legacy regression patches have cleanup.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Run component checks, local SQL parity and document partial criteria

Create a worktree-local venv and install src distributions only after missing
dependency detection. Run configured checks, procurement/API and tightly coupled
stock/finance/grant/hazard tests. Use existing installed SQL driver and a uniquely
named task-owned loopback SQL container; clean exactly that container and any
task-owned secret file. Record actual results, skips and unmet human criteria.
PC-002: expose a backend-selectable shared behavior mixin with JsonConsultation,
SqlConsultation and opt-in MssqlConsultation in the new core test module. MSSQL
uses existing test_mssqlstore.wipe/factory through a local import and a temporary
fictional seed; no shared harness edit. Execute the exact selector
`python -m unittest test_consultation_controls.MssqlConsultation -q` under
ZF_TEST_MSSQL=1 and local task-owned ZF_SQL_* settings. Include record reload,
competing expected versions, source-rowversion/procurement conflicts, and rollback.
Update core/API READMEs and existing KB synthesis/index/log. No legal snapshots.
Independent Review occurs once after plan/details/changes/validation reconciliation.

## Completion and Review Handoff

P01/P01-T01/P02/P02-T01/P02-T02 complete. Actual implementation follows the
record-only boundary, using legacy test-local patches rather than shared
dataset or other-domain source edits. Core suite: 10 canonical methods; API:
3 canonical methods. Configured Ruff/format/mypy pass. 321 targeted executions
include 47 explicit opt-in/browser skips; no failure remains. Actual local
SQL Server replay: 70 passes/no skips, including new core methods, three
unpatched HTTP methods and existing provider/stock/finance integration.
Migration tests: 25 passes after restoring missing python-pptx/Pillow/PyYAML
in the local venv. Five individual guard-removal mutants killed in memory.
No real Legal approval, let/renew acceptance or browser/UI conformance claim.

## Authorized Integration Evidence (2026-10-17)

Original P01/P02 execution and one independent Review are not repeated.
Coordinator-authorized rebase from original PR head 5411f0d4 onto main
1a05dfb8 incorporates merged hazard #388. Only manual conflict was append-only
KB log; upstream exact prefix and all own entries/routes retained.
All own src added/removed bytes match across bases; upstream hazard/workflow/
Store/SQL recovery hooks remain byte-unchanged.
Fresh combined JSON/SQLite/API/domain/manifest run: 348 executions, 300 passes,
48 explicit skips. Configured full core/API lint/format/types pass (114/54
typed files). Six added documentation links/anchors verified.
No new MSSQL run for docs-only conflict; original 70 SQL passes are historical.
Exact Legal-record criterion remains partial without current verified authority;
exact let/renew criterion separately remains missing genuine workflow engineering.
Bounded proposed coordinator follow-up is in changes and plan, not active work.
Coordinator independent final-head review remains pending.
