<!-- markdownlint-disable-file -->
# Review: Issue #122 Local RAI Incident, Restart Gate, Suspension Fallback, and SQL Old-Image Exclusion

## Scope and Evidence

* Task ID: issue-122-restart-gate-0228
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`, `P04`)
* Assessed boundary: Issue #122 local RAI Incident and Restart acceptance criteria 1, 2, and 3 across `src/core` and `src/api` (`FR-1` through `FR-4`, `NFR-1`, `NFR-2`, `AC-1` through `AC-4`), planner-direct critique dispositions `PC-001` through `PC-007`, implementation-time updates, validation coverage, and non-code follow-up items (`OD-35`/`OQ-017` human appointment, witnessed drills, Azure ledger-head custody, live `ZF_TEST_MSSQL=1` execution).
* Plan: .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-research.md (`C1` through `C18`); working-tree diff and untracked test modules across `src/core` and `src/api`; independent bounded read-only `rubber-duck` lens assessment.

## Opening Review State

* Interpreted review goal: Perform one evidence-based, read-only post-implementation review of `issue-122-restart-gate-0228` across `P01` through `P04`, keeping execution status separate from outcome verdict and routing any defect, decision/plan drift, evidence gap, or residual follow-up item to its canonical destination without mutating code or prior artifacts.
* Review scope: Full task (`P01`, `P02`, `P03`, `P04`)
* Evidence readiness: Ready; plan markers (`P01` through `P04` and `P01-T01` through `P04-T02`), phase details, single-pass plan critique (`PC-001` through `PC-007`), changes record (`Completed`), research (`C1` through `C18`), and validation outputs are present and synchronized.
* Acceptance basis: User prompt target acceptance criteria 1-3 for Issue #122, plan `FR-1` through `FR-4`, `NFR-1`, `NFR-2`, `AC-1` through `AC-4`, and critique dispositions `PC-001` through `PC-007`.
* First comparison boundary: Reconcile `P01` through `P04` plan/detail requirements and critique dispositions `PC-001` through `PC-007` against the actual `src/core` and `src/api` source, test, and README changes, excluding external owner-witnessed Azure drills and `OD-35` appointments tracked under `## Follow-Up Items`.
* Active read-only boundaries: Review may create and update only `.copilot-tracking/reviews/logs/2026-11-15/issue-122-restart-gate-0228-review.md` (plus RPI session state transitions owned by the parent RPI Agent); source, test, documentation, plan, detail, critique, research, and changes files are read-only during Review.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass read-only post-implementation review on 2026-11-15 across the full declared task scope (`P01` through `P04`, `P01-T01` through `P04-T02`), comparing `.copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-plan.md`, `.copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-changes.md`, `.copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-research.md`, and the uncommitted working-tree changes across `src/core` and `src/api`, supplemented by a bounded read-only `rubber-duck` lens check.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Restart Gate Corrective Evidence, Anti-Replay, and Identity Controls (`P01`) | Partial | `validate_corrective_evidence`, `_refuse_view_only`, `proposal_seq` digest anti-replay, and approver `actor` snapshots are implemented, but `_check_claim_replay` requires matching `corrective_evidence` (and `candidate` across suspensions) instead of rejecting normalized `test_id` reuse independently (`RV-001`). |
| `P02` (`P02-T01`, `P02-T02`) | SQL Continuity Gate Protocol and Old-Image Exclusion Triggers (`P02`) | Partial | `continuity_gate_state`, `continuity_open_holds`, and `assistant_attempts` triggers are wired in SQLite and T-SQL, plus implementation-time `gate_hold` alignment in `Assistants.export` and `Assistants._view`, but `assistant_attempts` hold-update triggers check `NEW.outcome <> OLD.outcome` (`RV-002`), `assistant_tasks` acceptance lacks a SQL gate trigger against genuine pre-gate images (`RV-003`), and `SqlStore._proc_sync` / `continuity.load("")` still fail or treat empty string as blank on startup (`RV-004`). |
| `P03` (`P03-T01`, `P03-T02`) | Core, HTTP, Suspension-Fallback, Concurrency, and Old-Image Restart Tests (`P03`) | Partial | 17 tests (8 in `src/core`, 9 in `src/api`, within the `<= 25` budget) pass, including core SQLite trigger checks and HTTP restart/manual/hazard coverage, but several planned `P03-T02` scenarios (`PasswordProvider` `restart-decide` 403, HTTP `challenge_update`/`challenge_escalate`, HTTP store-denial audit checks, genuine pre-gate `ready` review, and racing `verify` and mid-flight `_fence_in` directly against `suspend`) are incomplete (`RV-003`, `RV-005`). |
| `P04` (`P04-T01`, `P04-T02`) | Component Documentation and Validation Gate (`P04`) | Reconciled | `src/core/README.md` and `src/api/README.md` preserve all non-operative `OD-35`/`OQ-017`, witnessed-drill, accessibility, and custody disclosures, and `ruff check`, `ruff format --check`, strict `mypy`, and unit/regression suites ran cleanly. |
| `Follow-Up Items` | External governance/witnessed drill (`OD-35`/`OQ-017`/`RULE-020`) and Azure ledger-head/SQL drill | Reconciled | Both external non-code items remain outside active `Pxx` scope with named owners and `Refs #122` linkage. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/restart_authority.py` | Added prose-safe `_EVIDENCE_PLACEHOLDER_PATTERNS` and strictly typed `validate_corrective_evidence` (`min_len=4` default, `min_len=3` for `test_id`) without echoing raw inputs. | Implemented and exercised in `test_restart_gate_sql_fences.py` and `test_continuity_restart_gate.py`. | Passed (`unittest`, `ruff`, strict `mypy`) | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/continuity.py` | Added `_refuse_view_only`, `validate_corrective_evidence` re-verification on `Restart`, monotonic `proposal_seq`, `_check_digest_replay`, `_check_claim_replay`, approver `actor` snapshot, and SQL gate helpers. | Implemented, but `_check_claim_replay` gates on `(test_id, corrective_evidence[, candidate])` rather than normalized `test_id` independently. | Passed existing + new suites, but misses tweaked-prose `test_id` replay | Gap (`RV-001`) |
| `P02-T01` | `src/core/src/zava_forward/core/continuity.py`, `src/core/src/zava_forward/core/sqlstore.py`, `src/core/src/zava_forward/core/mssqlstore.py`, `src/api/tests/test_mssqlstore.py`, `src/api/tests/test_assistants.py` | Added `continuity_gate_state` and `continuity_open_holds` DDL + no-delete/monotonic triggers, `sync_sql_gate` calls, `SqlStore.continuity_suspension` `gate_hold`, and MSSQL teardown table drops. | Implemented, but `SqlStore._proc_sync` still parses `continuity` with raw `json.loads` on reopen and `continuity.load("")` returns `blank()`. | Passed unit/portability checks; startup corruption reopen gap found in review | Gap (`RV-004`) |
| `P02-T02` | `src/core/src/zava_forward/core/assistants.py` | Added `continuity_gate_state`, `continuity_open_holds`, `assistant_attempts` gate columns and SQLite/T-SQL triggers, and `gate_hold` checks in `suspended`, `export`, and `_view`. | Implemented for `assistant_attempts` transitions, but hold-update trigger omits same-outcome `sending` refreshes and `assistant_tasks` lacks a SQL trigger blocking genuine pre-gate `state='accepted'` writes. | Passed unit suites; trigger bypasses confirmed in review | Gap (`RV-002`, `RV-003`) |
| `P03-T01` | `src/core/tests/test_restart_gate_sql_fences.py` | Added 8 strictly typed `src/core` tests for corrective evidence, anti-replay, manual/accessible-challenge/hazard fallback, SQLite triggers, and T-SQL DDL parity. | 8/8 tests passing. | Passed (`unittest`, `ruff`, strict `mypy`) | Reconciled (needs explicit `PYTHONPATH` on subprocess per `PC-003` and updated assertions once `RV-001`..`RV-004` land) |
| `P03-T02` | `src/api/tests/test_continuity_restart_gate.py` | Added 9 strictly typed `src/api` tests for HTTP `TrustedProxyProvider`, suspension fallback, independent SQL connections, barrier races, and subprocess worker restarts. | 9/9 tests passing, but omits several planned sub-assertions and uses mutated `GATE_VERSION` rather than a genuine pre-gate worker for `ready` proposals. | Passed (`unittest`, `ruff`, strict `mypy`) | Gap (`RV-003`, `RV-005`) |
| `P04-T01` | `src/core/README.md`, `src/api/README.md` | Documented SQL `continuity-gate-v1`, anti-replay, `view_only` refusal, and suspension fallback while preserving non-operative governance/custody disclosures. | Diff inspected; no new `.copilot-tracking/` references introduced. | Markdown/diff inspected | Reconciled |
| `P04-T02` | `src/core`, `src/api`, `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-changes.md` | Ran focused and regression test suites, `tools/rename-zava-tests.py`, `ruff check`, `ruff format --check`, and strict `mypy`; removed `.venv-122-local`. | Validation table recorded in `changes.md`. | Passed | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P02-T02` (`src/core/src/zava_forward/core/assistants.py`: `Assistants.export`, `Assistants._view`) | Extended `Assistants.export` and `Assistants._view` to check `continuity.gate_hold(db, mssql=self.mssql)` before `continuity.active(...)` so `detail`, `review`, and `export` fail closed on gate-version mismatch for gate-aware images. | Discovered during `P03` verification that `export` and `_view` read `meta('continuity')` directly rather than calling `self.suspended()`; local judgment preserving `FR-4` / `PC-004` intent (no user decision needed). | Recorded in `.copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-changes.md` (`## Implementation-Time Plan and Detail Updates`). | Not needed (preserves `PC-004` fail-closed intent; no repeat critique). | Reconciled for gate-aware images; needs complementary SQL trigger on `assistant_tasks` (`RV-003`) for genuine pre-gate images. |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001` (NULL-safe `NOT EXISTS` predicates, set-based T-SQL triggers, `Latin1_General_100_BIN2` collations), `PC-002` (portable `WHERE NOT EXISTS` seeding passing `SharedSqlIsPortableTests`, MSSQL teardown table registration), and `PC-007` (strict `mypy` with `: Any` boundary aliases and zero `pyproject.toml` edits) were fully applied and verified. `PC-003` (workspace-local `.venv-122-local` instead of `/tmp`, subprocess timeouts) was applied except `test_restart_gate_sql_fences.py` omitted explicit `PYTHONPATH` in one subprocess call (`RV-005`). `PC-004`, `PC-005`, and `PC-006` were only partially realized in code/tests (`RV-001`, `RV-004`, `RV-005`).
* Material revisions: None required new user direction or architectural reconsideration; Architecture Option B remains sound.
* Dependent-work pause assessment: No improper early resumption occurred; all critique findings were `planner-direct`.
* Justification assessment: The five gaps identified below (`RV-001` through `RV-005`) are implementation defects against the accepted plan rather than justified divergences, so they are routed to a follow-up `rpi-implement` cycle.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Owner-witnessed continuity/restart drill and `OQ-017` / `OD-35` / `RULE-020` human restart authority appointment | Requires live Zava North Homes governance delegation and human witness participation outside software code (`actual_hold=True` preserved). | Owner: Programme Sponsor / Building Safety | Open distinct follow-up (`Refs #122`); properly excluded from active `Pxx` claims. |
| Immutable external Azure ledger-head storage and owned Azure SQL continuity/restart drill | Requires live Azure resource provisioning, custody approvals, and hosted `ZF_TEST_MSSQL=1` / Azure SQL environment execution. | Owner: Platform / Data Governance | Open distinct follow-up (`Refs #122`); properly excluded from active `Pxx` claims. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: `_check_claim_replay` allows replaying rejected, open, or consumed `test_id` values when `corrective_evidence` text or `candidate` changes

