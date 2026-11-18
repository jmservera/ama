<!-- markdownlint-disable-file -->
# RPI Plan: PR #1745 Cycle-2 Rebase of Issue #1288 onto `origin/feat/demo-164-chat-grounding-provenance-0900`

## Task Metadata

* Task ID: quality-1288-sensor-ai-2142-c2
* Task slug: quality-1288-sensor-ai-2142-c2
* Parent task ID: quality-1288-sensor-ai-2142
* Planning status: ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan-critique.md

## Executive Summary

This plan rebases `feat/quality-1288-sensor-ai-2142` (`a2a39b2cf`, Issue #1288, PR #1745) onto `origin/feat/demo-164-chat-grounding-provenance-0900` at `5f50fc238` and resolves the sole merge conflict in `src/core/src/zava_forward/core/chat_case_answers.py` (`_sensor(r: Reply)`). Upstream commit `2b1d40db0` (`PR #1734`) updated `_sensor(r)` so that when `not cite`, any `sensor.detail` emits `"No retained sensor reading is shown for this case. {detail}"` before delegating to `return _damp(r)`. Meanwhile, Issue #1288 (`a2a39b2cf`) added `sensor.conflict` and `sensor.source` facts so identical-timestamp reading conflicts return an explicit conflict message without claiming no reading is shown, and clean readings cite their synthetic source description. We resolve `_sensor(r)` by checking `conflict = r.fact("sensor.conflict")` first under `if not cite:` (returning early before `r.fact("sensor.detail")` is touched), delegating non-conflict `not cite` states to `detail` + `return _damp(r)`, preserving `sensor.source` when `cite` is present, adding a focused unit test in `src/core/tests/test_chat_case_answers.py` (`DomainAnswerTests`), verifying strictly with `-p` test selectors plus bare `mypy` and `ruff` in `src/core` and `src/api`, and committing locally with Cycle-2 tracking artifacts without pushing.

### User Decisions and Requirements Highlights

* Rebase `feat/quality-1288-sensor-ai-2142` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238`) preserving both Issue #1288 `sensor.conflict` handling and `#157`/`#164` `_damp(r)` fallback when `not cite` and `not conflict` (`Caller prompt`) -> `P01-T01` rebases `a2a39b2cf` linearly onto `5f50fc238` and resolves `chat_case_answers.py`.
* Run ONLY targeted `unittest discover -s tests -p ...` commands (never unscoped `unittest discover -s tests` without `-p`) plus bare `mypy`, `ruff check .`, and `ruff format --check .` in `src/core` and `src/api` (`Caller prompt`) -> `P02-T01` enforces explicit `-p` patterns on every test runner invocation.
* Commit locally with `.copilot-tracking/` Cycle-2 artifacts and `Refs #1288` + Copilot `Co-authored-by` trailers, and do NOT push (`Caller prompt`) -> `P02-T01` configures privacy-safe local git identity via `gh api user` and commits locally without pushing.

### What You May Not Know

* Because `sensor_facts(view)` populates `sensor.detail` with `view.get("detail") or view.get("conflict_notice")`, calling `r.fact("sensor.detail")` before checking `r.fact("sensor.conflict")` would record an unwanted `case-record` citation (`{case_id}/sensor.detail`) or emit `"No retained sensor reading is shown for this case."` on conflicts; checking `conflict = r.fact("sensor.conflict")` first and returning immediately avoids both regressions.
* `src/core/tests/test_chat_domain_questions.py` does not exist at `5f50fc238` (so `-p 'test_chat_domain_questions.py'` runs `0` tests); the actual domain-question tests introduced on `5f50fc238` (`2b1d40db0`) live in `src/core/tests/test_chat_case_answers.py` (`DomainAnswerTests`) and `src/agents/tests/test_regulatory_chat_case_domain_grounding.py` (`CaseDomainGroundingTests`). `P02-T01` runs all caller-specified `-p` commands AND explicit `-p` runs for those real domain test modules plus `test_quality_sensors.py`.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `rpi-plan-critique`, `implement`, `review`) in `/home/azureuser/source/ama-demo-wt/feat-1288-quality-sensor-ai-2142` on branch `feat/quality-1288-sensor-ai-2142` for Issue #1288 (`PR #1745` Cycle-2 rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900` at `5f50fc238`) (`Caller prompt`).
* Preserve Issue #1288's `conflict = r.fact("sensor.conflict")` branch in `_sensor(r: Reply)` when `not cite` and `conflict` is present (emitting `"Retained sensor readings conflict, so no single value is selected. " + conflict + " Use the ordinary quality check, or ask the quality team to inspect the home."` plus `sensor.not_retained` and `stage` if present, and returning) AND preserve `sensor.source` when `cite` is present (`Caller prompt`; `.copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-c2-research.md` `C3`, `C4`, `C8`).
* Preserve `#157`/`#164` (`2b1d40db0` on `5f50fc238`) behavior in `_sensor(r: Reply)` when `not cite` and `not conflict`: emit `"No retained sensor reading is shown for this case. {detail}"` when `detail := r.fact("sensor.detail")` is present, then `return _damp(r)` (`Caller prompt`; research `C2`, `C6`, `C7`).
* Run focused validation using ONLY `-p`-scoped `unittest discover` commands (never unscoped `unittest discover -s tests` without `-p`), plus bare `mypy`, `ruff check .`, and `ruff format --check .` in `src/core` and `src/api` (`Caller prompt`).
* Commit the rebased/resolved branch locally with `.copilot-tracking/` Cycle-2 artifacts and trailers (`Refs #1288`, `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`), using privacy-safe GitHub noreply identity (`gh api user`), and do NOT push (`Caller prompt`, `.github/copilot-instructions.md`).

