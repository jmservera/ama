<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #216 Child Hardening Pass 2 (`RV-001`..`RV-007`)

## Metadata

* Task ID: 216-citation-eval-2142-c2
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c2-plan.md

<!-- rpi:phase id=P01 -->
## P01: Implement and Verify `RV-001`..`RV-007` Hardening in `src/core`

<!-- rpi:task id=P01-T01 -->
### P01-T01: Apply `RV-001`..`RV-007` fixes in `regulatory_eval_gates.py` and `src/core/README.md`

* `RV-007` + `PC-001`: Add `_normalize_json_value(value: object) -> object` handling `Mapping` (converting keys via `str(k)` and recursing on values), `Sequence` (when not `isinstance(value, (str, bytes, bytearray))`), and non-finite `float` (`{"__nonfinite_float__": repr(value)}`) before `json.dumps(..., sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False, default=repr)`, and guard `isinstance(bundle, Mapping)` in `deterministic_rule_cards` and `resolve_regulatory_surface`.
* `RV-001`: Populate exact `expected_reason` strings on `adv-certify-compliance`, `adv-prompt-injection`, `adv-zero-width-approve`, `adv-lease-contract`, and `adv-suppress-hazard` in `DEFAULT_EVAL_CASES` (using their exact `_REFUSAL_PATTERNS` / `out_of_scope` strings), and require `expected_reason = _nonblank_str(expected.get("reason"))` to be non-`None` and equal to `actual_refusal` in both `grade_chat_turn` and `_classify_refusal_confusion`.
* `RV-006`: In `agreement_gaps`, loop `for key in ("refusal_owner", "compliance_owner"):` and require `_nonblank_str(agreement.get(key))` to canonically match `COMPLIANCE_GATE_OWNER` whenever `key in agreement`.
* `RV-002`: Add `gates_report_integrity_digest(payload)` over canonical `schema`, `case_set_sha256`, `evaluated_outputs_sha256`, `threshold_status`, `agreement_gaps`, `dataset_gaps`, `sets`, `adversarial_prompts`, and `checks`; emit `"report_integrity_sha256"` in `evaluate_citation_and_refusal_gates`; and in `compare_chat_against_rule_cards`, verify `report_integrity_sha256`, `threshold_status == "owner_agreed"`, `agreement_gaps == []`, `dataset_gaps == []`, `gate_results["citation_validity"].outcome == PASS` (isinstance `GateResult`), `gate_results["refusal_accuracy"].outcome == PASS` (isinstance `GateResult`), non-empty `"graded"` and `"adversarial"` sets, and direct `grade_chat_turn` + `_classify_refusal_confusion` pass across all `cases`.
* `RV-004` + `RV-005`: Document `/api/law/cards/{quote(card_id, safe='')}` (`card_id = id.split("@", 1)[0]`) vs `/api/law/provisions/{quote(provision_id, safe='')}` in `_exact_card_links_match` and `src/core/README.md`; require `len(act_card_provs) > 0` for every card in `_exact_card_links_match`; and guard `if not isinstance(entry, Mapping): unmatched_case_ids.append(f"invalid-paired-{idx}"); continue` and `if not isinstance(case, Mapping): ...` in `_score_structural_baseline`.
* `RV-003`: Add `_expected_from_bundle(bundle: Mapping[str, Any]) -> dict[str, Any]` deriving `kind`, `reason`, `expect_out_of_cadence`, `sources`, `facts`, `cards`, `unknown`, and `as_of` from `bundle`, and require `grade_chat_turn(chat_reply, _expected_from_bundle(bundle)) == {"citation_validity": True, "answer_contract": True}` inside `resolve_regulatory_surface` before enabling `"chat_with_cards"`.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add regression assertions for `RV-001`..`RV-007` in `test_regulatory_eval_gates_216.py` and verify `src/core`

* Add assertions in `src/core/tests/test_regulatory_eval_gates_216.py` for:
  * Appended claim inside `actual["refusal"]` and `sections["unknown_or_conflict"]` on a refused turn failing `grade_chat_turn` and `evaluate_citation_and_refusal_gates` (`RV-001`).
  * Mutating `checks[*]["gate_met"] = True` on a provisional `gates_report` failing `compare_chat_against_rule_cards` (`RV-002`).
  * Passing an ungraded/tampered `chat_reply` (or `workflow_only = False` or mismatched bundle quote) to `resolve_regulatory_surface` with a passing `comparison` falling back to `ship_mode == "cards_only"` and `chat is None` (`RV-003`).
  * Multi-card test using versioned `card-alpha@v1` / `card-beta@v1` IDs, verifying `/api/law/cards/card-alpha` passes when aligned and `/api/law/cards/card-alpha%40v1` or an empty secondary card `provisions: []` or a `None` entry in `paired_cards` fails closed without raising (`RV-004`, `RV-005`).
  * Mismatched `compliance_owner` in `agreement` failing `agreement_gaps` (`RV-006`).
  * Nested `collections.UserDict` inside `cases` hashing deterministically in `case_set_digest` and `evaluated_outputs_digest` (`RV-007`).
