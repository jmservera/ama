---
title: "Implementation Plan - Issue #122 RAI Incident and Restart Gate Remediation (Cycle 2)"
description: "Surgical remediation plan for Cycle 1 review findings RV-001 through RV-005 in src/core and src/api"
author: "Copilot"
ms.date: "2026-11-15"
---

## Metadata

* Task ID: `issue-122-restart-gate-0228-c2`
* Task Slug: `issue-122-restart-gate-0228-c2`
* Parent Task: `issue-122-restart-gate-0228`
* Branch: `feat/platform-122-restart-gate-0228` (targeting `feat/demo-164-chat-grounding-provenance-0900`, `PR #1641`)
* Date: `2026-11-15`
* Planning Status: `Ready after Critique`
* Validation Tier: `Full` (SQL trigger and gate-semantics refinement on `continuity.py`, `sqlstore.py`, and `assistants.py`; local focused + full unit suites, `ruff`, and strict `mypy` executed in this cycle without pushing per caller freeze instruction)
* Research Artifact: `.copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-research.md` (`reused`)
* Parent Review Artifact: `.copilot-tracking/reviews/logs/2026-11-15/issue-122-restart-gate-0228-review.md` (`RV-001`–`RV-005`)
* Phase Details Artifact: `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md`
* Critique Artifact: `.copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan-critique.md`
* Downstream Changes Artifact: `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c2-changes.md`

## Executive Summary

Cycle 2 (`issue-122-restart-gate-0228-c2`) resolves all five defects (`RV-001` through `RV-005`) routed to implementation by the single-pass Cycle 1 review of Issue `#122`'s local RAI Incident and Restart criteria:

1. **Normalized `test_id` anti-replay (`RV-001`)**: Tighten `_check_claim_replay` in `src/core/src/zava_forward/core/continuity.py` so normalized `test_id` (`strip().casefold()`) is rejected independently across prior `"Keep suspended"` decisions on the active suspension, open proposals on other active suspensions, and `"Restart"` approvals on prior `"Restarted"` suspensions, regardless of whether `corrective_evidence` text or `candidate` changes, while keeping normalized `(candidate, corrective_evidence)` replay rejection intact.
2. **Active `assistant_attempts` hold-update SQL trigger enforcement (`RV-002`)**: Remove the `NEW.outcome <> OLD.outcome` (`i.outcome <> d.outcome`) condition from `assistant_attempts_hold_update` (SQLite) and the open-hold branch of `assistant_attempts_gate_update` (T-SQL) in `src/core/src/zava_forward/core/assistants.py` so any update leaving `outcome IN ('reserved', 'sending')` (such as refreshing `active_until` or `send_gate_version` on an already-`sending` or `reserved` row) aborts at the SQL trigger boundary whenever a matching hold exists in `continuity_open_holds`, while terminal settlement (`outcome` moving out of `('reserved', 'sending')`) continues cleanly.
3. **Genuine pre-gate exclusion for `ready` proposal review/accept and export (`RV-003`)**: Enforce defense-in-depth exclusion of genuine pre-gate (`HEAD`) and mismatched-gate workers/readers across both `ready` proposals and export:
   * Wrap SQL-persisted `meta('continuity')` via `continuity.dump_sql` (`{"gate_version": "continuity-gate-v1", "epoch": -1, "continuity": <doc>}`) and `continuity.load` / `continuity.unwrap_sql` so an unmodified pre-gate (`HEAD`) image sees top-level `epoch == -1`, fails `HEAD`'s `history_valid`, marks `ready`/`accepted` proposals `epoch_current=False`, `actionable=False`, `relied_on=False` in `export()` and `detail()`, and refuses `review("verify" | "accept" | "edit-accept")` while preserving `review("reject")` and manual operations; and so `v1` likewise fails closed if a future `gate_version` envelope is encountered.
   * Add `review_gate_version` and `reviewed_revision` columns plus SQLite (`BEFORE INSERT`, `BEFORE UPDATE`) and T-SQL (`AFTER INSERT, UPDATE`) triggers on `assistant_tasks` (`assistant_tasks_gate_insert`, `assistant_tasks_hold_insert`, `assistant_tasks_gate_update`, `assistant_tasks_hold_update` in SQLite; `assistant_tasks_gate_insert`, `assistant_tasks_gate_update` in T-SQL), stamping `review_gate_version = continuity.GATE_VERSION` and `reviewed_revision = revision + 1` in `Assistants.review()` for `verify`, `accept`, and `edit-accept` so direct or pre-gate SQL updates that accept or verify a `ready` proposal without a matching `review_gate_version`/`reviewed_revision` or under an open hold abort at the database layer.
