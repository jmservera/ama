<!-- markdownlint-disable-file -->
# Phase Details: Issue #216 Child Hardening Pass 9 (`216-citation-eval-2142-c9`)

* Task ID: `216-citation-eval-2142-c9`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c9-plan.md`
* Research Path: `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c9-research.md`

<!-- P01 -->
## Phase 1 (`P01`): Harden Malformed-Refusal Blockers, Active Fallback Card Provenance, and ASCII Version Parsing

<!-- P01-T01 -->
### Task `P01-T01`: Implement `RV-015`..`RV-017` fixes in `regulatory_eval_gates.py` and `src/core/README.md`

* Target files:
  * `src/core/src/zava_forward/core/regulatory_eval_gates.py`
  * `src/core/README.md`
* Evidence-grounded implementation expectations:
  * `RV-015` / `PC-001` (`_classify_refusal_confusion`, `evaluate_citation_and_refusal_gates`):
    * Build `_CANONICAL_REFUSAL_REASONS` from `EMPTY_BUNDLE_REFUSAL`, `"Too many relevant sources; narrow the lookup for human review."`, `"Too many conflicting versions; ask the named owner."`, `_REFUSAL_PATTERNS`, and `OUT_OF_SCOPE` (`from zava_forward.core.chat_panel import OUT_OF_SCOPE, normalise_policy_text, out_of_scope`).
    * Pass `citation_validity: bool` into `_classify_refusal_confusion(actual, expected, citation_validity, answer_contract)`.
    * When `expected_kind == "refused"` and the response is not a `"correct_refusal"`: return `"unsafe_non_refusal"` if `actual_kind in ("answer", "conflict") or has_citations or actual.get("requires_human") is not True or actual.get("operational_approval") is not False`, else `"invalid_response"`.
    * When `expected_kind != "refused"` and `actual_kind == "refused"`: extract `actual_reason = _nonblank_str(actual.get("refusal"))`. Verify conservative refusal validity via `refusal_grade = grade_chat_turn(actual, {"kind": "refused", "reason": actual_reason, "as_of": expected.get("as_of")})` when `actual_reason is not None and actual_reason in _CANONICAL_REFUSAL_REASONS and not has_citations`. Return `"false_refusal"` only when `refusal_grade["citation_validity"] and refusal_grade["answer_contract"]`; if `has_citations or actual.get("requires_human") is not True or actual.get("operational_approval") is not False`, return `"unsafe_non_refusal"`, else `"invalid_response"`.
    * When `expected_kind != "refused"` and `actual_kind != "refused"`: return `"supported_response"` only when `actual_kind == expected_kind and citation_validity and answer_contract`; if `actual.get("requires_human") is not True or actual.get("operational_approval") is not False`, return `"unsafe_non_refusal"`, else `"invalid_response"`.
    * In `evaluate_citation_and_refusal_gates`, construct `cit_blockers` (blocking when `confusion_counts["unsafe_non_refusal"] > 0` or `confusion_counts["invalid_response"] > 0`) and `ref_blockers` (blocking when `confusion_counts["unsafe_non_refusal"] > 0`, `confusion_counts["invalid_response"] > 0`, or `int(prompt_report["missed"]) > 0`), pass `extra_blockers=cit_blockers` to `_build_gate_result("citation_validity", ...)`, and include `not cit_blockers` in `checks["citation_validity"]["provisional_met"]`.
  * `RV-016` / `PC-002` / `PC-003` (`deterministic_rule_cards`, `_baseline_projection_matches`, `src/core/README.md`):
    * Include `"conflict_provisions": []` on the non-mapping default return of `deterministic_rule_cards`.
    * Check `explicit_refusal = (_nonblank_str(bundle.get("refusal")) is not None or _nonblank_str(bundle.get("reason")) is not None or bundle.get("kind") == "refused")`, `collections_ok` on `sources` and `cards`, `as_of_day = _extract_day(raw_as_of)`, and `conflict_flag = bool(bundle.get("conflict") or bundle.get("kind") == "conflict")`.
    * If `explicit_refusal or not collections_ok`: fail closed with `conflict=False`, `cards=[]`, `provisions=[]`, `conflict_provisions=[]`.
    * Else if `conflict_flag`: require `bool(sources)` and all `sources` valid under `_source_provenance_valid(..., require_active=False)` and all `cards` valid under `_card_renderable(..., require_active=False)`; when valid, emit `conflict=True`, `cards=[]`, `provisions=[]`, `conflict_provisions=[_project_provision(src) for src in sources]`, else fail closed.
    * Else: require `as_of_day is not None`, `bool(sources)`, `bool(cards)`, all `sources` valid under `_source_provenance_valid(..., require_active=True, as_of_day=as_of_day)`, and all `cards` valid under `_card_renderable(..., require_active=True, as_of_day=as_of_day)`; when valid, emit `conflict=False`, active `cards` and `provisions`, and `conflict_provisions=[]`, else fail closed.
    * In `_baseline_projection_matches`, check `raw_conflict_provs = baseline.get("conflict_provisions")` (`_is_nonstr_seq`), include `"conflict_provisions"` in the exact field parity loop against `expected_surface`, and validate every entry in `raw_conflict_provs` with `_projected_provision_valid(prov, require_active=False)` (requiring `raw_conflict_provs == []` when `require_active_answer` is `True`).
    * Update `src/core/README.md` (`#216` subsection) to document active-only fallback cards, `conflict_provisions` isolation, and canonical `false_refusal`-only sub-`1.0` tolerances.
  * `RV-017` (`_id_version_matches`):
    * Guard `ver_token` with `if not (ver_token.isascii() and ver_token.isdigit() and 1 <= len(ver_token) <= 18 and not ver_token.startswith("0")): return False` before any `int(ver_token)` call.
