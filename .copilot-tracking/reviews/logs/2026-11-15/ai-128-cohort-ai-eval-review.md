<!-- markdownlint-disable-file -->
# Review: Local RAI Cohort Evaluation Slice of Issue #128

## Scope and Evidence

* Task ID: 2026-11-15-ai-128-cohort-ai-eval
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Pure `src/core` RAI Cohort Evaluation slice of Issue #128 (`Refs #128`) across `paired_equity.py`, `cohort_eval.py`, `test_paired_equity.py`, `test_cohort_eval.py`, and `src/core/README.md`, with `journey_register.py` held untouched for sibling-branch (`#1735`) compatibility and Focused local validation.
* Plan: .copilot-tracking/plans/2026-11-15/ai-128-cohort-ai-eval-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/ai-128-cohort-ai-eval-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/ai-128-cohort-ai-eval-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/ai-128-cohort-ai-eval-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/ai-128-cohort-ai-eval-research.md; git diff across `src/core`; Focused validation runs (`unittest`, `ruff`, `mypy`).

## Opening Review State

* Interpreted review goal: Verify once and read-only that the completed full-plan implementation (`P01`..`P03`) satisfies all 8 RAI Cohort Acceptance Criteria of Issue #128 (`Refs #128`), preserves `fairness_evidence=False` and `activation_allowed=False` fail-closed invariants, honors all 6 critique dispositions (`PC-001`..`PC-006`), leaves `journey_register.py` untouched, and passes Focused validation without undocumented drift.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; plan, phase details, one-pass plan critique, reconciled changes record, research synthesis, and Focused validation outputs are present and synchronized.
* Acceptance basis: `## Acceptance Criteria` (`AC-1`..`AC-9`) and `## Critique Disposition` (`PC-001`..`PC-006`) in .copilot-tracking/plans/2026-11-15/ai-128-cohort-ai-eval-plan.md, plus repository Markdown and Focused validation rules.
* First comparison boundary: Reconcile `plan.md`, `phase-details.md`, `plan-critique.md`, and `changes.md` against the exact `src/core` source, test, and documentation diffs.
* Active read-only boundaries: Write access restricted exclusively to .copilot-tracking/reviews/logs/2026-11-15/ai-128-cohort-ai-eval-review.md (plus parent RPI session state tracking); no mutation of `src/` or earlier RPI artifacts.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass post-implementation review on 2026-11-15 across the reconciled full-plan boundary (`P01`, `P02`, `P03`), comparing `.copilot-tracking/plans/2026-11-15/ai-128-cohort-ai-eval-plan.md`, `.copilot-tracking/details/2026-11-15/ai-128-cohort-ai-eval-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-15/ai-128-cohort-ai-eval-plan-critique.md`, and `.copilot-tracking/changes/2026-11-15/ai-128-cohort-ai-eval-changes.md` against the exact `src/core` source, test, and documentation diffs and Focused validation outputs.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Failing-first RAI cohort evaluation test suites (`P01`) | Reconciled | 7 focused tests in `test_paired_equity.py` and 7 focused tests in `test_cohort_eval.py` verified failing (`failures=10, errors=4`) before `P02` and passing afterward; within locked test-addition cap (`<= 12` per file, `0` removals). |
| `P02` (`P02-T01`, `P02-T02`) | Pure `src/core` RAI cohort evaluation controls (`P02`) | Reconciled | `paired_equity.py` and `cohort_eval.py` deliver FR-1..FR-6, AC-1..AC-8, and all 6 critique dispositions (`PC-001`..`PC-006`) without touching `journey_register.py`. |
| `P03` (`P03-T01`) | Component documentation and Focused validation (`P03`) | Reconciled | `src/core/README.md` updated cleanly; Focused validation (`unittest`, `ruff check`, `ruff format --check`, bare `mypy`) passed with zero errors. |
| `## Follow-Up Items` | Deferred operational fairness evidence and post-`#1735` status alignment | Reconciled | Preserved outside active `Pxx`/`Pxx-Txx` scope and mirrored in `changes.md`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01` (`P01-T01`, `P01-T02`) | `src/core/tests/test_paired_equity.py`, `src/core/tests/test_cohort_eval.py` | Added 14 focused tests covering AC-1..AC-8 and `PC-001`..`PC-006` without removing or altering any existing regression tests. | Verified failing before `P02` (`69` tests run: `10` failures, `4` errors across the 14 new tests; all `55` existing tests passed) and passing after `P02`. | Passed (`107` tests in `src/core`, `ruff`, `mypy`). | Reconciled and conformant |
| `P02-T01` | `src/core/src/zava_forward/core/paired_equity.py` | Added `PREDECLARED_CONTRASTS`, `predeclared_cohorts()`, `input_digest()`, optional `geography`/`archetype` relevance approvals, DPO minimum-necessary protected-field gating, signed `ranking_policy` ownership/hash/rule-order verification, `ai_task` evaluation + `non_ai_comparison`, safe abstention vs service-lowering/prohibited-inference distinction, sensor fixture anti-provisioning/anti-threshold-invention guards, retained definitions/counts/sufficiency/Wilson intervals, and fail-closed `disposition`. | All `test_paired_equity.py` tests pass, including default-ranker `record_hash` parity (`rank=ranking.rank` vs `rank=None`). | Passed (`unittest`, `ruff`, `mypy`). | Reconciled and conformant |
| `P02-T02` | `src/core/src/zava_forward/core/cohort_eval.py` | Added `"abstained"` outcome, retained `cohort_definitions`, `version_definitions`, `counts` (`eligible`, `tested`, `abstained`, `failed`, `missing`), `approve_protected_characteristics()`, `approve_context_dimensions()`, approval-envelope exclusion in `manifest_digest()`, human-approver/ISO-date checks on thresholds and dispositions, `ranking_policy` + `non_ai_comparison` regression checks, `service_lowered` & `prohibited_inference` blockers/accounting, sensor fixture guards, `_is_generated_cohort` non-fairness invariants, and `export_record()` enforcement. | All `test_cohort_eval.py`, `test_rai_threshold_live_approval_guard.py`, `test_heldout_eval.py`, and `src/agents` cohort suites (`test_cohort_ranking_eval.py`, `test_cohort_ai_eval.py`, `test_ai_eval.py`) pass unmodified. | Passed (`unittest`, `ruff`, `mypy`). | Reconciled and conformant |
| `P03-T01` | `src/core/README.md` | Updated `#222 and #128 cohort evaluator` and `paired_equity.evaluate` documentation sections with exact function contracts, approval gates, and non-fairness boundaries. | Relative links verified by `test_live_doc_links.py`; zero `.copilot-tracking/` references in `src/` verified by `test_cutover_audit.py` and `grep`. | Passed (`11` doc/cutover audit tests). | Reconciled and conformant |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| None | No implementation-time plan or phase-detail amendments were needed; execution followed the critique-reconciled plan verbatim. | None | Checklist markers `P01`..`P03` checked upon completion and mirrored in `changes.md`. | Not needed (`Planning status: Ready`, `PC-001`..`PC-006` resolved prior to `P01`). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All 6 findings (`PC-001`..`PC-006`) in `.copilot-tracking/reviews/plans/2026-11-15/ai-128-cohort-ai-eval-plan-critique.md` have explicit `Resolved` entries in `plan.md` (`## Critique Disposition`) and verified implementation + test coverage in `paired_equity.py`, `cohort_eval.py`, `test_paired_equity.py`, and `test_cohort_eval.py`.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No dependent-work pause was triggered; `P01` -> `P02` -> `P03` executed strictly in dependency order.
* Justification assessment: Keeping `journey_register.py` untouched is justified by codebase evidence (`C3`, sibling `#1735` stacked-branch isolation) and preserves full contract compatibility.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| External human governance, live accessibility/usability user-research runs, and live OQ-018 DPO/RAI/policy sign-offs on Issue #128 | Requires real human approvers, approved operational datasets, and human-participant sessions outside local `src/core` code (`Refs #128`, not closing `#128`). | Named DPO, RAI Owner, Policy Owner, and UX Research Lead | Open external governance/research follow-up; kept outside active `Pxx` scope. |
| Post-merge alignment with sibling `#1735` appointment statuses (`reschedule_requested`, `cancelled`) | Sibling branch `#1735` owns `journey_register.py` expansion; avoiding cross-branch edits prevents stacked merge conflicts. | Backlog delivery coordinator after `#1735` merges | Distinct engineering follow-up item outside current task scope. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No material defects, decision gaps, or evidence gaps were identified across `P01`..`P03`.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None | None | None | Implementation is conformant across all 8 RAI Cohort Acceptance Criteria and Focused validation checks. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Post-merge contrast alignment with sibling `#1735` appointment-history values (`reschedule_requested`, `cancelled`) once `#1735` merges into `main` (owner: backlog delivery coordinator).
* Operational/population fairness evaluation and OQ-018 live cohort/threshold/policy sign-off once real approved datasets and named human governance sign-offs exist (owner: DPO / RAI Owner / Asset Policy Owner; `Refs #128`).