4. **Corrupt `meta('continuity')` startup and manual-continuity recovery (`RV-004`)**: Fix `continuity.load(raw)` so `raw is None` returns `blank()` while `raw == ""` or malformed/non-dict JSON returns `dict(epoch=-1, suspensions=[], changes=[])` (failing `history_valid` closed), and route `key == "continuity"` through `continuity.load(...)` in `SqlStore._proc_sync` and `SqlStore._discard` (and `continuity.unwrap_sql` in `SqlStore.merge_seed`) so reopening `SqlStore` over corrupt `meta('continuity')` never crashes with `JSONDecodeError`, holds all AI capabilities fail-closed, and preserves manual case work, accessible challenge, and statutory hazard response.
5. **Planned verification completeness and pre-gate worker test (`RV-005`)**: Expand `src/core/tests/test_restart_gate_sql_fences.py` and `src/api/tests/test_continuity_restart_gate.py` within the locked `<= 25` combined test method ceiling (target: `20` methods total, zero removals) with explicit worktree `PYTHONPATH` on subprocesses, a commit-invariant git-free pre-gate worker subprocess shim (`pre-gate continuity.load` + no-op `gate_hold` + legacy pre-gate SQL write shapes) tested against `queued`, `leased`, and `ready` proposals (plus `export()` at `epoch = 0` and during suspension), corrupt `meta('continuity')` reopen + sequential-save/rollback manual-continuity proof, MSSQL ledger `_add_column` DDL proof, `PasswordProvider` `restart-decide` `403` + `ai_restart_decide_denied` audit proof, HTTP denial audit assertions, HTTP `challenge_update` and `challenge_escalate` coverage, and `threading.Barrier(2)` races for `verify` vs `suspend` and mid-flight `_fence_in`/`complete_result` vs `suspend`.

## Sources and Evidence

* `.copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-research.md` (`C1`–`C18`)
* `.copilot-tracking/reviews/logs/2026-11-15/issue-122-restart-gate-0228-review.md` (`RV-001`–`RV-005`)
* `.copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan-critique.md` (`PC-001`–`PC-006`)
* `src/core/src/zava_forward/core/continuity.py` (`load`, `dump_sql`, `unwrap_sql`, `_check_claim_replay`, `gate_sync_rows`, `sync_sql_gate`)
* `src/core/src/zava_forward/core/sqlstore.py` (`_seed`, `merge_seed`, `save`, `_discard`, `_proc_sync`, `_proc_write`)
* `src/core/src/zava_forward/core/assistants.py` (`SQLITE_DDL`, `MSSQL_DDL`, `SQLITE_ATTEMPT_TRIGGERS`, `MSSQL_ATTEMPT_TRIGGERS`, `_add_column`, `_upgrade`, `review`)
* `src/api/tests/test_mssqlstore.py` (`wipe` trigger drop list)
* `src/core/tests/test_restart_gate_sql_fences.py` and `src/api/tests/test_continuity_restart_gate.py`
* `src/core/pyproject.toml` and `src/api/pyproject.toml` (`[tool.ruff.format].exclude` on `continuity.py`, `sqlstore.py`, `mssqlstore.py`, `assistants.py`, `test_mssqlstore.py`, `test_assistants.py`)

## User Decisions and Requirements

