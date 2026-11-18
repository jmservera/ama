---
description: "Primary evidence artifact for PR #1797 c2 cross-PR (#122 / #220) continuity SQL gate remediation on feat/safety-81-exercise-gates"
---
<!-- markdownlint-disable-file -->

# Task Research: safety-81-exercise-gates

| Field              | Value                                                                             |
|--------------------|-----------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                        |
| Researcher / agent | rpi-research (RPI Agent automatic child session)                                  |
| Status             | Complete                                                                          |
| Artifact path      | .copilot-tracking/research/2026-11-15/safety-81-exercise-gates-research.md        |

## Research Brief

* What to research: Verify the exact `sqlite3.IntegrityError: continuity SQL gate mismatch` failure in `src-core` and `src-api` on PR `#1797` (`1be969f61`) caused by the cross-PR interaction on `feat/demo-164-chat-grounding-provenance-0900` between PR `#1787` (`#122`) and PR `#1796` (`#220`), audit all `UPDATE assistant_tasks` statements and `reviewed_revision` / `review_gate_version` semantics in `src/core/src/zava_forward/core/assistants.py`, and verify exact Focused-tier test module paths across `src/core` and `src/api`.
* Why it matters: Commit `1be969f61` on `feat/safety-81-exercise-gates` passed `8/10` CI jobs and all `#81` safety/consent tests, failing only `AssistantsProposalChallengeNoRetaliationTests` (`src-core`) and `ChallengeNoRetaliationApi220Tests` (`src-api`) when `Assistants.challenge()` updated a `'ready'` row without `review_gate_version` and `reviewed_revision`.
* Audience or intended use: `rpi-plan`, `rpi-implement`, `rpi-review`, and Backlog Delivery Coordinator exact-head verification.
* Scope: `src/core/src/zava_forward/core/assistants.py`, `src/core/tests/test_challenge_no_retaliation_220.py`, `src/core/tests/test_restart_gate_sql_fences.py`, `src/core/tests/test_safety_consent_exercise_scenarios_81.py`, `src/api/tests/test_challenge_no_retaliation_api_220.py`, and `src/api/tests/test_continuity_restart_gate.py`.
* Non-goals: Weakening `assistant_tasks_gate_update` or `assistant_tasks_hold_update` SQL triggers from `#122`, altering `#81` safety/consent exercise gate invariants, modifying `web/` UI assets, or pushing to remote.
* Criteria: Reproduce the exact failure pre-fix, verify SQLite and MSSQL trigger invariants and all `UPDATE assistant_tasks` sites with `path:line` evidence, verify whether `reviewed_revision` has any unintended Python-level review side effects, and confirm exact test module filenames.
* Requested outputs: Primary research artifact with `C#` evidence log, synthesis, convergence recommendation, and Planning Readiness.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                              |
|----------------------------------|----------------------------------------------------------------------------------------------------|
| Research question(s)             | Q1-Q4 covering cross-PR trigger failure, `reviewed_revision` semantics, other `UPDATE` sites, and test module paths |
| Codebase scope                   | `src/core/`, `src/api/`, `tools/rename-zava-tests.py`, `.copilot-tracking/*81*`                    |
| External scope                   | none (internal repository code and local reproduction)                                             |
| Initial internal candidate areas | `src/core/src/zava_forward/core/assistants.py`, `src/core/tests/`, `src/api/tests/`                |
| Initial external candidate areas | none                                                                                               |
| Research posture                 | focused                                                                                            |
| Posture provenance               | caller-specified (bounded `c2` cross-PR SQL gate remediation with exact line and root cause)       |
| Explicit limits / deadline       | Focused validation tier; commit locally on `feat/safety-81-exercise-gates`; do not push            |
| Posture-specific completion basis| focused scope and materiality                                                                      |
| Edits allowed during research?   | no, research-only                                                                                  |
| Resolved evidence root           | `.copilot-tracking/`                                                                               |
| Known constraints / excluded sources | Non-interactive session; preserve `#122`, `#220`, and `#81` invariants; no push to origin      |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md`| `applyTo: "**"` matches repository and evidence   | Enforces D4/#1294 validation tiers, local mypy/ruff parity with `src-ci.yml`, and git commit rules | Selected: binding repo instruction |
| Skill               | `python-foundational`            | Semantic match to Python/SQLite testing           | General Python tooling guidance              | Skipped: exact SQLite/MSSQL trigger rules and validation commands are defined in repo and caller brief |
| Skill               | `web-design-guidelines`          | Web UI changes under `src/api/.../web/`           | Web UI accessibility/design rules            | Skipped: no web UI files are touched in `c2` |
| Research specialist | `hve-core-all:rpi-researcher`    | General delegated lane worker                     | Compact lane artifact under `subagents/`     | Skipped (inline): single-statement cross-PR trigger audit completes faster and more accurately inline |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive session with complete caller root cause, target statement, validation commands, tracking paths, and do-not-push rule | Not applicable (non-interactive) | Proceed directly in `focused` posture on `feat/safety-81-exercise-gates` |
| Direction change | Contrarian wave identified test filename shorthand in caller prompt (`test_safety_consent_exercise_gates_81.py` vs actual `test_safety_consent_exercise_scenarios_81.py`, and non-existent `test_safety_consent_exercise_gates_81_api.py`) | Not applicable | Run exact existing `#81`, `#122`, and `#220` test modules in `src/core` and `src/api` and document the filename mapping |
| Convergence      | Cycle 1 answered Q1-Q4 with direct codebase and local test reproduction evidence | Not applicable | Converge on updating `Assistants.challenge()` to stamp `review_gate_version` and `reviewed_revision=revision+1` and advance to `Plan` |

