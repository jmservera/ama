<!-- markdownlint-disable-file -->
# RPI Changes: Issue #216 Child Hardening Pass 4 (`RV-001`..`RV-002`)

## Metadata

* Task ID: 216-citation-eval-2142-c4
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c4-plan.md
* Declared scope: Full plan (`P01`)
* Execution status: Complete

## Completed Work

### P01: Implement JSON-Serializable Full-Replay Parity in `src/core`

#### P01-T01: Implement JSON-serializable `verified_comparison_inputs` and full `re_gates` / `re_comparison` equality in `regulatory_eval_gates.py`

* Added `_to_plain_json` and updated `compare_chat_against_rule_cards` so `verified_comparison_inputs` stores only JSON-serializable projected `cases`, `paired_cards`, `prompts`, `agreement`, `observations`, `observation_count`, `benefit_thresholds`, `cost_inputs`, `rule_hazard_misses`, and `now` without embedding `GateResult` dataclasses (`RV-002`, `PC-001`).
* Updated `_verify_agreed_gates_report` to reconstruct `re_gates = evaluate_citation_and_refusal_gates(...)` and require exact `dict(gates_report) == re_gates` equality, and updated `_verify_comparison_evidence` to reconstruct `re_gates` and `re_comparison = compare_chat_against_rule_cards(...)` from `verified_comparison_inputs` and require `re_comparison["measured_value"] is True` and exact `dict(comparison) == re_comparison` equality across every section including all `beside_cost` scalars (`RV-001`).

#### P01-T02: Add regression assertions for `beside_cost` tampering and `json.dumps`/`json.loads` round-trip in `test_regulatory_eval_gates_216.py`

* Added unit assertions verifying that mutating `beside_cost["ai_cost_per_accepted_check"]` or `beside_cost["citation_validity_rate"]` and recomputing `comparison_integrity_sha256` fails closed to `ship_mode == "cards_only"`, and that `json.loads(json.dumps(passing_cmp))` round-trips cleanly and resolves `"chat_with_cards"`.

## Implementation Discoveries and Decisions

* None beyond approved plan scope.

## Validation

* `python3 -m mypy` in `src/core`: PASS (`Success: no issues found in 318 source files`)
* `python3 -m ruff check .` and `python3 -m ruff format --check .` in `src/core`: PASS (`265 files already formatted`)
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v` in `src/core`: PASS (`Ran 9 tests in 14.239s - OK`)
* `test_dependency_rule.py` (2 tests), `test_live_doc_links.py` (2 tests), `test_regulatory_chat.py` (25 tests), `test_gates.py` (31 tests): PASS

## Remaining Work and Blockers

* Remaining active-plan markers: none (`P01`, `P01-T01`, and `P01-T02` complete).
* Blockers: none.

## Follow-Up Items

* Optional `src/agents` helper delegation to `zava_forward.core.regulatory_eval_gates`.
* Out-of-band human threshold sign-off, external held-out legal benchmark, and live staff paired trial with authorised pricing.

## Handoff

* Ready for single post-implementation `rpi-review` at `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c4-review.md`.
