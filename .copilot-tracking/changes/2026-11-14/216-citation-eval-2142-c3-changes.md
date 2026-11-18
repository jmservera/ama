<!-- markdownlint-disable-file -->
# RPI Changes: Issue #216 Child Hardening Pass 3 (`RV-001`..`RV-003`)

## Metadata

* Task ID: 216-citation-eval-2142-c3
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c3-plan.md
* Declared scope: Full plan (`P01`)
* Execution status: Complete

## Completed Work

### P01: Implement and Verify `RV-001`..`RV-003` Final Hardening in `src/core`

#### P01-T01: Implement tagged `_normalize_json_value`, prompt recomputation in `_verify_agreed_gates_report`, and `_verify_comparison_evidence` in `resolve_regulatory_surface`

* Replaced `_normalize_json_value` with injective structural type-tagged canonicalization (`["prim", ...]`, `["int", ...]`, `["float", val.hex()]`, `["nonfinite_float", ...]`, `["gate_result", ...]`, `["map", sorted_pairs]`, `["bytes", ...]`, `["seq", ...]`, `["repr", ...]`), preserving `Mapping` equivalence (`dict` == `UserDict`) while eliminating cross-type digest collisions (`RV-003`, `PC-002`).
* Updated `_verify_agreed_gates_report` to require `set(ADVERSARIAL_PROMPTS).issubset(raw_prompts)` and recompute `evaluate_adversarial_prompts(raw_prompts, refuse=refuse_question)` directly, rejecting reports whose standalone adversarial prompt results were altered or bypassed (`RV-001`).
* Added `comparison_report_integrity_digest`, captured `effective_now` once inside `compare_chat_against_rule_cards`, emitted `comparison_integrity_sha256` and `verified_comparison_inputs` when `measured_value` is `True`, and added `_verify_comparison_evidence` inside `resolve_regulatory_surface` to verify `comparison_integrity_sha256` and replay `_verify_agreed_gates_report`, `_score_structural_baseline`, `_score_paired_observations`, `cost_per_accepted_check`, and zero-hazard invariants from `verified_comparison_inputs` (`RV-002`, `PC-001`).

#### P01-T02: Add regression tests for tampered prompt totals, forged 4-flag comparisons, and non-finite float vs dict collision resistance in `test_regulatory_eval_gates_216.py`

* Extended `test_hardened_fail_closed_invariants` to assert distinct digests for `float("nan")` vs `{"__nonfinite_float__": "nan"}` and `True` vs `1` alongside `UserDict` == `dict` digest equivalence, rejection of forged + rehashed `adversarial_prompts` gate reports, rejection of forged 4-flag `comparison` dicts in `resolve_regulatory_surface`, and rejection of tampered + rehashed `verified_comparison_inputs` (`rule_hazard_misses = 1`) in `resolve_regulatory_surface`.

## Implementation Discoveries and Decisions

* Ordinary local judgment: Normalized `GateResult` explicitly using `(gate, outcome, reason, owner, correction, rule.as_record() if rule is not None else None)` to satisfy `mypy` (`strict = true`) on `GateRule | None`.

## Validation

* `python3 -m mypy` in `src/core`: PASS (`Success: no issues found in 318 source files`)
* `python3 -m ruff check .` in `src/core`: PASS (`All checks passed!`)
* `python3 -m ruff format --check .` in `src/core`: PASS (`265 files already formatted`)
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v` in `src/core`: PASS (`Ran 9 tests in 14.396s - OK`)
* `test_dependency_rule.py` (2 tests), `test_live_doc_links.py` (2 tests), `test_regulatory_chat.py` (25 tests), `test_gates.py` (31 tests): PASS

## Remaining Work and Blockers

* Remaining active-plan markers: none (`P01`, `P01-T01`, and `P01-T02` complete).
* Blockers: none.

## Follow-Up Items

* Optional `src/agents` helper delegation to `zava_forward.core.regulatory_eval_gates`.
* Out-of-band human threshold sign-off, external held-out legal benchmark, and live staff paired trial with authorised pricing.

## Handoff

* Ready for single post-implementation `rpi-review` at `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c3-review.md`.
