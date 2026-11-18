<!-- markdownlint-disable-file -->
# RPI Plan: Issue #216 Child Hardening Pass 2 (`RV-001`..`RV-007`)

## Metadata

* Task ID: 216-citation-eval-2142-c2
* Parent task: 216-citation-eval-2142-c1
* Planning date: 2026-11-14
* Planning status: finalized

## Executive Summary

Close all seven remaining findings (`RV-001`..`RV-007`) routed from `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c1-review.md` inside `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md`: mandatory canonical refusal reasons, tamper-evident `gates_report` integrity verification + direct per-case grading in `compare_chat_against_rule_cards`, bundle-bound `grade_chat_turn` verification inside `resolve_regulatory_surface`, explicit versioned-card vs versioned-provision URL documentation and tests, non-Mapping `paired_cards` and empty-card-provision guards, optional `compliance_owner` validation, and recursive `_canon_json` normalization.

## Sources

* .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c2-research.md (`E1`..`E7`)
* .copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-c1-review.md (`RV-001`..`RV-007`)

## Goals and Scope

* Scope: `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md`.
* Non-Goals: Touching `src/agents`, `src/api`, or `pyproject.toml`.

## Functional Requirements

* `FR-1` (`RV-001`): Every refused case in `DEFAULT_EVAL_CASES` carries its exact canonical non-blank `expected_reason`, and `grade_chat_turn` + `_classify_refusal_confusion` require `expected_reason = _nonblank_str(expected.get("reason"))` to be non-`None` and equal to `actual["refusal"]` (and `sections["unknown_or_conflict"]`).
* `FR-2` (`RV-002`): `evaluate_citation_and_refusal_gates` emits `report_integrity_sha256` over the canonical gate report summary, and `compare_chat_against_rule_cards` verifies `report_integrity_sha256`, `threshold_status == "owner_agreed"`, `agreement_gaps == []`, `dataset_gaps == []`, `gate_results["citation_validity"].outcome == PASS`, `gate_results["refusal_accuracy"].outcome == PASS`, non-empty graded & adversarial sets, and direct `grade_chat_turn` + `_classify_refusal_confusion` pass across all `cases` before accepting `gates_report`.
* `FR-3` (`RV-003`): `resolve_regulatory_surface` builds expected turn ground truth from `bundle` (`kind`, `reason`, `expect_out_of_cadence`, `sources`, `facts`, `cards`, `unknown`, `as_of`) and requires `grade_chat_turn(chat_reply, expected_from_bundle) == {"citation_validity": True, "answer_contract": True}` before returning `"chat_with_cards"`.
* `FR-4` (`RV-004`): Document `/api/law/cards/{quote(card_id, safe='')}` (`card_id = id.split("@", 1)[0]`) vs `/api/law/provisions/{quote(provision_id, safe='')}` in `regulatory_eval_gates.py` and `src/core/README.md`, and test versioned `card-alpha@v1` / `card-beta@v1` IDs.
* `FR-5` (`RV-005`): `_score_structural_baseline` rejects non-`Mapping` entries in `paired_cards` without raising `AttributeError`, and `_exact_card_links_match` requires `len(act_card_provs) > 0` for every card in an active `answer` case.
* `FR-6` (`RV-006`): `agreement_gaps` validates both optional `refusal_owner` and optional `compliance_owner` against `COMPLIANCE_GATE_OWNER`.
* `FR-7` (`RV-007`): `_canon_json` recursively normalizes nested `Mapping` and non-string/bytes `Sequence` objects (`dict`/`list` with string keys) before `json.dumps`.

## Acceptance Criteria

* All seven findings (`RV-001`..`RV-007`) are resolved in `src/core` and covered by unit assertions in `test_regulatory_eval_gates_216.py`; bare `mypy`, `ruff check .`, `ruff format --check .`, `test_*216*.py`, `test_dependency_rule.py`, and `test_live_doc_links.py` pass cleanly.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement and Verify `RV-001`..`RV-007` Hardening in `src/core`

* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Apply `RV-001`..`RV-007` fixes in `regulatory_eval_gates.py` and `src/core/README.md`

* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c2-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add regression assertions for `RV-001`..`RV-007` in `test_regulatory_eval_gates_216.py` and verify `src/core`

* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c2-phase-details.md

## Critique Disposition

Single final-candidate critique recorded at `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c2-plan-critique.md` (`PC-001` applied directly: non-finite float normalization + `default=repr` in `_canon_json` and runtime `isinstance(bundle, Mapping)` guard in `deterministic_rule_cards` / `resolve_regulatory_surface`).

## Follow-Up Items

* Optional `src/agents` helper deduplication against `zava_forward.core.regulatory_eval_gates`.
* Out-of-band human threshold sign-off, external held-out legal benchmark, and live staff paired trial with authorised pricing.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c2-changes.md
* Ready phase or task: Complete (`P01` / `P01-T01`, `P01-T02`); ready for `rpi-review`
* Remaining provisional question or blocker: none
