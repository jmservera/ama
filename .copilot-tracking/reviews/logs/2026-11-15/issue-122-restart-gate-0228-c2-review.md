<!-- markdownlint-disable-file -->
# Review: Issue #122 RAI Incident and Restart Gate Remediation (Cycle 2)

## Scope and Evidence

* Task ID: issue-122-restart-gate-0228-c2
* Parent Task ID: issue-122-restart-gate-0228
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Cycle 2 surgical remediation of Cycle 1 review findings `RV-001` through `RV-005` across `src/core` and `src/api` (`FR-01` through `FR-05`, `NFR-01`, `NFR-02`, `AC-01` through `AC-05`), single-pass plan critique dispositions `PC-001` through `PC-006`, reconciled implementation-time updates, focused and regression validation suites, and distinct external follow-up items (`OD-35`/`OQ-017` human restart authority appointment and witnessed drills, immutable external Azure ledger-head custody, and live `ZF_TEST_MSSQL=1` Azure SQL execution under `Refs #122`).
* Plan: .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c2-changes.md
* Other evidence considered: .copilot-tracking/reviews/logs/2026-11-15/issue-122-restart-gate-0228-review.md (`RV-001` through `RV-005`); .copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-research.md (`C1` through `C18`); working-tree changes across `src/core` and `src/api`.

## Opening Review State

