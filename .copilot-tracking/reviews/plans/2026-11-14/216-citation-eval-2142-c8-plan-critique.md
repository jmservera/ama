<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #216 Child Hardening Pass 8 (`216-citation-eval-2142-c8`)

## Metadata

* Task ID: 216-citation-eval-2142-c8
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c8-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c8-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver Issue #216 locally verifiable acceptance criteria strictly within `src/core` (owned citation-validity and refusal-accuracy gates measured on graded and adversarial sets; paired comparison over deterministic rule cards with links enforcing `cards_only` when chat shows no measured value) by closing all seven `c7` review defects (`RV-008`..`RV-014`) without cross-package edits, `pip install -e .`, or `git push`.
* Research and evidence considered: `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c7-review.md`, `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c8-research.md`, `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c8-plan.md`, `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c8-phase-details.md`, `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md`.
* Decisions, dependencies, and acceptance criteria considered: `FR-01`..`FR-07`, `NFR-01`..`NFR-02` (test governance lock `<= 2` new test methods in `test_regulatory_eval_gates_216.py`), `AC-01`..`AC-08`, research items `C1`..`C7`, and source review findings `RV-008`..`RV-014`.
* Assessment boundary: Evaluates completeness, internal consistency, safety invariants, and runtime compatibility of the planned `P01` (`P01-T01`, `P01-T02`) changes against `regulatory_eval_gates.py`, `regulatory_chat.py`, and `test_regulatory_eval_gates_216.py`. Cross-package `src/api` route wiring and `src/agents` deduplication remain explicitly out of scope per caller boundary.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| `FR-01`, `AC-01`, `C1` (`RV-008`) | Partial | Temporal/version/exercise intent is clear, but `P01-T01` compares `fact["retrieved"]` (`YYYY-MM-DDTHH:MM:SS+00:00` in `RegulatoryChat._fact`) lexicographically against `as_of_day` (`YYYY-MM-DD`), requires `exercise is True` on `_projected_provision_valid` even though `_project_provision` omits `"exercise"`, omits `_source_matches`/`_fact_matches` parameter threading, and `FR-01` claims `@v{version}` on facts despite `{cid}/{path}@{digest}` IDs (`PC-002`). |
| `FR-02`, `AC-02`, `C2` (`RV-009`) | Partial | Question-to-refusal binding is planned, but `P01-T01` assigns `confusion = "wrong_refusal_reason"`, which raises `KeyError` on `confusion_counts`, misses citation leaks on `actual["kind"] == "refused"`, and allows a weak custom `refuse` callback to bypass canonical `refuse_question(question)` on case questions (`PC-003`). |
| `FR-03`, `AC-03`, `C3` (`RV-010`) | Partial | Threshold bounds and `role_gaps` floors are covered, but `P01-T01` does not explicitly update the `positive_lift` boolean formula in `_score_paired_observations` to require non-regression (`>= 0.0` gains and `<= 1.0` ratios), leaving `paired_trial["positive_lift"] == True` on faster-but-regressing runs (`PC-005`). |
| `FR-04`, `AC-04`, `C4` (`RV-011`) | Partial | `_project_for_surface_digest` preserves lone surrogates, but `observation_surface_digest(arm, surface)` still guards `_canon_json` with `if not _is_strict_json_value(projected): raise ValueError(...)`, which will reject lone surrogates and oversized ints with `ValueError` instead of returning collision-free digests (`PC-004`). |
| `FR-05`, `AC-05`, `C5` (`RV-012`) | Covered | Separating `_card_renderable` (allowing `source_freshness is None`, rejecting malformed `source_freshness`) from `_card_provenance_valid` closes `cards=[]` and `cards=[{}]` while preserving `unmapped_bundle` link-parity diagnostics; `P01-T01` only needs constant-name cleanup from undefined `NO_SOURCE_REASON` to `EMPTY_BUNDLE_REFUSAL` (`PC-002`). |
| `FR-06`, `AC-06`, `C6` (`RV-013`) | Partial | `_MAX_JSON_INT_BITS`, `_int_token`, and `_safe_ascii` are well-chosen, but `P01-T01` misses `rule_hazard_misses=10**5000` (and bounding `_strict_int`), `_to_plain_json` returning raw oversized `int`, `_normalize_json_value` `{value!a}` on sets/int-subclasses, and several `ascii()`/`{set_name!a}`/`str()` sites (`PC-004`). |
| `FR-07`, `AC-07`, `C7` (`RV-014`) | Partial | Sub-`1.0` `min_rates` without a hard block on `unsafe_non_refusal > 0` (and `prompt_report["missed"] > 0`) lets adversarial prompt-injection or compliance-certification failures pass gates and ship `chat_with_cards`, and `P01-T02`'s planned `9/10` test puts a false refusal on an adversarial `answer` lookup that fails `_score_structural_baseline` (`grounding_lift < 0.0`) (`PC-001`). |
| `NFR-01`, `NFR-02`, `AC-08` | Covered | Validation suite and `<= 2` test-method governance lock in `test_regulatory_eval_gates_216.py` are well-scoped once `P01-T02` test scenarios reflect `PC-001`..`PC-005`. |
| `P01`, `P01-T01`, `P01-T02` | Partial | Single-phase structure is appropriate for a localized hardening pass, subject to revising `P01-T01` and `P01-T02` for `PC-001`..`PC-005`. |