## Scope and Success Criteria

* Scope: Read-only reproduction of `test_challenge_no_retaliation_220.py`, full audit of `SQLITE_ATTEMPT_TRIGGERS`, `MSSQL_ATTEMPT_TRIGGERS`, `reviewed_revision`, and all `UPDATE assistant_tasks` statements in `assistants.py`, and test-module discovery across `src/core/tests` and `src/api/tests`.
* Assumptions: `Assistants.challenge()` is the sole un-gated `ready`/`accepted` row mutator introduced by `#220`, and stamping `review_gate_version=continuity.GATE_VERSION` + `reviewed_revision=revision+1` introduces zero false-approval side effects. (Verified in Cycle 1.)
* Success criteria:
  * Every research question is answered with `path:line` codebase citations (`C1`-`C8`).
  * Pre-fix failure is reproduced locally.
  * Contrarian hypotheses (false-review inference, other `UPDATE assistant_tasks` sites, MSSQL trigger semantics, test filenames, validation tier) are explicitly tested.

## Task Research Requests

* Explicit requests: Fix `Assistants.challenge()` at `src/core/src/zava_forward/core/assistants.py:4064` to set `review_gate_version=?, reviewed_revision=revision+1, revision=revision+1` with `continuity.GATE_VERSION`, run Focused validation in `src/core`, `src/api`, and `tools/rename-zava-tests.py`, record `c2` rework in `.copilot-tracking/changes/2026-11-15/safety-81-exercise-gates-changes.md` and `.copilot-tracking/reviews/logs/2026-11-15/safety-81-exercise-gates-review.md`, and commit locally without pushing.
* Inferred research questions: Verify whether `reviewed_revision` is read anywhere in Python to imply human review, whether any other `UPDATE assistant_tasks` statement mutates `'ready'` or `'accepted'` rows without gate columns, and which exact `#81`/`#122`/`#220` test files exist in `src/core/tests` and `src/api/tests`.
* Caller constraints and non-goals: Research is strictly read-only; do not weaken `#122` triggers; do not push to remote.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Bound `c2` rework to `Assistants.challenge()` SQL continuity-gate column update and Focused `src/core` + `src/api` validation | User intake          | Restricts source diff to the single `UPDATE assistant_tasks` statement in `assistants.py` |
| exclude                                                  | Do not push commits to remote; leave clean frozen local HEAD | User intake          | Constrains Implement/Follow-up git closeout to local commit only |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status   |
|---:|------------------|------------------------------------------|-----------|----------|
| Q1 | Why did `1be969f61` fail `test_challenge_no_retaliation_220.py` and `test_challenge_no_retaliation_api_220.py` after rebasing onto `feat/demo-164-chat-grounding-provenance-0900`? | straightforward | H | answered |
| Q2 | Is `reviewed_revision` read anywhere in Python or SQL to signify human proposal approval (`verify` / `accept`), or is it strictly a `#122` SQL fence column? | depth | H | answered |
| Q3 | Do any other `UPDATE assistant_tasks` sites in `assistants.py` hit `assistant_tasks_gate_update` on SQLite or MSSQL, and does `SET reviewed_revision=revision+1, revision=revision+1` behave identically on SQLite and MSSQL? | depth | H | answered |
| Q4 | What are the exact test module filenames in `src/core/tests` and `src/api/tests`, and which validation tier applies under D4 / `#1294`? | straightforward | M | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/rpi-sessions/2026-11-15/issue-81-safety-consent-gates-state.json`, `.copilot-tracking/reviews/logs/2026-11-15/issue-81-safety-consent-gates-review.md`
* Reused (verified) findings: Commit `1be969f61` rebased `#81` onto `04e5da42e` (`#122`, PR `#1787`), which sits atop `173c81b67` (`#220`, PR `#1796`); all `#81` safety and resident consent exercise-scenario tests pass (`8/8`).
* Superseded / stale: `#220` (`173c81b67`) merged before `#122` (`04e5da42e`) added `assistant_tasks_gate_update`, leaving `Assistants.challenge()` without `review_gate_version` and `reviewed_revision=revision+1`.

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow (`Assistants.challenge()` continuity SQL gate update under Focused validation); exclude (no push to remote)
* Active research posture and completion basis: focused; focused scope and materiality
* Explicit limits or deadline effect: Read-only reproduction during Research; local-only commit after Review