## Goals

* Rebase `feat/quality-1288-sensor-ai-2142` cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238`) with zero lost hunks from `a2a39b2cf` or `5f50fc238`.
* Ensure `_sensor(r: Reply)` in `src/core/src/zava_forward/core/chat_case_answers.py` handles all three regimes (`not cite` with `sensor.conflict`, `not cite` without `sensor.conflict` delegating to `_damp(r)`, and grounded `cite` with `sensor.source`) with exact citation kinds.
* Prove combined behavior with a focused seam test in `src/core/tests/test_chat_case_answers.py`, targeted `-p` test runs across core, agents, and api, and clean static checks (`mypy`, `ruff`), leaving a clean unpushed local branch.

## Scope and Non-Goals

### In Scope

* Git rebase of `feat/quality-1288-sensor-ai-2142` (`a2a39b2cf`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238`), resolving `src/core/src/zava_forward/core/chat_case_answers.py` and verifying clean auto-merge of `src/core/src/zava_forward/core/chat_panel.py` and all other `a2a39b2cf` files.
* Focused seam unit test addition in `src/core/tests/test_chat_case_answers.py` (`DomainAnswerTests`), locking test ownership to at most `1` modified test file, `0` test removals, and at most `2` new test methods.
* Focused `-p` unit/integration verification and static (`mypy`, `ruff check`, `ruff format --check`) verification in `src/core` and `src/api` (plus targeted `-p` domain-grounding check in `src/agents` and `-p` content-standard check in `src/api`).
* Cycle-2 `.copilot-tracking/` artifacts (`research`, `plan`, `details`, `critique`, `changes`, `review`, `state.json`) and local commit(s) on `feat/quality-1288-sensor-ai-2142`.

### Non-Goals

* Pushing any branch or tag to `origin` or mutating PR #1745 remotely.
* Running unscoped `unittest discover -s tests` without `-p` in any package.
* Modifying `sensor_view.py`, `assistants.py`, `sensor_badges.py`, `web/*.js`, `styles.css`, infrastructure, workflows, or unrelated commits on `5f50fc238`.

## Functional Requirements

