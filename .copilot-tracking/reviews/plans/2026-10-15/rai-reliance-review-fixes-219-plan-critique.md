---
title: RAI reliance review fixes final-candidate plan critique
description: Single bounded credibility assessment for follow-up 219-review-fixes
ms.date: 2026-10-15
---

## Metadata

* Task ID: 219-review-fixes.
* Slug: rai-reliance-review-fixes-219.
* Critique date: 2026-10-15.
* Plan: .copilot-tracking/plans/2026-10-15/rai-reliance-review-fixes-219-plan.md.
* Phase details: .copilot-tracking/details/2026-10-15/rai-reliance-review-fixes-219-phase-details.md.
* Critique execution status: Complete.
* Execution: exactly one final-candidate assessment; no implementation, test execution, nested delegation or source-artifact modification.

## Inputs and Criterion Boundary

* Primary evidence: the supplied plan, phase details and original .copilot-tracking/reviews/logs/2026-10-15/src-rai-release-record-219-review.md, including its actual reproductions and RV-001 through RV-004 dispositions.
* Caller requirements: retain the current worktree, feat/src-rai-release-record-219 and PR 315; use local core/API suites, CI API PYTHONPATH, the specified /tmp/zf164 tooling and pip-only restoration; avoid mvp, protected/private data paths and prohibited new SQL. No commands using that tooling were executed by this critique.
* Change budget: one existing test owner, src/api/tests/test_assistant_release.py; at most eight added test methods and one added route helper; no removals, new modules or test files.
* Bounded source checks: src/core/src/zava_forward/core/ai_registry.py, src/core/src/zava_forward/core/store.py, src/core/src/zava_forward/core/sqlstore.py, src/core/src/zava_forward/core/ai_tasks.py and src/api/tests/test_assistant_release.py. These establish the existing guard, cache and test-owner seams, not implementation correctness.
* Repository context consulted: docs/case_study_48_original.md, the relevant opening exercise/governance context in docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md. Memory was treated as context, not acceptance evidence.
* Acceptance boundary: assess whether the proposed corrections and semantic regressions can close RV-001 through RV-003 locally while preserving manual/template review, rejection and historical-output invalidation. Do not certify live use, human authority, real evaluation or platform acceptance.
* Dependencies and decisions: P01 supplies corrected behavior for P02 validation/publication. The caller has already selected the branch, PR, toolchain, scope and test budget. The original review is historical; its statement that no PR existed then does not contradict the caller's current PR 315 direction.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| RV-001: inference-off historical references | Covered | Acceptance Criteria explicitly require SQL/JSON ordinary/document accept/edit, cached AI and priority view/review denial for absent/malformed references. P01 requires a nonempty valid exact reference and current selection independently of inference configuration. This addresses the reproduced None-equals-None guard failure. |
| RV-001: preserve ordinary human routes | Covered | Functional Requirements and P01 preserve manual/template acceptance and AI rejection. These are required positive controls, not permission to accept invalid AI history. |
| RV-002: current fast/strong routing | Covered | Functional Requirements and P01 derive the current route from registered metadata for all six retained tasks, not the historical output alias. Current selection and exact original invocation reference are separate requirements. |
| RV-002: observable reliance and non-revival | Covered | Acceptance Criteria and P01 require cached-output and ordinary/document/priority accept/edit route-change checks, fast and strong changes, and renewal that cannot revive old outputs. Existing source has shared reliance seams suitable for the one-helper budget. |
| RV-003: denied-cache approval recovery | Covered | P01 specifies denied configured fallback must not hide approval at unchanged store version. Acceptance Criteria require deny/repeat/approve/request and exactly one scripted call without case editing, an observable cache-lifecycle regression rather than a mocked guard result. |
| Semantic regression ownership and size | Covered | Plan Critique Disposition requires the three actual failure scenarios, not guard proxies; P01 owns all new tests in the existing API release file with an eight-method ceiling. Table-driven subtests can exercise the required combinations without new test modules. |
| P01-T01: reproduce before correction | Covered | The task explicitly orders adding regressions, reproducing defects and correcting shared guards/cache. P02-T01 reiterates capturing targeted failing evidence before fixes; it is a cross-phase execution requirement, not a requirement to postpone reproduction until after P01. |
| P02-T01: local validation and evidence | Covered | Details give core/API unittest commands, API PYTHONPATH=../core/tests:../agents/tests, specified Python/ruff/mypy tooling, lint/format/type checks in both projects and pip-only restoration after missing-package evidence. Actual outcomes and skips must be recorded, with no live-service claims. |
| Scope, SQL and documentation boundaries | Covered | Plan excludes schema, dependencies, private data and protected-path changes, requires existing portable SQL and limits changes to retained reliance/routing/cache, owning tests and directly related README. No implementation requires expanding those boundaries on the supplied evidence. |
| P02-T02: delivery continuity | Covered | Same-topic commit/push and existing PR 315 update preserve Refs #219, required identity/trailer, unmet criteria and no merge. The phase's one later bounded implementation review is expressly requested for this follow-up; it does not authorize another plan critique. |
| RV-004: human/platform evidence | Covered, deliberately open | Plan and details retain named holders/competent oversight, actual approved evaluation/serving proof, Docker/SQL Server/Azure and direct human acceptance as unverified follow-ups. Local engineering acceptance and PR readiness do not close those gates. |

