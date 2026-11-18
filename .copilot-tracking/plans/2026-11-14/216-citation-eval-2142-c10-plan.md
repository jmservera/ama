<!-- markdownlint-disable-file -->
# Implementation Plan: Issue #216 Child Hardening Pass 10 (`216-citation-eval-2142-c10`)

* Task ID: `216-citation-eval-2142-c10`
* Parent Task ID: `216-citation-eval-2142-c9`
* Date: `2026-11-14`
* Status: `Finalized`

## Executive Summary

Resolve the five remaining in-scope `src/core` review findings (`RV-018`..`RV-022`) identified in `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c9-review.md`:
1. Require `_CANONICAL_REFUSAL_REASONS` for `correct_refusal` / `grade_chat_turn` as well as `false_refusal`, and coerce non-canonical bundle refusal strings to `EMPTY_BUNDLE_REFUSAL` (`RV-018`).
2. Share one unified bundle-validation helper `_inspect_bundle_surface(bundle)` across `deterministic_rule_cards`, `render_extractive_answer`, and `_expected_from_bundle` so explicit-refusal flags (`refusal`, `reason`, `kind == "refused"`, unknown `kind`) and whole-bundle `sources`/`facts`/`cards` validity never diverge (`RV-019`).
3. Fail closed (`cards=[], provisions=[]`) on `cards_only` fallback whenever any active card lacks `_card_provenance_valid(..., require_active=True)` or verified linked provisions covering `bundle["sources"]`, while retaining comparator `missing_link_case_ids` detection (`RV-020`).
4. Catch `OverflowError` during UTC conversion in `_aware_dt` and `_usage_valid` so extreme offset timestamps (`0001-01-01T00:00:00+14:00`, `9999-12-31T23:59:59-14:00`) fail closed without crashing (`RV-021`).
5. Guard `RegulatoryChat.surface` rendered-envelope fields and `offline_usage(...)` so malformed custom renderer outputs safely fall back to `cards_only` (`RV-022`).

## Sources

* `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c10-research.md`
* `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c9-review.md`
* `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* `src/core/src/zava_forward/core/regulatory_chat.py`
* `src/core/tests/test_regulatory_eval_gates_216.py`
* `src/core/README.md`

## User Decisions and Requirements

* Deliver all locally verifiable Issue #216 acceptance criteria strictly within `src/core`.
* Verify in `src/core` using bare `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*216*.py' -v`.
* Write all `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`), commit cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and do not push.

## Goals

* Close `RV-018`, `RV-019`, `RV-020`, `RV-021`, and `RV-022` in `src/core` with complete regression test coverage and updated `src/core/README.md` documentation.

## Scope and Non-Goals

* In scope: `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md`.
* Out of scope: `src/api` route changes and `src/agents` helper deduplication.

## Functional Requirements

* `FR-01` (`RV-018` + `PC-001`): Enforce exact unstripped `_is_utf8_str` membership in `_CANONICAL_REFUSAL_REASONS` across `grade_chat_turn`, `_classify_refusal_confusion` (classifying missing or non-canonical `actual.get("refusal")` on `actual_kind == "refused"` as `unsafe_non_refusal`), `evaluate_adversarial_prompts` (also verifying `(canon_reason is None or reason == canon_reason)`), and custom `refuse` callbacks in `evaluate_citation_and_refusal_gates`; coerce non-canonical or disagreeing bundle `refusal`/`reason` values to `EMPTY_BUNDLE_REFUSAL`.
* `FR-02` (`RV-019` + `RV-020` + `PC-003`): Extract `_inspect_bundle_surface(bundle)` shared across `deterministic_rule_cards`, `render_extractive_answer`, and `_expected_from_bundle`, enforcing identical explicit-refusal detection (non-`None` `refusal`/`reason`, `kind == "refused"`, or invalid `kind` outside `None | "answer" | "conflict" | "refused"` checked with `_is_utf8_str`), whole-bundle `sources`/`facts`/`cards` provenance validation (`_card_provenance_valid` + `_is_strict_json_value(freshness)` on both conflict and active cards), normalized `_to_plain_json(freshness)` card projection, and shared active card-to-provision link coverage across `_inspect_bundle_surface` and `grade_chat_turn`.
* `FR-03` (`RV-021` + `PC-004`): Wrap both `parsed.utcoffset()` and `parsed.astimezone(UTC)` in `try ... except (OverflowError, ValueError): return None` inside `_aware_dt`, and catch `(ValueError, OverflowError, TypeError)` in `_usage_valid`.
* `FR-04` (`RV-022` + `PC-004`): Guard `self.render(snap)` and `offline_usage(...)` in `RegulatoryChat.surface` with `try ... except Exception: candidate_reply = None`, require `isinstance(rendered, Mapping)` with `type(rendered.get("kind")) is str` (`in ("answer", "conflict", "refused")`) and `type(rendered.get("as_of")) is str`, and construct `candidate_reply = {**rendered, "usage": usage}` without mutating `rendered`.
* `FR-05` (`PC-002`): Update `src/core/README.md`, adjust `forged_reason_cases` in `test_c9_unsafe_refusal_blocker_active_fallback_cards_and_unicode_versions` to mutate `actual` post-render once `render_extractive_answer` normalizes non-canonical bundle refusals, and add 1 regression test (`test_c10_canonical_refusals_bundle_parity_linked_cards_and_utc_overflow`) in `src/core/tests/test_regulatory_eval_gates_216.py` (exact removals: `none`; max test additions: `1`).