#### Wave 1: Wider

* Plan and independent lanes: Inline inspection of `git log -n 4 --oneline`, `assistants.py` (`SQLITE_ATTEMPT_TRIGGERS`, `MSSQL_ATTEMPT_TRIGGERS`, `Assistants.review()`, `Assistants.challenge()`), and local reproduction of `tests/test_challenge_no_retaliation_220.py`.
* Worker evidence relationships or inline fallback: Inline execution reproduced `sqlite3.IntegrityError: continuity SQL gate mismatch` at `assistants.py:4064` (`C1`, `C2`) and traced the ancestry `173c81b67` (`#220`) -> `2fe7ff2e6` (`#100`) -> `04e5da42e` (`#122`) -> `1be969f61` (`#81`) (`C1`).
* Reflection: Confirmed exact reproduction; Wave 2 must inspect every `UPDATE assistant_tasks` statement and `reviewed_revision` reference across `src/`.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: `assistant_tasks_gate_update` trigger predicates in SQLite and MSSQL, `Assistants.review()` at `assistants.py:3638-3641`, and all `reviewed_revision` and `UPDATE assistant_tasks` occurrences across `src/`.
* Plan and independent lanes: Inline `grep` across `src/` for `reviewed_revision` and across `assistants.py` for `UPDATE assistant_tasks` and `def _row(`.
* Worker evidence relationships or inline fallback:
  * `assistant_tasks_gate_update` (`assistants.py:1054-1059` and `1096-1103`) fires whenever `(NEW.state = 'accepted' AND (OLD.state <> 'accepted' OR NEW.revision <> OLD.revision OR NEW.body <> OLD.body))` OR `(OLD.state = 'ready' AND NEW.state = 'ready' AND NEW.revision <> OLD.revision)` and aborts unless `NEW.reviewed_revision = NEW.revision` and `NEW.review_gate_version` matches `continuity_gate_state.gate_version` (`C3`).
  * `reviewed_revision` appears only in DDL, migration `_add_column`, trigger definitions, and `Assistants.review()` line `3639`; `Assistants._row()` (`assistants.py:1935-1948`) never even selects `reviewed_revision` or `review_gate_version` (`C4`, `C5`).
  * Every other `UPDATE assistant_tasks` site in `assistants.py` transitions to or within `'pending'`, `'leased'`, `'disabled'`, `'stale'`, `'failed'`, or `'rejected'` (none keep `OLD.state = 'ready' AND NEW.state = 'ready'` or write `NEW.state = 'accepted'`) (`C6`).