* Related scope: `P01-T02`
* Evidence: src/core/src/zava_forward/core/continuity.py (`_check_claim_replay` and `restart_propose` / `validate_sql`); .copilot-tracking/plans/2026-11-15/issue-122-restart-gate-0228-plan.md (`FR-1`, `AC-1`); .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md (`P01-T02`); .copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-plan-critique.md (`PC-005`)
* Impact: A proposer can reuse a normalized `test_id` already rejected by `"Keep suspended"`, concurrently proposed on another open suspension, or already consumed by a committed `"Restart"` simply by changing one word in `corrective_evidence` (or after a candidate change), contradicting `FR-1`, `P01-T02`, and `PC-005`.
* Destination: `rpi-implement`
* Smallest useful next action: Update `_check_claim_replay` in `src/core/src/zava_forward/core/continuity.py` to reject casefolded `test_id.strip().casefold()` independently across prior `"Keep suspended"` decisions on the suspension, active `proposal` records on other open `"Suspended"` incidents, and committed `"Restarted"` incidents (checking both in `restart_propose` and against `"Restarted"` incidents in `restart_decide("Restart")`), and add explicit tweaked-evidence `test_id` replay assertions in `src/core/tests/test_restart_gate_sql_fences.py` and `src/api/tests/test_continuity_restart_gate.py`.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: `assistant_attempts` hold-update SQL triggers check `NEW.outcome <> OLD.outcome`, permitting in-place updates to already-`sending` or `reserved` rows during an open hold

