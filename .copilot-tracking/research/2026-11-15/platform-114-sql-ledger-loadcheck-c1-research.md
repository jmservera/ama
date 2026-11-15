---
description: "Primary evidence artifact for Issue #114 c1 CI correction making SqlStoreTests pre-reliance tests backend-agnostic across SQLite and SQL Server"
---
<!-- markdownlint-disable-file -->

# Task Research: platform-114-sql-ledger-loadcheck-c1

| Field              | Value                                                                                          |
|--------------------|------------------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                                     |
| Researcher / agent | RPI Agent (`rpi-research`)                                                                     |
| Status             | Complete                                                                                       |
| Artifact path      | .copilot-tracking/research/2026-11-15/platform-114-sql-ledger-loadcheck-c1-research.md         |

## Research Brief

* What to research: Exact runtime mechanics of `MssqlStoreTests(base.SqlStoreTests)` in `src/api/tests/test_mssqlstore.py` during the `mssql` CI job in `.github/workflows/src-ci.yml`, why all three `test_pre_reliance_*` methods in `src/core/tests/test_sqlstore.py` failed on `PR #1814`, and how to make them backend-agnostic across SQLite (`SqlStore`) and SQL Server (`MssqlStore`) while adding an offline unit check that exercises the `MssqlStoreTests` factory-patching pattern without requiring a live SQL Server container.
* Why it matters: `MssqlStoreTests` replays `SqlStoreTests` against a disposable SQL Server 2022 container by patching `test_sqlstore.SqlStore = factory`. Direct `sqlite3.connect(self.db)` calls, SQLite-only trigger names, explicit `seq` identity inserts, secondary `s2` store creation without `wipe()`, and referencing the patched global `SqlStore` in `issubclass(...)` break `mssql` CI on `PR #1814`.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, `rpi-review`, and branch verification for `PR #1814`.
* Scope: `src/core/tests/test_sqlstore.py` (edit target) and read-only evidence across `src/api/tests/test_mssqlstore.py`, `src/core/src/zava_forward/core/{sqlstore,mssqlstore,store,ledger}.py`, `src/core/pyproject.toml`, and `.github/workflows/src-ci.yml`.
* Non-goals: Modifying `src/api/tests/test_mssqlstore.py` or production `src/core/src/` code, running `tools/rpi-checks.py --all`, pushing to remote, or opening/updating a PR.
* Criteria: All three `test_pre_reliance_*` methods in `SqlStoreTests` pass against both `SqlStore` (SQLite) and `MssqlStore` (SQL Server `factory` hook), no `sqlite3.connect(self.db)` or SQLite-only DDL is sent to `MssqlStore`, `issubclass(MssqlStore, BaseSqlStore)` survives `test_sqlstore.SqlStore = factory`, an offline unit check simulates `test_sqlstore.SqlStore = lambda data, db, *a, **k: ...` to guard against regressions, and focused `src/core` checks (`test_sqlstore.py`, `test_loadcheck.py`, `ruff check`, `mypy`) pass cleanly.
* Requested outputs: Converged backend-agnostic test design with `path:line` codebase evidence (`C1`–`C10`) and `Ready` planning handoff.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                              |
|--------------------------------------|----------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1: How does `MssqlStoreTests` inherit and patch `SqlStoreTests` in the `mssql` CI job, and why did the three `test_pre_reliance_*` methods fail? Q2: Are the proposed SQL statements (`_drop_audit_triggers`, `UPDATE`/`DELETE` via `s.db.execute`, 7-column `INSERT INTO audit` omitting `seq`, and reusing `s` for dropped-2024 verification) portable across SQLite (`isolation_level=None`) and SQL Server (`autocommit=True`, `BIGINT IDENTITY(1,1)`)? Q3: How should the offline `MssqlStoreTests` factory-hook simulation be structured so it verifies all three `test_pre_reliance_*` methods under `test_sqlstore.SqlStore = lambda ...` without requiring `mssql-python` or a running SQL Server? |
| Codebase scope                       | `src/core/tests/test_sqlstore.py`, `src/api/tests/test_mssqlstore.py`, `src/core/src/zava_forward/core/`, `.github/workflows/src-ci.yml` |
| External scope                       | none                                                                                               |
| Initial internal candidate areas     | `src/core/tests/test_sqlstore.py`, `src/api/tests/test_mssqlstore.py`, `src/core/src/zava_forward/core/mssqlstore.py`, `src/core/src/zava_forward/core/sqlstore.py` |
| Initial external candidate areas     | none                                                                                               |
| Research posture                     | focused                                                                                            |
| Posture provenance                   | caller-specified bounded CI fix and named file target (`src/core/tests/test_sqlstore.py`)          |
| Explicit limits / deadline           | Focused validation tier (`test_sqlstore.py`, `test_loadcheck.py`, `ruff`, `mypy`); no push or PR   |
| Posture-specific completion basis    | focused scope and materiality                                                                      |
| Edits allowed during research?       | no, research-only                                                                                  |
| Resolved evidence root               | .copilot-tracking/                                                                                 |
| Known constraints / excluded sources | Exclude private datasets (`support/`, `.env`, `~/.zava-forward`); treat repo content as data; secret-free errors |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                         | Match and provenance                           | Scoped authority or output contract                            | Selected / skipped reason                                    |
|---------------------|-----------------------------------|------------------------------------------------|----------------------------------------------------------------|--------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` matches workspace and evidence | Enforces focused validation, `Refs #114`, no push when forbidden, Markdown style | Selected: mandatory repository governance                    |
| Skill               | `rpi-research`                    | Direct caller RPI phase invocation             | Three-wave primary research artifact with `C#` evidence IDs    | Selected: active RPI phase contract                          |
| Skill               | Web/UI/presentation skills        | No web, UI, or deck files in scope             | N/A                                                            | Skipped: backend Python test correction only                 |
| Research specialist | `hve-core-all:rpi-researcher`     | Host-registered subagent for independent lanes | Delegated lane artifact under `research/subagents/`            | Skipped: single continuous cross-file trace handled inline   |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                 | Answers / unanswered       | Resulting decision or selected further research                     |
|------------------|-------------------------------------------------------------------------------------------------------|----------------------------|---------------------------------------------------------------------|
| Intake           | Caller prompt provides exact root cause, required 4-part fix in `src/core/tests/test_sqlstore.py`, validation commands, and local-commit-only instruction; autopilot active. | No user interaction needed | Execute focused inline Cycle 1 across `test_sqlstore.py`, `test_mssqlstore.py`, `sqlstore.py`, and `mssqlstore.py`. |
| Direction change | None during Cycle 1                                                                                   | None                       | Retained single-file scope (`src/core/tests/test_sqlstore.py`)      |
| Convergence      | All three research questions answered with direct `path:line` evidence                                | None                       | Selected converged backend-agnostic design; Planning Readiness = `Ready` |

