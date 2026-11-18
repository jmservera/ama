<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #216 Child Hardening Pass 3 (`RV-001`..`RV-003`)

## P01: Implement and Verify `RV-001`..`RV-003` Final Hardening in `src/core`

### P01-T01

* Target file: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`src/core/README.md` updated if exported digest helper mentioned)
* Exact edits:
  1. Replace `_normalize_json_value` with tagged structural normalization:
     * `None` / `bool` / `str` -> `["prim", type(value).__name__, value]`
     * `int` (non-`bool`) -> `["int", str(value)]`
     * `float` -> `["nonfinite_float", "-inf" | "inf" | "nan"]` if not `math.isfinite(value)` else `["float", value.hex()]`
     * `Mapping` -> `["map", sorted(([_normalize_json_value(k), _normalize_json_value(v)] for k, v in value.items()), key=lambda pair: json.dumps(pair[0], separators=(",", ":"), ensure_ascii=True))]`
     * `Sequence` (excluding `str`, `bytes`, `bytearray`) -> `["seq", [_normalize_json_value(item) for item in value]]`
     * `bytes` / `bytearray` -> `["bytes", bytes(value).hex()]`
     * `GateResult` -> `["gate_result", _normalize_json_value(value.rule.as_record()), value.outcome, value.reason, list(value.missing)]`
     * fallback -> `["repr", f"{type(value).__qualname__}:{value!r}"]`
  2. In `_verify_agreed_gates_report`:
     * Require `set(ADVERSARIAL_PROMPTS).issubset(raw_prompts)` and recompute `recomputed_prompts = evaluate_adversarial_prompts(raw_prompts, refuse=refuse_question)`.
     * Require `recomputed_prompts["missed"] == 0`, `recomputed_prompts["refused"] == len(raw_prompts)`, and `dict(adv_prompts) == recomputed_prompts`.
  3. Capture `effective_now = now if now is not None else datetime.now(UTC)` in `compare_chat_against_rule_cards`, add `comparison_report_integrity_digest(comparison: Mapping[str, Any]) -> str`, and emit `comparison_integrity_sha256` and `verified_comparison_inputs` (`cases`, `paired_cards`, `gates_report`, `observations`, `benefit_thresholds`, `cost_inputs`, `rule_hazard_misses`, `now`) when `measured_value` is `True`.
  4. Add `_verify_comparison_evidence(comparison: object) -> bool` called inside `resolve_regulatory_surface`, checking `comparison_integrity_sha256`, `reasons == []`, `recommendation == "ship_chat_with_cards"`, `overall_pass is None`, and replaying `_verify_agreed_gates_report`, `_score_structural_baseline`, `_score_paired_observations`, `cost_per_accepted_check`, and zero-hazard checks directly from `verified_comparison_inputs`, requiring exact structural parity with the reported comparison sections (`PC-001`, `PC-002`).

### P01-T02

* Target file: `src/core/tests/test_regulatory_eval_gates_216.py`
* Exact edits:
  1. Assert `case_set_digest` / `evaluated_outputs_digest` produce distinct SHA-256 digests for `float("nan")` vs `{"__nonfinite_float__": "nan"}`, `1` vs `True` vs `"1"`, and `-0.0` vs `0.0`, while `UserDict({"k": 1})` equals `{"k": 1}`.
  2. Assert a `gates_report` built with `refuse=lambda _q: None` whose `adversarial_prompts`, `checks`, `gate_results`, `threshold_status`, `verified_agreement`, and `report_integrity_sha256` are forged still fails `compare_chat_against_rule_cards` -> `cards_only`.
  3. Assert passing a forged 4-flag dict (`{"schema": COMPARISON_SCHEMA, "measured_value": True, "cards_alone": False, "ship_mode": "chat_with_cards"}`) — and even a tampered + rehashed `comparison` — to `resolve_regulatory_surface` fails closed to `ship_mode == "cards_only"` (`cards_alone is True`, `chat is None`).
