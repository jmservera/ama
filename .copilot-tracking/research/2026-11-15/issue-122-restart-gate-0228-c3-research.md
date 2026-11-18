<!-- markdownlint-disable-file -->

# Task Research: issue-122-restart-gate-0228-c3

| Field              | Value                                                                          |
|--------------------|--------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                     |
| Researcher / agent | rpi-research (RPI Agent automatic mode)                                        |
| Status             | Complete                                                                       |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-c3-research.md |

## Research Brief

* What to research: Exact CI failure in `PR #1787` (job `132785382777`) across `test_mssqlstore.MssqlLedgerMigration` (`5` tests) and `test_assistants.MssqlLedgerTests` (`2` tests) on SQL Server `WITH LEDGER = ON` databases, plus clean base-branch synchronization with `origin/feat/demo-164-chat-grounding-provenance-0900` preserving `PR #1781` (`#117`) `is_available_case_document` filtering in `src/core/src/zava_forward/core/assistants.py:capture()`.
* Why it matters: SQL Server 2022 makes every non-append-only table created inside a `WITH LEDGER = ON` database (`continuity_gate_state`, `continuity_open_holds`, `assistant_attempts`, `assistant_tasks`) a system-versioned `UPDATABLE_LEDGER_TABLE` and forbids creating DML triggers on system-versioned ledger tables. Unconditional execution of `GATE_TRIGGERS` and `MSSQL_ATTEMPT_TRIGGERS` fails schema initialization in SQL Server ledger databases.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` in this automatic RPI Cycle 3 session, plus reviewers of `PR #1787` targeting `feat/demo-164-chat-grounding-provenance-0900`.
* Scope: `src/core/src/zava_forward/core/mssqlstore.py`, `src/core/src/zava_forward/core/assistants.py`, `src/core/README.md`, `src/api/tests/test_assistants.py`, and git branch synchronization with `origin/feat/demo-164-chat-grounding-provenance-0900`.
* Non-goals: Do not alter SQLite trigger enforcement or non-ledger SQL Server trigger enforcement; do not weaken Python-side fail-closed continuity gating (`continuity.sync_sql_gate`, `continuity.gate_hold`, `Assistants.suspended`, `Assistants._fence_in`); do not push to `origin`; do not fabricate operational OD-35 / OQ-017 human approvals (`Refs #122` retained).
* Criteria: Every codebase finding uses stable `C#` IDs with `path:line`; verifies exact `ledger` branching in `MssqlStore._create_schema_serialized` and `Assistants.migrate`; verifies zero-conflict base-branch integration preserving `is_available_case_document`; defines deterministic local SQLite dialect test coverage simulating `SELECT is_ledger_on -> 1` without requiring live SQL Server container availability during unit test discovery.
* Requested outputs: Convergence recommendation for `mssqlstore.py`, `assistants.py`, `src/core/README.md`, `src/api/tests/test_assistants.py`, and non-rewriting git merge strategy.
* Output mode: convergence

## Research Parameters

