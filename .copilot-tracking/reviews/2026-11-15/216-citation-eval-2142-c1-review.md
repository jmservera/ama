---
title: Review - Rebase #216 Onto Grounding Provenance and Restore Card Envelope Compatibility
description: Single-pass evidence-based RPI review of the #216 rebase, conditional RegulatoryChat card provision_ids disambiguation, deterministic rule-card comparator alias, and cross-package core/agents validation
author: GitHub Copilot
ms.date: 2026-11-15
---

## Review Metadata

* Task slug: `216-citation-eval-2142-c1`
* Plan: .copilot-tracking/plans/2026-11-15/216-citation-eval-2142-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/216-citation-eval-2142-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/216-citation-eval-2142-c1-plan-critique.md
* Changes record: .copilot-tracking/changes/2026-11-15/216-citation-eval-2142-c1-changes.md
* Research: .copilot-tracking/research/2026-11-15/216-citation-eval-2142-c1-research.md
* Scope reviewed: Full plan (`P01`–`P03`: `P01-T01`, `P02-T01`, `P02-T02`, `P03-T01`)
* Execution status: Complete
* Outcome: Conformant

## Executive Summary

Execution of the single-pass review across the reconciled `2026-11-15` `216-citation-eval-2142-c1` artifact set and workspace diff is **Complete**, with outcome **Conformant**. Branch `feat/ai-216-citation-eval-2142` (PR `#1774`) is cleanly rebased onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`) with all `2026-11-15` `c1` artifacts preserved. `RegulatoryChat.bundle()` (`src/core/src/zava_forward/core/regulatory_chat.py`) now attaches `provision_ids` strictly when `len(result["cards"]) > 1` and a card's base `source_id` maps to multiple provisions in `sources`, restoring exact 10-field `regulatory-chat-v1` card compatibility for `src/agents` while preserving fail-closed multi-card shared-source linkage in `src/core`. `compare_chat_against_deterministic_rule_cards` is exported in `src/core/src/zava_forward/core/regulatory_eval_gates.py` and documented in `src/core/README.md`, `test_c23_single_card_envelope_compatibility_and_deterministic_comparator_alias` covers both envelope parity and the comparator alias, and both verbatim Required Step 5 verification commands (`src/core` and `src/agents`) pass with zero lint, format, or strict `mypy` issues. Zero defects, decision gaps, or research gaps remain; repository-level human governance gates for Issue `#216` remain routed as distinct follow-up work (`Refs #216`).

## Findings

### RV-001: Issue #216 human governance and live-trial gates remain distinct post-harness follow-up work

* Severity: Low
* Category: Residual work
* Related IDs: Plan `## Follow-Up Items`, `AC-4`, Issue `#216`
* Evidence: .copilot-tracking/plans/2026-11-15/216-citation-eval-2142-c1-plan.md (`## Follow-Up Items`), .copilot-tracking/changes/2026-11-15/216-citation-eval-2142-c1-changes.md (`## Follow-Up Items`), src/core/README.md (`#216` evaluation gates documentation).
* Impact: Offline executable gates, deterministic rule-card shipping comparators, and `src/core` + `src/agents` parity are complete (`ship_mode == "deterministic_cards_only"` fail-closed default until human agreement and live observations are supplied), while full Issue `#216` closure continues to require human `OwnerGateAgreement` dual-capacity sign-off (Legal/DPO and Compliance/Building Safety owners), a live non-synthetic staff paired trial across `repairs`, `housing`, and `grants`, and `BRD OD-51` unit-cost ceiling ratification (`Refs #216`, not `Closes #216`).
* Recommended destination: Follow-up item (human governance / operational trial workstream outside offline executable scope; does not downgrade `Conformant` verdict per plan follow-up boundary).

## Requirement and Criterion Trace

