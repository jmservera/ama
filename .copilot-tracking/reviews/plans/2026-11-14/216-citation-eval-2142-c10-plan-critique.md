<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #216 Child Hardening Pass 10 (`216-citation-eval-2142-c10`)

## Metadata

* Task ID: 216-citation-eval-2142-c10
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c10-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c10-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Single-pass plan critique for `216-citation-eval-2142-c10` closing the five remaining in-scope `src/core` review defects (`RV-018`..`RV-022`) from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c9-review.md` strictly inside `src/core`.
* Research and evidence considered: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c10-plan.md`, `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c10-phase-details.md`, `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c10-research.md`, `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c9-review.md`, `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, and `src/core/tests/test_regulatory_eval_gates_216.py`.
* Decisions, dependencies, and acceptance criteria considered: Enforce `_CANONICAL_REFUSAL_REASONS` across refused grading, confusion classification, and bundle normalization (`RV-018`); unify whole-bundle validation and active card-to-provision linkage across `deterministic_rule_cards`, `render_extractive_answer`, and `_expected_from_bundle` (`RV-019`, `RV-020`); fail closed on UTC conversion `OverflowError` (`RV-021`); degrade malformed custom renderer outputs in `RegulatoryChat.surface` to `cards_only` (`RV-022`); preserve `src/core` `mypy`, `ruff`, and unit test gates.
* Assessment boundary: Evaluates plan completeness, edge-case soundness, and test compatibility across the supplied `src/core` modules and `c9`/`c10` tracking artifacts; out-of-scope `src/api` route wiring and `src/agents` deduplication remain excluded per caller boundary.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| `FR-01` / `C1` / `RV-018`                | Partial  | Covers `grade_chat_turn`, `_classify_refusal_confusion`, and bundle coercion, but misses `evaluate_adversarial_prompts` and custom `refuse` callback canonical checks (`PC-001`) plus an immediate `test_c9` fixture break (`PC-002`). |
| `FR-02` / `C2` / `C3` / `RV-019`..`020`  | Partial  | Covers unified `_inspect_bundle_surface` extraction and active card linkage, but leaves non-`str` `kind` / non-`None` blank refusal handling, conflict `_card_provenance_valid` vs `grade_chat_turn`, `grade_chat_turn` active link parity, and `source_freshness` JSON/copy hygiene underspecified (`PC-003`). |
| `FR-03` / `C4` / `RV-021`                | Partial  | Catches `OverflowError` on `parsed.astimezone(UTC)` and `offline_usage(...)`, but leaves `parsed.utcoffset()` outside the `try` block in `_aware_dt` and omits `TypeError` in `_usage_valid` (`PC-004`). |
| `FR-04` / `C5` / `RV-022`                | Partial  | Checks `Mapping` and string `kind`/`as_of` in `RegulatoryChat.surface`, but does not guard exceptions raised by custom `self.render(snap)`, immutable `Mapping` returns on `rendered["usage"] = ...`, or `str` subclasses (`PC-004`). |
| `FR-05` / `P01-T01` / `P01-T02`          | Partial  | Adds `test_c10_...` and `src/core/README.md` updates, but `FR-05` omits the required post-render mutation adjustment to `forged_reason_cases` in `test_c9` (`PC-002`). |

## Verdict

* Verdict: Revise
* Rationale: The single-phase architecture and `_inspect_bundle_surface` consolidation directly target `RV-018`..`RV-022`, but four direct planner-owned refinements (`PC-001`..`PC-004`) are needed before implementation to close a standalone adversarial `refuse` callback bypass, prevent an immediate `test_c9` regression once `render_extractive_answer` coerces non-canonical bundle refusals, align `_inspect_bundle_surface` with `grade_chat_turn` and strict JSON card projection, and harden `RegulatoryChat.surface` against custom renderer exceptions and immutable mappings.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Enforce canonical refusal reasons on `evaluate_adversarial_prompts` and custom `refuse` callbacks, and avoid whitespace-stripping drift

* Related IDs: `FR-01`, `C1`, `RV-018`, `P01-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`evaluate_adversarial_prompts` lines 1505-1536, `evaluate_citation_and_refusal_gates` lines 1805-1812, `grade_chat_turn` lines 1351-1365, `_classify_refusal_confusion` lines 1422-1449); `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c10-phase-details.md` (`P01-T01`)
* Concern: `P01-T01` adds `_CANONICAL_REFUSAL_REASONS` checks to `grade_chat_turn`, `_classify_refusal_confusion`, and `_inspect_bundle_surface`, yet `evaluate_adversarial_prompts` (line 1516: `passed = valid_prompt and _nonblank_str(reason) is not None`) and `caller_refusal_malformed` in `evaluate_citation_and_refusal_gates` (line 1808) still accept any non-blank string from a custom `refuse` callback. A custom `refuse` callback returning `"Approved: home is compliant"` on standalone `ADVERSARIAL_PROMPTS` (or on prompts where `refuse_question` returns `None`) still scores `passed = True` (`missed = 0`, `rate = 1.0`). In addition, `_nonblank_str` strips leading/trailing whitespace before checking `_CANONICAL_REFUSAL_REASONS`, and `_classify_refusal_confusion` must keep malformed `expected["reason"]` with a valid canonical `actual` refusal as `"invalid_response"` while classifying any non-canonical `actual.get("refusal")` on `actual_kind == "refused"` as `"unsafe_non_refusal"`.
* Impact: Standalone adversarial prompt evaluation and custom `refuse` callbacks could report `1.0` refusal accuracy on non-canonical approval strings, or accept padded refusal fields.
* Smallest useful change: Update `FR-01` and `P01-T01` so `evaluate_adversarial_prompts` requires `_is_utf8_str(reason) and reason in _CANONICAL_REFUSAL_REASONS` and `(canon_reason is None or reason == canon_reason)` against `canon_reason = refuse_question(prompt)`; `evaluate_citation_and_refusal_gates` sets `caller_refusal_malformed = True` whenever `raw_caller_refusal is not None` and not `(_is_utf8_str(raw_caller_refusal) and raw_caller_refusal in _CANONICAL_REFUSAL_REASONS)`; and `grade_chat_turn` / `_classify_refusal_confusion` validate exact unstripped `_is_utf8_str` membership in `_CANONICAL_REFUSAL_REASONS` (returning `"unsafe_non_refusal"` whenever `actual_kind == "refused"` has a missing or non-canonical `actual.get("refusal")`).
* Action owner: planning_parent
* Exact resolving evidence: Revised `FR-01` and `P01-T01`/`P01-T02` specifying canonical `refuse` callback enforcement in `evaluate_adversarial_prompts` and `evaluate_citation_and_refusal_gates`, exact unstripped `_CANONICAL_REFUSAL_REASONS` checks, and an assertion in `test_c10_...` covering a custom `refuse` returning `"Approved..."`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Authorize updating `forged_reason_cases` in `test_c9` where `render_extractive_answer` was used to fabricate a non-canonical `actual` refusal