## Verdict

* Verdict: Pass.
* Rationale: the narrow plan directly addresses each reproduced failure and requires behavioral regressions on the affected reliance surfaces. It separates valid reference shape, present current-route selection and exact historical identity, and it specifies approval-only cache recovery with an observable call count. Implementation fits the existing guard/cache seams and bounded test owner without an additional module, schema change or authority decision.
* Severity summary: 0 Critical, 0 High, 0 Medium, 0 Low actionable findings.
* This is planning credibility, not closure of RV-001 through RV-003. Those findings remain engineering acceptance blockers until the planned implementation and actual validation establish resolution.

## Findings

The complete actionable PC set is empty. No substantive plan correction is required by the supplied boundary; no findings are withheld for a later critique.

* Planner-owned compatible corrections: none required. The planning parent may record this Pass in its own disposition without changing scope or obtaining another critique.
* Significant or divergent user decisions: none. Reopening branch/PR selection, increasing test/module budgets, adding platforms or treating RV-004 as engineering evidence would conflict with current direction rather than resolve a planning gap.

## Strengths and Residual Risk

* The semantic acceptance requirements are stronger than testing release_current alone: review actions must deny, priority view must become non-actionable, invalid cached AI must not be reused, and approval must recover briefing generation without a case edit.
* The original reference remains authoritative for historical identity; a fresh matching release must not make old output acceptable merely because the current route has become authorized again.
* Manual/template acceptance and invalid-AI rejection remain explicit positive controls. Their preservation prevents fail-closed fixes from blocking ordinary human work.
* The eight-method ceiling is feasible with subtests, but implementation must genuinely exercise SQL and JSON, ordinary and document records, both route classes, priority view/review and the complete cache recovery sequence. Counting methods or passing helper-only tests cannot substitute for these acceptance outcomes.
* RV-004 remains an accepted scope exclusion, not an accepted live-use risk. Its owners still owe the actual human, evaluation and platform evidence before the respective operational gates can close.
* The plan's origin/main conflict-resolution script reference is historical in the phase details. This critique neither executes it nor authorizes additional merge/conflict handling; the current task writes only this artifact.

## Questions or Blocking Evidence Gaps

* None for the bounded planning assessment. Unavailable RV-004 evidence is explicitly excluded and must remain open; it does not prevent assessing the three known engineering defects.

## Limitations

* No source changes, failing regressions, full suites, lint/type checks, GitHub mutations or provider/platform exercises were performed. Existing tests were inspected only to assess ownership and feasible extension.
* Current PR lifecycle and earlier merge history were not independently queried; the caller's explicit same-branch/PR 315 direction controls this assessment.
* Initial git inspection showed the supplied plan/details and session state as untracked. They were preserved; no existing work was moved, staged, committed or rewritten.
* Only the specified critique artifact is written. Plan, phase details, original review and state remain unchanged.

## Recommended Next Action

* Highest-impact finding: none.
* Action owner: active planning parent.
* Smallest next action: record the Complete / Pass disposition, finalize the supplied plan and continue to implementation with the specified semantic regressions and existing change budget.
* User response required: no.
* Do not run another plan critique. Close RV-001 through RV-003 only against actual implementation evidence, and retain RV-004 and unmet issue criteria as open.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-15/rai-reliance-review-fixes-219-plan.md](.copilot-tracking/plans/2026-10-15/rai-reliance-review-fixes-219-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-15/rai-reliance-review-fixes-219-phase-details.md](.copilot-tracking/details/2026-10-15/rai-reliance-review-fixes-219-phase-details.md) | Assessed phase details and validation boundary |
| [.copilot-tracking/reviews/logs/2026-10-15/src-rai-release-record-219-review.md](.copilot-tracking/reviews/logs/2026-10-15/src-rai-release-record-219-review.md) | Original defect reproductions and open RV-004 evidence |
| [.copilot-tracking/reviews/plans/2026-10-15/rai-reliance-review-fixes-219-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-15/rai-reliance-review-fixes-219-plan-critique.md) | This single final-candidate critique |

## Next Steps

Return Complete / Pass to the active planning parent for finalization and implementation handoff. No user action, new decision or repeat critique is required. This critique stops after its one artifact.
