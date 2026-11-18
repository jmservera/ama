<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #122 Local RAI Incident, Restart Gate, Suspension Fallback, and SQL Old-Image Exclusion

## Metadata

* Task ID: issue-122-restart-gate-0228
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Single-pass credibility critique for branch `feat/platform-122-restart-gate-0228` targeting `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) delivering the three remaining local RAI Incident and Restart acceptance criteria of Issue #122 across `src/core` and `src/api`: (1) corrective-evidence and distinct authorized human approval restart gate refusing replayed, stale, self-approved, or unauthorized restarts; (2) uninterrupted manual case work, accessible challenge, and independent hazard response during suspension; and (3) independent SQL connection, concurrent suspend/review, race, and restart tests covering `queued` (`pending`), `leased`, and `ready` proposals plus old-image restart, validated with focused `src/core` and `src/api` unit tests, `ruff check`, `ruff format --check`, and `mypy`, and committed locally with `Refs #122` without pushing.
* Research and evidence considered:
  * .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-plan.md
  * .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md
  * .copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-research.md (`C1` through `C18`)
  * src/core/src/zava_forward/core/restart_authority.py
  * src/core/src/zava_forward/core/continuity.py
  * src/core/src/zava_forward/core/sqlstore.py
  * src/core/src/zava_forward/core/mssqlstore.py
  * src/core/src/zava_forward/core/assistants.py
  * src/core/src/zava_forward/core/resident_decisions.py
  * src/core/src/zava_forward/core/challenges.py
  * src/api/src/zava_forward/api/server.py
  * src/api/src/zava_forward/api/auth.py
  * src/core/README.md
  * src/api/README.md
  * Referenced regression and typing targets cited by the supplied artifacts: src/core/pyproject.toml, src/api/pyproject.toml, src/core/tests/test_operator_suspension_drill.py, src/core/tests/test_seed_merge.py, src/api/tests/test_operator_suspension.py, src/api/tests/test_continuity_epoch_export.py, src/api/tests/test_mssqlstore.py, and src/api/tests/test_assistants.py.