* Deliver the remaining local RAI Incident and Restart acceptance criteria of Issue `#122` in `src/core` and `src/api` on branch `feat/platform-122-restart-gate-0228` targeting `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`).
* Resolve all defects (`RV-001`–`RV-005`) identified in Cycle 1 review `.copilot-tracking/reviews/logs/2026-11-15/issue-122-restart-gate-0228-review.md` while preserving all Cycle 1 passing behavior.
* Keep dated RPI artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews/logs`) and keep `.copilot-tracking/` references out of production code, tests, docs, and commit messages.
* Run focused and regression unit tests in `src/core` and `src/api`, `tools/rename-zava-tests.py`, `ruff check`, `ruff format --check`, and strict `mypy`.
* Commit locally with `Refs #122` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`; do NOT push; leave `git status --short` empty.

## Goals

* Eliminate `test_id` claim replay even when `corrective_evidence` text or `candidate` is altered (`RV-001`).
* Block active `reserved`/`sending` updates on `assistant_attempts` under open holds at the SQLite and T-SQL trigger layer even when `outcome` does not change (`RV-002`).
* Prevent genuine pre-gate (`HEAD`) and mismatched-gate workers/readers from verifying, accepting, or exporting `ready` proposals as actionable/relied-on, backed by both SQL `assistant_tasks` triggers and a versioned `meta('continuity')` SQL envelope (`RV-003`).
* Recover cleanly on `SqlStore` startup/reload when `meta('continuity')` is empty or corrupt JSON so manual case work, accessible challenge, and hazard response remain available while AI capabilities stay held fail-closed (`RV-004`).
* Complete all planned concurrency, audit, `PasswordProvider`, HTTP challenge lifecycle, subprocess `PYTHONPATH`, MSSQL ledger `_add_column`, and commit-invariant pre-gate worker tests within the `<= 25` combined test method ceiling (`RV-005`).

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/continuity.py`
* `src/core/src/zava_forward/core/sqlstore.py`
* `src/core/src/zava_forward/core/assistants.py`
* `src/api/tests/test_mssqlstore.py`
* `src/core/tests/test_restart_gate_sql_fences.py`
* `src/api/tests/test_continuity_restart_gate.py`
* `src/core/README.md` and `src/api/README.md`

### Non-Goals

* External cloud deployment, multi-replica container rollout, or hosted MSSQL infrastructure validation (unmet external criteria of Issue `#122`, documented via `Refs #122`).
* Any edits to `src/core/pyproject.toml` or `src/api/pyproject.toml` `[tool.ruff.format].exclude` lists or formatting of excluded legacy files.
* Modifying Cycle 1 immutable historical review or critique artifacts.

## Functional Requirements

