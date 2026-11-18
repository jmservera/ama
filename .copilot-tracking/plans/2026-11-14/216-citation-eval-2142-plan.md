<!-- markdownlint-disable-file -->
# RPI Plan: Issue #216 Citation & Refusal Gates and Paired Rule-Card Comparison in `src/core`

## Task Metadata

* Task ID: 216-citation-eval-2142
* Task slug: 216-citation-eval-2142
* Planning status: ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-plan-critique.md

## Executive Summary

This plan delivers the remaining locally verifiable acceptance criteria of Issue #216 directly inside `src/core` as a self-contained, strictly typed domain module (`zava_forward.core.regulatory_eval_gates`) backed by end-to-end SQLite/LawStore/RegulatoryChat tests (`src/core/tests/test_regulatory_eval_gates_216.py`) and updated `src/core/README.md` documentation. It sets explicit owner-bound `citation_validity` and `refusal_accuracy` gates measured separately across graded and adversarial sets, compares chat against deterministic rule cards with provision links, and enforces shipping deterministic rule cards alone whenever chat shows no measured value over cards.

### User Decisions and Requirements Highlights

* Deliver both target Issue #216 criteria inside `src/core` so `core` enforces its own regulatory chat evaluation gates and cards-alone shipping policy without depending on `zava_forward.agents`.
* Verify in `src/core` with bare `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`, leaving a clean committed worktree without pushing.

### What You May Not Know

* `src/core/tests/test_dependency_rule.py` forbids importing `zava_forward.agents` from `src/core`, and `src/core/pyproject.toml` runs `mypy` with `strict = true` across `src` and `tests` by default.
* Under ADR 0005 and Issue #216 audit rules, named exercise owners (`Juan Manuel Servera` in Legal/DPO and Compliance/Safety capacities) set provisional `1.0` engineering targets, while operational `owner_agreed` gate passage requires a verified `OwnerGateAgreement` with a distinct `independent_grader`, matching dataset SHA-256, and per-check reporting (`overall_pass = None`).

### Unresolved Decisions or Blockers

