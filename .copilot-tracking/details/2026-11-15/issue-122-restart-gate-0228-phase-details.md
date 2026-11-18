<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #122 Local RAI Incident, Restart Gate, Suspension Fallback, and SQL Old-Image Exclusion

## Metadata

* Task ID: issue-122-restart-gate-0228
* Task slug: issue-122-restart-gate-0228
* Related plan: .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-research.md (`C1`-`C18`)

## Phase Index

| Phase ID | Name                                                                          | Status | Detail sections          |
|----------|-------------------------------------------------------------------------------|--------|--------------------------|
| P01      | Harden Restart Gate Corrective Evidence, Anti-Replay, and Identity Controls   | Ready  | P01, P01-T01, P01-T02    |
| P02      | Enforce SQL Continuity Gate Protocol and Old-Image Exclusion Triggers         | Ready  | P02, P02-T01, P02-T02    |
| P03      | Author Core, HTTP, Suspension-Fallback, Concurrency, and Old-Image Restart Tests | Ready | P03, P03-T01, P03-T02  |
| P04      | Update Component Documentation and Execute Validation Gate                    | Ready  | P04, P04-T01, P04-T02    |

<!-- rpi:phase id=P01 -->
## P01: Harden Restart Gate Corrective Evidence, Anti-Replay, and Identity Controls

### Context

`continuity.py` and `restart_authority.py` (`C2`, `C3`, `C4`) enforce RULE-024 human restart authority naming, constructed-fixture test gating, trusted-proxy OID + `ai_restart` capability checks, and multi-person separation. However, `restart_propose` currently validates `corrective_evidence` and `test_id` only through `controls.evidence_text` (allowing `"Unavailable"`, `"TBD"`, `"none"`, `"n/a"`, `"pending"`), permits replaying a `(test_id, corrective_evidence)` claim rejected by `"Keep suspended"` or reusing a `test_id` already consumed by an earlier `"Restart"`, does not guard against `view_only=True` user mappings, and omits an `actor` identity snapshot on `restart_decide` records.

### Intent

Ensure restart proposals and decisions require substantive, unconsumed corrective evidence and non-view-only authorized human actors, with immutable `actor` identity snapshots retained on restart decisions.

### Boundaries

* Included: `restart_authority.py` and `continuity.py` validation, anti-replay, `view_only` refusal, and `actor` snapshot recording.
* Excluded: Granting live non-constructed restart (`actual_hold` must stay `True` and `evidence_class="constructed-fixture"` mandatory).

### Likely Targets

* `src/core/src/zava_forward/core/restart_authority.py`: Add strictly typed `validate_corrective_evidence`.
* `src/core/src/zava_forward/core/continuity.py`: Enforce `validate_corrective_evidence`, anti-replay, `view_only` check, and `actor` snapshot in `suspend`, `restart_propose`, and `restart_decide`.

### Dependencies

* None.

### Validation Expectations

* Existing `test_continuity.py`, `test_operator_suspension.py`, and `test_operator_suspension_drill.py` continue to pass (`"Reviewed."`, `"synthetic:tests"`, `"synthetic:corrective-tests-221"`, and `"constructed-negative-and-fallback-drill"` remain valid).
* Placeholder/unavailable strings, Keep-suspended-replayed claims, Restart-consumed `test_id` values, and `view_only` callers fail closed with audited denial entries.

### Completion Evidence

* Updated `restart_authority.py` and `continuity.py` passing `ruff`, `mypy`, and unit assertions.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add substantive corrective-evidence validator in `restart_authority.py`

#### Context

`controls.evidence_text` (`C2`) strips whitespace and blocks chat-memory references (`controls.MEMORY_REF`), whereas `restart_authority.py` (`C4`) already maintains `_EXACT_PLACEHOLDERS` and `_PLACEHOLDER_PATTERNS` without echoing raw inputs in exception messages.

#### Intent

