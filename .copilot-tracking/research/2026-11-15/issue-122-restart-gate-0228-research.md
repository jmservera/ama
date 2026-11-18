<!-- markdownlint-disable-file -->

# Task Research: issue-122-restart-gate-0228

| Field              | Value                                                                       |
|--------------------|-----------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                  |
| Researcher / agent | rpi-research (RPI Agent automatic mode)                                     |
| Status             | Complete                                                                    |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-122-restart-gate-0228-research.md |

## Research Brief

* What to research: Current implementation and gaps across `src/core` and `src/api` for Issue #122's three remaining local RAI Incident and Restart acceptance criteria:
  1. Corrective evidence and distinct authorized human approval gate restart; replayed, stale, self-approved, or unauthorized restart fails.
  2. Manual case work, accessible challenge, and independent hazard response remain available during suspension.
  3. Independent SQL connection, concurrent suspend/review, race, and restart tests cover queued, leased, and ready proposals and old-image restart.
* Why it matters: Delivers enforceable runtime invariants and test coverage in `src/core` and `src/api` without fabricating live operational approvals (OD-35 / OQ-017) or witnessed live drills, so local software enforcement of Issue #122 RAI Incident and Restart criteria is complete and verified.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` in this automatic RPI session, plus PR reviewers targeting `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`).
* Scope: `src/core/src/zava_forward/core/`, `src/core/tests/`, `src/api/src/zava_forward/api/`, `src/api/tests/`, `src/core/README.md`, `src/api/README.md`, PRD v0.16.0+ RAI contract in `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, and prior `#122` / `#221` / `#146` / `#220` artifacts.
* Non-goals: Do not add a separate governance microservice; do not transfer human authority to AI; do not fabricate real human authorization (OD-35/OQ-017) or witnessed operational drills; do not push to remote; do not close `#122` (`Refs #122` required because witnessed live operational drill and human appointment remain outside code).
* Criteria: Every codebase claim cites `path:line` with `C#` IDs; covers exact failure modes for replayed, stale, self-approved, unauthorized, and missing-corrective-evidence restart; covers suspension independence of manual case work, accessible challenge, and hazard response; covers independent SQL connection / dialect / old-image version fence / concurrent suspend-review race across `queued`, `leased`, and `ready` proposals.
* Requested outputs: Convergence recommendation for `src/core` and `src/api` runtime changes and deterministic unit/concurrency/SQL tests.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                                              |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | Q1-Q5 covering restart gate invariants, old-image restart fencing, manual/challenge/hazard availability during suspension, SQL/store persistence, and concurrency tests |
| Codebase scope                   | `src/core/**`, `src/api/**`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/brds/agentic-retrofit-programme-brd.md`, `.copilot-tracking/**`    |
| External scope                   | none (bounded internal repository contract and runtime verification)                                                                                               |
| Initial internal candidate areas | `src/core/src/zava_forward/core/continuity.py`, `restart_authority.py`, `rai_release.py`, `assistant_release.py`, `assistants.py`, `governance.py`, `sqlstore.py`, `mssqlstore.py`, `challenges.py`, `hazard.py`, `home_case.py`, `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_continuity*.py`, `test_rai_restart_sql_reconstruction.py`, `test_operator_suspension.py` |
| Initial external candidate areas | none                                                                                                                                                               |
| Research posture                 | balanced                                                                                                                                                           |
| Posture provenance               | default (bounded internal task with named `src/core` and `src/api` targets plus adjacent persistence/HTTP/concurrency interactions)                                |
| Explicit limits / deadline       | Local `src/core` and `src/api` scope only; no `git push`; clean frozen worktree after commit with `Refs #122`                                                      |
| Posture-specific completion basis | balanced scope coverage and adequate evidence across all three target criteria and adjacent store/HTTP surfaces                                                    |
| Edits allowed during research?   | no, research-only                                                                                                                                                  |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                                               |
| Known constraints / excluded sources | Constructed fixtures permit offline testing only, never live operational authorization; preserve existing API/SQL state and bounded assistant runtime               |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                                            | Scoped authority or output contract                                              | Selected / skipped reason                                                                                   |
|---------------------|---------------------------------------|-----------------------------------------------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`     | `applyTo: "**"` repository custom instruction                   | Branch/commit rules, validation tiers, RAI/regulatory governance, Markdown style | Selected: governs local validation, `Refs #122`, privacy-safe commit author, and non-fabrication boundaries |
| Skill               | `rpi-research`                        | Explicit RPI loop Phase 1 skill                                 | Read-only three-wave research artifact and Planning Readiness                    | Selected: active phase skill                                                                                |
| Skill               | `rai-standards` / `python-foundational` | Domain skills available in host catalog                       | General RAI / Python guidance                                                    | Skipped: repository PRD/BRD and existing `continuity.py` / `restart_authority.py` contracts are more specific |
| Research specialist | `hve-core-all:rpi-researcher`         | Registered host subagent for independent delegated lanes        | Writes lane evidence under `.copilot-tracking/research/subagents/`               | Skipped (inline preferred): `continuity.py`, `assistants.py`, `sqlstore.py`, and `server.py` are tightly coupled |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                     | Answers / unanswered | Resulting decision or selected further research                                                       |
|------------------|---------------------------------------------------------------------------------------------------------------------------|----------------------|-------------------------------------------------------------------------------------------------------|
| Intake           | Non-interactive session with explicit caller scope, branch, target PR (`#1641`), and three target acceptance criteria.    | n/a (autonomous)     | Proceed in `balanced` posture with `convergence` output mode across `src/core` and `src/api`.         |
| Direction change | None at intake.                                                                                                           | n/a                  | Retain initial brief.                                                                                 |
| Convergence      | Cycle 1 answered Q1-Q5 with direct codebase evidence (`C1`-`C18`); no ambiguity requiring interactive user input. | n/a (autonomous)     | Converged on single SQL-fenced continuity gate + restart validation + comprehensive SQL/HTTP/multiprocess test design (`Planning Readiness: Ready`). |

## Scope and Success Criteria

* Scope: `src/core` and `src/api` runtime modules, SQLite/MSSQL store adapters, HTTP endpoints, and unit/concurrency tests addressing the three target RAI Incident and Restart criteria of Issue #122.
* Assumptions:
  * Recent commits (`9a0dd54fa` for `#221`, plus `#146` and `#220` work) already introduced parts of `restart_authority.py`, `continuity.py`, `challenges.py`, and `test_rai_restart_sql_reconstruction.py`, which must be inspected and extended cleanly rather than duplicated.
  * Local environment may or may not have a live SQL Server daemon; we must inspect how `sqlstore.py` / `mssqlstore.py` and independent SQL connection tests are structured in `src/core/tests` and `src/api/tests`.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and one recommendation is selected in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  1. Corrective evidence and distinct authorized human approval gate restart; replayed, stale, self-approved, or unauthorized restart fails.
  2. Manual case work, accessible challenge, and independent hazard response remain available during suspension.
  3. Independent SQL connection, concurrent suspend/review, race, and restart tests cover queued, leased, and ready proposals and old-image restart.
* Inferred research questions:
  * How are suspension epochs, incidents, corrective evidence, restart approvals, replay tokens/nonces or decision IDs, and release/image versions currently persisted and checked across JSON, SQLite (`sqlstore.py`), and SQL Server (`mssqlstore.py`)?
  * How do `queued`, `leased`, and `ready` assistant proposals behave during concurrent suspend/claim/complete/review/restart across independent SQL connections, and what stops an old container/process image from restarting or dispatching after a release/version suspension?
  * Which HTTP routes and core workflows implement manual case work, accessible challenge (`#220`), and independent hazard response, and could any global or route-level suspension check inadvertently block them?
* Caller constraints and non-goals: Research-only during Phase 1; do not add a separate governance service; commit at end of Implement/Review with `Refs #122` and no push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Deliver local `src/core` and `src/api` engineering criteria 1-3 for Issue #122; do not push to remote. | Caller intake       | Scopes research and convergence to `src/core` and `src/api` plus tracking records. |
| exclude                                                  | Do not add a separate governance service or fabricate live human approvals / witnessed drills.         | Issue #122 & caller | Preserves `Refs #122` and keeps live operational drill / OD-35 appointment honest. |

## Research Questions

|  # | Sub-question                                                                                                                                         | Type            | Priority | Status   |
|---:|------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | How does `continuity.py` / `restart_authority.py` / `server.py` currently gate restart, and which of corrective evidence, distinct human approval, replay, staleness, self-approval, or unauthorized actor checks are missing or incomplete? | depth           | H        | answered |
| Q2 | How are assistant proposal states (`queued`, `leased`, `ready`) and old-image / release versions fenced across `assistants.py`, `assistant_release.py`, `rai_release.py`, and `continuity.py` on restart and worker execution? | depth           | H        | answered |
| Q3 | How do `sqlstore.py` and `mssqlstore.py` persist continuity/assistant/governance state across independent SQL connections and concurrent suspend/review/restart operations? | depth           | H        | answered |
| Q4 | Are manual case work, accessible challenge, and independent hazard response completely available (and verified by tests) while tasks/releases or global AI continuity are suspended? | breadth         | H        | answered |
| Q5 | What SQL drivers/servers and test harnesses are available locally in this worktree environment for `src/core` and `src/api` tests, `ruff`, and `mypy`? | straightforward | M        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/reviews/2026-11-04-issue-122-r2-review.md`, `.copilot-tracking/reviews/logs/2026-10-21/continuity-custody-preparation-122-recovery-review.md`, `.copilot-tracking/rpi-sessions/2026-11-14/issue-221-operator-suspension-2235-state.json`
* Reused (verified) findings: Issue #122 keeps `Refs #122` because witnessed operational drills and live OD-35 human appointment cannot be fabricated by code; commit `9a0dd54fa` recently added `zava_forward.core.restart_authority`.
* Superseded / stale: `2026-11-04-issue-122-r2-review.md` predates `9a0dd54fa` (`#1752`) and mid-November `#146`/`#220`/`#221` merges, so all `continuity.py`, `assistants.py`, `sqlstore.py`, and `server.py` code paths were freshly verified at HEAD `02ab20cac`.

## Cycle 1 Execution

### Wave 1: Wider

* Investigated inline across Issue #122 closure-audit notes (`2026-10-31` and `2026-11-05`), `src/core/README.md`, `src/api/README.md`, `continuity.py`, `restart_authority.py`, `assistants.py`, `sqlstore.py`, `mssqlstore.py`, `resident_decisions.py`, `challenges.py`, `auth.py`, `server.py`, and existing continuity/suspension test suites (`test_continuity.py`, `test_continuity_epoch_export.py`, `test_operator_suspension.py`, `test_assistant_restart_non_replenishment.py`, `test_operator_suspension_drill.py`).
* Breadth findings:
  * Issue #122's `2026-11-05` closure audit and `src/core/README.md:4580` (`C16`) explicitly identify that pre-gate (legacy / old) image exclusion is not enforced or evidenced in SQL, whereas human OD-35/OQ-017 delegation, witnessed drills, accessibility sign-off, and external immutable Azure head custody remain non-code owner activities requiring `Refs #122`.
  * `continuity.py` + `restart_authority.py` (`C1`, `C2`, `C3`, `C4`) enforce RULE-024 human restart authority naming, `constructed-fixture` / `Pass` gating, trusted-proxy OID + `ai_restart` capability checks, and distinct-actor separation at `restart_decide`.
  * `resident_decisions.py` + `challenges.py` (`C11`, `C12`) implement the full affected-person accessible challenge lifecycle (`Digital`, `Phone`, `Letter`, `In person` plus `ChallengeRegister` `digital` and `staff_recorded` `phone`, `in_person`, `paper`, `assisted_visit`) with anti-retaliation, no-inferred-refusal, and non-interference with statutory hazard clocks, completely outside AI continuity gates.

### Wave 2: Deeper

* Deepened inspection of exact validation, transaction, HTTP routing, and SQL schema boundaries:
  * **Restart gate (`Q1`)**:
    * `restart_propose` (`src/core/src/zava_forward/core/continuity.py:514-518`, `C2`) validates `corrective_evidence` and `test_id` only through `controls.evidence_text`, which permits placeholder/non-evidence strings (`"Unavailable"`, `"TBD"`, `"TODO"`, `"none"`, `"n/a"`, `"pending"`, `"unknown"`, `"-"`, `"?"`).
    * After `"Keep suspended"` clears `s["proposal"]` (`continuity.py:605-607`, `C3`), `restart_propose` does not prevent replaying the exact rejected `(test_id, corrective_evidence)` claim on the same suspension, nor does it prevent replaying a `test_id` already consumed by an earlier `"Restart"` decision across `doc["suspensions"]`.
    * `restart_decide` (`continuity.py:524-615`, `C3`) records `by=user["email"]` on `rec` without an immutable `actor` identity snapshot (`email`, `name`, `code`, `oid`), does not explicitly refuse `view_only=True` principals if combined with a manager role, and lacks HTTP integration tests through `TrustedProxyProvider` (`src/api/src/zava_forward/api/server.py:1492-1499`, `src/api/src/zava_forward/api/auth.py:139-158`, `C14`, `C15`) covering `ZavaForward.AIRestart`, `ZavaForward.ApplicationAdmin` view-only isolation, password-provider denial, self-approval across email/code/OID aliases, stale epoch, superseded/rejected proposal digest, and replayed POSTs.
  * **Manual, accessible challenge, and hazard independence during suspension (`Q4`)**:
    * `Store.resolve_priority` (`src/core/src/zava_forward/core/store.py:1079-1133`, `C13`) blocks `accept`/`edit` of AI priority suggestions when suspended, while explicitly allowing `reject` and leaving `resident_action` (`challenge_open`, `challenge_update`, `challenge_escalate`, `challenge_resolve` in `resident_decisions.py:1506-1617`, `C11`) and statutory hazard transitions (`server.py:1595-1610`, `C14`) unblocked.
    * Existing continuity suspension tests (`test_continuity_epoch_export.py:1265`, `test_continuity.py:150`) exercise `service_open(route="Complaint")` and basic hazard steps, but do NOT exercise accessible `challenge_open` (both `Digital` and non-digital `Phone`/`Letter`/`In person` with `non_digital_route`), `challenge_update`, `challenge_escalate` to a distinct named human owner, and `challenge_resolve("Correction recorded")` invalidating dependent AI suggestions while AI is actively suspended (`all` and task scope) across independent SQL connections and HTTP routes.
  * **Old-image exclusion and independent SQL race semantics (`Q2`, `Q3`)**:
    * `Assistants` (`src/core/src/zava_forward/core/assistants.py:1555-1665`, `C5`, `C6`, `C7`) reserves capacity via `INSERT INTO assistant_attempts` (`_reserve`) and transitions to `'sending'` in `_fence_in` (`fence_send` / `issue_permit`) on independent `store.assistant_connection()` SQL connections (`src/core/src/zava_forward/core/sqlstore.py:254-258`, `C8`).
    * Neither `sqlstore.py` (`C8`, `C9`) nor `mssqlstore.py` (`C10`) nor `assistants.py` (`C5`, `C6`) persists a SQL-enforced continuity gate protocol table or database triggers on `assistant_attempts` / `continuity_gate_state`. Consequently, a pre-gate / legacy worker or rolled-back image connecting to the shared SQL database is not excluded by the SQL engine (`C16`).

### Wave 3: Contrarian

* Tested candidate designs against existing failure/corruption tests and dialect constraints:
  * **Contrarian check 1 (raw `meta` / `assistant_tasks` corruption fixtures)**:
    * Grepping `meta.*continuity` and `UPDATE assistant_tasks` revealed `src/api/tests/test_operator_suspension.py:426` (`C17`) and `src/core/tests/test_seed_merge.py:147` (`C18`), which intentionally write malformed JSON to `meta WHERE key='continuity'`, plus raw `UPDATE assistant_tasks SET body=...` tests in `test_continuity_epoch_export.py` and `test_operator_suspension.py` that test reader fail-closed handling.
    * **Result**: Putting raw JSON-parsing triggers on `meta` or `assistant_tasks.body` would break legitimate corruption unit tests! By contrast, grepping `INSERT INTO assistant_attempts` and `UPDATE assistant_attempts` across all of `src/` proved that ONLY `assistants.py` writes `outcome='reserved'` or `outcome='sending'` on `assistant_attempts` (`C6`, `C7`). Placing `capability`, `gate_version`, and `send_gate_version` columns + SQL triggers on `assistant_attempts` alongside normalized `continuity_gate_state` and `continuity_open_holds` tables enforces old-image exclusion and open-suspension dispatch blocking in BOTH SQLite and T-SQL without breaking any existing corruption fixture!
  * **Contrarian check 2 (`actual_hold=True` after constructed `"Restart"`)**:
    * After a constructed `"Restart"`, `s["status"] == "Restarted"` while `s["actual_hold"]` remains `True` (`continuity.py:465, 608-612`, `C2`, `C3`); `assistants.py:841, 905, 1109` (`C5`) passes `constructed=not isinstance(self.store.ai, Ai)` so constructed drill tests can resume synthetic assistant execution after `"Restart"`, while live `Ai` remains held until actual OD-35 authority exists.
    * **Result**: `continuity_open_holds` must track `status == "Suspended"` incidents (active open suspensions that block ALL images, constructed and live alike) and clear a row when its incident transitions to `"Restarted"`, while `s["actual_hold"] = True` continues to hold live `Ai` at the application gate.
  * **Contrarian check 3 (suspender vs proposer separation)**:
    * Existing tests (`test_operator_suspension.py:60-85`, `test_continuity.py:132-145`) intentionally have `self.pm` record `suspend` and `restart_propose` while a distinct provisioned manager (`actor`) executes `restart_decide`, which checks `ensure_distinct_restart_actor` against BOTH `s["actor"]` and `p["actor"]`.
    * **Result**: Keep proposer allowed to match suspender, while keeping `restart_decide` strictly distinct from BOTH suspender and proposer (across email, `display_email`, `code`, `name`, `oid`, and `actors_for_store` OID-linked roster entries).
  * **Contrarian check 4 (local Python/test environment, `Q5`)**:
    * Dependencies (`aiohttp`, `azure-identity`, `mssql-python`, `mypy` 2.4.1, `ruff`) are pre-installed in `--user` site-packages; creating a disposable `--system-site-packages` venv in `/tmp/zf-122-0228-venv` with editable `--no-deps` installs of `src/core`, `src/agents`, and `src/api` enables clean isolated execution and trivial cleanup before commit.

## Evidence Log

| ID  | Kind | Location                                                              | Summary                                                                                                                                         |
|-----|------|-----------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| C1  | code | `src/core/src/zava_forward/core/continuity.py:78-175`                 | `active`, `record_task`, `history_valid`, and `epoch_current` fail-closed continuity history and epoch validity rules.                          |
| C2  | code | `src/core/src/zava_forward/core/continuity.py:424-522`                | `suspend` and `restart_propose` logic; `restart_propose` uses `k.evidence_text` without placeholder/replay rejection on `corrective_evidence` / `test_id`. |
| C3  | code | `src/core/src/zava_forward/core/continuity.py:524-615`                | `restart_decide` enforces `trusted_route`, `MANAGER_ROLES`, distinct actor, `trusted-proxy` + `oid` + `ai_restart`, epoch, digest, and `authority_ref`. |
| C4  | code | `src/core/src/zava_forward/core/restart_authority.py:19-289`          | RULE-024 placeholder/non-human/chat-memory rejection and `_same_actor` / `actors_for_store` multi-person separation helpers.                    |
| C5  | code | `src/core/src/zava_forward/core/assistants.py:835-925`                | `Assistants.continuity`, `suspended`, `disabled`, and `claim` re-check persisted SQL `continuity` on independent connections.                   |
| C6  | code | `src/core/src/zava_forward/core/assistants.py:1555-1615`              | `claim` stamps `claim_epoch` / `claim_binding` and `_reserve` inserts `'reserved'` rows into `assistant_attempts`.                              |
| C7  | code | `src/core/src/zava_forward/core/assistants.py:1645-1715`              | `fence_send`, `_fence_in`, and `complete_result` gate `'sending'` transitions and late-result quarantine / permitted-attempt settlement.        |
| C8  | code | `src/core/src/zava_forward/core/sqlstore.py:254-335`                  | `SqlStore.assistant_connection`, `continuity_suspension`, and `_migrate` SQLite schema and WAL connection lifecycle.                            |
| C9  | code | `src/core/src/zava_forward/core/sqlstore.py:1135-1375`                | `SqlStore.save`, `_proc_sync`, and `_proc_write` atomic SQLite transaction and optimistic conflict checks on `meta` documents (`continuity`).   |
| C10 | code | `src/core/src/zava_forward/core/mssqlstore.py:28-235`                 | `MssqlStore` T-SQL DDL, `APPEND_ONLY` trigger pattern, `sp_getapplock` writer serialization, and connection adapter.                            |
| C11 | code | `src/core/src/zava_forward/core/resident_decisions.py:1506-1617`      | `_res_challenge_open`, `_res_challenge_update`, `_res_challenge_escalate`, and `_res_challenge_resolve` accessible challenge workflow on `Store`. |
| C12 | code | `src/core/src/zava_forward/core/challenges.py:24-255`                 | `ChallengeRegister` (`digital` + `staff_recorded` `phone`/`in_person`/`paper`/`assisted_visit`), `assert_no_adverse_challenge_effects`, and `hazard_concern` referral. |
| C13 | code | `src/core/src/zava_forward/core/store.py:1079-1133`                   | `Store.resolve_priority` blocks AI `accept`/`edit` during suspension or stale epoch while keeping `reject` and manual controls available.       |
| C14 | code | `src/api/src/zava_forward/api/server.py:1485-1665`                    | HTTP handlers for `/api/continuity/*` (`trusted_route=app.provider.name == "trusted-proxy"`), `/api/cases/<id>/resident`, manual case actions, and hazard endpoints. |
| C15 | code | `src/api/src/zava_forward/api/auth.py:118-175`                        | `TrustedProxyProvider` role mapping: `ZavaForward.AIRestart` grants `rule_roles=["ai_restart"]`; `ZavaForward.ApplicationAdmin` is `view_only=True` and never grants `ai_restart`. |
| C16 | doc  | `src/core/README.md:4575-4585`                                        | Documents that pre-gate (legacy) image exclusion was previously neither enforced nor evidenced in repository sources.                            |
| C17 | test | `src/api/tests/test_operator_suspension.py:420-435`                   | Existing test mutates `meta WHERE key='continuity'` directly with malformed JSON to verify `history_valid` fail-closed behavior.                |
| C18 | test | `src/core/tests/test_seed_merge.py:145-155`                           | Existing test writes synthetic JSON directly to `meta ('continuity', ...)` to verify `merge_seed` preservation.                                 |

## Synthesis and Convergence

### Selected Recommendation (Accepted)

1. **Harden Criterion 1 (`restart_authority.py`, `continuity.py`, `server.py`)**:
   * Add `validate_corrective_evidence(value, *, label, limit)` in `restart_authority.py` (rejecting blank/oversized values, chat-memory citations, `"Unavailable..."`, and `_EXACT_PLACEHOLDERS` / `_PLACEHOLDER_PATTERNS` placeholder strings without echoing raw input, while preserving legitimate concise strings such as `"Reviewed."` and `"synthetic:corrective-tests-221"`), and enforce it in both `restart_propose` and `restart_decide` (`C2`, `C3`, `C4`).
   * Enforce anti-replay on corrective claims in `restart_propose` and `restart_decide`: reject re-proposing a `(test_id, corrective_evidence)` pair that was already rejected via `"Keep suspended"` on the same suspension, and reject reusing a `test_id` already consumed by a committed `"Restart"` decision on an earlier suspension in the continuity register (`C2`, `C3`).
   * Refuse `view_only` callers in `suspend`, `restart_propose`, and `restart_decide`; record `actor` identity snapshot (`email`, `name`, `code`, `oid`) on `restart_decide` records; and add end-to-end HTTP `TrustedProxyProvider` + `PasswordProvider` tests covering authorized two-person restart vs replayed, superseded, Keep-suspended-replayed, stale-epoch, candidate-drifted, self-approved (suspender/proposer/OID-alias), view-only `ApplicationAdmin`, unprovisioned manager, disabled/demoted roster, and password-route failures (`C3`, `C14`, `C15`).
2. **Verify and Protect Criterion 2 (`resident_decisions.py`, `challenges.py`, `hazard.py`, `server.py`)**:
   * Keep manual case progression, accessible resident challenge (`Digital`, `Phone`, `Letter`, `In person` via `/api/cases/<id>/resident` plus `ChallengeRegister` non-digital `phone`/`in_person`/`paper`/`assisted_visit` and immediate `hazard_concern` referral), and statutory hazard response (`raise_hazard` through `release_hazard`) completely decoupled from AI suspension and gate-version holds (`C11`, `C12`, `C13`, `C14`).
   * Add dedicated SQL + HTTP suspension-availability tests proving that during active task-scope and `all`-scope suspension (and during continuity gate mismatch), staff can execute manual case updates/advances, open/update/escalate/resolve accessible challenges (including `"Correction recorded"` marking dependent AI priority proposals `stale=True` and `priority_correction=1` without altering consent, priority, or hazard clocks), reject suspended AI suggestions/proposals, and complete full statutory hazard lifecycles across independent SQL connections.
3. **Enforce Old-Image Exclusion and Multi-Connection/Multi-Process Races for Criterion 3 (`continuity.py`, `sqlstore.py`, `mssqlstore.py`, `assistants.py`)**:
   * Introduce `continuity.GATE_VERSION = "continuity-gate-v1"` and SQL-backed tables `continuity_gate_state (id=1, gate_version, epoch)` + `continuity_open_holds (scope, incident_id, epoch)` maintained transactionally by `SqlStore` / `MssqlStore` (`_create_schema`, `_migrate`, `_seed`, `_proc_write`) and `Assistants.migrate()` (`C6`, `C7`, `C8`, `C9`, `C10`, `C16`).
   * Add monotonic/non-delete SQL triggers on `continuity_gate_state` (`NEW.epoch < OLD.epoch` or `DELETE` aborts/throws) and gate-enforcement SQL triggers on `assistant_attempts` (`capability`, `gate_version`, `send_gate_version` columns): any `INSERT` with `outcome='reserved'` lacking matching `gate_version`, any `UPDATE` to `outcome='sending'` lacking matching `send_gate_version`, or any `'reserved'`/`'sending'` write while `continuity_open_holds` covers `'all'` or `capability` is aborted directly by SQLite (`RAISE(ABORT, ...)`) and T-SQL (`THROW 50004/50005, ...`) (`C6`, `C7`, `C10`, `C17`, `C18`).
   * Make `SqlStore.continuity_suspension` and `Assistants.disabled` also fail closed when `continuity_gate_state.gate_version` in SQL differs from `continuity.GATE_VERSION` (protecting against rollback from a newer future schema to an older image while preserving manual/challenge/hazard routes).
   * Add independent SQL connection, threaded barrier race, and real multi-process (`subprocess`) worker restart tests covering `queued` (`pending`), `leased` (in-flight completion quarantine, `issue_permit`/`fence_send` withdrawal, expired-lease reclaim after suspension/restart, and `permitted`-marker `blocked-reclaim`), `ready` (non-actionable during suspension and across epoch/release restart, `verify`/`accept`/`edit-accept` refused, `reject` allowed), and old-image restart (both pre-gate SQL write rejection by database triggers and older model/prompt/release worker restart).
   * Update `src/core/README.md` (`C16`) and `src/api/README.md` accurately to document the SQL `continuity-gate-v1` old-image exclusion control and its exact scope without overclaiming external deployment orchestration, OD-35 authority, witnessed drills, or accessibility sign-off.

### Alternatives Evaluated and Rejected

* **Alternative A (Rejected): Raw JSON triggers on `meta` (`key='continuity'`) and `assistant_tasks.body`.**
  * Rejected because `test_operator_suspension.py:426` (`C17`) and `test_seed_merge.py:147` (`C18`) intentionally write raw/malformed JSON into `meta ('continuity')` and `assistant_tasks.body` to verify reader fail-closed handling, and T-SQL/SQLite JSON path expressions differ across dialects. Normalized `continuity_gate_state` / `continuity_open_holds` + `assistant_attempts` triggers are dialect-portable and preserve all corruption fixtures.
* **Alternative B (Rejected): Application-only version check without SQL triggers.**
  * Rejected because an old pre-gate container/worker binary by definition does not run new Python checks; only a database-level schema default + trigger on `assistant_attempts` / `continuity_gate_state` physically prevents a pre-gate image from reserving or dispatching against a migrated SQL database (`C16`).
* **Alternative C (Rejected): Separate governance service for continuity/restart gating.**
  * Rejected per caller non-goals and Issue #122 architecture: shared SQL state + optimistic/transactional fences in `src/core` and `src/api` enforce the invariants with zero extra network hops or split-brain risk.

## Unresolved Decisions, Risks, and Potential Further Research

* **Open human/external blockers on Issue #122 (preserved honestly, outside local scope)**:
  * Actual human restart authority appointment (`OQ-017` / `OD-35` / `RULE-020`), witnessed operational drill, external immutable Azure head storage, owned live Azure SQL drill, and accessibility acceptance remain open owner activities (`C16`). Therefore `actual_hold=True` and `evidence_class="constructed-fixture"` remain mandatory and the commit must use `Refs #122`.
* **Local SQL Server daemon availability**:
  * No disposable SQL Server container is assumed running in the local environment (`ZF_TEST_MSSQL` opt-in skips cleanly when unset), so T-SQL DDL/trigger generation in `mssqlstore.py` and `assistants.py` will also be verified via deterministic unit assertions on generated T-SQL statements alongside live SQLite multi-connection and multi-process execution.
* **Potential further research**: None required before planning; all Q1-Q5 uncertainties are resolved with direct codebase evidence.

## Readiness and Handoff

* **Research execution status**: Completed (Cycle 1 Wider, Deeper, and Contrarian waves executed inline).
* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`
* **Self-check**:
  * All 5 research questions (`Q1`-`Q5`) answered with `C1`-`C18` `path:line` anchors: Pass.
  * Wider, Deeper, and Contrarian waves recorded in order with parent synthesis and rejected alternatives: Pass.
  * Research-only constraint honored (zero `src/` or `docs/` edits during Research): Pass.
* **Continuation**: Returning pointer-first handoff to confirmed automatic `RPI Agent` parent to transition directly to `Plan` (`rpi-plan`).

