<!-- markdownlint-disable-file -->
# RPI Review: Issue #216 Child Hardening Pass 4 (`RV-001`..`RV-002`)

## Metadata

* Task ID: 216-citation-eval-2142-c4
* Review date: 2026-11-14
* Execution status: Complete
* Outcome: Defects found

## Compared Artifacts

* Research: .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c4-research.md
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c4-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c4-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c4-plan-critique.md
* Changes record: .copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c4-changes.md
* Prior parent review: .copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c3-review.md

## Boundary and Reconciliation Assessment

* Full `beside_cost` and report replay equality (`RV-001` from `c3` and `PC-001` from `c4`) are resolved and verified.
* Independent `rubber-duck` review identified two remaining strict-JSON replay invariants on non-JSON-compatible caller inputs (`RV-001` and `RV-002` below).

## Findings

### RV-001 (High) - `projected_cases` copies `scenario` and `question` without strict JSON validation or normalization

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`compare_chat_against_rule_cards`). When an evaluation case carries a non-JSON-serializable `scenario` or `question` value (for example an arbitrary object or non-finite float), `compare_chat_against_rule_cards` can still report `measured_value=True` while `json.dumps(comparison, allow_nan=False)` raises `TypeError` or `ValueError`.
* Destination: `rpi-implement` (child task `216-citation-eval-2142-c5`)

### RV-002 (High) - Coercing non-JSON-compatible values via `_to_plain_json` alters digest semantics between initial evaluation and replay

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_normalize_json_value`, `_to_plain_json`, `compare_chat_against_rule_cards`). When accepted inputs (`cases`, `paired_cards`, `agreement`, `observations`, `benefit_thresholds`, `cost_inputs`) contain non-JSON-native values (such as `bytes`, non-`str` mapping keys, non-finite floats, custom objects, or primitive subclasses tagged by `type(value).__name__`), `_to_plain_json` transforms them into different canonical types on replay, causing `resolve_regulatory_surface` to reject a comparison report that reported `measured_value=True`. Comparison inputs must fail closed unless strictly JSON-compatible, and primitive canonical tags must use base JSON types (`null`, `bool`, `str`, `int`, `float` with `-0.0` normalized to `0.0`).
* Destination: `rpi-implement` (child task `216-citation-eval-2142-c5`)

## Validation Coverage

* `python3 -m mypy`: PASS (318 source files)
* `python3 -m ruff check .` and `python3 -m ruff format --check .`: PASS (265 files)
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: PASS (9 tests)

## Plan Follow-Up Assessment

* `src/agents` helper deduplication and out-of-band human threshold/trial governance remain distinct non-defect follow-ups outside `src/core` scope.

## Routing Summary

* Route `RV-001` and `RV-002` to child RPI hardening loop `216-citation-eval-2142-c5` in `src/core`.