Provide `validate_corrective_evidence(value: object, *, label: str, limit: int) -> str` in `restart_authority.py` using prose-safe checks: strip whitespace, enforce `1 <= len(text) <= limit`, reject chat-memory/thread citations (`controls.MEMORY_REF`), reject exact placeholder tokens (`_EXACT_PLACEHOLDERS`), reject leading placeholder/unavailability prefixes (`^(?:pending|tbd|todo|tbc|placeholder|unavailable)\b`), and reject self/automatic-approval claims, without banning legitimate domain words (`placeholder`, `unassigned`) mid-sentence in remediation prose and while keeping `test_id="constructed"` (`test_continuity_epoch_export.py`) valid.

#### Boundaries

* Included: Strictly typed helper in `restart_authority.py` raising `ValueError` (without echoing raw input) on invalid or placeholder evidence.
* Excluded: Rejecting legitimate concise test strings (`"Reviewed."`, `"constructed"`, `"synthetic:tests"`, `"synthetic:corrective-tests-221"`) or multi-word remediation prose.

#### Likely Targets

* `src/core/src/zava_forward/core/restart_authority.py`: Add `validate_corrective_evidence`.

#### Dependencies

* None.

#### Validation Expectations

* `mypy` and `ruff` pass strictly on `restart_authority.py`; unit tests verify rejection of all placeholder/unavailable/chat-memory forms and acceptance of valid corrective claims.

#### Completion Evidence

