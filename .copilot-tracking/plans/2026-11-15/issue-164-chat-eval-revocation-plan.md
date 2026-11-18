<!-- markdownlint-disable-file -->
# RPI Plan: Issue #164 Chat Multi-Turn Revocation, Refusal Preservation, and Separate Held-Out Evaluation

## Task Metadata

* Task ID: issue-164-chat-eval-revocation
* Task slug: issue-164-chat-eval-revocation
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-164-chat-eval-revocation-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/issue-164-chat-eval-revocation-plan-critique.md

## Executive Summary

This plan delivers the remaining local-testable RAI multi-turn, revocation, refusal-routing, and version-bound evaluation criteria for Issue #164 (`Grounding, evaluation and human-review boundaries for chat`) across `src/core`, `src/agents`, and `src/api`. It introduces a pure-`core` multi-turn chat and held-out evaluation contract (`src/core/src/zava_forward/core/ai_eval.py`), closes mid-thread resident AI-consent revocation and fallback out-of-scope routing gaps in `RegulatoryChat` (`src/core/src/zava_forward/core/regulatory_chat.py`), tightens held-out freeze verification so scenarios cannot pass with unfrozen per-turn expected outcomes (`chat_heldout.py`), and exposes multi-turn `chat_evaluation` separately from single-turn `evaluation` on `/api/ai/report` while keeping live chat enablement `disabled`.

### User Decisions and Requirements Highlights

* Deliver deterministic unit coverage in `src/core` (`ai_eval.py`, `regulatory_chat.py`, `tests/test_ai_eval.py`) and `src/api` (`tests/test_ai_tasks.py`) proving mid-thread permission and source revocation clear prior-turn authority, multi-turn out-of-scope asks preserve human workflow routes without manufactured approval or consent, and held-out evaluation freezes expected outcomes, critical errors, and 6 version bindings while reporting chat multi-turn results separately from single-turn task results.
* Keep live task enablement `disabled` until owner threshold approval, use the focused validation tier (`unittest`, `mypy`, `ruff`) without running `tools/rpi-checks.py --all`, and create a clean local commit with the Copilot trailer without pushing.

### What You May Not Know

* `src/core/tests/test_dependency_rule.py` enforces `ALLOWED = {"core"}` for every `.py` file under `src/core/src` and `src/core/tests` (`C1`). `zava_forward.core.ai_eval` therefore imports only `zava_forward.core.*` and never imports `zava_forward.agents` or `zava_forward.api`.
* `chat_heldout.freeze_problems` previously verified the file SHA-256, independent labeller, critical errors, and 6 version bindings, but did not verify that each held-out turn freezes a concrete expected outcome (`expect.kind` or `expect.error`), allowing turns with `expect={}` to pass vacuously (`C10`, `C11`).
* `agents/tests/regulatory_gate_fixture.py` asserts the exact string `"This question needs a human decision or legal interpretation."` when `agents.regulatory_chat.refusal` is wired (`C17`); `RegulatoryChat` therefore honors a non-empty `self.refuse(question)` first and falls back to `REFUSED + out_of_scope(question)[1]` when `self.refuse` returns `None` (`C16`).

### Unresolved Decisions or Blockers

