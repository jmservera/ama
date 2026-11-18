---
title: "Phase Details - Issue #122 RAI Incident and Restart Gate Remediation (Cycle 2)"
description: "Evidence-based task specifications for Cycle 2 remediation of RV-001 through RV-005"
author: "Copilot"
ms.date: "2026-11-15"
---

## Task Context

* Task ID: `issue-122-restart-gate-0228-c2`
* Parent Task ID: `issue-122-restart-gate-0228`
* Plan Path: `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-c2-plan.md`
* Parent Review Path: `.copilot-tracking/reviews/logs/2026-11-15/issue-122-restart-gate-0228-review.md`
* Research Path: `.copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-research.md`

<!-- P01 -->
## Phase P01: Core Continuity Anti-Replay, SQL Envelope, and Corrupt-Meta Recovery (`RV-001`, `RV-003`, `RV-004`)

### Phase Direction

Harden `continuity.py` and `sqlstore.py` so claim anti-replay enforces normalized `test_id` uniqueness independently of `corrective_evidence` text or `candidate`, SQL-persisted `meta('continuity')` carries a versioned envelope that causes unmodified pre-gate (`HEAD`) and mismatched-gate readers to fail closed automatically, and `SqlStore` startup/reload recovers from empty or malformed `meta('continuity')` without raising `JSONDecodeError`.

<!-- P01-T01 -->
### Task P01-T01: Update `continuity.py` (`load`, `dump_sql`, `unwrap_sql`, `sync_sql_gate`, and `_check_claim_replay`)

* Target file: `src/core/src/zava_forward/core/continuity.py` (`[tool.ruff.format].exclude` in `src/core/pyproject.toml`; preserve concise style and never run single-file `ruff format` on it).
* Envelope, migration, & corrupt-load helpers (`RV-003`, `RV-004`, `PC-002`):
  * `dump_sql(doc)`: return `json.dumps(dict(gate_version=GATE_VERSION, epoch=-1, continuity=doc))`.
  * `unwrap_sql(obj)`: when `isinstance(obj, dict) and obj.get("gate_version") == GATE_VERSION and isinstance(obj.get("continuity"), dict)`, return `obj["continuity"]`; otherwise return `obj`.
  * `load(raw)`:
    * Return `blank()` ONLY when `raw is None`.
    * Parse `raw` (`deepcopy(raw)` when `isinstance(raw, dict)`, else `json.loads(raw)` when `isinstance(raw, str)`, else invalid). On `ValueError`, `TypeError`, or non-dict result (including `raw == ""`), return `dict(epoch=-1, suspensions=[], changes=[])`.
    * When `"gate_version" in doc`: if `doc.get("gate_version") != GATE_VERSION` or not `isinstance(doc.get("continuity"), dict)`, return `dict(epoch=-1, suspensions=[], changes=[], gate_mismatch=True)`; otherwise unwrap `doc = deepcopy(doc["continuity"])`.
    * Apply `doc.setdefault("epoch", 0)`, `doc.setdefault("suspensions", [])`, and `doc.setdefault("changes", [])` on valid dicts.
  * `sync_sql_gate(db, raw_value=None, *, read_meta=False, mssql=False)` (`PC-002`):
    * When `read_meta` is `True` and table `meta` exists:
      * If `meta_row is None`: execute portable `INSERT INTO meta (key, value) SELECT 'continuity', ? WHERE NOT EXISTS (SELECT 1 FROM meta WHERE key = 'continuity')` with `(dump_sql(blank()),)` and set `raw_value = dump_sql(blank())`.
      * Else if `isinstance(meta_row[0], str)`: if `meta_row[0]` parses as a `dict` without `"gate_version"` and `history_valid(load(parsed))` is `True`, upgrade in place via `UPDATE meta SET value = ? WHERE key = 'continuity'` with `(dump_sql(load(parsed)),)` and set `raw_value = dump_sql(load(parsed))`; leave malformed/corrupt or mismatched-`gate_version` rows untouched so corrupt evidence is never silently overwritten.