* `validate_corrective_evidence` exported in `restart_authority.py` and covered in `test_restart_gate_sql_fences.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Enforce corrective-claim anti-replay, `view_only` refusal, and approver `actor` snapshot in `continuity.py`

#### Context

In `continuity.py` (`C2`, `C3`), `"Keep suspended"` appends to `s["decisions"]` and clears `s["proposal"]`, while `"Restart"` records `s["restart"]` with `proposal=p`. Without anti-replay checks against prior rejected decisions and prior consumed restarts, a rejected `(test_id, corrective_evidence)` pair or a previously consumed `test_id` can be replayed. In addition, `restart_decide` currently stores `by=user["email"]` without `actor={email, name, code, oid}`.

#### Intent

1. Refuse `user.get("view_only")` with `PermissionError` in `suspend`, `restart_propose`, and `restart_decide`.
2. Validate `corrective_evidence` and `test_id` via `validate_corrective_evidence` in `restart_propose` and re-verify `p["corrective_evidence"]` and `p["test_id"]` in `restart_decide` when `decision == "Restart"`.
3. Normalize `test_id` via `.strip().casefold()` for anti-replay:
   * In `restart_propose`, refuse reusing any normalized `test_id` recorded on a prior `"Keep suspended"` decision in `s.get("decisions", [])`, attached to another open suspension's active `proposal` in `doc["suspensions"]`, or already consumed by a committed `"Restart"` decision (`other.get("restart", {}).get("proposal", {}).get("test_id")`) in `doc["suspensions"]`.
   * In `restart_decide` when `decision == "Restart"`, re-verify that `p["test_id"].strip().casefold()` has not been consumed by any `"Restarted"` suspension in `doc["suspensions"]`.
4. Record `actor={key: user.get(key) for key in ("email", "name", "code", "oid")}` on `rec` in `restart_decide`, and guard `(self.local if hasattr(self, "db") else self).incident_validation["persisted"] = True` in `restart_propose` and `restart_decide` so non-SQL `Store` callers never hit `AttributeError`.

#### Boundaries

* Included: `ContinuityMixin.suspend`, `ContinuityMixin.restart_propose`, and `ContinuityMixin.restart_decide` in `continuity.py`.
* Excluded: Changing proposer-vs-suspender allowance (existing tests intentionally let `self.pm` suspend and propose while a distinct third actor decides).

#### Likely Targets

* `src/core/src/zava_forward/core/continuity.py`: Import `validate_corrective_evidence` and enforce anti-replay, `view_only`, and `actor` snapshot rules.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Replaying `restart_decide` after `"Restart"` or `"Keep suspended"`, re-proposing a rejected `(test_id, corrective_evidence)` after `"Keep suspended"`, or reusing a consumed `test_id` on a new incident `SUS-2` fails closed and writes an `ai_restart_*_denied` audit entry.

#### Completion Evidence

* Updated `continuity.py` passing existing and new unit/HTTP restart matrices.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Enforce SQL Continuity Gate Protocol and Old-Image Exclusion Triggers

### Context

`src/core/README.md:4580` (`C16`) and the Issue #122 closure audit note that pre-gate (legacy) images were not excluded from serving by any repository control. Contrarian analysis (`C6`, `C7`, `C17`, `C18`) showed that normalized SQL tables (`continuity_gate_state`, `continuity_open_holds`) plus database triggers on `continuity_gate_state` and `assistant_attempts` (`capability`, `gate_version`, `send_gate_version`) enforce fail-closed old-image exclusion in both SQLite and T-SQL without breaking raw `meta ('continuity')` or `assistant_tasks.body` corruption fixtures.

### Intent

Prevent pre-gate or gate-mismatched worker/API images from reserving capacity, transitioning attempts to `'sending'`, dispatching while suspended, or rolling back the continuity epoch on shared SQLite and Azure SQL / SQL Server stores.

### Boundaries

* Included: `continuity.py`, `sqlstore.py`, `mssqlstore.py`, and `assistants.py` schema, migrations, triggers, transactional synchronization, and gate-version checks.
* Excluded: Raw triggers on `meta` or `assistant_tasks.body` (preserving `C17` and `C18` corruption test fixtures); keeping `continuity_open_holds` scoped to `status == "Suspended"` incidents so constructed restart drills (`s["status"] == "Restarted"`, `actual_hold=True`) continue to work for synthetic test doubles while live `Ai` stays blocked by `actual_hold=True`.

### Likely Targets

* `src/core/src/zava_forward/core/continuity.py`: Define `GATE_VERSION = "continuity-gate-v1"` and helper `open_hold_rows(doc)` extracting `(scope, incident_id, epoch)` rows when `history_valid(doc)` (or `('all', 'invalid-history', max_epoch)` if history is malformed).
* `src/core/src/zava_forward/core/sqlstore.py`: Create/migrate `continuity_gate_state` and `continuity_open_holds` + SQLite triggers, synchronize them inside `_seed` / `_migrate` / `_proc_write`, and check `continuity_gate_state.gate_version` in `continuity_suspension`.
* `src/core/src/zava_forward/core/mssqlstore.py`: Add `continuity_gate_state` and `continuity_open_holds` to `TABLES` and T-SQL triggers (`continuity_gate_state_guard`) in `_create_schema` / `_create_indexes`.
* `src/core/src/zava_forward/core/assistants.py`: Ensure `Assistants.migrate()` creates/migrates `continuity_gate_state`, `continuity_open_holds`, `assistant_attempts` columns (`capability`, `gate_version`, `send_gate_version`), and SQLite/T-SQL `assistant_attempts` gate triggers; stamp and check `continuity.GATE_VERSION` in `_reserve`, `_fence_in`, and `disabled`.

### Dependencies

* P01.

### Validation Expectations

* Any raw SQL `INSERT INTO assistant_attempts` without `gate_version='continuity-gate-v1'` or `UPDATE assistant_attempts SET outcome='sending'` without `send_gate_version='continuity-gate-v1'` aborts in SQLite and generates matching `THROW` triggers in T-SQL.
* Any `'reserved'` or `'sending'` write on `assistant_attempts` while `continuity_open_holds` covers `'all'` or `capability` aborts at the SQL trigger layer.
* Decreasing `continuity_gate_state.epoch` or deleting `continuity_gate_state` aborts at the SQL trigger layer.
* If `continuity_gate_state.gate_version` in SQL is upgraded to a newer string (e.g., `'continuity-gate-v2'`), an older `v1` `SqlStore` / `Assistants` process fails closed (`continuity_suspension` / `disabled`) while manual case work, accessible challenge, and hazard routes remain available.

### Completion Evidence

* Updated `continuity.py`, `sqlstore.py`, `mssqlstore.py`, and `assistants.py` passing all existing SQL/assistant/corruption tests plus new SQL fence tests.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Persist `continuity_gate_state` and `continuity_open_holds` with monotonic SQLite/T-SQL triggers in `continuity.py`, `sqlstore.py`, and `mssqlstore.py`

#### Context

`SqlStore` (`C8`, `C9`) stores `continuity` JSON in `meta` (`key='continuity'`) inside `BEGIN IMMEDIATE` transactions (`sp_getapplock` in `MssqlStore`, `C10`). Synchronizing normalized `continuity_gate_state` and `continuity_open_holds` tables inside the same transaction gives SQL triggers direct relational state without dialect-specific JSON parsing.

#### Intent

1. In `continuity.py`, define `GATE_VERSION = "continuity-gate-v1"`, `gate_mismatch_hold(found)` returning `{"id": "gate-mismatch", "scope": "all", "status": "Suspended", "gate_mismatch": True, "gate_version": found}`, update `reason_text` to report `gate_mismatch` cleanly without missing-key `KeyError`, and define `gate_sync_rows(raw_value, current_sql_epoch=0)` catching `ValueError`/`TypeError` on `json.loads`, clamping `safe_epoch = max(current_sql_epoch, parsed_nonneg_int_epoch)` so sync never lowers `continuity_gate_state.epoch`, and returning `(safe_epoch, holds)` where `holds` lists `(scope, incident_id, epoch)` for each open `status == "Suspended"` suspension when `history_valid(doc)` (or `[("all", "invalid-history", safe_epoch)]` when `raw_value is not None` and `doc` is malformed).
2. In `sqlstore.py` and `mssqlstore.py`, create `continuity_gate_state (id INTEGER PRIMARY KEY CHECK (id = 1), gate_version TEXT NOT NULL, epoch INTEGER NOT NULL)` and `continuity_open_holds (scope TEXT PRIMARY KEY, incident_id TEXT NOT NULL, epoch INTEGER NOT NULL)` (using `NVARCHAR(64) COLLATE Latin1_General_100_BIN2` in T-SQL), seed `(1, 'continuity-gate-v1', 0)` using portable `INSERT INTO continuity_gate_state (id, gate_version, epoch) SELECT 1, ?, 0 WHERE NOT EXISTS (SELECT 1 FROM continuity_gate_state WHERE id = 1)` (never raw `INSERT OR IGNORE` outside `_insert_ignore`), and install SQLite (`BEFORE DELETE` + `BEFORE INSERT` + `BEFORE UPDATE` with `RAISE(ABORT, ...)`) and set-based T-SQL (`INSTEAD OF DELETE` + `AFTER INSERT, UPDATE` over `inserted`/`deleted` with `THROW`) triggers preventing `DELETE`, blank `gate_version`, or `epoch` decrease. Also register the new tables/triggers in `src/api/tests/test_mssqlstore.py` and `src/api/tests/test_assistants.py` MSSQL teardown lists.
3. Synchronize `continuity_gate_state` (`epoch = safe_epoch`, preserving any existing non-empty `gate_version` if higher/different during read-only migrate or setting `continuity.GATE_VERSION` when initializing) and `continuity_open_holds` atomically inside `SqlStore._migrate`, `_seed`, `merge_seed(apply=True)`, and `_proc_write` (and `Assistants.migrate()` when `meta` exists).
4. In `SqlStore.continuity_suspension`, check `continuity_gate_state` singleton presence and `gate_version == continuity.GATE_VERSION` under `self.dblock`, returning `continuity.gate_mismatch_hold(found)` if missing or mismatched.

#### Boundaries

* Included: `continuity.py`, `sqlstore.py`, `mssqlstore.py`, `src/api/tests/test_mssqlstore.py`, and `src/api/tests/test_assistants.py`.
* Excluded: Blocking `merge_seed` or raw `meta` writes in `test_operator_suspension.py:426` / `test_seed_merge.py:147`.

#### Likely Targets

* `src/core/src/zava_forward/core/continuity.py`
* `src/core/src/zava_forward/core/sqlstore.py`
* `src/core/src/zava_forward/core/mssqlstore.py`
* `src/api/tests/test_mssqlstore.py`
* `src/api/tests/test_assistants.py`

#### Dependencies

* P01.

#### Validation Expectations

* `test_seed_merge.py`, `test_sqlstore.py`, `test_operator_suspension.py`, and new `continuity_gate_state` / `continuity_open_holds` unit tests pass.

#### Completion Evidence

* Relational gate tables and monotonic triggers active in SQLite and T-SQL schema builders.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Enforce `continuity-gate-v1` and open-hold SQL triggers on `assistant_attempts` in `assistants.py`

#### Context

`Assistants._reserve` (`C6`) is called from both `claim` (`tid` in `assistant_tasks`) and `begin_call` (`call_id` for direct calls such as `simulation_lane.CAPABILITY`), and `_fence_in` (`C7`) transitions `assistant_attempts.outcome` to `'sending'` immediately before network send or permit issuance.

#### Intent

1. In `Assistants.migrate()`, idempotently ensure `continuity_gate_state` (seeded via portable `WHERE NOT EXISTS`) and `continuity_open_holds` exist (and sync from `meta('continuity')` if `meta` exists), add `capability` (`DEFAULT ''` / `NVARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL DEFAULT N''`), `gate_version` (`DEFAULT ''` / `NVARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL DEFAULT N''`), and `send_gate_version` (`DEFAULT ''` / `NVARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL DEFAULT N''`) columns to `assistant_attempts` on both fresh and upgraded SQLite/T-SQL databases, and create NULL-safe fail-closed SQLite (`BEFORE INSERT`, `BEFORE UPDATE` with `RAISE(ABORT, ...)`) and set-based T-SQL (`AFTER INSERT, UPDATE` over `inserted` with `THROW`) triggers on `assistant_attempts` that abort/throw whenever:
   * `outcome = 'reserved'` and (`capability = ''` or `NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = <row>.gate_version)`),
   * `outcome = 'sending'` and (`capability = ''` or `NOT EXISTS (SELECT 1 FROM continuity_gate_state g WHERE g.id = 1 AND g.gate_version = <row>.gate_version AND g.gate_version = <row>.send_gate_version)`), or
   * `outcome IN ('reserved', 'sending')` and `EXISTS (SELECT 1 FROM continuity_open_holds h WHERE h.scope = 'all' OR h.scope = <row>.capability)`.
2. Pass `capability` into `Assistants._reserve(self, db, now, attempt, tid, fence, capability)` from `claim` (`task["capability"]`) and `begin_call` (`capability`), stamping `capability=capability` and `gate_version=continuity.GATE_VERSION`.
3. Stamp `send_gate_version=continuity.GATE_VERSION` (and backfill `capability` if empty) in `Assistants._fence_in` when updating `outcome='sending'`.
4. Check `continuity_gate_state` singleton presence and `gate_version == continuity.GATE_VERSION` directly inside `Assistants.suspended(db, capability)` (returning `continuity.gate_mismatch_hold(found)`) so `disabled()`, `review()`, `complete()`, `_permit_block()`, `execute()`, `_view()`, and `export()` all fail closed on gate mismatch.

#### Boundaries

* Included: `src/core/src/zava_forward/core/assistants.py`.
* Excluded: Altering `assistant_tasks` raw test-corruption behavior (`UPDATE assistant_tasks SET body=...` in existing tests remains unaffected).

#### Likely Targets

* `src/core/src/zava_forward/core/assistants.py`

#### Dependencies

* P02-T01.

#### Validation Expectations

* All existing `test_assistants*.py`, `test_permit_sql.py`, `test_ai_consumption_api.py`, `test_continuity*.py`, and new pre-gate trigger/subprocess tests pass.

#### Completion Evidence

* SQLite and T-SQL triggers on `assistant_attempts` enforced and verified.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Author Core, HTTP, Suspension-Fallback, Concurrency, and Old-Image Restart Tests

### Context

To prove Criteria 1, 2, and 3 end-to-end without gaps, tests must cover both core/SQL invariants and HTTP `TrustedProxyProvider` / `PasswordProvider` boundaries, accessible digital + non-digital challenges and statutory hazards during suspension, concurrent multi-connection suspend/review/dispatch races, and `subprocess` old-image restarts across `queued`, `leased`, and `ready` proposals.

### Intent

Add two focused, strictly typed test modules (`src/core/tests/test_restart_gate_sql_fences.py` and `src/api/tests/test_continuity_restart_gate.py`) within the <= 25-method test budget, with zero removals of existing tests.

### Boundaries

* Included: `src/core/tests/test_restart_gate_sql_fences.py` and `src/api/tests/test_continuity_restart_gate.py` using complete `-> None` / generic annotations and `: Any` boundary aliases for untyped Core/fixture symbols (`src/core/tests/test_operator_suspension_drill.py:25-31`).
* Excluded: Modifying `pyproject.toml` typing overrides.

### Likely Targets

* `src/core/tests/test_restart_gate_sql_fences.py`
* `src/api/tests/test_continuity_restart_gate.py`

### Dependencies

* P01, P02.

### Validation Expectations

* Both new test modules pass `unittest`, `ruff check`, `ruff format --check`, and `mypy --strict` cleanly and deterministically without sleeps or flaky timing assumptions (using `threading.Barrier`, deterministic clock/lease expiry, and bounded `subprocess.run` workers).

### Completion Evidence

* Passing test output recorded in `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add `src/core/tests/test_restart_gate_sql_fences.py` for core restart, suspension availability, and SQL trigger/T-SQL invariants

