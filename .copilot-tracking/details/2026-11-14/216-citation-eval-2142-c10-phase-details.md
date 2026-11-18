<!-- markdownlint-disable-file -->
# Phase Details: Issue #216 Child Hardening Pass 10 (`216-citation-eval-2142-c10`)

* Task ID: `216-citation-eval-2142-c10`
* Plan: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c10-plan.md`

<!-- P01 -->
## Phase 1 (`P01`): Unify Canonical Refusal Reasons, Whole-Bundle Linked Card Parity, and UTC/Surface Guards

<!-- P01-T01 -->
### Task `P01-T01`: Implement `RV-018`..`RV-022` in `regulatory_eval_gates.py`, `regulatory_chat.py`, and `src/core/README.md`

* Target files:
  * `src/core/src/zava_forward/core/regulatory_eval_gates.py`
  * `src/core/src/zava_forward/core/regulatory_chat.py`
  * `src/core/README.md`
* Evidence & completion expectations:
  * `_aware_dt` wraps both `parsed.utcoffset()` and `parsed.astimezone(UTC)` in `try ... except (OverflowError, ValueError): return None`; `_usage_valid` catches `(ValueError, OverflowError, TypeError)` around `offline_usage(...)` and returns `False`.
  * Extract `_active_cards_link_provisions(cards, sources)` and `_inspect_bundle_surface(bundle)` returning normalized `kind` (`"answer" | "conflict" | "refused"`), canonical `reason` (`str | None` constrained to exact unstripped `_is_utf8_str` membership in `_CANONICAL_REFUSAL_REASONS` with fallback `EMPTY_BUNDLE_REFUSAL`), `as_of`, `sources`, `facts`, `cards`, `projected_provisions`, `projected_cards`, and `conflict_provisions`:
    * Explicit refusal triggers when `bundle.get("refusal") is not None`, `bundle.get("reason") is not None`, `raw_kind == "refused"`, or `"kind" in bundle and not (raw_kind is None or (_is_utf8_str(raw_kind) and raw_kind in ("answer", "conflict", "refused")))`; canonical reason requires any present `refusal`/`reason` values to agree and belong to `_CANONICAL_REFUSAL_REASONS` (else `EMPTY_BUNDLE_REFUSAL`).
    * Whole-bundle collection check requires `sources`, `facts`, and `cards` (defaulting to `()`) to be non-string sequences of `Mapping`.
    * On `conflict_flag = bool(bundle.get("conflict") or (_is_utf8_str(raw_kind) and raw_kind == "conflict"))`: requires non-empty `sources` passing `_source_provenance_valid(..., require_active=False)`, `facts` passing `_fact_provenance_valid(..., require_active=False)`, and `cards` passing `_card_provenance_valid(..., require_active=False)` with `_is_strict_json_value(card.get("source_freshness"))`.
    * On active non-conflict (`conflict_flag == False`): requires `as_of_day is not None`, non-empty `sources` passing `_source_provenance_valid(..., require_active=True, as_of_day=as_of_day)`, `facts` passing `_fact_provenance_valid(..., require_active=True, as_of=as_of_str, as_of_day=as_of_day)`, non-empty `cards` passing `_card_provenance_valid(..., require_active=True, as_of_day=as_of_day)` with `_is_strict_json_value(card.get("source_freshness"))`, and `_active_cards_link_provisions(cards, projected_provisions)` verifying non-empty `source_freshness["sources"]` where every entry is a `Mapping` with an exact unstripped `_is_utf8_str` nonblank `source_id` matching at least one projected provision and covering all projected `provisions`; normalize `projected_cards` with `_to_plain_json(freshness)` and `[dict(prov) for prov in card_provisions]`.
    * Wire `deterministic_rule_cards`, `render_extractive_answer`, and `_expected_from_bundle` to `_inspect_bundle_surface(bundle)`, and enforce `_active_cards_link_provisions` in `grade_chat_turn` when `expected_kind == "answer"`.
  * In `grade_chat_turn`, `_classify_refusal_confusion`, `evaluate_adversarial_prompts`, and `evaluate_citation_and_refusal_gates`, require exact unstripped `_is_utf8_str` membership in `_CANONICAL_REFUSAL_REASONS`; classify missing or non-canonical `actual.get("refusal")` on `actual_kind == "refused"` as `"unsafe_non_refusal"`.
  * In `RegulatoryChat.surface`, wrap `self.render(snap)` and `offline_usage(...)` in `try ... except Exception: candidate_reply = None`, require `isinstance(rendered, Mapping)` with `_is_utf8_str(rendered.get("kind"))` (`in ("answer", "conflict", "refused")`) and `_is_utf8_str(rendered.get("as_of"))`, and build `candidate_reply = {**rendered, "usage": usage}` without mutating `rendered`.
  * Update `src/core/README.md` `#216` notes to document canonical refusal reason enforcement and unified whole-bundle linked-card projection parity.

<!-- P01-T02 -->
### Task `P01-T02`: Add `c10` regression tests in `test_regulatory_eval_gates_216.py` and run full `src/core` validation checks

* Target file: `src/core/tests/test_regulatory_eval_gates_216.py`
* Evidence & completion expectations:
  * Update `forged_reason_cases` in `test_c9_unsafe_refusal_blocker_active_fallback_cards_and_unicode_versions` to mutate `actual` post-render after `render_extractive_answer` normalizes non-canonical bundle refusals.
  * Add `test_c10_canonical_refusals_bundle_parity_linked_cards_and_utc_overflow` testing `RV-018`..`RV-022` and `PC-001`..`PC-004`.
  * Run `mypy`, `ruff check .`, `ruff format --check .`, `unittest discover -s tests -p 'test_*216*.py' -v`, and companion unit tests (`test_regulatory_chat`, `test_gates`, `test_live_doc_links`).