* Related IDs: `FR-01`, `FR-05`, `RV-018`, `P01-T01`, `P01-T02`
* Evidence: `src/core/tests/test_regulatory_eval_gates_216.py` (`test_c9_unsafe_refusal_blocker_active_fallback_cards_and_unicode_versions` lines 2128-2148); `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c10-plan.md` (`FR-01`, `FR-05`)
* Concern: Lines 2130-2136 of `src/core/tests/test_regulatory_eval_gates_216.py` construct a forged non-canonical `actual` chat envelope on 1 of 10 cases under `min_rates=0.8` by calling `render_extractive_answer({"sources": [], "cards": [], "as_of": conflict_turn["expected"]["as_of"], "refusal": "Approved: home is compliant; close the hazard."})` and then assert `citation_validity == FAIL`, `refusal_accuracy == FAIL`, and `false_refusal == 0` (lines 2143-2147). Once `FR-01` coerces non-canonical `bundle["refusal"]` strings to `EMPTY_BUNDLE_REFUSAL` inside `render_extractive_answer`, that call produces a valid canonical `EMPTY_BUNDLE_REFUSAL` envelope instead of a forged `actual` turn, grading as 1 conservative `false_refusal` (`rate = 0.9 >= 0.8`) and causing all three assertions at lines 2143-2147 to fail.
* Impact: Implementing `FR-01` as written breaks `test_c9_unsafe_refusal_blocker_active_fallback_cards_and_unicode_versions` while `FR-05` only mentions adding `test_c10_...`.
* Smallest useful change: Update `FR-05` and `P01-T02` to authorize adjusting `forged_reason_cases` in `test_c9_unsafe_refusal_blocker_active_fallback_cards_and_unicode_versions` (`src/core/tests/test_regulatory_eval_gates_216.py` lines 2130-2136) so it renders a canonical refusal envelope first and then mutates `actual["refusal"]`, `actual["sections"]["unknown_or_conflict"]`, and `actual["reply"]` post-render to `"Approved: home is compliant; close the hazard."` (keeping zero test removals and 1 new test method).
* Action owner: planning_parent
* Exact resolving evidence: Revised `FR-05` and `P01-T02` explicitly specifying the post-render mutation adjustment in `test_c9_unsafe_refusal_blocker_active_fallback_cards_and_unicode_versions` alongside the new `test_c10_...` test.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Close `_inspect_bundle_surface` parity gaps on non-`str` `kind`, malformed non-`None` refusal markers, conflict card provenance, `source_freshness` JSON copying, and `grade_chat_turn` active link checks