* Claim anti-replay (`RV-001`, `PC-004`, implementation-time refinement for `test_operator_suspension.py`):
  * In `_check_claim_replay(doc, current_suspension, test_id, corrective_evidence, current_candidate=None, *, for_decision=False)`:
    * Compute `norm_tid = test_id.strip().casefold()` and `norm_ev = corrective_evidence.strip().casefold()`.
    * Helper `_raw_tid(prop)`: returns `True` when `isinstance(prop, dict)` and `isinstance(prop.get("test_id"), str)` and `prop["test_id"].strip().casefold() == norm_tid`.
    * Helper `_raw_ev(prop)`: returns `True` when `isinstance(prop, dict)` and `isinstance(prop.get("corrective_evidence"), str)` and `prop["corrective_evidence"].strip().casefold() == norm_ev`.
    * Helper `_same_candidate_claim(prop)`: returns `True` when `current_candidate is not None` and `isinstance(prop, dict)` and `prop.get("candidate") == current_candidate` and `(_raw_tid(prop) or _raw_ev(prop))`. (Implementation-time refinement: existing regression drill `src/api/tests/test_operator_suspension.py:377-379` installs a new active release candidate `release_version="new"` after a prior `"Restarted"` incident and re-runs the standard regression suite `test_id="constructed-negative-and-fallback-drill"`, so decided/restarted claim checks compare `(_raw_tid(prop) or _raw_ev(prop))` within `current_candidate` while concurrent open `"Suspended"` incidents reject `_raw_tid(open_prop) or _raw_ev(open_prop)` unconditionally.)
    * Check `current_suspension.get("decisions", [])`: if `_same_candidate_claim(prior_prop)`, raise `PermissionError("Rejected corrective test evidence cannot be replayed; record fresh corrective tests.")`.
    * Check every `other` in `doc["suspensions"]` where `other.get("id") != current_suspension.get("id")`:
      * Check `other.get("decisions", [])`: if `_same_candidate_claim(prior_prop)`, raise `PermissionError("Rejected corrective test evidence cannot be replayed; record fresh corrective tests.")`.
      * When `other.get("status") == "Restarted"`: if `_same_candidate_claim(used_prop)`, raise `PermissionError("Corrective test claim was already consumed on a prior suspension; record fresh corrective tests.")`.
      * When `other.get("status") == "Suspended"`: if `_raw_tid(open_prop) or _raw_ev(open_prop)`, raise `PermissionError("Corrective test claim is already proposed on another open suspension; record fresh corrective tests.")`.
* Completion expectation: `load("")` and `load("{bad")` return `epoch == -1` (`history_valid(doc) is False`), `load(None)` returns `blank()`, `load(dump_sql(blank()))` round-trips to `blank()`, pre-gate `continuity.load(dump_sql(blank()))` fails `history_valid` (`epoch == -1`), `sync_sql_gate(read_meta=True)` seeds/wraps `meta('continuity')`, and `_check_claim_replay` rejects reused `test_id` independently of altered `corrective_evidence` across same/other rejected decisions and prior Restarted suspensions for the candidate and unconditionally across concurrent open suspensions while preserving `test_operator_suspension.py` across candidate upgrades.

<!-- P01-T02 -->
### Task P01-T02: Update `sqlstore.py` (`_seed`, `merge_seed`, `save`, `_discard`, `_proc_sync`, `_proc_write`)

