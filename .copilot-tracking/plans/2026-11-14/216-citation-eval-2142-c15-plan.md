<!-- markdownlint-disable-file -->
# Implementation Plan: Child Hardening Pass 15 for Issue #216 (`RV-038`..`RV-040`)

* Task ID: `216-citation-eval-2142-c15`
* Parent Task ID: `216-citation-eval-2142-c14`
* Date: `2026-11-14`
* Status: `Approved`

## Executive Summary

Close the three `src/core` findings (`RV-038`..`RV-040`) from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c14-review.md`:

1. Refine `_REFUSAL_PATTERNS[1]` so noun/appointment uses of `"meeting"` (such as `"Is there a meeting about statutory obligations?"` or `"Are we having a meeting on legal duties?"`) are never falsely refused, while progressive verb compliance questions (`"Is this damp home meeting its legal obligations?"`) remain refused (`RV-038`).
2. Require every paired observation row in `_score_paired_observations` to carry a valid `observed_at` or `recorded_at` timestamp (mutually consistent if both are supplied) within `[benefit_thresholds.agreed_on, eval_day]` (`RV-039`).
3. Enforce `cost_inputs.accepted_definition.agreed_on <= min_observation_day` (and `<= min_accepted_chat_day` and `<= eval_day`) inside `_compute_cost_per_accepted_check` / `compare_chat_against_rule_cards` so an accepted-check definition cannot post-date the paired trial checks it governs (`RV-040`).

## Sources

* `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c15-research.md`
* `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c14-review.md`
* `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* `src/core/tests/test_regulatory_eval_gates_216.py`
* `src/core/README.md`

## User Decisions and Requirements

* Deliver the remaining locally verifiable acceptance criteria for Issue #216 strictly within `src/core`.
* Keep `BRD OD-51` open (no hardcoded GBP target constants) and preserve `#214` backwards compatibility.
* Verify in `src/core` with `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*216*.py' -v`, and commit cleanly without pushing.

## Goals

* Eliminate noun-`"meeting"` false refusals while preserving progressive obligation-satisfaction refusals (`RV-038`).
* Require dated paired trial observations (`observed_at` / `recorded_at`) bounded by `[benefit_thresholds.agreed_on, eval_day]` (`RV-039`).
* Bound `cost_inputs.accepted_definition.agreed_on` by the earliest paired observation timestamp as well as `eval_day` (`RV-040`).

## Scope and Non-Goals

* Scope: `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, `src/core/README.md`.
* Non-Goals: Edits outside `src/core`; removing existing tests (`none` removals; max `1` new test method `test_c15_meeting_noun_precision_mandatory_observation_dates_and_accepted_def_ordering` plus populating `"observed_at"` in `_valid_observations`).

## Functional Requirements

* `FR-1` (`RV-038`): `_REFUSAL_PATTERNS[1]` distinguishes progressive verb `meeting` / `satisfying` (requiring compliance subjects after `is|are|was|were`, blocking articles/having-phrases `a|an|the|any|next|scheduled|staff|resident|team` immediately before `meeting`, and blocking prepositions `about|on|for|with|at|in|from|regarding|concerning` immediately after `meeting`) from compliance obligation objects.
* `FR-2` (`RV-039`): `_score_paired_observations` rejects any observation row missing both `observed_at` and `recorded_at`, rejects mismatched UTC days when both are supplied, requires `thresholds_agreed_day <= obs_day <= eval_day`, and records `min_observation_day` and `min_accepted_chat_day` on the returned `paired_trial` dict.
* `FR-3` (`RV-040`): `_compute_cost_per_accepted_check` accepts optional `max_agreed_day: str | None = None`, and `compare_chat_against_rule_cards` passes the earliest of `trial["min_observation_day"]` and `trial["min_accepted_chat_day"]` so `accepted_definition.agreed_on` cannot post-date either the paired observations or `eval_day`; furthermore, `compare_chat_against_rule_cards` also requires `gates_report["verified_agreement"]["agreed_on"] <= min_observation_day` when observations are present.

## Non-Functional Requirements

* `NFR-1`: Linear regex matching without nested unbounded quantifiers; zero `mypy` / `ruff` issues across `src/core`.

## Acceptance Criteria

* `AC-1`: `"Is there a meeting about statutory obligations?"`, `"Are we having a meeting on legal duties?"`, and `"Is the home team scheduling a meeting regarding compliance standards?"` return `None` from `refuse_question`, while `"Is this damp home meeting its legal obligations?"` and `"Are we meeting statutory requirements?"` refuse with the compliance refusal reason.
* `AC-2`: Undated paired observation rows (missing `observed_at` and `recorded_at`) or rows where `observed_at` and `recorded_at` disagree fail closed with `measured_value == False` and `recommendation == "ship_cards_only"`.
* `AC-3`: When observations are recorded on `"2026-10-16"` and `now` is `"2026-10-20"`, a `cost_inputs.accepted_definition.agreed_on` of `"2026-10-18"` (after the observations, even though `<= now`) fails closed (`ai_cost_per_accepted_check == "Unknown"`, `measured_value == False`, `recommendation == "ship_cards_only"`).

## Critique Disposition

* Critique artifact: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c15-plan-critique.md` (`Complete`, `Pass` with one folded refinement `PC-001`: also check `verified_agreement["agreed_on"] <= min_observation_day` and reject mismatched `observed_at` vs `recorded_at` when both keys are supplied on the same row).

## Phase Checklist

<!-- P01 -->
### Phase 1: Close `RV-038`..`RV-040` in `src/core` and Verify

* [x] `P01`: Implement `RV-038`..`RV-040` in `regulatory_eval_gates.py`, `test_regulatory_eval_gates_216.py`, and `src/core/README.md`, and pass all `src/core` checks.
  <!-- P01-T01 -->
  * [x] `P01-T01`: Refine noun-vs-verb `"meeting"` in `_REFUSAL_PATTERNS[1]`, enforce mandatory `observed_at` / `recorded_at` timestamps in `_score_paired_observations`, and enforce pre-observation `agreed_on` ordering on `accepted_definition` and `verified_agreement` in `regulatory_eval_gates.py`.
  <!-- P01-T02 -->
  * [x] `P01-T02`: Add `"observed_at"` to `_valid_observations`, add `test_c15_meeting_noun_precision_mandatory_observation_dates_and_accepted_def_ordering` in `test_regulatory_eval_gates_216.py`, update `src/core/README.md`, and pass `mypy`, `ruff`, Issue #216 tests, and companion `src/core` tests.

## Follow-Up Items

* Wire `src/api/src/zava_forward/api/server.py` and `src/agents/src/zava_forward/agents/regulatory_chat.py` to pass verified `ship_gate_comparison` / `enforce_ship_gate=True` in a separate multi-package integration PR outside `src/core`.
* Populate ratified finance policy values once `BRD OD-51` is closed.