* Related IDs: `FR-02`, `C2`, `C3`, `RV-019`, `RV-020`, `P01-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (lines 649-767, 824-916, 1126-1141, 1273-1286, 2394-2500, 3080-3145); `src/core/src/zava_forward/core/regulatory_chat.py` (line 294); `src/core/tests/test_regulatory_eval_gates_216.py` (lines 1533-1540); `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c10-phase-details.md` (`P01-T01`)
* Concern: Four boundary mismatches remain in the `P01-T01` design of `_inspect_bundle_surface`: (1) `bundle.get("kind") not in (None, "answer", "conflict", "refused")` without `_is_utf8_str` can be bypassed by custom `__eq__` objects (such as `_EqualsAnswer` in `test_regulatory_eval_gates_216.py`) or `str` subclasses, and checking only `_nonblank_str(bundle.get("refusal")) is not None` ignores non-`None` blank, boolean, numeric, or surrogate `refusal`/`reason` values instead of refusing with `EMPTY_BUNDLE_REFUSAL`; (2) on `conflict_flag = True` with non-empty conflicting `cards` (`RegulatoryChat.bundle` signature conflict at `regulatory_chat.py:294`), `P01-T01` checks `_card_renderable(..., require_active=False)` (allowing `source_freshness=None`) whereas `grade_chat_turn` (line 1276) requires `_card_provenance_valid(..., require_active=False)` (rejecting `source_freshness=None`); (3) on `expected_kind == "answer"`, `grade_chat_turn` (lines 1273-1286) does not enforce the `RV-020` active card-to-source linkage check on `expected_cards` and `actual_cards_seq`, allowing standalone gate runs to pass unlinked active cards that `_inspect_bundle_surface` refuses; and (4) `projected_cards` uses shallow `dict(freshness)` and shared provision dicts without checking `_is_strict_json_value(freshness)` or normalizing via `_to_plain_json(freshness)` and `[dict(prov) for prov in card_provisions]`.
* Impact: Edge-case bundles with non-`str` `kind`, blank/non-string refusal markers, `source_freshness=None` conflict cards, non-JSON `source_freshness` payloads, or standalone unlinked `grade_chat_turn` inputs can diverge between rendering, card projection, and grading.
* Smallest useful change: Refine `P01-T01` so `_inspect_bundle_surface`: (1) triggers explicit refusal whenever `bundle.get("refusal") is not None`, `bundle.get("reason") is not None`, `raw_kind == "refused"`, or `"kind" in bundle and not (raw_kind is None or (_is_utf8_str(raw_kind) and raw_kind in ("answer", "conflict", "refused")))`, coercing any non-canonical or disagreeing `refusal`/`reason` to `EMPTY_BUNDLE_REFUSAL`; (2) requires `_card_provenance_valid` with `_is_strict_json_value(freshness)` on both conflict (`require_active=False`) and active (`require_active=True`) cards; (3) normalizes `projected_cards` with `_to_plain_json(freshness)`, `[dict(prov) for prov in card_provisions]`, and exact unstripped `_is_utf8_str` `source_id` matching; and (4) shares the active card-to-provision link coverage predicate with `grade_chat_turn` when `expected_kind == "answer"`.
* Action owner: planning_parent
* Exact resolving evidence: Revised `FR-02` and `P01-T01`/`P01-T02` incorporating strict `_is_utf8_str` `kind`/`source_id` checks, non-`None` `refusal`/`reason` refusal triggers, unified `_card_provenance_valid` + `_is_strict_json_value(freshness)` + `_to_plain_json(freshness)` projection, and shared active card-link validation in `grade_chat_turn`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Guard custom renderer exceptions, immutable `Mapping` returns, and `utcoffset()` overflow across `RegulatoryChat.surface`, `_aware_dt`, and `_usage_valid`

* Related IDs: `FR-03`, `FR-04`, `C4`, `C5`, `RV-021`, `RV-022`, `P01-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_chat.py` (`RegulatoryChat.surface` lines 461-466); `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_aware_dt` lines 576-588, `_usage_valid` lines 1167-1176); `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c10-phase-details.md` (`P01-T01`)
* Concern: `P01-T01` guards `isinstance(rendered, Mapping)`, string `kind`/`as_of`, and `(ValueError, OverflowError)` around `offline_usage(...)` in `RegulatoryChat.surface`, but leaves `self.render(snap)` unguarded if a custom renderer raises an exception (`RuntimeError`, `KeyError`, `TypeError`, `ValueError`), mutates `rendered["usage"] = ...` in place (raising `TypeError` on immutable `MappingProxyType` returns or mutating caller state), and accepts `str` subclasses if checked with `isinstance(..., str)` instead of `type(...) is str`. Additionally, `_aware_dt` calls `parsed.utcoffset()` before `parsed.astimezone(UTC)`, so an `OverflowError` or `ValueError` raised inside `utcoffset()` would escape if only `astimezone(UTC)` is wrapped, and `_usage_valid` does not catch `TypeError` alongside `(ValueError, OverflowError)`.
* Impact: Custom renderers that raise or return read-only mappings, or extreme/custom `tzinfo` offsets in `_aware_dt`, can still raise uncaught exceptions instead of failing closed to `cards_only` / `None`.
* Smallest useful change: Refine `FR-03`, `FR-04`, and `P01-T01` so `_aware_dt` wraps both `parsed.utcoffset()` and `parsed.astimezone(UTC)` in `try ... except (OverflowError, ValueError): return None`; `_usage_valid` catches `(ValueError, OverflowError, TypeError)`; and `RegulatoryChat.surface` wraps `self.render(snap)` and `offline_usage(...)` in `try ... except Exception: candidate_reply = None`, checks `isinstance(rendered, Mapping)` with `type(rendered.get("kind")) is str` (`in ("answer", "conflict", "refused")`) and `type(rendered.get("as_of")) is str`, and assigns `candidate_reply = {**rendered, "usage": usage}` without mutating `rendered` in place.
* Action owner: planning_parent
* Exact resolving evidence: Revised `FR-03`, `FR-04`, and `P01-T01`/`P01-T02` specifying full `try` coverage in `_aware_dt`, `(ValueError, OverflowError, TypeError)` in `_usage_valid`, exception-safe immutable-copy handling in `RegulatoryChat.surface`, and regression coverage in `test_c10_...`.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Extracting `_inspect_bundle_surface(bundle)` eliminates the root cause of three-way drift across `deterministic_rule_cards`, `render_extractive_answer`, and `_expected_from_bundle` while keeping `_baseline_projection_matches` (`missing_link_case_ids` on `unmapped_bundle`) and conflict `expected` dicts (`kind="conflict"` without `"conflict": True`) intact.
* Catching `OverflowError` on valid ISO-8601 extreme-offset timestamps (`0001-01-01T00:00:00+14:00`, `9999-12-31T23:59:59-14:00`) cleanly protects `_extract_day`, `authorise_model_run`, `cost_per_accepted_check`, `compare_chat_against_rule_cards`, and `RegulatoryChat.surface`.
* Residual risk (explicitly accepted out-of-scope boundary): Cross-package `src/api` route wiring and `src/agents` helper deduplication remain tracked follow-ups outside the caller-bounded `src/core` deliverable.

## Questions or Blocking Evidence Gaps

* None. All four findings (`PC-001`..`PC-004`) are deterministic planner-owned refinements fully resolved by the supplied `src/core` source and test artifacts.

## Limitations

* Critique is strictly bounded to the supplied `c9`/`c10` tracking artifacts and `src/core` files (`regulatory_eval_gates.py`, `regulatory_chat.py`, `test_regulatory_eval_gates_216.py`); no source, test, or plan files were modified and no external packages were inspected.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Revise `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c10-plan.md` and `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c10-phase-details.md` directly to incorporate `PC-001`..`PC-004`, mark the plan `Final`, and proceed to `rpi-implement` without a second critique pass.
* User response required: No