* Target file: `src/core/src/zava_forward/core/sqlstore.py` (`[tool.ruff.format].exclude` in `src/core/pyproject.toml`).
* Changes (`PC-002`, `PC-003`):
  * Initialize `self._proc_loaded = {}` alongside `self._proc_snap = {}` on `SqlStore` setup.
  * `_seed`: when writing `doc in self.DOCS`, serialize `"continuity"` via `continuity.dump_sql(src[doc])` and other docs via `json.dumps(src[doc])`.
  * `merge_seed`: when comparing existing `meta` value for `key == "continuity"`, unwrap stored JSON safely (`try: existing = continuity.unwrap_sql(json.loads(row[0]))` / `canon(existing) == canon(src[key])`, treating `ValueError` or mismatched envelope as preserved non-identical continuity without crashing), and if `"continuity"` is ever in `docs_inserted`, serialize with `continuity.dump_sql(src[key])` and pass to `continuity.sync_sql_gate`.
  * `_discard` and `_proc_sync`: when `key == "continuity"`, load `self.data["continuity"]` via `continuity.load(body)` / `continuity.load(row[0])` instead of `json.loads(...)`, preserve raw `snapshots["continuity"] = row[0]` for optimistic concurrency comparison, and record `self._proc_loaded[key] = copy.deepcopy(self.data[key])` for loaded docs (`self._proc_loaded.pop(key, None)` when absent).
  * `_proc_write`: for `key == "continuity"`, treat `self.data["continuity"]` as unchanged when `(self._proc_snap.get("continuity") is None and self.data["continuity"] == continuity.blank())` or `(self._proc_snap.get("continuity") is not None and self.data["continuity"] == self._proc_loaded.get("continuity"))`; otherwise serialize `body = continuity.dump_sql(self.data["continuity"])`, verify `(row[0] if row else None) == self._proc_snap.get("continuity")`, write `_meta_set("continuity", body)`, and run `continuity.sync_sql_gate(self.db, body, mssql=hasattr(self, "_env"))`.
  * `save`: right after `self._proc_snap.update(proc_body)` on the post-`COMMIT` path (`cur == self._seq` fast path included), update `for key in proc_body: self._proc_loaded[key] = copy.deepcopy(self.data[key])` so sequential saves in the same store instance stay strictly synchronized.
* Completion expectation: Reopening `SqlStore` over `""` or `"{not-json"` in `meta('continuity')` succeeds cleanly, syncs the fail-closed `'all'` hold into `continuity_open_holds`, preserves the untouched raw corrupt `meta('continuity')` row across manual case/challenge/hazard saves and `_discard()` rollbacks, keeps sequential fast-path continuity and manual saves conflict-free, and passes all `test_seed_merge.py` and `test_operator_suspension.py` tests.

<!-- P02 -->
## Phase P02: SQL Trigger Hardening on `assistant_attempts` and `assistant_tasks` (`RV-002`, `RV-003`)

### Phase Direction

Close both SQL-trigger bypasses identified in Cycle 1 review so neither active `assistant_attempts` updates during a hold nor pre-gate/open-hold `assistant_tasks` verification/acceptance updates can commit.

<!-- P02-T01 -->
### Task P02-T01: Harden `assistant_attempts` and `assistant_tasks` DDL, `_upgrade`, `review()`, and MSSQL test cleanup

* Target files:
  * `src/core/src/zava_forward/core/assistants.py` (ADR 0006 format-excluded)
  * `src/api/tests/test_mssqlstore.py` (ADR 0006 format-excluded)
  * `src/core/README.md` and `src/api/README.md`
* `assistant_attempts` trigger fix (`RV-002`):
  * In `SQLITE_ATTEMPT_TRIGGERS` (`assistant_attempts_hold_update`): change `WHEN NEW.outcome IN ('reserved', 'sending') AND NEW.outcome <> OLD.outcome AND EXISTS ...` to `WHEN NEW.outcome IN ('reserved', 'sending') AND EXISTS (SELECT 1 FROM continuity_open_holds h WHERE h.scope = 'all' OR h.scope = NEW.capability)`.
  * In `MSSQL_ATTEMPT_TRIGGERS` (`assistant_attempts_gate_update`): change `IF EXISTS (SELECT 1 FROM inserted i JOIN deleted d ON d.id = i.id WHERE i.outcome IN (''reserved'', ''sending'') AND i.outcome <> d.outcome AND EXISTS ...)` to `IF EXISTS (SELECT 1 FROM inserted i WHERE i.outcome IN (''reserved'', ''sending'') AND EXISTS (SELECT 1 FROM continuity_open_holds h WHERE h.scope = ''all'' OR h.scope = i.capability))`.
