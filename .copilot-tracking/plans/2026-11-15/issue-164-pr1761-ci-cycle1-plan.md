<!-- markdownlint-disable-file -->
# RPI Plan: Issue #164 PR #1761 Cycle 1 Hosted CI `src-api` Fix

## Task Metadata

* Task ID: issue-164-pr1761-ci-cycle1
* Task slug: issue-164-pr1761-ci-cycle1
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-164-pr1761-ci-cycle1-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/issue-164-pr1761-ci-cycle1-plan-critique.md

## Executive Summary

This Cycle 1 plan fixes the hosted CI (`src-api`) failure on PR #1761 (`feat/ai-164-chat-revocation-0042`, Issue #164) in `test_manager_report_local_http_and_bad_period` (`src/api/tests/test_ai_consumption_api.py`). Commit `7124ab572` added the separate top-level `chat_evaluation` sibling to `GET /api/ai/report`, including during `"meter-capacity-reached"` and `"meter-evidence-invalid"` consumption holds, while `test_ai_consumption_api.py` still asserted the four pre-#164 top-level keys `{"evaluation", "live", "registry", "consumption"}`. Updating the held-report assertion set to include `"chat_evaluation"` and verifying `held["chat_evaluation"]` parity (`keys`, `version`, and `enablement.state == "disabled"`) against `result["chat_evaluation"]` aligns the consumption-hold contract with `/api/ai/report`.

### User Decisions and Requirements Highlights

* Update `src/api/tests/test_ai_consumption_api.py` (and related held-report assertions) so `chat_evaluation` is expected in `set(held)` when metering is held, update `.copilot-tracking/` Cycle 1 RPI artifacts, pass the targeted `src/api` `unittest`, `ruff`, and `mypy` suite, and commit locally with `Refs #164` and the Copilot trailer without pushing.

### What You May Not Know

* In `src/api/src/zava_forward/api/server.py`, `GET /api/ai/report` catches `ai_consumption.DispatchHeld` only around `consumption` and still executes both `ai_eval.run_eval()` and `chat_eval.run_eval()` (`C2`), so held responses preserve `chat_evaluation` (`version`, `passed`, and `enablement.state == "disabled"`) identically to `evaluation`.
* Repository-wide search confirms `src/api/tests/test_ai_consumption_api.py` is the only test asserting an exact top-level key set on `/api/ai/report` that omitted `"chat_evaluation"` (`C3`).

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run a Cycle 1 RPI fix in `/home/azureuser/source/ama-demo-wt/feat-164-chat-revocation-0042` on branch `feat/ai-164-chat-revocation-0042` for PR #1761 (Issue #164) (caller prompt).
* Update `src/api/tests/test_ai_consumption_api.py` (and any related assertion) so `chat_evaluation` is expected in `set(held)` when held, resolving `AssertionError: Items in the first set but not the second: 'chat_evaluation'` in `test_manager_report_local_http_and_bad_period` (caller prompt; `C1`–`C3`).
* Update `.copilot-tracking/` Cycle 1 changes/review artifacts preserving original RPI history (caller prompt; repository RPI rules).
* Run `cd /home/azureuser/source/ama-demo-wt/feat-164-chat-revocation-0042/src/api && PYTHONPATH=src:tests:../core/src:../agents/src:../orchestrator/src:../importer/src:../core/tests:../agents/tests python3 -B -m unittest tests/test_ai_consumption_api.py tests/test_ai_tasks.py && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy tests/test_ai_consumption_api.py` (caller prompt; `C4`).
* Commit with `Refs #164` and trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, do NOT push, and leave a clean frozen worktree (`git status --short` empty) (caller prompt).

## Goals

* Align `test_manager_report_local_http_and_bad_period` in `src/api/tests/test_ai_consumption_api.py` with the separate `chat_evaluation` field added to `GET /api/ai/report` in Issue #164.
* Verify `src/api` unit tests (`test_ai_consumption_api.py`, `test_ai_tasks.py`), `ruff check`, `ruff format --check`, and `mypy` pass cleanly under the focused validation tier.

## Scope and Non-Goals

### In Scope

* Updating held-report key-set and `chat_evaluation` parity assertions in `src/api/tests/test_ai_consumption_api.py`.
* Recording Cycle 1 RPI artifacts under `.copilot-tracking/*/2026-11-15/issue-164-pr1761-ci-cycle1-*` and executing focused `src/api` validation.

### Non-Goals

* Modifying `src/api/src/zava_forward/api/server.py` or enabling live chat tasks (`state` remains `"disabled"`).
* Running `tools/rpi-checks.py --all` or pushing to `origin`.

## Functional Requirements

