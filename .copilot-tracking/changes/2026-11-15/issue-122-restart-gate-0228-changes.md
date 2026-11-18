<!-- markdownlint-disable-file -->
# RPI Changes: Issue #122 Local RAI Incident, Restart Gate, Suspension Fallback, and SQL Old-Image Exclusion

## Metadata

* Task ID: issue-122-restart-gate-0228
* Related plan: .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Completed
* Declared invocation scope: Full plan (`P01`, `P02`, `P03`, `P04`)
* Completed scope markers: `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`, `P02-T02`), `P03` (`P03-T01`, `P03-T02`), `P04` (`P04-T01`, `P04-T02`)
* All remaining active-plan markers: `none`
* Status basis: Full plan (`P01`–`P04`) implemented, documented, and validated across `src/core` and `src/api` unit suites, `tools/rename-zava-tests.py`, `ruff check`, `ruff format --check`, and strict `mypy`.

## Execution Summary

Delivered all four phases (`P01`–`P04`) for Issue #122's three local RAI Incident and Restart acceptance criteria in `src/core` and `src/api`: substantive non-placeholder corrective-evidence validation and anti-replay (`proposal_seq`, digest replay, Keep-suspended rejected-claim replay, candidate-consumed claim replay, `view_only` refusal, and approver `actor` provenance); normalized SQL `continuity_gate_state` (`continuity-gate-v1`) and `continuity_open_holds` tables and triggers across SQLite and T-SQL so pre-gate or gate-mismatched worker images fail closed across `queued`, `leased`, `ready`, and `export` surfaces; HTTP and unit verification that manual case work, accessible challenge/correction, and independent statutory hazard response remain available during `all` suspension and gate mismatch; and component documentation updates in `src/core/README.md` and `src/api/README.md`.

## Completed Work

### Restart Gate Corrective Evidence, Anti-Replay, and Identity Controls (`P01`)

* `P01-T01`: Added prose-safe `_EVIDENCE_PLACEHOLDER_PATTERNS` and `validate_corrective_evidence` (`min_len=4` default, `min_len=3` for `test_id`) in `src/core/src/zava_forward/core/restart_authority.py`, rejecting blank, oversized, chat-memory, and placeholder/unavailable/self-approved/automatic-restart values without echoing raw inputs.
* `P01-T02`: Updated `src/core/src/zava_forward/core/continuity.py` to refuse `view_only` principals in `suspend`, `restart_propose`, and `restart_decide`; enforce `validate_corrective_evidence`; bind monotonic `proposal_seq` into proposal digests; reject replayed `proposal_digest` values (`_check_digest_replay`) and replayed `(test_id, corrective_evidence)` claims rejected by `"Keep suspended"` or already consumed/open against the same candidate release (`_check_claim_replay`); record full `actor` snapshots on decision records; and expose `GATE_VERSION`, `gate_mismatch_hold`, `gate_hold`, `gate_sync_rows`, and `sync_sql_gate` helpers for `P02`.

### SQL Continuity Gate Protocol and Old-Image Exclusion Triggers (`P02`)

* `P02-T01`: Added `continuity_gate_state` and `continuity_open_holds` DDL plus `continuity_gate_no_delete` and `continuity_gate_monotonic` triggers to `sqlstore.py` (`SCHEMA`) and `mssqlstore.py` (`TABLES`, `GATE_TRIGGERS` with `COLLATE Latin1_General_100_BIN2`); wired `continuity.sync_sql_gate` into `_migrate`, `_seed`, `merge_seed`, and `_proc_write`; checked `continuity.gate_hold` in `SqlStore.continuity_suspension`; and updated MSSQL test teardown and dialect table checks in `src/api/tests/test_mssqlstore.py` and `src/api/tests/test_assistants.py`.
* `P02-T02`: Added `continuity_gate_state`, `continuity_open_holds`, and `assistant_attempts` columns (`capability`, `gate_version`, `send_gate_version`) plus NULL-safe SQLite (`SQLITE_ATTEMPT_TRIGGERS`) and T-SQL (`MSSQL_ATTEMPT_TRIGGERS`) insert/update gate and open-hold triggers in `src/core/src/zava_forward/core/assistants.py`; updated `migrate`, `_upgrade`, `suspended`, `export`, `_view`, `claim`, `_reserve`, `begin_call`, and `_fence_in` to stamp and enforce `continuity.GATE_VERSION`.

### Core, HTTP, Suspension-Fallback, Concurrency, and Old-Image Restart Tests (`P03`)

* `P03-T01`: Added `src/core/tests/test_restart_gate_sql_fences.py` (8 semantic tests) covering substantive corrective-evidence validation, anti-replay (`proposal_seq`, digest replay, Keep-suspended claim replay, candidate-consumed claim replay, `view_only` refusal, OID/email self-approval), manual/accessible-challenge/priority-correction/hazard independence during `all` suspension and `gate_version` mismatch, SQLite trigger rejection of pre-gate/epoch-regressed/open-hold `assistant_attempts` writes, and T-SQL DDL/trigger collation parity.
* `P03-T02`: Added `src/api/tests/test_continuity_restart_gate.py` (9 semantic tests, 17 combined across both new modules <= 25 budget) covering HTTP `TrustedProxyProvider` and `PasswordProvider` restart gate authorization and OID-alias self-approval refusal, HTTP manual case work + accessible challenge + statutory hazard independence while `all` AI work is suspended and `gate_version` mismatches, independent SQL connection visibility, barrier-synchronized races (`suspend` vs `review`, `suspend` vs `claim`/`fence_send`/`complete_result`, concurrent `restart_decide`), and `subprocess` old-image worker exclusion across `queued`, `leased` (including `permitted`-marker `blocked-reclaim`), and `ready` proposals.