#### Context

Core tests in `src/core` run without HTTP scaffolding and directly verify `restart_authority`, `continuity`, `SqlStore`, `MssqlStore` DDL generation, `Assistants`, `ChallengeRegister`, `resident_decisions`, and `hazard`.

#### Intent

Verify in `src/core/tests/test_restart_gate_sql_fences.py`:
1. `validate_corrective_evidence` and `restart_propose`/`restart_decide` rejection of placeholder/unavailable/chat-memory claims, Keep-suspended claim replay, Restart-consumed `test_id` replay across incidents, `view_only` principals, and retention of approver `actor` OID snapshot.
2. During active `all`-scope suspension, task-scope suspension, and SQL `gate_version` mismatch (`continuity-gate-v2`), manual case actions (`log_call`, `set_decision`), `ChallengeRegister` (`digital` and `staff_recorded` `phone`, `in_person`, `paper`, `assisted_visit`, plus `hazard_concern=True` immediate referral), `Store.resident_action` (`challenge_open` across non-digital channels, `challenge_update`, `challenge_escalate` to distinct owner, `challenge_resolve` with `"Correction recorded"` marking AI priority suggestion `stale=True` and `priority_correction=1` while preserving consent and hazard clocks), AI suggestion `reject`, and statutory hazard progression (`raise_hazard`, `refer_hazard`, `receive_hazard`, `accept_hazard`, `observe_hazard_times`, `record_repair`, `release_hazard`) all succeed across reopened SQL connections.
3. SQLite triggers on `continuity_gate_state` and `assistant_attempts` abort pre-gate `'reserved'` inserts (default empty `gate_version`), pre-gate `'sending'` updates (default empty `send_gate_version`), open-hold `'reserved'`/`'sending'` writes, and `epoch` decreases or row deletion, and `MssqlStore` / `Assistants(mssql=True)` emit the matching T-SQL DDL and `THROW` triggers.

