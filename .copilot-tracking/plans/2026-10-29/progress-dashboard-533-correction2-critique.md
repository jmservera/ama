---
title: Progress dashboard correction round 2 final-candidate plan critique
ms.date: 2026-10-29
---
<!-- markdownlint-disable-file -->

# RPI Plan Critique: progress-dashboard-533-correction2

## Metadata

* Task ID: 533-correction2-2026-10-29
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction2-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/progress-dashboard-533-correction2-phase-details.md
* Critique execution status: Complete
* Assessment: Exactly one independent final-candidate plan critique.

## Inputs and Criterion Boundary

* Caller requirements: Correct malformed closure/return evidence without aborting progress or archive reads; preserve JSON/SQLite behavior; replace quadratic dashboard work-context/building scans with shared clock-only evaluation. Retain the locked test ownership and addition limits.
* Research: .copilot-tracking/research/2026-10-29/progress-dashboard-533-correction2-research.md, including Q1-Q3, C1-C7, alternatives and stated environment limitations.
* Decisions: Existing feat/progress-dashboard-533 workstream; first pull already completed; local commits only; no push, az, force-push, historical evidence replacement or publication claim.
* Validation criteria: API/core strict mypy, Ruff lint and format checks, current-worktree unit imports, progress browser check, nonblocking heavy-suite lock admission and explicit targeted fallback.
* Dependencies: P01 and P02 must both precede final P03 validation and independent Review. The combined open-case malformed-return regression requires the P02 dashboard bypass as well as P01 lifecycle validation; P01 alone is not expected to make that endpoint regression green.
* Source examined: src/api/src/zava_forward/api/progress.py; src/core/src/zava_forward/core/taskqueues.py; the narrowly relevant Store work-context adapter, building membership scan and handoff projection; existing progress/taskqueue tests, building fixture, project static-check configuration and progress browser harness.
* Repository context: Original case study, addendum opening context, knowledge-base index and owner memory were consulted. No new domain or regulatory conclusion is made.
* Boundary: Assess credibility and readiness of the supplied plan/details, not correctness of an implementation or successful execution of future checks. No application edits, test execution, environment mutation, additional agent or remote operation formed part of this critique.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1, C1, P01-T01: Malformed lifecycle evidence | Covered | Lifecycle currently iterates both auxiliary collections without collection/row guards. Planned list-of-dictionaries validation rejects the whole malformed collection, including irrelevant malformed rows, without treating null as absent. |
| P01-T01: Valid and unknown lifecycle semantics | Covered | Missing/empty collections and non-transition dictionaries remain valid; malformed evidence remains admitted but unknown. Persist/reopen checks cover sibling totals, archive null dates and date-filter exclusion. |
| C4, P01-T01: JSON/SQLite ownership | Covered | Existing SqliteProgressDashboard inherits ProgressDashboard. The plan explicitly requires persisted malformed values and reopened stores rather than relying only on in-memory edits. |
| Q2, C2-C3, P02-T01: Scan removal | Covered | Dashboard currently calls work_context per open case; Store supplies building blockers whose record validation scans case membership. Planned patches make both work_context and building.record fail if invoked during the new dashboard read. |
| C5-C6, P02-T01: Clock parity | Covered | Planned helper preserves ordered hazard response/update, resident update and pending-handoff rows, provenance and snapshot semantics. Existing handoff_view retains chase-owner normalization. |
| P02-T01: Independent regression oracle | Covered | Frozen exact core rows supplement Store-context parity, avoiding reliance solely on two callers of the same extracted helper. Closed/unmarked exclusion and multiple tasks per case protect the aggregate denominator. |
| P01/P02 integration: Open malformed returns | Covered | The plan explicitly exercises this endpoint path; clock-only evaluation avoids the unrelated return-narrative access in taskqueues.context. |
| Test ownership and change budget | Covered | Existing API/core semantic files own the changes; four inherited API methods and two core methods are maximum additions, with no assertion/test removals and fixture reuse. Parameterized coverage fits that boundary. |
| Q3, C7, P03-T01: Static and runtime validation | Covered | Both owning projects configure strict mypy and existing Ruff rules. Plan requires all six project-level static commands, focused units and progress browser checks, with current-worktree source/test paths. |
| P03-T01: Heavy admission and prerequisites | Covered | Full API/core discovery requires one nonblocking lock admission; contention means targeted fallback. Missing Playwright/browser prerequisites and differing tool versions must be recorded, not represented as successful validation or pinned CI equivalence. |
| P03-T02: Evidence, Review and local stop | Covered | Implementation/evidence commit precedes one independent correction-diff Review. Original verdict is retained; closeout commits are local. Later exact-head publication gates remain separate. |

## Verdict

* Verdict: Pass
* Rationale: The plan and details credibly address both supplied defects, preserve the relevant behavior contracts, provide non-circular and backend-persistent regression evidence, and bound validation and delivery appropriately. No substantive plan correction or unresolved user decision was identified within the supplied criterion boundary.
* Severity counts: Critical 0; High 0; Medium 0; Low 0.

## Findings

No actionable PC-xxx findings. This is the complete finding set for this single
assessment; no discoverable concern is being withheld for another critique.
Consequently, there is no finding-specific action owner, resolving evidence or
direct-correction/user-decision disposition to assign.

## Strengths and Residual Risk

* Strict collection validation preserves the distinction between absent evidence and malformed evidence without broad exception handling or partial replay.
* Clock extraction is grounded in the existing algorithm, including released hazards with outstanding deadlines, future completions, strict snapshot boundaries and projected handoff accountability.
* Deterministic call-avoidance assertions directly address the expensive path without an unsupported benchmark or timing threshold.
* P01 and P02 may be authored separately, but the open malformed-return endpoint check must be judged after both are present. P03 already supplies that combined validation boundary.
* Tool versions, browser availability and heavy-lock admission remain execution-time uncertainties explicitly acknowledged by the plan. This Pass accepts their stated reporting/fallback treatment, not an unexecuted check or waiver of required validation.
* The independent Review applies to its recorded correction candidate. A later evidence-only closeout commit does not imply fresh exact-head publication approval.

## Questions or Blocking Evidence Gaps

None for plan readiness. Runtime prerequisite checks and actual validation results
remain the implementation parent's responsibility under P03.

## Limitations

* No implementation was reviewed and no unit, static, browser, performance or full publication gate was run.
* Source reads were restricted to the supplied evidence chain and directly relevant test/validation boundaries; no whole-repository audit was performed.
* Research claims about installed environments and the completed pull were treated as supplied evidence, not independently re-executed.
* Only this critique artifact was written. Plan, phase details, research and historical evidence remain unchanged.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent.
* Smallest next action: Record this single Pass disposition and proceed with the bounded P01/P02 implementation, followed by P03 validation and the one independent Review.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/progress-dashboard-533-correction2-research.md](.copilot-tracking/research/2026-10-29/progress-dashboard-533-correction2-research.md) | Supplied focused research and evidence. |
| [.copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction2-plan.md](.copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction2-plan.md) | Assessed final-candidate plan. |
| [.copilot-tracking/details/2026-10-29/progress-dashboard-533-correction2-phase-details.md](.copilot-tracking/details/2026-10-29/progress-dashboard-533-correction2-phase-details.md) | Assessed phase details. |
| [.copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction2-critique.md](.copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction2-critique.md) | This complete independent critique. |

## Next Steps

No user action is required. Return Complete / Pass to the active planning parent
for disposition and continuation within the existing local-only RPI authorization.
This critique invocation stops here; it does not implement, launch another
assessment, commit or publish.