* Related scope: `P02-T02`
* Evidence: src/core/src/zava_forward/core/assistants.py (`SQLITE_ATTEMPT_TRIGGERS` `assistant_attempts_hold_update` and `MSSQL_ATTEMPT_TRIGGERS` `assistant_attempts_gate_update`)
* Impact: While a continuity hold is active in `continuity_open_holds`, an update to an existing `assistant_attempts` row whose `outcome` remains `'sending'` or `'reserved'` (for example refreshing `active_until` or `send_gate_version`) bypasses the hold-update trigger because `NEW.outcome <> OLD.outcome` is false, whereas settling/withdrawing an attempt transitions `outcome` out of `('reserved', 'sending')`.
* Destination: `rpi-implement`
* Smallest useful next action: Remove the `NEW.outcome <> OLD.outcome` / `i.outcome <> d.outcome` guard (or trigger whenever `NEW.outcome IN ('reserved', 'sending')` and `(NEW.active_until > 0 OR NEW.outcome <> OLD.outcome OR NEW.send_gate_version <> OLD.send_gate_version)`) in both SQLite and T-SQL `assistant_attempts` update triggers so any active reservation/sending mutation during an open hold aborts while terminal settlement (`outcome` changing to `'withdrawn'`, `'quarantined'`, `'failed'`, `'succeeded'`, `'expired'`, etc.) remains permitted, and add a unit test updating an existing `'sending'` attempt under hold.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Ready-proposal acceptance is not SQL-fenced against genuine pre-gate images that omit Python `gate_hold` checks