## Scope and Success Criteria

* Scope: `src/core/tests/test_sqlstore.py` only for implementation, verified against `SqlStore`, `MssqlStore`, and `MssqlStoreTests` contracts.
* Assumptions to verify:
  * Both `SqlStore.db` and `MssqlStore.db` (`_Conn`) operate in autocommit mode outside `BEGIN IMMEDIATE`, so `s.db.execute(...)` commits immediately without `raw.commit()`.
  * Reusing `s` after `DELETE FROM audit` produces valid auto-generated `seq` values (`7, 8, 9`) accepted by both `s.verify_audit()` and `s._reliance_audit_snapshot()`.
  * `MssqlStoreTests` runs against SQL Server `master` (`is_ledger_on == 0`), where `audit_append_only` is an `INSTEAD OF UPDATE, DELETE` trigger.
* Success criteria:
  * Every research question is answered with `path:line` `C#` evidence.
  * Wave 1 (Wider), Wave 2 (Deeper), and Wave 3 (Contrarian) completed in order.
  * Contrarian checks verify there are no hidden T-SQL, `seq` ordering, `digest_dir`, or infinite-recursion traps in the simulated factory hook.
  * Artifact self-check passes.

## Task Research Requests

* Explicit requests: Make `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years`, `test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head`, and `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` in `src/core/tests/test_sqlstore.py` backend-agnostic via `_drop_audit_triggers`, `s.db.execute(...)`, reusing `s` with 7-column `INSERT INTO audit` (omitting `seq`), `BaseSqlStore` import alias, and a unit check simulating `MssqlStoreTests` patching `test_sqlstore.SqlStore = lambda data, db, *a, **k: ...`.
* Inferred research questions: Does any other test file subclass `SqlStoreTests`? How does `MssqlStoreTests` handle `SqlStore` restoration, `wipe()`, and `digest_dir`? How should the offline factory-hook simulation work when `mssql-python` is not installed in `src/core` dev/CI environments?
* Caller constraints and non-goals: Edit `src/core/tests/test_sqlstore.py` only; run focused validation; commit locally with Copilot trailer; do not push or open a PR.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                 | Source / checkpoint | Effect on active brief, evidence, or revalidation           |
|----------------------------------------------------------|---------------------------------------------------------------------------------------|---------------------|-------------------------------------------------------------|
| narrow                                                   | Scope code changes strictly to `src/core/tests/test_sqlstore.py`                      | User intake prompt  | Keeps production `src/core/src/` and `src/api/tests/` untouched |
| exclude                                                  | Do not push to remote, do not open/update a PR, and do not run `rpi-checks.py --all`  | User intake prompt  | Focused validation tier and clean local commit on branch    |