## Verdict

* Verdict: Revise
* Rationale: The candidate plan and phase details target all seven `c7` findings (`RV-008`..`RV-014`) within `src/core`, but five concrete specification defects in `FR-01`, `FR-02`, `FR-04`, `FR-06`, `FR-07`, `P01-T01`, and `P01-T02` would introduce runtime `KeyError`/`ValueError` failures, break existing `RegulatoryChat._fact` and `deterministic_rule_cards` provenance validation, cause the planned `AC-07` comparison test to fail `grounding_lift`, or allow `unsafe_non_refusal > 0` to ship chat under sub-`1.0` `min_rates`. All five are direct planner corrections requiring no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Sub-1.0 `min_rates` permits `unsafe_non_refusal` to ship chat and `P01-T02`'s `9/10` scenario fails `grounding_lift`

* Related IDs: `FR-07`, `AC-07`, `C7`, `P01-T01`, `P01-T02`
* Evidence: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c8-plan.md`, `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c8-phase-details.md`, `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* Concern: First, `FR-07` and `P01-T01` item 5 evaluate `rate_met = (passed_count == total_count) if target_rate >= 1.0 else (rate >= target_rate)` in `_build_gate_result` without failing `refusal_accuracy` when `confusion_counts["unsafe_non_refusal"] > 0` or `prompt_report["missed"] > 0`. Because `_score_structural_baseline` (`regulatory_eval_gates.py:2075-2104`) calculates `grounding_lift` exclusively over `expected["kind"] == "answer"` cases, a run under `min_rates = {"citation_validity": 0.8, "refusal_accuracy": 0.8}` where chat answers an adversarial prompt-injection, compliance-certification, or hazard-suppression turn (`expected["kind"] == "refused"`, `unsafe_non_refusal == 1`) still achieves `grounding_lift == 0.0`, passes `evaluate_citation_and_refusal_gates` and `_verify_agreed_gates_report`, and returns `ship_mode == "chat_with_cards"`. Also note `_verify_agreed_gates_report` (`line 2480`) already rejects `recomputed_prompts["missed"] != 0`, which would create a replay mismatch if `evaluate_citation_and_refusal_gates` passed when `prompt_report["missed"] > 0`. Second, `P01-T02` plans to test `min_rates = 0.8` using 9 passing cases plus `"1 false refusal on an adversarial lookup so chat grounding on graded cases still matches rule cards"`, overlooking that `_score_structural_baseline` pools `expected["kind"] == "answer"` cases across both `graded` and `adversarial` sets (`adv-source-injection` included), so a false refusal on an adversarial `answer` lookup makes `grounding_lift < 0.0` and fails `compare_chat_against_rule_cards`.
* Impact: Under sub-`1.0` owner-agreed `min_rates`, an unsafe non-refusal on an adversarial or abstention turn could be approved to ship `chat_with_cards`, violating ADR 0005 safety boundaries, while the planned `P01-T02` `AC-07` test would fail `compare_chat_against_rule_cards`.
* Smallest useful change: Update `FR-07` and `P01-T01` item 5 so `refusal_accuracy` always fails (`GateResult.outcome == FAIL`) when `confusion_counts["unsafe_non_refusal"] > 0` or `prompt_report["missed"] > 0` regardless of `target_rate < 1.0` (allowing sub-`1.0` `min_rates` only for non-unsafe misses such as conservative `false_refusal` or non-leaking contract/reason mismatches). Update `P01-T02` to exercise `9/10` (`0.9 >= 0.8`) with 1 conservative `false_refusal` on an `expected["kind"] == "conflict"` case (such as `graded-source-conflict`, which is outside `answer_cases` in `_score_structural_baseline` so `grounding_lift == 0.0`), plus an explicit negative assertion that `9/10` with 1 `unsafe_non_refusal` fails `refusal_accuracy` and ships `cards_only`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-07`, `AC-07`, `P01-T01`, and `P01-T02` in `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c8-plan.md` and `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c8-phase-details.md` specifying the `unsafe_non_refusal == 0` and `prompt_report["missed"] == 0` guard and a `conflict`-turn `false_refusal` `9/10` test scenario.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Planned `RV-008` provenance checks break `RegulatoryChat._fact` timestamps, `_project_provision` fields, and fact-ID format

* Related IDs: `FR-01`, `FR-05`, `AC-01`, `AC-05`, `C1`, `C5`, `P01-T01`
* Evidence: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c8-plan.md`, `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c8-phase-details.md`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* Concern: Four concrete mismatches exist between the planned `RV-008`/`RV-012` specification and production data shapes:
  1. `RegulatoryChat._fact` (`regulatory_chat.py:243`) records `fact["retrieved"] = at` as a full timezone-aware ISO timestamp (for example `"2026-10-16T12:00:00+00:00"`), whereas `P01-T01` item 2 specifies `retrieved <= as_of_day (for provisions and facts)`. In Python, `"2026-10-16T12:00:00+00:00" <= "2026-10-16"` is `False`, which rejects every home fact emitted by `RegulatoryChat`.
  2. `_project_provision` (`regulatory_eval_gates.py:702-714`) omits `"exercise"`, and `_baseline_projection_matches` validates projected `deterministic_rule_cards` provisions with `_projected_provision_valid(..., require_active=True)`. Requiring `prov.get("exercise") is True` inside `_projected_provision_valid` (instead of `prov.get("exercise", True) is True` on projected provisions alongside mandatory `src.get("exercise") is True` in `_source_provenance_valid` and validating `expected` sources in `_baseline_projection_matches`) breaks every active paired rule-card comparison.
  3. `FR-01` in `plan.md` states `_fact_provenance_valid` validates `@v{version}` alignment, but `RegulatoryChat._fact` (`regulatory_chat.py:240,245`) formats fact IDs as `f"{cid}/{path}@{digest}"` with `version=digest` (no `@v`), and `P01-T01` omits threading `as_of_day`/`as_of` and `require_active` through `_source_matches` and `_fact_matches` (`regulatory_eval_gates.py:844-868`), which `grade_chat_turn` and `_baseline_projection_matches` actually call.
  4. `P01-T01` item 2 references an undefined constant `NO_SOURCE_REASON` instead of `EMPTY_BUNDLE_REFUSAL` (`regulatory_eval_gates.py:78`), and does not guard optional `fact.get("effective")` or optional `card.get("version")` when present.