* Interpreted review goal: Conduct one evidence-based, read-only post-implementation review of Cycle 2 (`issue-122-restart-gate-0228-c2`) across `P01` through `P03`, verifying closure of Cycle 1 findings `RV-001` through `RV-005` and Cycle 2 critique dispositions `PC-001` through `PC-006`, keeping execution status separate from outcome verdict, and preserving external governance/cloud items outside active `Pxx` scope.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; plan checklist markers (`P01` through `P03` and `P01-T01` through `P03-T03`), phase details, single-pass plan critique (`PC-001` through `PC-006`), changes record (`Completed`), parent review (`RV-001` through `RV-005`), and local validation results are complete and reconciled.
* Acceptance basis: Cycle 2 `FR-01` through `FR-05`, `NFR-01`, `NFR-02`, `AC-01` through `AC-05`, critique dispositions `PC-001` through `PC-006`, and Issue `#122` local RAI Incident and Restart software criteria (`Refs #122`).
* First comparison boundary: Compare `P01` through `P03` plan/detail specifications, implementation-time candidate-scoping reconciliation, and critique dispositions `PC-001` through `PC-006` against `src/core` and `src/api` source, test, and README changes.
* Active read-only boundaries: Review writes only canonical review records under `.copilot-tracking/reviews/` while parent RPI Agent manages session state transitions; all source, test, documentation, plan, detail, critique, research, and changes files remain read-only.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass read-only post-implementation review on 2026-11-15 across the full Cycle 2 task boundary (`P01` through `P03`, `P01-T01` through `P03-T03`), auditing `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md`, `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c2-changes.md`, `.copilot-tracking/reviews/logs/2026-11-15/issue-122-restart-gate-0228-review.md`, and the exact working-tree diff and test suites in `src/core` and `src/api`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Core Continuity Anti-Replay, SQL Envelope, and Corrupt-Meta Recovery (`RV-001`, `RV-003`, `RV-004`) | Reconciled | `continuity.dump_sql`, `continuity.unwrap_sql`, fail-closed `continuity.load`, portable `meta('continuity')` seeding/wrapping in `sync_sql_gate(read_meta=True)`, synchronized `SqlStore._proc_loaded` across `_proc_sync`/`_discard`/`_proc_write`/fast-path `save()`, and independent `test_id` / `corrective_evidence` anti-replay in `_check_claim_replay` match the reconciled plan and phase details. |
| `P02` (`P02-T01`) | SQL Trigger Hardening on `assistant_attempts` and `assistant_tasks` (`RV-002`, `RV-003`) | Reconciled | Removed `NEW.outcome <> OLD.outcome` (`i.outcome <> d.outcome`) from `assistant_attempts` open-hold update triggers, added `review_gate_version` (`COLLATE Latin1_General_100_BIN2` on MSSQL) and `reviewed_revision` with ledger-safe `Assistants._add_column`, enforced SQLite and T-SQL `assistant_tasks` gate/hold triggers, updated `test_mssqlstore.py:wipe()`, and documented the controls in `src/core/README.md` and `src/api/README.md`. |
| `P03` (`P03-T01`, `P03-T02`, `P03-T03`) | Focused SQL/API Verification Expansion and Full Local Validation (`RV-005`) | Reconciled | Delivered 18 combined test methods (`9` in `src/core/tests/test_restart_gate_sql_fences.py` + `9` in `src/api/tests/test_continuity_restart_gate.py`, within `<= 25`), covering tweaked-prose `test_id` replay, active-`sending` hold updates, `assistant_tasks` review triggers, corrupt `meta('continuity')` reopen and rollback, `PasswordProvider` `403` + denial audits, HTTP challenge lifecycle, `threading.Barrier(2)` races, commit-invariant git-free `gate-v0`/`pre-gate` subprocess workers at `epoch = 0`, MSSQL ledger `_add_column` DDL, clean `ruff` and strict `mypy`, and `.venv-122-local` cleanup. |
| `Follow-Up Items` | External `OD-35`/`OQ-017` witnessed drills, Azure ledger-head custody, and live `ZF_TEST_MSSQL=1` Azure SQL drill | Reconciled | Remain outside active `Pxx` implementation and acceptance claims under `Refs #122` with explicit owners. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | src/core/src/zava_forward/core/continuity.py | Added `dump_sql`, `unwrap_sql`, fail-closed `load(raw)` (`blank()` only when `raw is None`, `epoch = -1` on `""`/corrupt/mismatched `gate_version`), portable `meta('continuity')` initialization/upgrade in `sync_sql_gate(read_meta=True)`, and split `_raw_tid` / `_raw_ev` anti-replay in `_check_claim_replay`. | Resolves `RV-001`, `RV-003`, `RV-004`, `PC-002`, and `PC-004`. | Passed (`test_restart_gate_sql_fences.py`, `test_operator_suspension*.py`, `ruff`, `mypy`) | Reconciled |
| `P01-T02` | src/core/src/zava_forward/core/sqlstore.py | Maintained `self._proc_loaded` across `_proc_sync`, `_discard`, `_proc_write`, and post-`COMMIT` fast-path `save()`; persisted `continuity` with `dump_sql` in `_seed`, `merge_seed`, and `_proc_write`; unwrapped in `merge_seed`; and loaded via `continuity.load` on startup/rollback. | Resolves `RV-003`, `RV-004`, `PC-002`, and `PC-003` without corrupt-row crashes or spurious `ConflictError('continuity')`. | Passed (`test_restart_gate_sql_fences.py`, `test_seed_merge.py`, `test_mssqlstore.py`, `ruff`, `mypy`) | Reconciled |
| `P02-T01` | src/core/src/zava_forward/core/assistants.py, src/api/tests/test_mssqlstore.py, src/core/README.md, src/api/README.md | Hardened `assistant_attempts` open-hold update triggers; added `review_gate_version` and `reviewed_revision` columns, ledger-safe MSSQL `_add_column`, and SQLite/T-SQL `assistant_tasks` triggers; stamped gate columns in `Assistants.review()` for `verify`/`accept`/`edit-accept` while leaving `reject` unfenced; updated MSSQL trigger teardown and component READMEs. | Resolves `RV-002`, `RV-003`, and `PC-005` while preserving all existing sensor/epoch/suspension fixtures and non-operative `OD-35` disclosures. | Passed (`test_restart_gate_sql_fences.py`, `test_continuity_restart_gate.py`, `test_assistants.py`, `test_mssqlstore.py`, `ruff`, `mypy`) | Reconciled |
| `P03-T01` | src/core/tests/test_restart_gate_sql_fences.py | Added/expanded 9 strictly typed core tests for independent normalized `test_id` anti-replay, same-outcome `sending` hold-update aborts, `assistant_tasks` review trigger aborts, corrupt `meta('continuity')` reopen + sequential fast-path `save()` + `_discard()` rollback manual continuity, and explicit worktree `PYTHONPATH` on subprocesses. | Resolves core verification scope of `RV-001` through `RV-005`. | Passed (`9/9` tests, `ruff`, strict `mypy`) | Reconciled |
| `P03-T02` | src/api/tests/test_continuity_restart_gate.py | Expanded 9 strictly typed API tests covering `PasswordProvider` `restart-decide` `403` + denial audit, HTTP negative-path audit increments, HTTP `challenge_open`/`challenge_update`/`challenge_escalate`/`challenge_resolve` during `all` suspension, `threading.Barrier(2)` races (`claim`, `_fence_in`/`complete`, `verify`, `accept` vs `suspend`), commit-invariant git-free `gate-v0` and `pre-gate` subprocess workers at `epoch = 0`, and MSSQL ledger `_add_column` 4-step DDL emission. | Resolves API verification scope of `RV-003`, `RV-005`, `PC-001`, and `PC-005` within `18 <= 25` combined test methods. | Passed (`9/9` tests, `ruff`, strict `mypy`) | Reconciled |
| `P03-T03` | .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md, .copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c2-changes.md | Executed focused and regression unit suites, `tools/rename-zava-tests.py`, `ruff check`, `ruff format --check`, and strict `mypy`, removed `.venv-122-local`, and re-verified focused suites without `.venv*`. | Validation recorded in `c2-changes.md`; worktree free of temporary `.venv*` directories. | Passed | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` (`FR-01`, `AC-01` in `continuity._check_claim_replay`) | Normalized `test_id` (`_raw_tid`) and `corrective_evidence` (`_raw_ev`) are checked independently (`_raw_tid(prop) or _raw_ev(prop)`) unconditionally across concurrent open `"Suspended"` incidents and scoped to `current_candidate` across `"Keep suspended"` decisions and `"Restarted"` incidents, rather than blocking a standard regression `test_id` across newly promoted release candidates. | Existing regression drill `src/api/tests/test_operator_suspension.py` (`drill` -> `retained_snapshot`) promotes a new active release (`release_version="new"`, changing `candidate`) after a `"Restarted"` incident and re-runs `propose()` with the standard suite `test_id="constructed-negative-and-fallback-drill"`; preserving candidate-upgrade regression re-runs while blocking tweaked-prose `test_id` replay on the active candidate fulfills `RV-001` intent without breaking issue `#221` regressions. | Synchronized across `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md`, `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md`, `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c2-changes.md`, `src/core/README.md`, and `src/api/README.md`. | Not needed (justified local refinement preserving `RULE-024` / `RV-001` anti-replay intent and backward regression compatibility; single-pass critique preserved). | Justified and reconciled |
| `P03-T02` (`NFR-01` combined test count) | Delivered `9` core + `9` API = `18` test methods instead of `20` by consolidating new HTTP, barrier-race, pre-gate subprocess, and MSSQL ledger assertions inside the existing 9 API test methods. | Kept within the locked `<= 25` combined test method ceiling with zero test removals. | Synchronized in `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md` and `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c2-changes.md`. | Not needed. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All six planner-direct findings in `.copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan-critique.md` (`PC-001` commit-invariant git-free pre-gate worker subprocess shim; `PC-002` portable `meta('continuity')` `dump_sql` seeding/wrapping in `sync_sql_gate(read_meta=True)`, `_seed`, and `merge_seed`; `PC-003` post-`COMMIT` fast-path `self._proc_loaded` synchronization in `SqlStore.save()`; `PC-004` `current_candidate=None` default, self-exclusion, and cross-suspension rejected-decision checks in `_check_claim_replay`; `PC-005` 4-step MSSQL updatable-ledger `Assistants._add_column` DDL with `Latin1_General_100_BIN2` collation; `PC-006` accurate `src/core/pyproject.toml` and `src/api/pyproject.toml` `[tool.ruff.format].exclude` citations) are fully implemented and verified.
* Material revisions: None required user escalation or architectural re-planning.
* Dependent-work pause assessment: No improper early execution occurred; all critique dispositions were planner-direct.
* Justification assessment: The candidate-scoped `test_id` anti-replay refinement on decided/restarted incidents is grounded in existing `test_operator_suspension.py` candidate-promotion behavior, documented in component READMEs and RPI artifacts, and prevents tweaked-prose `test_id` replay on any unchanged candidate or concurrent open incident.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Owner-witnessed operational continuity/restart drill and `OD-35` / `OQ-017` / `RULE-020` human restart authority appointment | Requires live Zava North Homes governance appointment and human witness sign-off outside software code (`actual_hold=True` preserved). | Owner: Programme Sponsor / Building Safety | Open distinct follow-up (`Refs #122`); properly excluded from active `Pxx` claims. |
| Immutable external Azure ledger-head storage and live multi-replica Azure SQL (`ZF_TEST_MSSQL=1`) continuity/restart drill | Requires live Azure resource custody and hosted SQL Server runtime outside local worktree validation. | Owner: Platform / Data Governance | Open distinct follow-up (`Refs #122`); properly excluded from active `Pxx` claims. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No material implementation defects, decision gaps, or evidence gaps remain within the supplied local `src/core` and `src/api` task boundary (`RV-001` through `RV-005` from Cycle 1 and `PC-001` through `PC-006` from Cycle 2 plan critique are all resolved and verified).

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None (active local scope) | none | No further `rpi-implement`, `rpi-plan`, or `rpi-research` pass required for local `src/core` / `src/api` restart-gate scope | Cycle 1 findings `RV-001` through `RV-005` are closed and verified |

