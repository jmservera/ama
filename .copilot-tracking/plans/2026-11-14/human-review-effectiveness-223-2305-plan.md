<!-- markdownlint-disable-file -->
# RPI Plan: Meaningful Human-Review Effectiveness Gate and Automation-Bias Harness (#223)

## Task Metadata

* Task ID: 223-human-review-effectiveness-2305
* Task slug: human-review-effectiveness-223-2305
* Planning status: ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/human-review-effectiveness-223-2305-plan-critique.md

## Executive Summary

This plan delivers the locally verifiable `src/core` engineering controls and automation-bias evaluation harness for GitHub Issue #223 (`AC-070`, `FR-026`, `FR-027`, `NFR-009`, `OQ-017`). Currently, `Store.review_ai` checks only input presence and `statement_sources` checks only whether `[[...]]` labels exist in `source_labels`, which allows citation-valid proposals that reverse open safety hazards, repeat stale survey state, invent unsupported funding promises, or omit resident accessibility adjustments to be accepted by an automation-biased reviewer. We will add `src/core/src/zava_forward/core/human_review_effectiveness.py` integrating directly with `zava_forward.core.gates.GateResult`, paired 1-to-1 with `Store.ai_run(..., mode="workflow")` scenarios across both `summary` and `message` tasks, plus targeted unit tests in `src/core/tests/test_human_review_effectiveness_223.py` and concise documentation in `src/core/README.md`.

### User Decisions and Requirements Highlights

* Implement all locally verifiable Issue #223 acceptance criteria inside `src/core` (`human_review_effectiveness.py` + `test_human_review_effectiveness_223.py`), keeping `pyproject.toml` and workflow manifests untouched.
* Detect and block seeded critical defects (`wrong`, `stale`, `unsupported`, `incomplete`) from satisfying a controlled `GateResult` gate even when every `[[...]]` citation resolves (`verified == True`) or a reviewer clicks default `accept`.
* Retain `reviewer`, `source` (`case_ids`, resolving source citation, `source_hashes` snapshot, `compared` workflow baseline), and `reason` through `Store.review_ai` and `Store.verify_audit()`.
* Report overall and per-class detection, corrections, rejections, false rejects, and total review effort (`total_ai_review_seconds`, `total_workflow_seconds`, `net_effort_delta_seconds`) against the exact same workflow-only scenarios, including an automation-bias harness and blind human-session worksheet scorer.
* Validate strictly with targeted `mypy`, `ruff check .`, `ruff format --check .`, and `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*223*.py' -v`, then commit locally with `Refs #223` without pushing.

### What You May Not Know

* Public JSON files added under `src/*/evals/` must be registered in `provenance-register.json` (`privacy.public_issues`) and are excluded from wheel `package-data` in `src/core/pyproject.toml`; embedding the canonical synthetic scenario pack in typed Python structures (while supporting JSON export/import for worksheets) avoids dataset-register drift and works in both editable checkouts and wheels.
* `src/core/pyproject.toml` enforces `mypy --strict` across `src` and `tests` while exempting legacy `store.py` and `ai_tasks.py`; encapsulating `Store` and `ai_tasks` behind narrow typed helper wrappers satisfies strict typing with zero manifest edits.

### Unresolved Decisions or Blockers

* Governance boundary (`OQ-017`, non-blocking for engineering slice): Sponsor, Programme, Safety, DPO/Legal, and Assurance sign-off on competent-review authority roles, minimum oversight thresholds, and real human reviewer participant sessions remain human post-implementation gates (`live=True` fails closed until named-human approval is supplied; commit uses `Refs #223`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Deliver Issue #223 locally verifiable engineering acceptance criteria in `src/core` on branch `feat/ai-223-human-review-effectiveness-2305` targeting `feat/demo-164-chat-grounding-provenance-0900` (caller prompt; Issue #223).
* Ensure seeded critical defects — plausible-but-wrong (`wrong`), `stale`, `unsupported`, and `incomplete` proposals — are detected and prevented from satisfying a controlled gate (`AC-070`).
* Retain reviewer identity, authoritative source evidence, and reviewer reason across review records and audit history (`FR-026`, `FR-027`, `AC-070`).
* Report detection, corrections, and total review effort against the exact same workflow-only scenarios (`FR-028`, `NFR-009`, `AC-070`).
* Prove that default acceptance and citation validity alone (`verified == True`) cannot satisfy the controlled gate, and include an automation-bias test harness (`AC-070`, `docs/case_study_48_addendum.md:1005-1013`).
* Write all four dated (`2026-11-14`) `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`), validate only with targeted `mypy`, `ruff`, and `unittest -p 'test_*223*.py'`, and commit cleanly without pushing (caller prompt).

