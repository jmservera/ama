<!-- markdownlint-disable-file -->
# RPI Plan: Issue #133 Criterion 5 — No Causation, Blame, or Savings Promise in Aftercare Text

## Task Metadata

* Task ID: rpi-133-no-causation-blame-savings-20261115T0316Z
* Task slug: 133-no-causation-blame-savings
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/133-no-causation-blame-savings-plan-critique.md

## Executive Summary

This plan closes every remaining text-generation, template, draft, persistence, and snapshot-restore gap for Issue #133 Criterion 5 (`No causation, blame or savings promise appears in any generated or templated text`). It hardens `zava_forward.core.aftercare.neutral_text` against Unicode/whitespace obfuscation and multi-clause uncertainty whitewashing, expands deterministic detection of resident lifestyle attribution, measure-causation proof claims, blame language, and financial/energy savings promises, and enforces `neutral_text` across all `AftercareRegister`, `AftercareService`, and `quality.py:add_aftercare` boundaries while preserving verbatim household statements.

### User Decisions and Requirements Highlights

* Target Issue #133 Criterion 5 (`No causation, blame or savings promise appears in any generated or templated text`) on branch `feat/ai-133-no-causation-blame-savings` (stacked on `feat/demo-164-chat-grounding-provenance-0900` / PR #1641).
* Enforce deterministic boundary validation across concern acknowledgements, receipts, investigation summaries, remedy templates/notes, evaluator view summaries, and optional `FR-036` AI concern-pack proposal drafts/summaries so prohibited causation, blame, or savings-promise phrasing cannot be persisted, registered as a proposal, restored, or rendered.
* Validate with `ruff check`, `ruff format --check`, `mypy`, and the full `test_aftercare*` suites in `src/core` and `src/api`, then commit code and `.copilot-tracking/` artifacts in one clean local commit without pushing.

### What You May Not Know

* `neutral_text` in `src/core/src/zava_forward/core/aftercare.py` already uses span-bounded `_UNCERTAIN.sub(" ", ...)` on indirect `whether|if` clauses, but lacked newline-preserving boundary stops, conjunction/dash lookaheads (`however`, `therefore`, `yet`, `so`, `while`, `though`), and NFKC/invisible-character folding, allowing newline-wrapped or conjunction-spliced claims to slip past.
* `src/api/pyproject.toml` places both `src/api/tests` and `../core/tests` on `mypy_path` (and `src/api` unittest runs with `PYTHONPATH=../core/tests:../agents/tests`), so `AftercareService` intake tests live in `src/core/tests/test_aftercare_intake.py` while HTTP served API tests live in `src/api/tests/test_aftercare_served.py` (preventing duplicate-module collisions while keeping both `test_aftercare*` suites comprehensive).
* Verbatim resident `statement` and `representative_basis` inputs intentionally remain uncensored so a household report quoting what an installer promised or describing perceived damp causes is never refused at intake.

### Unresolved Decisions or Blockers

