# Implementation Plan: Child Hardening Pass 12 for Issue #216 (`RV-026`..`RV-029`)

* Task ID: `216-citation-eval-2142-c12`
* Date: `2026-11-14`
* Status: `Finalized`

## Executive Summary

Resolve the four remaining in-scope `src/core` findings (`RV-026`..`RV-029`) recorded in `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c11-review.md` together with single-pass critique refinements (`PC-001`..`PC-003`):
1. Enforce single `(safe_default, clock)` signature agreement across active cards in `_active_bundle_nonconflicting` with explicit `Mapping` and `_nonblank_str` (`type(v) is str`) guards before hashing so malformed or unhashable card fields fail closed instead of raising `TypeError` (`RV-026`, `PC-001`).
2. Validate aggregate `source_freshness["status"]` (`"in_cadence" | "out_of_cadence" | "unknown"`), mandatory nonblank `label` with exact `out_of_cadence` label biconditional, optional `as_of` day agreement, constituent `source_freshness["sources"]` status/`due_on`/`last_success`/`cadence_days` parity, cross-card and source-`currentness` consistency (including `"currentness"` in `_source_matches`), and strict boolean / omitted-key `expect_out_of_cadence` parity across both `citation_validity` and `answer_contract` in `grade_chat_turn` (`RV-027`, `PC-001`, `PC-002`).
3. Enforce canonical `refuse_question(question.strip()) or refuse_question(masked)` directly inside `RegulatoryChat.surface` so the shipped surface cannot bypass the evaluated refusal policy when a permissive `self.refuse` callback is injected (`RV-028`).
4. Align `multi_bundle`'s two synthetic cards on one `(safe_default, clock)` signature, isolate `v2_source["link"]` in `test_c11`, and add `test_c12_card_signature_conflict_freshness_consistency_and_surface_refusal_policy` covering both `comparison=None` and verified `comparison=positive_cmp` surface refusal paths (`RV-029`, `PC-003`).

## Sources

* `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c11-review.md`
* `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c12-research.md`

## User Decisions and Requirements

* Deliver all locally verifiable Issue #216 acceptance criteria strictly inside `src/core` (`src/api` and `src/agents` remain out of scope).
* Verify in `src/core` with bare `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*216*.py' -v`.
* Keep `.copilot-tracking/` references out of production code, tests, docs, and commit messages.

## Goals

* Reject unflagged `conflict=False` bundles whose active cards disagree on `(safe_default, clock)`.
* Reject cards whose aggregate `source_freshness` contradicts constituent `source_freshness["sources"]` statuses/due dates, omits the mandatory `out_of_cadence` label, or contradicts bundle-level staleness.
* Enforce `refuse_question` inside `RegulatoryChat.surface` before returning either `chat` or actionable `rule_cards`.
* Maintain 100% isolated regression coverage in `test_regulatory_eval_gates_216.py`.

## Scope and Non-Goals

* In scope: `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md`.
* Out of scope: `src/api`, `src/agents`, and overriding injectable `self.refuse` in `RegulatoryChat.ask` / `RegulatoryChat.bundle` unit-test seams.

## Functional Requirements

* `FR-01` (`RV-026`, `PC-001`): In `_active_bundle_nonconflicting`, check `isinstance(card, Mapping)`, `_nonblank_str(card.get("safe_default")) is not None`, and `_nonblank_str(card.get("clock")) is not None` before inserting `(card["safe_default"], card["clock"])` into `signatures`, and return `False` when any check fails or `len(signatures) > 1`.
* `FR-02` (`RV-027`, `PC-001`, `PC-002`):
  * In `_card_provenance_valid`, require `freshness["status"] in ("in_cadence", "out_of_cadence", "unknown")`; require `_nonblank_str(freshness.get("label")) is not None` with `(freshness.get("label") == OUT_OF_CADENCE_LABEL) == (freshness["status"] == "out_of_cadence")`; validate optional `"as_of"` on `freshness` and constituent entries via `_extract_day` (`== as_of_day` when `require_active and as_of_day is not None`); validate `freshness["sources"]` unconditionally as a non-empty `_is_nonstr_seq` of `Mapping` with unique nonblank unstripped `_is_utf8_str` `source_id`s; require uniform `"status"` key presence across constituent entries when any entry specifies `"status"` and enforce `card_freshness` status aggregation (`"out_of_cadence"` if any constituent is `"out_of_cadence"` or has valid `due_on <= as_of_day`; `"in_cadence"` only if all present constituent statuses are `"in_cadence"` and valid `due_on > as_of_day`; `"unknown"` forbids any `"out_of_cadence"` constituent or valid `due_on <= as_of_day`); require `entry.get("status") in (None, "unknown")` whenever `"due_on" in entry and entry["due_on"] is None`; and validate optional `"last_success"` (`None` or valid ISO day, `<= as_of_day` when active) and `"cadence_days"` (`None` or `_strict_int` in `1..36600`), requiring `due_on is None` and `status in (None, "unknown")` when either is `None` and exact `due_on == (date.fromisoformat(last_success) + timedelta(days=cadence_days)).isoformat()` when both are set.
  * In `_active_bundle_nonconflicting`, guard `source_freshness`, `sources`, and constituent fields (`status`, `due_on`, `last_success`) with `Mapping` / `_is_nonstr_seq` / `None | _is_utf8_str` checks before hashing, reject cross-card disagreements on `(status, due_on, last_success)` for the same `source_id`, and enforce constituent-level parity whenever `src.get("currentness") in ("in_cadence", "out_of_cadence", "unknown")` (requiring any referencing constituent `entry` with `"status"` to equal `src["currentness"]` and requiring card aggregate `status == "out_of_cadence"` when `src["currentness"] == "out_of_cadence"`). Add `"currentness"` to `_source_matches` `required_keys`.
  * In `grade_chat_turn` (`expected_kind == "answer"`), validate `"expect_out_of_cadence"` strictly when present (`type(expected["expect_out_of_cadence"]) is bool and expected["expect_out_of_cadence"] == exp_stale_card_present`), default `expect_stale = exp_stale_card_present` when `"expect_out_of_cadence" not in expected`, and gate both `cards_prov_ok` (`citation_validity`) and `safe_fields_ok` (`answer_contract`) on `exp_expect_stale_ok and exp_stale_card_present == stale_card_present`.