* None for this offline local-testable increment. Owner threshold approval, real independently labelled held-out exercises, live serving-model evaluation, and competent-human effectiveness exercises remain explicit post-merge human gates (`state="disabled"`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`rpi-research`, `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, `rpi-review`) writing dated artifacts under `.copilot-tracking/research/`, `.copilot-tracking/plans/`, `.copilot-tracking/details/`, `.copilot-tracking/changes/`, and `.copilot-tracking/reviews/` for Issue #164 (caller prompt).
* Work on the active coordinator worktree branch stacked on `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) and leave a clean frozen local commit with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing (caller prompt; worktree `feat/ai-164-chat-revocation-0042` at `fef48b6df`).
* Inspect and cover `src/core/src/zava_forward/core/ai_eval.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/tests/test_ai_eval.py`, and `src/api/tests/test_ai_tasks.py` (caller prompt).
* Prove with deterministic unit tests that prior-turn content cannot retain authority after permission or source revocation mid-thread, covering unsupported claims with valid citations, stale/conflicting sources, ambiguity, abstention, and mid-thread revocation (caller prompt; Issue #164; PRD FR-036/FR-037/AC-054).
* Prove that multi-turn requests to approve, decide, consent, diagnose, or contact residents preserve existing refusal and human workflow routes, and that previous conversation turns or memory cannot manufacture approval or resident consent (caller prompt; Issue #164; PRD AC-045/AC-057).
* Verify and regression-test that independently labelled held-out conversation scenarios freeze expected outcomes, critical errors, and `task`/`model`/`prompt`/`policy`/`source`/`memory` versions before testing, and that chat-specific failures and complete review effort are reported separately from single-turn task results while keeping live task enablement `disabled` until owner threshold approval (caller prompt; Issue #164; PRD v0.16.0 RAI evaluation contract).
* Validate using the focused tier (`python3 -m unittest discover -s tests -p "test_*ai_eval*.py" -q` in `src/core`, focused tests in `src/api`, `python3 -m mypy`, `python3 -m ruff check .`, and `python3 -m ruff format --check .`); do not run `tools/rpi-checks.py --all` (caller prompt).

## Goals

* Establish a pure-`core` deterministic multi-turn chat evaluation and version-bound held-out freeze module (`zava_forward.core.ai_eval`) that satisfies `src/core`'s strict `ALLOWED = {"core"}` boundary.
* Close mid-thread resident AI-consent withdrawal and core-level out-of-scope refusal routing gaps in `RegulatoryChat` while preserving existing extractive regulatory gate contracts.
* Guarantee that held-out scenario sets freeze per-turn expected outcomes alongside critical errors and all six version bindings before scoring, and surface multi-turn chat evaluation (`chat_specific` failures, complete `review_effort`, and `state="disabled"` enablement) separately from single-turn task evaluation across `core`, `agents`, and `/api/ai/report`.

## Scope and Non-Goals

### In Scope

* Creating `src/core/src/zava_forward/core/ai_eval.py` and `src/core/tests/test_ai_eval.py` with zero imports outside `zava_forward.core`.
* Hardening `src/core/src/zava_forward/core/regulatory_chat.py` and extending `src/core/tests/test_regulatory_chat.py` for mid-thread `ai_data_use_consent` revocation and fallback `out_of_scope` human-workflow refusal routing.
* Extending `src/agents/src/zava_forward/agents/chat_eval.py`, `src/agents/evals/chat_golden.json`, `src/agents/src/zava_forward/agents/chat_heldout.py`, and `src/agents/tests/test_chat_heldout.py` for mid-thread source-field/AI-consent revocation, ambiguity abstention, and mandatory per-turn frozen expected outcomes.
* Exposing separate `chat_evaluation` alongside single-turn `evaluation` in `/api/ai/report` (`src/api/src/zava_forward/api/server.py`) and regression-testing in `src/api/tests/test_ai_tasks.py`.

### Non-Goals

* Enabling `chat-case-conversation` or any live provider calls (`state` remains `"disabled"` and `ai_registry.authorizes_live("chat-case-conversation")` remains `False`).
* Fabricating owner threshold approval, accountable reviewer appointments, actual-model runs, or human effectiveness trial results.
* Running `tools/rpi-checks.py --all` or pushing commits to `origin`.

## Functional Requirements

* Mid-thread permission, source, rule-card, and AI-consent revocation clear prior-turn authority across `ChatPanel` and `RegulatoryChat`.
  * Observable acceptance criteria: After mid-thread role downgrade, staff removal, case removal, case-field deletion (`revoke_source`), regulatory rule-card hold/retirement/provision supersession, or `ai_data_use_consent` change from `"Given"` to `"Withdrawn"`/`"Declined"`, subsequent turns exclude or block prior-turn content, drop revoked citations, withhold unsupported numeric/status claims on valid citations (`UNGROUNDED`), abstain or flag conflicts on stale/conflicting/ambiguous inputs, and block `RegulatoryChat.doubt` forwarding when AI consent is withdrawn.
* Multi-turn out-of-scope requests preserve refusal and human workflow routes without manufactured authority.
  * Observable acceptance criteria: Multi-turn requests to `approve`, `decide`, `consent`, `diagnose`, or `contact` residents after valid cited turns or poisoned memory (`authority="none"`, `evidence=False`) return refused/withheld outcomes with `model_calls == 0` for pre-model refusals, preserve human workflow routes (`reviewer`/`sign-off`, `accountable person`, `consent control`, `qualified` specialist, `contact log`), and never create approval or resident consent across `ChatPanel` or `RegulatoryChat`.
* Held-out conversation scenarios enforce pre-test expected-outcome and version freezes, and chat multi-turn evaluation reports separately from single-turn evaluation with `disabled` enablement.
  * Observable acceptance criteria: `freeze_problems` blocks scoring (`scored=False`, `outcome="insufficient"`) when `scenarios_sha256` or optional `expected_outcomes_sha256` mismatches, `labelled_by` is blank or matches the implementer, `frozen_at` or `critical_errors` is missing, any of `(task, model, prompt_version, policy_version, source_version, memory_version)` changed since freeze, any scenario/turn omits a frozen expected outcome (`expect.kind` or `expect.error`), or development/prompt text leaks; `/api/ai/report` and `separate_evaluation_report` emit multi-turn `chat_evaluation` (`chat_specific` failures, 4-part `review_effort`, `enablement.state == "disabled"`) separately from single-turn `evaluation`.

## Non-Functional Requirements

* Package architecture isolation in `src/core`.
  * Objective threshold or evaluation condition: Zero imports from `zava_forward.agents` or `zava_forward.api` in `src/core/src` and `src/core/tests`.
  * Operating condition or verification approach, if needed: Verified via `src/core/tests/test_dependency_rule.py`.
  * Observable acceptance criteria: `DependencyRuleTests` passes with `ai_eval.py` and `test_ai_eval.py` present.
* Deterministic, offline test execution and static type/style cleanliness.
  * Objective threshold or evaluation condition: Zero network/provider calls, 100% deterministic pass across `unittest`, `mypy`, `ruff check`, and `ruff format --check`.
  * Operating condition or verification approach, if needed: Local focused test commands in `src/core`, `src/agents`, and `src/api`.
  * Observable acceptance criteria: All targeted unit suites, `mypy`, and `ruff` exit `0`.

## Acceptance Criteria

* `src/core/src/zava_forward/core/ai_eval.py` and `src/core/tests/test_ai_eval.py` exist, obey `ALLOWED = {"core"}`, and pass `python3 -m unittest discover -s tests -p "test_*ai_eval*.py" -q`.
* Deterministic tests prove prior-turn content retains no authority after mid-thread permission, source, rule-card, or AI-consent revocation, and cover unsupported claims with valid citations, stale/conflicting sources, ambiguity, and abstention across `ChatPanel` and `RegulatoryChat`.
* Deterministic tests prove multi-turn `approve`, `decide`, `consent`, `diagnose`, and `contact` requests preserve refusal and human workflow routes across `ChatPanel` and `RegulatoryChat`, and neither prior conversation turns nor user memory can manufacture approval or resident consent.
* Held-out scenario freeze validation rejects unfrozen per-turn expected outcomes (`expect={}`), missing `critical_errors`, non-independent `labelled_by`, tampered digests, development/prompt leaks, and stale `task`/`model`/`prompt_version`/`policy_version`/`source_version`/`memory_version` bindings before testing.
* Chat-specific failures and 4-component review effort (`reviewer minutes per reviewed answer`, `reviewer minutes per rejected or withheld answer`, `rework and escalation minutes`, `comparator minutes on the non-AI path (case card)`) are reported separately from single-turn task results in `core.ai_eval`, `agents.chat_eval`/`chat_heldout`, and `/api/ai/report` (`chat_evaluation` vs `evaluation`), while keeping live enablement `disabled` until owner threshold approval.

## Test Ownership and Evidence Matrix

| Target test file | Exact removals | Maximum additions | Canonical targets covered | Semantic vs regression role | Validation command |
|---|---|---|---|---|---|
| `src/core/tests/test_ai_eval.py` (new) | `none` | `<= 22` test methods | `src/core/src/zava_forward/core/ai_eval.py`, `chat_panel.py`, `regulatory_chat.py` | Semantic & boundary regression for Criteria 1, 2, 3 in `core` | `cd src/core && python3 -m unittest discover -s tests -p "test_*ai_eval*.py" -q` |
| `src/core/tests/test_regulatory_chat.py` | `none` | `<= 3` test methods | `src/core/src/zava_forward/core/regulatory_chat.py` | Semantic regression for mid-thread AI-consent revocation & fallback `out_of_scope` routes | `cd src/core && python3 -m unittest discover -s tests -p "test_regulatory_chat.py" -q` |
| `src/agents/tests/test_chat_heldout.py` | `none` | `<= 4` test methods | `src/agents/src/zava_forward/agents/chat_heldout.py`, `chat_eval.py`, `evals/chat_golden.json` | Semantic regression for frozen per-turn expected outcomes & separate held-out reporting | `cd src/agents && python3 -m unittest discover -s tests -p "test_chat_*.py" -q` |
| `src/api/tests/test_ai_tasks.py` | `none` | `<= 4` test methods | `src/api/src/zava_forward/api/server.py` (`/api/ai/report`), `ai_registry.py` | API contract regression for separate `chat_evaluation` vs single-turn `evaluation` and `disabled` state | `cd src/api && PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_ai_tasks.py" -q` |

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/issue-164-chat-eval-revocation-plan.md                                                                |
| Phase details                    | .copilot-tracking/details/2026-11-15/issue-164-chat-eval-revocation-phase-details.md                                                     |
| Latest critique                  | .copilot-tracking/reviews/2026-11-15/issue-164-chat-eval-revocation-plan-critique.md (`Revise` findings `PC-001`–`PC-004` all resolved directly by planner) |
| Relevant research                | .copilot-tracking/research/2026-11-15/issue-164-chat-eval-revocation-research.md                                                         |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/issue-164-chat-eval-revocation-changes.md is created by implementation as its evidence record       |
| Planning execution and readiness | Complete and implementation-ready                                                                                                        |
| Continuation context             | Confirmed automatic RPI Agent session continues to `rpi-implement` after `rpi-plan-critique` dispositions are recorded                   |

## Sources

* `.copilot-tracking/research/2026-11-15/issue-164-chat-eval-revocation-research.md`: Evidence IDs `C1`–`C17` establishing package boundaries, `RegulatoryChat` and `ChatPanel` mechanics, `chat_heldout` expected-outcome freeze gap, and `/api/ai/report` single-turn vs multi-turn separation.
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: FR-036, FR-037, AC-045, AC-054, AC-057, and v0.16.0 RAI evaluation contract.
* GitHub Issue `#164`: Acceptance criteria for grounding, multi-turn revocation, refusal workflow routes, held-out version freeze, separate chat reporting, and human-review boundaries.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core `RegulatoryChat` Hardening and `zava_forward.core.ai_eval` Contract

* Intent: Close core-level mid-thread AI-consent revocation and fallback out-of-scope routing gaps in `RegulatoryChat` and provide a pure-`core` deterministic multi-turn chat evaluation, held-out freeze, and separate reporting module in `zava_forward.core.ai_eval`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Harden `RegulatoryChat` mid-thread AI-consent revocation and fallback `out_of_scope` routing

* Requirement and evidence: Mid-thread revocation clearing and multi-turn refusal preservation (`C4`, `C6`, `C7`, `C16`, `C17`).
* Expected result: `RegulatoryChat` checks pre-`detail` `_question_refusal(question)` (`self.refuse(question)` first, falling back to `REFUSED + out_of_scope(question)[1]`), checks `consent_guidance(self.iso.ai_consent_state(cid))` only after `self.store.detail(cid, user)` confirms case visibility, re-verifies `ai_consent_state` inside `ask()`'s `repo.txn()` block, and raises `ChatForbidden` in `doubt()` when recorded AI consent is withdrawn/not `Given`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-164-chat-eval-revocation-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Create pure-`core` `src/core/src/zava_forward/core/ai_eval.py`

* Requirement and evidence: Core-owned multi-turn revocation/refusal harness, held-out expected-outcome + 6-binding freeze gate, and separate multi-turn vs single-turn reporting (`C1`–`C12`).
* Expected result: `zava_forward.core.ai_eval` imports only `zava_forward.core.*`, executes deterministic multi-turn `ChatPanel` and `RegulatoryChat` scenarios (unsupported claims on valid citations, stale/conflicting sources, ambiguity, abstention, mid-thread permission/source/card/consent revocation, multi-turn `approve`/`decide`/`consent`/`diagnose`/`contact` refusals, memory/turn non-manufacture of approval or consent), validates frozen held-out manifests including per-turn expected outcomes, and builds separate single-turn vs chat multi-turn reports with 4-part `review_effort` and `enablement["state"] == "disabled"`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/issue-164-chat-eval-revocation-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Agents Multi-Turn Golden Coverage and Held-Out Expected-Outcome Freeze

* Intent: Align `zava_forward.agents.chat_eval`, `evals/chat_golden.json`, and `zava_forward.agents.chat_heldout` with mid-thread source-field/AI-consent revocation, ambiguity abstention, and mandatory pre-test frozen expected outcomes.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Extend `agents.chat_eval`, `evals/chat_golden.json`, and `agents.chat_heldout`

* Requirement and evidence: Contrarian gaps in `Run._apply`, golden ambiguity/source-revocation scenarios, and vacuous `expect={}` turns in `chat_heldout` (`C9`, `C10`, `C11`, `C12`).
* Expected result: `Run._apply` supports `revoke_source` and `set_ai_consent`; `chat_golden.json` and `REVOCATION_SCENARIOS` include mid-thread source-field/AI-consent revocation and multi-turn ambiguity abstention; `chat_heldout.freeze_problems` rejects missing/unfrozen per-turn expected outcomes (`expect.kind` / `expect.error`) and mismatched optional `expected_outcomes_sha256`, and `run_heldout` surfaces `chat_specific`, `review_effort`, and `enablement` (`state="disabled"`).
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-164-chat-eval-revocation-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Separate Chat Multi-Turn Reporting in `/api/ai/report`

* Intent: Report multi-turn chat evaluation (`chat_evaluation`) separately from single-turn task evaluation (`evaluation`) at the manager AI evaluation endpoint while keeping live chat `disabled`.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add separate `chat_evaluation` sibling to `/api/ai/report` in `src/api/src/zava_forward/api/server.py`

* Requirement and evidence: Separate chat multi-turn vs single-turn reporting (`C13`, `C14`, `C15`).
* Expected result: `/api/ai/report` returns `evaluation` (single-turn task harness, unchanged) and a separate top-level `chat_evaluation` (multi-turn conversation harness with `chat_specific` failures, `review_effort` completeness, and `enablement.state == "disabled"`), never conflating their summary metrics.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/issue-164-chat-eval-revocation-phase-details.md

<!-- rpi:phase id=P04 -->
### [x] P04: Deterministic Regression Suites and Focused Validation

* Intent: Prove all three Issue #164 criteria with deterministic unit tests in `src/core`, `src/agents`, and `src/api` and pass focused `unittest`, `mypy`, and `ruff` checks.
* Dependencies: P01, P02, P03

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Create `src/core/tests/test_ai_eval.py` and extend `src/core/tests/test_regulatory_chat.py`

* Requirement and evidence: Caller-mandated `src/core/tests/test_ai_eval.py` discovery target and `RegulatoryChat` regression coverage (`C1`, `C2`, `C7`, `C16`).
* Expected result: `src/core/tests/test_ai_eval.py` and `src/core/tests/test_regulatory_chat.py` deterministically test Criteria 1, 2, and 3, including negative/failure-injection proofs and `DependencyRuleTests` compliance.
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-15/issue-164-chat-eval-revocation-phase-details.md

<!-- rpi:task id=P04-T02 -->
#### [x] P04-T02: Extend `src/agents/tests/test_chat_heldout.py` and `src/api/tests/test_ai_tasks.py` and run focused checks

* Requirement and evidence: Held-out expected-outcome freeze and API separate-reporting coverage plus focused tier checks (`C11`, `C13`, `C14`).
* Expected result: All focused unit suites in `src/core`, `src/agents`, and `src/api`, plus `mypy`, `ruff check .`, and `ruff format --check .`, exit `0`.
* Detail section: P04-T02 in .copilot-tracking/details/2026-11-15/issue-164-chat-eval-revocation-phase-details.md

## Dependencies

* `src/core/tests/test_dependency_rule.py`: Enforces `ALLOWED = {"core"}`; `P01` must keep `zava_forward.core.ai_eval` free of `agents`/`api` imports.
* `src/agents/tests/regulatory_gate_fixture.py`: Asserts exact `REASONS["legal"]` string from `agents.regulatory_chat.refusal`; `P01-T01` preserves caller-supplied `self.refuse` precedence.
* Editable package installations in environment: Existing Python environment runs `unittest`, `mypy`, and `ruff` directly across `src/core`, `src/agents`, and `src/api`.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` (High: `RegulatoryChat` pre-`detail` `ai_consent_state` leak, `self.refuse` precedence, and missing transactional re-check in `ask()`) | Resolved | Updated `P01-T01` to run `_question_refusal(question)` (`self.refuse` then `out_of_scope`) before `store.detail(cid, user)`, evaluate `ai_consent_state(cid)` only after `detail` succeeds, and re-verify `ai_consent_state` inside `ask()`'s `repo.txn()` as well as `doubt()`. |
| `PC-002` (High: `revoke_source` key deletion breaking `Store.detail()`, `WORKFLOW_RULES` citations in `_comparison`, and `test_chat_eval.py` golden invariants) | Resolved | Updated `P02-T01` so `revoke_source` clears optional source values to `""`/`None` without deleting required case keys, `_comparison` unions `WORKFLOW_RULES` with `permitted_sources`, and new golden scenarios stay in `permission`/`grounding` categories preserving `component_probes == 5` and `model_called: false` on `refused` turns. |
| `PC-003` (Medium: strict closed-set `expected_outcome_problems` checks and canonical 4-item `REVIEW_EFFORT_INPUTS` alignment) | Resolved | Updated Acceptance Criteria, `P01-T02`, and `P02-T01` to reject empty `turns`, non-dict `expect`, invalid `kind` outside `VALID_KINDS`, or blank/null `error`, and unified on the 4 canonical `REVIEW_EFFORT_INPUTS` strings. |
| `PC-004` (Medium: per-package `mypy`/`ruff` invocations and `strict = true` untyped call bindings without `pyproject.toml` edits) | Resolved | Updated `P01-T02` and `P04` to run `mypy` and `ruff` per package (`src/core`, `src/agents`, `src/api`) and bind untyped `core` collaborators as `Any` so `strict = true` passes with zero `pyproject.toml` modifications. |

## Follow-Up Items

* Owner-approved thresholds, named accountable reviewer appointment, independently labelled non-implementer held-out dataset execution, budget-authorized live serving-model evaluation, and competent-human review effectiveness exercises remain post-merge owner/governance gates under Issue #164 before `chat-case-conversation` can ever move from `disabled`.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-164-chat-eval-revocation-changes.md
* Ready phase or task: Complete (`P01`–`P04`); ready for `rpi-review`
* Remaining provisional question or blocker: None
