<!-- markdownlint-disable-file -->
# RPI Plan: Issue #216 Child Hardening Pass 3 (`RV-001`..`RV-003`)

## Metadata

* Task ID: 216-citation-eval-2142-c3
* Parent task: 216-citation-eval-2142-c2
* Planning date: 2026-11-14
* Planning status: finalized

## Executive Summary

Close all three remaining findings (`RV-001`..`RV-003`) from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c2-review.md` in `src/core/src/zava_forward/core/regulatory_eval_gates.py` and `src/core/tests/test_regulatory_eval_gates_216.py`: recomputing standalone adversarial prompt refusals in `_verify_agreed_gates_report`, verifying full comparison evidence and integrity at `resolve_regulatory_surface`, and using collision-free tagged structural canonicalization in `_normalize_json_value`.

## Sources

* .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c3-research.md (`E1`..`E3`)
* .copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c2-review.md (`RV-001`..`RV-003`)

## Goals and Scope

* Scope: `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md` (if needed).
* Non-Goals: Touching `src/agents`, `src/api`, or `pyproject.toml`.

## Functional Requirements

* `FR-1` (`RV-001`): `_verify_agreed_gates_report` requires `set(ADVERSARIAL_PROMPTS).issubset(raw_prompts)` and recomputes `evaluate_adversarial_prompts(raw_prompts, refuse=refuse_question)`, requiring `missed == 0`, `refused == len(raw_prompts)`, and exact match against `gates_report["adversarial_prompts"]`, plus verified case rates >= `verified_agreement["min_rates"]`.
* `FR-2` (`RV-002`, `PC-001`): `compare_chat_against_rule_cards` captures `effective_now` once, emits `comparison_integrity_sha256` (`comparison_report_integrity_digest`), and populates `verified_comparison_inputs` (`cases`, `paired_cards`, `gates_report`, `observations`, `benefit_thresholds`, `cost_inputs`, `rule_hazard_misses`, and `effective_now` ISO string) when `measured_value` is `True`. `resolve_regulatory_surface` calls `_verify_comparison_evidence(comparison)` to verify `comparison_integrity_sha256` and replay `_verify_agreed_gates_report`, `_score_structural_baseline`, `_score_paired_observations`, `cost_per_accepted_check`, and zero-hazard invariants from `verified_comparison_inputs` before enabling `"chat_with_cards"`.
* `FR-3` (`RV-003`): `_normalize_json_value` encodes every Python node with an explicit structural type tag so `float("nan")`, `{"__nonfinite_float__": "nan"}`, `bool`, `int`, `float`, `str`, `Sequence`, `Mapping`, and `GateResult` have zero canonical JSON collisions while preserving `Mapping` equivalence (`dict` == `UserDict`).

## Acceptance Criteria

* All three findings (`RV-001`..`RV-003`) are resolved in `src/core` and covered by unit tests in `test_regulatory_eval_gates_216.py`; bare `mypy`, `ruff check .`, `ruff format --check .`, and `test_*216*.py` pass cleanly.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement and Verify `RV-001`..`RV-003` Final Hardening in `src/core`

* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement tagged `_normalize_json_value`, prompt recomputation in `_verify_agreed_gates_report`, and `_verify_comparison_evidence` in `resolve_regulatory_surface`

* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c3-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add regression tests for tampered prompt totals, forged 4-flag comparisons, and non-finite float vs dict collision resistance in `test_regulatory_eval_gates_216.py`

* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c3-phase-details.md

## Critique Disposition

Single final-candidate critique recorded at `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c3-plan-critique.md` (`PC-001` and `PC-002` applied directly).

## Follow-Up Items

* Optional `src/agents` helper deduplication against `zava_forward.core.regulatory_eval_gates`.
* Out-of-band human threshold sign-off, external held-out legal benchmark, and live staff paired trial with authorised pricing.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c3-changes.md
* Ready phase or task: Complete (`P01` / `P01-T01`, `P01-T02`); ready for `rpi-review`
* Remaining provisional question or blocker: none