## Goals

* Enforce a deterministic, fail-closed `human_review_gate` in `zava_forward.core` returning `gates.GateResult` (`PASS`, `FAIL`, `UNKNOWN`) compatible with `gates.transition_allowed`.
* Exercise real `Store.ai_run(..., mode="workflow")`, `Store.review_ai(...)`, and `Store.verify_audit()` flows across `summary` and `message` tasks so comparative detection, correction, and effort metrics share identical case state and workflow baselines.
* Expose automation-bias, default-acceptance, citation-only, and unauthorised-reviewer failure modes via a deterministic harness while providing blind worksheet generation and duplicate-safe scoring for future `OQ-017` human participant trials.

## Scope and Non-Goals

### In Scope

* New strictly typed module `src/core/src/zava_forward/core/human_review_effectiveness.py`.
* New targeted unit test module `src/core/tests/test_human_review_effectiveness_223.py` (selected by `-p 'test_*223*.py'`).
* Concise documentation update in `src/core/README.md` describing the core human-review effectiveness gate, automation-bias harness, and `OQ-017` boundary.
* Full `2026-11-14` RPI tracking suite under `.copilot-tracking/`.

### Non-Goals

* Modifying `src/core/pyproject.toml`, `.github/workflows/`, `provenance-register.json`, or `src/agents/`.
* Fabricating `OQ-017` human authority sign-off or claiming scripted reviewer profiles constitute live human-oversight acceptance (`Closes #223` is prohibited; use `Refs #223`).
* Running unfiltered `unittest discover -s tests` without `-p 'test_*223*.py'`.

## Functional Requirements

* FR-223-01 Controlled human-review gate (`human_review_gate`):
  * Evaluates a `Store` AI recommendation record against case state, reviewer staff authority (`AuthorityPolicy`), live-mode `OQ-017` sign-off status, `HOLD`/`QUARANTINED` lifecycle status, post-draft `ai_tasks.source_hashes(store, reviewer, case_ids)` freshness, named-human identity (`rai_release.named_human` plus placeholder/automation token refusal for `tbd`, `pending`, `unassigned`, `workflow`, `model`), non-memory substantive reason (`>= min_reason_chars`, `<= 300` chars, refusing both `controls.is_memory_reference` tokens and conversational chat-memory phrases), verified case `source_labels` citation in `reviewer_reason` across all dispositions (`accept`, `edit`, and `reject`), and semantic defect resolution across `wrong`, `stale`, `unsupported`, and `incomplete` discrepancies.
  * Observable acceptance criteria: Returns `gates.GateResult(gate, outcome, reason, owner, correction, rule)` bound to an effective `gates.GateRule` (with explicit `on` / past ISO `effective_date`), returning `UNKNOWN` when unreviewed (`status == "Not reviewed"`) or missing authority policy, `FAIL` on `HOLD`/`QUARANTINED`, default/unreasoned acceptance (`reason=""` or citation-badge-only reason), citation-only reliance (`verified=True` with unresolved defect), cosmetic/incomplete edits in `override_text`, unresolved citations in `override_text`, missing/unrelated/memory-based source reasons, non-human/placeholder/unauthorised reviewers, stale `source_hashes`, or unapproved provisional authority when `live=True`; returns `PASS` only when an authorised named human provides a source-cited reason and accurately edits/rejects a defective proposal or verifies a valid control.
* FR-223-02 Retained oversight provenance:
  * Preserves `resolved_by` / `review_evidence["reviewer"]`, `case_ids`, verified `source_labels` key in `reviewer_reason`, `review_evidence["source_hashes"]`, `review_evidence["compared"]` (`{"ai": ..., "workflow": ...}`), `override_text` (when edited), and `reviewer_reason` across all accepted, edited, and rejected competent reviews in `Store`, backed by tamper-evident `Store.verify_audit()`.
  * Observable acceptance criteria: Every competent reviewed scenario record exposes complete `reviewer`, `source`, and `reason` provenance fields and `Store.verify_audit()` returns `True`.