* Held `/api/ai/report` responses assert the complete 5-key top-level payload and `chat_evaluation` parity.
  * Observable acceptance criteria: For both `"meter-capacity-reached"` and `"meter-evidence-invalid"` holds in `test_manager_report_local_http_and_bad_period`, `set(held)` equals `{"evaluation", "chat_evaluation", "live", "registry", "consumption"}`, `set(held["chat_evaluation"])` equals `set(result["chat_evaluation"])`, `held["chat_evaluation"]["version"]` equals `result["chat_evaluation"]["version"]`, and `held["chat_evaluation"]["enablement"]["state"]` equals `"disabled"`.

## Non-Functional Requirements

* Focused `src/api` test, lint, format, and static-type cleanliness.
  * Objective threshold or evaluation condition: Zero failures across `unittest`, `ruff check`, `ruff format --check`, and `mypy`.
  * Operating condition or verification approach, if needed: Caller-specified `src/api` validation command with explicit `PYTHONPATH` and `-B`.
  * Observable acceptance criteria: Command exits `0` and leaves zero untracked/bytecode files in `git status --short`.

## Acceptance Criteria

* `test_manager_report_local_http_and_bad_period` passes for both `"meter-capacity-reached"` and `"meter-evidence-invalid"` subtests with `"chat_evaluation"` verified in `set(held)` and parity-checked against `result["chat_evaluation"]`.
* `tests/test_ai_consumption_api.py`, `tests/test_ai_tasks.py`, `ruff check src tests`, `ruff format --check src tests`, and `mypy tests/test_ai_consumption_api.py` all exit `0`.
* Cycle 1 RPI tracking artifacts (`.copilot-tracking/*/2026-11-15/issue-164-pr1761-ci-cycle1-*`) are complete, reconciled, and committed cleanly with `Refs #164` and the Copilot trailer without pushing.

## Test Ownership and Evidence Matrix

| Target test file | Exact removals | Maximum additions | Canonical targets covered | Semantic vs regression role | Validation command |
|---|---|---|---|---|---|
| `src/api/tests/test_ai_consumption_api.py` | `none` | `0` new test methods (in-place assertion update in `test_manager_report_local_http_and_bad_period`) | `src/api/src/zava_forward/api/server.py` (`GET /api/ai/report` held-metering contract) | API contract regression for `chat_evaluation` presence and parity under consumption holds | `cd src/api && PYTHONPATH=src:tests:../core/src:../agents/src:../orchestrator/src:../importer/src:../core/tests:../agents/tests python3 -B -m unittest tests/test_ai_consumption_api.py tests/test_ai_tasks.py` |

## Sources

* `.copilot-tracking/research/2026-11-15/issue-164-pr1761-ci-cycle1-research.md`: Evidence IDs `C1`–`C4` establishing the hosted `src-api` CI failure, `/api/ai/report` held-response contract, and focused validation scope.
* `.copilot-tracking/plans/2026-11-15/issue-164-chat-eval-revocation-plan.md`: Parent Issue #164 plan introducing separate `chat_evaluation` on `/api/ai/report`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Align Held Manager Report Test Contract and Validate `src/api`

* Intent: Update `test_manager_report_local_http_and_bad_period` in `src/api/tests/test_ai_consumption_api.py` to expect `chat_evaluation` during consumption holds and verify `src/api` unit, lint, format, and `mypy` checks.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Update held `/api/ai/report` assertions in `src/api/tests/test_ai_consumption_api.py` and run focused validation

* Requirement and evidence: Hosted `src-api` CI failure on `set(held)` and `chat_evaluation` parity during metering holds (`C1`–`C4`).
* Expected result: `test_manager_report_local_http_and_bad_period` asserts `set(held) == {"evaluation", "chat_evaluation", "live", "registry", "consumption"}` plus `held["chat_evaluation"]` key, version, and `"disabled"` enablement parity, and the full `src/api` `unittest` + `ruff` + `mypy` validation command exits `0`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-164-pr1761-ci-cycle1-phase-details.md

## Dependencies

* `src/api/src/zava_forward/api/server.py` and `src/agents/src/zava_forward/agents/chat_eval.py`: Existing Issue #164 implementation emitting `chat_evaluation` with `version` and `enablement.state == "disabled"`.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass critique (`Pass`, 0 findings) | Accepted | Candidate plan and `P01-T01` details verified ready against `server.py` and `test_ai_consumption_api.py`; downstream coordinator owns any pre-push external receipt refresh if applicable. |

## Follow-Up Items

* Post-merge Issue #164 owner governance prerequisites (`RV-001` from parent task `issue-164-chat-eval-revocation`): non-implementer held-out scenario labelling, measured 4-part reviewer effort against the case-card comparator, budget-authorized serving-model run, and owner threshold approval before changing `chat-case-conversation` from `disabled`.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-164-pr1761-ci-cycle1-changes.md
* Ready phase or task: Complete (`P01`, `P01-T01`); ready for `rpi-review`
* Remaining provisional question or blocker: None