### Component Documentation and Validation Gate (`P04`)

* `P04-T01`: Updated `src/core/README.md` and `src/api/README.md` to document SQL `continuity-gate-v1` state/open-hold tables and `assistant_attempts` triggers, substantive corrective-evidence and anti-replay enforcement, `view_only` refusal, and suspension-time manual/accessible-challenge/hazard availability while preserving explicit non-operative disclosures for OD-35/OQ-017 human appointment, witnessed drills, WCAG/resident accessibility acceptance, and external ledger-head custody.
* `P04-T02`: Executed `ruff check`, `ruff format --check`, and strict `mypy` in both `src/core` and `src/api`, focused and regression suites in `src/core` and `src/api`, `tools/rename-zava-tests.py`, cleaned up temporary `.venv-122-local`, and reconciled all RPI tracking artifacts.

## Implementation-Time Plan and Detail Updates

* Local judgment / immediately relevant current-state alignment in `P02-T02` (`src/core/src/zava_forward/core/assistants.py`): During `P03` old-image verification, discovered that `Assistants.export` and `Assistants._view` (used by `detail` and `review`) checked `continuity.active(...)` directly without checking `continuity.gate_hold(db, mssql=self.mssql)`. Updated both to check `continuity.gate_hold(db, mssql=self.mssql) or continuity.active(...)` so `detail`, `review`, and `export` fail closed (`actionable=False`, `relied_on=False`, `suspension="gate-mismatch"`) whenever `continuity_gate_state.gate_version` mismatches.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `test_restart_gate_sql_fences.py` | `src/core` (`P03-T01`) | Passed | 8/8 tests passed |
| `test_continuity_restart_gate.py` | `src/api` (`P03-T02`) | Passed | 9/9 tests passed |
| Continuity / SQL / assistant / restart / seed regression suites | `src/api` (`test_continuity`, `test_continuity_epoch_export`, `test_epic149_manual_fallback_continuity`, `test_operator_suspension`, `test_rai_restart_sql_reconstruction`, `test_assistant_restart_non_replenishment`, `test_assistants`, `test_assistant_release`, `test_assistants_dispatch`, `test_assistant_reserve_guard`, `test_mssqlstore`, `test_seed_merge`) | Passed | 612 tests passed (`605` + `7`), 0 failures |
| Full `src/core` unit discovery | `src/core` (`tests/`) | Passed (except optional SDK extra) | 3,437 passed across all changed/related modules; only `test_device_registry_azure` failed when optional `azure-iot-hub` extra was absent in isolated temp venv |
| `python3 tools/rename-zava-tests.py` | Repository migration guard | Passed | 25/25 tests passed |
| `ruff check` & `ruff format --check` | `src/core` (282 formatted files) & `src/api` (197 formatted files) | Passed | All checks passed; ADR 0006 format-exclude lists respected |
| `mypy` (strict) | `src/core` (335 source files) & `src/api` (281 source files) | Passed | 0 issues in 335 + 281 files |

## Pre-Review Reconciliation

* Plan markers and phase details: Synchronized (`P01`, `P02`, `P03`, `P04` and all `P01-T01`..`P04-T02` checked)
* Completed-work evidence and handoff prose: Synchronized
* Validation, blockers, remaining work, and follow-up items: Synchronized; `.venv-122-local` removed
* Review readiness: Ready for single-pass `rpi-review`

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-plan.md, `## Follow-Up Items`
* Execute an owner-witnessed continuity/restart drill and record appointed human restart authority (`OQ-017` / `OD-35` / `RULE-020`) once Zava North Homes governance sign-off exists (Owner: Programme Sponsor / Building Safety).
* Configure immutable external Azure ledger-head storage and execute an owned Azure SQL continuity/restart drill once Azure resource provisioning and custody approvals exist (Owner: Platform / Data Governance).

## Return-to-Caller State

* Implementation execution status: Completed
* Declared scope and markers: Full plan; completed: `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`, `P02-T02`), `P03` (`P03-T01`, `P03-T02`), `P04` (`P04-T01`, `P04-T02`); remaining: `none`
* Validation coverage: Complete across `src/core` and `src/api` unit/regression suites, `tools/rename-zava-tests.py`, `ruff check`, `ruff format --check`, and strict `mypy`
* Blockers: none
* Current plan and detail updates: Local `P02-T02` fail-closed alignment in `Assistants.export` and `Assistants._view` recorded above
* Planning and critique state: Ready (`PC-001`–`PC-007` applied; no repeat critique)
* Follow-up items: 2 external governance/Azure follow-up items tracked in plan
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
