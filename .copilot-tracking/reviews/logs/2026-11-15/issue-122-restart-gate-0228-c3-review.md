<!-- markdownlint-disable-file -->
# Review: Issue #122 SQL Server Ledger Trigger Guard and Base Merge (Cycle 3)

## Scope and Evidence

* Task ID: issue-122-restart-gate-0228-c3
* Parent Task ID: issue-122-restart-gate-0228-c2
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`)
* Assessed boundary: Cycle 3 remediation of `PR #1787` CI failure (job `132785382777`) on SQL Server `WITH LEDGER = ON` databases across `src/core/src/zava_forward/core/mssqlstore.py`, `src/core/src/zava_forward/core/assistants.py`, `src/core/README.md`, and `src/api/tests/test_assistants.py`, plus non-rewriting base-branch synchronization with `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) preserving `PR #1781` (`#117`) `is_available_case_document` in `assistants.py:capture()` (`FR-01` through `FR-04`, `NFR-01`, `NFR-02`, `AC-01` through `AC-04`, and critique dispositions `PC-001` through `PC-003`).
* Plan: .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c3-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c3-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c3-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-c3-research.md (`C1` through `C10`); git merge commit `81229546ed26d6b048e1746c96f12f116cd925ce`; working-tree diff across `src/core` and `src/api`.

## Opening Review State

* Interpreted review goal: Execute a single-pass, evidence-based, read-only post-implementation review of Cycle 3 (`issue-122-restart-gate-0228-c3`) across `P01` and `P02`, confirming closure of the SQL Server `WITH LEDGER = ON` DML trigger failure, preservation of `PR #1781` `is_available_case_document`, fidelity to plan critique dispositions `PC-001` through `PC-003`, and clean separation of external follow-up items under `Refs #122`.
* Review scope: Full task (`P01`, `P02`)
* Evidence readiness: Ready; all `P01` and `P02` checklist markers (`P01-T01` through `P02-T02`), phase details, single-pass plan critique (`PC-001` through `PC-003`), changes record (`Completed`), and local unit/type/lint validations are complete and reconciled.
* Acceptance basis: `FR-01` through `FR-04`, `NFR-01`, `NFR-02`, `AC-01` through `AC-04`, and `PC-001` through `PC-003`.
* First comparison boundary: Compare `P01` and `P02` plan/detail specifications and critique dispositions against the git merge commit and working-tree diff across `mssqlstore.py`, `assistants.py`, `src/core/README.md`, and `src/api/tests/test_assistants.py`.
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/logs/2026-11-15/issue-122-restart-gate-0228-c3-review.md` while the parent RPI Agent persists session state transitions and performs the final requested git commit freeze.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass read-only post-implementation review on 2026-11-15 across `P01` (`P01-T01` through `P01-T04`) and `P02` (`P02-T01`, `P02-T02`), inspecting merge commit `81229546ed26d6b048e1746c96f12f116cd925ce`, working-tree diffs in `src/core` and `src/api`, reconciled Cycle 3 RPI artifacts, and full local validation output.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`–`P01-T04`) | Base-Branch Synchronization and SQL Server Ledger Trigger Guards | Reconciled | Merged `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) cleanly without rewriting `d0d4135d3`, preserved `is_available_case_document` in `assistants.py:capture()`, moved `GATE_TRIGGERS` inside `else:` in `MssqlStore._create_schema_serialized`, initialized `ledger = False` and guarded trigger execution with `if not (self.mssql and ledger):` in `Assistants.migrate` while leaving `continuity.sync_sql_gate` unconditional, and updated `src/core/README.md`. |
| `P02` (`P02-T01`, `P02-T02`) | Ledger Dialect Unit Test, Validation, and Local Commit Freeze | Reconciled | Extended `DialectConnection` with `ledger=False` and exact `PC-001` guard ordering, verified non-ledger `CREATE TRIGGER` emission in `test_mssql_sql_shapes_enqueue_claim_complete_review_scan`, added `test_mssql_ledger_mode_skips_triggers_and_syncs_continuity_gate` covering both `MssqlStore._create_schema_serialized` and `Assistants.migrate`, and passed all focused unit, `mypy`, `ruff`, and migration checks. |
| `Follow-Up Items` | External `OD-35`/`OQ-017` witnessed drills, Azure ledger-head custody, and hosted CI / live SQL Server 2022 ledger run after push | Reconciled | Remain outside active `Pxx` scope under `Refs #122` and caller's no-push freeze instruction. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | Git merge `81229546ed`, src/core/src/zava_forward/core/assistants.py | Merged `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) using privacy-safe GitHub noreply email and Copilot trailer, preserving `is_available_case_document(d)` in `capture()` and keeping `d0d4135d3` in ancestry. | Satisfies `FR-01` and `AC-01`. | Passed (`test_document_controls.py`, `test_assistants.py`) | Reconciled |
| `P01-T02` | src/core/src/zava_forward/core/mssqlstore.py | Moved `for trigger in GATE_TRIGGERS: self.db.execute(trigger)` inside `else:` of `if ledger:` in `_create_schema_serialized`. | Satisfies `FR-02` and `AC-02`. | Passed (`DialectTests`, `test_mssqlstore.py`, `mypy`, `ruff`) | Reconciled |
| `P01-T03` | src/core/src/zava_forward/core/assistants.py | Initialized `ledger = False` and wrapped `MSSQL_ATTEMPT_TRIGGERS` / `SQLITE_ATTEMPT_TRIGGERS` loop in `if not (self.mssql and ledger):` while running `continuity.sync_sql_gate` unconditionally. | Satisfies `FR-03` and `AC-02`. | Passed (`DialectTests`, `test_restart_gate_sql_fences.py`, `mypy`, `ruff`) | Reconciled |
| `P01-T04` | src/core/README.md | Documented the SQLite / non-ledger SQL Server DML trigger boundary versus SQL Server `WITH LEDGER = ON` updatable ledger tables. | Satisfies `FR-04` documentation sync without `.copilot-tracking/` leaks. | Passed (diff review) | Reconciled |
| `P02-T01` | src/api/tests/test_assistants.py | Extended `DialectConnection` (`ledger=False`) and added `DialectTests.test_mssql_ledger_mode_skips_triggers_and_syncs_continuity_gate` plus non-ledger trigger assertion. | Satisfies `FR-04`, `NFR-01`, `AC-03`, `PC-001`, and `PC-002`. | Passed (`DialectTests` `2/2`, `mypy`, `ruff`) | Reconciled |
| `P02-T02` | .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c3-plan.md, .copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c3-changes.md | Executed full focused validation matrix and reconciled plan/changes artifacts. | Satisfies `NFR-02`, `AC-04`, and `PC-003`. | Passed (`0` errors across all suites) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P02-T02` (worktree `PYTHONPATH` invocation) | Supplied explicit worktree `PYTHONPATH` (`PYTHONPATH=src/core/src` for `src/core/tests` and `PYTHONPATH=../core/src:../agents/src` for `src/api` `mypy`) because packages are not editable-installed into global `/usr/lib/python3.12` in this worktree. | `.github/copilot-instructions.md` and `.github/workflows/src-ci.yml` command conventions. | Recorded in `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c3-changes.md`. | Not needed (ordinary local execution detail; zero behavioral or scope divergence). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All three planner-owned findings in `.copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c3-plan-critique.md` (`PC-001` `DialectConnection` branch ordering ahead of `"FROM sys.tables"` and `"N'TR'"`; `PC-002` exact `DialectTests` method/helper/lock/`dbpath`/`assistant_connection`/`svc.sql`/dialect `suspended` interfaces; `PC-003` `src/api/tests/test_document_controls.py` module path) were applied before implementation and verified in code.
* Material revisions: None.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Observe hosted `Source projects CI` (`MssqlLedgerMigration` and `MssqlLedgerTests` against live SQL Server 2022) after push | Caller explicitly forbade `git push` in this session (`Do not push directly`), and no local `ZF_TEST_MSSQL=1` SQL Server container is running in the worktree. | Owner / Orchestrator: push frozen branch and read exact-head hosted CI. | Open distinct follow-up; properly excluded from local freeze scope. |
| Owner-witnessed operational continuity/restart drill, `OD-35`/`OQ-017` human restart authority appointment, and immutable external Azure ledger-head drill | Non-code organizational and cloud-custody criteria of Issue `#122`. | Owner: Programme Sponsor / Building Safety / Platform. | Open distinct follow-up (`Refs #122`); properly excluded from active `Pxx` claims. |

