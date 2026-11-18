<!-- markdownlint-disable-file -->
# RPI Plan: Issue #216 Child Closure (`RV-001`..`RV-006`) in `src/core`

## Metadata

* Task ID: 216-citation-eval-2142-c1
* Parent task: 216-citation-eval-2142
* Planning date: 2026-11-14
* Planning status: finalized

## Executive Summary

Close all six fail-closed defects (`RV-001`..`RV-006`) routed from parent review `.copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-review.md` inside `src/core/src/zava_forward/core/regulatory_eval_gates.py` and `src/core/tests/test_regulatory_eval_gates_216.py`: exact extractive section matching, `evaluated_outputs_sha256` report-to-cases binding, critical severity on any `cards`-arm or `chat`-arm hazard miss, named gate-owner binding on both `OwnerGateAgreement` (`LEGAL_GATE_OWNER`) and `benefit_thresholds` (`COMPLIANCE_GATE_OWNER`), exact URL-encoded card/provision link and per-card provision mapping parity, and overflow-safe `_finite_float` token conversion in `cost_per_accepted_check`.

## Sources

* .copilot-tracking/research/2026-11-14/216-citation-eval-2142-c1-research.md (`E1`..`E6`)
* .copilot-tracking/reviews/2026-11-14/216-citation-eval-2142-review.md (`RV-001`..`RV-006`)
* .copilot-tracking/plans/2026-11-14/216-citation-eval-2142-plan.md

## User Decisions and Requirements

* Deliver both locally verifiable Issue #216 acceptance criteria in `src/core` without fail-open edge cases (`RV-001`..`RV-006`).
* Preserve `ALLOWED = {"core"}`, zero `pyproject.toml` relaxations, and clean verification under bare `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*216*.py' -v`.

## Goals

* Harden `zava_forward.core.regulatory_eval_gates` so every routed review finding (`RV-001`..`RV-006`) fails closed deterministically.
* Add direct regression assertions for all six findings in `src/core/tests/test_regulatory_eval_gates_216.py` without adding new test files.

## Scope and Non-Goals

* Scope: `src/core/src/zava_forward/core/regulatory_eval_gates.py`, `src/core/tests/test_regulatory_eval_gates_216.py`, and `src/core/README.md` (if precision note needed).
* Non-Goals: Editing `src/agents`, `src/api`, `pyproject.toml`, or operational sign-off artifacts.

## Functional Requirements

* `FR-1` (`RV-001`, `PC-001`): `grade_chat_turn` requires exact canonical extractive strings across all sections for `answer`, `conflict`, and `refused` turns (including `expected.get("unknown") or "No permitted structured home fact selected for this purpose."`, exact `FRESH_SNAPSHOT_NOTE` / `STALE_SNAPSHOT_NOTE` on `unknown_or_conflict`, and exact `refused` section strings), rejecting appended unsupported claims anywhere.
* `FR-2` (`RV-002`, `PC-005`): `evaluate_citation_and_refusal_gates` emits `evaluated_outputs_sha256` over `(id, set_name, scenario, question, expected, actual)`, and `compare_chat_against_rule_cards` requires `gates_report.get("schema") == EVAL_SCHEMA` and `gates_report.get("evaluated_outputs_sha256") == evaluated_outputs_digest(cases)`, resetting `beside_cost` gate rates/outcomes to `None`/`UNKNOWN` when unbound.
* `FR-3` (`RV-003`): `compare_chat_against_rule_cards` treats any `hazard_missed is True` across `chat`, `cards`, or unpaired observations as `failure_severity = "critical"` and blocks `measured_value`.
* `FR-4` (`RV-004`, `PC-004`): `agreement_gaps` requires `_canon_name(owner) == _canon_name(LEGAL_GATE_OWNER)` and rejects parenthetical-capacity self-grading aliases (`_canon_name(name.split("(", 1)[0])`), while `_validate_benefit_thresholds` requires `_canon_name(owner) == _canon_name(COMPLIANCE_GATE_OWNER)`.
* `FR-5` (`RV-005`, `PC-003`): `_score_structural_baseline` guards `Mapping`/`list` types and `_nonblank_str` IDs before `quote(..., safe="")`, checking exact URL-encoded `/api/law/cards/{quote(card_id, safe='')}` and `/api/law/provisions/{quote(prov_id, safe='')}` links and exact per-card `provisions` `(id, link)` parity against `deterministic_rule_cards(expected)`.
* `FR-6` (`RV-006`, `PC-002`): `cost_per_accepted_check` converts `in_tokens`, `out_tokens`, and `accepted_count` via `_finite_float` after `_strict_int` validation before float arithmetic, returning `"Unknown"` cleanly on huge-integer float overflow (such as `10**400`).