#### Boundaries

* Included: `src/core/tests/test_restart_gate_sql_fences.py` (<= 12 focused test methods).
* Excluded: Live external SQL Server network dependency.

#### Likely Targets

* `src/core/tests/test_restart_gate_sql_fences.py`

#### Dependencies

* P01, P02.

#### Validation Expectations

* `python -m unittest discover -s tests -p 'test_restart_gate_sql_fences.py'` in `src/core`, plus `ruff` and `mypy`.

#### Completion Evidence

* Passing `src/core` unit, lint, format, and mypy runs.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Add `src/api/tests/test_continuity_restart_gate.py` for HTTP `TrustedProxyProvider`, suspension fallback, concurrent races, and subprocess old-image restart

#### Context

`server.py` (`C14`) wires `/api/continuity/restart-decide` with `trusted_route=app.provider.name == "trusted-proxy"` and `TrustedProxyProvider` (`C15`) maps `ZavaForward.AIRestart` vs `ZavaForward.ApplicationAdmin` (`view_only=True`). Criterion 3 also requires independent SQL connection, concurrent suspend/review/race, and old-image restart coverage across `queued`, `leased`, and `ready` proposals.

#### Intent

Verify in `src/api/tests/test_continuity_restart_gate.py`:
1. **HTTP Restart Gate Matrix (`TrustedProxyProvider` & `PasswordProvider`)**:
   * Password-authenticated `POST /api/continuity/restart-decide` returns 403 (`trusted_route=False`) with `ai_restart_decide_denied` audit.
   * `TrustedProxyProvider` requests fail closed: outer HTTP RBAC `view_only=True` (`ZavaForward.ApplicationAdmin` + `ZavaForward.AIRestart` without staff role) returns 403 before reaching the store with continuity unchanged (while direct Core `Store` calls in `P03-T01` write `ai_restart_*_denied`); `POST /api/continuity/restart-propose` rejects placeholder corrective evidence (400) and Keep-suspended/concurrent/Restart-consumed `test_id` values (403) with `ai_restart_propose_denied`; and `POST /api/continuity/restart-decide` rejects manager without `ZavaForward.AIRestart` (403), suspender self-approval (403), proposer self-approval (403), distinct roster email sharing proposer/suspender Entra `oid` (403), stale `epoch` (403), superseded `proposal_digest` after re-proposal or `"Keep suspended"` (403), candidate release/model drift before decision (403), mismatched `authority_ref` (403), `automatic=True` (403), and replayed POST after `"Restart"` (400) with `ai_restart_decide_denied`, while a distinct OID-bound `ZavaForward.AIRestart` manager succeeds (200) with `actual_hold=True` preserved.