* `FR-01` (`RV-001`): `continuity._check_claim_replay` (retaining `current_candidate=None` default) must normalize `test_id` (`strip().casefold()`) and `corrective_evidence` (`strip().casefold()`) independently so reusing either `test_id` or `corrective_evidence` (even when the other field changes) is rejected unconditionally across concurrently open `"Suspended"` incidents (`other["id"] != current_suspension["id"]`) and rejected for the same `candidate` across prior `"Keep suspended"` decisions (same or other suspension) and approved `"Restart"` proposals on `"Restarted"` incidents, preserving legitimate re-execution of a named regression suite against a newly promoted candidate release (`test_operator_suspension.py`).
* `FR-02` (`RV-002`): SQLite `assistant_attempts_hold_update` and T-SQL `assistant_attempts_gate_update` must abort/throw on any `UPDATE assistant_attempts` where `NEW.outcome IN ('reserved', 'sending')` (`i.outcome IN ('reserved', 'sending')`) and a matching `'all'` or capability row exists in `continuity_open_holds`, even when `NEW.outcome = OLD.outcome`.
* `FR-03` (`RV-003` SQL trigger fence + ledger-safe upgrade): `assistant_tasks` must define `review_gate_version` (`COLLATE Latin1_General_100_BIN2` on MSSQL) and `reviewed_revision` columns (in fresh SQLite/MSSQL DDL and ledger-safe `Assistants._add_column` / `_upgrade`) and SQLite/T-SQL triggers blocking `INSERT` (`state = 'accepted'`) and `UPDATE` (`state = 'accepted'` transition/mutation, or `OLD.state = 'ready' AND NEW.state = 'ready' AND NEW.revision <> OLD.revision AND NEW.dispatched = OLD.dispatched`) unless `NEW.reviewed_revision = NEW.revision`, `NEW.review_gate_version` matches `continuity_gate_state.gate_version`, and no matching row exists in `continuity_open_holds`. `Assistants.review()` must stamp `review_gate_version = continuity.GATE_VERSION` and `reviewed_revision = revision + 1` for `verify`, `accept`, and `edit-accept` while leaving `reject` unfenced.
* `FR-04` (`RV-003` + `RV-004` SQL continuity envelope & corrupt recovery): `continuity.dump_sql(doc)` must store `{"gate_version": GATE_VERSION, "epoch": -1, "continuity": doc}` in `meta('continuity')` (including seeding absent `meta('continuity')` and upgrading valid unwrapped plain-JSON rows during `sync_sql_gate(read_meta=True)` plus `_seed` and `merge_seed`) so pre-gate readers see `epoch == -1` even at `epoch = 0` before any suspension and fail `history_valid` closed across `export()`, `detail()`, `review()`, and AI dispatch; `continuity.load(raw)` must return `blank()` only when `raw is None`, unwrap matching `GATE_VERSION` envelopes, fail closed (`epoch = -1`) on mismatched `gate_version`, empty string `""`, malformed JSON, or non-dict values, and still load un-enveloped seed/test dicts; `SqlStore._proc_sync`, `SqlStore._discard`, `SqlStore._proc_write`, and `SqlStore.save()` must keep `self._proc_loaded` synchronized across fast-path saves while leaving untouched corrupt `meta('continuity')` intact, and `SqlStore.merge_seed` must compare `key == "continuity"` through `continuity.unwrap_sql`.
* `FR-05` (`RV-005`): `test_restart_gate_sql_fences.py` and `test_continuity_restart_gate.py` must verify `FR-01`–`FR-04` plus `PasswordProvider` `restart-decide` `403`, HTTP `ai_restart_propose_denied` / `ai_restart_decide_denied` audit rows, HTTP `challenge_update` and `challenge_escalate` during `all` suspension, `threading.Barrier(2)` races for `verify` vs `suspend` and mid-flight `_fence_in`/`complete_result` vs `suspend`, explicit subprocess `PYTHONPATH`, MSSQL ledger `_add_column` DDL emission, and a commit-invariant git-free pre-gate worker subprocess shim against `queued`, `leased`, and `ready` proposals (including `export()` at `epoch = 0` and during suspension).

## Non-Functional Requirements

* `NFR-01` (Test Ownership and Ceiling):
  * Canonical test targets: `src/core/tests/test_restart_gate_sql_fences.py`, `src/api/tests/test_continuity_restart_gate.py`, and `src/api/tests/test_mssqlstore.py` (`wipe` trigger drop tuple only).
  * Generated targets: `none`.
  * Exact test removals: `none`.
  * Maximum test method count across `test_restart_gate_sql_fences.py` + `test_continuity_restart_gate.py`: `<= 25` combined (`9` core + `9` API = `18` delivered).
  * Semantic vs regression split: semantic tests in the two dedicated restart-gate test modules validate `RV-001`–`RV-005`; full `src/core` and `src/api` `unittest` discovery plus `tools/rename-zava-tests.py` guard existing behavior (including `test_seed_merge.py`, `test_quality_sensors*.py`, `test_operator_suspension*.py`, `test_continuity_epoch_export.py`, `test_assistants.py`, and `test_mssqlstore.py`).
* `NFR-02` (Lint, Format, and Type Safety): Respect `[tool.ruff.format].exclude` in `src/core/pyproject.toml` and `src/api/pyproject.toml` by running `ruff check src/core src/api`, `ruff format --check src/core src/api`, and strict `mypy` on `src/core` and `src/api` from a temporary workspace-local `.venv-122-local` removed before completion. Never use `/tmp`.