* Related scope: `P02-T02`, `P03-T02`
* Evidence: src/core/src/zava_forward/core/assistants.py (`SQLITE_DDL`, `MSSQL_DDL`, `review`); src/api/tests/test_continuity_restart_gate.py (`test_subprocess_old_image_worker_exclusion_across_queued_leased_and_ready`)
* Impact: `test_continuity_restart_gate.py` simulates an old image on `ready` proposals by importing the current codebase with a mutated `GATE_VERSION`, exercising the new Python `gate_hold` branch. A genuine pre-gate image (`HEAD` prior to `continuity-gate-v1`) lacks `gate_hold` in Python and updates `assistant_tasks` (`SET body=?, state='accepted'`) without writing `assistant_attempts`, so SQL does not block a genuine pre-gate API/worker process from accepting a `ready` proposal unless `assistant_tasks` also carries a SQL gate/open-hold trigger on `state = 'accepted'`.
* Destination: `rpi-implement`
* Smallest useful next action: Add `gate_version` (`DEFAULT ''` / `VARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL DEFAULT ''`) to `assistant_tasks` in `assistants.py` (`SQLITE_DDL`, `MSSQL_DDL`, `_upgrade`), stamp `gate_version = continuity.GATE_VERSION` when `review()` transitions/writes `state = 'accepted'` (leaving non-`accepted` test-corruption `UPDATE assistant_tasks SET body=...` untouched), enforce SQLite and T-SQL triggers on `assistant_tasks` rejecting `state = 'accepted'` when `gate_version` does not match `continuity_gate_state` or when `continuity_open_holds` covers `'all'` or `capability`, and test genuine pre-gate SQL/worker behavior in subprocess tests.

<!-- rpi:review id=RV-004 -->
### RV-004 [High]: `SqlStore._proc_sync` uses raw `json.loads` on `meta('continuity')` at startup and `continuity.load("")` treats an empty persisted string as valid blank history