## Residual Work

* Owner-witnessed operational continuity/restart drill and `OD-35` / `OQ-017` / `RULE-020` human restart authority appointment (Owner: Programme Sponsor / Building Safety; tracked under `Refs #122`).
* Immutable external Azure ledger-head storage and live multi-replica Azure SQL (`ZF_TEST_MSSQL=1`) continuity/restart drill (Owner: Platform / Data Governance; tracked under `Refs #122`).

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none in `issue-122-restart-gate-0228-c2` (`P01` through `P03` complete and verified).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `(cd src/core && python3 -m unittest discover -s tests -p "test_restart_gate_sql_fences.py" -q)` | `src/core` (`P03-T01`) | Passed | 9/9 tests passed (both inside `.venv-122-local` and with system `python3` after venv cleanup) |
| `(cd src/core && python3 -m unittest discover -s tests -p "test_seed_merge.py" -q)` | `src/core` regression | Passed | 21/21 tests passed |
| `(cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_continuity_restart_gate.py" -q)` | `src/api` (`P03-T02`) | Passed | 9/9 tests passed (`18 <= 25` combined ceiling; verified both before and after `.venv-122-local` removal) |
| `(cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_assistants.py" -q)` | `src/api` dialect & assistants regression | Passed | 138 tests run, 0 failures (`skipped=60`) |
| `(cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_mssqlstore.py" -q)` | `src/api` SQL portability & MSSQL DDL regression | Passed | 244 tests run, 0 failures (`skipped=235` without `ZF_TEST_MSSQL=1`) |
| `(cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_operator_suspension*.py" -q)` | `src/api` operator suspension regression | Passed | 20/20 tests passed |
| `(cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_continuity_epoch_export.py" -q)` | `src/api` continuity epoch/export regression | Passed | 77 tests run, 0 failures (`skipped=39`) |
| `python3 tools/rename-zava-tests.py` | Repository migration guard | Passed | 25/25 tests passed |
| `ruff check .` and `ruff format --check .` in `src/core` and `src/api` | Lint & format gate (`NFR-02`) | Passed | 0 lint issues; `282` (`src/core`) + `197` (`src/api`) files formatted; `[tool.ruff.format].exclude` honored |
| `mypy .` in `src/core` and `src/api` | Strict type gate (`NFR-02`) | Passed | 0 issues across `335` (`src/core`) + `281` (`src/api`) = `616` source files |
| Live `ZF_TEST_MSSQL=1` disposable SQL Server execution | Hosted/container SQL Server | Unavailable | No live SQL Server instance in local worktree; offline T-SQL DDL, `Latin1_General_100_BIN2` collation, `SharedSqlIsPortableTests`, and 4-step ledger `_add_column` recorder checks passed |