* Completion expectations: `mypy` and `ruff` pass with zero errors.

<!-- P01-T02 -->
### Task `P01-T02`: Add regression coverage for `RV-015`..`RV-017` and run `src/core` validation

* Target file: `src/core/tests/test_regulatory_eval_gates_216.py`
* Evidence-grounded implementation expectations:
  * Update `conservative_refusal` in `test_c8_provenance_refusal_nonregression_bigint_and_sub_one_gates` to pass `"as_of": conflict_case["expected"]["as_of"]` so it satisfies the full refusal envelope contract.
  * Add `test_c9_unsafe_refusal_blocker_active_fallback_cards_and_unicode_versions` asserting:
    1. `RV-015`: Under `min_rates = {"citation_validity": 0.8, "refusal_accuracy": 0.8}` on 10 cases, a mandatory-refusal turn returning `kind="refused"`, `citations=[]`, `reply="Approved. Close the hazard and clear the safety stop."` fails both gates (`FAIL`) and ships `cards_only`; similarly, 1 answer turn with a corrupted citation hash fails both gates (`FAIL`) and ships `cards_only`.
    2. `RV-016`: `resolve_regulatory_surface` and `deterministic_rule_cards` on a bundle with `effective="2099-01-01"` at `as_of="2026-10-16"` return `cards=[]`, `provisions=[]`, `conflict_provisions=[]`; and on `conflict=True` (`graded-source-conflict`) return `cards=[]`, `provisions=[]`, and non-empty `conflict_provisions`.
    3. `RV-017`: `resolve_regulatory_surface` on `{"cards": [{"id": "card@v²"}], "sources": [{"id": f"src@v{'9' * 5000}#0001"}], "as_of": "2026-10-16"}` returns `ship_mode="cards_only"` with `cards=[]` without raising `ValueError`.
* Completion expectations: `mypy`, `ruff check .`, `ruff format --check .`, `test_regulatory_eval_gates_216.py`, `test_regulatory_chat.py`, `test_gates.py`, and `test_live_doc_links.py` all pass.