* `assistant_tasks` columns, ledger-safe `_add_column`, and triggers (`RV-003`, `PC-005`):
  * Add `review_gate_version` (`TEXT NOT NULL DEFAULT ''` in SQLite; `VARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL DEFAULT ''` in T-SQL) and `reviewed_revision` (`INTEGER NOT NULL DEFAULT 0` in SQLite; `BIGINT NOT NULL DEFAULT 0` in T-SQL) to `assistant_tasks` in `SQLITE_DDL`, `MSSQL_DDL`, and `Assistants._upgrade`.
  * In `Assistants._add_column(self, db, table, column, ddl)` (`PC-005`): when `self.mssql` and `not present`, query `row = db.execute("SELECT ledger_type FROM sys.tables WHERE object_id = OBJECT_ID(?)", (table,)).fetchone()`; when `bool(row and isinstance(row[0], int) and row[0] != 0)` (updatable MSSQL ledger table), split `sqltype, default = ddl.split(" NOT NULL DEFAULT ", 1)` and run the 4-step sequence (`ALTER TABLE {table} ADD {column} {sqltype} NULL`, `UPDATE {table} SET {column} = {default} WHERE {column} IS NULL`, `ALTER TABLE {table} ADD CONSTRAINT ck_{table}_{column}_nn CHECK ({column} IS NOT NULL)`, `ALTER TABLE {table} ADD CONSTRAINT df_{table}_{column} DEFAULT {default} FOR {column}`); otherwise run `ALTER TABLE {table} ADD {column} {ddl}` as before.
  * Add SQLite triggers to `SQLITE_ATTEMPT_TRIGGERS`:
    * `assistant_tasks_gate_insert`: `BEFORE INSERT ON assistant_tasks WHEN NEW.state = 'accepted' AND (NEW.reviewed_revision <> NEW.revision OR NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = NEW.review_gate_version)) BEGIN SELECT RAISE(ABORT, 'continuity SQL gate mismatch'); END`
    * `assistant_tasks_hold_insert`: `BEFORE INSERT ON assistant_tasks WHEN NEW.state = 'accepted' AND EXISTS (SELECT 1 FROM continuity_open_holds h WHERE h.scope = 'all' OR h.scope = NEW.capability) BEGIN SELECT RAISE(ABORT, 'continuity scope is suspended'); END`
    * `assistant_tasks_gate_update`: `BEFORE UPDATE ON assistant_tasks WHEN ((NEW.state = 'accepted' AND (OLD.state <> 'accepted' OR NEW.revision <> OLD.revision OR NEW.body <> OLD.body)) OR (OLD.state = 'ready' AND NEW.state = 'ready' AND NEW.revision <> OLD.revision AND NEW.dispatched = OLD.dispatched)) AND (NEW.reviewed_revision <> NEW.revision OR NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = NEW.review_gate_version)) BEGIN SELECT RAISE(ABORT, 'continuity SQL gate mismatch'); END`
    * `assistant_tasks_hold_update`: `BEFORE UPDATE ON assistant_tasks WHEN ((NEW.state = 'accepted' AND (OLD.state <> 'accepted' OR NEW.revision <> OLD.revision OR NEW.body <> OLD.body)) OR (OLD.state = 'ready' AND NEW.state = 'ready' AND NEW.revision <> OLD.revision AND NEW.dispatched = OLD.dispatched)) AND EXISTS (SELECT 1 FROM continuity_open_holds h WHERE h.scope = 'all' OR h.scope = NEW.capability) BEGIN SELECT RAISE(ABORT, 'continuity scope is suspended'); END`
  * Add T-SQL triggers to `MSSQL_ATTEMPT_TRIGGERS` (and drop names in `src/api/tests/test_mssqlstore.py:wipe()`):
    * `assistant_tasks_gate_insert` (`AFTER INSERT ON assistant_tasks`) and `assistant_tasks_gate_update` (`AFTER UPDATE ON assistant_tasks`) with identical conditions and `h.scope = i.capability COLLATE Latin1_General_100_BIN2`.
  * In `Assistants.review()`:
    * When `action == "reject"`: keep `UPDATE assistant_tasks SET body=?,state=?,revision=revision+1 WHERE id=? AND revision=?` so rejection always remains available during suspension or gate mismatch.
    * When `action in ("verify", "accept", "edit-accept")`: execute `UPDATE assistant_tasks SET body=?,state=?,review_gate_version=?,reviewed_revision=revision+1,revision=revision+1 WHERE id=? AND revision=?` with `continuity.GATE_VERSION`.
  * Update `src/core/README.md` and `src/api/README.md` to mention `assistant_tasks` review/acceptance SQL trigger fencing alongside `assistant_attempts` and the versioned SQL continuity envelope.
