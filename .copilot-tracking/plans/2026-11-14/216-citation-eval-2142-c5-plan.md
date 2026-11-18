<!-- markdownlint-disable-file -->
# Implementation Plan: Issue #216 Child Hardening Pass 5 (`RV-001`..`RV-002`)

## Metadata

* Task ID: 216-citation-eval-2142-c5
* Parent Task ID: 216-citation-eval-2142-c4
* Date: 2026-11-14
* Research reference: .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c5-research.md
* Phase details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c5-phase-details.md

## Scope and Objectives

Resolve the two strict-JSON replay findings from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c4-review.md` (`RV-001`, `RV-002`) in `src/core`:

1. Ensure canonical primitive tagging in `_normalize_json_value` uses exact base JSON types (`value is None`, `type(value) is bool`, `type(value) is str`, `type(value) is int`, `type(value) is float` with `-0.0` normalized to `0.0`, while primitive subclasses fall through to `["repr", ...]`) and `_to_plain_json` normalizes `-0.0` to `0.0` (`PC-001`), preserving digest invariance across `tuple`/`list`, `UserDict`/`dict`, and `-0.0`/`0.0` while remaining injective across distinct JSON types, subclasses, and non-JSON types.
2. Add `_is_strict_json_value` (accepting only exact `None`, `type(v) in (bool, int, str)`, `type(v) is float and math.isfinite(v)`, non-bytes `Sequence`s of strict JSON values, and `Mapping`s with `type(k) is str` keys and strict JSON values; `PC-001`) and enforce it fail-closed in `agreement_gaps` and `compare_chat_against_rule_cards` across all replayable inputs (`cases` 6 canonical fields `id`/`set_name`/`scenario`/`question`/`expected`/`actual`, `paired_cards`, `prompts_evaluated`, `verified_agreement`, `observations`, `benefit_thresholds`, and `normalized_cost_inputs` after converting any aware `datetime` `authority.expires_at` to `.isoformat()`), projecting `normalized_cost_inputs` (`PC-002`) and all 6 case fields through `_to_plain_json` (`RV-001`, `RV-002`) and sanitizing fallback `beside_cost` rates/outcomes (`PC-003`) so both passing and failing comparison reports serialize cleanly with `json.dumps(..., allow_nan=False)` and replay bit-for-bit identically in `resolve_regulatory_surface`.

## Implementation Checklist

* [x] `P01`: Enforce strict JSON-compatible comparison inputs and base-type canonical digest/replay invariance
  * [x] `P01-T01`: Update `_normalize_json_value`, `_to_plain_json`, `_is_strict_json_value`, `agreement_gaps`, `evaluate_citation_and_refusal_gates`, `_score_structural_baseline`, and `compare_chat_against_rule_cards` in `src/core/src/zava_forward/core/regulatory_eval_gates.py` to resolve `RV-001` and `RV-002`.
  * [x] `P01-T02`: Add regression tests in `src/core/tests/test_regulatory_eval_gates_216.py` covering non-serializable `scenario`/`question` rejection (`RV-001`), non-JSON `bytes`/int-key/`nan` input rejection without digest drift (`RV-002`), and `tuple`/`UserDict`/aware-`datetime` `expires_at` JSON round-trip replay acceptance, then run full `src/core` validation (`mypy`, `ruff check .`, `ruff format --check .`, `unittest`).

## Follow-Up Items

* Optional `src/agents` helper delegation to `zava_forward.core.regulatory_eval_gates` remains outside `src/core` scope.
