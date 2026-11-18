<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #216 Child Hardening Pass 9 (`216-citation-eval-2142-c9`)

## Metadata

* Task ID: 216-citation-eval-2142-c9
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c9-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c9-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver remaining locally verifiable Issue #216 acceptance criteria strictly inside `src/core` on branch `feat/ai-216-citation-eval-2142` and resolve `c8` review defects `RV-015`..`RV-017`.
* Research and evidence considered: `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c8-review.md`, `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c9-research.md`, `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/src/zava_forward/core/chat_panel.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md`.
* Decisions, dependencies, and acceptance criteria considered: `FR-01`..`FR-03`, `NFR-01`..`NFR-02`, `AC-01`..`AC-04`, `P01-T01`, `P01-T02`.
* Assessment boundary: Evaluates `src/core` implementation credibility, invariants across existing 11 tests and `RV-015`..`RV-017` reproducers; excludes out-of-scope `src/api` and `src/agents` edits.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| `FR-01` / `AC-01` (`RV-015`)             | Partial  | `PC-001`: `_classify_refusal_confusion` lacks `citation_validity` and canonical refusal-reason allowlisting, and `_build_gate_result("citation_validity", ...)` must receive `extra_blockers=cit_blockers`. |
| `FR-02` / `AC-02` (`RV-016`)             | Partial  | `PC-002`: `deterministic_rule_cards` must fail closed on explicit `refusal`/`reason`/`kind == "refused"`, malformed collections, empty cards, or mixed active/inactive items so `bundle` and `_expected_from_bundle(bundle)` agree identically. |
| `FR-03` / `AC-03` (`RV-017`)             | Covered  | Bounded ASCII decimal check `ver_token.isascii() and ver_token.isdigit() and 1 <= len(ver_token) <= 18 and not ver_token.startswith("0")` prevents Unicode-digit and >4300-digit `ValueError`. |
| `P01-T01` / `P01-T02` / `AC-04`          | Partial  | `PC-003`: Specify exact `src/core/README.md` documentation updates alongside `P01-T01`. |

## Verdict

* Verdict: Revise
* Rationale: Three direct planner-owned refinements (`PC-001`..`PC-003`) are needed before implementation so corrupted citations on `answer`/`conflict` turns cannot be classified `"supported_response"`, forged refusal reasons cannot masquerade as `"false_refusal"`, and `deterministic_rule_cards` preserves exact parity on refused and mixed-provenance bundles.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Critical]: Pass `citation_validity` and enforce canonical refusal reasons in `_classify_refusal_confusion` plus `extra_blockers=cit_blockers`

