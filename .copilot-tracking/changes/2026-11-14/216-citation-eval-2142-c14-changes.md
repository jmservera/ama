<!-- markdownlint-disable-file -->
# Changes Record: Child Hardening Pass 14 for Issue #216 (`RV-034`..`RV-037`)

* Task ID: `216-citation-eval-2142-c14`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c14-plan.md`
* Phase Details Path: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c14-phase-details.md`
* Critique Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c14-plan-critique.md`
* Status: `Completed`

## Summary

Completed `P01-T01` and `P01-T02` in `src/core` to close `RV-034`..`RV-037` and `PC-001`..`PC-003`:

* `src/core/src/zava_forward/core/regulatory_eval_gates.py`:
  * Expanded `_REFUSAL_PATTERNS[1]` to refuse progressive/participle obligation-satisfaction questions and full modal subject-compliance questions (`RV-034`).
  * Exported `IN_CADENCE_LABEL` and `UNKNOWN_CADENCE_LABEL` alongside `OUT_OF_CADENCE_LABEL` and enforced exact 3-way `_FRESHNESS_LABELS` parity in `_card_provenance_valid` and `_active_bundle_nonconflicting` (`RV-035`).
  * Enforced pre-evaluation `agreed_on` temporal ordering across `agreement_gaps` (via `_min_case_as_of_day` in `evaluate_citation_and_refusal_gates` and `_verify_agreed_gates_report`, plus `<= eval_day` in `compare_chat_against_rule_cards`), `_validate_benefit_thresholds`, and `_compute_cost_per_accepted_check`, rejected observations marked `synthetic` / `simulated` or carrying non-observed `evidence_class`, validated optional `observed_at` / `recorded_at` timestamps (`[agreed_on, eval_day]`), and stamped integrity-hashed `evidence_scope = "offline_workflow_evaluation_not_live_release_approval"` (`RV-036`, `PC-002`).
  * Evaluated `within_unit_ceiling = exact_unit_cost <= agreed_unit_ceiling` using exact unrounded float arithmetic (`RV-037`).
* `src/core/src/zava_forward/core/regulatory_chat.py`:
  * Added keyword-only `ship_gate_comparison` and `enforce_ship_gate: bool = False` to `RegulatoryChat.__init__`, guarded `start()` and `ask()` via `_require_ship_gate()` when `enforce_ship_gate=True`, and defaulted `surface(..., comparison=_UNSET)` to `self.ship_gate_comparison` unless explicitly overridden (`RV-037`, `PC-001`).
* `src/core/tests/test_regulatory_eval_gates_216.py` & `src/core/README.md`:
  * Aligned the 3 synthetic inline card freshness labels to canonical `IN_CADENCE_LABEL` / `UNKNOWN_CADENCE_LABEL`, added `test_c14_progressive_refusal_canonical_freshness_labels_preagreed_timing_and_ship_gate`, and updated the Issue #216 subsection in `src/core/README.md`.

## Task Progress

* [x] `P01-T01`: Harden `regulatory_eval_gates.py` and `regulatory_chat.py` (`RV-034`..`RV-037`, `PC-001`..`PC-003`).
* [x] `P01-T02`: Align 3 inline synthetic freshness labels, add `test_c14_progressive_refusal_canonical_freshness_labels_preagreed_timing_and_ship_gate`, update `src/core/README.md`, and pass all `src/core` static and unit gates.

## Divergences and Amendments

* None.

## Validation Evidence

* `cd src/core && python3 -m mypy`: `Success: no issues found in 318 source files`
* `cd src/core && python3 -m ruff check .`: `All checks passed!`
* `cd src/core && python3 -m ruff format --check .`: `265 files already formatted`
* `cd src/core && python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `Ran 17 tests in 29.881s — OK`
* `cd src/core && PYTHONPATH=src:tests python3 -m unittest tests/test_regulatory_chat.py tests/test_gates.py tests/test_live_doc_links.py`: `Ran 58 tests in 56.716s — OK`