2. **HTTP Manual, Accessible Challenge, and Hazard Availability During Suspension**:
   * While `all` AI work is suspended via `/api/continuity/suspend` (blocking `/api/ai/priority`, `/api/cases/<id>/ai`, and `/api/assistants/<cap>/invoke`), HTTP requests to `/api/cases/<id>/call`, `/api/cases/<id>/decision`, `/api/cases/<id>/resident` (`challenge_open` via `Phone` and `Digital`, `challenge_update`, `challenge_escalate`, `challenge_resolve` with `"Correction recorded"`), `/api/ai/priority/<id>/reject`, `/api/assistants/proposals/<id>/review` (`reject`), and `/api/cases/<id>/hazard-raise`..`hazard-release` succeed (200) and persist across a second `App`/`SqlStore` instance.
3. **Independent SQL Connection, Concurrent Suspend/Review Race, and Subprocess Old-Image Restart (`queued`, `leased`, `ready`)**:
   * Concurrent `threading.Barrier` races across independent `SqlStore` / `Assistants` SQL connections: (a) `suspend` racing `assistants.review(accept)` on a `ready` proposal -> either `accept` commits strictly before suspension (and suspension then renders the accepted proposal `actionable=False`, `relied_on=False`) or `review(accept)` is refused by suspension, never leaving an actionable post-suspension acceptance, while `review(reject)` remains allowed; (b) `suspend` racing `claim` / `fence_send` / `issue_permit` / `complete_result` on `queued` and `leased` proposals -> `queued` disables with zero provider calls, `leased` permit/send withdraws or late completion quarantines (`state='quarantined'`, `output=None`, `actionable=False`).
   * Separate OS process (`subprocess.run(..., env={**os.environ, "PYTHONPATH": ...}, timeout=15)`) old-image restart tests against the shared SQLite file covering: (i) pre-gate legacy worker subprocess attempting raw pre-gate SQL reservation/send on `assistant_attempts` (aborted by SQL trigger, zero capacity leak), and (ii) restarted worker subprocess running an older model/prompt/release image (and post-restart new-epoch worker) encountering pre-existing `queued` (`pending` -> `disabled`), `leased` with expired lease (`epoch-stale` -> `disabled`, and `permitted`-marker -> `failed` `blocked-reclaim` with zero duplicate provider calls), and `ready` (`actionable=False`, `verify`/`accept` refused, `reject` allowed) proposals.

