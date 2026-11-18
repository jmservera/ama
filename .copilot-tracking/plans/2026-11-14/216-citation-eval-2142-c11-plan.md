<!-- markdownlint-disable-file -->
# Implementation Plan: Issue #216 Child Hardening Pass 11 (`216-citation-eval-2142-c11`)

* Task ID: `216-citation-eval-2142-c11`
* Parent Task ID: `216-citation-eval-2142-c10`
* Date: `2026-11-14`
* Status: `Finalized`

## Executive Summary

Resolve the three remaining in-scope `src/core` review defects (`RV-023`..`RV-025`) recorded in `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c10-review.md`, incorporating all four direct refinements (`PC-001`..`PC-004`) from `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c11-plan-critique.md`:
1. Emit exact per-card `"provision_ids": list(card["provisions"])` in `RegulatoryChat.bundle` (and return early with cleared `sources`/`facts`/`cards`/`conflict` whenever `result["refusal"]` triggers mid-loop before hazard projection), validate `"provision_ids"` strictly in `_card_provenance_valid` and `_active_cards_link_provisions` (including conflict subset checks and `act_linked == exp_linked` equality in `grade_chat_turn`), and fail closed on ambiguous multi-provision source sharing when `"provision_ids"` is omitted (`RV-023`, `PC-001`, `PC-004`).
2. Add guarded `_active_bundle_nonconflicting(sources, facts, cards)` across `_inspect_bundle_surface` and `grade_chat_turn` (both `citation_validity` and `answer_contract`, plus duplicate-ID checks on conflict bundles and base home-fact path / single-`case_id` checks on active facts) so unflagged `conflict=False` version or duplicate-ID contradictions fail closed (`RV-024`, `PC-003`).
3. Validate `expected["sources"]`, `expected["facts"]`, and `expected["cards"]` unconditionally in `grade_chat_turn` without pre-zeroing them, require empty `sources`/`facts`/`cards` (and `actual` `citations`/`cards`) on `refused` turns and empty `facts` on `conflict` turns across both `citation_validity` and `answer_contract`, and verify `expected` self-consistency in `_classify_refusal_confusion` and `_baseline_projection_matches` so corrupted ground truth cannot pass sub-`1.0` gates as `"false_refusal"` (`RV-025`, `PC-002`, `PC-004`).

## Sources

* `.copilot-tracking/research/2026-11-14/216-citation-eval-2142-c11-research.md`
* `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c10-review.md`
* `src/core/src/zava_forward/core/regulatory_eval_gates.py`
* `src/core/src/zava_forward/core/regulatory_chat.py`
* `src/core/tests/test_regulatory_eval_gates_216.py`
* `src/core/README.md`

## User Decisions and Requirements

* Deliver all locally verifiable Issue #216 acceptance criteria strictly within `src/core`.
* Verify in `src/core` using bare `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*216*.py' -v`.
* Write all `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`), commit cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and do not push.

## Goals

* Close `RV-023`, `RV-024`, and `RV-025` in `src/core` with complete regression test coverage and updated `src/core/README.md` documentation.

## Scope and Non-Goals

* In scope: `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md`.
* Out of scope: `src/api` route changes and `src/agents` helper deduplication.

## Functional Requirements

* `FR-01` (`RV-023` + `PC-001` + `PC-004`): Emit `"provision_ids": list(card["provisions"])` on every card in `RegulatoryChat.bundle`, and if `result["refusal"]` is set mid-loop, clear `result["sources"] = []`, `result["facts"] = []`, `result["cards"] = []`, `result["conflict"] = False` and return immediately before hazard-fact projection. Whenever `"provision_ids" in card`, require a non-empty `_is_nonstr_seq` (rejecting `None`) of unique unstripped `_is_utf8_str` IDs each satisfying `"#" in pid and _id_version_matches(pid, None, allow_fragment=True)` whose base source IDs `{pid.split("@v", 1)[0] for pid in raw_pids}` equal the validated `source_freshness["sources"]` `source_id` set; require `set(card["provision_ids"]).issubset({src.get("id") for src in sources})` on conflict bundles/turns as well, and require `exp_linked is not None and act_linked == exp_linked` and matching `"provision_ids"` key presence in `grade_chat_turn` (`require_active=True`). Fall back to unambiguous source-level matching (`len(cards) == 1` or 1 provision per `sid`) only when `"provision_ids" not in card`.
* `FR-02` (`RV-024` + `PC-002` + `PC-003`): Enforce guarded `_active_bundle_nonconflicting(sources, facts, cards)` (using `.get(...)` and `.split("@v", 1)`, rejecting duplicate `source`/`fact`/`card` IDs, multi-version base `source_id` or base `card_id` sets, duplicate base fact paths `fact_id.rsplit("@", 1)[0]`, and mixed `fact.get("case_id")` values; plus duplicate `source`/`card` ID rejection on `conflict` bundles/turns) across `_inspect_bundle_surface` and both `citation_validity` and `answer_contract` in `grade_chat_turn`.
* `FR-03` (`RV-025` + `PC-002` + `PC-004`): In `grade_chat_turn`, validate `expected.get("sources", ())`, `expected.get("facts", ())`, and `expected.get("cards", ())` unconditionally as `_is_nonstr_seq` of `Mapping`, preserve `expected_sources`, `expected_facts`, and `expected_cards` without pre-zeroing, and require `len(expected_sources) == len(expected_facts) == len(expected_cards) == len(citations_seq) == len(actual_cards_seq) == 0` on `expected_kind == "refused"` and `len(expected_facts) == 0` on `expected_kind == "conflict"` across both `citation_validity` and `answer_contract`. Verify `expected` self-consistency (`grade_chat_turn(render_extractive_answer(expected), expected)`) in `_classify_refusal_confusion` before classifying `"false_refusal"` and in `_baseline_projection_matches` on non-answer turns.
* `FR-04`: Update `src/core/README.md` and add 1 regression test (`test_c11_exact_card_provision_ids_unflagged_version_conflicts_and_expected_refusal_guards`) in `src/core/tests/test_regulatory_eval_gates_216.py` (exact removals: `none`; max test additions: `1`).