## Findings

No material defects, decision gaps, or evidence gaps were found within the Cycle 3 task boundary (`0` Critical, `0` High, `0` Medium, `0` Low).

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None (active local scope) | none | Ready for local commit freeze and owner/orchestrator push to `PR #1787` | All Cycle 3 requirements (`FR-01`–`FR-04`, `AC-01`–`AC-04`) are satisfied and verified |

## Residual Work

* Push `feat/platform-122-restart-gate-0228` to `origin` and confirm hosted `Source projects CI` passes live SQL Server 2022 `MssqlLedgerMigration` (`5` tests) and `MssqlLedgerTests` (`2` tests) on `PR #1787`.
* Complete external non-code criteria of Issue `#122` (`OD-35`/`OQ-017` human restart authority appointment, witnessed drill, and external Azure ledger-head drill; `Refs #122`).

## Blockers and Remaining Work

* Blockers: none
* Remaining active task work: Commit tracked changes and Cycle 3 `.copilot-tracking/` artifacts locally with `Refs #122` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leaving `git status --short` empty without pushing.

## Outcome

* Execution status: Complete
* Outcome: Conformant
* Summary: Cycle 3 cleanly merges `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) preserving `PR #1781` `is_available_case_document` in `assistants.py:capture()`, guards DML trigger creation on SQL Server `WITH LEDGER = ON` databases in `MssqlStore._create_schema_serialized` and `Assistants.migrate` while preserving `continuity.sync_sql_gate` and SQLite/non-ledger SQL Server triggers, adds deterministic local `DialectTests` ledger verification, and passes all focused unit, `mypy`, `ruff`, and migration checks.