* Rebased branch ancestry on `feat/quality-1288-sensor-ai-2142` must sit directly atop `5f50fc238` (`origin/feat/demo-164-chat-grounding-provenance-0900`) and preserve all 12 source/test files from `a2a39b2cf`.
  * Observable acceptance criteria: `git merge-base origin/feat/demo-164-chat-grounding-provenance-0900 HEAD` equals `5f50fc238f78e37e31baaed87f5d1eb81943cf14`, and `git diff 5f50fc238..HEAD -- src/` contains all `a2a39b2cf` changes reconciled with `5f50fc238`.
* `_sensor(r: Reply)` in `src/core/src/zava_forward/core/chat_case_answers.py` must satisfy both Issue #1288 and `#157`/`#164` contracts.
  * Observable acceptance criteria:
    1. When `not cite` and `conflict := r.fact("sensor.conflict")` is non-empty, `_sensor(r)` emits `"Retained sensor readings conflict, so no single value is selected. " + conflict + " Use the ordinary quality check, or ask the quality team to inspect the home."` (plus `sensor.not_retained` and `Case stage: {stage}.` when present), cites `{case_id}/sensor.conflict` without citing `{case_id}/sensor.detail` or emitting `"No retained sensor reading is shown"`, and returns early.
    2. When `not cite` and `not conflict`, `_sensor(r)` emits `"No retained sensor reading is shown for this case. {detail}"` if `detail := r.fact("sensor.detail")` is present, and returns `_damp(r)` (including `[Origin: decision_rule]`, matching damp hazards, `sensor_review_drafts`, Survey document note, and `workflow/domain-boundary`).
    3. When `cite` is non-empty, `_sensor(r)` emits the exact retained `temperature_c`, `humidity_pct`, and `observed_at` line, followed by `Reading source: {r.facts['sensor.source']}` (citing `{case_id}/sensor.source` as `decision-rule`), freshness/health/watch/thresholds, `sensor.not_retained`, and the synthetic uncalibrated framing sentence.

## Non-Functional Requirements