#### Boundaries

* Included: `src/api/tests/test_continuity_restart_gate.py` (<= 12 focused test methods).
* Excluded: Browser/Playwright tests (no web assets or UI templates change).

#### Likely Targets

* `src/api/tests/test_continuity_restart_gate.py`

#### Dependencies

* P01, P02.

#### Validation Expectations

* `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p 'test_continuity_restart_gate.py'` in `src/api`, plus `ruff` and `mypy`.

#### Completion Evidence

* Passing `src/api` unit, lint, format, and mypy runs.

#### Unresolved Items

* None.

<!-- rpi:phase id=P04 -->
## P04: Update Component Documentation and Execute Validation Gate

### Context

`src/core/README.md:4580` (`C16`) currently states that pre-gate (legacy) image exclusion is neither enforced nor evidenced in repository sources. Once P01-P03 are implemented, `src/core/README.md` and `src/api/README.md` must accurately reflect the SQL `continuity-gate-v1` exclusion triggers and corrective-claim anti-replay rules while keeping non-code Issue #122 boundaries (`actual_hold=True`, OD-35/OQ-017, witnessed drill, immutable external Azure head, accessibility acceptance) clearly flagged as unestablished.

### Intent

Synchronize component documentation and verify all `src/core` and `src/api` unit tests, linters, formatters, and strict type checks.