* Completion expectation: `len(MSSQL_DDL)` remains `9`; existing corruption/backfill tests in `test_quality_sensors*.py`, `test_continuity_epoch_export.py`, and `test_operator_suspension.py` pass untouched; and any pre-gate or open-hold SQL `verify`/`accept`/`edit-accept` write aborts at the database trigger layer.

<!-- P03 -->
## Phase P03: Focused SQL/API Verification Expansion and Full Local Validation (`RV-005`)

### Phase Direction

Prove every Cycle 2 remediation and planned race/audit/manual/pre-gate scenario in `test_restart_gate_sql_fences.py` and `test_continuity_restart_gate.py` within `<= 25` combined test methods, then run full local validation and clean up temporary tooling state.

<!-- P03-T01 -->
### Task P03-T01: Expand `src/core/tests/test_restart_gate_sql_fences.py`

* Target file: `src/core/tests/test_restart_gate_sql_fences.py`
* Additions/updates (keeping `<= 10` test methods):
  * Ensure all non-replay setup steps use distinct `test_id` values, and add explicit assertions proving `_check_claim_replay` / `restart_propose` / `restart_decide` reject a reused normalized `test_id` (`"  SUITE-ALPHA-122  "`) even when `corrective_evidence` text and `candidate` are completely changed across Keep-suspended retry on the same suspension, rejected Keep-suspended decision on a different suspension, open suspension, and prior Restarted suspension (`RV-001`, `PC-004`).
  * Assert that updating an already-`'sending'` row in `assistant_attempts` (`SET active_until = active_until + 30` with `outcome = 'sending'` unchanged) during an open hold in `continuity_open_holds` raises `sqlite3.IntegrityError` (`continuity scope is suspended`) (`RV-002`), and that updating a `'ready'` row in `assistant_tasks` to `'accepted'` or verifying it (`revision = revision + 1`) without matching `review_gate_version` / `reviewed_revision` or under an open hold raises `sqlite3.IntegrityError` (`RV-003`).
  * Add a test reopening `SqlStore` when `meta WHERE key='continuity'` is corrupted (`""` and `"{not-json"`), proving `SqlStore` initializes without raising, syncs `('all', 'unavailable', ...)` into `continuity_open_holds`, blocks AI continuity checks, preserves untouched corrupt `meta('continuity')` across manual case/challenge/hazard saves and `_discard()` rollbacks, and keeps consecutive fast-path continuity + manual saves conflict-free (`RV-004`, `PC-003`).
  * Pass explicit `env` with worktree `src/core/src` (+ `src/agents/src`, `src/api/src`) prepended to `PYTHONPATH` in `subprocess.run` (`RV-005`).

<!-- P03-T02 -->
### Task P03-T02: Expand `src/api/tests/test_continuity_restart_gate.py`

