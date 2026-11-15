<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #122 Cycle 2 Remediation (RV-001 through RV-005)

## Metadata

* Task ID: issue-122-restart-gate-0228-c2
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Single-pass credibility critique of Cycle 2 (`issue-122-restart-gate-0228-c2`, child of `issue-122-restart-gate-0228`) on branch `feat/platform-122-restart-gate-0228` targeting `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) to resolve Cycle 1 post-implementation review findings `RV-001` through `RV-005` cleanly across `src/core` and `src/api`, validate with focused unit tests, `ruff check`, `ruff format --check`, and strict `mypy`, commit locally with `Refs #122` and the Copilot trailer without pushing, and leave a clean worktree.
* Research and evidence considered:
  * .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md
  * .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md
  * .copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-research.md
  * .copilot-tracking/reviews/logs/2026-11-15/issue-122-restart-gate-0228-review.md (`RV-001` through `RV-005`)
  * src/core/src/zava_forward/core/continuity.py
  * src/core/src/zava_forward/core/sqlstore.py
  * src/core/src/zava_forward/core/mssqlstore.py
  * src/core/src/zava_forward/core/assistants.py
  * src/core/src/zava_forward/core/seed_merge.py
  * src/core/tests/test_restart_gate_sql_fences.py
  * src/core/tests/test_seed_merge.py
  * src/api/tests/test_continuity_restart_gate.py
  * src/api/tests/test_continuity_epoch_export.py
  * src/api/tests/test_operator_suspension.py
  * src/api/tests/test_assistants.py
  * src/api/tests/test_mssqlstore.py
  * src/api/tests/test_permit_sql.py
  * src/api/tests/test_quality_sensors.py
  * src/api/tests/test_quality_sensors_c7.py
  * src/api/tests/test_quality_sensors_e1.py
  * src/api/tests/test_quality_sensors_e2.py
  * src/core/pyproject.toml and src/api/pyproject.toml
  * docs/adrs/0006-src-layout-and-cutover.md (verifying the non-existent `docs/adr/0006-ruff-format-exclude-on-six-core-modules.md` citation)
* Decisions, dependencies, and acceptance criteria considered: Architecture Decision (`assistant_tasks` SQL triggers + versioned `meta('continuity')` envelope), `FR-01` through `FR-05`, `NFR-01`, `NFR-02`, `AC-01` through `AC-05`, and phases `P01` through `P03` (`P01-T01` through `P03-T03`).
* Assessment boundary: Evaluates SQLite and T-SQL trigger semantics, `sqlstore.py` snapshot/optimistic-concurrency/rollback/seed-merge edge cases, `continuity.load`/`dump_sql`/`unwrap_sql` interactions with `MssqlStore` and `Assistants.continuity(db)`, genuine pre-gate worker subprocess isolation before and after `git commit`, ledger-database column upgrades, and test coverage completeness from supplied repository evidence. Live disposable SQL Server execution (`ZF_TEST_MSSQL=1`) and human-witnessed Azure deployment drills (`OD-35` / `RULE-020`) remain outside local offline execution scope.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-01, AC-01, RV-001, P01-T01 | Partial | Splits `test_id` and `corrective_evidence` comparisons cleanly in concept, but `P01-T01` drops the `current_candidate=None` default required by two call sites, omits checking rejected decisions on other suspensions (`other.get('decisions', [])`), and omits explicit `other['id'] != current_suspension['id']` and `current_candidate is not None` guards (`PC-004`). |
| FR-02, AC-02, RV-002, P02-T01 | Partial | SQLite and T-SQL trigger predicates on `assistant_tasks` cleanly fence `verify`, `accept`, and `edit-accept` while allowing `reject` and existing `dispatched` / body-tamper test fixtures, and include `COLLATE Latin1_General_100_BIN2` on `h.scope = i.capability`; however, `Assistants._add_column` fails on updatable MSSQL ledger tables (`WITH LEDGER = ON`) during in-place `_upgrade` (`PC-005`). |
| FR-03, AC-03, RV-003, P01-T01, P01-T02, P02-T01 | Partial | `dump_sql` (`epoch: -1`) + `review_gate_version` blocks pre-gate workers once `meta('continuity')` is wrapped, but `meta('continuity')` stays `None` on freshly seeded databases and unwrapped plain JSON on in-place migrated, `_seed`, and `merge_seed` databases until a later continuity write (`PC-002`), and `SqlStore.save()` never updates `self._proc_loaded` on the `cur == self._seq` fast path (`PC-003`). |
| FR-04, AC-04, RV-004, P01-T01, P01-T02 | Partial | Hardening `continuity.load`, `_discard`, `_proc_sync`, and `merge_seed` against malformed or empty JSON resolves `JSONDecodeError`, provided `self._proc_loaded` stays synchronized on `save()` (`PC-003`) and `P03-T01` exercises `SqlStore` rollback/unrelated-save/merge paths directly. |
| FR-05, AC-03, RV-005, P03-T01, P03-T02 | Partial | Test counts (`8` in `src/core`, `9` in `src/api`) comfortably respect the `<= 25` ceiling (`NFR-02`), but `P03-T02` loads pre-gate worker sources via `git show HEAD:...`, which points to the new gate-aware code as soon as Cycle 2 commits locally and fails in gitless/container environments (`PC-001`). |
| NFR-01, NFR-02, AC-05, P03-T03 | Partial | Validation commands avoid `/tmp` and preserve `ruff format --check` exclusions, but the plan cites a non-existent ADR path (`docs/adr/0006-ruff-format-exclude-on-six-core-modules.md`) instead of `src/core/pyproject.toml` and `src/api/pyproject.toml` (`PC-006`). |

