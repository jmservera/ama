<!-- markdownlint-disable-file -->
# RPI Research: Issue #216 Child Hardening Pass 2 (`RV-001`..`RV-007`)

## Metadata

* Task ID: 216-citation-eval-2142-c2
* Parent task: 216-citation-eval-2142-c1
* Date: 2026-11-14
* Research disposition: reused
* Planning Readiness: Ready

## Evidence Summary

Existing review `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c1-review.md` and `src/core/src/zava_forward/core/regulatory_eval_gates.py` provide exact, self-contained evidence (`E1`..`E7`) for closing all seven findings:

* `E1` (`RV-001`): Populate explicit canonical `expected_reason` strings on all refused `DEFAULT_EVAL_CASES` (computed deterministically via `refuse_question` / `EMPTY_BUNDLE_REFUSAL`) and require `expected_reason is not None and actual_refusal == expected_reason` in `grade_chat_turn` and `_classify_refusal_confusion`.
* `E2` (`RV-002`): Add `gates_report_integrity_digest(report)` over canonical `case_set_sha256`, `evaluated_outputs_sha256`, `threshold_status`, `agreement_gaps`, `dataset_gaps`, and `checks`, emit `report_integrity_sha256` from `evaluate_citation_and_refusal_gates`, and in `compare_chat_against_rule_cards` verify `report_integrity_sha256`, `threshold_status == "owner_agreed"`, `agreement_gaps == []`, `dataset_gaps == []`, `gate_results[*].outcome == PASS`, and direct per-case `grade_chat_turn` pass.
* `E3` (`RV-003`): Derive expected turn ground truth from `bundle` inside `resolve_regulatory_surface` and require `grade_chat_turn(chat_reply, expected_from_bundle) == {"citation_validity": True, "answer_contract": True}` before returning `"chat_with_cards"`.
* `E4` (`RV-004`): Explicitly document the unversioned rule-card route `/api/law/cards/{quote(card_id, safe='')}` (`card_id = id.split("@", 1)[0]`) vs versioned provision route `/api/law/provisions/{quote(provision_id, safe='')}` in `regulatory_eval_gates.py` and `src/core/README.md`, and test versioned `card-alpha@v1` / `card-beta@v1` IDs.
* `E5` (`RV-005`): Guard `isinstance(entry, Mapping)` in `_score_structural_baseline` and require non-empty `provisions` (`len(act_card_provs) > 0`) on every card in `_exact_card_links_match`.
* `E6` (`RV-006`): Validate both optional `refusal_owner` and optional `compliance_owner` against `COMPLIANCE_GATE_OWNER` in `agreement_gaps`.
* `E7` (`RV-007`): Recursively normalize nested `Mapping` and non-string/bytes `Sequence` values in `_canon_json`.
