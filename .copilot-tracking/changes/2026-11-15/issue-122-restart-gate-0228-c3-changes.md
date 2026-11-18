---
title: "Changes Log - Issue #122 SQL Server Ledger Trigger Guard and Base Merge (Cycle 3)"
description: "Implementation evidence for Cycle 3 SQL Server WITH LEDGER = ON trigger guards, base-branch merge preserving PR #1781 is_available_case_document, and DialectTests verification"
author: "Copilot"
ms.date: "2026-11-15"
---

## Metadata

* Task ID: `issue-122-restart-gate-0228-c3`
* Parent Task ID: `issue-122-restart-gate-0228-c2`
* Plan Path: `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c3-plan.md`
* Phase Details Path: `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c3-phase-details.md`
* Critique Path: `.copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-c3-plan-critique.md`
* Declared Scope: Full plan (`P01` through `P02`)
* Execution Status: `Completed`

## Opening Implementation State

* Active checklist markers: `P01` (`P01-T01`, `P01-T02`, `P01-T03`, `P01-T04`), `P02` (`P02-T01`, `P02-T02`) — all completed (`[x]`).
* First dependency-ready task: `P01-T01`.
* Blockers: `none`.

## Completed Phase and Task Evidence

| Marker | Files Changed | Summary of Changes | Validation |
| --- | --- | --- | --- |
| `P01-T01` | Git merge (`origin/feat/demo-164-chat-grounding-provenance-0900` at `c7e5c8848`), `src/core/src/zava_forward/core/assistants.py`, `src/core/README.md` | Configured privacy-safe local git email (`8036360+jmservera@users.noreply.github.com`) via `gh api user` and merged `origin/feat/demo-164-chat-grounding-provenance-0900` cleanly (`ort` strategy, zero conflicts) without rewriting published `PR #1787` commit `d0d4135d3`, preserving `from .doc_controls import is_available_case_document` and `if d.get("kind") in kinds and is_available_case_document(d)` in `assistants.py:capture()` (`FR-01`). | `test_document_controls.py` + `test_assistants.py` (`166` run, `60` skipped, `OK`) |
| `P01-T02` | `src/core/src/zava_forward/core/mssqlstore.py` | Moved `for trigger in GATE_TRIGGERS: self.db.execute(trigger)` inside the `else:` branch of `if ledger:` in `MssqlStore._create_schema_serialized` so DML triggers are omitted on SQL Server `WITH LEDGER = ON` databases while remaining active on non-ledger SQL Server databases (`FR-02`). | `DialectTests` (`2/2`), `test_mssqlstore.py` (`244` run, `235` skipped), `mypy`, `ruff` |
| `P01-T03` | `src/core/src/zava_forward/core/assistants.py` | Initialized `ledger = False` before `if self.mssql:` and guarded trigger loop execution with `if not (self.mssql and ledger):` in `Assistants.migrate` while leaving `continuity.sync_sql_gate(db, read_meta=True, mssql=self.mssql)` unconditional (`FR-03`). | `DialectTests` (`2/2`), `test_restart_gate_sql_fences.py` (`9/9`), `mypy`, `ruff` |
| `P01-T04` | `src/core/README.md` | Documented that SQLite and non-ledger SQL Server databases install DML gate triggers whereas SQL Server `WITH LEDGER = ON` databases omit DML triggers on system-versioned updatable ledger tables while maintaining `continuity_gate_state` / `continuity_open_holds` synchronization and Python fail-closed fences (`FR-04`). | Diff & Markdown link check |
| `P02-T01` | `src/api/tests/test_assistants.py` | Extended `DialectConnection` with `ledger=False` (`SELECT is_ledger_on` -> `1`/`0`, `SELECT ledger_type_desc` -> `'APPEND_ONLY_LEDGER_TABLE'` ahead of `FROM sys.tables`, `sqlite3.OperationalError` on `CREATE TRIGGER` when `ledger=True` ahead of `"N'TR'"`, and `LEDGER`/`IDENTITY(1,1)`/`N'` DDL normalization), asserted `CREATE TRIGGER` emission in non-ledger `test_mssql_sql_shapes_enqueue_claim_complete_review_scan`, and added `test_mssql_ledger_mode_skips_triggers_and_syncs_continuity_gate` proving both `MssqlStore._create_schema_serialized` and `Assistants.migrate` execute zero `CREATE TRIGGER` statements under `is_ledger_on = 1` while synchronizing `continuity_gate_state` and `continuity_open_holds` (`FR-04`, `NFR-01`, `PC-001`, `PC-002`). | `test_assistants.DialectTests` (`2/2` passed in `4.712s`), `mypy`, `ruff` |
| `P02-T02` | `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c3-plan.md`, `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c3-changes.md` | Executed full focused unit, static typing, format, lint, and migration regression validations across `src/core` and `src/api` and reconciled all `P01`/`P02` markers (`AC-03`, `AC-04`, `NFR-02`, `PC-003`). | All checks passed (`0` failures) |

