<!-- markdownlint-disable-file -->
# RPI Plan: Issue #216 PR #1774 CI Correction Cycle 1

## Task Metadata

* Task ID: 216-citation-eval-2142-c1
* Task slug: 216-citation-eval-2142-c1
* Planning status: Approved for implementation
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/216-citation-eval-2142-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/216-citation-eval-2142-c1-plan-critique.md

## Executive Summary

Rebase PR `#1774` (`feat/ai-216-citation-eval-2142`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`) while preserving the `2026-11-15` `c1` tracking files, and fix the `src-agents` CI regression in `RegulatoryChat.bundle()` (`src/core/src/zava_forward/core/regulatory_chat.py`). Instead of unconditionally adding `provision_ids` to every card dictionary (which broke `src/agents` exact `regulatory-chat-v1` 10-field card contract equality and propagated into `refusal_accuracy.failed_case_ids` across all 6 `answer` cases), `RegulatoryChat.bundle()` will attach `provision_ids` only when disambiguating multi-card bundles (`len(result["cards"]) > 1`) whose `sources` contain multiple provisions for a card's base `source_id`. We also export `compare_chat_against_deterministic_rule_cards` (including `__all__` parity) as a compatibility alias for `compare_chat_against_rule_cards` in `src/core/src/zava_forward/core/regulatory_eval_gates.py`, update `src/core/README.md`, add focused regression coverage in `src/core/tests/test_regulatory_eval_gates_216.py`, validate `src/core` and `src/agents` verbatim under the focused tier, and commit locally with `Refs #216` without pushing.

### User Decisions and Requirements Highlights

* Rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`), preserving the `2026-11-15` `c1` tracking files across the rebase.
* Preserve `src/agents` answer-versus-refusal classification and frozen `regulatory-chat-v1` evaluation gates (`test_regulatory_citation_card_gates.py` and `test_regulatory_gates.py`, including the 60,000-home `evals/regulatory_gates_results.json` parity test) while keeping all `#216` citation/refusal gates and deterministic rule-card comparison tests passing in `src/core`.
* Validate strictly under the focused tier (`unittest`, `ruff check .`, `ruff format --check .`, `mypy` in `src/core` and `src/agents` using the caller's exact commands), write dated `2026-11-15` `c1` RPI artifacts, and commit locally with `Refs #216` and the Copilot trailer without running `tools/rpi-checks.py` or `git push`.

### What You May Not Know

* Neither branch contains `regulatory_assistant.py`; upstream triage inferred a refusal-pattern false positive because `src/agents/src/zava_forward/agents/regulatory_gates.py` defines `refusal_ok = answer_contract and citation_validity` on `answer` cases, so `actual["cards"] != expected["cards"]` (caused by the extra `provision_ids` key) surfaced all 6 `answer` case IDs under `refusal_accuracy.failed_case_ids`.
* PR `#1774`'s checked-out head branch in worktree `/home/azureuser/source/ama-demo-wt/feat-216-citation-eval-2142` is `feat/ai-216-citation-eval-2142` (no `feat/demo-216-citation-eval-2142` ref exists locally or on `origin`), so rebasing `feat/ai-216-citation-eval-2142` in place preserves PR `#1774` lineage cleanly.

### Unresolved Decisions or Blockers

* None for implementation. Repository-level human governance items for `#216` (`OwnerGateAgreement` dual-capacity sign-off, live staff paired trial, and `BRD OD-51` unit-cost ratification) remain open outside code scope, so the commit uses `Refs #216`.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Fetch `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`) and rebase the `#216` topic branch onto it in `/home/azureuser/source/ama-demo-wt/feat-216-citation-eval-2142`, preserving the `2026-11-15` `c1` tracking files across the rebase (caller prompt; branch verified as `feat/ai-216-citation-eval-2142` via `C1` and re-verified on fetch per `PC-004`).
* Fix the `src/core` regulatory chat / gate regression that caused `src-agents` CI (`PR #1774`, job `132718061819`) to fail on `['automated-source', 'lookup-hazard', 'lookup-home', 'lookup-emergency', 'source-injection', 'stale-source-label']` while preserving `#216` `evaluate_citation_and_refusal_gates` and `compare_chat_against_deterministic_rule_cards` across both `src/core` and `src/agents` (caller prompt; root cause localized to `src/core/src/zava_forward/core/regulatory_chat.py` and `regulatory_eval_gates.py` via `C3`–`C9`).
* Write dated `2026-11-15` `c1` RPI artifacts under `.copilot-tracking/research/2026-11-15/`, `.copilot-tracking/plans/2026-11-15/`, `.copilot-tracking/details/2026-11-15/`, `.copilot-tracking/reviews/plans/2026-11-15/`, `.copilot-tracking/changes/2026-11-15/`, and `.copilot-tracking/reviews/2026-11-15/` (caller prompt).
* Run focused-tier validation only (`unittest`, `ruff check .`, `ruff format --check .`, `mypy` in `src/core` and `src/agents`, including the caller's exact Step 5 commands verbatim); do NOT run `tools/rpi-checks.py` (caller prompt).
* Commit locally with `Refs #216` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` using privacy-safe GitHub noreply email; do NOT `git push` (caller prompt + `.github/copilot-instructions.md`).

## Goals

* Rebase `feat/ai-216-citation-eval-2142` cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`) with `2026-11-15` `c1` tracking files preserved.
* Restore exact `regulatory-chat-v1` 10-field card contract compatibility on unambiguous `RegulatoryChat.bundle()` lookups so all `src/agents` regulatory evaluation tests and the committed 60,000-home `evals/regulatory_gates_results.json` oracle pass unchanged.
* Preserve fail-closed multi-card shared-source `provision_ids` disambiguation (`RV-023`) and export `compare_chat_against_deterministic_rule_cards` alongside `compare_chat_against_rule_cards` and `evaluate_citation_and_refusal_gates` in `src/core`.

## Scope and Non-Goals

### In Scope

* Fetching `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`), verifying branch refs, and rebasing `feat/ai-216-citation-eval-2142` onto it while preserving the `2026-11-15` `c1` tracking files.
* Updating `RegulatoryChat.bundle()` in `src/core/src/zava_forward/core/regulatory_chat.py` to emit `provision_ids` on cards only when `len(result["cards"]) > 1` and multiple bundle `sources` share a card's base `source_id`.
* Exporting `compare_chat_against_deterministic_rule_cards = compare_chat_against_rule_cards` (with `__all__` parity) in `src/core/src/zava_forward/core/regulatory_eval_gates.py` (and package `__init__.py` if `compare_chat_against_rule_cards` is re-exported there) and documenting the conditional `provision_ids` behavior in `src/core/README.md`.
* Adding one focused regression test method in `src/core/tests/test_regulatory_eval_gates_216.py` covering single-card 10-key `regulatory-chat-v1` envelope compatibility, multi-card shared-source `provision_ids` emission, and the `compare_chat_against_deterministic_rule_cards` alias.
* Running verbatim focused validation (`unittest`, `ruff check .`, `ruff format --check .`, `mypy`) across `src/core` and `src/agents` (plus minimal test-import-path fallback in `src/agents/tests/test_regulatory_citation_card_gates.py` and `test_regulatory_gates.py` if and only if verbatim `PYTHONPATH=../core/src:src:../core/tests` fails with `ModuleNotFoundError`), completing `rpi-review`, and creating the local git commit after review.

