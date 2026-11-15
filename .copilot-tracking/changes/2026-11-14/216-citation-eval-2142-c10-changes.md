<!-- markdownlint-disable-file -->
# Changes Log: Issue #216 Child Hardening Pass 10 (`216-citation-eval-2142-c10`)

* Task ID: `216-citation-eval-2142-c10`
* Date: `2026-11-14`
* Status: `Completed`
* Plan Artifact: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c10-plan.md`

## Completed Work by Plan Marker

### Phase 1 (`P01`) — Completed

* `P01-T01`: Implemented `RV-018`..`RV-022` and `PC-001`..`PC-004` across `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, and `src/core/README.md`:
  * Added `_canonical_refusal_reason` and enforced exact unstripped `_is_utf8_str` membership in `_CANONICAL_REFUSAL_REASONS` across `grade_chat_turn` (both `citation_validity` and `answer_contract`), `_classify_refusal_confusion`, `evaluate_adversarial_prompts` (including agreement with `refuse_question` when canonical prompt obligation applies), and `evaluate_citation_and_refusal_gates` (including `dataset_gaps` when `expected["reason"]` is non-canonical and `invalid_response` promotion when a custom `refuse` callback returns malformed/non-canonical output).
  * Extracted `_active_cards_link_provisions` and `_inspect_bundle_surface` shared across `render_extractive_answer`, `deterministic_rule_cards`, and `_expected_from_bundle` (with matching active card-link and strict-JSON `source_freshness` checks in `grade_chat_turn`), unifying explicit-refusal triggers (`refusal`, `reason`, `kind == "refused"`, invalid `kind`), normalizing non-canonical or disagreeing refusal text to `EMPTY_BUNDLE_REFUSAL`, requiring whole-bundle `sources`/`facts`/`cards` provenance validity, and requiring active cards to carry verified `source_freshness["sources"]` links covering all active provisions.
  * Guarded `parsed.utcoffset()` and `parsed.astimezone(UTC)` in `_aware_dt` against `(OverflowError, ValueError)` and `_usage_valid` against `(ValueError, OverflowError, TypeError)`.
  * Guarded `self.render(snap)` and `offline_usage(...)` in `RegulatoryChat.surface` with `try ... except Exception` and strict `Mapping` / `str` envelope checks without mutating `rendered`.
  * Updated `src/core/README.md` to document unified whole-bundle validation, verified active card-to-provision linkage, canonical refusal enforcement, and UTC/render guards.
* `P01-T02`: Updated `forged_reason_cases` in `test_c9_unsafe_refusal_blocker_active_fallback_cards_and_unicode_versions` to mutate `actual` post-render (`PC-002`) and added `test_c10_canonical_refusals_bundle_parity_linked_cards_and_utc_overflow` in `src/core/tests/test_regulatory_eval_gates_216.py` covering `RV-018`..`RV-022` and `PC-001`..`PC-004`.

## Amendments and Divergences

* Local judgment (`grade_chat_turn` on `expected_kind == "refused"`): Also required canonical refusal reason agreement and empty `expected` `sources`/`facts`/`cards` inside `citations_ok` (`citation_validity`), aligning standalone `grade_chat_turn` with `answer_contract` and `_classify_refusal_confusion`.

## Validation Evidence

* `cd src/core && python3 -m mypy`: `Success: no issues found in 318 source files`.
* `cd src/core && python3 -m ruff check .`: `All checks passed!`.
* `cd src/core && python3 -m ruff format --check .`: `265 files already formatted`.
* `cd src/core && python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `Ran 13 tests in 16.553s — OK`.
* `cd src/core && PYTHONPATH="src:tests" python3 -m unittest test_regulatory_chat test_gates test_live_doc_links -q`: `Ran 58 tests in 33.493s — OK`.

## Remaining Work and Blockers

* Remaining in-scope `Pxx` / `Pxx-Txx` markers: None (`P01`, `P01-T01`, `P01-T02` complete).
* Blockers: None.
* Follow-up items: Cross-package `src/api` route wiring and `src/agents` helper deduplication remain outside `src/core`.