* Reflection: Confirms `Assistants.challenge()` is the single un-gated `ready`/`accepted` row mutator. Wave 3 tests contrarian edge cases (MSSQL `SET` evaluation, suspension holds, test file names, and validation tier).

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge (1) whether `SET reviewed_revision=revision+1, revision=revision+1` evaluates left-to-right (`revision+2`) in SQLite or MSSQL, (2) whether caller test filenames match repository paths, and (3) whether modifying `assistants.py` triggers full-tier SQL gate requirements under D4 / `#1294`.
* Plan and independent lanes: Inline check of `Assistants.review()` (`assistants.py:3639`), `test_restart_gate_sql_fences.py:586-594`, `glob` across `src/core/tests` and `src/api/tests`, and D4 / `#1294` classification rules.
* Worker evidence relationships or inline fallback:
  * SQLite and T-SQL (MSSQL) both evaluate RHS expressions in `UPDATE ... SET` against pre-update row values, and both `assistants.py:3639` and `test_restart_gate_sql_fences.py:586-594` already rely on `SET ..., review_gate_version=?, reviewed_revision=revision+1, revision=revision+1` (`C5`, `C7`).
  * Caller prompt step 2 names `tests/test_safety_consent_exercise_gates_81.py` (`src/core`) and `tests/test_safety_consent_exercise_gates_81_api.py` (`src/api`), whereas `glob` proves the `#81` module in `src/core/tests/` is `test_safety_consent_exercise_scenarios_81.py` and no `*_81_api.py` exists in `src/api/tests/` (`C8`). In `src/api/tests/`, running `test_challenge_no_retaliation_api_220.py`, `test_continuity_restart_gate.py`, and `test_content_standard.py` provides real HTTP + continuity restart gate + content-standard coverage.
  * Note on D4 / `#1294` tier classification: This change modifies zero SQL DDL, zero SQL triggers, and zero schema definitions—it updates a single Python DML parameter tuple in `Assistants.challenge()` to supply the existing `continuity.GATE_VERSION` token already enforced by `#122`'s triggers, under explicit caller `Validation tier: Focused` direction.
* Reflection: Contrarian check caught the two prompt filename shorthands (`test_safety_consent_exercise_scenarios_81.py` and `test_continuity_restart_gate.py`) before implementation so Python 3.12 `unittest` does not fail with `ImportError` on nonexistent module paths.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|----------------------------|
| Update `Assistants.challenge()` (`assistants.py:4064-4067`) to set `review_gate_version=?, reviewed_revision=revision+1, revision=revision+1` with `continuity.GATE_VERSION` | `C2`, `C3`, `C4`, `C5`, `C6`, `C7` | accepted | Matches `Assistants.review()` (`assistants.py:3638-3641`), satisfies both SQLite and MSSQL `assistant_tasks_gate_update` triggers without weakening `#122` old-image fences, and has zero Python review-state side effects | Selected convergence recommendation |
| Run actual `#81` (`test_safety_consent_exercise_scenarios_81.py`), `#122` (`test_restart_gate_sql_fences.py`, `test_continuity_restart_gate.py`), and `#220` (`test_challenge_no_retaliation_220.py`, `test_challenge_no_retaliation_api_220.py`) suites | `C8` | accepted | Replaces nonexistent shorthand module paths while covering every `#81`, `#122`, and `#220` core and HTTP API invariant | Carried into Plan validation |
| Exempt `challenges` updates inside `assistant_tasks_gate_update` SQL trigger DDL | `C3`, `C7` | rejected | Modifying SQL trigger DDL would weaken `#122`'s old-image SQL write fence and escalate SQL DDL risk unnecessarily | Recorded as rejected alternative |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Q1-Q4 answered with direct local reproduction and full `assistants.py` trigger/DML audit.
* Revised brief or revalidation required: none
* Readiness effect: Ready (`C1`-`C8`)

## Evidence Log