## Acceptance Criteria

* `AC-01`: Reusing a normalized `test_id` (`strip().casefold()`) with altered `corrective_evidence` raises `PermissionError` (`403` over HTTP with denial audit) across Keep-suspended retry (same or other suspension for the candidate), concurrently open suspension (regardless of candidate), and prior Restarted suspension for the candidate, while allowing a newly promoted candidate release to run its regression suite (`RV-001`).
* `AC-02`: Updating an already-`sending` or `reserved` row in `assistant_attempts` while keeping `outcome IN ('reserved', 'sending')` during an open hold in `continuity_open_holds` aborts in SQLite and matches the T-SQL trigger predicate (`RV-002`).
* `AC-03`: Both raw pre-gate SQL and a commit-invariant git-free pre-gate worker subprocess (pre-gate `continuity.load`, no-op `gate_hold`, and legacy pre-gate SQL write shapes) operating on a migrated SQLite store with `queued`, `leased`, and `ready` proposals fail closed on `claim`/`execute`, `_fence_in`, `review("verify")`, and `review("accept")`, and report `actionable=False`, `relied_on=False`, `epoch_current=False` in `export()` even at `epoch = 0` before any suspension, while `review("reject")` and manual routes succeed (`RV-003`).
* `AC-04`: Reopening `SqlStore` when `meta WHERE key='continuity'` is `""` or `"{not-json"` succeeds without raising, holds AI capabilities fail-closed, preserves sequential fast-path `save()` / `_discard()` rollback consistency, and allows manual case progress, accessible challenge, and hazard escalation/mitigation (`RV-004`).
* `AC-05`: `PasswordProvider` `restart-decide` returns `403` with `ai_restart_decide_denied`; HTTP store-dispatched restart denials record `ai_restart_propose_denied` / `ai_restart_decide_denied`; HTTP `challenge_open` (`Phone` + `Digital`), `challenge_update`, `challenge_escalate`, and `challenge_resolve` succeed during `all` suspension; `threading.Barrier(2)` races cover `claim`, `_fence_in`/`complete_result`, `verify`, and `accept` against `suspend`; subprocesses pin worktree `PYTHONPATH`; MSSQL ledger `_add_column` emits the 4-step sequence; and all `src/core` + `src/api` unit suites, `ruff`, and strict `mypy` pass (`RV-005`).

## Phase Checklist

<!-- P01 -->
### [x] Phase P01: Core Continuity Anti-Replay, SQL Envelope, and Corrupt-Meta Recovery (`RV-001`, `RV-003`, `RV-004`)

<!-- P01-T01 -->
* [x] Task P01-T01: Update `continuity.py` (`load`, `dump_sql`, `unwrap_sql`, `gate_sync_rows`, and independent normalized `test_id` anti-replay in `_check_claim_replay`)
<!-- P01-T02 -->
* [x] Task P01-T02: Update `sqlstore.py` (`_seed`, `merge_seed`, `_discard`, `_proc_sync`, `_proc_write`) to persist the versioned continuity SQL envelope and recover cleanly from corrupt `meta('continuity')`

<!-- P02 -->
### [x] Phase P02: SQL Trigger Hardening on `assistant_attempts` and `assistant_tasks` (`RV-002`, `RV-003`)

<!-- P02-T01 -->
* [x] Task P02-T01: Tighten `assistant_attempts` open-hold update triggers and add `review_gate_version` + `reviewed_revision` columns and SQLite/T-SQL triggers on `assistant_tasks` in `assistants.py` (plus `wipe()` in `test_mssqlstore.py` and `README.md` notes)

<!-- P03 -->
### [x] Phase P03: Focused SQL/API Verification Expansion and Full Local Validation (`RV-005`)