| Requirement or criterion | Status | Evidence | Notes |
|--------------------------|--------|----------|-------|
| `FR-1`: Conditional `provision_ids` emission in `RegulatoryChat.bundle()` | Satisfied | src/core/src/zava_forward/core/regulatory_chat.py (`bundle()`), src/core/tests/test_regulatory_eval_gates_216.py (`test_c11`, `test_c23`) | Emits exact 10-key `regulatory-chat-v1` card dicts on single-card and distinct-source multi-card bundles; attaches `provision_ids` when `len(result["cards"]) > 1` shares a multi-provision `source_id`, matching `_active_cards_link_provisions` 1-for-1 |
| `FR-2`: Export `compare_chat_against_deterministic_rule_cards` alias | Satisfied | src/core/src/zava_forward/core/regulatory_eval_gates.py, src/core/tests/test_regulatory_eval_gates_216.py (`test_c23`) | Module-level `compare_chat_against_deterministic_rule_cards = compare_chat_against_rule_cards` verified by `assertIs` and functional execution |
| `FR-3`: Update `src/core/README.md` | Satisfied | src/core/README.md | Documents `compare_chat_against_deterministic_rule_cards` alias and conditional `provision_ids` multi-card shared-source disambiguation |
| `NFR-1`: Rebase onto `36aeddae345426fdf8ee53565fef1540979de967` preserving `2026-11-15` `c1` files | Satisfied | `git merge-base --is-ancestor 36aeddae345426fdf8ee53565fef1540979de967 HEAD` (exit `0`), `.copilot-tracking/**/2026-11-15/216-citation-eval-2142-c1-*` | Rebased commit `be8fa85cb` sits cleanly atop `36aeddae3`; critique dispositions `PC-001` and `PC-004` satisfied |
| `NFR-2`: Focused validation tier across `src/core` and `src/agents` without modifying `src/agents` production logic or recorded report | Satisfied | .copilot-tracking/changes/2026-11-15/216-citation-eval-2142-c1-changes.md (`## Validation Record`), `git diff src/agents/` | Zero edits to `src/agents/src/`, `regulatory_gate_fixture.py`, or `src/agents/evals/regulatory_gates_results.json`; only 3-line `_TESTS_DIR` `sys.path` guard added in 2 test files per `PC-002` |
| `AC-1`: Ancestor check `36aeddae345426fdf8ee53565fef1540979de967` | Satisfied | `git merge-base --is-ancestor 36aeddae345426fdf8ee53565fef1540979de967 HEAD` exited `0` | Verified in `P01-T01` |
| `AC-2`: Verbatim `src/core` test + lint + format + `mypy` command | Satisfied | `Ran 89 tests in 97.805s — OK`, `ruff check .` passed, `ruff format --check .` (`291 files`), `mypy` (`344 source files`) | All exited `0` |
| `AC-3`: Verbatim `src/agents` test + lint + format + `mypy` command | Satisfied | `Ran 27 tests in 52.437s — OK` (plus `discover` `40 tests in 40.773s — OK`), `ruff check .` passed, `ruff format --check .` (`62 files`), `mypy` (`66 source files`) | All exited `0` including exact parity with `evals/regulatory_gates_results.json` |
| `AC-4`: Complete `2026-11-15` `c1` RPI artifact chain + local commit (`Refs #216`, Copilot trailer, no `git push`) | Satisfied | `.copilot-tracking/{research,plans,details,reviews/plans,changes,reviews,rpi-sessions}/**/2026-11-15/216-citation-eval-2142-c1-*` | All phase artifacts complete and reconciled; single final commit staged immediately upon `Follow-up` state persistence so `review.md` and `state.json` are committed cleanly together without `git push` |

## Implementation-Time Updates Assessment