* FR-223-03 Workflow-only comparator and effort reporting:
  * Pairs every seeded critical-defect and valid-control scenario (`summary` and `message`) with `Store.ai_run(..., mode="workflow")` on identical constructed case data and reports overall and per-class (`wrong`, `stale`, `unsupported`, `incomplete`) detection, corrections, rejections, false rejects, gate leakage, `total_ai_review_seconds`, `total_workflow_seconds`, and `net_effort_delta_seconds`.
  * Observable acceptance criteria: Comparative report matches scenario-by-scenario against `mode="workflow"` baselines and records `gate_leakage == 0` across all panels.
* FR-223-04 Automation-bias harness and blind human-session scorer:
  * Evaluates `competent`, `default_accept`, `automation_bias` (trusting confident + citation-valid proposals while checking hedged ones), `citation_only`, and `unauthorised_competent` panels, plus `blank_worksheet()`, `score_human_session()`, and duplicate-rejecting `pool_human_sessions()`.
  * Observable acceptance criteria: `automation_bias` misses confident citation-valid defects (`detection_rate < 1.0`, `automation_bias_exposed == True`) and fails the controlled gate (`gate_leakage == 0`), while `competent` detects 100% of seeded defects (`false_rejects == 0`) and `blank_worksheet()` leaks zero defect or confidence labels.

## Non-Functional Requirements

* NFR-223-01 Strict static typing and lint cleanliness:
  * Objective threshold or evaluation condition: Zero errors under `python3 -m mypy` (`strict = true`), `python3 -m ruff check .`, and `python3 -m ruff format --check .` in `src/core` without adding `pyproject.toml` overrides.
  * Observable acceptance criteria: All three static checks exit `0`.
* NFR-223-02 Deterministic offline execution and synthetic-privacy safety:
  * Objective threshold or evaluation condition: Runs 100% offline using constructed synthetic data in temporary directories (`tempfile.TemporaryDirectory`), zero network/model spend, and zero unregistered `src/core/evals/` payloads.
  * Observable acceptance criteria: Targeted test command completes deterministically under 5 seconds with clean git worktree and `privacy.public_issues` unaffected.

## Acceptance Criteria

* AC-1: Seeded `wrong`, `stale`, `unsupported`, and `incomplete` proposals (all carrying valid `[[...]]` case citations so `verified == True`) are detected by the competent panel and prevented from satisfying `human_review_gate` (`gates.transition_allowed` is `False`) under `default_accept`, `citation_only`, `automation_bias`, cosmetic edits, and unauthorised reviewers.
* AC-2: Reviewer (`resolved_by` / `review_evidence.reviewer`), authoritative source (`case_ids`, resolving `source_labels` key, `source_hashes`, `compared` workflow output), and `reviewer_reason` are retained in `Store` and verified with `Store.verify_audit() == True`.
* AC-3: Detection (`detection_rate` and `by_defect_class`), `corrections`, `rejections`, `false_rejects`, and total review effort (`total_ai_review_seconds`, `total_workflow_seconds`, `net_effort_delta_seconds`) are reported against the exact same workflow-only scenarios across `summary` and `message` tasks.
* AC-4: Default acceptance (`reason=""` or citation-badge-only reason) and citation validity alone fail closed across both defective proposals and valid controls (`gate_passed_count == 0` for `default_accept` and `citation_only`); `HOLD`/`QUARANTINED` states, post-draft case mutations (`stale_case_sources`), canonical and conversational chat-memory reasons, non-human/placeholder identities (`Copilot`, `system`, `TBD`, `pending`, `workflow`), and `live=True` with unapproved `OQ-017` provisional authority all fail closed.
* AC-5: Blind `blank_worksheet()`, `score_human_session()`, and `pool_human_sessions()` support external human trials without leaking labels or allowing scripted harness results to claim human-oversight closure.

## Test Ownership and Validation Lock

* Canonical implementation target: `src/core/src/zava_forward/core/human_review_effectiveness.py` (generated targets: `none`).
* Canonical test target: `src/core/tests/test_human_review_effectiveness_223.py` (exact test removals: `none`; maximum test file additions: `1`).
* Semantic vs regression coverage:
  * Semantic coverage: 4 seeded defect classes + 2 valid controls across `summary` and `message`, live case semantic invariant checks (open safety hazard, resident accessibility adjustment, unapproved funding, current stage, citation resolution), automation-bias confidence contrast, blind worksheet/session pooling, and `OQ-017` live fail-closed gate.
  * Regression coverage: `Store.ai_run(..., mode="workflow")`, `Store.review_ai(...)`, `Store.verify_audit()`, `gates.transition_allowed(...)`, `rai_release.named_human(...)`, and `controls.is_memory_reference(...)` contracts preserved without modifying legacy core modules.