* Related scope: `P02-T01`
* Evidence: src/core/src/zava_forward/core/sqlstore.py (`_proc_sync`, `_reload`); src/core/src/zava_forward/core/continuity.py (`load`); .copilot-tracking/reviews/plans/2026-11-15/issue-122-restart-gate-0228-plan-critique.md (`PC-004`)
* Impact: If `meta WHERE key='continuity'` contains malformed JSON or `""` and `SqlStore` is reopened or reloaded, `_proc_sync` raises `json.JSONDecodeError` during initialization (blocking manual case work, accessible challenges, and statutory hazard operations on reopen), and `continuity.load("")` returns `blank()` (`epoch=0`, valid) instead of an invalid document (`epoch=-1`) that fails closed for AI work while keeping manual routes live.
* Destination: `rpi-implement`
* Smallest useful next action: In `continuity.load(raw)`, return `blank()` only when `raw is None` and return `dict(epoch=-1, suspensions=[], changes=[])` on empty/malformed/non-dict persisted values; in `SqlStore._proc_sync` and `_reload`, load `key == "continuity"` via `continuity.load(...)` so reopening a store with corrupt `meta('continuity')` succeeds for manual/challenge/hazard routes while holding all AI scopes closed; and add a reopen-after-corruption test.

<!-- rpi:review id=RV-005 -->
### RV-005 [Medium]: `P03-T02` and `P03-T01` omit several planned HTTP, audit, subprocess `PYTHONPATH`, and mid-flight race assertions

* Related scope: `P03-T01`, `P03-T02`
* Evidence: src/api/tests/test_continuity_restart_gate.py; src/core/tests/test_restart_gate_sql_fences.py; .copilot-tracking/details/2026-11-15/issue-122-restart-gate-0228-phase-details.md (`P03-T02`); .copilot-tracking/changes/2026-11-15/issue-122-restart-gate-0228-changes.md
* Impact: `test_continuity_restart_gate.py` does not yet exercise `PasswordProvider` `POST /api/continuity/restart-decide` (`403` + `ai_restart_decide_denied`), store `ai_restart_propose_denied` / `ai_restart_decide_denied` audit rows on HTTP negative subtests, HTTP `challenge_update` and `challenge_escalate` during `all` suspension, racing `verify` directly against `suspend`, and racing mid-flight `_fence_in` (`sending`) / `complete` on an already-`leased` task directly against `suspend`; additionally, `test_restart_gate_sql_fences.py` spawns a child Python process without explicit worktree `PYTHONPATH` (`PC-003`).
* Destination: `rpi-implement`
* Smallest useful next action: Expand the existing test methods (staying within the `<= 25` combined test-method budget) in `src/api/tests/test_continuity_restart_gate.py` and `src/core/tests/test_restart_gate_sql_fences.py` to cover `PasswordProvider` `restart-decide` denial + audit assertions, HTTP `challenge_update` + `challenge_escalate`, barrier races for `verify`/`accept` and `leased` `_fence_in`/`complete` vs `suspend`, and explicit worktree `PYTHONPATH` on all `subprocess.run` calls.

## Defects

* `RV-001` [High] -> `rpi-implement`: Reject normalized `test_id` replay independently across Keep-suspended, concurrently open, and Restart-consumed suspensions.
* `RV-002` [High] -> `rpi-implement`: Fence in-place updates to active `reserved`/`sending` rows in `assistant_attempts` SQLite and T-SQL hold-update triggers.
* `RV-003` [High] -> `rpi-implement`: Enforce SQL `continuity_gate_state` / `continuity_open_holds` triggers on `assistant_tasks` `state = 'accepted'` transitions and verify genuine pre-gate worker exclusion.
* `RV-004` [High] -> `rpi-implement`: Use `continuity.load` on `SqlStore` `_proc_sync`/`_reload` and fail closed on `raw == ""` so corrupt `meta('continuity')` preserves manual recovery across store reopen.
* `RV-005` [Medium] -> `rpi-implement`: Complete planned `PasswordProvider` `restart-decide`, HTTP denial-audit, HTTP `challenge_update`/`challenge_escalate`, barrier `verify`/`_fence_in` race, and subprocess `PYTHONPATH` assertions within the `<= 25` test budget.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Child task / follow-up `rpi-implement` cycle on `continuity.py` + tests | Implementation defect within accepted `FR-1` / `PC-005` design |
| `RV-002` | `rpi-implement` | Child task / follow-up `rpi-implement` cycle on `assistants.py` + tests | Implementation defect in SQLite/T-SQL trigger predicate (`FR-4`) |
| `RV-003` | `rpi-implement` | Child task / follow-up `rpi-implement` cycle on `assistants.py` + subprocess test | Implementation defect in database-enforced old-image exclusion for `ready` proposals (`FR-4`, `AC-3`) |
| `RV-004` | `rpi-implement` | Child task / follow-up `rpi-implement` cycle on `continuity.py` + `sqlstore.py` + tests | Implementation defect against `AC-2` / `PC-004` corrupt-store manual recovery |
| `RV-005` | `rpi-implement` | Child task / follow-up `rpi-implement` cycle on `test_continuity_restart_gate.py` + `test_restart_gate_sql_fences.py` | Test-coverage gap against planned `P03-T02` / `PC-003` / `PC-006` checks |

