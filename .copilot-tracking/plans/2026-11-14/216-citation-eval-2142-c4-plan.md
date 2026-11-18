<!-- markdownlint-disable-file -->
# RPI Plan: Issue #216 Child Hardening Pass 4 (`RV-001`..`RV-002`)

## Metadata

* Task ID: 216-citation-eval-2142-c4
* Parent task: 216-citation-eval-2142-c3
* Planning date: 2026-11-14
* Planning status: finalized

## Executive Summary

Close `RV-001` and `RV-002` from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c3-review.md` in `src/core/src/zava_forward/core/regulatory_eval_gates.py` and `src/core/tests/test_regulatory_eval_gates_216.py` by storing JSON-serializable replay inputs in `verified_comparison_inputs` and enforcing full replayed-report equality (`dict(gates_report) == re_gates` in `_verify_agreed_gates_report` and `dict(comparison) == re_comparison` in `_verify_comparison_evidence`).

## Sources

* .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c4-research.md (`E1`)
* .copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c3-review.md (`RV-001`, `RV-002`)

## Goals and Scope

* Scope: `src/core/src/zava_forward/core/regulatory_eval_gates.py` and `src/core/tests/test_regulatory_eval_gates_216.py`.
* Non-Goals: Touching `src/agents`, `src/api`, or `pyproject.toml`.

## Functional Requirements

* `FR-1` (`RV-001`): `_verify_agreed_gates_report` reconstructs `re_gates = evaluate_citation_and_refusal_gates(cases, prompts=raw_prompts, refuse=refuse_question, agreement=verified_agreement)` (after checking `set(ADVERSARIAL_PROMPTS).issubset(raw_prompts)` and zero-defect per-case grades) and requires `dict(gates_report) == re_gates`. `_verify_comparison_evidence` reconstructs `re_gates` and `re_comparison = compare_chat_against_rule_cards(...)` from `verified_comparison_inputs` and requires `re_comparison["measured_value"] is True` and `dict(comparison) == re_comparison` so mutating ANY field in `beside_cost`, `economics`, `paired_trial`, `structural_benchmark`, or `hazard_misses` (even with recomputed digest) fails closed.
* `FR-2` (`RV-002`): `verified_comparison_inputs` stores only JSON-serializable values (`_to_plain_json` over projected `cases`, `paired_cards`, `prompts`, `agreement`, `observations`, `observation_count`, `benefit_thresholds`, `cost_inputs`, `rule_hazard_misses`, `now`) with no `GateResult` instances, so `json.dumps(comparison)` succeeds and `resolve_regulatory_surface` accepts `json.loads(json.dumps(comparison))` identically to the in-memory report.

## Acceptance Criteria

* `RV-001` and `RV-002` are resolved in `src/core` and covered by unit assertions (`beside_cost` mutation + rehash fails closed; `json.loads(json.dumps(passing_cmp))` round-trips cleanly); bare `mypy`, `ruff check .`, `ruff format --check .`, and `test_*216*.py` pass cleanly.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement JSON-Serializable Full-Replay Parity in `src/core`

* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement JSON-serializable `verified_comparison_inputs` and full `re_gates` / `re_comparison` equality in `regulatory_eval_gates.py`

* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c4-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add regression assertions for `beside_cost` tampering and `json.dumps`/`json.loads` round-trip in `test_regulatory_eval_gates_216.py`

* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c4-phase-details.md

## Critique Disposition

Single final-candidate critique recorded at `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c4-plan-critique.md` (`PC-001` applied directly: project each stored case in `verified_comparison_inputs["cases"]` to canonical `{id, set_name, scenario, question, expected, actual}` so extra caller scratch keys that aren't JSON-serializable cannot break `json.dumps`, while `_verify_agreed_gates_report` compares `gates_report` directly against `evaluate_citation_and_refusal_gates(cases, ...)`).

## Follow-Up Items

* Optional `src/agents` helper deduplication against `zava_forward.core.regulatory_eval_gates`.
* Out-of-band human threshold sign-off, external held-out legal benchmark, and live staff paired trial with authorised pricing.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c4-changes.md
* Ready phase or task: Complete (`P01` / `P01-T01`, `P01-T02`); ready for `rpi-review`
* Remaining provisional question or blocker: none