* Exact validation command:
  * `cd /home/azureuser/source/ama-demo-wt/feat-223-human-review-effectiveness-2305/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*223*.py' -v`

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/human-review-effectiveness-223-2305-plan.md                                                           |
| Phase details                    | .copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md                                                |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-14/human-review-effectiveness-223-2305-plan-critique.md with Revise disposition; PC-001 through PC-004 resolved in place |
| Relevant research                | .copilot-tracking/research/2026-11-14/human-review-effectiveness-223-2305-research.md                                                    |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/human-review-effectiveness-223-2305-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for implementation                                                                                                    |
| Continuation context             | Confirmed automatic RPI Agent session continues automatically to Implement                                                               |

## Sources

* `.copilot-tracking/research/2026-11-14/human-review-effectiveness-223-2305-research.md`: Cycle 1 research synthesis (`C1`–`C8`) establishing `AC-070`, `Store`/`gates`/`rai_release`/`controls` seams, `mypy --strict` wrapper pattern, and `privacy.public_issues` constraints.
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: Authoritative `FR-026`, `FR-027`, `FR-028`, `NFR-009`, `AC-070`, and `OQ-017` specifications.
* `docs/case_study_48_addendum.md`: Responsible AI Release Position (`2026-10-14`) on meaningful oversight, automation bias, and default acceptance.
* `src/core/src/zava_forward/core/ai_tasks.py`, `store.py`, `gates.py`, `rai_release.py`, `controls.py`: Core runtime surfaces integrated by `human_review_effectiveness.py`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Gate, Authority Policy, and Seeded Scenarios

* Intent: Build the strictly typed authority policy, constructed multi-task scenario pack, live-case semantic discrepancy inspector, and `human_review_gate` returning `gates.GateResult`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Define typed Store/ai_tasks boundary, `AuthorityPolicy`, and constructed `summary`/`message` scenario pack

* Requirement and evidence: FR-223-01, FR-223-03, NFR-223-01, NFR-223-02 (`C1`, `C3`, `C4`, `C7`, `C8`)
* Expected result: `AuthorityPolicy` (`PROVISIONAL_AUTHORITY` with `OQ-017` gap notice), constructed synthetic dataset (`ZF-223-A`, `ZF-223-B`), and 8 citation-valid scenarios covering `wrong`, `stale`, `unsupported`, `incomplete`, and hedged/confident valid controls (`none`) across `summary` and `message`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Implement fail-closed `human_review_gate` integrated with `gates.GateResult`

* Requirement and evidence: FR-223-01, FR-223-02, AC-1, AC-2, AC-4 (`C1`, `C2`, `C4`, `C5`)
* Expected result: `human_review_gate` enforces reviewed status, `live=True` `OQ-017` block, `named_human` identity, role/task authorization, `source_hashes` freshness, non-memory substantive reason citing a resolving case `source_labels` key, and semantic verification of both live case invariants and seeded scenario claims on `accept`, `edit`, and `reject`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Workflow-Only Comparator, Automation-Bias Harness, and Human Session Scoring

* Intent: Execute scenarios end-to-end against `Store.ai_run(..., mode="workflow")` and `Store.review_ai(...)`, compare reviewer panels (`competent`, `default_accept`, `automation_bias`, `citation_only`, `unauthorised_competent`), and support blind human worksheets and pooled scoring.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Implement workflow-paired scenario runner, scripted panels, and effort/detection reporting

* Requirement and evidence: FR-223-02, FR-223-03, FR-223-04, AC-2, AC-3 (`C1`, `C3`, `C4`, `C6`)
* Expected result: `evaluate_panel` and `run_automation_bias_harness` run both AI review and `mode="workflow"` baselines per scenario, verify `Store.verify_audit()`, enforce zero gate leakage across defective proposals, expose automation bias on confident citation-valid defects, and report detection (`overall` and `by_defect_class`), corrections, rejections, false rejects, and total/delta review effort.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Implement `blank_worksheet`, `score_human_session`, and duplicate-safe `pool_human_sessions`