### Non-Goals

* Modifying `src/agents/src/`, `src/agents/tests/regulatory_gate_fixture.py`, `src/agents/evals/regulatory_gates_results.json`, `src/api/`, `src/orchestrator/`, `src/importer/`, or `infra/`.
* Weakening `_REFUSAL_PATTERNS` or `refuse_question` in `regulatory_eval_gates.py`.
* Running `tools/rpi-checks.py` or pushing to `origin` (`git push`).

## Functional Requirements

* FR-1: `RegulatoryChat.bundle()` omits `provision_ids` from returned card dictionaries when `len(result["cards"]) <= 1` or when every referenced base `source_id` has a single provision in `result["sources"]`.
  * Observable acceptance criteria: Single-card and distinct-source active `RegulatoryChat.bundle()` outputs contain the exact 10 `regulatory-chat-v1` card keys (`id`, `status`, `approved_by`, `approved_on`, `effective`, `exercise`, `link`, `safe_default`, `clock`, `source_freshness`), and all 4 previously failing tests in `src/agents/tests/test_regulatory_citation_card_gates.py` and `src/agents/tests/test_regulatory_gates.py` pass.
* FR-2: `RegulatoryChat.bundle()` attaches `provision_ids=list(card["provisions"])` to returned card dictionaries whenever `len(result["cards"]) > 1` and any card's `card["provisions"]` belongs to a base `source_id` (`pid.split("@v", 1)[0]`) that maps to more than one provision in `sources`.
  * Observable acceptance criteria: `test_c11_exact_card_provision_ids_unflagged_version_conflicts_and_expected_refusal_guards` and all `#216` evaluation tests in `src/core/tests/test_regulatory_eval_gates_216.py` pass.
