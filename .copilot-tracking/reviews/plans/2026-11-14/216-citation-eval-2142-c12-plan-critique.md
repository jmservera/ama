<!-- markdownlint-disable-file -->
# RPI Plan Critique: Child Hardening Pass 12 for Issue #216 (`RV-026`..`RV-029`)

## Metadata

* Task ID: `216-citation-eval-2142-c12`
* Critique date: `2026-11-14`
* Plan: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c12-plan.md`
* Phase details: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c12-phase-details.md`
* Critique execution status: `Complete`

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver locally verifiable Issue #216 acceptance criteria strictly inside `src/core` (`src/api` and `src/agents` remain out of scope; `RegulatoryChat.ask` and `RegulatoryChat.bundle` retain injectable `self.refuse` unit-test seams while `RegulatoryChat.surface` is the shipping surface selector) to close `RV-026`..`RV-029` without `.copilot-tracking/` references in production code, tests, docs, or commit messages.
* Research and evidence considered: `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c11-review.md`, `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c12-research.md`, `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c12-plan.md`, `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c12-phase-details.md`, `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/src/zava_forward/core/source_monitor.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md`.
* Decisions, dependencies, and acceptance criteria considered: Active-card `(safe_default, clock)` signature conflict parity (`RV-026`), `source_freshness` aggregate/constituent/label/bundle-currentness and `expect_out_of_cadence` grading parity (`RV-027`), canonical `refuse_question` enforcement in `RegulatoryChat.surface` (`RV-028`), isolated `multi_bundle` and `v2_source["link"]` test fixtures plus one `test_c12_...` addition (`RV-029`), and `src/core` validation (`mypy`, `ruff check .`, `ruff format --check .`, and `unittest` suites).
* Assessment boundary: Evaluates completeness, fail-closed safety, and test accuracy against the supplied `src/core` codebase and `RV-026`..`RV-029`; cross-package `src/api` route wiring and `src/agents` helper deduplication are excluded per caller boundary.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| `FR-01` / `C1` (`RV-026`) | Partial | Captures `(safe_default, clock)` cardinality in `_active_bundle_nonconflicting`, but omits pre-hash `_is_utf8_str` / `Mapping` guards even though `_active_bundle_nonconflicting` runs before `_card_provenance_valid` (`PC-001`). |
| `FR-02` / `C2` (`RV-027`) | Partial | Covers primary aggregate/constituent status rollup, `out_of_cadence` label, and overdue `due_on`, but misses unhashable constituent guards (`PC-001`) plus `due_on=None` / `last_success`+`cadence_days` / `as_of` / `label` invariants, constituent-level `currentness` + `_source_matches` parity, and strict boolean / omitted-key `expect_out_of_cadence` handling across `citation_validity` and `answer_contract` (`PC-002`). |
| `FR-03` / `C3` (`RV-028`) | Covered | Importing `refuse_question` in `src/core/src/zava_forward/core/regulatory_chat.py` without circular imports and evaluating `refuse_question(question.strip()) or refuse_question(masked)` in `RegulatoryChat.surface` closes permissive `self.refuse` bypasses while preserving `ask`/`bundle` unit-test seams. |
| `FR-04` / `C4` (`RV-029`) | Partial | `multi_bundle` signature alignment and `v2_source["link"]` isolation are sound, but `P01-T02` specifies `ship_mode == "cards_only"` for `RegulatoryChat.surface` refusal instead of distinguishing `comparison=None` from verified `comparison=positive_cmp` (`ship_mode == "chat_with_cards"` with `chat["kind"] == "refused"`) (`PC-003`). |
| `P01` / `P01-T01` | Partial | Needs fail-closed type/hashability guards in `_active_bundle_nonconflicting` (`PC-001`) and complete freshness/currentness/`expect_out_of_cadence` invariants (`PC-002`). |
| `P01-T02` | Partial | Needs corrected `RegulatoryChat.surface` assertion expectations across `comparison=None` and `comparison=positive_cmp` (`PC-003`) plus regression coverage for `PC-001` and `PC-002`. |

## Verdict

* Verdict: `Revise`
* Rationale: The candidate plan targets all four review findings (`RV-026`..`RV-029`) inside `src/core`, but three substantive gaps require direct planner revision before implementation: (1) unguarded `set`/dict hashing on raw card fields inside `_active_bundle_nonconflicting` can raise `TypeError` on malformed inputs before `_card_provenance_valid` runs (`PC-001`); (2) constituent `due_on=None` / `last_success`+`cadence_days` / `as_of` / `label` invariants, `_source_matches` `currentness` parity, and strict boolean / omitted-key `expect_out_of_cadence` grading remain incomplete (`PC-002`); and (3) `P01-T02` specifies `ship_mode == "cards_only"` on `RegulatoryChat.surface` refusal, which either fails under `comparison=positive_cmp` or skips testing the verified-comparison `chat_with_cards` refusal path (`PC-003`).

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Unhashable or malformed card fields in `_active_bundle_nonconflicting` can raise `TypeError` instead of failing closed