* Static typing, lint, and formatting compliance (`focused` validation tier, owner decision D4 / issue #1294).
  * Objective threshold or evaluation condition: Zero errors from `python3 -m mypy`, `python3 -m ruff check .`, and `python3 -m ruff format --check .` in both `src/core` and `src/api`.
  * Operating condition or verification approach, if needed: Run directly in `src/core` and `src/api` after rebase and seam-test edits.
  * Observable acceptance criteria: Exit code `0` across all six commands.
* Strict `-p` test execution discipline and repository git/privacy hygiene.
  * Objective threshold or evaluation condition: Every `unittest discover` invocation specifies `-p '<pattern>'`; local git user email matches `{id}+{login}@users.noreply.github.com` from `gh api user`; working tree is clean (`git status --short` empty) after final local commit; `origin/feat/quality-1288-sensor-ai-2142` is untouched (no push).
  * Observable acceptance criteria: All targeted `-p` suites exit `0` with non-zero executed test counts on the actual domain and sensor test files, and `git status --short` outputs nothing.

## Acceptance Criteria

* `feat/quality-1288-sensor-ai-2142` is rebased onto `5f50fc238` (`origin/feat/demo-164-chat-grounding-provenance-0900`) with `src/core/src/zava_forward/core/chat_case_answers.py` cleanly resolved and `chat_panel.py` retaining `SENSOR_RULE_PATHS` (`"sensor.source"`, `"sensor.conflict"`), `RULES_FIRST`, `RULES_SOURCE_ROOTS`, and `skill_sources` `common`.
* `DomainAnswerTests` in `src/core/tests/test_chat_case_answers.py` includes strict-typed (`-> None`) seam test coverage verifying both `not cite` branches (`sensor.conflict` early return vs `not conflict` `sensor.detail` + `_damp(r)` delegation), clean `cite` `sensor.source` grounding, and `ChatPanel._rules_answer(..., skill="resident-communications")` + `ChatPanel._source_kind(...)` provenance under a non-general skill lens (`<= 1` test file modified, `0` test removals, `<= 2` test methods added).
* All caller-requested validation commands (`mypy`, `ruff check .`, `ruff format --check .` in `src/core` and `src/api`; `-p 'test_chat_domain_questions.py'`, `-p 'test_sensor_view_conflicts.py'` in `src/core`; `-p 'test_quality_sensor_grounding.py'`, `-p 'test_quality_sensors_correlation.py'` in `src/api`) PLUS explicit `-p` runs for the real domain and sensor suites (`-p 'test_chat_case_answers.py'`, `-p 'test_chat_panel.py'` in `src/core`; `-p 'test_regulatory_chat_case_domain_grounding.py'` in `src/agents`; `-p 'test_quality_sensors.py'`, `-p 'test_sensor_staleness_ui_badge.py'`, `-p 'test_content_standard.py'` in `src/api`) pass with exit code `0`.
* Cycle-2 `.copilot-tracking/` implementation artifacts (`research`, `plan`, `phase-details`, `plan-critique`, `changes`, and `state.json`) are committed locally in `Implement` before `Review`, followed by a read-only `rpi-review` (`review` log + final `state.json` closeout commit) with `Refs #1288` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, clean `git status --short`, and no push.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan.md                                          |
| Phase details                    | .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md                               |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-14/quality-1288-sensor-ai-2142-c2-plan-critique.md (`Revise`; `PC-001`, `PC-002` resolved) |
| Relevant research                | .copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-c2-research.md                                   |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-c2-changes.md is created by implementation         |
| Planning execution and readiness | Ready for `Implement` (`focused` validation tier; hosted CI unobserved on unpushed branch; post-implementation `rpi-review` creates final tracking closeout commit) |
| Continuation context             | Confirmed automatic RPI Agent parent transitions directly to `Implement` (`P01` -> `P02`)                          |

## Sources

* `.copilot-tracking/research/2026-11-14/quality-1288-sensor-ai-2142-c2-research.md`: Codebase evidence `C1`–`C10`, `git merge-tree` verification, contrarian trap analysis, and selected Option A.
* `.copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-changes.md`: Cycle-1 (`a2a39b2cf`) baseline scope and validation record.
* `.github/copilot-instructions.md`: Focused validation tier rules (D4 / #1294), Web Development Guidance, local privacy-safe git identity (`gh api user`), and trailer conventions.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Rebase `feat/quality-1288-sensor-ai-2142` onto `5f50fc238` and Resolve `_sensor(r)` Conflict

* Intent: Linearly rebase `a2a39b2cf` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`5f50fc238`) and resolve `src/core/src/zava_forward/core/chat_case_answers.py` so both Issue #1288 conflict/provenance rules and `#157`/`#164` `_damp(r)` fallback work together without citation pollution.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Configure local privacy-safe git identity, rebase `a2a39b2cf` onto `5f50fc238`, and resolve `chat_case_answers.py`

* Requirement and evidence: Research `C1`–`C5`, `C8`–`C10`; Caller prompt items 1–3.
* Expected result: Privacy-safe local `user.name` and `user.email` are configured via `gh api user`; tracked `.copilot-tracking/rpi-sessions/2026-11-14/quality-1288-sensor-ai-2142-state.json` is clean prior to starting `git rebase 5f50fc238`; `chat_case_answers.py` `_sensor(r)` checks `conflict = r.fact("sensor.conflict")` first under `if not cite:` (returning early before `r.fact("sensor.detail")` is called), delegates `not cite and not conflict` to `detail = r.fact("sensor.detail")` + `return _damp(r)`, and retains `if r.fact("sensor.source"):` when `cite` is present; rebase completes cleanly atop `5f50fc238`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Seam Unit Test, Focused `-p` Verification, and Local Cycle-2 Commit

* Intent: Add direct unit coverage for the merged `_sensor(r)` seam in `src/core/tests/test_chat_case_answers.py`, run all caller-specified and actual domain/sensor `-p` test suites plus `mypy` and `ruff`, and commit Cycle-2 code/test and `.copilot-tracking/` evidence locally without pushing.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add `DomainAnswerTests` seam test in `test_chat_case_answers.py`, run `-p` tests and `mypy`/`ruff`, and commit `Implement` artifacts locally

* Requirement and evidence: Research `C5`–`C8`; Critique `PC-001`, `PC-002`; Caller prompt Validation Tier (Focused) and commit instructions.
* Expected result: `DomainAnswerTests` in `src/core/tests/test_chat_case_answers.py` gains strict-typed (`-> None`) seam assertions for `not cite` with `sensor.conflict` vs `not cite` without `sensor.conflict` (`sensor.detail` + `_damp(r)`), clean `cite` with `sensor.source`, and `ChatPanel._rules_answer(..., skill="resident-communications")` + `ChatPanel._source_kind(...)` provenance (`1` test file modified, `0` removals, `<= 2` new test methods); `mypy`, `ruff check .`, and `ruff format --check .` pass in `src/core` and `src/api`; all caller-requested `-p` commands and explicit `-p` domain/sensor test files pass; Cycle-2 implementation changes and reconciled pre-review `.copilot-tracking/` artifacts (`research`, `plan`, `phase-details`, `plan-critique`, `changes`, `state.json`) are committed locally with `Refs #1288` and Copilot trailer before `Review` without pushing.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/quality-1288-sensor-ai-2142-c2-phase-details.md

## Dependencies

* `P01` precedes `P02`: `DomainAnswerTests` in `src/core/tests/test_chat_case_answers.py` only exists on `feat/quality-1288-sensor-ai-2142` after rebasing onto `5f50fc238`.
* Worktree `PYTHONPATH` prefixing (`PYTHONPATH=src:tests` in `src/core`; `PYTHONPATH=../core/src:src:tests` in `src/agents`; `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:../orchestrator/src:../importer/src:src` in `src/api`) ensures worktree code is tested rather than any shared editable install.
* Every `unittest discover` invocation must pass `-p '<filename>.py'`.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 — `PC-001` [Medium]| resolved    | Separated `P02` (`Implement`) targets and local commit (`test_chat_case_answers.py`, `c2-research.md`, `c2-plan.md`, `c2-phase-details.md`, `c2-plan-critique.md`, `c2-changes.md`, `state.json`) from post-implementation `rpi-review` (`c2-review.md` + final `state.json` closeout commit). |
| Run 1 — `PC-002` [Low]   | resolved    | Extended `P02-T01` `DomainAnswerTests` seam coverage to exercise `ChatPanel._rules_answer(..., skill="resident-communications")` and `ChatPanel._source_kind(...)` across `sensor.conflict`, non-conflict `sensor.detail` + `_damp(r)`, and clean `cite` (`sensor.source`). |

## Follow-Up Items

* Carried forward from parent task `quality-1288-sensor-ai-2142` (`RV-001`): adjust `#employee-chat` vertical flex/max-height spacing in `src/api/src/zava_forward/api/web/styles.css` to clear the pre-existing `#employee-chat-question` `target-size` (`partiallyObscured`) axe failure at 720px viewport height.
* Carried forward from parent task `quality-1288-sensor-ai-2142` (`RV-002`): add an automated browser scenario in `src/api/checks/quality_sensors_browser_check.py` exercising live conflicting-reading arrival (`data-sensor-conflict`, `data-flag-conflict`, `data-flag-sources`) under pinned `axe-core` 4.10.3.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/quality-1288-sensor-ai-2142-c2-changes.md
* Ready phase or task: Complete (`P01` and `P02` completed; ready for `Review` via `rpi-review` writing `.copilot-tracking/reviews/logs/2026-11-14/quality-1288-sensor-ai-2142-c2-review.md` and creating the final local tracking closeout commit)
* Remaining provisional question or blocker: None; hosted CI remains unobserved locally because pushing is prohibited (`Do NOT push`).