* FR-3: `zava_forward.core.regulatory_eval_gates` exports `compare_chat_against_deterministic_rule_cards` bound to `compare_chat_against_rule_cards` (with matching `__all__` / re-export parity) alongside `evaluate_citation_and_refusal_gates`.
  * Observable acceptance criteria: Importing and calling `compare_chat_against_deterministic_rule_cards` returns identical results to `compare_chat_against_rule_cards` and appears in `__all__` wherever `compare_chat_against_rule_cards` is listed.

## Non-Functional Requirements

* NFR-1: Focused-tier static, format, type, and unit-test conformance across `src/core` and `src/agents`.
  * Objective threshold or evaluation condition: Zero test failures, zero `ruff check` or `ruff format --check` errors, and zero `mypy` errors across both `src/core` and `src/agents` under the exact Step 5 verification commands.
  * Operating condition or verification approach: Run verbatim `unittest`, `ruff check .`, `ruff format --check .`, and `mypy` commands in `src/core` and `src/agents` after rebasing onto `36aeddae345426fdf8ee53565fef1540979de967`.
  * Observable acceptance criteria: All focused validation commands exit `0`.
* NFR-2: Bounded test-suite discipline and backward-compatible frozen artifact preservation.
  * Objective threshold or evaluation condition: Exact test removals = `none`; maximum test additions = `1` test method (`test_c23_single_card_envelope_compatibility_and_deterministic_comparator_alias`) in `src/core/tests/test_regulatory_eval_gates_216.py`; zero modifications to `src/agents/src/`, `src/agents/tests/regulatory_gate_fixture.py`, or `src/agents/evals/regulatory_gates_results.json` (and zero edits anywhere in `src/agents/` unless verbatim `PYTHONPATH=../core/src:src:../core/tests` requires a non-behavioral `tests/` path guard in the two target test files).
  * Observable acceptance criteria: `src/agents/evals/regulatory_gates_results.json` is completely unchanged and `test_recorded_60000_home_report_matches_exact_rerun` passes.

## Acceptance Criteria