* `FR-03` (`RV-028`): Import `refuse_question` in `src/core/src/zava_forward/core/regulatory_chat.py` and in `RegulatoryChat.surface`, check `canonical_refusal = refuse_question(question.strip()) or refuse_question(masked)`; when non-`None`, construct a canonical refused bundle (`sources=[]`, `facts=[]`, `cards=[]`, `as_of=self.clock().isoformat(timespec="seconds")`, `conflict=False`, `refusal=canonical_refusal`) so neither `chat` nor actionable `rule_cards` can be returned on a prohibited prompt even if `self.refuse` is permissive.
* `FR-04` (`RV-029`, `PC-003`): Update `multi_bundle` (`card-alpha@v1` and `card-beta@v1` sharing one `(safe_default, clock)`), fix `v2_source["link"]` in `test_c11`, update `src/core/README.md`, and add 1 regression test (`test_c12_card_signature_conflict_freshness_consistency_and_surface_refusal_policy`) in `src/core/tests/test_regulatory_eval_gates_216.py` covering both `comparison=None` and `comparison=positive_cmp` on `RegulatoryChat.surface` (exact removals: `none`; max test additions: `1`).

## Non-Functional Requirements

* Zero `mypy`, `ruff check`, or `ruff format --check` diagnostics in `src/core`.
* Preserve all 14 existing tests in `test_regulatory_eval_gates_216.py` and all 58 companion tests (`test_regulatory_chat`, `test_gates`, `test_live_doc_links`).

## Acceptance Criteria

* Two active cards with divergent `clock` or `safe_default` on a `conflict=False` bundle fail closed in `render_extractive_answer`, `deterministic_rule_cards`, and `grade_chat_turn` (`citation_validity` and `answer_contract`).
* A card claiming `source_freshness["status"] == "in_cadence"` (or `"unknown"`) while a constituent source has `status == "out_of_cadence"` or `due_on <= as_of_day` (or omitting the mandatory `out_of_cadence` label) fails closed in `render_extractive_answer`, `deterministic_rule_cards`, and `grade_chat_turn`.
* `RegulatoryChat.surface` initialized with a permissive `lambda _q: None` refusal callback still refuses prohibited questions (returning `cards == []` and no `answer` chat envelope).
* `v2_source` in `test_c11` carries `/api/law/provisions/synthetic%40v2%230001` so `unflagged_v1_v2` isolates `_active_bundle_nonconflicting`.

## Phase Checklist

<!-- P01 -->
### [x] Phase 1 (`P01`): Card-Signature Conflict, Freshness Aggregate Parity, and Surface Refusal Enforcement

<!-- P01-T01 -->
* [x] `P01-T01`: Implement `RV-026`..`RV-028` in `regulatory_eval_gates.py`, `regulatory_chat.py`, and `src/core/README.md`.

<!-- P01-T02 -->
* [x] `P01-T02`: Apply `RV-029` fixture updates, add `test_c12_card_signature_conflict_freshness_consistency_and_surface_refusal_policy` in `test_regulatory_eval_gates_216.py`, and run all `src/core` checks.

## Critique Disposition

Single-pass critique executed at `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c12-plan-critique.md` (`Complete`, verdict `Revise`, `0 Critical, 2 High, 1 Medium, 0 Low`):

* `PC-001` [High] (`direct_planner_correction` — Applied): Added explicit `Mapping`, `_is_nonstr_seq`, `_nonblank_str` (`type(v) is str`), and `None | _is_utf8_str` guards in `_active_bundle_nonconflicting` before hashing `(safe_default, clock)` or constituent `(status, due_on, last_success)` tuples, plus unhashable card-field regression cases in `P01-T02`.
* `PC-002` [High] (`direct_planner_correction` — Applied): Expanded `FR-02` and `P01-T01`/`P01-T02` to enforce nonblank `label` with exact `out_of_cadence` biconditional, optional `as_of` day checks, `due_on=None` -> `status in (None, "unknown")`, `last_success` + `cadence_days` arithmetic parity, constituent-level `src["currentness"]` parity + `"currentness"` in `_source_matches`, and strict boolean / omitted-key `expect_out_of_cadence` validation across both `citation_validity` and `answer_contract`.
* `PC-003` [Medium] (`direct_planner_correction` — Applied): Updated `FR-04` and `P01-T02` so `test_c12` asserts `RegulatoryChat.surface` refusal on a purpose-matching prohibited prompt under both `comparison=None` (`ship_mode == "cards_only"`, `chat is None`, `rule_cards["cards"] == []`) and verified `comparison=positive_cmp` (`ship_mode == "chat_with_cards"`, `chat["kind"] == "refused"`, `rule_cards["cards"] == []`).

## Follow-Up Items

* Cross-package `src/api` route wiring (`RegulatoryChat.surface`) and `src/agents` helper deduplication remain distinct follow-ups outside `src/core`.
