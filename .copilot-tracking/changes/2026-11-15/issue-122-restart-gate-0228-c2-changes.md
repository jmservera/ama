---
title: "Changes Log - Issue #122 RAI Incident and Restart Gate Remediation (Cycle 2)"
description: "Implementation evidence for Cycle 2 remediation of RV-001 through RV-005 across src/core and src/api"
author: "Copilot"
ms.date: "2026-11-15"
---

## Metadata

* Task ID: `issue-122-restart-gate-0228-c2`
* Parent Task ID: `issue-122-restart-gate-0228`
* Plan Path: `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md`
* Phase Details Path: `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md`
* Critique Path: `.copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan-critique.md`
* Declared Scope: Full plan (`P01` through `P03`)
* Execution Status: `Completed`

## Opening Implementation State

* Active checklist markers: `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`), `P03` (`P03-T01`, `P03-T02`, `P03-T03`) — all completed (`[x]`).
* First dependency-ready task: `P01-T01`.
* Blockers: `none`.

## Completed Phase and Task Evidence

| Marker | Files Changed | Summary of Changes | Validation |
| --- | --- | --- | --- |
| `P01-T01` | `src/core/src/zava_forward/core/continuity.py` | Added `dump_sql` (`{"gate_version": GATE_VERSION, "epoch": -1, "continuity": doc}`), `unwrap_sql`, fail-closed `load(raw)` (`blank()` only when `raw is None`; `epoch = -1` on `""`, malformed JSON, non-dict, or mismatched `gate_version`), portable `meta('continuity')` envelope initialization/upgrade inside `sync_sql_gate(read_meta=True)`, and split `test_id` / `corrective_evidence` anti-replay in `_check_claim_replay` (`RV-001`, `RV-003`, `RV-004`, `PC-002`, `PC-004`). | `test_restart_gate_sql_fences.py` (9/9), `test_operator_suspension*.py` (20/20), `ruff`, `mypy` |
| `P01-T02` | `src/core/src/zava_forward/core/sqlstore.py` | Initialized and maintained `self._proc_loaded` across `_proc_sync`, `_discard`, `_proc_write`, and post-`COMMIT` fast-path `save()`; serialized `continuity` via `continuity.dump_sql` in `_seed`, `merge_seed`, and `_proc_write`; unwrapped `continuity` via `continuity.unwrap_sql` in `merge_seed`; and loaded `continuity` via `continuity.load` in `_proc_sync` and `_discard` so corrupt `meta('continuity')` never crashes `SqlStore` reopen while holding AI scopes closed (`RV-003`, `RV-004`, `PC-002`, `PC-003`). | `test_restart_gate_sql_fences.py` (9/9), `test_seed_merge.py` (21/21), `test_mssqlstore.py` (244 run, 235 skipped), `ruff`, `mypy` |
| `P02-T01` | `src/core/src/zava_forward/core/assistants.py`, `src/api/tests/test_mssqlstore.py`, `src/core/README.md`, `src/api/README.md` | Removed `NEW.outcome <> OLD.outcome` (`i.outcome <> d.outcome`) from `assistant_attempts` open-hold update triggers (`RV-002`); added `review_gate_version` (`COLLATE Latin1_General_100_BIN2` on MSSQL) and `reviewed_revision` to `assistant_tasks` in `SQLITE_DDL`, `MSSQL_DDL`, and ledger-safe `Assistants._add_column` / `_upgrade` (`PC-005`); added `assistant_tasks` SQLite and T-SQL gate/hold triggers plus trigger drops in `test_mssqlstore.py:wipe()`; stamped `review_gate_version` and `reviewed_revision = revision + 1` in `Assistants.review()` for `verify`/`accept`/`edit-accept` while keeping `reject` unfenced (`RV-003`); and updated `src/core/README.md` and `src/api/README.md`. | `test_restart_gate_sql_fences.py` (9/9), `test_continuity_restart_gate.py` (9/9), `test_assistants.py` (138 run, 60 skipped), `ruff`, `mypy` |
| `P03-T01` | `src/core/tests/test_restart_gate_sql_fences.py` | Expanded to 9 strictly typed core tests covering tweaked-prose normalized `test_id` anti-replay across same/other Keep-suspended, concurrent open, and Restarted incidents, in-place `sending` `assistant_attempts` hold-update aborts, `assistant_tasks` `verify`/`accept` trigger aborts, corrupt `meta('continuity')` (`""` and `"{not-json"`) store reopen + sequential fast-path `save()` + `_discard()` rollback manual continuity, and explicit worktree `PYTHONPATH` on subprocesses (`RV-001`–`RV-005`). | `python3 -m unittest discover -s tests -p "test_restart_gate_sql_fences.py" -q` (9/9 passed) |
| `P03-T02` | `src/api/tests/test_continuity_restart_gate.py` | Expanded 9 strictly typed API tests (`9 + 9 = 18 <= 25` combined ceiling) with `PasswordProvider` `POST /api/continuity/restart-decide` `403` + `ai_restart_decide_denied`, HTTP store-dispatched denial audit assertions (including tweaked-prose `test_id` replay), HTTP `challenge_update` and `challenge_escalate` during `all` suspension, `threading.Barrier(2)` races for `verify` vs `suspend` and mid-flight `_fence_in`/`complete` vs `suspend`, commit-invariant git-free `gate-v0` and `pre-gate` subprocess workers at `epoch = 0` across `queued`/`leased`/`ready`/`export`, and MSSQL ledger `_add_column` 4-step DDL verification (`RV-003`, `RV-005`, `PC-001`, `PC-005`). | `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_continuity_restart_gate.py" -q` (9/9 passed) |
| `P03-T03` | `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md`, `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c2-changes.md` | Executed focused and regression unit suites across `src/core` and `src/api`, `tools/rename-zava-tests.py`, `ruff check`, `ruff format --check`, and strict `mypy`, then removed temporary workspace-local `.venv-122-local` (`rm -rf .venv*`) and re-verified focused suites with system `python3`. | All checks passed; `.venv-122-local` removed |