## Non-Functional Requirements

* Zero new files (`0` test removals, `0` new test files; edit existing `src/core/tests/test_regulatory_eval_gates_216.py`).
* Strict `mypy` (`strict = true`), `ruff check .`, `ruff format --check .`, `test_*216*.py`, and `test_dependency_rule.py` pass cleanly.

## Acceptance Criteria

* All six routed defects (`RV-001`..`RV-006`) are fixed in `regulatory_eval_gates.py` and verified by failing-without-fix unit assertions in `test_regulatory_eval_gates_216.py`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Close Fail-Open Grading, Binding, Link-Parity, and Overflow Defects (`RV-001`..`RV-006`)

* Intent: Harden `regulatory_eval_gates.py` and extend `test_regulatory_eval_gates_216.py` + `src/core/README.md` to close `RV-001`..`RV-006`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Harden `regulatory_eval_gates.py` for `RV-001`..`RV-006`

* Requirement and evidence: `FR-1`..`FR-6` (`E1`..`E6`).
* Expected result: `grade_chat_turn`, `evaluated_outputs_digest`, `evaluate_citation_and_refusal_gates`, `agreement_gaps`, `_validate_benefit_thresholds`, `cost_per_accepted_check`, `_score_structural_baseline`, `_score_paired_observations`, `compare_chat_against_rule_cards`, and `resolve_regulatory_surface` fail closed on all six edge cases.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c1-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add regression assertions in `test_regulatory_eval_gates_216.py` and run `src/core` checks

* Requirement and evidence: `FR-1`..`FR-6`, `NFR` (`E1`..`E6`).
* Expected result: `test_regulatory_eval_gates_216.py` asserts appended unsupported claims fail grading, mutated cases after `gates_report` fail comparison, `cards`-arm hazard misses trigger `critical` severity and `cards_only`, wrong gate owners fail `agreement_gaps` and `benefit_thresholds`, swapped card provisions or wrong link paths fail structural link parity, and `10**400` tokens return `"Unknown"` without raising `OverflowError`; `mypy`, `ruff`, and `unittest` pass cleanly.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/216-citation-eval-2142-c1-phase-details.md

## Dependencies

* `zava_forward.core.regulatory_eval_gates` and `src/core/tests/test_regulatory_eval_gates_216.py` from parent task `216-citation-eval-2142`.

## Critique Disposition

Single final-candidate critique executed at `.copilot-tracking/reviews/plans/2026-11-14/216-citation-eval-2142-c1-plan-critique.md` (`Verdict: Revise`; `PC-001`..`PC-005`). All five findings applied directly:

* `PC-001` (applied): Aligned empty-facts fallback in `grade_chat_turn` with `render_extractive_answer` (`str(expected.get("unknown") or "No permitted structured home fact selected for this purpose.")`) and required exact canonical equality on `refused` sections and `answer` `unknown_or_conflict` (`STALE_SNAPSHOT_NOTE` / `FRESH_SNAPSHOT_NOTE`).
* `PC-002` (applied): Converted `accepted_count` via `_finite_float` alongside `in_tokens` and `out_tokens` after `_strict_int` validation in `cost_per_accepted_check` so `accepted_checks = 10**400` also returns `"Unknown"` without `OverflowError`.
* `PC-003` (applied): Guarded `Mapping`/`list` types and `_nonblank_str` IDs before `quote(..., safe="")` in `_score_structural_baseline`.
* `PC-004` (applied): Added base-person alias normalization (`_canon_name(name.split("(", 1)[0])`) to `agreement_gaps` so same-person parenthetical capacity suffixes cannot bypass `independent_grader` separation.
* `PC-005` (applied): Gated `cit_check`/`ref_check` in `compare_chat_against_rule_cards` and `beside_cost` on `gates_report.get("schema") == EVAL_SCHEMA` and matching `evaluated_outputs_sha256`, resetting unbound outcomes to `UNKNOWN`.

## Follow-Up Items

* Optional refactoring in `src/agents`: Delegate duplicated pure evaluation logic in `src/agents/src/zava_forward/agents/regulatory_chat/` to `zava_forward.core.regulatory_eval_gates` in a dedicated `src/agents` task.
* Operational owner threshold agreement, external held-out legal benchmark, and live staff paired trial with authorised pricing: Out-of-band human governance prerequisites before live chat enablement.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/216-citation-eval-2142-c1-changes.md
* Ready phase or task: Completed (`P01` verified; ready for Review)
* Remaining provisional question or blocker: none