* Decisions, dependencies, and acceptance criteria considered: Architecture Decision Option B (SQLite and T-SQL `continuity_gate_state` + `continuity_open_holds` + triggers on `assistant_attempts`), `FR-1` through `FR-4`, `NFR-1`, `NFR-2`, `AC-1` through `AC-4`, and phases `P01` through `P04` (`P01-T01` through `P04-T02`).
* Assessment boundary: Evaluates local software design, SQLite and T-SQL dialect semantics, upgrade/seed/merge/corruption-fixture interactions, anti-replay invariants, HTTP/auth route semantics, strict `mypy` and test-budget constraints, and workspace execution constraints from the supplied repository files. Live disposable SQL Server execution (`ZF_TEST_MSSQL=1`) and human-witnessed Azure deployment drills (`OD-35` / `RULE-020` / Issue #122 AC 4) remain outside local execution scope and are properly scoped to `Refs #122`.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1, AC-1, C1-C6, P01-T01 | Partial | Covers empty/placeholder corrective-evidence refusal, but reusing `_PLACEHOLDER_PATTERNS[0]` from `restart_authority.py` substring-rejects legitimate 600-character corrective prose containing words such as `placeholder` or `unassigned`, and `restart_decide` does not re-validate stored proposal text (`PC-005`). |
| FR-2, AC-1, C1-C6, P01-T02 | Partial | Covers distinct OID-bound `ZavaForward.AIRestart` approval and `view_only` refusal in Core, but anti-replay leaves casefolding, rejected-`test_id`, and concurrent open-incident `test_id` gaps (`PC-005`), and `FR-2` conflates outer HTTP `403` `view_only` rejection with store-level `ai_restart_*_denied` audit rows (`PC-006`). |
| FR-3, AC-2, C7-C9, P03-T01, P03-T02 | Covered | Manual case progression (`log_call`, `set_decision`, `advance`), accessible digital and non-digital `challenge_open` / `challenge_resolve`, and statutory Awaab's Law emergency hazard routing are verified free of `continuity_block` / `Assistants` hooks across Core and HTTP during `'all'` and task-scope suspensions. |
| FR-4, AC-3, C10-C18, P02-T01, P02-T02 | Partial | Architecture Option B is sound, but scalar `!= (SELECT gate_version ...)` fails open on `NULL` in SQLite and T-SQL, T-SQL trigger specs use SQLite-only `NEW`/`OLD` syntax and risk `VARCHAR` vs `NVARCHAR ... BIN2` collation conflicts (`PC-001`), raw `INSERT OR IGNORE` violates `SharedSqlIsPortableTests` and MSSQL harness teardown lists omit the new tables (`PC-002`), and `gate_version` mismatch in `Assistants.disabled()` misses `review`/`complete`/`_permit_block`/`export` (`PC-004`). |
| C17, C18, P02-T01, P02-T02 | Partial | Identifies corruption-test and seed-merge interactions, but omits `SqlStore.merge_seed(apply=True)`, raw JSON decode failures in `continuity.load`, and monotonic-epoch trigger aborts if malformed `meta('continuity')` sync attempts to lower `continuity_gate_state.epoch` (`PC-004`). |
| NFR-1, P04-T01 | Covered | Constructed-drill framing (`RULE-024`, `OD-35` unappointed, `Refs #122`) and `src/core/README.md` + `src/api/README.md` documentation updates match repository conventions. |
| NFR-2, AC-4, P03-T01, P03-T02, P04-T02 | Partial | Combined `<= 25` test-method budget (`<= 12` + `<= 12`) is well bounded, but `NFR-2` and `P04-T02` prescribe `/tmp/zf-122-0228-venv` against the workspace `/tmp` prohibition, `P03-T02` omits `PYTHONPATH`/timeout on `subprocess.run` (`PC-003`), and `P03` excludes `pyproject.toml` edits without specifying `: Any` boundary aliases required by strict `mypy` (`PC-007`). |

## Verdict

* Verdict: Revise
* Rationale: Option B and the four-phase decomposition credibly cover all three Issue #122 local acceptance criteria, and no divergent architectural or scope question requires user input. However, seven concrete technical defects in the candidate plan and phase details (`1 Critical`, `3 High`, `3 Medium`) would cause trigger fail-open behavior on missing singleton state, invalid T-SQL DDL/collation errors, immediate `SharedSqlIsPortableTests` failure in `src/api`, workspace `/tmp` rule violation, incomplete `gate_version` fail-closed enforcement on `ready`/`leased` proposals, and strict-`mypy` or HTTP audit-assertion failures during implementation unless corrected directly by the planning parent before `rpi-implement`.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Critical]: SQLite and T-SQL trigger specifications fail open on NULL scalar subqueries, use invalid T-SQL NEW/OLD syntax, and mix T-SQL collations

* Related IDs: FR-4, AC-3, C13, C14, C15, P02-T01, P02-T02
* Evidence: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md (`P02-T01`, `P02-T02`); src/core/src/zava_forward/core/mssqlstore.py (`_t` at line 30, `APPEND_ONLY` at lines 67-68); src/core/src/zava_forward/core/assistants.py (`SQLITE_DDL` / `MSSQL_DDL` at lines 586-602)
* Concern: Three SQL dialect defects appear in `P02-T01` and `P02-T02`. First, `P02-T02` specifies aborting when `NEW.gate_version != (SELECT gate_version FROM continuity_gate_state WHERE id = 1)` (and similarly for `send_gate_version`). Under SQL three-valued logic in both SQLite (`WHEN (...)`) and T-SQL (`IF (...)`), if `continuity_gate_state` has no `id = 1` row, the scalar subquery yields `NULL`, `gate_version != NULL` evaluates to `UNKNOWN` (treated as false), and the trigger fails open instead of blocking old-image or unseeded inserts/updates. Second, `P02-T01` and `P02-T02` express trigger logic in SQLite per-row `NEW.*` / `OLD.*` terms (`NEW.epoch < OLD.epoch`, `NEW.outcome = 'reserved'`), whereas T-SQL supports only set-based `INSTEAD OF` or `AFTER` triggers over `inserted` and `deleted` tables with `THROW`. Third, `mssqlstore._t()` declares `NVARCHAR(...) COLLATE Latin1_General_100_BIN2`, while `assistants.py` `MSSQL_DDL` declares `VARCHAR(...)` using the database default collation; comparing `continuity_open_holds.scope = i.capability` or `g.gate_version = i.gate_version` across mismatched collations raises SQL Server Error 468 on non-BIN2 default databases.
* Impact: Old-image or unseeded `assistant_attempts` writes can bypass the database gate if row `id = 1` is absent, and T-SQL DDL creation or trigger execution fails on SQL Server (`ZF_TEST_MSSQL=1`).
* Smallest useful change: Update `P02-T01` and `P02-T02` to: (1) enforce `CHECK (id = 1)` on `continuity_gate_state` and replace scalar `!=` comparisons with NULL-safe fail-closed `NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = ...)` in both SQLite and T-SQL; (2) write explicit set-based T-SQL triggers (`INSTEAD OF DELETE` on `continuity_gate_state` and `AFTER INSERT, UPDATE` on `continuity_gate_state` and `assistant_attempts` querying `inserted` / `deleted` and issuing `THROW 50004` / `50005`); and (3) declare `NVARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL DEFAULT N''` (or explicit `COLLATE Latin1_General_100_BIN2` in trigger predicates) on the new T-SQL columns so collations match across `mssqlstore.py` and `assistants.py`.
* Action owner: planning parent
* Exact resolving evidence: Revised `P02-T01` and `P02-T02` specifications contain explicit NULL-safe `NOT EXISTS` predicates, separate SQLite (`BEFORE ... RAISE(ABORT, ...)`) and set-based T-SQL (`INSTEAD OF` / `AFTER ... inserted`/`deleted` + `THROW`) DDL patterns, and matched `Latin1_General_100_BIN2` collation definitions.
* Decision route: planner-direct

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Raw INSERT OR IGNORE breaks offline SharedSqlIsPortableTests and omitted MSSQL teardown tables break hosted SQL Server suites

* Related IDs: FR-4, AC-3, AC-4, P02-T01, P02-T02
* Evidence: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md (`P02-T01` step 2, `P02-T02` step 1); src/api/tests/test_mssqlstore.py (`TABLES` and `wipe()` at lines 42-51, `SharedSqlIsPortableTests.test_sqlite_only_syntax_confined_to_dialect_hooks` at lines 308-317); src/api/tests/test_assistants.py (`MssqlFixture.setUp` at lines 1580-1583)
* Concern: First, `SharedSqlIsPortableTests.test_sqlite_only_syntax_confined_to_dialect_hooks` runs unconditionally during offline `src/api` unittest discovery (even without SQL Server) and inspects every line of `zava_forward.core.sqlstore` and `zava_forward.core.assistants`, failing if `INSERT OR IGNORE`, `INSERT OR REPLACE`, or `REPLACE INTO` appears outside `def _meta_set` or `def _insert_ignore`. Implementing `P02-T01` / `P02-T02`'s `INSERT OR IGNORE` seeding in `_create_schema`, `_migrate`, or `Assistants.migrate()` will immediately fail `src/api` unit tests. Second, in hosted SQL Server CI (`ZF_TEST_MSSQL=1`), `test_mssqlstore.wipe()` and `test_assistants.MssqlFixture.setUp()` drop hardcoded table lists that omit `continuity_open_holds` and `continuity_gate_state`. Because `continuity_gate_state` rejects `epoch` decreases via trigger, leaving `continuity_gate_state` with `epoch > 0` after dropping `meta` will cause subsequent `MssqlStore` setups (`epoch = 0`) to fail in `_migrate` / `_seed`.
* Impact: Offline `src/api` unittest discovery fails `SharedSqlIsPortableTests`, and hosted `ZF_TEST_MSSQL=1` suites fail across consecutive test classes once any test increments `continuity.epoch`.
* Smallest useful change: Specify in `P02-T01` and `P02-T02` that `sqlstore.py` and `assistants.py` must seed `continuity_gate_state` using `self._insert_ignore(...)` or portable `INSERT INTO continuity_gate_state (id, gate_version, epoch) SELECT 1, ?, 0 WHERE NOT EXISTS (SELECT 1 FROM continuity_gate_state WHERE id = 1)` (never raw `INSERT OR IGNORE` outside `_insert_ignore`), and include updating the table-drop lists in `src/api/tests/test_mssqlstore.py` and `src/api/tests/test_assistants.py` to drop `continuity_open_holds` and `continuity_gate_state` (and any standalone trigger names if needed).
* Action owner: planning parent
* Exact resolving evidence: Revised plan target files and `P02-T01`/`P02-T02` explicitly require portable `WHERE NOT EXISTS` / `_insert_ignore` seeding and add `continuity_open_holds` and `continuity_gate_state` to `test_mssqlstore.py` and `test_assistants.py` teardown lists.
* Decision route: planner-direct

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Validation steps prescribe creating a /tmp virtual environment and omit subprocess PYTHONPATH/timeout controls

* Related IDs: NFR-2, AC-3, AC-4, P03-T02, P04-T02
* Evidence: .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-plan.md (`NFR-2` at line 97); .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md (`P03-T02` at line 319, `P04-T02` at lines 384-386)
* Concern: `NFR-2` and `P04-T02` instruct `rpi-implement` to create and execute `/tmp/zf-122-0228-venv`, violating the repository/session execution constraint prohibiting any writes or redirects to `/tmp` or `/var/tmp`. Additionally, `P03-T02` spawns `subprocess.run([sys.executable, "-c", ...])` to verify cross-process SQLite old-image rejection without specifying `env` (`PYTHONPATH` propagation for `src/core/src`, `src/agents/src`, `src/api/src`) or a bounded `timeout`, risking `ModuleNotFoundError`, importing stale installed wheels instead of the worktree sources, or hanging on SQLite lock contention.
* Impact: Implementing `P04-T02` verbatim violates workspace policy or fails execution, and the multi-process old-image test in `P03-T02` can test the wrong code path or hang.
* Smallest useful change: Replace `/tmp/zf-122-0228-venv` in `NFR-2` and `P04-T02` with non-`/tmp` tooling execution (using installed Python/`ruff`/`mypy` or a temporary workspace-relative environment such as `.venv-122-local` that is deleted before verifying `git status --short` is empty), and specify explicit `env` (`PYTHONPATH` pointing at the worktree `src/*/src` roots) plus `timeout=15` on `subprocess.run` in `P03-T02`.
* Action owner: planning parent
* Exact resolving evidence: Zero `/tmp` paths remain in the plan or phase details, and `P03-T02` specifies worktree `PYTHONPATH` propagation and a bounded timeout for the child process.
* Decision route: planner-direct

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Assistants gate_version check misses ready/leased review and completion paths, and SqlStore sync misses merge_seed and malformed-JSON epoch monotonicity

* Related IDs: FR-4, AC-3, C14, C17, C18, P02-T01, P02-T02
* Evidence: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md (`P02-T01` steps 3-4, `P02-T02` step 4); src/core/src/zava_forward/core/assistants.py (`suspended` at lines 840-842, `export` at line 884, `disabled` at lines 906-910, `_view` at line 1252, `_permit_block` at line 1775, `complete` at line 1857, `execute` at line 1999, `review` at line 2044); src/core/src/zava_forward/core/continuity.py (`load` at lines 72-76, `reason_text` at lines 140-143); src/core/src/zava_forward/core/sqlstore.py (`_initialize` at lines 163-204, `merge_seed` at lines 940-941); src/api/tests/test_operator_suspension.py (lines 422-430); src/core/tests/test_seed_merge.py (lines 49-58, 146-151)
* Concern: Two fail-closed synchronization gaps exist across `SqlStore` and `Assistants`:
  1. `P02-T02` places the `continuity_gate_state.gate_version == continuity.GATE_VERSION` check in `Assistants.disabled()`. However, `Assistants._permit_block`, `Assistants.complete`, `Assistants.execute` (post-claim check), `Assistants._view` / `Assistants.review`, and `Assistants.export` call `self.suspended(db, capability)` directly without calling `self.disabled()`. Under a bumped `gate_version` (for example `'continuity-gate-v2'`), an old image could still `review(..., "accept")` an already-`ready` proposal or `complete()` an already-`leased` proposal without quarantining it. Also, `continuity.reason_text(s)` indexes `s["id"]`, so a synthetic hold dict lacking `"id"` will raise `KeyError`.
  2. On initialization, `merge_seed`, and corruption fixtures: `SqlStore.merge_seed(..., apply=True)` inserts missing `meta` documents (`sqlstore.py:940-941`) without calling `_proc_write`; `Assistants.migrate()` can run before `SqlStore` has synced pre-existing `meta('continuity')` holds on custom harnesses; and `continuity.load(raw)` calls `json.loads(raw)` without catching `ValueError`/`TypeError`. If a test or corrupted store writes invalid JSON or lowers/omits `epoch` in `meta('continuity')` (`C17`, `C18`) and `SqlStore` is reopened, `_migrate()` either crashes on `json.loads` or attempts to update `continuity_gate_state.epoch` to a smaller integer than already stored, tripping the monotonic `epoch` trigger and failing `SqlStore.__init__`.
* Impact: Old-image `review(accept)` and `complete()` remain open on `gate_version` mismatch, and reopening a store with corrupted `meta('continuity')` crashes initialization instead of failing closed cleanly on AI operations while preserving manual work (`AC-2`, `C17`, `C18`).
* Smallest useful change: Put the `continuity_gate_state` singleton + `gate_version == continuity.GATE_VERSION` check directly inside `Assistants.suspended(db, capability)` (and `SqlStore.continuity_suspension`), returning a complete synthetic hold dict (`{"id": "gate-mismatch", "scope": "all", "status": "Suspended", "gate_mismatch": True}`) handled cleanly by `continuity.reason_text`. Define `continuity.gate_sync_rows(raw_value, current_sql_epoch=0)` to catch JSON/type errors, clamp `safe_epoch = max(current_sql_epoch, parsed_nonneg_int_epoch)` so sync never decrements `continuity_gate_state.epoch`, project `[("all", "invalid-history", safe_epoch)]` only when a `meta('continuity')` row exists and fails `history_valid`, and invoke sync from `SqlStore._migrate`, `_seed`, `merge_seed(apply=True)`, `_proc_write`, and `Assistants.migrate()` (when `meta` exists).
* Action owner: planning parent
* Exact resolving evidence: `P02-T01` and `P02-T02` route `gate_version` verification through `Assistants.suspended` and `SqlStore.continuity_suspension`, support `gate_mismatch` in `continuity.reason_text`, sync in `merge_seed(apply=True)` and `Assistants.migrate()`, and clamp `safe_epoch >= current_sql_epoch` with JSON-error handling.
* Decision route: planner-direct

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Placeholder regex false-positives on valid corrective prose, anti-replay leaves concurrent/casefolded test_id gaps, and JSON incident_validation persistence assumes self.local

* Related IDs: FR-1, FR-2, AC-1, C1-C4, P01-T01, P01-T02
* Evidence: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md (`P01-T01`, `P01-T02`); src/core/src/zava_forward/core/restart_authority.py (`_EXACT_PLACEHOLDERS` and `_PLACEHOLDER_PATTERNS` at lines 20-56); src/core/src/zava_forward/core/continuity.py (`suspend` at line 483, `restart_propose` at line 535, `restart_decide` at line 615); src/api/tests/test_continuity_epoch_export.py (lines 1096-1102)
* Concern: Three edge cases affect Phase 1:
  1. `P01-T01` reuses `_PLACEHOLDER_PATTERNS` directly for `validate_corrective_evidence` (up to 600 chars of free-text remediation/test prose). `_PLACEHOLDER_PATTERNS[0]` matches `\b(?:tbd|todo|tbc|placeholder|unappointed|unassigned|unapproved)\b` anywhere in the string, which is appropriate for a person/role authority field (`OD-35`) but false-positives on legitimate corrective evidence descriptions such as `"Regression pack rejects placeholder authority and unassigned owner"`, while needing to keep existing valid test tokens like `test_id="constructed"` (`test_continuity_epoch_export.py:1098`) valid. Also, `restart_decide("Restart")` does not re-validate `p["corrective_evidence"]` and `p["test_id"]` if a proposal was persisted before upgrade or tampered in storage.
  2. `P01-T02` checks `test_id` only against `other["restart"]["proposal"]["test_id"]` (exact string) and exact `(test_id, corrective_evidence)` pairs from `"Keep suspended"` decisions. This permits (a) case-variant `test_id` replay (`"SYN-TEST-1"` vs `"syn-test-1"`), (b) reusing an already-rejected `"Keep suspended"` `test_id` by tweaking one word of `corrective_evidence` without running a new test (no existing suite reuses a `test_id` after a committed `"Keep suspended"` decision), and (c) proposing the same `test_id` concurrently across two open task-scope suspensions before either is decided unless both `restart_propose` (against open proposals and restarted incidents) and `restart_decide("Restart")` (against restarted incidents) check normalized `test_id.strip().casefold()`.
  3. In `continuity.py:535` and `615`, `restart_propose` and `restart_decide` access `self.local.incident_validation["persisted"] = True` unconditionally rather than `(self.local if hasattr(self, "db") else self).incident_validation["persisted"] = True` as `suspend` does at line 483.
* Impact: Legitimate corrective evidence prose can be rejected with `400`, case-changed or concurrently cloned `test_id` claims can be replayed across incidents, and non-SQL `Store` calls hit `AttributeError` if reaching the post-save marker.
* Smallest useful change: In `P01-T01`, define prose-safe placeholder detection for `validate_corrective_evidence` (exact placeholder tokens, leading `^(?:pending|tbd|todo|tbc|placeholder|unavailable)\b`, chat-memory/thread citations, and self/automatic-approval claims, without banning domain words mid-sentence) and call it in both `restart_propose` and `restart_decide("Restart")`. In `P01-T02`, normalize `test_id` with `.strip().casefold()`, reject reuse of any `test_id` from prior `"Keep suspended"` decisions on the suspension, any other open suspension's active `proposal`, or any `"Restarted"` suspension in `restart_propose`, re-verify against `"Restarted"` suspensions in `restart_decide("Restart")`, and guard `incident_validation["persisted"]` with `(self.local if hasattr(self, "db") else self)`.
* Action owner: planning parent
* Exact resolving evidence: `P01-T01` and `P01-T02` specify prose-safe regex rules, normalized `.casefold()` anti-replay across rejected/open/restarted proposals in both `restart_propose` and `restart_decide`, and safe `incident_validation` holder access.
* Decision route: planner-direct

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: FR-2 and P03-T02 conflate outer HTTP 403 view_only rejection with store-level audited denials and blur endpoint routing

* Related IDs: FR-2, AC-1, C5, C6, P01-T02, P03-T02
* Evidence: .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-plan.md (`FR-2` at line 79); .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md (`P03-T02` at lines 295-303); src/api/src/zava_forward/api/server.py (`do_POST` `view_only` guard at lines 1395-1396, `/api/continuity/*` dispatch at lines 1485-1501); src/api/src/zava_forward/api/auth.py (`ADMIN_EFFECTIVE_ROLE` at line 47, `TrustedProxyProvider.authenticate` at lines 143-157); src/core/src/zava_forward/core/continuity.py (`_incident_action` at lines 345-372)
* Concern: `FR-2` asserts that both Core and HTTP tests verify `400`/`403` *with audited denial on every negative case*. However, in `server.py:1395-1396`, `do_POST` intercepts `if u.get("view_only") and url.path != "/api/logout"` and immediately returns HTTP `403` before dispatching to `s.suspend`, `s.restart_propose`, or `s.restart_decide`. Therefore, an HTTP request from a `ZavaForward.ApplicationAdmin` + `ZavaForward.AIRestart` principal without a staff role (`view_only=True`) returns `403` without writing a store `ai_restart_*_denied` audit entry, whereas calling Core `Store.restart_decide` directly with that principal reaches `_incident_action` (because `ADMIN_EFFECTIVE_ROLE` maps to `"Retrofit Programme Manager"` in `MANAGER_ROLES`) and writes `ai_restart_decide_denied` once `P01-T02`'s `view_only` check raises `PermissionError`. In addition, `P03-T02` lists `"placeholder corrective evidence (400)"` and `"consumed test_id on SUS-2 (403)"` under `/api/continuity/restart-decide` and `/api/continuity/restart-propose` without clarifying that `corrective_evidence` and `test_id` payloads belong to `/api/continuity/restart-propose` (`restart-decide` accepts `{id, epoch, proposal_digest, decision, authority_ref}`).
* Impact: Implementing `P03-T02` literally will fail an audit-entry count assertion on the HTTP `ApplicationAdmin` (`view_only=True`) subtest or send `corrective_evidence` to the wrong HTTP endpoint.
* Smallest useful change: Clarify `FR-2` and `P03-T02` so that: (1) store-dispatched negative cases assert `ai_restart_propose_denied` / `ai_restart_decide_denied` audit entries at both Core and HTTP, while the outer HTTP `view_only` (`ApplicationAdmin`) guard asserts HTTP `403` + unchanged continuity state at HTTP and `PermissionError` + `ai_restart_*_denied` audit when invoked directly on Core `Store` (`P03-T01`); and (2) `P03-T02` explicitly maps placeholder `corrective_evidence` (`400`) and consumed/rejected `test_id` (`403`) to `POST /api/continuity/restart-propose` (and stale `epoch` / concurrently consumed `test_id` `403` to `POST /api/continuity/restart-decide`).
* Action owner: planning parent
* Exact resolving evidence: `FR-2`, `P03-T01`, and `P03-T02` distinguish outer HTTP RBAC `403` (`view_only=True`) from store-audited denials and map each negative subtest to its exact HTTP route.
* Decision route: planner-direct

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Strict mypy configuration in src/core and src/api rejects direct calls to untyped Core symbols when pyproject.toml edits are excluded

* Related IDs: NFR-2, AC-4, P03, P03-T01, P03-T02, P04-T02
* Evidence: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md (`P03` Boundaries at line 244, `P03-T01`, `P03-T02`); src/core/pyproject.toml (lines 14-60); src/api/pyproject.toml (lines 14-59); src/core/tests/test_operator_suspension_drill.py (lines 25-31)
* Concern: `P03` Boundaries explicitly forbid modifying `pyproject.toml` typing overrides. Under `src/core/pyproject.toml`, `strict = true` (`disallow_untyped_calls = true`, `disallow_untyped_defs = true`, `disallow_any_generics = true`) applies to any new `tests.test_*` module not listed in the legacy override table, while `sqlstore`, `mssqlstore`, `continuity`, `assistants`, `store`, `dataset`, and `release_support` are untyped (`ignore_errors = true`). Calling `SqlStore(...)`, `Assistants(...)`, `continuity.*`, `dataset.*`, or `release_support.*` directly inside `src/core/tests/test_continuity_restart_gate.py` triggers `mypy` `[no-untyped-call]` errors unless untyped imports are bound through explicit `: Any` aliases as done in `src/core/tests/test_operator_suspension_drill.py:25-31`. Likewise, `src/api/pyproject.toml` enforces `strict = true` on `tests.test_continuity_restart_gate` for all function annotations, generics, and any imported local test helpers not covered by `follow_imports = "skip"`.
* Impact: Phase 4 `mypy` validation (`P04-T02`) will fail with `[no-untyped-call]` or `[no-untyped-def]` unless the `: Any` boundary convention is planned into `P03-T01` and `P03-T02`.
* Smallest useful change: Document in `P03-T01` and `P03-T02` that both new test files must provide complete type annotations (`-> None` and parameterized generics) and bind untyped Core/fixture modules or classes through `: Any` boundary aliases mirroring `src/core/tests/test_operator_suspension_drill.py:25-31`, keeping `pyproject.toml` unchanged.
* Action owner: planning parent
* Exact resolving evidence: `P03-T01` and `P03-T02` explicitly specify `: Any` boundary aliases for untyped modules/classes and strict function/generic annotations so `mypy` passes with zero `pyproject.toml` changes.
* Decision route: planner-direct

## Strengths and Residual Risk

* Architecture Option B (`continuity_gate_state` + `continuity_open_holds` + database triggers on `assistant_attempts`) directly closes the true root cause identified in `C15` (an old worker binary omitting Python-side suspension queries during `_reserve` / `_fence_in`) at the SQL engine layer without requiring an external governance service.
* Phase 3 cleanly pairs deterministic `threading.Barrier` race tests across `pending` (`queued`), `leased`, and `ready` assistant proposals with an actual child `subprocess` worker simulation and end-to-end manual fallback, accessible digital/non-digital resident challenge, and statutory Awaab's Law emergency hazard checks, staying within the `<= 25` combined test-method budget.
* Residual risk (explicitly accepted and documented under `NFR-1` / `Refs #122`): Local SQLite and offline T-SQL DDL/portability checks prove software and SQL-contract enforcement, while live throwaway SQL Server trigger execution (`ZF_TEST_MSSQL=1` in hosted CI) and human-witnessed Azure deployment drills (`OD-35` / `RULE-020` / Issue #122 AC 4) remain external to local `Refs #122` execution.

## Questions or Blocking Evidence Gaps

* None. Every finding is resolvable directly from the supplied repository code and research artifacts without user intervention.

## Limitations

* This critique is a static, read-only credibility assessment against the supplied plan, phase details, research (`C1` through `C18`), and canonical `src/core` and `src/api` source/test files; it did not mutate repository files or execute live `ZF_TEST_MSSQL=1` SQL Server containers.

## Recommended Next Action

* Highest-impact finding: `PC-001` (SQLite and T-SQL trigger NULL fail-open on scalar subquery, invalid T-SQL `NEW`/`OLD` pseudo-record syntax, and T-SQL `VARCHAR` vs `NVARCHAR ... BIN2` collation mismatch in `P02-T01` / `P02-T02`).
* Action owner: planning parent
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-plan.md` and `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md` to incorporate planner-direct fixes `PC-001` through `PC-007` (plus adding `src/api/tests/test_mssqlstore.py` and `src/api/tests/test_assistants.py` to the canonical target list for MSSQL teardown table registration), then finalize the plan to `Ready for implementation` without another critique pass.
* User response required: No