* Target file: `src/api/tests/test_continuity_restart_gate.py`
* Additions/updates (keeping combined core + API test methods `<= 25`):
  * Commit-invariant, git-free pre-gate worker/reviewer/exporter subprocess test (`RV-003`, `RV-005`, `PC-001`, `PC-002`): prepare a live migrated SQLite store at `epoch = 0` (before any suspension, verifying `meta('continuity')` is already wrapped with `dump_sql`) and during suspension with `queued` (`pending`), `leased`, and `ready` proposals, then spawn a `subprocess.run` (with explicit worktree `PYTHONPATH` and zero `.git` dependency) whose isolated child process patches `continuity.load` to the exact pre-gate implementation (`json.loads(raw) if raw else continuity.blank()`, without `unwrap_sql`) and `continuity.gate_hold` to `lambda *a, **kw: None`, and verifies:
    1. `export()` and `detail()` on the pre-gate worker mark the `ready` proposal `epoch_current=False`, `actionable=False`, `relied_on=False`, `suspension="unavailable"` even at `epoch = 0` before any suspension is recorded;
    2. `execute_next` / `claim` (`queued`), `_fence_in` / `renew` (`leased`), `review("verify")` (`ready`), and `review("accept")` (`ready`) all fail closed on the pre-gate worker (`provider.calls == 0`), while `review("reject")` on a disposable `ready` proposal remains available; and
    3. Direct legacy pre-gate SQL write shapes bypassing Python checks (legacy 8-column `INSERT INTO assistant_attempts`, `UPDATE assistant_attempts SET outcome='sending'` without `send_gate_version`, and legacy 4-bind `UPDATE assistant_tasks SET body=?,state=?,revision=revision+1 WHERE id=? AND revision=?` for both `verify` and `accept`) all fail with `sqlite3.IntegrityError` at the SQLite trigger layer.
  * Add a recorder unit assertion verifying `Assistants._add_column` emits the 4-step nullable `ADD` + `UPDATE` + `CHECK` + `DEFAULT` DDL sequence with `COLLATE Latin1_General_100_BIN2` when `sys.tables.ledger_type` is `2` (`UPDATABLE_LEDGER_TABLE`) and single-step `ALTER TABLE ... ADD` when `ledger_type` is `0` (`PC-005`).
  * `PasswordProvider` `POST /api/continuity/restart-decide` -> `403` + `ai_restart_decide_denied` audit entry (`RV-005`).
  * Store-dispatched HTTP negative subtests assert `ai_restart_propose_denied` and `ai_restart_decide_denied` audit rows increment as expected, including normalized `test_id` replay with altered `corrective_evidence` (`RV-001`, `RV-005`).
  * During `all` suspension, exercise HTTP `challenge_update` and `challenge_escalate` (to a distinct owner) alongside `challenge_open` (`Phone` + `Digital`) and `challenge_resolve` (`"Correction recorded"`) (`RV-005`).
  * Add `threading.Barrier(2)` concurrent races for `verify` vs `suspend` on a `ready` proposal and mid-flight `_fence_in` + `complete_result` vs `suspend` on an already-`leased` proposal alongside `accept` vs `suspend` and `claim` vs `suspend` (`RV-005`).

<!-- P03-T03 -->
### Task P03-T03: Full Validation and Workspace Cleanup

* Create workspace-local `.venv-122-local` (`python3 -m venv .venv-122-local`, never `/tmp`), install editable `./src/core ./src/agents ./src/api` plus `ruff` and `mypy`.
* Run:
  1. Focused suites: `test_restart_gate_sql_fences.py`, `test_continuity_restart_gate.py`, `test_seed_merge.py`, `test_operator_suspension*.py`, `test_continuity_epoch_export.py`, `test_quality_sensors*.py`, `test_assistants.py`, `test_mssqlstore.py`.
  2. Full suites: `src/core` (`unittest discover -s tests -q`), `src/api` (`PYTHONPATH=../core/tests:../agents/tests ... unittest discover -s tests -q`), and `tools/rename-zava-tests.py`.
  3. Static gates: `ruff check src/core src/api`, `ruff format --check src/core src/api`, `mypy src/core`, and `mypy src/api`.
* Remove `.venv-122-local` immediately after validation completes.