## Non-Functional Requirements

* Zero `mypy` errors across `src/core`, clean `ruff check .` and `ruff format --check .`, zero `.copilot-tracking/` strings in Issue #216 files.

## Acceptance Criteria

* Two active cards citing `src@v1#0001` and `src@v1#0002` respectively receive only `[src@v1#0001]` and `[src@v1#0002]` in `deterministic_rule_cards`, while a multi-card bundle omitting `provision_ids` on a multi-provision source fails closed (`cards == []`, `kind == "refused"`).
* An unflagged `conflict=False` bundle containing `src@v1#0001` and `src@v2#0001` (or `card@v1` and `card@v2`, or duplicate IDs) fails closed in `deterministic_rule_cards`, `render_extractive_answer`, `_expected_from_bundle`, and `grade_chat_turn`.
* `grade_chat_turn` returns `{"citation_validity": False, "answer_contract": False}` whenever `expected_kind == "refused"` carries malformed or non-empty `sources`/`facts`/`cards` or `expected_kind == "conflict"` carries malformed or non-empty `facts`.

## Phase Checklist

<!-- P01 -->
### [x] Phase 1 (`P01`): Exact Per-Card Provision Linkage, Unflagged Version-Conflict Rejection, and Expected-Collection Guards

<!-- P01-T01 -->
* [x] `P01-T01`: Implement `RV-023`..`RV-025` in `regulatory_chat.py`, `regulatory_eval_gates.py`, and `src/core/README.md`.

<!-- P01-T02 -->
* [x] `P01-T02`: Add `c11` regression test in `test_regulatory_eval_gates_216.py` and run full `src/core` validation checks.

## Critique Disposition

* Critique artifact: `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c11-plan-critique.md` (`Complete`, `Revise`).
* `PC-001` (High, direct planner correction — Applied): Required strict `"provision_ids" in card` validation (rejecting `None`, enforcing `"#" in pid and _id_version_matches(pid, None, allow_fragment=True)` and base `source_id` parity with `source_freshness["sources"]`, plus conflict subset checks) and `act_linked == exp_linked` equality in `grade_chat_turn`.
* `PC-002` (High, direct planner correction — Applied): Required `expected` self-consistency check (`grade_chat_turn(render_extractive_answer(expected), expected)`) in `_classify_refusal_confusion` (`"false_refusal"` path) and `_baseline_projection_matches` (`not require_active_answer` path) so corrupted `expected` ground truth fails sub-`1.0` gates and baseline comparison.
* `PC-003` (Medium, direct planner correction — Applied): Hardened `_active_bundle_nonconflicting` with `.get(...)` and `.split("@v", 1)`, added base home-fact path / single-`case_id` uniqueness and conflict duplicate-ID checks, and required `_active_bundle_nonconflicting` in `answer_contract` (`safe_fields_ok`) as well as `citation_validity`.
* `PC-004` (Low, direct planner correction — Applied): Returned immediately on mid-loop refusals in `RegulatoryChat.bundle` before hazard-fact projection, and asserted empty `citations_seq` and `actual_cards_seq` inside `safe_fields_ok` on `refused` turns.

## Follow-Up Items

* Cross-package `src/api` route wiring (`RegulatoryChat.surface`) and `src/agents` helper deduplication remain distinct follow-ups outside `src/core`.