## Implementation-Time Plan and Detail Updates

* **`P01-T01` (`FR-01` / `AC-01` candidate-scoped independent `test_id` replay across decided/restarted incidents)**: Existing regression suite `src/api/tests/test_operator_suspension.py` (`drill` -> `retained_snapshot(test, "assistant", "prior")`, lines 377–379) promotes a new active release (`release_version="new"`, changing `candidate`) after restarting a prior suspension and legitimately re-executes the standard regression suite identifier `test_id="constructed-negative-and-fallback-drill"` against the new candidate. Scoping decided/restarted `_raw_tid(prop) or _raw_ev(prop)` checks to `current_candidate` while keeping concurrent open-suspension `_raw_tid(open_prop) or _raw_ev(open_prop)` checks unconditional rejects every tweaked-prose `test_id` replay for the active candidate (closing `RV-001`) while preserving existing candidate-upgrade regression drills (`20/20` passing in `test_operator_suspension*.py`). Reconciled in `c2-plan.md`, `c2-phase-details.md`, `src/core/README.md`, and `src/api/README.md`.
* **`P03-T02` (`NFR-01` combined test count)**: Consolidated the new `PasswordProvider`, HTTP challenge lifecycle, barrier races, commit-invariant `pre-gate` subprocess, and MSSQL ledger `_add_column` assertions cleanly inside 9 `test_continuity_restart_gate.py` methods + 9 `test_restart_gate_sql_fences.py` methods (`18 <= 25` combined ceiling, zero test removals). Reconciled in `c2-plan.md`.

## Validation Results

| Check | Command | Result |
| --- | --- | --- |
| Core restart-gate & SQL fences (`P03-T01`) | `(cd src/core && python3 -m unittest discover -s tests -p "test_restart_gate_sql_fences.py" -q)` | Passed (`9` tests) |
| Core seed-merge regression | `(cd src/core && python3 -m unittest discover -s tests -p "test_seed_merge.py" -q)` | Passed (`21` tests) |
| API continuity restart-gate (`P03-T02`) | `(cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_continuity_restart_gate.py" -q)` | Passed (`9` tests) |
| API assistants & dialect regression | `(cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_assistants.py" -q)` | Passed (`138` run, `60` skipped) |
| API MSSQL portability & DDL regression | `(cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_mssqlstore.py" -q)` | Passed (`244` run, `235` skipped) |
| API operator suspension regression | `(cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_operator_suspension*.py" -q)` | Passed (`20` tests) |
| API continuity epoch/export regression | `(cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_continuity_epoch_export.py" -q)` | Passed (`77` run, `39` skipped) |
| Migration regression guard | `python3 tools/rename-zava-tests.py` | Passed (`25` tests) |
| Ruff lint & format check (`src/core`, `src/api`) | `ruff check . && ruff format --check .` in `src/core` and `src/api` | Passed (`0` issues; `282` + `197` formatted; `[tool.ruff.format].exclude` honored) |
| Strict Mypy (`src/core`, `src/api`) | `mypy .` in `src/core` (`335` files) and `src/api` (`281` files) | Passed (`0` issues across `616` files) |
| Temporary venv cleanup | `rm -rf .venv*` | Clean (no `.venv*` directories remain) |

## Blockers, Remaining Work, and Follow-Ups

* Blockers: `none`
* Remaining active implementation work: `none` (`P01` through `P03` complete and reconciled)
* Follow-up items outside local scope (`Refs #122`):
  1. Owner-witnessed operational continuity/restart drill and `OD-35` / `OQ-017` / `RULE-020` human restart authority appointment (Programme Sponsor / Building Safety).
  2. Immutable external Azure ledger-head storage and live multi-replica Azure SQL (`ZF_TEST_MSSQL=1`) continuity/restart drill (Platform / Data Governance).

## Handoff

Implementation of `issue-122-restart-gate-0228-c2` is complete and reconciled across plan, phase details, changes evidence, and local validation. Ready for single-pass post-implementation `rpi-review`.
