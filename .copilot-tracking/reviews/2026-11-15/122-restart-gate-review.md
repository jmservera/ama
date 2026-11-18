<!-- markdownlint-disable-file -->
# Review: Issue #122 Continuity Restart Authority, Suspension Fallback, and SQL Fence Gates

## Scope and Evidence

* Task ID: issue-122-restart-gate-0228-c2 (remediating parent task `issue-122-restart-gate-0228`)
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03` of Cycle 2 over `P01`–`P04` of Cycle 1)
* Assessed boundary: Issue `#122` local RAI Incident and Restart acceptance criteria across `src/core` and `src/api` (`RULE-024` distinct human restart authority and `view_only` refusal, prose-safe `validate_corrective_evidence` and monotonic `proposal_seq` / `proposal_digest` + normalized `test_id` / `corrective_evidence` anti-replay, versioned `meta('continuity')` SQL envelope + corrupt-meta fail-closed manual recovery, `continuity_gate_state` and `continuity_open_holds` SQLite and T-SQL triggers across `assistant_attempts` and `assistant_tasks`, manual case/accessible-challenge/statutory-hazard continuity during whole-release suspension, focused and regression tests, and component READMEs), plus distinct external follow-up items (`OD-35`/`OQ-017` human appointment and witnessed drills, immutable Azure ledger-head custody, and live `ZF_TEST_MSSQL=1` Azure SQL execution under `Refs #122`).
* Canonical review log: .copilot-tracking/reviews/logs/2026-11-15/issue-122-restart-gate-0228-c2-review.md
* Cycle 1 parent review log: .copilot-tracking/reviews/logs/2026-11-15/issue-122-restart-gate-0228-review.md
* Plan: .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c2-changes.md
* Research: .copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-research.md

## Opening Review State