Later implementation of a routed finding does not require another Review of this completed parent task; in automatic RPI Agent mode, selecting the routed child item runs its own bounded RPI cycle.

## Residual Work

* Owner-witnessed continuity/restart drill and `OQ-017` / `OD-35` / `RULE-020` human restart authority appointment (Owner: Programme Sponsor / Building Safety; outside local code scope under `Refs #122`).
* Immutable external Azure ledger-head storage and owned Azure SQL continuity/restart drill (Owner: Platform / Data Governance; outside local code scope under `Refs #122`).

## Blockers and Remaining Work

* Blockers: none
* Remaining active work: none in parent task `issue-122-restart-gate-0228` (`P01` through `P04` executed; defects `RV-001` through `RV-005` routed to follow-up child task).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python -m unittest discover -s tests -p 'test_restart_gate_sql_fences.py'` | `src/core` (`P03-T01`) | Passed | 8/8 tests passed |
| `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p 'test_continuity_restart_gate.py'` | `src/api` (`P03-T02`) | Passed | 9/9 tests passed |
| Focused `src/api` continuity/SQL/assistant/restart/seed suites (12 modules) | `src/api` | Passed | 612 tests passed (`605` + `7`), 0 failures |
| `python -m unittest discover -s tests -q` | `src/core` | Passed (optional SDK extra skipped/absent) | 3,437 tests passed; only `test_device_registry_azure` lacked optional `azure-iot-hub` extra in isolated local venv |
| `python3 tools/rename-zava-tests.py` | Repository migration guard | Passed | 25/25 tests passed |
| `ruff check` and `ruff format --check` | `src/core` & `src/api` | Passed | 0 issues; ADR 0006 format-exclude lists respected |
| `mypy` (strict) | `src/core` (335 files) & `src/api` (281 files) | Passed | 0 issues across 616 checked files |
| Live `ZF_TEST_MSSQL=1` SQL Server container execution | Disposable SQL Server (`src/api`) | Unavailable | No live SQL Server instance configured in local worktree; offline T-SQL DDL, collation, and `SharedSqlIsPortableTests` passed |

## Outcome

* Outcome: Defects found
* Outcome rationale: Planned phases `P01` through `P04` executed completely and pass `ruff`, strict `mypy`, and 629 targeted/regression unit tests, establishing the core SQL gate architecture and HTTP/manual/hazard continuity baselines. However, five substantive implementation and test-completeness defects (`RV-001` through `RV-004` High, `RV-005` Medium) leave gaps in normalized `test_id` anti-replay, same-outcome `sending` hold triggers, genuine pre-gate SQL exclusion on `ready` proposal acceptance, corrupt-`meta('continuity')` startup recovery, and planned `P03-T02` test scenarios. Per RPI Stop rules, a conformant verdict cannot be reported while material findings remain open.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` | Execute child follow-up cycle resolving `RV-001`, `RV-002`, `RV-003`, `RV-004`, and `RV-005` across `continuity.py`, `sqlstore.py`, `mssqlstore.py`, `assistants.py`, and the two new test modules |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | Distinct external follow-up items (`Refs #122`) | Programme Sponsor / Building Safety (`OD-35`/`OQ-017` witnessed drill) and Platform / Data Governance (immutable Azure ledger-head custody and live Azure SQL drill) |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: `src/core` and `src/api` unit/regression suites, `tools/rename-zava-tests.py`, `ruff check`, `ruff format --check`, and strict `mypy` passed; live `ZF_TEST_MSSQL=1` unavailable locally
* Blockers: none