## Research Questions

|  # | Sub-question | Type (depth / breadth / straightforward) | Priority | Status   |
|---:|--------------|------------------------------------------|----------|----------|
| Q1 | Which test suites import or subclass `SqlStoreTests`, and how does `MssqlStoreTests` configure `test_sqlstore.SqlStore` and the SQL Server test database in CI? | breadth | H | answered |
| Q2 | How do `SqlStore` and `MssqlStore` handle autocommit, trigger names, `audit.seq` auto-numbering after `DELETE FROM audit`, `digest_dir`, and `_reliance_audit_snapshot()`? | depth | H | answered |
| Q3 | How can an offline unit check faithfully simulate `MssqlStoreTests` patching `test_sqlstore.SqlStore = lambda data, db, *a, **k: ...` (including `isinstance(store, MssqlStore)` and non-existent `self.db`) without `mssql-python` or infinite recursion? | depth | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-15/platform-114-sql-ledger-loadcheck-research.md`, `.copilot-tracking/plans/2026-11-15/platform-114-sql-ledger-loadcheck-plan.md`, `.copilot-tracking/reviews/logs/2026-11-15/platform-114-sql-ledger-loadcheck-review.md`
* Reused (verified) findings: `SqlStore._reliance_audit_snapshot` (`sqlstore.py:1493`) validates `audit_head` (`id=1`) and monotonic `seq >= 1` (`seq > prev_seq`, not dense `1..N`), and `Store._reliance_db_errors` (`store.py:224`) safely catches `ImportError` when `MssqlStore.dberror` is accessed without `mssql_python`.
* Superseded / stale: The parent task's `test_sqlstore.py` tamper helpers assumed `self.db` was always a populated SQLite database and `test_sqlstore.SqlStore` remained a class; `PR #1814` `mssql` CI disproved that assumption because `MssqlStoreTests` subclasses `SqlStoreTests` with `base.SqlStore = factory`.

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow to `src/core/tests/test_sqlstore.py`; exclude push/PR and full gate
* Active research posture and completion basis: focused; focused scope and materiality
* Explicit limits or deadline effect: Focused validation tier (`src/core` unit tests, `ruff`, `mypy`)

#### Wave 1: Wider

