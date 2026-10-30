---
title: Workbook fuzzy-union correction plan critique
description: Single independent final-candidate assessment for issue-146-pr-512-fix-cycle-1
ms.date: 2026-10-29
---

## Metadata

* Task ID: issue-146-pr-512-fix-cycle-1
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/monitoring-146-pr512-fix-cycle-1-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/monitoring-146-pr512-fix-cycle-1-phase-details.md
* Critique execution status: Complete
* Assessment count: One final-candidate critique; no second critique requested or performed.

## Inputs and Criterion Boundary

* Caller requirements: Full dated RPI correction for Refs #146 / PR #512 cycle 1; completed initial pull/rebase; both bare-table fuzzy unions with outer projection; valid JSON; regression rejection of both old forms; scoped existing tests and changed-Python Ruff lint/format; local commit with required Copilot trailer. No Azure operations, latest.json edits, push, closing keyword or publication.
* Locked scope: infra/monitoring-workbook.json, infra/tests/test_monitoring_workbook.py and infra/README.md; maximum one new Python module and one test method with both subtests; no removals or generated delivery targets.
* Research: .copilot-tracking/research/2026-10-29/monitoring-146-pr512-fix-cycle-1-research.md, including Q1-Q2 and C1-C4.
* Supplied evidence inspected: infra/monitoring-workbook.json, infra/tests/test_bicep_policy.py, the five selected existing test modules' prerequisite/scratch declarations, infra/README.md, and .copilot-tracking/changes/2026-10-29/monitoring-146-rebase-changes.md.
* Repository context: Required case-study, addendum, knowledge-base index and owner-memory context; active branch feat/monitoring-146. Existing untracked candidate/state inputs were not modified.
* Assessment covers requirements, evidence, phases, tasks, dependencies, acceptance criteria, decisions, risks and execution constraints. It does not execute implementation, tests, Kusto, Azure, publication checks or GitHub operations.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1, C1-C2, P01-T01 | Covered | Workbook contains both reported projected operands; one new table-driven unittest is appropriate without unrelated refactoring. |
| Both union corrections and locked targets | Covered | Exact initial-statement oracle covers typed fallback, bare source, field order and outer projection for both panels. |
| Red/green acceptance | Covered | Both old subtests must fail before correction, then both pass; actual outputs must be preserved. |
| Q2, C3, semantic preservation | Covered | Unchanged suffix after the first semicolon protects sampling, filters, invalid-row accounting, Insufficient status and null metrics. |
| C4, P01-T02, scoped validation | Partial | Required tests, JSON, isolated Ruff and no-skips rule are named, but execution paths conflict with current filesystem constraints: PC-001. |
| P02-T01, independent Review | Covered | One fresh Review has a fixed starting head and requires actual validation evidence; original adverse outcomes remain preserved. |
| P02-T02, local commit | Covered | Finite staging, privacy-safe identity, Refs-only message, required trailer, metadata and clean-status checks; no remote writes. |
| Dependencies and residual operational risks | Covered | Missing prerequisites block success; live verification and historical findings remain explicitly unresolved, not issue acceptance. |
| Decisions and publication boundary | Covered | Owner already selected the correction and unpublished local commit; later publication still requires its separate gates. |

## Verdict

* Verdict: Revise
* Rationale: The source correction and regression plan are credible. One concrete validation-path correction is required before execution can follow the current filesystem restrictions. No significant or divergent user decision is necessary.
* Severity counts: Critical 0; High 0; Medium 1; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Make validation filesystem paths compliant

* Related IDs: P01-T02; scoped-validation acceptance criterion; validation dependencies.
* Evidence: .copilot-tracking/plans/2026-10-29/monitoring-146-pr512-fix-cycle-1-plan.md explicitly permits using /tmp/mv tools. .copilot-tracking/details/2026-10-29/monitoring-146-pr512-fix-cycle-1-phase-details.md directs validation logs to external session storage. Current execution instructions prohibit /tmp and /var/tmp file operations and require newly created files to be relative to the working directory. infra/tests/test_bicep_policy.py:324 uses TemporaryDirectory without an explicit directory, so the proposed command does not itself ensure permitted scratch placement.
* Concern: The validation recipe can use forbidden tools or filesystem destinations even though its test selectors are correct. A missing explicit scratch setting also leaves existing test subprocess output placement dependent on inherited environment.
* Impact: Required validation could violate execution constraints or be blocked; claimed successful local completion would then lack an executable compliant recipe.
* Smallest useful change: Remove the /tmp tooling instruction. Specify permitted pre-existing tool locations, or report a missing tool as a blocker. Specify working-tree-relative scratch/log locations and set the test process's TMPDIR to the resolved permitted project scratch path before Python starts. Account for tool caches/output paths as needed. Keep scratch/log products outside the finite staged delivery targets and handle them under the retention policy; do not edit existing tests or add generated delivery targets.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T02 plan/details name compliant tool, scratch and log paths plus the explicit environment setup for the existing TemporaryDirectory test. Subsequent implementation evidence records actual scoped test results with zero skips, JSON parsing, isolated changed-file Ruff lint/format and diff hygiene using that recipe, without forbidden-path file operations.
* Decision route: Direct planner correction. The current restrictions already resolve the choice; no significant or divergent user decision.

## Strengths and Residual Risk

* The exact-prefix regression rejects the actual defective form rather than merely testing already-present fuzzy/datatable keywords.
* The bounded source changes and unchanged-suffix comparison preserve the existing monitoring calculations without unrelated cleanup.
* The candidate explicitly accepts source-only evidence: local checks cannot establish live absent-table Kusto binding, portal operation, named approvals or whole-issue acceptance.
* No removal, additional Python test method, generated delivery target, Azure operation or publication is needed to resolve PC-001.

## Questions or Blocking Evidence Gaps

* No user question or decision-critical research gap. Tool availability must be established during implementation; a missing prerequisite remains a blocker, not permission to skip or substitute cloud execution.

## Limitations

* This is a plan credibility assessment, not an implementation Review or test receipt. No runtime, compiler, lint or service validation was executed.
* Prior validation evidence supplies context only and does not prove the new candidate passes.
* Only this critique artifact was written. Plan, details, research, source and session state remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001, Medium.
* Action owner: Planning parent.
* Smallest next action: Correct the validation filesystem recipe directly, record the disposition and continue the authorized implementation and one independent Review.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/monitoring-146-pr512-fix-cycle-1-plan.md](.copilot-tracking/plans/2026-10-29/monitoring-146-pr512-fix-cycle-1-plan.md) | Assessed candidate plan |
| [.copilot-tracking/details/2026-10-29/monitoring-146-pr512-fix-cycle-1-phase-details.md](.copilot-tracking/details/2026-10-29/monitoring-146-pr512-fix-cycle-1-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-29/monitoring-146-pr512-fix-cycle-1-research.md](.copilot-tracking/research/2026-10-29/monitoring-146-pr512-fix-cycle-1-research.md) | Supplied research boundary |
| [.copilot-tracking/reviews/plans/2026-10-29/monitoring-146-pr512-fix-cycle-1-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/monitoring-146-pr512-fix-cycle-1-plan-critique.md) | Complete critique; Revise verdict |

## Next Steps

Planning parent resolves PC-001 directly and continues after recording its disposition. No user action or second critique is required. This independent critique stops here.