* Requirement and evidence: FR-223-04, AC-5 (`C1`, `C2`, `C6`)
* Expected result: Blind reviewer worksheet strips all defect/confidence spoilers; `score_human_session` and `pool_human_sessions` validate human participant identity, positive review effort, scenario completeness, and duplicate-reviewer rejection while preserving `oq017_live_approved=False` until named human authority exists.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Targeted Tests, Documentation, and Strict Validation

* Intent: Prove all Issue #223 acceptance criteria and adversarial bypasses in `test_human_review_effectiveness_223.py`, document the core module in `src/core/README.md`, and pass targeted `mypy`, `ruff`, and `unittest` checks.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Author `src/core/tests/test_human_review_effectiveness_223.py`, update `src/core/README.md`, and run targeted validation

* Requirement and evidence: AC-1 through AC-5, NFR-223-01, NFR-223-02 (`C1`–`C8`)
* Expected result: Focused test suite covers all 4 defect classes, valid controls, workflow effort deltas, audit retention, every gate bypass/staleness/`live=True` failure path, and blind worksheet/session pooling; `src/core/README.md` documents the gate and `OQ-017` boundary; `mypy`, `ruff check .`, `ruff format --check .`, and `unittest -p 'test_*223*.py'` all pass cleanly.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md

## Dependencies

* `zava_forward.core.store.Store` and `zava_forward.core.ai_tasks`: provide `ai_run(..., mode="workflow")`, `review_ai`, `source_labels`, `source_hashes`, `statement_sources`, and `verify_audit()`.
* `zava_forward.core.gates`, `rai_release`, and `controls`: provide `GateResult` (`PASS`, `FAIL`, `UNKNOWN`), `transition_allowed`, `AUTHORITY_GAP`, `named_human`, and `is_memory_reference`.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| PC-001 (Critical: `GateResult` / `GateRule` signature and `effective_date`) | Resolved | Updated `FR-223-01` and `P01-T02` to construct `gates.GateRule` (effective `2026-01-01` with explicit `on` support) and `gates.GateResult(gate, outcome, reason, owner, correction, rule)` matching `src/core/src/zava_forward/core/gates.py`. |
| PC-002 (High: Offline `Store.ai_run`/`review_ai` release binding, same-user ownership, field names, `source_labels`, `HOLD`) | Resolved | Updated `FR-223-01`, `FR-223-02`, `P01-T01`, `P01-T02`, `P02-T01`, and `P02-T02` to bind synthetic `release_context` + offline `store.ai.run` under the reviewing user, pass `(user, rec_id, action, reason, text)` (`<= 300` chars), inspect `override_text` and `compared["ai" \| "workflow"]`, format exact `source_labels` citations with matching `can_see_reason` role visibility, fail `HOLD`/`QUARANTINED`, and call 3-arg `ai_tasks.source_hashes(store, user, case_ids)`. |
| PC-003 (High: Mandatory case-source-cited `reviewer_reason` on `"accept"`) | Resolved | Updated `FR-223-01`, `FR-223-02`, `AC-4`, `P01-T02`, and `P02-T01` so every passing review disposition (`accept`, `edit`, and `reject`) requires a substantive non-memory case-source-cited `reviewer_reason`, ensuring `gate_passed_count == 0` for `default_accept` and `citation_only` and 100% provenance retention on `competent`. |
| PC-004 (Medium: Placeholder human tokens and conversational memory phrases) | Resolved | Updated `FR-223-01`, `AC-4`, `P01-T02`, and `P03-T01` to supplement `rai_release.named_human` with placeholder/automation token refusal (`tbd`, `todo`, `pending`, `unassigned`, `placeholder`, `workflow`, `model`, `n/a`) and supplement `controls.is_memory_reference` with conversational chat/assistant-memory phrase refusal. |

## Follow-Up Items

* Appoint competent-review authority holders and owner-defined oversight thresholds under `OQ-017` (Sponsor, Programme, Safety, DPO/Legal, Assurance), then execute blind human reviewer sessions using `blank_worksheet()` and `pool_human_sessions()` before enabling `live=True` release gating.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/human-review-effectiveness-223-2305-changes.md
* Ready phase or task: P01 (P01-T01 -> P01-T02 -> P02-T01 -> P02-T02 -> P03-T01)
* Remaining provisional question or blocker: None for engineering implementation (`OQ-017` remains an explicit fail-closed governance boundary)