* Plan and independent lanes: Search all references to `SqlStoreTests` and `test_sqlstore` across `src/` and `.github/workflows/` to find every subclass, monkeypatch, and CI job invoking `test_sqlstore.py`.
* Worker evidence relationships or inline fallback: inline (tightly coupled 4-file trace); `Q1 -> MssqlStoreTests is the sole subclass of SqlStoreTests and runs against SQL Server 2022 master in src-ci.yml -> C1, C2, C3`.
* Reflection: `MssqlStoreTests` in `src/api/tests/test_mssqlstore.py:596` is the only subclass of `SqlStoreTests` (`test_chat_panel.py`, `test_chat_privacy.py`, `test_chat_memory.py`, `test_chatthreads.py`, and `test_timecapture.py` only call `base.seed`). In `.github/workflows/src-ci.yml:301-323`, the `mssql` job runs `MssqlStoreTests` against `ZF_SQL_DATABASE=master` on `mcr.microsoft.com/mssql/server:2022-latest`.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Inspect `test_sqlstore.py:113-227`, `test_mssqlstore.py:42-57,595-617`, `mssqlstore.py:49-78,137-225,274-288`, `sqlstore.py:89-99,181-225,1493-1555`, and `ledger.py:85-113`.
* Plan and independent lanes: Verify autocommit semantics, trigger DDL, `IDENTITY(1,1)` vs `AUTOINCREMENT` numbering after `DELETE FROM audit`, `digest_dir` path resolution, and `BaseSqlStore` class resolution.
* Worker evidence relationships or inline fallback: inline; `Q2 -> Both SqlStore and MssqlStore autocommit single statements, use distinct trigger names, auto-generate strictly increasing seq >= 1 when seq is omitted, and keep sealed 2024/2025 digests in s.digest_dir -> C4, C5, C6, C7, C8, C9`.
* Reflection:
  1. `SqlStore._open` opens SQLite with `isolation_level=None` (`C6`), and `MssqlStore._Conn._connect` opens `mssql_python` with `autocommit=True` (`C5`). Therefore `s.db.execute(...)` commits each `DROP TRIGGER`, `UPDATE`, `DELETE`, and `INSERT` immediately on both backends.
  2. On SQL Server `master`, `is_ledger_on` is `0`, so `MssqlStore._create_schema_serialized` creates `audit_append_only` (`C4`), whereas `SqlStore` creates `audit_no_update` and `audit_no_delete` (`C6`). `_drop_audit_triggers` branching on `isinstance(store, MssqlStore)` matches `wipe()` in `test_mssqlstore.py:47-48` (`C2`).
  3. Reusing `s` directly for the dropped-2024 check also fixes a second SQL Server hazard: `MssqlStoreTests.setUp` calls `wipe()` once per test method (`C2`), so opening a second `s2 = SqlStore(self.data, db2)` inside the same test method on SQL Server would reuse the same `master` tables (already containing tampered rows) and the same `os.path.dirname(db)/digests` directory (`C5`, `C6`). Reusing `s` after `s.db.execute("DELETE FROM audit")` with 7-column `INSERT INTO audit (at, who, action, case_id, detail, prev, hash) VALUES (?,?,?,?,?,?,?)` lets both SQLite `AUTOINCREMENT` and SQL Server `BIGINT IDENTITY(1,1)` assign strictly increasing `seq` (`7, 8, 9`), which satisfies `SqlStore._reliance_audit_snapshot` (`seq >= 1` and `seq > prev_seq`, `C7`) and `s.verify_audit() == True` while `s.verify_ledger_before_reliance(current_year=2026)` detects `missing_years == ["2024"]` and `missing_audit_year` against the already-sealed `year-2024.json` in `s.digest_dir` (`C9`).

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge the offline `MssqlStoreTests` factory-hook simulation (`Q3`) for three potential pitfalls: (a) missing `mssql_python` package in offline `src/core` test environments (`C10`), (b) accidental mutation of `test_sqlstore.SqlStore` or infinite recursion if `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` runs under `MssqlStoreTests` on real SQL Server in CI, and (c) permissive SQLite fallback that fails to catch T-SQL/SQLite trigger mismatches or explicit `seq` inserts.
* Plan and independent lanes: Analyze MRO, `patch.dict` restoration, re-entrancy guards, and SQL guard assertions on a SQLite-backed `MssqlStore` test double.
* Worker evidence relationships or inline fallback: inline; `Q3 -> A SQLite-backed _MssqlFactoryStore(MssqlStore) double wrapped with an SQL guard and scoped via patch.dict(globals(), {"SqlStore": ...}) + re-entrancy guard safely tests both SqlStoreTests and MssqlStoreTests -> C4, C5, C8, C10`.
* Reflection:
  1. Because `src/core` CI runs without `mssql-python` (`C10`), `_MssqlFactoryStore(MssqlStore)` can delegate storage hooks (`_open`, `_create_schema`, `_create_indexes`, `_columns`, `_has_rec_order`, `_create_rec_order_index`, `_meta_set`, `_insert_ignore`, `_priority_correction_rows`, `_epoch_sql`, `_add_column_default`, `_contains`, `_limit`, and `dberror = sqlite3.Error`) to `BaseSqlStore` while keeping `isinstance(store, MssqlStore) is True` and storing its SQLite file at `os.path.join(os.path.dirname(db), "mssql-hook.sqlite")` so `db` (`pw.sqlite`) is never created on disk!
  2. Wrapping `store.db` in a tiny `_MssqlSqlGuard` that translates `"IF OBJECT_ID(N'audit_append_only', N'TR') IS NOT NULL DROP TRIGGER audit_append_only"` into dropping the two SQLite triggers — while raising `AssertionError` if `audit_no_update` / `audit_no_delete` or an explicit `seq` `INSERT INTO audit` is ever executed — proves offline that `_drop_audit_triggers` took the `isinstance(store, MssqlStore)` T-SQL path and that no SQLite-only DDL or identity-column insert remains.
  3. Scoping the hook with `with patch.dict(globals(), {"SqlStore": hook_factory}):` restores `globals()["SqlStore"]` cleanly whether it started as `BaseSqlStore` (in `SqlStoreTests`) or `test_mssqlstore.factory` (in `MssqlStoreTests`), and guarding the simulation block with `if not getattr(self, "_running_factory_hook", False):` prevents recursion while replaying all three `test_pre_reliance_*` methods in isolated temp directories!

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|----------------------------|
| Add `_drop_audit_triggers(self, store)` branching on `isinstance(store, MssqlStore)` | `C2`, `C4`, `C6`, `C8` | accepted | Matches T-SQL `audit_append_only` on `MssqlStore` and SQLite `audit_no_update` / `audit_no_delete` on `SqlStore` | Selected recommendation (Part 1) |
| Replace `sqlite3.connect(self.db)` with `s.db.execute(...)`, reuse `s` for dropped-2024 check, and omit `seq` in `INSERT INTO audit` | `C2`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9` | accepted | Avoids uninitialized `pw.sqlite`, SQL Server `IDENTITY_INSERT` failure, and shared-DB `s2` collision on `MssqlStoreTests` | Selected recommendation (Parts 2 & 3) |
| Alias `from zava_forward.core.sqlstore import SqlStore as BaseSqlStore` and replay all three `test_pre_reliance_*` methods under a guarded `SqlStore = lambda ...` `MssqlStore` factory simulation | `C2`, `C4`, `C5`, `C8`, `C10` | accepted | Prevents `TypeError: issubclass() arg 2 must be a class` under `MssqlStoreTests` and catches SQLite-only regressions offline without `mssql-python` | Selected recommendation (Part 4) |
| Edit `src/api/tests/test_mssqlstore.py` to override `test_pre_reliance_*` | `C2`, `C8` | rejected | Duplicating three tests in `test_mssqlstore.py` violates caller scope (`src/core/tests/test_sqlstore.py`) and leaves `SqlStoreTests` non-portable | Recorded as rejected alternative |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: All questions (`Q1`–`Q3`) answered with direct `path:line` evidence and contrarian checks resolved within focused scope.
* Revised brief or revalidation required: none
* Readiness effect: `Ready` (`C1`–`C10`)

## Evidence Log

* Delegation: inline: single tightly coupled cross-file trace across `test_sqlstore.py`, `test_mssqlstore.py`, `sqlstore.py`, and `mssqlstore.py` completed in <= 5 targeted reads.

### Codebase Evidence

| ID   | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|------|-----------------|------------------------|------|------------|-------|
| `C1` | Only `MssqlStoreTests` subclasses `SqlStoreTests` across the repository; other importers only use `test_sqlstore.seed`. | `src/api/tests/test_mssqlstore.py:596` | grep / view | high | Swept `SqlStoreTests\|test_sqlstore` across `src/` |
| `C2` | `MssqlStoreTests.setUpClass` swaps `base.SqlStore = factory` (where `factory(data, db, *a, **k)` returns `MssqlStore(data, state_dir=os.path.dirname(db))`), and `wipe()` runs once per test in `setUp()` dropping `audit_append_only` via `IF OBJECT_ID(N'audit_append_only', N'TR') IS NOT NULL DROP TRIGGER audit_append_only`. | `src/api/tests/test_mssqlstore.py:47` | view | high | Lines `42-57` and `595-617` |
| `C3` | The `mssql` job in `Source projects CI` executes `test_mssqlstore` against `mcr.microsoft.com/mssql/server:2022-latest` with `ZF_SQL_DATABASE=master` (non-ledger system DB where trigger `audit_append_only` is active). | `.github/workflows/src-ci.yml:301` | grep / view | high | Lines `301-323` |
| `C4` | `MssqlStore` defines `audit.seq` as `BIGINT IDENTITY(1,1) PRIMARY KEY` and creates `TRIGGER audit_append_only ON audit INSTEAD OF UPDATE, DELETE` when `is_ledger_on` is `0`. | `src/core/src/zava_forward/core/mssqlstore.py:49` | view | high | Lines `49-51`, `77-78`, `274-288` |
| `C5` | `MssqlStore._Conn._connect` sets `autocommit=True` and `MssqlStore.__init__` passes `os.path.join(state_dir, "mssql")` to `SqlStore.__init__`, placing `digest_dir` at `os.path.join(state_dir, "digests")` without creating `pw.sqlite`. | `src/core/src/zava_forward/core/mssqlstore.py:139` | view | high | Lines `139-140`, `217-219` |
| `C6` | `SqlStore._open` connects `sqlite3` with `isolation_level=None` (autocommit), defines `audit.seq INTEGER PRIMARY KEY AUTOINCREMENT`, and creates `audit_no_update` and `audit_no_delete` triggers. | `src/core/src/zava_forward/core/sqlstore.py:93` | view | high | Lines `93-99`, `187`, `221-225` |
| `C7` | `SqlStore._reliance_audit_snapshot` requires `type(seq) is int and seq >= 1 and seq > prev_seq` (strictly increasing, not dense `1..N`), so auto-generated sequences `7, 8, 9` after `DELETE FROM audit` are valid on both SQLite and SQL Server. | `src/core/src/zava_forward/core/sqlstore.py:1525` | view | high | Lines `1493-1555` |
| `C8` | In `src/core/tests/test_sqlstore.py`, lines `147-180` and `192-203` open `sqlite3.connect(self.db)` and run SQLite-only `DROP TRIGGER` + 8-column `INSERT INTO audit VALUES (...)`, while line `209` calls `issubclass(MssqlStore, SqlStore)` against the monkeypatched module global `SqlStore`. | `src/core/tests/test_sqlstore.py:147` | view | high | Exact root cause of the 3 CI failures on `PR #1814` (`lines 133-241`) |
| `C9` | `ledger.verify_years` checks `missing = sorted(y for y in sealed if y not in by)` against sealed `year-YYYY.json` files, while `Store.verify_audit` checks only `verify_entries(..., read_digests(digest_dir))` (root digests), explaining why rewriting `2025`+`2026` from `GENESIS` after sealing `2024`+`2025` yields `verify_audit() == True` and `missing_years == ["2024"]`. | `src/core/src/zava_forward/core/ledger.py:111` | view | high | Lines `85-113` and `store.py:203-210` |
| `C10` | `src/core/pyproject.toml` marks `mssql_python` optional (`ignore_missing_imports = true`) and lists `tests/test_sqlstore.py` in `ruff.format.exclude` and `mypy` `ignore_errors`, while `ruff check` lints `src/core/tests/test_sqlstore.py` under `select = ["E", "F", "I", "B", "UP"]` with per-file ignores. | `src/core/pyproject.toml:34` | view | high | Lines `12-85` |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* none

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1       | `MssqlStoreTests` is the sole subclass of `SqlStoreTests`; in `src-ci.yml` (`mssql` job) it sets `test_sqlstore.SqlStore = factory` against SQL Server `master`, causing `sqlite3.connect(self.db)` and `issubclass(MssqlStore, SqlStore)` to fail. | `C1`, `C2`, `C3`, `C8` | high | Confirms fixing `src/core/tests/test_sqlstore.py` resolves all `PR #1814` `mssql` CI failures without touching `src/api`. |
| Q2       | Using `_drop_audit_triggers(self, s)`, `s.db.execute(...)` with `WHERE at=?`, reusing `s` after `DELETE FROM audit`, and omitting `seq` in 7-column `INSERT INTO audit` works identically on SQLite (`isolation_level=None`) and SQL Server (`autocommit=True`, `BIGINT IDENTITY(1,1)`). | `C2`, `C4`, `C5`, `C6`, `C7`, `C9` | high | Eliminates both SQLite-only trigger syntax and SQL Server shared-database / `IDENTITY_INSERT` hazards. |
| Q3       | Aliasing `SqlStore as BaseSqlStore` and replaying all three `test_pre_reliance_*` methods in isolated temp dirs under `patch.dict(globals(), {"SqlStore": lambda data, db, *a, **k: ...})` with a SQLite-backed `_MssqlFactoryStore(MssqlStore)` + `_MssqlSqlGuard` verifies the `MssqlStoreTests` hook offline without `mssql-python` or recursion. | `C2`, `C4`, `C5`, `C8`, `C10` | high | Provides deterministic offline regression protection in `src/core` unit tests while remaining safe when inherited by `MssqlStoreTests`. |

