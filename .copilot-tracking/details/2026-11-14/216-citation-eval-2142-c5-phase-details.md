<!-- markdownlint-disable-file -->
# Phase Details: Issue #216 Child Hardening Pass 5 (`216-citation-eval-2142-c5`)

## `P01`: Enforce strict JSON-compatible comparison inputs and base-type canonical digest/replay invariance

### `P01-T01`: Strict JSON validation and base-type canonicalization in `regulatory_eval_gates.py`

* Target file: `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* Exact changes:
  1. Update `_normalize_json_value(value)` to check exact base primitive types (`value is None` -> `["null"]`, `type(value) is bool` -> `["bool", value]`, `type(value) is str` -> `["str", value]`, `type(value) is int` -> `["int", str(value)]`, `type(value) is float` -> nonfinite or `["float", (0.0 if value == 0.0 else value).hex()]`), letting custom primitive subclasses fall through to `["repr", f"{type(value).__qualname__}:{value!r}"]` (`PC-001`).
  2. Update `_to_plain_json(value)` to preserve exact primitives (normalizing `-0.0` to `0.0`), serialize aware `datetime` values via `.isoformat()`, and convert non-strict values deterministically for fallback structures.
  3. Add `_is_strict_json_value(value: object) -> bool` returning `True` iff `value is None`, `type(value) in (bool, int, str)`, `type(value) is float and math.isfinite(value)`, `isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))` whose elements satisfy `_is_strict_json_value`, or `isinstance(value, Mapping)` whose keys have `type(k) is str` and whose values satisfy `_is_strict_json_value` (`PC-001`).
  4. Add `_normalize_cost_inputs_for_json(cost_inputs: Mapping[str, Any] | None) -> dict[str, Any] | None` that converts an aware `datetime` at `cost_inputs["authority"]["expires_at"]` to `.isoformat()` while leaving all other keys/values intact for `_is_strict_json_value` validation, and project `_to_plain_json(normalized_cost_inputs)` into `verified_comparison_inputs["cost_inputs"]` (`PC-002`).
  5. Require `_is_strict_json_value(agreement)` in `agreement_gaps`, normalize `scenario` / `verified_agreement` in `evaluate_citation_and_refusal_gates` when `_is_strict_json_value` holds, normalize `expected_kind` in `_score_structural_baseline` when `_is_strict_json_value` holds (otherwise `repr`), and sanitize `beside_cost` rate (`_finite_float`) and outcome (`_nonblank_str(...) or UNKNOWN`) fields (`PC-003`).
  6. In `compare_chat_against_rule_cards`, validate that `cases` (non-empty `Sequence` of `Mapping`s whose 6 canonical fields `id`, `set_name`, `scenario`, `question`, `expected`, `actual` each satisfy `_is_strict_json_value`), `paired_cards` (`Sequence` of `Mapping`s satisfying `_is_strict_json_value`), `observations` (`Sequence` of `Mapping`s satisfying `_is_strict_json_value`), `gates_report["prompts_evaluated"]` (when present), `gates_report["verified_agreement"]` (when present), `benefit_thresholds` (when a `Mapping`), and `normalized_cost_inputs` (when a `Mapping`) satisfy `_is_strict_json_value`; otherwise append an explicit fail-closed reason to `reasons` so `measured_value` is `False`. When `measured_value` is `True`, project all 6 case fields (`id`, `set_name`, `scenario`, `question`, `expected`, `actual`) and `normalized_cost_inputs` via `_to_plain_json`.
* Completion evidence: `compare_chat_against_rule_cards` rejects non-JSON-compatible inputs fail-closed (`measured_value=False`), `json.dumps(..., allow_nan=False)` succeeds on both passing and failing comparison reports, and every accepted comparison report replays identically through `resolve_regulatory_surface` before and after `json.loads(json.dumps(report, allow_nan=False))`.

### `P01-T02`: Regression tests and `src/core` verification

* Target file: `src/core/tests/test_regulatory_eval_gates_216.py`
* Exact changes:
  1. Test that non-serializable `scenario` or `question` (e.g. `object()`) and non-JSON `expected` values (`bytes`, integer mapping keys, `nan`) cause `compare_chat_against_rule_cards` to fail closed (`measured_value=False`, `ship_mode="cards_only"`) while `json.dumps(failed_cmp, allow_nan=False)` still succeeds.
  2. Test that accepted inputs using `UserDict`, `tuple`, `-0.0`, and aware `datetime` `cost_inputs["authority"]["expires_at"]` produce `measured_value=True`, survive `json.loads(json.dumps(cmp, allow_nan=False))`, and resolve to `chat_with_cards` in `resolve_regulatory_surface`.
* Completion evidence: Clean passes of `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `python3 -m unittest discover -s tests -p 'test_*216*.py' -v` in `src/core`.