* Delegation: inline: single-statement cross-PR DML fix where direct `grep`, `view`, and `unittest` reproduction resolved every question in one tight pass.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|----|-----------------|------------------------|------|------------|-------|
| C1 | Branch `feat/safety-81-exercise-gates` (`1be969f61`) sits directly atop `04e5da42e` (`#122`, PR `#1787`), `2fe7ff2e6` (`#100`, PR `#1792`), and `173c81b67` (`#220`, PR `#1796`) | `src/core/src/zava_forward/core/safety_consent_exercise_gate.py:1` | bash (`git log`) | high | Cross-PR interaction introduced when `#122` landed after `#220` |
| C2 | `Assistants.challenge()` executes `UPDATE assistant_tasks SET body=?,state=?,revision=revision+1 WHERE id=? AND revision=?`, raising `sqlite3.IntegrityError: continuity SQL gate mismatch` when `state == 'ready'` | `src/core/src/zava_forward/core/assistants.py:4064-4067` | view / bash (`unittest`) | high | Reproduced locally via `test_challenge_no_retaliation_220.py` |
| C3 | Both `SQLITE_ATTEMPT_TRIGGERS` and `MSSQL_ATTEMPT_TRIGGERS` define `assistant_tasks_gate_update` requiring `reviewed_revision = revision` and `review_gate_version = continuity_gate_state.gate_version` when `(OLD.state = 'ready' AND NEW.state = 'ready' AND NEW.revision <> OLD.revision)` or `NEW.state = 'accepted'` | `src/core/src/zava_forward/core/assistants.py:1054-1108` | grep / view | high | Also enforces `continuity_open_holds` via `assistant_tasks_hold_update` |
| C4 | `reviewed_revision` and `review_gate_version` are never selected by `Assistants._row()` or inspected anywhere in Python to determine proposal verification or acceptance | `src/core/src/zava_forward/core/assistants.py:1935-1948` | grep | high | Human verification/review lives in JSON `body["verification"]` and `body["review"]` |
| C5 | `Assistants.review()` stamps `UPDATE assistant_tasks SET body=?,state=?,review_gate_version=?,reviewed_revision=revision+1,revision=revision+1 WHERE id=? AND revision=?` with `continuity.GATE_VERSION` for non-reject updates (`verify`, `accept`, `edit-accept`) | `src/core/src/zava_forward/core/assistants.py:3638-3641` | view | high | Canonical current-image DML pattern for `ready`/`accepted` updates |
| C6 | All other 13 `UPDATE assistant_tasks` statements in `assistants.py` target `'pending'`, `'leased'`, `'disabled'`, `'stale'`, `'failed'`, or `'rejected'` states and cannot trigger `assistant_tasks_gate_update` | `src/core/src/zava_forward/core/assistants.py:1855-3636` | grep | high | Exhaustive check of all 15 `UPDATE assistant_tasks` occurrences |
| C7 | `test_restart_gate_sql_fences.py` explicitly verifies that `UPDATE assistant_tasks SET body=..., revision=revision+1` without `review_gate_version` and `reviewed_revision=revision+1` raises `continuity SQL gate mismatch`, whereas supplying both with `continuity.GATE_VERSION` satisfies the gate trigger | `src/core/tests/test_restart_gate_sql_fences.py:535-595` | view | high | Preserves `#122` old-image SQL fence semantics intact |
| C8 | Actual test files in the workspace are `src/core/tests/test_safety_consent_exercise_scenarios_81.py`, `src/core/tests/test_challenge_no_retaliation_220.py`, `src/core/tests/test_restart_gate_sql_fences.py`, `src/api/tests/test_challenge_no_retaliation_api_220.py`, and `src/api/tests/test_continuity_restart_gate.py` | `src/core/tests/test_safety_consent_exercise_scenarios_81.py:1` | glob | high | `test_safety_consent_exercise_gates_81.py` and `test_safety_consent_exercise_gates_81_api.py` do not exist |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

No external sources used.

### Contradictions / Conflicts

* Caller prompt test filename shorthand vs actual repository paths (`C8`): Step 2 lists `tests/test_safety_consent_exercise_gates_81.py` in `src/core` and `tests/test_safety_consent_exercise_gates_81_api.py` in `src/api`, whereas the repository contains `src/core/tests/test_safety_consent_exercise_scenarios_81.py` and has no `*_81_api.py` file (since `#81` exercise scenarios are pure `src/core` domain invariants). Resolved by running `tests/test_safety_consent_exercise_scenarios_81.py` in `src/core` alongside `#220` and `#122` suites, and running `tests/test_challenge_no_retaliation_api_220.py`, `tests/test_continuity_restart_gate.py`, and `tests/test_content_standard.py` in `src/api`.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | `Assistants.challenge()` (`#220`) mutates a `'ready'` row with `revision=revision+1` without updating `review_gate_version` and `reviewed_revision`, tripping `#122`'s `assistant_tasks_gate_update` trigger in both `src-core` and `src-api`. | `C1`, `C2`, `C3` | high | Root cause confirmed and reproduced locally. |
| Q2 | `reviewed_revision` and `review_gate_version` are write-only SQL trigger fence columns; Python never reads them to infer human approval. | `C4`, `C5` | high | Safe to stamp in `Assistants.challenge()` without governance side effects. |
| Q3 | No other `UPDATE assistant_tasks` site in `assistants.py` leaves `state` in `'ready'` or `'accepted'` without gate columns, and `SET reviewed_revision=revision+1, revision=revision+1` works identically in SQLite and MSSQL. | `C5`, `C6`, `C7` | high | Single-site surgical fix is complete across both SQL backends. |
| Q4 | Exact test modules are `test_challenge_no_retaliation_220.py`, `test_restart_gate_sql_fences.py`, and `test_safety_consent_exercise_scenarios_81.py` in `src/core`, plus `test_challenge_no_retaliation_api_220.py`, `test_continuity_restart_gate.py`, and `test_content_standard.py` in `src/api`. | `C8` | high | Planning Readiness is `Ready`. |