## Key Discoveries

* Reusing `s` directly for the dropped-2024 check in `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years` is essential on SQL Server not only to avoid `sqlite3.connect(db2)` but also because `MssqlStoreTests` wipes the single `master` database only in `setUp()` (`C2`), so a second `SqlStore(...)` call inside the same test method would attach to the already-populated SQL Server tables (`C5`).
* Omitting `seq` in `INSERT INTO audit (at, who, action, case_id, detail, prev, hash) VALUES (?,?,?,?,?,?,?)` avoids T-SQL `IDENTITY_INSERT` errors (`C4`) while producing strictly increasing `seq` values (`7, 8, 9`) accepted by `SqlStore._reliance_audit_snapshot` (`C7`).
* Importing `from zava_forward.core.sqlstore import LedgerRelianceError, SqlStore as BaseSqlStore` (while keeping `SqlStore = BaseSqlStore` as the module-level symbol that `MssqlStoreTests` patches) preserves full compatibility with `MssqlStoreTests.setUpClass` (`base.SqlStore = factory`, `C2`) and lets `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` always reference the true `BaseSqlStore` class (`C8`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Update `src/core/tests/test_sqlstore.py` with (1) `BaseSqlStore` class reference alongside patchable module-global `SqlStore = BaseSqlStore`, (2) `SqlStoreTests._drop_audit_triggers(self, store)` dispatching T-SQL `audit_append_only` vs SQLite `audit_no_update` / `audit_no_delete`, (3) backend-agnostic `s.db.execute(...)` mutations and single-store reuse with 7-column `INSERT INTO audit` in `test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years` and `test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head`, and (4) an offline `MssqlStoreTests` factory-hook check in `test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore` that patches `SqlStore = lambda data, db, *a, **k: ...` to a SQLite-backed `MssqlStore` double enforcing T-SQL trigger drop, no `pw.sqlite` access, and no explicit `seq` insert across all three `test_pre_reliance_*` methods.
* Rationale: Directly addresses both `PR #1814` root causes (`C8`), respects SQL Server `IDENTITY(1,1)` and single-DB `wipe()` semantics (`C2`, `C4`, `C7`), and proves the `MssqlStoreTests` hook offline in `src/core` (`C10`).
* Evidence refs: `C1`, `C2`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`
* Implementation impact: Single test file modified (`src/core/tests/test_sqlstore.py`).
* Confidence: high: all SQL statements and adapter paths are verified directly against `SqlStore` and `MssqlStore._Conn`.

File tree:

```text
src/core/tests/
└── test_sqlstore.py  (modified: backend-agnostic pre-reliance tests + MssqlStoreTests factory hook simulation)
```

### Alternative: Override the three `test_pre_reliance_*` methods in `src/api/tests/test_mssqlstore.py`

* Approach: Leave `src/core/tests/test_sqlstore.py` SQLite-specific and write three separate T-SQL overrides on `MssqlStoreTests` in `src/api/tests/test_mssqlstore.py` (similar to `test_ledger_is_append_only_and_detects_tampering`).
* Trade-offs: Avoids touching `test_sqlstore.py`, but duplicates ~80 lines of multi-year verification assertions across two packages and leaves `SqlStoreTests` coupled to `self.db` file paths despite `s.db.execute` already abstracting SQLite and T-SQL.
* Evidence refs: `C2`, `C5`, `C8`
* Rejection rationale: Violates explicit caller scope (`src/core/tests/test_sqlstore.py`) and misses single-source parity between `SqlStoreTests` and `MssqlStoreTests`.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Local environment does not run the GitHub Actions SQL Server 2022 service container during focused `src/core` unit tests; mitigated by verifying exact `MssqlStore._Conn` T-SQL compatibility (`C4`, `C5`) and replaying all three `test_pre_reliance_*` methods under a strict `MssqlStore` SQL-guard factory hook offline.
* Follow-up: Hosted `mssql` CI job verification on `PR #1814` once the owner/coordinator pushes the frozen commit; plus inherited parent follow-ups (`RV-001`/`RV-002` hardening and live Azure SQL / DH-005 Issue #114 operational gates).
* Residual uncertainty: none within offline `src/core` test scope.

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------|-----------|--------------|--------------|
| Make all three `test_pre_reliance_*` methods in `src/core/tests/test_sqlstore.py` backend-agnostic via `_drop_audit_triggers`, `s.db.execute`, single-store reuse, and 7-column `INSERT INTO audit` | confirmed | user / `C2`, `C4`, `C6`, `C7`, `C8` | Fixes SQLite-only `sqlite3.connect(self.db)` and trigger/identity incompatibilities on `MssqlStoreTests` | `C2`, `C4`, `C6`, `C7`, `C8` | Single-file edit in `src/core/tests/test_sqlstore.py` |
| Alias `BaseSqlStore` and verify `SqlStoreTests` pre-reliance methods under a simulated `SqlStore = lambda data, db, *a, **k: ...` `MssqlStore` factory hook | confirmed | user / `C2`, `C8`, `C10` | Fixes `issubclass` `TypeError` when `SqlStore` is patched to `factory` and guards against future SQLite-only regressions offline | `C2`, `C8`, `C10` | Runs in `test_sqlstore.py` without requiring `mssql-python` |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Hosted `mssql` CI job confirmation on `PR #1814` | Push frozen commit to `PR #1814` and observe GitHub Actions `mssql` job | Coordinator / owner (push excluded in this run) | Confirms live SQL Server 2022 container execution in CI | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L        | None needed for `c1` test fix | Focused scope fully covered | Only if `MssqlLedgerMigration` (`WITH LEDGER = ON`) ever subclasses `SqlStoreTests` (currently independent `unittest.TestCase`) | no | Q1, Q2; `C1`, `C2`, `C4` |

## Planning Readiness

* Status: Ready
* Decision state: Converged single-file test correction in `src/core/tests/test_sqlstore.py`
* Evidence basis: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`, `C9`, `C10`
* Preconditions met: Exact failure mechanisms verified (`C8`), T-SQL and SQLite statement parity verified (`C4`–`C7`, `C9`), offline `MssqlStore` factory simulation designed without external driver dependency (`C10`).
* Blockers: none
* Smallest action to change readiness: none

## Closeout Record

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                     |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian                                                                       |
| Lane evidence or inline fallback | inline fallback: tightly coupled 4-file inspection completed directly without subagent overhead               |
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`–`C10`)                                                                                           |
| Blockers                         | none                                                                                                         |
| Continuation owner and state     | confirmed automatic RPI Agent; automatic continuation to `rpi-plan`                                          |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`–`C10`)                                                                                           |
| Output mode and planning support | convergence; yes, single converged approach selected                                                         |
| Acting owner                     | confirmed automatic RPI Agent                                                                                |
| Required gates or confirmations  | Research disposition recorded (`passed`), Planning Readiness `Ready` (`passed`), three waves complete (`passed`), pre-transition state write (`passed`) |
| Continuation result              | automatic continuation to `rpi-plan`                                                                         |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/platform-114-sql-ledger-loadcheck-c1-research.md                       |
| Notes for planning or re-entry   | Keep implementation strictly in `src/core/tests/test_sqlstore.py`, guard factory-hook simulation with `patch.dict` + non-recursion flag so `MssqlStoreTests` also runs cleanly in CI, and run focused `src/core` checks. |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: Further research is immaterial because `MssqlStoreTests` is the sole subclass (`C1`) and every SQL statement and Python hook in the 4-part fix has been verified line-by-line against `SqlStore` and `MssqlStore` (`C2`–`C10`).

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry and Provenance, User Participation and Research Decisions, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings Mapped to Questions and Evidence, Key Discoveries, Alternatives and Decision State, Open Questions, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources.