| Field                             | Value                                                                                                                                      |
|-----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)              | Q1-Q4 covering SQL Server ledger trigger prohibition, `continuity.sync_sql_gate` compatibility on updatable ledger tables, base-branch merge preservation of `#1781`, and local `DialectTests` verification |
| Codebase scope                    | `src/core/**`, `src/api/tests/**`, `.copilot-tracking/**/2026-11-15/issue-122-restart-gate-0228*`                                          |
| External scope                    | none (bounded internal repository and supplied CI failure trace)                                                                           |
| Initial internal candidate areas  | `src/core/src/zava_forward/core/mssqlstore.py`, `src/core/src/zava_forward/core/assistants.py`, `src/core/src/zava_forward/core/continuity.py`, `src/core/src/zava_forward/core/sqlstore.py`, `src/api/tests/test_assistants.py`, `src/api/tests/test_mssqlstore.py`, `src/core/README.md` |
| Initial external candidate areas  | none                                                                                                                                       |
| Research posture                  | focused                                                                                                                                    |
| Posture provenance                | caller-supplied exact CI failure (`job 132785382777`) and bounded file targets                                                             |
| Explicit limits / deadline        | Local worktree `/home/azureuser/source/ama-demo-wt/feat-122-restart-gate` (`feat/platform-122-restart-gate-0228`); no `git push`           |
| Posture-specific completion basis | All four questions answered with direct codebase and git-object evidence; contrarian checks completed                                      |
| Edits allowed during research?    | no, research-only                                                                                                                          |
| Resolved evidence root            | `.copilot-tracking/`                                                                                                                       |
| Known constraints / excluded sources | Preserve `ruff.format` exclusion boundaries in `src/core/pyproject.toml` and `src/api/pyproject.toml`; never rewrite published branch history silently |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                         | Match and provenance                          | Scoped authority or output contract                                              | Selected / skipped reason                                                                                  |
|---------------------|-----------------------------------|-----------------------------------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` repository custom instruction | Branch/merge safeguards, validation commands, `Refs #122`, privacy-safe author   | Selected: governs focused validation tier, non-rewriting merge on published PR head, and commit conventions |
| Skill               | `rpi-research`                    | Active Phase 1 RPI skill                      | Read-only three-wave research artifact, `Planning Readiness`, and `disposition`  | Selected: active phase skill                                                                               |
| Research specialist | `hve-core-all:rpi-researcher`     | Host subagent for independent lanes           | Subagent lane artifact under `.copilot-tracking/research/subagents/`             | Skipped (inline preferred): tightly coupled two-file trigger guard and single test harness                 |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                  | Answers / unanswered | Resulting decision or selected further research                                                  |
|------------------|------------------------------------------------------------------------------------------------------------------------|----------------------|--------------------------------------------------------------------------------------------------|
| Intake           | Non-interactive session with exact CI failure details, named line ranges, base-branch preservation contract, and tests | n/a (autonomous)     | Execute single focused three-wave cycle in `convergence` mode.                                   |
| Direction change | None.                                                                                                                  | n/a                  | Retain initial focused scope.                                                                    |
| Convergence      | All questions Q1-Q4 resolved with codebase and `git merge-tree` evidence (`C1`-`C10`).                                 | n/a (autonomous)     | Selected non-rewriting `git merge` of `origin/feat/demo-164-chat-grounding-provenance-0900` plus ledger trigger guards and `DialectTests` ledger verification (`Planning Readiness: Ready`). |

## Scope and Success Criteria

* Scope: Guarding SQL Server DML trigger creation when `SELECT is_ledger_on` returns `1` in `mssqlstore.py` and `assistants.py`, preserving `continuity.sync_sql_gate` synchronization, merging `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) to keep `is_available_case_document`, adding unit coverage in `src/api/tests/test_assistants.py`, and updating `src/core/README.md`.
* Assumptions (verified):
  * Local branch `feat/platform-122-restart-gate-0228` at `d0d4135d3` is the exact published head of `PR #1787` (`refs/pull/1787/head`).
  * `origin/feat/demo-164-chat-grounding-provenance-0900` (`refs/pull/1641/head`) is now at `c7e5c8848` (incorporating `#1785` and `#1781`, superseding the earlier `e088f278a` SHA referenced before stack advancement while containing the identical `#1781` `doc_controls.is_available_case_document` commit).

## Prior Knowledge and Decomposed Questions

* Prior artifacts `.copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-research.md` and `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-c2-changes.md` introduced `GATE_TRIGGERS` in `mssqlstore.py` and `MSSQL_ATTEMPT_TRIGGERS` / `SQLITE_ATTEMPT_TRIGGERS` in `assistants.py`.
* Questions:
  * Q1: Why did `MssqlLedgerMigration` (`5` tests) and `MssqlLedgerTests` (`2` tests) fail in CI job `132785382777`, and how do `MssqlStore._create_schema_serialized` and `Assistants.migrate` currently branch on `ledger`?
  * Q2: When DML triggers are skipped on `WITH LEDGER = ON` SQL Server databases, do `continuity_gate_state` and `continuity_open_holds` DDL and `continuity.sync_sql_gate` DML remain valid on system-versioned updatable ledger tables, and do Python fail-closed fences still hold?
  * Q3: Should we merge or rebase `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`), and does `is_available_case_document(d)` merge cleanly and pass existing `#122` tests?
  * Q4: How can `DialectTests` in `src/api/tests/test_assistants.py` deterministically verify both `MssqlStore._create_schema_serialized` and `Assistants.migrate` under `SELECT is_ledger_on -> 1` without a live SQL Server container?

## Cycle 1 Execution

### Wave 1: Wider

* Inspected `mssqlstore.py`, `assistants.py`, `sqlstore.py`, `continuity.py`, `test_mssqlstore.py`, `test_assistants.py`, `src/core/README.md`, `src/core/pyproject.toml`, `src/api/pyproject.toml`, and git refs (`HEAD`, `refs/pull/1787/head`, `origin/feat/demo-164-chat-grounding-provenance-0900`).

### Wave 2: Deeper