## Non-Functional Requirements

* Zero `mypy` errors across `src/core`, clean `ruff check .` and `ruff format --check .`, zero `.copilot-tracking/` strings in `src/`.

## Acceptance Criteria

* Non-canonical expected/actual refusal reason (`"Approved..."`) fails `grade_chat_turn` and blocks both gates at `min_rates=1.0` and `0.8`, and `render_extractive_answer` coerces non-canonical `bundle["refusal"]` to `EMPTY_BUNDLE_REFUSAL`.
* `facts=[{}]` causes `deterministic_rule_cards`, `render_extractive_answer`, and `_expected_from_bundle` to fail closed identically; `reason="Refused"` or `kind="refused"` refuses across all three; active cards whose `source_freshness["sources"]` match no provision fail closed (`cards=[], provisions=[]`) while comparator `missing_link_case_ids` detection remains intact.
* `as_of="0001-01-01T00:00:00+14:00"` and `9999-12-31T23:59:59-14:00` fail closed without `OverflowError`, and `RegulatoryChat.surface` with a custom renderer returning `{}` returns `ship_mode="cards_only"` without raising `KeyError`.

## Phase Checklist

<!-- P01 -->
### [x] Phase 1 (`P01`): Unify Canonical Refusal Reasons, Whole-Bundle Linked Card Parity, and UTC/Surface Guards

<!-- P01-T01 -->
* [x] `P01-T01`: Implement `RV-018`..`RV-022` in `regulatory_eval_gates.py`, `regulatory_chat.py`, and `src/core/README.md`.

<!-- P01-T02 -->
* [x] `P01-T02`: Add `c10` regression tests in `test_regulatory_eval_gates_216.py` and run full `src/core` validation checks.

## Critique Disposition

* Critique artifact: `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c10-plan-critique.md` (`Complete`, `Revise`).
* `PC-001` (High, direct planner correction — Applied): Enforced exact unstripped `_is_utf8_str` `_CANONICAL_REFUSAL_REASONS` checks across `evaluate_adversarial_prompts`, custom `refuse` callbacks in `evaluate_citation_and_refusal_gates`, `grade_chat_turn`, and `_classify_refusal_confusion`.
* `PC-002` (High, direct planner correction — Applied): Updated `FR-05` and `P01-T02` to mutate `actual` post-render in `forged_reason_cases` (`test_c9`) after `render_extractive_answer` normalizes non-canonical bundle refusals.
* `PC-003` (Medium, direct planner correction — Applied): Specified `_is_utf8_str` `kind`/`source_id` checks, non-`None` `refusal`/`reason` triggers, `_card_provenance_valid` + `_is_strict_json_value(freshness)` + `_to_plain_json(freshness)` on both conflict and active cards, and shared active card-link validation in `grade_chat_turn`.
* `PC-004` (Medium, direct planner correction — Applied): Wrapped `utcoffset()` + `astimezone(UTC)` in `_aware_dt`, caught `(ValueError, OverflowError, TypeError)` in `_usage_valid`, and guarded custom `self.render(snap)` exceptions and immutable `Mapping` returns in `RegulatoryChat.surface`.

## Follow-Up Items

* Cross-package `src/api` route wiring (`RegulatoryChat.surface`) and `src/agents` helper deduplication remain distinct follow-ups outside `src/core`.