* AC-1: `feat/ai-216-citation-eval-2142` has `36aeddae345426fdf8ee53565fef1540979de967` (`origin/feat/demo-164-chat-grounding-provenance-0900`) as its ancestor, with all `2026-11-15` `c1` tracking files preserved.
* AC-2: `cd src/core && PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*regulatory*.py" -q && ruff check . && ruff format --check . && mypy` exits `0`.
* AC-3: `cd src/agents && PYTHONPATH=../core/src:src:../core/tests python3 -m unittest tests/test_regulatory_citation_card_gates.py tests/test_regulatory_gates.py -q && ruff check . && ruff format --check . && mypy` (as well as `unittest discover -s tests -p "test_*regulatory*.py" -q`) exits `0` with zero changes to `src/agents/src/`, `regulatory_gate_fixture.py`, or `evals/regulatory_gates_results.json`.
* AC-4: Dated `2026-11-15` `c1` RPI artifacts exist under `research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews`, and `rpi-sessions`, and changes are committed locally with privacy-safe git email, `Refs #216`, and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` (`git status --short` clean) without `git push`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/216-citation-eval-2142-c1-plan.md                                                                     |
| Phase details                    | .copilot-tracking/details/2026-11-15/216-citation-eval-2142-c1-phase-details.md                                                          |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/216-citation-eval-2142-c1-plan-critique.md (`Complete`, `Revise`; `PC-001`–`PC-004` applied)  |
| Relevant research                | .copilot-tracking/research/2026-11-15/216-citation-eval-2142-c1-research.md                                                              |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/216-citation-eval-2142-c1-changes.md is created by implementation as its evidence record            |
| Planning execution and readiness | Approved for implementation after applying single-pass `rpi-plan-critique` direct planner corrections                                    |
| Continuation context             | Confirmed automatic RPI Agent parent transitions directly to `Implement` (`P01-T01`)                                                     |

## Sources

* .copilot-tracking/research/2026-11-15/216-citation-eval-2142-c1-research.md: Evidence `C1`–`C10` establishing root cause, branch ancestry, and convergence recommendation.
* src/core/src/zava_forward/core/regulatory_chat.py: `RegulatoryChat.bundle()` card construction and multi-card source linkage.
* src/core/src/zava_forward/core/regulatory_eval_gates.py: `_active_cards_link_provisions`, `evaluate_citation_and_refusal_gates`, and `compare_chat_against_rule_cards`.
* src/agents/src/zava_forward/agents/regulatory_gates.py and src/agents/tests/regulatory_gate_fixture.py: Frozen 10-key `regulatory-chat-v1` card contract oracle and `refusal_accuracy` coupling.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Rebase Topic Branch Onto Target Parent

* Intent: Rebase `feat/ai-216-citation-eval-2142` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`) while preserving `2026-11-15` `c1` RPI session/planning files intact.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Fetch and rebase onto origin/feat/demo-164-chat-grounding-provenance-0900

* Requirement and evidence: AC-1; research `C1`, `C2`; critique `PC-001`, `PC-004`.
* Expected result: `git merge-base --is-ancestor 36aeddae345426fdf8ee53565fef1540979de967 HEAD` exits `0` with zero merge conflicts on `feat/ai-216-citation-eval-2142` and all `2026-11-15` `c1` tracking files preserved.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/216-citation-eval-2142-c1-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Fix RegulatoryChat Card Envelope Compatibility and Alias

* Intent: Emit `provision_ids` in `RegulatoryChat.bundle()` strictly when disambiguating multi-card shared-source bundles, export `compare_chat_against_deterministic_rule_cards`, update `src/core/README.md`, and add focused regression coverage.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Gate provision_ids emission in RegulatoryChat.bundle() and export comparator alias

* Requirement and evidence: FR-1, FR-2, FR-3; research `C4`–`C9`; critique `PC-003`.
* Expected result: `RegulatoryChat.bundle()` preserves the 10-key `regulatory-chat-v1` card envelope on single-card and distinct-source bundles while emitting `provision_ids` when `len(result["cards"]) > 1` shares a multi-provision `source_id`, `compare_chat_against_deterministic_rule_cards` is exported in `regulatory_eval_gates.py`, and `src/core/README.md` reflects both.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/216-citation-eval-2142-c1-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Add focused regression coverage in test_regulatory_eval_gates_216.py