* **C1** (`src/core/src/zava_forward/core/mssqlstore.py:307-321`): `MssqlStore._create_schema_serialized` computes `ledger = bool(row and row[0])` from `LEDGER_DB` (`SELECT is_ledger_on FROM sys.databases WHERE name = DB_NAME()`), executes `TABLES` (with `LEDGER_CLAUSE` only on `LEDGER_APPEND_ONLY_TABLES`), verifies `APPEND_ONLY_LEDGER_TABLE` when `if ledger:`, executes `self.db.execute(APPEND_ONLY)` in `else:`, and then unconditionally runs `for trigger in GATE_TRIGGERS: self.db.execute(trigger)` at lines 320-321.
* **C2** (`src/core/src/zava_forward/core/assistants.py:1214-1255`): `Assistants.migrate` checks `if self.mssql:` and computes `ledger = bool(row and row[0])` inside that `if` block (`ledger` is unbound when `self.mssql` is `False`). Inside `if self.mssql:`, `if ledger:` verifies `assistant_events` is `APPEND_ONLY_LEDGER_TABLE` while `else:` installs `assistant_events_immutable`. After `self._upgrade(db)` (line 1241), lines 1242-1243 unconditionally execute `for trigger in (MSSQL_ATTEMPT_TRIGGERS if self.mssql else SQLITE_ATTEMPT_TRIGGERS): db.execute(trigger)`, followed by `continuity.sync_sql_gate(db, read_meta=True, mssql=self.mssql)` at line 1244.
* **C3** (`src/api/tests/test_mssqlstore.py:181-225` and `src/api/tests/test_assistants.py:1357-1404`): `MssqlLedgerMigration` (`5` tests) and `MssqlLedgerTests` (`2` tests) create fresh SQL Server 2022 databases with `CREATE DATABASE [{name}] WITH LEDGER = ON`. In SQL Server 2022, every table created without `APPEND_ONLY = ON` inside a `WITH LEDGER = ON` database becomes a system-versioned `UPDATABLE_LEDGER_TABLE`, on which `CREATE OR ALTER TRIGGER` raises `[Microsoft][SQL Server]Cannot create a trigger on a system-versioned ledger table`.
* **C4** (`src/core/src/zava_forward/core/continuity.py:216-248` and `src/core/src/zava_forward/core/sqlstore.py:324-330`): `SqlStore._migrate()` calls `self._create_schema()` and then `continuity.sync_sql_gate(self.db, read_meta=True, mssql=hasattr(self, "_env"))`. `sync_sql_gate` uses standard `SELECT`, `INSERT`, `UPDATE`, and `DELETE` statements (no `TRUNCATE TABLE`), all of which are supported on SQL Server `UPDATABLE_LEDGER_TABLE` tables (`continuity_gate_state` and `continuity_open_holds`).
* **C5** (`src/api/tests/test_assistants.py:1292-1345`): `DialectConnection` translates T-SQL migration probes and DDL so `Assistants(self.store, config())` runs `self.mssql = True` migrations against SQLite in `DialectTests.test_mssql_dialect_translation_runs_in_transaction_and_claims`. Currently line 1301 hardcodes `if "SELECT is_ledger_on" in sql: return self.raw.execute("SELECT 0")`.
* **C6** (`src/core/pyproject.toml:30-42` and `src/api/pyproject.toml:30-44`): Both `mssqlstore.py` / `assistants.py` and `test_assistants.py` are listed in `[tool.ruff.format].exclude`, so edits must preserve existing file formatting and pass `python3 -m ruff check src/core src/api`.
* **C7** (`src/core/README.md:4605-4613`): Documents `continuity_gate_state` and `assistant_attempts` / `assistant_tasks` SQL triggers; updating this bullet clarifies that DML triggers apply to SQLite and non-ledger SQL Server databases, whereas `WITH LEDGER = ON` SQL Server databases omit DML triggers (forbidden on system-versioned ledger tables) while maintaining `continuity_gate_state` / `continuity_open_holds` synchronization and Python fail-closed fences.

### Wave 3: Contrarian