## Verdict

* Verdict: Revise
* Rationale: The core Cycle 2 architecture (splitting `test_id` and `corrective_evidence` anti-replay checks, adding `reviewed_revision` and `review_gate_version` with SQLite and T-SQL triggers on `assistant_tasks`, wrapping `meta('continuity')` with an `epoch: -1` gate envelope, and fail-closed `continuity.load` parsing) directly resolves `RV-001` through `RV-005` without needing any user decision. However, six planner-correctable defects (`1 Critical`, `3 High`, `1 Medium`, `1 Low`) would cause the new `P03-T02` subprocess test to fail immediately after `git commit`, leave newly seeded or in-place migrated databases without a wrapped `meta('continuity')` envelope, desynchronize `SqlStore._proc_loaded` across consecutive single-writer saves, miss cross-suspension rejected `test_id` replay or raise `TypeError` on `current_candidate`, and break in-place MSSQL ledger upgrades unless revised before `rpi-implement`.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Critical]: P03-T02 loads pre-gate worker code via git show HEAD, which breaks immediately upon committing Cycle 2 and in gitless environments

* Related IDs: FR-05, AC-03, RV-005, P03-T02, P03-T03
* Evidence: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md (`P03-T02` lines 164-176); .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md (`AC-03` line 72, Testing Strategy lines 113-115); `git status --short` and `git log -n 1` (`HEAD` is currently pre-gate `02ab20cac` only because Cycle 1 edits are uncommitted)
* Concern: `P03-T02` specifies spawning `subprocess.run` to load `git show HEAD:src/core/src/zava_forward/core/continuity.py` and `git show HEAD:src/core/src/zava_forward/core/assistants.py` as the pre-gate worker. That works only while Cycle 1 and Cycle 2 remain uncommitted in the worktree. The moment `P03-T03` creates the required local commit (`Refs #122`), `HEAD` becomes the gate-aware Cycle 2 commit itself. On every post-commit test run, `tools/rpi-checks.py` gate run, PR `#1641` CI run, and later commit, `git show HEAD:...` loads the gate-aware modules instead of pre-gate code: `continuity.load` unwraps `dump_sql`, `export()` returns `epoch_current=True` and `actionable=True` when no hold is open, and `execute_next`/`claim`/`_fence_in`/`review` stamp `GATE_VERSION` and succeed instead of failing closed. In addition, container builds (`docker build -f src/api/Dockerfile src`) have no `.git` metadata at all.
* Impact: The `src/api` test suite passes before `git commit` and immediately fails after `git commit`, in hosted CI, and in container or sdist environments.
* Smallest useful change: Replace `git show HEAD:...` in `P03-T02` (and the plan's `AC-03` / Testing Strategy prose) with a deterministic, commit-invariant, git-free pre-gate worker shim inside the isolated child process: patch `continuity.load` to the exact pre-gate implementation (`json.loads(raw) if raw else continuity.blank()`, with no `unwrap_sql`) and `continuity.gate_hold` to `lambda *a, **kw: None`, then run real `Assistants.export()`, `Assistants.execute_next()` / `claim()` (`provider.calls == 0`), and pre-gate SQL write shapes (legacy 8-column `INSERT INTO assistant_attempts`, `UPDATE assistant_attempts` without `send_gate_version`, and legacy 4-bind `UPDATE assistant_tasks SET body=?,state=?,revision=revision+1 WHERE id=? AND revision=?` for both `verify` and `accept`) against the live SQLite database.
* Action owner: planning parent
* Exact resolving evidence: Updated `P03-T02` in `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md` and `AC-03` / Testing Strategy in `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md` contain zero `git show HEAD` dependencies and pass identically before and after `git commit` without `.git`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: meta('continuity') remains None on freshly seeded stores and unwrapped plain JSON on in-place migrated, _seed, and merge_seed stores until a continuity mutation occurs

* Related IDs: FR-03, AC-03, RV-003, P01-T01, P01-T02, P03-T02
* Evidence: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md (`P01-T01` lines 55-66, `P01-T02` lines 88-100); src/core/src/zava_forward/core/continuity.py (`sync_sql_gate` lines 121-147); src/core/src/zava_forward/core/sqlstore.py (`_migrate` line 322, `_seed` lines 886-896, `merge_seed` lines 967-971); src/api/tests/test_mssqlstore.py (`SharedSqlIsPortableTests` lines 286-320)
* Concern: Under `P01-T02`, `SqlStore._proc_write()` writes `continuity.dump_sql(...)` only when `self.data['continuity']` mutates. On a newly created/seeded `SqlStore` or `MssqlStore` (`dataset.DATA` has no `'continuity'` key), `SELECT value FROM meta WHERE key = 'continuity'` remains `None` until the first incident or change-register write. Likewise, on an in-place migrated pre-gate database whose `meta('continuity')` already holds valid plain JSON (`{"epoch": 2, ...}`), `_migrate()` runs `sync_sql_gate(read_meta=True)` without wrapping `meta('continuity')`, and `_proc_write()` skips rewriting unchanged `continuity`. Furthermore, `SqlStore._seed` (`sqlstore.py:888`) and `SqlStore.merge_seed` (`sqlstore.py:968`) still write `json.dumps(src[key])` (unwrapped plain JSON) when a seed includes `'continuity'`. Whenever `meta('continuity')` is `None` or unwrapped plain JSON and `continuity_open_holds` is empty, a pre-gate worker (`Assistants.continuity(db)` -> pre-gate `continuity.load`) sees valid `epoch >= 0`, so `export()` fails open (`epoch_current=True`, `actionable=True`, `relied_on=True`) and legacy `Store` AI paths (`recommendations` has no SQL trigger) fail open.
* Impact: Pre-gate `export()` and `Store` AI paths remain fail-open on freshly migrated/seeded and in-place upgraded SQLite/MSSQL databases prior to the first post-upgrade continuity write, leaving `RV-003` and `AC-03` only partially closed.
* Smallest useful change: Update `P01-T01` and `P01-T02` so that: (1) inside `continuity.sync_sql_gate(db, ..., read_meta=True, mssql=...)`, when the `meta` table exists and `meta_row is None`, it seeds `meta('continuity')` with `dump_sql(blank())` using portable `INSERT INTO meta (key, value) SELECT 'continuity', ? WHERE NOT EXISTS (SELECT 1 FROM meta WHERE key = 'continuity')` (which satisfies `SharedSqlIsPortableTests` and `MssqlStore._Conn._rewrite`), and when `meta_row` holds valid unwrapped plain JSON (`isinstance(parsed, dict)` without `schema == GATE_VERSION` and `history_valid` is `True`), it upgrades the row via `UPDATE meta SET value = ? WHERE key = 'continuity'` to `dump_sql(parsed)` while leaving malformed/corrupt or unknown-schema rows untouched; and (2) `SqlStore._seed` and `SqlStore.merge_seed` serialize `key == 'continuity'` with `continuity.dump_sql(src[key])`.
* Action owner: planning parent
* Exact resolving evidence: Updated `P01-T01`, `P01-T02`, and `P03-T01`/`P03-T02` in `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md` specify portable `meta('continuity')` envelope initialization/upgrade on `sync_sql_gate(read_meta=True)` plus `dump_sql` in `_seed` and `merge_seed`, and test pre-gate fail-closed `export()` at `epoch = 0` before any suspension is recorded.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: SqlStore.save() single-writer fast path updates _proc_snap without updating _proc_loaded, causing stale dirty-tracking and spurious ConflictError('continuity')

* Related IDs: FR-03, FR-04, AC-04, RV-004, P01-T02, P03-T01
* Evidence: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md (`P01-T02` lines 91-98); src/core/src/zava_forward/core/sqlstore.py (`save` lines 1207, 1264, 1277-1281; `_discard` lines 1334-1362; `_proc_sync` lines 1366-1378; `_proc_write` lines 1380-1394)
* Concern: `P01-T02` introduces `self._proc_loaded` in `_proc_sync()` and changes `_proc_write()` to skip writing `'continuity'` when `self.data.get('continuity') == self._proc_loaded.get('continuity')`. However, in `SqlStore.save()`, when `cur == self._seq` (the standard single-writer fast path at `sqlstore.py:1264, 1277-1279`), `save()` updates `self._proc_snap.update(proc_body)` after `COMMIT` and does NOT call `self._sync()` or `self._proc_sync()`. Because `self._proc_loaded` is never updated after `COMMIT` on that path: (1) after any continuity save (`D0 -> D1`), `self._proc_loaded['continuity']` remains stuck at `D0`, so every subsequent unrelated `save()` (`log_call`, case updates, audit writes) sees `D1 != D0`, needlessly rewrites `meta('continuity')` and `sync_sql_gate`, and raises a spurious `ConflictError('continuity')` if a peer writer touched `continuity` between `_sync()` and `BEGIN IMMEDIATE`; and (2) if `self.data['continuity']` later transitions back to a state equal to stale `D0`, `_proc_write()` sees `D0 == D0` and silently drops the write. In addition, when `meta('continuity')` is absent (`self._proc_snap.get('continuity') is None`), a read-only `self._cont()` call populates `self.data['continuity'] = blank()` while `self._proc_loaded.get('continuity')` is `None`, which would look dirty on an unrelated save unless `None` snapshot + `blank()` (or `PC-002`'s seeded `meta('continuity')`) is aligned.
* Impact: Broken optimistic-concurrency bookkeeping on `SqlStore` and `MssqlStore` across sequential saves in the same store instance, risking lost continuity writes or spurious `ConflictError('continuity')` during ordinary manual casework.
* Smallest useful change: Specify in `P01-T02` that `self._proc_loaded` is initialized to `{}` on store setup, updated alongside `self._proc_snap.update(proc_body)` in `SqlStore.save()` (`for key in proc_body: self._proc_loaded[key] = copy.deepcopy(self.data[key])`), and treated as unchanged when `self._proc_snap.get('continuity') is None and self.data.get('continuity') == continuity.blank()`. Add a sequential-save + corrupt-rollback regression assertion in `P03-T01`.
* Action owner: planning parent
* Exact resolving evidence: Updated `P01-T02` and `P03-T01` in `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md` include `SqlStore.save()` post-commit `self._proc_loaded` synchronization and test coverage for consecutive fast-path saves plus `_discard()` rollback over malformed `meta('continuity')`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: P01-T01 _check_claim_replay drops current_candidate=None default, misses rejected proposals on other suspensions, and omits self-exclusion and candidate-None guards

* Related IDs: FR-01, AC-01, RV-001, P01-T01, P03-T01
* Evidence: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md (`P01-T01` lines 67-76); .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md (`FR-01` line 51, `AC-01` line 70); src/core/src/zava_forward/core/continuity.py (`_check_claim_replay` lines 263-297, `validate_sql` lines 438-458, `restart_propose` line 686, `restart_decide` line 739); src/core/tests/test_restart_gate_sql_fences.py (lines 303-335)
* Concern: Four concrete edge cases exist in `P01-T01`'s specification of `_check_claim_replay`:
  1. `P01-T01` writes the signature with required `current_candidate` (`_check_claim_replay(doc, current_suspension, test_id, corrective_evidence, current_candidate, *, for_decision=False)`), but `restart_propose` (`continuity.py:686`) and `restart_decide` (`continuity.py:739`) call `_check_claim_replay` with 4 positional arguments before `self.save()` / `validate_sql` runs (and on JSON `Store`, `validate_sql` never runs). Removing `=None` raises `TypeError`.
  2. When `current_candidate is None` (on JSON `Store` or in the pre-`save()` check), `_same_tid(prop)` can and should run immediately across all suspensions, whereas `_same_ev(prop)` comparing `prop.get('candidate') == current_candidate` would evaluate `None == None` as `True` unless guarded by `current_candidate is not None` (or `('candidate' not in prop and current_candidate is None)` only if JSON-store cross-incident evidence blocking is intended).
  3. `FR-01` requires rejecting any reuse of a previously rejected `test_id` or `corrective_evidence` across rejected proposals, consumed restarts, and concurrently open suspensions, yet `P01-T01` checks `decisions` only on `current_suspension.get('decisions', [])` and never inspects `other.get('decisions', [])` on other suspensions. A `test_id` or `corrective_evidence` rejected via `'Keep suspended'` on `SUS-1` (which pops `SUS-1['proposal']`) can therefore be replayed freely on `SUS-2`.
  4. `P01-T01` says "Check other `doc['suspensions']`" without explicitly preserving `other.get('id') != current_suspension.get('id')` (needed so `validate_sql` does not reject `s['proposal']` against itself and so post-epoch re-proposals on the same incident in `test_restart_gate_sql_fences.py:325-333` remain valid), and keeps `not for_decision` on `other.get('status') == 'Suspended'` even though with `other['id'] != current_suspension['id']` a decision (`for_decision=True`) should also fail closed if another open suspension concurrently holds the same claim.
* Impact: Implementing `P01-T01` literally raises `TypeError` at `continuity.py:686` / `739` or self-blocks `validate_sql`, and still permits cross-incident replay of rejected `'Keep suspended'` `test_id` / `corrective_evidence` claims in violation of `FR-01`.
* Smallest useful change: Revise `P01-T01` (and add one assertion in `P03-T01`) so `_check_claim_replay` keeps `current_candidate=None`, guards `_same_ev(prop)` with `current_candidate is not None and prop.get('candidate') == current_candidate`, explicitly skips `other.get('id') == current_suspension.get('id')` in the `doc['suspensions']` loop, inspects `other.get('decisions', [])` for rejected `test_id` or `corrective_evidence` across all prior/other incidents, and checks `other.get('status') == 'Suspended'` on both propose and decide (`other['id'] != current_suspension['id']`).
* Action owner: planning parent
* Exact resolving evidence: Updated `P01-T01` and `P03-T01` in `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md` specify `current_candidate=None`, `other.get('id') != current_suspension.get('id')`, `other.get('decisions', [])` cross-suspension rejection checks, `current_candidate is not None` in `_same_ev`, and unit-test coverage for cross-suspension rejected-claim replay.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Assistants._add_column uses single-step NOT NULL DEFAULT DDL on MSSQL, failing on updatable ledger tables during in-place _upgrade

* Related IDs: FR-02, AC-02, RV-002, P02-T01, P03-T02
* Evidence: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md (`P02-T01` lines 115-116); src/core/src/zava_forward/core/assistants.py (`migrate` lines 764-770, `_add_column` lines 791-800, `_upgrade` lines 802-818); src/core/src/zava_forward/core/mssqlstore.py (`_is_ledger_table` and `_add_column_default` lines 263-279); src/api/tests/test_mssqlstore.py (`LedgerAddColumnStatements` lines 696-715, `MssqlLedgerMigration` lines 730-810)
* Concern: In a SQL Server / Azure SQL database created `WITH LEDGER = ON`, every table created without `WITH (LEDGER = OFF)` (including `assistant_tasks` and `assistant_attempts`) becomes an `UPDATABLE_LEDGER_TABLE`. As documented in `MssqlStore._add_column_default` (`mssqlstore.py:268-278`), SQL Server rejects `ALTER TABLE <table> ADD <col> <type> NOT NULL DEFAULT <val>` on an updatable ledger table (Error 37398). `Assistants._add_column` (`assistants.py:798`) currently runs that single-step `ALTER TABLE` unconditionally when `not present`, and `Assistants.__init__` (`assistants.py:767`) catches `Exception` from `self.migrate()` and silently sets `self.sql = False` (`Assistant schema unavailable`). Adding `reviewed_revision` and `review_gate_version` via `_add_column` on an existing ledger-enabled MSSQL database will therefore fail migration and silently disable assistants. In addition, `P02-T01` must state explicitly that `_upgrade` passes `COLLATE Latin1_General_100_BIN2` for `review_gate_version` on MSSQL so `g.gate_version = i.review_gate_version` in `assistant_tasks_gate_update` never raises T-SQL collation error 468 on upgraded databases.
* Impact: In-place schema upgrade of an existing ledger-enabled Azure SQL / SQL Server database fails `ALTER TABLE assistant_tasks` (and `assistant_attempts`) and disables all assistant operations.
* Smallest useful change: Update `P02-T01` so `Assistants._add_column` checks `SELECT ledger_type FROM sys.tables WHERE object_id = OBJECT_ID(?)` when `self.mssql` and `not present`: for non-ledger tables keep `ALTER TABLE {table} ADD {column} {ddl}`, and for updatable ledger tables (`bool(row and row[0])`) split `sqltype, default = ddl.split(' NOT NULL DEFAULT ', 1)` and apply the 4-step nullable `ADD` + `UPDATE ... WHERE IS NULL` + `CHECK (... IS NOT NULL)` + `DEFAULT ... FOR` sequence from `MssqlStore._add_column_default`, using `VARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL DEFAULT ''` for `review_gate_version` and `BIGINT NOT NULL DEFAULT 0` for `reviewed_revision`. Add a lightweight unit check (using a fake ledger DB recorder like `LedgerAddColumnStatements` in `test_mssqlstore.py` or in `test_continuity_restart_gate.py`) verifying both ledger and non-ledger `_add_column` DDL emission.
* Action owner: planning parent
* Exact resolving evidence: Updated `P02-T01` and `P03-T02` in `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md` specify ledger-safe MSSQL `_add_column` handling, explicit `Latin1_General_100_BIN2` collation in `_upgrade`, and unit verification of the emitted ledger `ALTER TABLE` statements.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: Plan references non-existent docs/adr/0006-ruff-format-exclude-on-six-core-modules.md instead of pyproject.toml format-exclude configuration

* Related IDs: NFR-01, P03-T03
* Evidence: .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md (`Scope` line 24, `NFR-01` line 57); docs/adrs/0006-src-layout-and-cutover.md; src/core/pyproject.toml (`[tool.ruff.format].exclude`); src/api/pyproject.toml (`[tool.ruff.format].exclude`)
* Concern: The Cycle 2 plan cites `docs/adr/0006-ruff-format-exclude-on-six-core-modules.md` in two places as the authority for excluding `continuity.py`, `sqlstore.py`, `mssqlstore.py`, `assistants.py`, and `test_mssqlstore.py` from `ruff format`. Neither `docs/adr/` nor any ADR on ruff format exclusions exists in the repository (`docs/adrs/0006-src-layout-and-cutover.md` covers the `src/` layout cutover); the canonical format-exclude lists are configured directly in `src/core/pyproject.toml` and `src/api/pyproject.toml`.
* Impact: Misleading broken reference in durable planning evidence that could confuse implementers or reviewers auditing ADR compliance.
* Smallest useful change: Replace `docs/adr/0006-ruff-format-exclude-on-six-core-modules.md` in `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md` with `src/core/pyproject.toml` and `src/api/pyproject.toml` (`[tool.ruff.format].exclude`).
* Action owner: planning parent
* Exact resolving evidence: `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md` cites only existing workspace paths (`src/core/pyproject.toml` and `src/api/pyproject.toml`).
* Decision route: direct planner correction

## Strengths and Residual Risk

* The `assistant_tasks` trigger predicate in `P02-T01` (`(NEW.state = 'accepted' AND (OLD.state <> 'accepted' OR NEW.revision <> OLD.revision OR NEW.body <> OLD.body)) OR (OLD.state = 'ready' AND NEW.state = 'ready' AND NEW.revision <> OLD.revision AND NEW.dispatched = OLD.dispatched)`) is well crafted: it fences `verify`, `accept`, and `edit-accept` while allowing `reject`, `_upgrade` `dispatched` backfills, raw-body corruption test setups (`test_continuity_epoch_export.py`, `test_operator_suspension.py`, `test_quality_sensors*.py`), `dispatched + revision` scan-order tests (`test_quality_sensors_e2.py:408`), leased-row lock probes (`test_permit_sql.py:303`), and serialized overlapping `review` vs `suspend/restart` transactions (`test_continuity_epoch_export.py:175`).
* Combining `gate` and `hold` checks into two T-SQL triggers (`assistant_tasks_gate_insert` and `assistant_tasks_gate_update`, each containing `NOT EXISTS` and `THROW 50004`) preserves `test_restart_gate_sql_fences.py:553` (`all("NOT EXISTS" in trig for trig in ASSISTANTS_MOD.MSSQL_ATTEMPT_TRIGGERS[2:])`), keeps `len(MSSQL_DDL) == 9` (`test_assistants.py:1345`), and matches `DialectConnection` (`test_assistants.py:1305`).
* Residual risk: Live SQL Server container execution (`ZF_TEST_MSSQL=1`) and human-witnessed Azure deployment drills (`OD-35` / `RULE-020` / Issue `#122` AC 4) are not executed in local unit-test validation; T-SQL trigger DDL, collation, teardown (`test_mssqlstore.wipe()`), and ledger `ALTER TABLE` emission are mitigated offline via structural/recorder assertions and remain subject to hosted CI / owner-witnessed drill gates (`Refs #122`).

## Questions or Blocking Evidence Gaps

* None. All six findings have unambiguous, evidence-backed direct planner corrections within the supplied boundary and require no user decision.

## Limitations

* This critique is a static, read-only credibility assessment against the working-tree Cycle 1 code, `HEAD` (`02ab20cac`), and existing test suites; no files in `src/` were modified and no live `mssql-python` SQL Server instance was queried.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: Apply direct planner revisions for `PC-001` through `PC-006` in `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md` and `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-c2-phase-details.md`, finalize the Cycle 2 plan without another critique pass, and proceed to `rpi-implement`.
* User response required: No
