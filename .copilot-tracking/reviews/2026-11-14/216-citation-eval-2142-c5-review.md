<!-- markdownlint-disable-file -->
# RPI Review: Issue #216 Child Hardening Pass 5 (`RV-001`..`RV-002`)

## Metadata

* Task ID: 216-citation-eval-2142-c5
* Review date: 2026-11-14
* Execution status: Complete
* Outcome: Defects found

## Compared Artifacts

* Research: .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c5-research.md
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c5-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c5-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c5-plan-critique.md
* Changes record: .copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c5-changes.md
* Prior parent review: .copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c4-review.md

## Boundary and Reconciliation Assessment

* Base-type canonical primitive tagging (`PC-001`), normalized `expires_at` projection (`PC-002`), and sanitized fallback `beside_cost` metrics (`PC-003`) are implemented and verified.
* Independent `rubber-duck` review found three remaining edge cases when non-`list` sequences or malformed non-iterable fields enter structural scoring prior to strict JSON validation (`RV-001`..`RV-003`).

## Findings

### RV-001 (High) - Accepted `tuple` in `recorded_home_facts` scores differently before and after JSON list projection

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_score_structural_baseline`, `compare_chat_against_rule_cards`). Checking `isinstance(..., list)` instead of non-string `Sequence` and scoring raw inputs prior to `_to_plain_json` projection caused a non-empty tuple in `baseline["recorded_home_facts"]` to be ignored on initial call (`measured_value=True`) and counted after list conversion on replay (`cards_only`).
* Destination: `rpi-implement` (child task `216-citation-eval-2142-c6`)

### RV-002 (High) - Non-iterable malformed collection fields (`expected.sources = object()`) raise `TypeError` during pre-validation scoring instead of failing closed

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_score_structural_baseline`, `grade_chat_turn`, `deterministic_rule_cards`, `compare_chat_against_rule_cards`). Iterating `.get("sources", ())` without verifying a non-string/bytes `Sequence` raises `TypeError` when a malformed non-iterable object is supplied.
* Destination: `rpi-implement` (child task `216-citation-eval-2142-c6`)

### RV-003 (Medium) - Answer-row `expected_kind` in `_score_structural_baseline` emits raw `expected_kind` instead of `safe_expected_kind`

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_score_structural_baseline`). When an object compares equal to `"answer"` (`__eq__`), copying raw `expected_kind` into `rows` leaves a failed comparison report unserializable by `json.dumps(..., allow_nan=False)`.
* Destination: `rpi-implement` (child task `216-citation-eval-2142-c6`)

## Validation Coverage

* `python3 -m mypy`: PASS (318 source files)
* `python3 -m ruff check .` and `python3 -m ruff format --check .`: PASS (265 files)
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: PASS (9 tests)

## Plan Follow-Up Assessment

* `src/agents` helper deduplication remains a distinct optional follow-up outside `src/core` scope.

## Routing Summary

* Route `RV-001`..`RV-003` to child RPI hardening loop `216-citation-eval-2142-c6` in `src/core`.
