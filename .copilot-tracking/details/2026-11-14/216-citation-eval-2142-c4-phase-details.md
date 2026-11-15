<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #216 Child Hardening Pass 4 (`RV-001`..`RV-002`)

## P01: Implement JSON-Serializable Full-Replay Parity in `src/core`

### P01-T01

* Target file: `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* Exact edits:
  1. Add `_to_plain_json(value: object) -> Any` recursively converting `Mapping` -> `{str(k): _to_plain_json(v) ...}` and non-string/bytes `Sequence` -> `[_to_plain_json(item) ...]` (rejecting non-JSON-serializable scalars safely or leaving `None`/`bool`/`int`/`float` finite/`str`).
  2. In `_verify_agreed_gates_report(cases, gates_report)`: after validating `raw_prompts` (`set(ADVERSARIAL_PROMPTS).issubset(raw_prompts)`) and `verified_agreement`, compute `re_gates = evaluate_citation_and_refusal_gates(cases, prompts=raw_prompts, refuse=refuse_question, agreement=verified_agreement)` and verify `re_gates["threshold_status"] == "owner_agreed"`, `re_gates["gate_results"]["citation_validity"].outcome == PASS`, `re_gates["gate_results"]["refusal_accuracy"].outcome == PASS`, and `dict(gates_report) == re_gates`.
  3. In `compare_chat_against_rule_cards`: when `measured_value` is `True`, build `projected_cases = [{"id": c.get("id"), "set_name": c.get("set_name"), "scenario": c.get("scenario"), "question": c.get("question"), "expected": _to_plain_json(c.get("expected")), "actual": _to_plain_json(c.get("actual"))} for c in cases if isinstance(c, Mapping)]` and store `verified_inputs = {"cases": projected_cases, "paired_cards": _to_plain_json(list(paired_cards)), "prompts": list(gates_report["prompts_evaluated"]), "agreement": _to_plain_json(gates_report["verified_agreement"]), "observations": _to_plain_json(list(observations)), "observation_count": len(observations), "benefit_thresholds": _to_plain_json(benefit_thresholds), "cost_inputs": _to_plain_json(cost_inputs), "rule_hazard_misses": rule_miss_count, "now": serialized_now}`.
  4. In `_verify_comparison_evidence(comparison)`: extract and type-check `verified_comparison_inputs`, reconstruct `re_gates = evaluate_citation_and_refusal_gates(v_cases, prompts=v_prompts, refuse=refuse_question, agreement=v_agreement)` and `re_comparison = compare_chat_against_rule_cards(v_cases, v_paired, gates_report=re_gates, observations=v_obs, benefit_thresholds=v_thresholds, cost_inputs=v_cost, rule_hazard_misses=v_rule_misses, now=v_now)`, and require `re_comparison["measured_value"] is True and dict(comparison) == re_comparison`.

### P01-T02

* Target file: `src/core/tests/test_regulatory_eval_gates_216.py`
* Exact edits:
  1. Assert `json_roundtrip = json.loads(json.dumps(passing_cmp))` succeeds and `resolve_regulatory_surface(sample["bundle"], json_roundtrip, chat_reply=sample["actual"])["ship_mode"] == "chat_with_cards"`.
  2. Assert mutating `passing_cmp["beside_cost"]["ai_cost_per_accepted_check"]` or `passing_cmp["beside_cost"]["citation_validity_rate"]` and recomputing `comparison_integrity_sha256` fails closed (`ship_mode == "cards_only"`, `chat is None`).