* Requirement and evidence: FR-1, FR-2, FR-3, NFR-2; research `C5`, `C8`, `C9`.
* Expected result: `test_c23_single_card_envelope_compatibility_and_deterministic_comparator_alias` asserts single-card 10-key envelope parity (`"provision_ids" not in card`), multi-card distinct-source omission vs multi-card shared-source `provision_ids` inclusion, and `compare_chat_against_deterministic_rule_cards is compare_chat_against_rule_cards`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/216-citation-eval-2142-c1-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Validation across Core and Agents

* Intent: Verify all unit tests, `ruff check`, `ruff format --check`, and `mypy` in both `src/core` and `src/agents` under the exact caller verification commands and record implementation evidence before `rpi-review` and final local commit.
* Dependencies: P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Execute src/core and src/agents focused validation suites and changes record

* Requirement and evidence: NFR-1, NFR-2, AC-2, AC-3, AC-4; research `C10`; critique `PC-002`.
* Expected result: All `src/core` and `src/agents` regulatory unit tests (including verbatim Step 5 `tests/test_regulatory_citation_card_gates.py tests/test_regulatory_gates.py` with minimal `_TESTS_DIR` `sys.path` guard per `PC-002`, plus `discover`), `ruff check .`, `ruff format --check .`, and `mypy` pass with exit code `0`, and `.copilot-tracking/changes/2026-11-15/216-citation-eval-2142-c1-changes.md` is complete for `rpi-review` (with local git commit finalized once `rpi-review` artifacts are written so the commit captures the full RPI loop cleanly).
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/216-citation-eval-2142-c1-phase-details.md

## Dependencies

* `origin/feat/demo-164-chat-grounding-provenance-0900` (`36aeddae345426fdf8ee53565fef1540979de967`): Parent PR `#1641` branch tip onto which `feat/ai-216-citation-eval-2142` must rebase.
* Local Python 3.12 toolchain (`unittest`, `ruff`, `mypy`): Required to validate both `src/core` and `src/agents`.

## Critique Disposition

Single-pass `rpi-plan-critique` completed (`Complete`, verdict `Revise`, `.copilot-tracking/reviews/plans/2026-11-15/216-citation-eval-2142-c1-plan-critique.md`):

* `PC-001` [High] (Applied directly): Updated target rebase SHA across plan and phase details from `243764945ea8f5b292eed0b73ea034b91c3b6e5f` to `36aeddae345426fdf8ee53565fef1540979de967` and required preserving all `2026-11-15` `c1` tracking files across the rebase.
* `PC-002` [High] (Applied directly): Required `P03-T01` and `AC-3` to execute the caller's exact Step 5 `src/agents` command verbatim (`PYTHONPATH=../core/src:src:../core/tests python3 -m unittest tests/test_regulatory_citation_card_gates.py tests/test_regulatory_gates.py -q && ruff check . && ruff format --check . && mypy`) alongside `unittest discover`, keeping `src/agents` untouched unless verbatim invocation requires a non-behavioral test-import-path fallback.
* `PC-003` [Low] (Applied directly): Specified `__all__` and package re-export parity for `compare_chat_against_deterministic_rule_cards` alongside `compare_chat_against_rule_cards`.
* `PC-004` [Low] (Applied directly): Added post-fetch branch ref verification in `P01-T01` confirming `feat/ai-216-citation-eval-2142` vs `feat/demo-216-citation-eval-2142` before rebasing.

## Follow-Up Items

* Human governance gates for `#216` (`OwnerGateAgreement` dual-capacity sign-off by Legal/DPO and Compliance/Building Safety owners, non-synthetic staff paired trial across `repairs`, `housing`, and `grants`, and `BRD OD-51` unit-cost ceiling ratification) remain outside executable offline-harness scope and keep `#216` tracked via `Refs #216`.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/216-citation-eval-2142-c1-changes.md
* Ready phase or task: Review (`P01`–`P03` complete)
* Remaining provisional question or blocker: None