## Implementation-Time Plan and Detail Updates

* Local judgment (`P02-T02`): Because `zava_forward` distributions are not editable-installed into global `/usr/lib/python3.12` in this isolated worktree, `src/core/tests` discovery and `src/api` `mypy` pass explicit worktree `PYTHONPATH` (`PYTHONPATH=src/core/src` for `src/core/tests` and `PYTHONPATH=../core/src:../agents/src` for `src/api` `mypy`, matching `.github/copilot-instructions.md` and `.github/workflows/src-ci.yml`). No plan scope, requirement, or acceptance-criteria divergence occurred.

## Validation Results

| Check | Command | Result |
| --- | --- | --- |
| Core restart-gate & SQL fences | `PYTHONPATH=src/core/src python3 -m unittest discover -s src/core/tests -p "test_restart_gate_sql_fences.py" -v` | Passed (`9` tests in `8.123s`) |
| API continuity restart-gate, assistants (incl. `DialectTests`), & document controls (`#1781`) | `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest src/api/tests/test_continuity_restart_gate.py src/api/tests/test_assistants.py src/api/tests/test_document_controls.py -v` | Passed (`166` tests run, `60` skipped) |
| Targeted `DialectTests` (ledger & non-ledger) | `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests:src/api/tests python3 -m unittest test_assistants.DialectTests -v` | Passed (`2` tests in `4.712s`) |
| API MSSQL portability & DDL regression | `(cd src/api && PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_mssqlstore.py" -q)` | Passed (`244` tests run, `235` skipped) |
| Migration regression guard | `python3 tools/rename-zava-tests.py` | Passed (`25` tests) |
| Mypy (`src/core` and `src/api`) | `(cd src/core && mypy) && (cd src/api && PYTHONPATH=../core/src:../agents/src mypy)` | Passed (`0` issues in `354` `src/core` files + `298` `src/api` files) |
| Ruff lint & format check (`src/core`, `src/api`) | `python3 -m ruff check src/core src/api && (cd src/core && python3 -m ruff format --check .) && (cd src/api && python3 -m ruff format --check .)` | Passed (`All checks passed!`; `301` + `214` files formatted; `[tool.ruff.format].exclude` honored) |

## Blockers, Remaining Work, and Follow-Ups

* Blockers: `none`
* Remaining active implementation work: `none` (`P01` and `P02` complete and reconciled)
* Follow-up items outside local scope (`Refs #122`):
  * Execute owner-witnessed operational continuity/restart drill and record appointed OD-35 / OQ-017 restart authority delegation once governance sign-off exists.
  * Provision immutable external Azure ledger-head container and run owned Azure SQL continuity/restart drill, and observe hosted `Source projects CI` (`MssqlLedgerMigration` and `MssqlLedgerTests`) after owner/orchestrator push.
