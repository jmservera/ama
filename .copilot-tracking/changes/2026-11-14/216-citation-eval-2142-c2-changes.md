<!-- markdownlint-disable-file -->
# RPI Changes: Issue #216 Child Hardening Pass 2 (`RV-001`..`RV-007`)

## Metadata

* Task ID: 216-citation-eval-2142-c2
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c2-plan.md
* Declared scope: Full plan (`P01`)
* Execution status: Complete

## Completed Work

### P01: Implement and Verify `RV-001`..`RV-007` Hardening in `src/core`

#### P01-T01: Apply `RV-001`..`RV-007` fixes in `regulatory_eval_gates.py` and `src/core/README.md`

* Populated exact canonical non-blank `expected_reason` strings across all refused items in `DEFAULT_EVAL_CASES` (`adv-certify-compliance`, `adv-prompt-injection`, `adv-zero-width-approve`, `adv-lease-contract`, `adv-suppress-hazard` alongside existing graded refusal cases) and tightened `grade_chat_turn` and `_classify_refusal_confusion` to require `expected_reason` to be non-`None` and equal to `actual["refusal"]` and `sections["unknown_or_conflict"]` (`RV-001`).
* Added `gates_report_integrity_digest`, `verified_agreement`, and `prompts_evaluated` to `evaluate_citation_and_refusal_gates`, and added `_verify_agreed_gates_report` inside `compare_chat_against_rule_cards` to verify `report_integrity_sha256`, `evaluated_outputs_sha256`, `verified_agreement` (`agreement_gaps == []`), `PASS` `GateResult` outcomes, non-empty `graded` and `adversarial` sets, zero adversarial prompt misses, and direct per-case `grade_chat_turn` + `_classify_refusal_confusion` passes (`RV-002`).
* Added `_expected_from_bundle` and verified `grade_chat_turn(chat_reply, _expected_from_bundle(bundle))` directly inside `resolve_regulatory_surface`, falling back to `ship_mode = "cards_only"` (`cards_alone = True`, `chat = None`) whenever `chat_reply` fails extractive citation or human-boundary verification against `bundle` (`RV-003`).
* Documented unversioned rule-card routes (`/api/law/cards/{quote(card_id, safe='')}`) versus versioned provision routes (`/api/law/provisions/{quote(provision_id, safe='')}`) in `_exact_card_links_match` and `src/core/README.md` (`RV-004`).
* Guarded `_score_structural_baseline` against non-`Mapping` entries in `paired_cards` and `cases`, and required `len(act_card_provs) > 0` for every active answer card in `_exact_card_links_match` (`RV-005`).
* Extended `agreement_gaps` to validate optional `compliance_owner` as well as `refusal_owner` against `COMPLIANCE_GATE_OWNER` (`RV-006`).
* Added `_normalize_json_value` (recursively converting nested `Mapping`, non-string/bytes `Sequence`, and non-finite `float` objects before `json.dumps(..., allow_nan=False, default=repr)`) in `_canon_json`, plus runtime `isinstance(bundle, Mapping)` guards in `deterministic_rule_cards` and `resolve_regulatory_surface` (`RV-007`, `PC-001`).

#### P01-T02: Add regression assertions for `RV-001`..`RV-007` in `test_regulatory_eval_gates_216.py` and verify `src/core`

* Updated `multi_bundle` card IDs to versioned `card-alpha@v1` / `card-beta@v1` while retaining unversioned `/api/law/cards/card-alpha` / `/api/law/cards/card-beta` routes, and added `test_hardened_fail_closed_invariants` covering appended refusal claims, `reason=None` rejection, `compliance_owner` validation, `UserDict` + non-finite float digests, tampered and re-hashed provisional `gates_report` rejection, malformed `paired_cards` entries, versioned `/api/law/cards/...%40v1` route rejection, unmapped empty-provision card rejection, and spoofed `chat_reply` fallback in `resolve_regulatory_surface`.

## Implementation Discoveries and Decisions

* Ordinary local judgment: Storing `verified_agreement` (populated only when `owner_agreed` is `True`) and `prompts_evaluated` in `evaluate_citation_and_refusal_gates` lets `compare_chat_against_rule_cards` re-verify owner agreement and per-case grades directly, defeating both raw flag mutations and recomputed unkeyed SHA-256 digests on forged provisional reports. No divergence from approved scope.

## Validation

* `python3 -m mypy` in `src/core`: PASS (`Success: no issues found in 318 source files`)
* `python3 -m ruff check .` in `src/core`: PASS (`All checks passed!`)
* `python3 -m ruff format --check .` in `src/core`: PASS (`265 files already formatted`)
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v` in `src/core`: PASS (`Ran 9 tests in 11.749s - OK`)
* `python3 -m unittest discover -s tests -p 'test_dependency_rule.py' -v` in `src/core`: PASS (`Ran 2 tests - OK`)
* `python3 -m unittest discover -s tests -p 'test_live_doc_links.py' -v` in `src/core`: PASS (`Ran 2 tests - OK`)
* `python3 -m unittest discover -s tests -p 'test_regulatory_chat.py' -v` in `src/core`: PASS (`Ran 25 tests - OK`)
* `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_gates.py' -q` in `src/core`: PASS (`Ran 31 tests - OK`)

## Remaining Work and Blockers

* Remaining active-plan markers: none (`P01`, `P01-T01`, and `P01-T02` complete).
* Blockers: none.

## Follow-Up Items

* Optional `src/agents` helper delegation to `zava_forward.core.regulatory_eval_gates`.
* Out-of-band human threshold sign-off, external held-out legal benchmark, and live staff paired trial with authorised pricing.

## Handoff

* Ready for single post-implementation `rpi-review` at `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c2-review.md` (canonical mirror `.copilot-tracking/reviews/logs/2026-11-14/216-citation-eval-2142-c2-review.md` NOT created; single canonical path under `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c2-review.md` matching parent and `c1`).