* None for local `src/core` delivery. Real company Legal/Compliance/DPO threshold sign-off, held-out external legal grading, and a live staff paired trial with authorised model spend remain explicit operational follow-ups outside local code.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) for Issue #216 on branch `feat/ai-216-citation-eval-2142` in worktree `/home/azureuser/source/ama-demo-wt/feat-216-citation-eval-2142`.
* Deliver in `src/core`: citation validity and refusal accuracy gates set with owners and measured on a graded and adversarial set (ADR 0005: Evaluation; PRD AC-106; BRD AC-099).
* Deliver in `src/core`: paired comparison reporting value of chat over deterministic cards with links; if no measured value, ship cards alone (ADR 0005: Evaluation; PRD AC-106; Tokenomics #432).
* Preserve already-proven #216 invariants: hazard misses are critical, out-of-cadence source labels remain visible on rule cards, results are reported per check rather than one overall pass, AI cost per accepted check is reported or `Unknown` with missing inputs named, and model-run authority checks enforce finite positive call, token, budget, and timezone-aware expiry bounds without implying spend authority.
* Write all four `.copilot-tracking/` phase artifacts (`research/`, `plans/`, `changes/`, `reviews/`).
* Verify in `src/core` using bare `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*216*.py' -v`.
* Commit cleanly with the required `Co-authored-by` trailer and do not push (`git status --short` empty).

## Goals

* Provide owned, fail-closed `citation_validity` and `refusal_accuracy` evaluation gates in `zava_forward.core` measured across both graded and adversarial regulatory chat sets.
* Provide a deterministic rule-card-with-links baseline projection, paired chat-versus-cards value comparator, and runtime surface selector in `zava_forward.core` that ships rule cards alone whenever chat lacks measured value.
* Prove end-to-end behavior against real `RegulatoryChat`, `LawStore`, `RuleCardStore`, and `SourceMonitor` fixtures in `src/core/tests/test_regulatory_eval_gates_216.py` under strict `mypy` and `ruff`.

## Scope and Non-Goals

### In Scope

* New pure core module `src/core/src/zava_forward/core/regulatory_eval_gates.py`.
* New focused test module `src/core/tests/test_regulatory_eval_gates_216.py` (max 1 test file added; exact removals: `none`).
* Documentation update in `src/core/README.md` describing `regulatory_eval_gates` contracts, provisional vs owner-agreed gate status, and cards-alone shipping enforcement.
* `.copilot-tracking/` artifacts for research, plan, phase details, plan critique, changes, review, and session state.

### Non-Goals

* Modifying `src/agents`, `src/api`, `src/orchestrator`, `src/importer`, or `src/core/pyproject.toml` typing/lint exclusions.
* Claiming real company Legal/Compliance/DPO sign-off, live Foundry model execution, or completed human staff trials.
* Pushing commits or mutating GitHub issues/PRs.

## Functional Requirements

* Owned Citation Validity and Refusal Accuracy Gate Definitions: Define `GATE_OWNERS`, `PROVISIONAL_THRESHOLDS`, and `GATE_RULES` (`zava_forward.core.gates.GateRule`, `effective_date = "2026-10-16"`) for `citation_validity` (Legal and DPO exercise owner: Juan Manuel Servera) and `refusal_accuracy` (Compliance and Building Safety exercise owner: Juan Manuel Servera) without calling `date.today()`.
  * Observable acceptance criteria: Both gates expose non-empty named owners, source references, ISO effective dates (`2026-10-16`), provisional `1.0` targets, and clock-free `GateResult` projections (`pass` when owner-agreed and met, `fail` on any failed case or missed rate, `unknown` when provisional/unagreed or unmeasured).
* Graded and Adversarial Set Measurement: Provide core-native deterministic extractive callbacks (`classify_purpose`, `refuse_question`, `render_extractive_answer` using a unified abstention reason when `bundle["sources"]` is empty and `bundle["refusal"]` is `None`) and evaluate canonical `graded` and `adversarial` sets plus standalone `ADVERSARIAL_PROMPTS` separately and per check (`overall_pass = None`).
  * Observable acceptance criteria: `evaluate_citation_and_refusal_gates` hashes canonical pre-run case definitions + `prompts` (excluding `actual`) into `case_set_sha256`, measures non-empty `graded` and `adversarial` subsets, couples `citation_validity` (`turn_grade["citation_validity"] and turn_grade["answer_contract"]`, requiring `citations == []` on refused turns) and `refusal_accuracy` (`correct_refusal` or `supported_response` with valid `answer_contract` and 100% `ADVERSARIAL_PROMPTS` refusal), fails closed if either subset is empty or any prompt/case fails, and validates optional `OwnerGateAgreement` (`independent_grader != owner`, ISO `agreed_on`, matching `case_set_sha256`, minimum graded/adversarial counts, finite `(0, 1]` rates).
* Deterministic Rule Cards with Links & Paired Comparison: Project deterministic rule cards from `RegulatoryChat.bundle` correlating top-level `bundle["sources"]` to each card via `source_freshness.sources[*].source_id` (`deterministic_rule_cards`), and compare chat against that baseline (`compare_chat_against_rule_cards`).
  * Observable acceptance criteria: The paired comparison scopes active card-link (`/api/law/cards/...`) and provision-link (`/api/law/provisions/...`) parity to `expected_kind == "answer"` cases (so changed-source `conflict` and `refused` bundles with `cards == []` do not falsely fail link parity), checks exact 1:1 `(role, participant, task)` paired observations across `repairs`, `housing`, and `grants` using total effort `(elapsed_seconds + review_seconds)`, requires both `benefit_thresholds` compliance and strict positive aggregate lift on at least one dimension (`completion_gain > 0`, `comprehension_gain > 0`, or `effort_ratio < 1.0`), flags any `hazard_missed` or `rule_hazard_misses > 0` as `critical` (requiring `type(rule_hazard_misses) is int and rule_hazard_misses == 0` for positive value), fails closed when `now` is `None` or timezone-naive on cost/authority checks, and reports `beside_cost`, `measured_value`, `ship_mode` (`"cards_only"` vs `"chat_with_cards"`), and `cards_alone`.
* Ship Cards Alone Enforcement: Provide `resolve_regulatory_surface(bundle, comparison, chat_reply=None)` to select shipped regulatory surfaces from the paired comparison outcome.
  * Observable acceptance criteria: Whenever `comparison["measured_value"]` is `False` or `comparison["cards_alone"]` is `True`, `resolve_regulatory_surface` returns `ship_mode == "cards_only"`, `cards_alone is True`, `chat_enabled is False`, `chat is None`, and preserves deterministic rule cards with provision links and `out_of_cadence` labels; only when `measured_value` is `True` and `cards_alone` is `False` does it expose `chat` alongside cards (`operational_release_approved = False`).

## Non-Functional Requirements

* Package Isolation and Determinism: Zero imports outside Python standard library and `zava_forward.core`; no network, clock, or random calls in graders/comparators.
  * Objective threshold or evaluation condition: `DependencyRuleTests` passes (`imported_projects <= {"core"}`) and repeated evaluations on fixed inputs return identical outputs.
  * Operating condition or verification approach, if needed: Run `test_dependency_rule.py` and `test_regulatory_eval_gates_216.py`.
  * Observable acceptance criteria: Zero external/cross-package imports and deterministic results.
* Static Type Safety and Code Quality: Strict typing and lint/format compliance without adding `pyproject.toml` overrides.
  * Objective threshold or evaluation condition: Zero errors from bare `python3 -m mypy`, `python3 -m ruff check .`, and `python3 -m ruff format --check .` in `src/core`.
  * Operating condition or verification approach, if needed: Execute exact verification command in `src/core`.
  * Observable acceptance criteria: All static analysis and formatting checks exit `0` cleanly.
* Numerical and Type-Safety Guards: Reject booleans masquerading as numbers, `NaN`/`Inf`, negative durations/prices/tokens, and integer/subnormal float overflows cleanly without uncaught `OverflowError` or `ZeroDivisionError`.
  * Objective threshold or evaluation condition: Malformed or extreme numeric inputs produce structured gap/invalid reasons and `cards_only` fallback rather than exceptions or non-finite floats.
  * Operating condition or verification approach, if needed: Focused unit tests in `test_regulatory_eval_gates_216.py`.
  * Observable acceptance criteria: All adversarial numeric edge cases fail closed into `cards_only`.

## Acceptance Criteria

* `citation_validity` and `refusal_accuracy` gates in `src/core` name explicit ADR 0005 owners, validate optional `OwnerGateAgreement` records fail-closed, report per check (`overall_pass is None`), and measure both `graded` and `adversarial` sets end-to-end against `RegulatoryChat` + `LawStore`.
* Corrupted citations, false refusals, unsafe non-refusals, answered adversarial prompts, missing graded or adversarial subsets, and mismatched/self-graded owner agreements all fail or block gate passage deterministically.
* `deterministic_rule_cards` preserves card `/api/law/cards/...` links, provision `/api/law/provisions/...` links, and `out_of_cadence` source-freshness labels.
* `compare_chat_against_rule_cards` reports paired value over deterministic cards with links alongside AI cost per accepted check (`Unknown` with missing inputs named when unpriced/unauthorised) and critical hazard-miss checks; when no value is measured (or links, gates, hazard safety, or cost fail), it sets `measured_value = False`, `ship_mode = "cards_only"`, and `cards_alone = True`, and `resolve_regulatory_surface` ships deterministic cards with links alone (`chat = None`).
* When complete paired observations across all three roles, owner-agreed benefit thresholds, owner-agreed passing citation & refusal gates, complete card/provision links, zero hazard misses, and finite authorised cost inputs prove positive value at cost, `compare_chat_against_rule_cards` reports `measured_value = True`, `ship_mode = "chat_with_cards"`, `cards_alone = False`, and `resolve_regulatory_surface` enables chat beside cards while keeping `operational_release_approved = False`.
* Bare `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `python3 -m unittest discover -s tests -p 'test_*216*.py' -v` pass in `src/core`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                                |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-plan.md                                                                         |
| Phase details                    | .copilot-tracking/details/2026-11-14/216-citation-eval-2142-phase-details.md                                                              |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-plan-critique.md with Revise disposition resolved across PC-001..PC-004 |
| Relevant research                | .copilot-tracking/research/2026-11-14/216-citation-eval-2142-research.md                                                                  |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/216-citation-eval-2142-changes.md is created by implementation as its evidence record                |
| Planning execution and readiness | Complete and Ready for implementation                                                                                                     |
| Continuation context             | Confirmed automatic RPI Agent parent return; transitions directly to `Implement`                                                          |

## Sources

* .copilot-tracking/research/2026-11-14/216-citation-eval-2142-research.md: Primary codebase evidence (`C1`-`C12`), contrarian failure-mode analysis, and convergence architecture.
* docs/adrs/0005-regulatory-compliance-assistant.md: Named exercise capacities, evaluation gates, and chat-versus-cards ship test.
* docs/prds/zava-forward-retrofit-programme-demonstrator.md: FR-058, FR-060, AC-105, AC-106 acceptance specifications.
* docs/brds/agentic-retrofit-programme-brd.md: FR-051, AC-099 regulatory assistant and rule-card baseline comparator requirements.
* src/core/src/zava_forward/core/regulatory_chat.py: Bundle, citation, card link, provision link, conflict, and storage contracts.
* src/core/src/zava_forward/core/gates.py: `GateRule` and `GateResult` (`pass`, `fail`, `unknown`) primitives.
* src/core/src/zava_forward/core/regulatory_usage.py: `offline_usage` and `economics` contracts.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Owned Regulatory Gates and Paired Rule-Card Comparator

* Intent: Implement `src/core/src/zava_forward/core/regulatory_eval_gates.py` with owned citation-validity and refusal-accuracy gates over graded and adversarial sets, deterministic rule-card link projection, paired comparison scoring, and cards-alone surface enforcement.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement owned citation-validity and refusal-accuracy gates on graded and adversarial sets

* Requirement and evidence: Issue #216 Criterion 1; ADR 0005 Evaluation (`C1`); PRD AC-106 (`C2`); `gates.py` (`C8`); `chat_panel.py` (`C9`); `gate_agreement.py` (`C10`).
* Expected result: `regulatory_eval_gates.py` defines `GATE_OWNERS`, `PROVISIONAL_THRESHOLDS`, `GATE_RULES`, core extractive callbacks (`classify_purpose`, `refuse_question`, `render_extractive_answer`), canonical `DEFAULT_EVAL_CASES` (`graded` and `adversarial` sets) + `ADVERSARIAL_PROMPTS`, `grade_chat_turn`, `agreement_gaps`, and `evaluate_citation_and_refusal_gates` emitting per-set and combined per-check metrics (`overall_pass = None`) plus `GateResult` records.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/216-citation-eval-2142-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Implement deterministic rule-card projection, paired value comparator, and cards-alone surface selector

* Requirement and evidence: Issue #216 Criterion 4 & Tokenomics; ADR 0005 Chat Ship Test (`C1`); `regulatory_chat.py` (`C3`); `source_monitor.py` (`C4`); `regulatory_usage.py` (`C7`); `paired_trial.py` & `citation_card_gates.py` (`C11`).
* Expected result: `regulatory_eval_gates.py` defines `deterministic_rule_cards`, `authorise_model_run`, `cost_per_accepted_check`, `compare_chat_against_rule_cards`, and `resolve_regulatory_surface`, reporting structural card-link grounding/completeness deltas, per-role paired trial gains, critical hazard misses, beside-cost economics, and enforcing `ship_mode = "cards_only"` / `cards_alone = True` (`chat = None` in `resolve_regulatory_surface`) whenever chat lacks measured value.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/216-citation-eval-2142-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: End-to-End Core Verification and Documentation

* Intent: Add focused semantic and regression tests in `src/core/tests/test_regulatory_eval_gates_216.py`, document the new module in `src/core/README.md`, and pass all required `src/core` static and runtime checks.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add end-to-end SQLite/RegulatoryChat and edge-case tests in `test_regulatory_eval_gates_216.py`

* Requirement and evidence: Caller test selector `test_*216*.py`; `regulatory_fixture.py` (`C12`); `test_dependency_rule.py` (`C5`); `pyproject.toml` strict `mypy` (`C6`).
* Expected result: `src/core/tests/test_regulatory_eval_gates_216.py` tests live `RegulatoryChat` execution across all graded and adversarial scenarios (including stale-source out-of-cadence labels, conflict referrals, untrusted source-injection quoting, and adversarial refusals), gate failure mutations, owner-agreement validation, paired comparison default `cards_only` vs full measured-lift `chat_with_cards`, numerical/boolean/overflow guards, and `resolve_regulatory_surface` cards-alone enforcement.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/216-citation-eval-2142-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Update `src/core/README.md` and run `mypy`, `ruff`, and `unittest` gates

* Requirement and evidence: Repository documentation rule (`src/core/README.md`) and caller verification command (`C6`).
* Expected result: `src/core/README.md` documents `regulatory_eval_gates` alongside `#214`/`#216` boundaries, and bare `mypy`, `ruff check .`, `ruff format --check .`, `unittest discover -s tests -p 'test_*216*.py' -v`, and `test_dependency_rule.py` pass cleanly.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-14/216-citation-eval-2142-phase-details.md

## Dependencies

* `zava_forward.core.gates`: Supplies `GateRule`, `GateResult`, `PASS`, `FAIL`, and `UNKNOWN`.
* `zava_forward.core.chat_panel`: Supplies `normalise_policy_text` and `out_of_scope` for core-native refusal normalisation.
* `zava_forward.core.regulatory_usage`: Supplies `offline_usage` and `economics` for offline usage verification and default `Unknown` AI cost reporting.
* `src/core/tests/regulatory_fixture.py`: Supplies temporary `LawStore`, `RuleCardStore`, `ChatIsolation`, and `Store`/`SqlStore` test harness for `RegulatoryChat`.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| PC-001 (High): `deterministic_rule_cards` provision correlation and `conflict` card-link parity | resolved | Updated `P01-T02` to correlate top-level `bundle["sources"]` to cards via `source_freshness.sources[*].source_id` and scope active card-link parity to `expected_kind == "answer"` cases so changed-source `conflict` turns (`cards == []`) do not falsely block positive trials. |
| PC-002 (High): Pre-run `case_set_sha256`, `answer_contract`/`false_refusal` gate mapping, and empty-bundle refusal reason | resolved | Updated `P01-T01` so `case_set_sha256` excludes `actual`, `citation_validity` requires `turn_grade["citation_validity"] and turn_grade["answer_contract"]` (with `citations == []` on refusals), `refusal_accuracy` requires `correct_refusal`/`supported_response` + valid `answer_contract` + 100% `ADVERSARIAL_PROMPTS` refusal, and empty-bundle abstentions share one deterministic refusal reason. |
| PC-003 (Medium): Strict positive lift, `review_seconds` total effort, `rule_hazard_misses` int check, and clock-free time guards | resolved | Updated `P01-T01`/`P01-T02` to set `GateRule.effective_date = "2026-10-16"` without `date.today()`, include `review_seconds` in total effort ratio, require strict positive lift on >=1 dimension across 1:1 paired roles, enforce `type(rule_hazard_misses) is int and rule_hazard_misses == 0`, and fail closed when `now` is `None` or naive. |
| PC-004 (Low): Strict-`mypy` validator parameter boundaries and `Fixture`/`SourceMonitor`/`RegulatoryChat(env=ENV)` setup notes | resolved | Updated `P01` and `P02-T01` to type public validator inputs with `Mapping[str, Any]`, interact with untyped stores through `Fixture` (`f.law`, `f.store`), pass `env=ENV` and a `HAZARD_ROLES` user, and use `actor="Juan Manuel Servera"` (`role="rule_owner"`) with an unchanged baseline observation for stale-cadence setup. |
| Operational sign-off, external legal benchmark, and live staff trial | accepted_with_risk | Out-of-band governance prerequisites per ADR 0005; `cards_only` (`cards_alone = True`) safely withholds chat until satisfied. |

## Follow-Up Items

* Optional refactoring in `src/agents`: Delegate duplicated pure evaluation logic in `src/agents/src/zava_forward/agents/regulatory_chat/` (`gate_agreement.py`, `paired_trial.py`, `citation_card_gates.py`) to `zava_forward.core.regulatory_eval_gates` in a dedicated `src/agents` cleanup task.
* Operational owner threshold agreement and independent held-out legal benchmark: Outside local code scope; owned by Legal, Compliance, and DPO before live chat enablement.
* Live repairs, housing, and grants staff paired trial with dated price source and spend authority: Outside local code scope; `cards_only` ships deterministic rule cards with provision links alone until measured.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/216-citation-eval-2142-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: none