* **C8** (Git branch lineage and merge vs. rebase check): `HEAD` (`d0d4135d3`) equals `refs/pull/1787/head` on `origin/feat/platform-122-restart-gate-0228`. Rebasing onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) would rewrite published PR commit history and require a force-push, conflicting with `.github/copilot-instructions.md` ("never silently rebase, force-push, rewrite or merge work merely to manage branch lineage"). By contrast, `git merge-tree --write-tree HEAD origin/feat/demo-164-chat-grounding-provenance-0900` succeeded with exit code `0` (`2da3ef2acac94893dc32b4566409c2c0175852a4`) and zero conflicts, cleanly combining `from .doc_controls import is_available_case_document` and `if d.get("kind") in kinds and is_available_case_document(d)` in `assistants.py:capture()` with all `#122` restart-gate changes while preserving fast-forward push compatibility.
* **C9** (Contrarian check on `ledger` variable binding in `Assistants.migrate`, `src/core/src/zava_forward/core/assistants.py:1214-1243`): If `if not (self.mssql and ledger):` were written without initializing `ledger = False` before `if self.mssql:`, Python short-circuit evaluation (`False and ledger`) would skip evaluating `ledger` on SQLite at runtime, **but** `mypy` in `src/core` (`possibly-undefined` / variable narrowing) could flag `ledger` or trip future refactors. Initializing `ledger = False` at the top of `migrate()` eliminates any unbound-local risk cleanly.
* **C10** (Contrarian check on `MssqlStore._create_schema_serialized` testing via `DialectConnection`): `MssqlStore.TABLES` (`src/core/src/zava_forward/core/mssqlstore.py:21-72`) uses `IDENTITY(1,1)`, `N'...'` string literals (in `audit`), and `WITH (LEDGER = ON (APPEND_ONLY = ON))` when `ledger=True`, plus `LEDGER_TYPE` (`SELECT ledger_type_desc ...`). Extending `DialectConnection` with `ledger: bool = False` so that `SELECT is_ledger_on` returns `1`, `SELECT ledger_type_desc` returns `'APPEND_ONLY_LEDGER_TABLE'`, `CREATE TRIGGER` raises `sqlite3.OperationalError("Cannot create a trigger on a system-versioned ledger table")` when `ledger=True`, and `IF OBJECT_ID` strips `WITH (LEDGER = ON (APPEND_ONLY = ON))`, `IDENTITY(1,1)`, and `N'` prefixes lets `DialectTests` execute the real `MssqlStore._create_schema_serialized` and `Assistants.migrate` paths end-to-end against SQLite!

## Parent Synthesis and Convergence

* **Accepted recommendation**:
  1. Merge `origin/feat/demo-164-chat-grounding-provenance-0900` (`c7e5c8848`) into `feat/platform-122-restart-gate-0228` without rewriting pushed history (`d0d4135d3`), preserving `is_available_case_document` in `src/core/src/zava_forward/core/assistants.py`.
  2. In `src/core/src/zava_forward/core/mssqlstore.py:_create_schema_serialized`, move `for trigger in GATE_TRIGGERS: self.db.execute(trigger)` inside the `else:` branch of `if ledger:`.
  3. In `src/core/src/zava_forward/core/assistants.py:migrate`, initialize `ledger = False` before `if self.mssql:` and guard trigger execution with `if not (self.mssql and ledger):` while keeping `continuity.sync_sql_gate(db, read_meta=True, mssql=self.mssql)` unconditional.
  4. Extend `DialectConnection` (`ledger=False`) and add `test_mssql_ledger_mode_skips_triggers_and_syncs_continuity_gate` in `src/api/tests/test_assistants.py` (`DialectTests`) verifying both `MssqlStore._create_schema_serialized` (with `continuity.sync_sql_gate`) and `Assistants.migrate` execute zero `CREATE TRIGGER` statements when `SELECT is_ledger_on` returns `1` while synchronizing `continuity_gate_state` and `continuity_open_holds`.
  5. Update `src/core/README.md` (`4605-4613`) to document the `WITH LEDGER = ON` trigger omission alongside preserved `sync_sql_gate` and Python fail-closed fences.
* **Rejected alternatives**:
  * Rebasing `feat/platform-122-restart-gate-0228` onto `origin/feat/demo-164-chat-grounding-provenance-0900`: rejected because `d0d4135d3` is already published on `PR #1787` and rewriting history would require force-push (`C8`).
  * Catching and ignoring `CREATE TRIGGER` exceptions in SQL Server: rejected because silent DDL error suppression in a `SERIALIZABLE` schema transaction can doom the T-SQL transaction (`XACT_STATE() = -1`) and mask real non-ledger trigger errors.
* **Risks and open items**:
  * Live SQL Server container tests (`MssqlLedgerMigration`, `MssqlLedgerTests`) skip locally unless `ZF_MSSQL_TEST_DSN` is set; hosted `Source projects CI` runs them against SQL Server 2022, while our `DialectTests` ledger unit test enforces the exact SQL statement and `CREATE TRIGGER` prohibition locally on every test run.
* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`