## Blockers and Remaining Work

* Blockers: None for the local engineering candidate (`Refs #128`). Live operational activation remains intentionally blocked fail-closed (`activation_allowed=False`, `fairness_evidence=False`) pending external human governance approvals (`OQ-018`).
* Remaining active work: None (`P01`, `P02`, and `P03` complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=src:tests python3 -m unittest test_paired_equity test_cohort_eval` (pre-`P02`) | `src/core/tests` failing-first verification | Passed (failed as expected pre-`P02`) | `Ran 69 tests`: `FAILED (failures=10, errors=4)` across all 14 new tests; all 55 existing tests passed. |
| `PYTHONPATH=src:tests python3 -m unittest test_paired_equity test_cohort_eval test_journey_register test_rai_threshold_live_approval_guard test_heldout_eval -q` | `src/core` unit and regression suites | Passed | `Ran 107 tests in 0.788s: OK`. |
| `PYTHONPATH=../core/src:src:tests python3 -m unittest test_cohort_ranking_eval test_cohort_ai_eval test_ai_eval -q` | Downstream `src/agents` cohort and AI eval callers | Passed | `Ran 45 tests in 14.153s: OK`. |
| `PYTHONPATH=src:tests python3 -m unittest test_live_doc_links test_cutover_audit -q` | `src/core/README.md` links and tracking-hygiene audit | Passed | `Ran 11 tests in 5.969s: OK`. |
| `python3 -m ruff check` & `python3 -m ruff format --isolated --line-length 100 --check` | `paired_equity.py`, `cohort_eval.py`, `test_paired_equity.py`, `test_cohort_eval.py` | Passed | `All checks passed!`; `4 files already formatted`. |
| `python3 -m mypy --cache-dir=/tmp/mypy-128` | Bare `mypy` inside `src/core` (`342` source files) | Passed | `Success: no issues found in 342 source files`. |
| Hosted GitHub Actions CI | Remote PR workflow runs | Skipped | Explicit caller instruction: leave a clean frozen local candidate and do NOT push or open a PR. |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every planned phase and task (`P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`, `P03-T01`), all 8 RAI Cohort Acceptance Criteria of Issue #128 (`Refs #128`), the `fairness_evidence=False` and `activation_allowed=False` fail-closed invariants, and all 6 plan-critique dispositions (`PC-001`..`PC-006`) are delivered, reconciled across tracking artifacts, backward-compatible with `src/agents` callers without touching `journey_register.py`, and proven by Focused local validation (`163` unit/audit tests, `ruff`, and strict `mypy`).

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | None | None |
| Decision gap or invalid assumption | None | None |
| Material evidence gap | None | None |
| Non-blocking residual work | Distinct follow-up | Reconcile sibling `#1735` appointment statuses post-merge; obtain external human OQ-018/DPO/user-research sign-offs for full Issue #128 closure |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused local tier passed (`107` core unit tests, `45` agent unit tests, `11` doc/cutover audit tests, `ruff check`, `ruff format --isolated --line-length 100 --check`, bare `mypy` across `342` source files); hosted CI not run because branch remains local-only by instruction.
* Blockers: None