## Outcome

* Outcome: Conformant with justified divergence
* Outcome rationale: Planned phases `P01` through `P03` (`P01-T01` through `P03-T03`) executed completely, closing all five Cycle 1 findings (`RV-001` through `RV-005`) and all six Cycle 2 plan critique findings (`PC-001` through `PC-006`) with clean `ruff`, strict `mypy` (`616` files), and passing focused and regression unit suites across `src/core` and `src/api`. One implementation-time refinement in `P01-T01` scopes decided/restarted `test_id` anti-replay to `current_candidate` (while keeping concurrent open-suspension `test_id` anti-replay unconditional) so tweaked-prose `test_id` replay on the active candidate fails closed without breaking candidate-promotion regression runs in `test_operator_suspension.py`; that refinement is documented and reconciled across plan, phase details, changes, and READMEs. External non-code Issue `#122` criteria (`OD-35`/`OQ-017` human appointment and witnessed drills, immutable Azure ledger-head custody, and live Azure SQL rollout drills) remain explicitly tracked as distinct follow-ups under `Refs #122`.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | Distinct external follow-up items (`Refs #122`) | Programme Sponsor / Building Safety (`OD-35`/`OQ-017` witnessed drill) and Platform / Data Governance (immutable Azure ledger-head custody and live multi-replica Azure SQL drill) |

* Execution status: Complete
* Outcome: Conformant with justified divergence
* Validation coverage: Focused and regression `src/core` and `src/api` unit suites, `tools/rename-zava-tests.py`, `ruff check`, `ruff format --check`, and strict `mypy` passed; temporary `.venv-122-local` removed; live `ZF_TEST_MSSQL=1` unavailable locally
* Blockers: none