### Boundaries

* Included: `src/core/README.md`, `src/api/README.md`, validation runs, and RPI tracking reconciliation.
* Excluded: Claiming Issue #122 closure or pushing to remote.

### Likely Targets

* `src/core/README.md`
* `src/api/README.md`

### Dependencies

* P01, P02, P03.

### Validation Expectations

* Full unit discovery in `src/core` and `src/api`, `tools/rename-zava-tests.py`, `ruff check`, `ruff format --check`, and `mypy` exit 0.

### Completion Evidence

* Recorded command outputs in `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Document SQL `continuity-gate-v1` old-image exclusion and corrective-claim anti-replay in `src/core/README.md` and `src/api/README.md`

#### Context

Repository instructions require updating directly related component documentation and keeping assumptions, constructed controls, and unestablished operational approvals distinct.

#### Intent

Update `src/core/README.md` (around line 4580 and continuity control summary) and `src/api/README.md` (`/api/continuity/*` section) to document:
* Substantive non-placeholder corrective evidence and anti-replay of rejected/consumed corrective test claims.
* SQL-enforced `continuity-gate-v1` (`continuity_gate_state`, `continuity_open_holds`, and `assistant_attempts` triggers in SQLite and T-SQL) excluding pre-gate worker/API images from reserving or dispatching assistant calls on a migrated SQL store while explicitly noting that external container-platform rollout/routing controls, OD-35/OQ-017 human authority, witnessed drills, external immutable head custody, and accessibility sign-off remain separate non-code requirements.

#### Boundaries

* Included: `src/core/README.md`, `src/api/README.md`.
* Excluded: Overclaiming deployment-plane image admission or live governance approvals.

#### Likely Targets

* `src/core/README.md`
* `src/api/README.md`

#### Dependencies

* P01, P02.

#### Validation Expectations

* Markdown link/structure check via `git diff` review.

#### Completion Evidence

* Clean documentation diff aligned with runtime behavior.

#### Unresolved Items

* None.

<!-- rpi:task id=P04-T02 -->
### P04-T02: Run `src/core` and `src/api` test suites, `ruff check`, `ruff format --check`, and `mypy`, and reconcile RPI artifacts

#### Context

Focused validation tier applies to bounded `src/core` and `src/api` feature/test changes without workflow, Dockerfile, or dependency-manifest changes; running full `src/core` and `src/api` unit suites plus `ruff` and `mypy` guarantees zero regressions across siblings.

#### Intent

Execute using workspace-local `.venv-122-local` (and remove `.venv-122-local` before final git status verification):
* From `src/core`: `.venv-122-local/bin/python -m unittest discover -s tests -q`, `ruff check`, `ruff format --check`, `mypy`.
* From `src/api`: `PYTHONPATH=../core/tests:../agents/tests .venv-122-local/bin/python -m unittest discover -s tests -q`, `ruff check`, `ruff format --check`, `mypy`.
* From repo root: `.venv-122-local/bin/python tools/rename-zava-tests.py`.
* Reconcile `[x]` markers across plan, phase details, changes record, and session state JSON.

#### Boundaries

* Included: Local test/lint/format/type verification and tracking reconciliation.
* Excluded: Remote push.

#### Likely Targets

* `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-plan.md`
* `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md`
* `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-changes.md`

#### Dependencies

* P01, P02, P03, P04-T01.

#### Validation Expectations

* Every command exits 0 with zero unexpected skips or errors.

#### Completion Evidence

* Reconciled changes artifact ready for `rpi-review`.

#### Unresolved Items

* None.