## Key Discoveries

* Reproduced exact CI error locally: `sqlite3.IntegrityError: continuity SQL gate mismatch` at `src/core/src/zava_forward/core/assistants.py:4064` (`C2`).
* Confirmed `reviewed_revision` is never queried by `Assistants._row()` or any Python/API view, eliminating any risk of falsely marking an unreviewed challenged proposal as human-reviewed (`C4`).
* Identified exact test filenames (`test_safety_consent_exercise_scenarios_81.py` in `src/core/tests` and `test_continuity_restart_gate.py` in `src/api/tests`) to avoid `unittest` module-not-found errors on prompt shorthand names (`C8`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Update `Assistants.challenge()` in `src/core/src/zava_forward/core/assistants.py` (`4064-4067`) to execute `UPDATE assistant_tasks SET body=?,state=?,review_gate_version=?,reviewed_revision=revision+1,revision=revision+1 WHERE id=? AND revision=?` with `(canonical(stored), state, continuity.GATE_VERSION, tid, revision)`, run Focused validation (`unittest`, `ruff check .`, `ruff format --check .`, `mypy` in both `src/core` and `src/api`, plus `tools/rename-zava-tests.py`), record `c2` changes and review under `safety-81-exercise-gates-*`, and commit locally on `feat/safety-81-exercise-gates` without pushing.
* Rationale: Aligns `Assistants.challenge()` with `Assistants.review()` (`C5`), preserves `#122` SQL trigger fences (`C3`, `C7`), fixes both `src-core` and `src-api` `#220` failures (`C2`), and leaves `#81` safety/consent invariants intact.
* Evidence refs: `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `C8`
* Implementation impact: 1 DML statement updated in `src/core/src/zava_forward/core/assistants.py` + complete dated `safety-81-exercise-gates` `.copilot-tracking/` artifact set committed locally.
* Confidence: high

### Alternative: Relax `assistant_tasks_gate_update` SQL trigger DDL for `ready -> ready` body updates

* Approach: Alter `SQLITE_ATTEMPT_TRIGGERS` and `MSSQL_ATTEMPT_TRIGGERS` so `OLD.state = 'ready' AND NEW.state = 'ready'` no longer checks `review_gate_version` and `reviewed_revision`.
* Trade-offs: Would break `test_restart_gate_sql_fences.py:542-550` (`C7`), weaken `#122`'s old-image SQL write fence for `verify` updates, and mutate SQL trigger DDL unnecessarily.
* Evidence refs: `C3`, `C7`
* Rejection rationale: Violates `#122` security/continuity SQL fence invariants and breaks existing `#122` trigger tests.

## Current Decisions

* Research disposition: `executed`
* Planning Readiness: `Ready`
* Validation tier: Focused (`src/core` and `src/api` targeted unit/integration suites, `ruff check .`, `ruff format --check .`, `mypy`, and `python3 tools/rename-zava-tests.py`) — single Python DML parameter-binding fix with zero SQL DDL/trigger/schema changes.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Keep `.copilot-tracking/` paths out of production code, comments, docs, and commit message; use local privacy-safe git email (`8036360+jmservera@users.noreply.github.com`) and do not push.
* Residual uncertainty: Remote PR `#1797` checks remain at `1be969f61` until the coordinator reviews and pushes the new frozen HEAD.