<!-- P03-T01 -->
* [x] Task P03-T01: Expand `src/core/tests/test_restart_gate_sql_fences.py` (`<= 10` tests) for independent `test_id` replay, active-sending hold-update trigger, `assistant_tasks` review trigger, corrupt `meta('continuity')` reopen, and explicit subprocess `PYTHONPATH`
<!-- P03-T02 -->
* [x] Task P03-T02: Expand `src/api/tests/test_continuity_restart_gate.py` (`<= 12` tests, combined `<= 25`) for commit-invariant pre-gate worker subprocess (`queued`/`leased`/`ready`/`export`), `PasswordProvider` `restart-decide` `403`, HTTP denial audits, HTTP `challenge_update`/`challenge_escalate`, and `verify` + `_fence_in` barrier races
<!-- P03-T03 -->
* [x] Task P03-T03: Run `src/core` and `src/api` focused and regression unit suites, `tools/rename-zava-tests.py`, `ruff check`, `ruff format --check`, and strict `mypy` in temporary workspace-local `.venv-122-local` and clean up `.venv-122-local`

## Critique Disposition

Single-pass critique `.copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan-critique.md` completed with verdict `Revise` (`1 Critical`, `3 High`, `1 Medium`, `1 Low`; `0` user decisions required). All six planner-owned corrections are applied directly:

* `PC-001` (`Critical`, applied): Replaced `git show HEAD:...` in `P03-T02` and `AC-03` with a commit-invariant, git-free pre-gate worker subprocess shim (exact pre-gate `continuity.load`, no-op `gate_hold`, and legacy pre-gate SQL write shapes for `assistant_attempts` and `assistant_tasks`) so tests pass identically before and after `git commit` and in gitless container environments.
* `PC-002` (`High`, applied): Updated `P01-T01` and `P01-T02` so `continuity.sync_sql_gate(..., read_meta=True)` portably seeds `meta('continuity')` with `dump_sql(blank())` when absent and upgrades valid unwrapped plain-JSON rows to `dump_sql(...)`, while `SqlStore._seed` and `SqlStore.merge_seed` also serialize `"continuity"` via `dump_sql`, ensuring pre-gate `export()` and `Store` AI paths fail closed even at `epoch = 0` before any suspension.
* `PC-003` (`High`, applied): Updated `P01-T02` and `P03-T01` so `self._proc_loaded` is initialized to `{}`, synchronized after `COMMIT` on `SqlStore.save()`'s `cur == self._seq` fast path, and aligned for `None`-snapshot + `blank()` reads, with sequential-save and corrupt-rollback test assertions.
* `PC-004` (`High`, applied): Updated `P01-T01` and `P03-T01` so `_check_claim_replay` preserves `current_candidate=None`, guards `current_candidate is not None` inside `_same_ev`, checks `other.get("id") != current_suspension.get("id")`, checks `other.get("decisions", [])` across all other suspensions for rejected-claim replay, and checks open suspensions on both propose and decide.
* `PC-005` (`Medium`, applied): Updated `P02-T01` and `P03-T02` so `Assistants._add_column` handles MSSQL updatable ledger tables (`sys.tables.ledger_type != 0`) with the 4-step nullable `ADD` + `UPDATE` + `CHECK` + `DEFAULT` sequence, passes `COLLATE Latin1_General_100_BIN2` for `review_gate_version` in `_upgrade`, and adds a unit check for ledger `ALTER TABLE` emission.
* `PC-006` (`Low`, applied): Replaced the non-existent `docs/adr/0006-ruff-format-exclude-on-six-core-modules.md` reference with `src/core/pyproject.toml` and `src/api/pyproject.toml` (`[tool.ruff.format].exclude`).

## Follow-Up Items

1. Hosted/containerized multi-replica Azure SQL (`MssqlStore`) rollout drill and live runtime verification for the external deployment criteria of Issue `#122` (outside local `src/core` and `src/api` worktree scope; tracked via `Refs #122`).

## Handoff

After single-pass `rpi-plan-critique` disposition, automatic RPI Agent mode transitions directly to `Implement` (`rpi-implement`) writing `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c2-changes.md`.
