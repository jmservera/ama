<!-- markdownlint-disable-file -->
# RPI Changes: Meaningful Human-Review Effectiveness Gate and Automation-Bias Harness (#223)

## Metadata

* Task ID: 223-human-review-effectiveness-2305
* Related plan: .copilot-tracking/plans/2026-11-14/human-review-effectiveness-223-2305-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/human-review-effectiveness-223-2305-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full_plan (P01, P02, P03)
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02, P03, P03-T01
* All remaining active-plan markers: none
* Status basis: All planned phases and tasks (`P01` through `P03`) are implemented in `src/core`, documented in `src/core/README.md`, and verified against targeted `mypy`, `ruff check .`, `ruff format --check .`, `unittest -p 'test_*223*.py'`, and `synthetic.privacy.public_issues()`.

## Execution Summary

Delivered `src/core/src/zava_forward/core/human_review_effectiveness.py`, `src/core/tests/test_human_review_effectiveness_223.py`, and concise documentation in `src/core/README.md` for GitHub Issue #223 (`AC-070`, `FR-026`, `FR-027`, `FR-028`, `NFR-009`, `OQ-017`). Seeded critical defects (`wrong`, `stale`, `unsupported`, and `incomplete`) and valid controls across `summary` and `message` all carry resolving inline `[[...]]` citations (`verified == True`), run 1-to-1 against `Store.ai_run(..., mode="workflow")` and `Store.review_ai(...)`, retain reviewer/source/reason provenance verified by `Store.verify_audit()`, prevent default acceptance, citation-only verification, automation-biased acceptance, memory citations, stale cases, cosmetic edits, and unauthorised/provisional live transitions from satisfying `human_review_gate` (`gates.GateResult`), and provide blind reviewer worksheets and duplicate-rejecting pooled human session scoring.

## Completed Work

### P01: Core Gate, Authority Policy, and Seeded Scenarios (`P01-T01`, `P01-T02`)

* Created `src/core/src/zava_forward/core/human_review_effectiveness.py` with `AuthorityPolicy`, `PROVISIONAL_AUTHORITY` (carrying `rai_release.AUTHORITY_GAP` and failing closed when `live=True`), `ReviewScenario`, `synthetic_dataset()` (`ZF-223-A`, `ZF-223-B`), and `DEFAULT_SCENARIOS` (`S-223-01` through `S-223-08`).
* Implemented `is_valid_human_identity` (supplementing `rai_release.named_human` with placeholder/automation token refusal), `cites_memory` (supplementing `controls.is_memory_reference` with conversational chat/assistant-memory phrase detection), `inspect_discrepancies`, and `human_review_gate` returning `gates.GateResult` + `gates.GateRule` compatible with `gates.transition_allowed`.

### P02: Workflow-Only Comparator, Automation-Bias Harness, and Human Session Scoring (`P02-T01`, `P02-T02`)

* Implemented `evaluate_panel` and `run_automation_bias_harness` executing both `Store.ai_run(..., mode="workflow")` and `Store.ai_run` + `Store.review_ai` per scenario across `competent`, `default_accept`, `automation_bias`, `citation_only`, and `unauthorised_competent` panels, verifying `Store.verify_audit()`, zero gate leakage, per-class and overall defect detection, corrections, rejections, false rejects, and review-effort deltas against the workflow-only baseline.
* Implemented `blank_worksheet` (stripping all defect/confidence/solution spoilers), `score_human_session`, and duplicate-safe `pool_human_sessions` preserving `oq017_live_approved=False` until named human authority exists.

### P03: Targeted Tests, Documentation, and Strict Validation (`P03-T01`)

* Created `src/core/tests/test_human_review_effectiveness_223.py` covering all 5 Issue #223 engineering criteria, citation-valid seeded defects, workflow effort comparisons, adversarial gate bypasses (unreviewed, missing policy, future effective date, cosmetic edit, unresolved edit citation, unrelated source reason, canonical and conversational memory citations, placeholder/non-human actors, task-scope mismatch, pre-review `Hold`, post-review source staleness), `live=True` `OQ-017` fail-closed enforcement, and blind worksheet/session pooling.
* Updated `src/core/README.md` with a concise section documenting `zava_forward.core.human_review_effectiveness`, its targeted test command, and the `OQ-017` governance boundary.

## Implementation-Time Plan and Detail Updates

* Local judgment refinements within approved plan intent (no plan scope or architecture change):
  * Bound `store.ai.fast = "synthetic-eval-223"` and `store.ai.strong = "synthetic-eval-223"` in the offline synthetic store helper so `ai_registry.legacy_deployment(task, store.ai)` matches the offline AI proposal deployment checked by `Store.release_current`.
  * Aligned synthetic scenario `Resident decision` citations to `[[Resident decision: Not recorded]]` matching `resident_decisions.resident_status` output in `ai_tasks.source_labels`, ensuring `verified == True` across all 8 seeded scenarios.
  * Scoped `gate_leakage` counting to undetected/uncorrected seeded defects (`allowed and not detected`) so competent edits and rejections that resolve seeded defects report `gate_leakage == 0`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m mypy` | `src/core` (329 source files) | Passed | `Success: no issues found in 329 source files` |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` (276 files) | Passed | `276 files already formatted` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*223*.py' -v` | `src/core/tests/test_human_review_effectiveness_223.py` | Passed | `Ran 6 tests in 0.730s — OK` |
| `synthetic.privacy.public_issues(repo_root)` | Repository synthetic provenance guard | Passed | `[]` (no unregistered eval files or prohibited fields) |

## Pre-Review Reconciliation

* Plan markers and phase details: current (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01` all `[x]`)
* Completed-work evidence and handoff prose: current and reconciled
* Validation, blockers, remaining work, and follow-up items: current
* Review readiness: ready for `rpi-review`

## Blockers

* None for local engineering scope (`OQ-017` human authority appointments and real participant trials remain explicit fail-closed governance follow-ups).

## Remaining Work

* None in declared plan scope.

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/human-review-effectiveness-223-2305-plan.md, `## Follow-Up Items`
* Appoint competent-review authority holders and owner-defined oversight thresholds under `OQ-017`, then run blind human reviewer sessions using `blank_worksheet()` and `pool_human_sessions()` before enabling `live=True` release gating.
* Optional downstream API/UI surface wiring once `OQ-017` governance roles and live thresholds are ratified.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full_plan; completed: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02, P03, P03-T01; remaining: none
* Validation coverage: `mypy` (329 files), `ruff check .`, `ruff format --check .`, `unittest discover -s tests -p 'test_*223*.py' -v` (6/6 passed), and `synthetic.privacy.public_issues` (`[]`)
* Blockers: None
* Current plan and detail updates: All `P01`–`P03` markers checked in `.copilot-tracking/plans/2026-11-14/human-review-effectiveness-223-2305-plan.md`; local judgment implementation notes recorded above
* Planning and critique state: Ready (`PC-001` through `PC-004` resolved)
* Follow-up items: `OQ-017` human authority appointment + blind participant sessions; downstream API/UI wiring post-ratification
* Review readiness or no-handoff reason: Ready for single-pass `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