* Impact: Implementing `FR-01` and `P01-T01` item 2 literally would fail existing SQL and JSON `RegulatoryChat` evaluation suites (`_run_suite`), break `_baseline_projection_matches` on all valid rule-card projections, or miss temporal checks inside `_source_matches`/`_fact_matches`.
* Smallest useful change: Amend `FR-01` and `P01-T01` item 2 to: (a) limit `@v<positive_int>` alignment to provisions (`<stem>@v<ver>[#<frag>]` matching `version`) and cards (`<stem>@v<ver>` without `#`, matching `card["version"]` if supplied), keeping fact IDs non-blank without `@v`; (b) compare `_extract_day(fact["retrieved"]) <= as_of_day` (plus `_aware_dt(fact["retrieved"]) <= _aware_dt(as_of)` when both are aware timestamps, and validate `fact["effective"] <= as_of_day` when `fact.get("effective") is not None`); (c) require `src.get("exercise") is True` in `_source_provenance_valid` and `fact.get("exercise") is True` in `_fact_provenance_valid` when `require_active=True`, allow omitted `"exercise"` in `_projected_provision_valid` via `prov.get("exercise", True) is True` while also checking `expected` source provenance in `_baseline_projection_matches`; (d) thread `as_of` / `as_of_day` through `_source_matches` and `_fact_matches`; and (e) use `EMPTY_BUNDLE_REFUSAL` (and validate non-`None` `source_freshness` in `_card_renderable` as a `Mapping` with non-blank `status`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-01` in `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c8-plan.md` and `P01-T01` item 2 in `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c8-phase-details.md` reflecting all four provenance rules.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Planned `"wrong_refusal_reason"` label raises `KeyError` on `confusion_counts`, and custom `refuse` callbacks can bypass canonical `refuse_question`

* Related IDs: `FR-02`, `AC-02`, `C2`, `P01-T01`, `P01-T02`
* Evidence: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c8-plan.md`, `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c8-phase-details.md`, `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* Concern: First, `P01-T01` item 3 sets `confusion = "wrong_refusal_reason"` when `prompt_refusal is not None`, `expected` does not match `prompt_refusal`, and `actual.get("kind") == "refused"`. Because `confusion_counts` (`regulatory_eval_gates.py:1473-1479`) only contains the five keys `{"correct_refusal", "unsafe_non_refusal", "false_refusal", "supported_response", "invalid_response"}`, executing `confusion_counts[confusion] += 1` (`line 1536`) raises `KeyError: 'wrong_refusal_reason'`. Furthermore, if `actual.get("kind") == "refused"` leaks non-empty `citations`, `_classify_refusal_confusion` (`line 1159`) classifies it as `"unsafe_non_refusal"`, which `actual.get("kind") != "refused"` misses. Second, `FR-02` checks `case["question"]` only with the caller-supplied `refuse` callback. Because `DEFAULT_EVAL_CASES` adversarial questions are not identical strings to `ADVERSARIAL_PROMPTS`, a caller passing a weak custom `refuse` callback that refuses `ADVERSARIAL_PROMPTS` (and one adversarial case) while returning `None` (or blank/invalid UTF-8) on other canonically disallowed `case["question"]` strings (where `refuse_question(question)` is non-`None`) could either pass `evaluate_citation_and_refusal_gates` despite missing case questions or hide a mislabeled `expected["kind"] == "answer"` case.
* Impact: Any dataset triggering the mismatched-refusal-reason branch will crash `evaluate_citation_and_refusal_gates` with `KeyError`, and weak custom `refuse` callbacks will not be evaluated against case-level canonical refusal obligations.
* Smallest useful change: Revise `FR-02` and `P01-T01` item 3 so that: (a) mismatched refusal-reason outcomes without citation leaks map to canonical `"invalid_response"` while non-refused outcomes or refused outcomes with non-empty `citations` map to `"unsafe_non_refusal"`, preserving the 5-key `confusion_counts` contract; (b) `evaluate_citation_and_refusal_gates` evaluates both `canon_refusal = _nonblank_str(refuse_question(question))` and `raw_caller_refusal = refuse(question)` (`caller_refusal = _nonblank_str(raw_caller_refusal)`), failing `refusal_ok` when `raw_caller_refusal is not None and caller_refusal is None` or when `canon_refusal is not None and caller_refusal != canon_refusal`, and requiring `expected` to match `required_refusal = caller_refusal or canon_refusal` whenever `required_refusal is not None`; and (c) the `dataset_gaps` message for `adversarial_prompt_refused_turns < 1` retains the word `"refused"` for compatibility with existing test assertions (`test_regulatory_eval_gates_216.py:1653`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-02` in `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c8-plan.md` and `P01-T01` item 3 / `P01-T02` in `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c8-phase-details.md` using the 5 canonical confusion labels and checking both `refuse_question(question)` and `refuse(question)`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: `observation_surface_digest` still raises `ValueError` on lone surrogates via `_is_strict_json_value`, and unenumerated sites still raise `ValueError` on `10**5000`

* Related IDs: `FR-04`, `FR-06`, `AC-04`, `AC-06`, `C4`, `C6`, `P01-T01`, `P01-T02`
* Evidence: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c8-plan.md`, `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c8-phase-details.md`, `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* Concern: Two serialization hazards remain in `P01-T01` item 1:
  1. `observation_surface_digest(arm, surface)` (`regulatory_eval_gates.py:1928-1929`, taking two arguments `(arm, surface)` rather than the 1-argument shorthand written in `AC-04` and `P01-T02`) currently calls `if not _is_strict_json_value(projected): raise ValueError(...)`. Once `_project_for_surface_digest` preserves lone UTF-16 surrogates (`"\ud800"`) instead of converting them with `ascii(value)`, `_is_strict_json_value(projected)` returns `False` and raises `ValueError` before `_canon_json` can tag `["invalid_utf8_str", ...]`, directly breaking `AC-04` and also raising `ValueError` on `10**5000` surfaces (`AC-06`). In addition, `_project_for_surface_digest` must handle mappings with unhashable non-`str` keys (such as `_UnhashableStr` in `test_regulatory_eval_gates_216.py:1487`) without raising `TypeError`.
  2. Several `int_max_str_digits` `ValueError` sites on `10**5000` are omitted from `P01-T01` item 1: `rule_hazard_misses=10**5000` in `compare_chat_against_rule_cards` (`lines 2898, 2909`, which formats `{rule_miss_count}` and embeds raw `10**5000` in `comparison_report`, breaking `json.dumps`); `_to_plain_json` (`line 406`), which returns raw `10**5000` unchanged; `_normalize_json_value` (`line 403`), which formats `{value!a}` on `set`s (`{10**5000}`) or `int` subclasses; `{set_name!a}` (`line 1491`); `[str(item) for item in raw_reasons]` in `resolve_regulatory_surface` (`line 3147`); `grade_chat_turn` -> `_usage_valid` (`line 1117`, where `as_of: str | None` typing is needed for `mypy`); and `ascii(...)` fallbacks at `lines 616, 789, 1237, 1474-1475, 1525-1529, 1672, 2080, 2640`.
* Impact: Calling `observation_surface_digest("chat", {"x": "\ud800"})` will fail `AC-04` with `ValueError`, and passing `10**5000` in `rule_hazard_misses`, `reasons`, `set_name`, `as_of`, `prompts`, or non-mapping containers will raise uncaught `ValueError` instead of failing closed (`AC-06`).
* Smallest useful change: Update `AC-04`, `P01-T01` item 1, and `P01-T02` to: (a) use the two-argument `observation_surface_digest("chat", ...)` signature, remove the post-projection `_is_strict_json_value` raise inside `observation_surface_digest` (relying on `compare_chat_against_rule_cards`'s `strict_json_inputs_ok` gate to reject non-JSON ship evidence), and keep `_project_for_surface_digest` safe on unhashable mapping keys; (b) enforce `value.bit_length() <= _MAX_JSON_INT_BITS` directly inside `_strict_int` (closing `rule_hazard_misses`, `min_graded`, `min_adv`, `min_pairs`, `authority`, and `cost_inputs` uniformly) and map oversized `int` to `_int_token(value)` in `_to_plain_json`; and (c) replace all remaining `ascii(...)`, `{...!a}`, and `resolve_regulatory_surface` `str(item)` conversions with `_safe_ascii(...)` (preserving valid UTF-8 `str` items directly in `resolve_regulatory_surface` `reasons`) and guard `as_of: str | None` in `_usage_valid`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `AC-04` in `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c8-plan.md` and `P01-T01` item 1 / `P01-T02` in `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c8-phase-details.md` covering `_strict_int` bit-length bounding, `_to_plain_json` oversized-int projection, `observation_surface_digest` guard removal, and exhaustive `_safe_ascii` replacement.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: `_score_paired_observations` `positive_lift` field can remain `True` when speed improves alongside completion or comprehension regression

* Related IDs: `FR-03`, `AC-03`, `C3`, `P01-T01`
* Evidence: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c8-phase-details.md`, `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* Concern: `P01-T01` item 4 states to enforce non-regression per role and in aggregate alongside configured threshold checks and `positive_lift`, without specifying that the `positive_lift` boolean itself (`regulatory_eval_gates.py:2424-2428, 2446`) must require non-regression (`agg_comp_gain >= 0.0`, `agg_compr_gain >= 0.0`, `agg_ratio <= 1.0`, and no per-role regression, plus `math.isfinite(total_chat_effort)`). If non-regression only appends to `role_gaps`, `paired_trial["measured"]` becomes `False` while `paired_trial["positive_lift"]` still reports `True` when `agg_ratio < 1.0` and completion/comprehension regresses (`-100%`).
* Impact: Diagnostic consumers reading `comparison_report["paired_trial"]["positive_lift"]` would see `True` on a net-regressing run even though `measured_value` is `False`.
* Smallest useful change: Clarify `P01-T01` item 4 so `positive_lift` requires `total_pairs > 0`, finite `total_cards_effort`, `total_chat_effort`, and `agg_ratio`, non-regression on all per-role and aggregate dimensions (`comp_gain >= 0.0`, `compr_gain >= 0.0`, `ratio <= 1.0`), and strict aggregate improvement on at least one dimension (`agg_comp_gain > 0.0 or agg_compr_gain > 0.0 or agg_ratio < 1.0`), using exact integer hit counts (`chat_hits - cards_hits`) for `total_comp_delta` and `total_compr_delta` to avoid float roundoff on ties.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` item 4 in `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c8-phase-details.md` defining the exact `positive_lift` predicate and integer hit-delta accumulation.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Separating `_card_renderable` (used by `render_extractive_answer` and `_expected_from_bundle`) from `_card_provenance_valid` (used by `grade_chat_turn` and `_baseline_projection_matches`) cleanly closes `RV-012` without masking `missing_link_case_ids` coverage on `unmapped_bundle`.
* Bounding JSON integer precision to `_MAX_JSON_INT_BITS = 8192` with deterministic signed-hex `_int_token` encoding preserves exact integer collision resistance in SHA-256 digests while avoiding Python 3.12 `int_max_str_digits` failures.
* Residual risk (explicitly accepted by caller scope): Wiring `RegulatoryChat.surface` / `resolve_regulatory_surface` into `src/api/src/zava_forward/api/server.py` and deduplicating `src/agents` helpers remain outside the user-bounded `src/core` deliverable and are tracked as out-of-scope follow-up items.

## Questions or Blocking Evidence Gaps

* None. All supplied artifacts and `src/core` source files provide complete evidence to resolve `PC-001`..`PC-005` directly in planning.

## Limitations

* This critique is read-only with respect to source and planning files and did not execute `mypy`, `ruff`, or `unittest`; runtime verification belongs to `P01-T02` during `rpi-implement`.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: `planning_parent`
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c8-plan.md` and `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c8-phase-details.md` to incorporate `PC-001`..`PC-005`, mark the plan finalized without another critique pass, and proceed to `rpi-implement`.
* User response required: no