* Related IDs: `FR-01`, `AC-01`, `P01-T01`, `P01-T02`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`_classify_refusal_confusion`, `evaluate_citation_and_refusal_gates`) and `src/core/src/zava_forward/core/chat_panel.py` (`OUT_OF_SCOPE`)
* Concern: `_classify_refusal_confusion` currently takes `answer_contract` without `citation_validity`; on an `answer` or `conflict` turn where a citation hash is corrupted (`citation_validity=False`, `answer_contract=True`), it returns `"supported_response"`, leaving `confusion_counts["invalid_response"] == 0` so 9/10 (`0.9 >= 0.8`) passes `citation_validity` unless `citation_validity` is checked and `extra_blockers=cit_blockers` is passed to `_build_gate_result("citation_validity", ...)`. Additionally, a crafted `false_refusal` on a non-refusal turn could inject `"Approved..."` as `actual["refusal"]` unless `actual_reason` is verified against the closed set of canonical refusal reasons (`_CANONICAL_REFUSAL_REASONS`).
* Impact: Without this tightening, `AC-01`'s corrupted-citation sub-`1.0` blocker test would fail and forged refusal strings could bypass `ref_blockers`.
* Smallest useful change: Pass `citation_validity` into `_classify_refusal_confusion`, require `citation_validity and answer_contract` for `"supported_response"`, verify `actual_reason in _CANONICAL_REFUSAL_REASONS` before returning `"false_refusal"`, and pass `extra_blockers=cit_blockers` to `_build_gate_result("citation_validity", ...)`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-01` and `P01-T01` in plan/details and passing assertions in `test_c9_unsafe_refusal_blocker_active_fallback_cards_and_unicode_versions`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Fail closed on explicit refusals, malformed collections, empty cards, and mixed-validity bundles in `deterministic_rule_cards`

* Related IDs: `FR-02`, `AC-02`, `P01-T01`
* Evidence: `src/core/src/zava_forward/core/regulatory_eval_gates.py` (`deterministic_rule_cards`, `_expected_from_bundle`) and `src/core/src/zava_forward/core/regulatory_chat.py` (`RegulatoryChat.bundle`)
* Concern: `RegulatoryChat.bundle` sets `result["refusal"]` on source/card cap overflow after populating `result["cards"]` or `result["conflict"] = True`, and `_expected_from_bundle` rejects any bundle where any source/card fails provenance validation rather than partially filtering individual items. Filtering per-item without checking `explicit_refusal`, `collections_ok`, non-empty `sources`/`cards`, and whole-bundle validity would expose partial cards on refused or mixed-provenance bundles and diverge between `deterministic_rule_cards(bundle)` and `deterministic_rule_cards(_expected_from_bundle(bundle))`.
* Impact: Prevents leaking partial or uncarded authority in `cards_only` fallback and maintains exact structural baseline parity.
* Smallest useful change: Require `not explicit_refusal` and `collections_ok` in `deterministic_rule_cards`; on `conflict_flag=True`, require non-empty `sources` and all `sources`/`cards` passing `require_active=False` (setting `conflict=True`, `cards=[]`, `provisions=[]`, `conflict_provisions=[...]`), else fail closed; on `conflict_flag=False`, require `as_of_day is not None`, non-empty `sources` and `cards`, and all `sources`/`cards` passing `require_active=True, as_of_day=as_of_day`, else fail closed (`conflict=False`, `cards=[]`, `provisions=[]`, `conflict_provisions=[]`).
* Action owner: planning_parent
* Exact resolving evidence: Updated `FR-02` and `P01-T01` in plan/details and passing structural parity across all 12 tests in `test_regulatory_eval_gates_216.py`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: Document `conflict_provisions` and sub-`1.0` blocker semantics in `src/core/README.md`

* Related IDs: `FR-01`, `FR-02`, `P01-T01`
* Evidence: `src/core/README.md` (`### Owned Citation/Refusal Gates and Paired Rule-Card Comparator (#216)`)
* Concern: `P01-T01` names `src/core/README.md` as a target without specifying the exact invariant updates for `conflict_provisions` and sub-`1.0` `invalid_response` / `unsafe_non_refusal` blockers.
* Impact: Keeps module documentation aligned with `deterministic_rule_cards` schema and gate blocker semantics.
* Smallest useful change: Specify updating the `#216` subsection in `src/core/README.md` to cover active-only fallback cards, `conflict_provisions`, and canonical `false_refusal`-only sub-`1.0` tolerances.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` details and passing `test_live_doc_links.py`.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Bounded ASCII decimal validation in `_id_version_matches` (`FR-03`) cleanly closes both Unicode-digit and >4300-digit `int(...)` `ValueError` vectors, and `grep` confirmed `_id_version_matches` is the sole string-to-`int` call in `regulatory_eval_gates.py`.
* Out-of-scope `src/api` route wiring remains cleanly separated as a non-goal under user instructions.

## Questions or Blocking Evidence Gaps

* None. All three findings are direct planner corrections within `src/core`.

## Limitations

* Assessed strictly within the `src/core` boundary specified by the caller.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: `planning_parent`
* Smallest next action: Apply `PC-001`..`PC-003` directly to `216-citation-eval-2142-c9-plan.md` and `216-citation-eval-2142-c9-phase-details.md`, record `## Critique Disposition`, finalize the plan, and advance to `Implement`.
* User response required: no