* Updates found: One pre-authorized implementation-time detail update (`Activate PC-002 Test Import-Path Fallback in Two Target Agents Test Modules` in `changes.md` and `P03` of `phase-details.md`), adding `_TESTS_DIR = str(Path(__file__).resolve().parent)` to `sys.path` in `src/agents/tests/test_regulatory_citation_card_gates.py` and `src/agents/tests/test_regulatory_gates.py`.
* Rationale and evidence quality: Clear and directly evidenced by running the caller's exact Step 5 `PYTHONPATH=../core/src:src:../core/tests python3 -m unittest tests/test_regulatory_citation_card_gates.py tests/test_regulatory_gates.py -q` command, which otherwise lacks `src/agents/tests` on `sys.path` when invoked by file path rather than `discover -s tests`.
* User intent preserved: Yes — ensures the caller's verbatim command exits `0` while keeping `src/agents` production modules, fixtures, and recorded evaluation report untouched, matching the existing repository idiom in `src/core/tests/test_regulatory_eval_gates_216.py` and critique disposition `PC-002`.
* Material revision readiness: Current and reconciled across `plan.md`, `phase-details.md`, and `changes.md`; no planning return required.

## Plan Follow-Up Items Assessment

* Follow-up items recorded: Human governance gates for Issue `#216` (`OwnerGateAgreement` dual-capacity sign-off by Legal/DPO and Compliance/Building Safety owners, live non-synthetic staff paired trial across `repairs`, `housing`, and `grants`, and `BRD OD-51` unit-cost ceiling ratification).
* Current relevance: Remains current and necessary before closing `#216` or switching live deployment from `deterministic_cards_only` to `chat_with_cards`.
* Scope boundary preserved: Yes — kept out of offline harness implementation scope and commit closing keywords (`Refs #216` enforced).
* Recommended routing: Distinct follow-up workstream (`RV-001`) plus optional hosted CI re-check once the owner pushes the rebased branch.

## Validation Assessment

* Executed checks:
  * `git merge-base --is-ancestor 36aeddae345426fdf8ee53565fef1540979de967 HEAD` -> Passed (`0`)
  * `cd src/core && PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*regulatory*.py" -q && ruff check . && ruff format --check . && mypy` -> Passed (`89` tests, `ruff`, `mypy` on `344` files)
  * `cd src/agents && PYTHONPATH=../core/src:src:../core/tests python3 -m unittest tests/test_regulatory_citation_card_gates.py tests/test_regulatory_gates.py -q && ruff check . && ruff format --check . && mypy` -> Passed (`27` tests, `ruff`, `mypy` on `66` files)
  * `cd src/agents && PYTHONPATH=../core/src:src:../core/tests python3 -m unittest discover -s tests -p "test_*regulatory*.py" -q` -> Passed (`40` tests)
  * `cd src/api && PYTHONPATH=../core/src:../agents/src:src:../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_*regulatory*.py" -q` -> Passed (`75` tests)
  * `python3 tools/rename-zava-tests.py` -> Passed (`25` tests)
  * Production/test diff audit for `.copilot-tracking/` leakage -> Passed (`0` matches in `src/`)
* Missing or skipped checks:
  * `tools/rpi-checks.py` skipped per focused validation tier (`D4` / `#1294`) and explicit caller exclusion.
  * Hosted GitHub Actions CI on PR `#1774` (`src-core`, `src-agents`, `src-api`) unobserved on the new local commit because caller Step 6 explicitly forbids `git push`.
* Assessment: Focused local validation coverage is complete, reproducible, and proves both the regression fix and cross-package compatibility across `src/core`, `src/agents`, and `src/api`.

## Outcome and Routing

* Execution status: Complete
* Outcome: Conformant
* `rpi-implement`: None (zero code/test/documentation defects).
* `rpi-plan`: None (zero unaccepted or divergent decision gaps).
* `rpi-research`: None (zero evidence gaps).
* Follow-up items:
  1. Push rebased `feat/ai-216-citation-eval-2142` when owner-authorized and confirm hosted PR `#1774` checks (`src-agents`, `src-core`, `src-api`) turn green against `feat/demo-164-chat-grounding-provenance-0900`.
  2. Complete human governance gates for `#216` (`OwnerGateAgreement` dual-capacity Legal/DPO + Compliance/Building Safety sign-off, live non-synthetic paired staff trial across `repairs`, `housing`, and `grants`, and `BRD OD-51` unit-cost ceiling ratification) before closing `#216`.
