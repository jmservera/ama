<!-- markdownlint-disable-file -->
# RPI Review: Issue #216 Child Hardening Pass 3 (`RV-001`..`RV-003`)

## Metadata

* Task ID: 216-citation-eval-2142-c3
* Review date: 2026-11-14
* Execution status: Complete
* Outcome: Defects found

## Compared Artifacts

* Research: .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c3-research.md
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c3-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c3-plan-critique.md
* Changes record: .copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c3-changes.md
* Prior parent review: .copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c2-review.md

## Boundary and Reconciliation Assessment

* Standalone adversarial prompt recomputation (`RV-001` from `c2`) and tagged structural canonicalization (`RV-003` from `c2`) are resolved and verified.
* Independent `rubber-duck` review identified one blocking comparison-parity gap on `beside_cost` scalar fields and one non-blocking JSON-serializability regression from embedding `GateResult` dataclasses inside `verified_comparison_inputs`.

## Findings

### RV-001 (High) - `_verify_comparison_evidence` checks `beside_cost` outcomes/hazards without verifying full `beside_cost` scalar parity

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_verify_comparison_evidence`). Mutating `beside_cost["ai_cost_per_accepted_check"]` or `beside_cost["citation_validity_rate"]` / `refusal_accuracy_rate` and recomputing `comparison_integrity_sha256` was not caught because `beside_cost` scalar fields were not compared for full equality against replayed gate and cost outputs.
* Destination: `rpi-implement` (child task `216-citation-eval-2142-c4`)

### RV-002 (Low) - Embedding raw `gates_report` (`GateResult` dataclasses) inside `verified_comparison_inputs` breaks `json.dumps` on passing comparison reports

* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`compare_chat_against_rule_cards`). Storing pure JSON-serializable replay inputs (`cases`, `paired_cards`, `prompts`, `agreement`, `observations`, `observation_count`, `benefit_thresholds`, `cost_inputs`, `rule_hazard_misses`, `now`) and replaying `evaluate_citation_and_refusal_gates` + `compare_chat_against_rule_cards` for full `dict(comparison) == re_comparison` equality resolves both `RV-001` and `RV-002` cleanly and preserves `json.loads(json.dumps(comparison))` round-trip verification.
* Destination: `rpi-implement` (child task `216-citation-eval-2142-c4`)

## Validation Coverage

* `python3 -m mypy`: PASS (318 source files)
* `python3 -m ruff check .` and `python3 -m ruff format --check .`: PASS (265 files)
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: PASS (9 tests)

## Plan Follow-Up Assessment

* `src/agents` helper deduplication and out-of-band human threshold/trial governance remain distinct non-defect follow-ups outside `src/core` scope.

## Routing Summary

* Route `RV-001` and `RV-002` to child RPI hardening loop `216-citation-eval-2142-c4` in `src/core`.