* Related IDs: `FR-01`, `FR-02`, `C1`, `C2`, `P01`, `P01-T01`, `P01-T02`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_inspect_bundle_surface` lines 926-943 and `grade_chat_turn` lines 1456-1511), `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c12-plan.md` (`FR-01`, `FR-02`), `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c12-phase-details.md` (`P01-T01`), and `src/core/tests/test_regulatory_eval_gates_216.py` (malformed container and `_UnhashableStr` fail-closed tests).
* Concern: Both `_inspect_bundle_surface` and `grade_chat_turn` call `_active_bundle_nonconflicting(sources, facts, cards)` before `_card_provenance_valid` validates `cards`. `FR-01` and `P01-T01` specify constructing `{(card.get("safe_default"), card.get("clock")) for card in cards}` directly as a `set` and indexing/comparing `(entry.get("status"), entry.get("due_on"), entry.get("last_success"))` per `source_id` across cards without prior type checks. If `safe_default`, `clock`, `source_id`, `status`, `due_on`, or `last_success` is a `dict`, `list`, or unhashable `str` subclass (`_UnhashableStr`), or if `source_freshness` / `sources` / `entry` is not a `Mapping` / `_is_nonstr_seq`, `_active_bundle_nonconflicting` raises `TypeError` or `AttributeError` instead of returning `False`.
* Impact: Malformed or adversarial in-memory bundles crash `deterministic_rule_cards`, `render_extractive_answer`, `grade_chat_turn`, `evaluate_citation_and_refusal_gates`, and `resolve_regulatory_surface` with unhandled exceptions rather than failing closed.
* Smallest useful change: Revise `FR-01`, `FR-02`, and `P01-T01` so `_active_bundle_nonconflicting` checks `isinstance(card, Mapping)`, `_nonblank_str(card.get("safe_default")) is not None`, and `_nonblank_str(card.get("clock")) is not None` (`_is_utf8_str` enforces `type(v) is str`, rejecting `_UnhashableStr` and containers) before inserting `(card["safe_default"], card["clock"])` into `signatures`, and checks `isinstance(freshness, Mapping)`, non-empty `_is_nonstr_seq(raw_sources)`, `isinstance(entry, Mapping)`, nonblank unstripped `_is_utf8_str` `source_id`, and `val is None or _is_utf8_str(val)` on `status`, `due_on`, and `last_success` before dict lookup or tuple storage, returning `False` on any mismatch. Include unhashable card-field inputs in `P01-T02`.
* Action owner: `planning_parent`
* Exact resolving evidence: Revised `FR-01`/`FR-02` in `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c12-plan.md` and `P01-T01`/`P01-T02` in `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c12-phase-details.md` specifying exact `_is_utf8_str`/`Mapping` guards before `set`/dict operations in `_active_bundle_nonconflicting` and regression assertions for unhashable card fields.
* Decision route: `direct_planner_correction`

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Incomplete `source_freshness` constituent, source-`currentness`, and `expect_out_of_cadence` rules leave staleness-forgery and omitted-key gaps

* Related IDs: `FR-02`, `C2`, `P01`, `P01-T01`, `P01-T02`
* Evidence: `src/core/src/zava_forward/core/source_monitor.py` (`source_freshness` lines 48-92 and `card_freshness` lines 95-125), `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_active_bundle_nonconflicting` lines 680-735, `_card_provenance_valid` lines 1298-1342, `_source_matches` lines 1345-1369, `grade_chat_turn` lines 1485-1620, `_classify_refusal_confusion` line 1693), `src/core/tests/test_regulatory_eval_gates_216.py` (`multi_bundle` lines 867-912, `unmapped_bundle` lines 1158-1182, `test_c11` line 2450), `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c12-plan.md` (`FR-02`), and `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c12-phase-details.md` (`P01-T01`).
* Concern: Three provenance and grading gaps remain in `FR-02` and `P01-T01`:
  * Constituent `due_on=None`, `last_success`/`cadence_days`, `as_of`, and `label` parity: `P01-T01` validates `due_on` only when present and not `None`. In `source_monitor.source_freshness`, `due_on is None` occurs only when monitoring has no valid observation, where `status` is always `"unknown"`. Under `P01-T01`, an entry with `{"source_id": sid, "status": "in_cadence", "due_on": None}`, a forged future `due_on` contradicting `last_success + timedelta(days=cadence_days)`, a stale `freshness["as_of"]` or `entry["as_of"]` disagreeing with active `as_of_day`, a missing/blank `freshness["label"]` on `"in_cadence"`/`"unknown"`, or the `out_of_cadence` label attached to a non-`out_of_cadence` card passes `_card_provenance_valid`.
  * Asymmetric bundle `currentness` check and `_source_matches` omission: `P01-T01` only requires card aggregate `status == "out_of_cadence"` when `src.get("currentness") == "out_of_cadence"`, missing constituent-level mismatches (such as a two-source card whose other source makes the aggregate `"out_of_cadence"` while `src`'s constituent entry claims `"in_cadence"`, or `src.get("currentness") == "in_cadence"` while its constituent entry claims `"out_of_cadence"`), and `_source_matches` omits `"currentness"` from `required_keys`, allowing `actual["citations"][i]["currentness"]` to diverge from `expected["sources"][i]["currentness"]`.
  * `expect_out_of_cadence` type coercion, omitted-key default, and `citation_validity` parity in `grade_chat_turn`: `grade_chat_turn` computes `expect_stale = bool(expected.get("expect_out_of_cadence"))` (`regulatory_eval_gates.py:1600`). With `P01-T01`'s `expect_stale == exp_stale_card_present == stale_card_present`, non-boolean values such as `"expect_out_of_cadence": "false"` coerce to `True`, callers omitting `"expect_out_of_cadence"` on a stale bundle (`{**stale_bundle, "kind": "answer"}`, matching the `test_c11` line 2450 caller pattern and `exp_self` self-grading) coerce `None` to `False` and spuriously fail, and checking staleness parity only in `safe_fields_ok` leaves `citation_validity == True` when `expected` supplies contradictory `expect_out_of_cadence=False` on an `out_of_cadence` card.
* Impact: Forged constituent freshness metadata (`due_on=None`, tampered `due_on` vs `last_success`/`cadence_days`, stale `as_of`, mutated `citations[i]["currentness"]`, or non-boolean `expect_out_of_cadence`) can slip past provenance/citation checks, while omitted-key stale bundle grading breaks self-consistency.
* Smallest useful change: Update `FR-02`, `P01-T01`, and `P01-T02` so that:
  * `_card_provenance_valid` requires `_nonblank_str(freshness.get("label")) is not None` with `(freshness.get("label") == OUT_OF_CADENCE_LABEL) == (fresh_status == "out_of_cadence")`; validates optional `"as_of"` on `freshness` and constituent entries via `_valid_iso_day` (and `== as_of_day` when `require_active and as_of_day is not None`); requires `entry.get("status") in (None, "unknown")` whenever `"due_on" in entry and entry["due_on"] is None`; and when `"last_success"` or `"cadence_days"` is present, validates `last_success` (`None` or valid ISO day, `<= as_of_day` when active) and `cadence_days` (`None` or `_strict_int` in `1..36600`), requiring `entry.get("due_on") is None` and `entry.get("status") in (None, "unknown")` if either is `None` and `entry.get("due_on") == (date.fromisoformat(last_success) + timedelta(days=cadence_days)).isoformat()` when both are set.
  * `_active_bundle_nonconflicting` enforces constituent-level parity whenever `src.get("currentness") in ("in_cadence", "out_of_cadence", "unknown")` (requiring any referencing constituent `entry` with `"status"` to equal `src["currentness"]`, and requiring card aggregate `status == "out_of_cadence"` when `src["currentness"] == "out_of_cadence"`), and `_source_matches` adds `"currentness"` to `required_keys`.
  * `grade_chat_turn` validates `"expect_out_of_cadence"` strictly when present (`type(expected["expect_out_of_cadence"]) is bool and expected["expect_out_of_cadence"] == exp_stale_card_present`), defaults `expect_stale = exp_stale_card_present` when `"expect_out_of_cadence" not in expected`, and gates `cards_prov_ok` (`citation_validity`) as well as `safe_fields_ok` (`answer_contract`) on `exp_expect_stale_ok and exp_stale_card_present == stale_card_present`.
* Action owner: `planning_parent`
* Exact resolving evidence: Revised `FR-02` in `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c12-plan.md` and `P01-T01`/`P01-T02` in `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c12-phase-details.md` specifying constituent `due_on=None` / `last_success`+`cadence_days` / `as_of` / `label` validation, bidirectional enum `currentness` + `_source_matches` parity, and strict boolean / omitted-key `expect_out_of_cadence` grading across `citation_validity` and `answer_contract`.
* Decision route: `direct_planner_correction`

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `P01-T02` specifies `ship_mode == "cards_only"` on `RegulatoryChat.surface` refusal instead of testing verified-comparison `chat_with_cards` refusal

* Related IDs: `FR-03`, `FR-04`, `C3`, `C4`, `P01`, `P01-T02`
* Evidence: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c12-phase-details.md` (`P01-T02`), `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c11-review.md` (`RV-028`), `src/core/src/zava_forward/core/regulatory_chat.py` (`RegulatoryChat.surface` lines 470-487), and `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`resolve_regulatory_surface` lines 3875-3935).
* Concern: `P01-T02` states that `RegulatoryChat.surface` initialized with a permissive `lambda _q: None` callback refuses prohibited prompts with `(cards == [], ship_mode == "cards_only", chat is None or refused)`. In `RegulatoryChat.surface` + `resolve_regulatory_surface`, when `comparison` passes `_verify_comparison_evidence(comparison)`, `self.render(snap)` renders a valid `kind == "refused"` chat envelope that passes `grade_chat_turn(..., _expected_from_bundle(snap))`, so `resolve_regulatory_surface` returns `ship_mode == "chat_with_cards"` with `rule_cards["cards"] == []` and `chat["kind"] == "refused"` rather than `ship_mode == "cards_only"`. Conversely, calling `surface(..., comparison=None)` returns `ship_mode == "cards_only"` with `chat is None` and never exercises the verified-comparison `chat` branch described in `RV-028` ("could return actionable `rule_cards` or grounded `chat`").
* Impact: Implementing `P01-T02` literally either fails on `ship_mode` when `comparison=positive_cmp` is passed or leaves untested the critical `comparison=positive_cmp` scenario where a compound prohibited prompt containing a supported purpose keyword (for example `"What is the hazard clock, and is this home legally compliant?"`) would otherwise retrieve active cards and ship `chat["kind"] == "answer"`.
* Smallest useful change: Update `P01-T02` in `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c12-phase-details.md` so `test_c12_...` exercises `RegulatoryChat.surface` (with `refuse=lambda _q: None`) on a compound prohibited prompt matching a supported purpose keyword under both `comparison=None` (`ship_mode == "cards_only"`, `chat is None`, `rule_cards["cards"] == []`, `rule_cards["refusal"] == expected_refusal`) and `comparison=positive_cmp` (`ship_mode == "chat_with_cards"`, `rule_cards["cards"] == []`, `rule_cards["refusal"] == expected_refusal`, `chat["kind"] == "refused"`, `chat["refusal"] == expected_refusal`, `chat["citations"] == []`, `chat["cards"] == []`).
* Action owner: `planning_parent`
* Exact resolving evidence: Updated `P01-T02` in `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c12-phase-details.md` specifying separate assertions for `comparison=None` (`ship_mode == "cards_only"`, `chat is None`) and `comparison=positive_cmp` (`ship_mode == "chat_with_cards"`, `chat["kind"] == "refused"`, `rule_cards["cards"] == []`) on a purpose-matching prohibited question.
* Decision route: `direct_planner_correction`

## Strengths and Residual Risk

* `FR-03` (`RV-028`) cleanly enforces `refuse_question(question.strip()) or refuse_question(masked)` inside `RegulatoryChat.surface` without circular imports (`regulatory_chat.py` already imports from `regulatory_eval_gates.py`) and without perturbing `RegulatoryChat.ask` or `RegulatoryChat.bundle` unit-test seams.
* `FR-04` (`RV-029`) accurately identifies the divergent `safe_default` values in `multi_bundle` (`test_regulatory_eval_gates_216.py:892,907`) that would otherwise regress once `RV-026` is enforced, and isolates `v2_source["link"]` in `test_c11`.
* Residual risk explicitly bounded by caller instructions: `src/api` route wiring to `RegulatoryChat.surface` and `src/agents` helper deduplication remain out-of-scope follow-ups outside `src/core`.

## Questions or Blocking Evidence Gaps

* None. All three findings are deterministic planner corrections resolvable from the supplied `src/core` codebase without user input.

## Limitations

* Critique is strictly bounded to the supplied `src/core` code targets and tracking artifacts; `src/api` and `src/agents` were not evaluated per caller boundary.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: `planning_parent`
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c12-plan.md` (`FR-01`, `FR-02`) and `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c12-phase-details.md` (`P01-T01`, `P01-T02`) to apply `PC-001`..`PC-003` and finalize the plan without another critique pass.
* User response required: `no`