* None. All in-scope technical decisions are settled from repository evidence.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the complete RPI loop in order (`rpi-research`, `rpi-plan` with `rpi-plan-critique`, `rpi-implement`, `rpi-review`) with dated `2026-11-15` artifacts under `.copilot-tracking/` (`research/`, `plans/`, `details/`, `reviews/plans/`, `changes/`, `reviews/logs/`, `rpi-sessions/`) for Issue #133 Criterion 5.
* Ensure deterministic, enforce-at-boundary validation across all generated/templated aftercare text (concern acknowledgements, receipts, investigation summaries, remedy templates, evaluator view summaries, and optional `FR-036` AI concern-pack proposal drafts/summaries).
* Guarantee no causation claim (e.g., attributing damp/mould/performance to resident lifestyle or proving measure causation), blame language, or financial/energy savings promise can appear in templated or generated aftercare text.
* Deterministically flag/reject prohibited generated or caller-supplied template/draft text before persistence, proposal registration, or UI/API rendering while keeping resident reports undismissed and verbatim (`docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `FR-036`, `FR-049`, `AC-063`).
* Keep optional `FR-036` AI concern-pack task `aftercare-concern-pack` registered as an unapproved, disabled proposal requiring named-owner review and never replacing human investigation (`src/core/src/zava_forward/core/ai_registry.py`).
* Add focused unit, service, and HTTP API tests across `test_aftercare*` in `src/core` and `src/api`, pass `ruff check`, `ruff format --check`, and `mypy`, and commit locally with the Copilot trailer without pushing.

## Goals

* Eliminate normalization, multi-clause uncertainty, and lexical bypasses in `zava_forward.core.aftercare.neutral_text`.
* Enforce `neutral_text` fail-closed at every write, proposal-registration,proposal-review, snapshot-restore, and template-render boundary in `AftercareRegister`, `AftercareService`, and `quality.py:add_aftercare`.
* Prove zero causation, blame, or savings-promise leakage and zero false-positive refusal of neutral observational copy or verbatim resident statements across core and API test suites.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/aftercare.py`: `neutral_text`, `neutral_violations`, `BANNED_PHRASES`, `PARAPHRASE_PATTERNS`, `_NEGATED_CLAIM`, `_UNCERTAIN`, `intake_form`, `intake_errors`, `_context`, `AftercareRegister` write/read/proposal/restore methods.
* `src/core/src/zava_forward/core/aftercare_intake.py`: `AftercareService` write validation (`record_outcome`, `set_remedy`, `add_sensor_context`, `propose_pack`, `review_pack`), plain-language no-echo `ValidationError` reporting, receipt/view/evaluator template self-guards, and `_validate` restore checks.
* `src/core/src/zava_forward/core/quality.py`: `add_aftercare` handover aftercare note boundary enforcement (`controls.is_memory_reference` and `aftercare.neutral_text`).
* `src/core/README.md`: Concise documentation update for expanded #133 neutral-text boundary coverage.
* `src/core/tests/test_aftercare.py`, `src/core/tests/test_aftercare_intake.py`, and `src/api/tests/test_aftercare_served.py`: Focused unit, intake-service, and HTTP API regression tests.

### Non-Goals

* Operational/human sign-off on Criterion 1 non-digital intake channels or external DPO sign-off on outcome data.
* Binding a live LLM route or opening a new HTTP endpoint for `aftercare-concern-pack` (which remains `disabled` and `unapproved` in `ai_registry.py` per `FR-036` and `test_role_endpoint_inventory.py`).
* Modifying `pyproject.toml`, workflows, Dockerfiles, or SQL schema.

## Functional Requirements

* `FR-1`: `neutral_text` normalizes Unicode compatibility characters (`NFKC`), removes invisible/zero-width/soft-hyphen characters, normalizes curly quotes/apostrophes, converts newlines (`[\r\n]+`) to clause delimiters (`"; "`), and collapses horizontal whitespace runs before evaluating prohibited phrases and patterns, returning the original string unchanged when valid.
  * Observable acceptance criteria: Obfuscated inputs (`"will\u200bsave"`, `"caused\n\nby"`, `"resident\u2019s fault"`, fullwidth `"ｗｉｌｌ ｓａｖｅ"`) raise `ValueError` deterministically.
* `FR-2`: `neutral_text` keeps `BANNED_PHRASES` unconditional while retaining span-bounded `_UNCERTAIN.sub(" ", ...)` (strictly anchored to indirect `whether|if` clauses) and `_NEGATED_CLAIM.sub(" ", ...)` with tight clause-boundary stop-lookaheads (`[.!?;:,\n\u2014\u2013]`, ` - `, `--`, and coordinating/subordinating conjunctions such as `and`, `but`, `or`, `however`, `therefore`, `yet`, `so`, `while`, `though`) ahead of `PARAPHRASE_PATTERNS`.
  * Observable acceptance criteria: Mixed-clause inputs pairing an uncertain clause with a prohibited claim across newlines, commas, or conjunctions (e.g., `"Unknown whether night flow dropped; however, damp is due to drying clothes indoors."`) raise `ValueError`, whereas committed single-clause `whether|if` uncertainty assertions (`test_aftercare.py:256-258`) and negated disclaimers (`EVALUATOR_NOTICE`) succeed.
* `FR-3`: `neutral_text` rejects resident lifestyle causation/blame, measure-causation proof claims, and financial/energy savings promises across literal and paraphrased forms.
  * Observable acceptance criteria: Lifestyle blame (`drying laundry indoors`, `not opening windows`, `heating habits`, `occupant lifestyle`, `improper use`, `user error`, `negligence`, `fault of the resident`), measure-causation proof (`proven to cause`, `proves the`, `attributable to`, `caused the damp/mould/cold/higher`, `is why your`), and savings promises (`save £150`, `save 20%`, `saves money`, `payback`, `pays for itself`, `cut/reduce/slash bills`, `energy/bill/cost/financial savings`, `cheaper to run`) all raise `ValueError`.
* `FR-4`: `AftercareRegister` enforces `neutral_text` across all templated outputs (`intake_form`, `intake_errors`, `view`, `evaluator_view` including `unknowns`, `propose_pack`), staff/caller write fields (`raise_concern` `owner`, optional `staff_recorded` `recorded_by`, and `sensor_context` keys/values; `add_sensor_context` keys/values; `record_outcome` `evidence`; `set_remedy` required `evidence` for `completed`/`not_needed` and optional `evidence` for `open`/`in_progress`; `record_closure` `home_ref` and `owner`; `propose_pack` `ai_summary`; `review_pack` `reviewer` and `reason`), and `from_state` snapshot restoration (concerns, closures, and packs including `reviewer_function`), while leaving household `statement` and `representative_basis` verbatim.
  * Observable acceptance criteria: Prohibited text in any guarded `AftercareRegister` write, pack draft/review, or restored state raises `ValueError` with zero register mutation; verbatim household statements continue to record cleanly.
* `FR-5`: `AftercareService` and `quality.py:add_aftercare` enforce `neutral_text` at service, HTTP route, template-render, and state-restore boundaries, raising structured plain-language `ValidationError` (HTTP `400`, zero input echo, `neutral_text`-clean error wording, no banned internal copy vocabulary) on prohibited `/outcome`, `/remedy`, `/sensor-context`, and `VIEW_ROLES` / `owner_label(actor["role"])`-gated pack `propose_pack` / `review_pack` calls, and raising non-echoing HTTP `400` `ValueError` inside `_quality_operation` (preserving `403` precedence for unauthorized actors) on `/api/cases/{cid}/quality-aftercare`.
  * Observable acceptance criteria: Prohibited submissions return HTTP `400` without echoing caller text or mutating persisted state bytes, unauthorized calls still return `403`, and tampered receipts or register snapshots fail closed on read/write.

## Non-Functional Requirements

* `NFR-1`: Determinism and zero external/model dependency.
  * Objective threshold or evaluation condition: 100% pure standard-library evaluation (`re`, `unicodedata`) with zero network, randomness, or model calls.
  * Operating condition or verification approach, if needed: Offline unit and served HTTP tests in `src/core` and `src/api`.
  * Observable acceptance criteria: Identical inputs always produce identical pass/refusal outcomes in `<1 ms` per check.
* `NFR-2`: Strict static typing, lint cleanliness, and plain-language copy compliance.
  * Objective threshold or evaluation condition: Zero errors under `ruff check`, `ruff format --check`, strict `mypy`, `test_content_standard.py`, `test_role_endpoint_inventory.py`, and `test_epic104_bounded_ai_invariants.py`.
  * Operating condition or verification approach, if needed: Local CLI validation across `src/core`, `src/api`, and `src/agents`.
  * Observable acceptance criteria: All linter, formatter, type-checker, and regression test commands exit `0`.

## Acceptance Criteria

* Every templated and generated string emitted by `AftercareRegister`, `AftercareService`, and `aftercare.js` passes hardened `neutral_text` with zero causation claims, blame language, or financial/energy savings promises.
* Prohibited causation, lifestyle-blame, and savings-promise phrasings (including Unicode/whitespace obfuscation and multi-clause uncertainty bypass attempts) are deterministically rejected before persistence, proposal registration, proposal review, snapshot restore, or HTTP response rendering across `AftercareRegister`, `AftercareService`, and `quality.py:add_aftercare`.
* Resident own-words `statement` and `representative_basis` remain verbatim at intake while generated receipts, concern views, evaluator summaries, and `FR-036` concern-pack templates stay strictly neutral.
* `test_aftercare*` suites in `src/core` and `src/api`, cross-cutting invariant tests, `ruff check`, `ruff format --check`, and `mypy` all pass with exit code `0`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/133-no-causation-blame-savings-plan.md                                                                |
| Phase details                    | .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md                                                     |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/133-no-causation-blame-savings-plan-critique.md with Revise verdict; all five findings (`PC-001`..`PC-005`) applied directly |
| Relevant research                | .copilot-tracking/research/2026-11-15/133-no-causation-blame-savings-research.md                                                         |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/133-no-causation-blame-savings-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for `rpi-implement`                                                                                                    |
| Continuation context             | Confirmed automatic RPI Agent parent continues directly to `Implement`                                                                    |

## Sources

* `.copilot-tracking/research/2026-11-15/133-no-causation-blame-savings-research.md`: Primary three-wave research synthesis (`C1`..`C25`, `CF1`..`CF4`).
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: `FR-036`, `FR-049`, and `AC-063` requirements for neutral aftercare text and bounded concern-pack proposals.
* `src/core/src/zava_forward/core/aftercare.py` and `src/core/src/zava_forward/core/aftercare_intake.py`: Core register, `neutral_text`, and staff-assisted intake service.
* `src/core/src/zava_forward/core/quality.py` and `src/api/src/zava_forward/api/server.py`: Handover quality aftercare route and `/api/aftercare/*` HTTP wiring.
* `src/api/tests/test_content_standard.py`, `src/api/tests/test_role_endpoint_inventory.py`, and `src/agents/tests/test_epic104_bounded_ai_invariants.py`: Plain-language copy, endpoint inventory, and bounded-AI constraints.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Harden Core `neutral_text` Guard and `AftercareRegister` Boundaries

* Intent: Eliminate normalization, multi-clause uncertainty, lexical, write-field, template, and snapshot-restore bypasses in `zava_forward.core.aftercare`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Normalize text, scope clause uncertainty, and expand prohibited phrasing detection in `aftercare.py`

* Requirement and evidence: `FR-1`, `FR-2`, `FR-3`; research findings `C1`, `C22`, `CF1`, `CF2`.
* Expected result: `neutral_text` and `neutral_violations` deterministically catch Unicode/whitespace obfuscation, multi-clause uncertainty whitewashing, lifestyle blame, measure-causation proof claims, and financial/energy savings promises while accepting genuine single-clause uncertainty and negated disclaimers.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Enforce `neutral_text` across all `AftercareRegister` write, template, proposal, and `from_state` boundaries

* Requirement and evidence: `FR-4`; research findings `C12`..`C15`, `C18`, `C20`, `CF3`.
* Expected result: Every templated string, `owner`/`recorded_by`, sensor-context key/value, outcome `evidence`, remedy `evidence`, concern-pack draft/review field, and `from_state` restored record passes `neutral_text` while resident `statement` and `representative_basis` remain verbatim.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Enforce Neutral-Text Boundaries in `AftercareService` and Handover Quality Notes

* Intent: Enforce plain-language fail-closed boundary validation, template self-guards, and restore checks across `AftercareService`, `quality.py:add_aftercare`, and core documentation.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Guard `AftercareService` write, pack-proposal, template-render, and `_validate` restore paths in `aftercare_intake.py`

* Requirement and evidence: `FR-5`, `NFR-2`; research findings `C16`, `C17`, `C19`, `C21`, `CF4`.
* Expected result: `record_outcome`, `set_remedy`, `add_sensor_context`, and bounded owner-gated `propose_pack` / `review_pack` raise plain-language no-echo `ValidationError` on prohibited phrasing; all templated strings and restored receipts pass `neutral_text`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Guard `quality.py:add_aftercare` and update `src/core/README.md`

* Requirement and evidence: `FR-5`; research findings `C6`, `C9`.
* Expected result: `Store.add_aftercare` rejects memory references and non-neutral causation/blame/savings notes before mutating case state or audit entries, and `src/core/README.md` documents the expanded #133 neutral-text boundary guarantees.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Expand Core & API Test Coverage and Run Validation

* Intent: Add focused regression tests across `src/core` and `src/api` and verify zero lint, formatting, typing, or test regressions.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add unit, intake-service, and HTTP-served neutral-text boundary tests

* Requirement and evidence: `FR-1`..`FR-5`; research findings `C10`, `C23`, `C25`.
* Expected result: `src/core/tests/test_aftercare.py`, `src/core/tests/test_aftercare_intake.py`, and `src/api/tests/test_aftercare_served.py` cover obfuscation, multi-clause uncertainty, lifestyle/causation/blame/savings corpora, verbatim resident preservation, pack proposal/review boundaries, restore refusal, and HTTP 400 non-mutation.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Run `ruff`, `mypy`, `test_aftercare*` in `src/core` and `src/api`, and cross-cutting invariant suites

* Requirement and evidence: `NFR-1`, `NFR-2`; repository focused-tier validation rules.
* Expected result: `ruff check`, `ruff format --check`, strict `mypy`, all `test_aftercare*` suites in `src/core` and `src/api`, `test_quality_procurement`, `test_content_standard`, `test_role_endpoint_inventory`, and `test_epic104_bounded_ai_invariants` exit `0`.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/133-no-causation-blame-savings-phase-details.md

## Dependencies

* `src/core` and `src/api` editable Python distributions and installed `ruff` (`0.17.3`) / `mypy` (`2.4.1`) tools: required to execute targeted linters, strict type checks, and unittest suites.
* Existing cross-cutting guards (`test_content_standard.py`, `test_role_endpoint_inventory.py`, `test_epic104_bounded_ai_invariants.py`): constrain error copy vocabulary, server route registration, and `CONCERN_PACK_TASK` disabled status.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [High]: Pattern split & newline/conjunction boundary stops | Resolved | Retained span-bounded `_UNCERTAIN.sub` (`whether\|if`) and `_NEGATED_CLAIM.sub` ahead of `PARAPHRASE_PATTERNS` (preserving `test_aftercare.py:256-258`), converted `[\r\n]+` to `"; "` before horizontal whitespace folding, and expanded clause-stop lookaheads to commas, dashes, and conjunctions (`however`, `therefore`, `yet`, `so`, `while`, `though`). |
| `PC-002` [High]: Field names (`closure.owner`, `recorded_by`, `pack.reviewer_function`) & `not_needed` remedy evidence | Resolved | Corrected `FR-4`, `P01-T02`, and `P02-T01` to guard `closure["owner"]`, `staff_recorded` `recorded_by`, `pack["reviewer_function"]`, `evaluator_view` `unknowns`, and required remedy `evidence` for `status in ("completed", "not_needed")`. |
| `PC-003` [High]: `NEUTRAL_NOTE_ERROR` self-check, `VIEW_ROLES`, `owner_label`, blank inputs, and receipt `_validate` | Resolved | Adopted `neutral_text`-clean `NEUTRAL_NOTE_ERROR`, gated `AftercareService.propose_pack`/`review_pack` on `VIEW_ROLES` and `owner_label(actor["role"])`, added blank-input `ValidationError` rules, and validated unknown-owner receipt labels and `recorded_by` in `_validate`. |
| `PC-004` [Medium]: `quality.py:add_aftercare` 403-before-400 order and non-echoing `ValueError` | Resolved | Placed `add_aftercare` note validation inside `with self._quality_operation(user, case_id):` before `_qrec` mutation, raised fixed plain-language non-echoing `ValueError`, and added `test_role_matrix.py` to regression checks. |
| `PC-005` [Medium]: Package-level `ruff format --check` excludes and inline typed quality fixture in `test_aftercare_served.py` | Resolved | Specified package-level `python3 -m ruff check` and `python3 -m ruff format --check` in `src/core` and `src/api` (respecting `[tool.ruff.format].exclude`) and inline typed quality fixtures in `test_aftercare_served.py`. |

## Follow-Up Items

* Criterion 1 of Issue #133 (`Household or representative can raise a concern through an accessible route without needing digital access`) and DPO sign-off on outcome data remain open outside Criterion 5; tracked on Issue #133 for subsequent delivery/human review.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/133-no-causation-blame-savings-changes.md
* Ready phase or task: P01 (`P01-T01`)
* Remaining provisional question or blocker: None