* Interpreted review goal: Verify single-pass post-implementation conformance of the completed Issue `#122` local continuity restart-gate and SQL fence implementation across `src/core` and `src/api` following Cycle 2 closure of Cycle 1 findings `RV-001` through `RV-005` and Cycle 2 critique items `PC-001` through `PC-006`.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; all Cycle 1 and Cycle 2 research, plans, phase details, plan critiques, changes logs, source/test updates, and validation outputs are complete and reconciled.
* Acceptance basis: Cycle 2 `FR-01` through `FR-05`, `NFR-01`, `NFR-02`, `AC-01` through `AC-05`, critique dispositions `PC-001` through `PC-006`, and Issue `#122` local software acceptance criteria (`Refs #122`).
* First comparison boundary: Reconcile `continuity.py`, `restart_authority.py`, `sqlstore.py`, `mssqlstore.py`, `assistants.py`, `test_restart_gate_sql_fences.py`, `test_continuity_restart_gate.py`, `test_assistants.py`, `test_mssqlstore.py`, and `src/{core,api}/README.md` against all Cycle 1 + Cycle 2 requirements.
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/` records while parent RPI Agent persists state transitions; repository code, tests, docs, plans, details, critiques, research, and changes logs remain read-only.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed read-only post-implementation review on 2026-11-15 across all modified and added files in `src/core` and `src/api` and the full RPI tracking set under `.copilot-tracking/**/2026-11-15/`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Core Continuity Anti-Replay, SQL Envelope, and Corrupt-Meta Recovery (`RV-001`, `RV-003`, `RV-004`) | Reconciled | `dump_sql`, `unwrap_sql`, fail-closed `load(raw)`, portable `meta('continuity')` seeding/wrapping in `sync_sql_gate(read_meta=True)`, synchronized `SqlStore._proc_loaded` on fast-path `save()`, and independent `test_id` / `corrective_evidence` anti-replay in `_check_claim_replay` are implemented and verified. |
| `P02` (`P02-T01`) | SQL Trigger Hardening on `assistant_attempts` and `assistant_tasks` (`RV-002`, `RV-003`) | Reconciled | Active-`sending` open-hold update triggers on `assistant_attempts`, `review_gate_version` / `reviewed_revision` columns + ledger-safe MSSQL `_add_column`, SQLite and T-SQL `assistant_tasks` gate/hold triggers, `test_mssqlstore.py:wipe()` trigger drops, and `README.md` updates are complete. |
| `P03` (`P03-T01`, `P03-T02`, `P03-T03`) | Focused SQL/API Verification Expansion and Full Local Validation (`RV-005`) | Reconciled | `9` core tests + `9` API tests (`18 <= 25`) plus existing `src/core` and `src/api` regression suites, `tools/rename-zava-tests.py`, `ruff check`, `ruff format --check`, and strict `mypy` (`616` files) all pass; temporary `.venv-122-local` is removed. |
| `Follow-Up Items` | External `OD-35`/`OQ-017` witnessed drills, Azure ledger-head custody, and live `ZF_TEST_MSSQL=1` Azure SQL drill | Reconciled | Properly retained outside active local `Pxx` claims under `Refs #122`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | src/core/src/zava_forward/core/continuity.py, src/core/src/zava_forward/core/restart_authority.py | Enforced `validate_corrective_evidence`, `_refuse_view_only`, monotonic `proposal_seq`, `_check_digest_replay`, independent `_raw_tid` / `_raw_ev` `_check_claim_replay`, approver `actor` snapshots, `dump_sql`/`unwrap_sql`/`load` fail-closed parsing, and `sync_sql_gate`. | Verified across core and HTTP negative/positive drills. | Passed (`test_restart_gate_sql_fences.py`, `test_operator_suspension*.py`, `ruff`, `mypy`) | Reconciled |
| `P01-T02` | src/core/src/zava_forward/core/sqlstore.py, src/core/src/zava_forward/core/mssqlstore.py | Added `continuity_gate_state` and `continuity_open_holds` DDL and triggers, `dump_sql`/`unwrap_sql`/`load` integration across `_seed`, `merge_seed`, `_proc_sync`, `_discard`, `_proc_write`, and post-`COMMIT` fast-path `save()` `self._proc_loaded` tracking. | Verified across corrupt `meta('continuity')` reopen, sequential saves, rollbacks, and SQL portability checks. | Passed (`test_restart_gate_sql_fences.py`, `test_seed_merge.py`, `test_mssqlstore.py`, `ruff`, `mypy`) | Reconciled |
| `P02-T01` | src/core/src/zava_forward/core/assistants.py, src/api/tests/test_assistants.py, src/api/tests/test_mssqlstore.py, src/core/README.md, src/api/README.md | Added `assistant_attempts` and `assistant_tasks` gate columns, ledger-safe MSSQL `_add_column`, SQLite and T-SQL gate/open-hold triggers, `gate_hold` checks in `suspended`/`export`/`_view`, `Assistants.review()` gate stamping (`reject` unfenced), MSSQL fixture teardown updates, and honest non-operative README disclosures. | Verified across SQLite triggers, T-SQL DDL/collation/ledger checks, and mixed-version worker subprocesses. | Passed (`test_restart_gate_sql_fences.py`, `test_continuity_restart_gate.py`, `test_assistants.py`, `test_mssqlstore.py`, `ruff`, `mypy`) | Reconciled |
| `P03-T01`..`P03-T03` | src/core/tests/test_restart_gate_sql_fences.py, src/api/tests/test_continuity_restart_gate.py | Delivered 18 focused tests (`<= 25` budget) proving anti-replay, HTTP `TrustedProxyProvider` vs `PasswordProvider` enforcement, manual/accessible-challenge/statutory-hazard continuity under `all` suspension and corrupt continuity metadata, `threading.Barrier(2)` races, and commit-invariant git-free `gate-v0`/`pre-gate` subprocess exclusion; removed `.venv-122-local`. | All focused, regression, lint, format, and strict type checks passed. | Passed | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` (`FR-01`, `AC-01` in `continuity._check_claim_replay`) | Checked normalized `test_id` and `corrective_evidence` independently (`_raw_tid(prop) or _raw_ev(prop)`) unconditionally across concurrent open `"Suspended"` incidents and scoped to `current_candidate` across `"Keep suspended"` decisions and `"Restarted"` incidents. | Existing regression drill `src/api/tests/test_operator_suspension.py` promotes a new active release (`release_version="new"`, changing `candidate`) after restarting an incident and re-executes the standard regression suite `test_id="constructed-negative-and-fallback-drill"`. Scoping decided/restarted checks to `current_candidate` blocks tweaked-prose `test_id` replay on the active candidate (`RV-001`) while preserving candidate-upgrade regression runs (`20/20` passing). | Reconciled across `c2-plan.md`, `c2-phase-details.md`, `c2-changes.md`, `src/core/README.md`, and `src/api/README.md`. | Not needed (preserves `RULE-024` / `RV-001` intent and existing issue `#221` regression contract). | Justified and reconciled |
| `P03-T02` (`NFR-01` combined test count) | Consolidated API assertions into `9` methods (`9 + 9 = 18 <= 25` combined ceiling) with zero test removals. | Preserves strict test budget while covering every planned scenario. | Reconciled in `c2-plan.md` and `c2-changes.md`. | Not needed. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: Cycle 1 (`PC-001` through `PC-007`) and Cycle 2 (`PC-001` through `PC-006`) planner-direct critique findings were all applied and verified in code and tests, including commit-invariant git-free pre-gate worker subprocess isolation (`PC-001`), portable `meta('continuity')` envelope seeding/upgrade (`PC-002`), fast-path `self._proc_loaded` synchronization (`PC-003`), cross-suspension rejected-claim checks (`PC-004`), 4-step MSSQL updatable-ledger `_add_column` DDL (`PC-005`), and `[tool.ruff.format].exclude` compliance (`PC-006`).
* Material revisions: None required user escalation.
* Dependent-work pause assessment: Compliant.
* Justification assessment: All implementation-time refinements are evidence-backed, preserve `RULE-024` fail-closed guarantees, and are synchronized across tracking and component docs.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Owner-witnessed operational continuity/restart drill and `OD-35` / `OQ-017` / `RULE-020` human restart authority appointment | Requires live Zava North Homes governance delegation and human witness participation outside software code (`actual_hold=True` preserved). | Owner: Programme Sponsor / Building Safety | Open distinct follow-up (`Refs #122`); excluded from active `Pxx` claims. |
| Immutable external Azure ledger-head storage and live multi-replica Azure SQL (`ZF_TEST_MSSQL=1`) continuity/restart drill | Requires live Azure custody approvals and hosted SQL Server runtime outside local worktree tests. | Owner: Platform / Data Governance | Open distinct follow-up (`Refs #122`); excluded from active `Pxx` claims. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No open defects, decision gaps, or evidence gaps remain within the local `src/core` and `src/api` boundary.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None (active local scope) | none | Ready for local commit (`Refs #122`) and rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900` | All Cycle 1 (`RV-001`–`RV-005`) and Cycle 2 (`PC-001`–`PC-006`) items verified closed |

## Residual Work

* Owner-witnessed operational continuity/restart drill and `OD-35` / `OQ-017` / `RULE-020` human restart authority appointment (Owner: Programme Sponsor / Building Safety; tracked under `Refs #122`).
* Immutable external Azure ledger-head storage and live multi-replica Azure SQL (`ZF_TEST_MSSQL=1`) continuity/restart drill (Owner: Platform / Data Governance; tracked under `Refs #122`).

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none in local code/test scope.

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `(cd src/core && python3 -m unittest discover -s tests -p "test_restart_gate_sql_fences.py" -q)` | `src/core` (`P03-T01`) | Passed | 9/9 tests passed |
| `(cd src/core && python3 -m unittest discover -s tests -p "test_seed_merge.py" -q)` | `src/core` regression | Passed | 21/21 tests passed |
| `(cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_continuity_restart_gate.py" -q)` | `src/api` (`P03-T02`) | Passed | 9/9 tests passed (`18 <= 25` combined ceiling) |
| `(cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_assistants.py" -q)` | `src/api` assistants & dialect regression | Passed | 138 tests run, 0 failures (`skipped=60`) |
| `(cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_mssqlstore.py" -q)` | `src/api` SQL portability & MSSQL DDL regression | Passed | 244 tests run, 0 failures (`skipped=235` without `ZF_TEST_MSSQL=1`) |
| `(cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_operator_suspension*.py" -q)` | `src/api` operator suspension regression | Passed | 20/20 tests passed |
| `(cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_continuity_epoch_export.py" -q)` | `src/api` continuity epoch/export regression | Passed | 77 tests run, 0 failures (`skipped=39`) |
| `python3 tools/rename-zava-tests.py` | Repository migration guard | Passed | 25/25 tests passed |
| `ruff check .` and `ruff format --check .` in `src/core` and `src/api` | Lint & format gate (`NFR-02`) | Passed | 0 lint issues; `282` + `197` files formatted; `[tool.ruff.format].exclude` honored |
| `mypy .` in `src/core` and `src/api` | Strict type gate (`NFR-02`) | Passed | 0 issues across `335` + `281` = `616` source files |
| Live `ZF_TEST_MSSQL=1` disposable SQL Server execution | Hosted/container SQL Server | Unavailable | No live SQL Server instance in local worktree; offline T-SQL DDL, collation, `SharedSqlIsPortableTests`, and ledger `_add_column` recorder checks passed |

## Outcome

* Outcome: Conformant with justified divergence
* Outcome rationale: Local `src/core` and `src/api` continuity restart-authority controls, anti-replay checks, corrupt-metadata manual recovery, and SQLite/T-SQL `continuity-gate-v1` fences across `assistant_attempts` and `assistant_tasks` satisfy all planned requirements (`P01` through `P03`) and pass all targeted, regression, lint, format, and strict type gates, with one reconciled candidate-scoping refinement preserving `test_operator_suspension.py` candidate-upgrade drills and honest `Refs #122` tracking for external governance and live Azure drills.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | Distinct external follow-up items (`Refs #122`) | Programme Sponsor / Building Safety (`OD-35`/`OQ-017` witnessed drill) and Platform / Data Governance (immutable Azure ledger-head custody and live Azure SQL drill) |

* Execution status: Complete
* Outcome: Conformant with justified divergence
* Validation coverage: Focused and regression `src/core` and `src/api` unit suites, `tools/rename-zava-tests.py`, `ruff check`, `ruff format --check`, and strict `mypy` passed; temporary `.venv-122-local` removed; live `ZF_TEST_MSSQL=1` unavailable locally
* Blockers: none
