---
title: Transactional hazard hold review follow-up assessment
description: Single review of the selected RV-001 correction and RV-002 documentation
ms.date: 2026-10-15
---

## Execution and Outcome

Task hazard-hold-rv001; parent src-hazard-referral-85; issue 85; PR 314.
Review execution: Complete. Review outcome: Residual work.
RV-001 is corrected within the assessed local engineering boundary.
RV-002 documentation is honest; authority/timing ratification remains open.
No new local implementation defect found. No product/operational acceptance.
Exactly one post-implementation review in this selected child task; no repeat
of the parent's completed review and no further correction loop.

## Compared Artifacts

* .copilot-tracking/research/2026-10-15/hazard-hold-rv001-research.md
* .copilot-tracking/plans/2026-10-15/hazard-hold-rv001-plan.md
* .copilot-tracking/details/2026-10-15/hazard-hold-rv001-phase-details.md
* .copilot-tracking/reviews/plans/2026-10-15/hazard-hold-rv001-plan-critique.md
* .copilot-tracking/changes/2026-10-15/hazard-hold-rv001-changes.md
* .copilot-tracking/reviews/logs/2026-10-15/src-hazard-referral-85-review.md
* Current correction diff in sqlstore.py, store.py, test_hazard_referral.py
  and core/API READMEs; procurement/quality/signoff call sites and existing
  MssqlStore transaction adapter contract.

## Requirement and Evidence Assessment

| Boundary | Assessment |
| --- | --- |
| Actual Completed reproduction | New test first failed on all five procurement transitions before the fix, including completion; preserved red command/result |
| Every guarded transition | Shared require_safety_clear registers dependencies for procurement, quality and signoff; advancement explicitly joins it without changing prior gate explanations |
| Transaction-local state | save reads current case body/rowversion after existing writer begin and before writes, applies base safety predicate, then checks optimistic version |
| Check-to-commit race | Existing cross-process writer serialization spans validation and commit; real second SQLite writer cannot commit inside that interval |
| No unchanged-case shortcut | Dependency validation runs independently of touched-case body comparison; procurement-only transitions cannot skip it |
| Refusal atomicity | GateError and ConflictError rollback and discard case/procurement edits, pending audit and dependency state; reopened store has original work-order/quality/signoff/stage state and retained hold |
| Request lifecycle | Successful save, discard and outer lock exit clear dependencies; stale-clear conflicts and unsaved-precheck tests preserve unrelated work and safe withdrawal |
| SQL portability | New SQL is only parameterized SELECT of existing columns; MssqlStore inherits validation under its transaction-owned application lock; no new dialect, schema or driver-specific exception assumption |
| RV-002 documentation | Both component READMEs explicitly say release authority and response/resident-update/escalation policy are unratified; no invented approval or timetable |
| Existing behavior | Sequential JSON/SQLite and loopback HTTP tests retained; full core/API suites pass; consent/building/role controls unchanged |
| Plan/critique reconciliation | P01-T01/P01-T02/P02-T01 complete; one independent critique Pass, no PC findings; four new methods below eight-method ceiling, no removals |
| Implementation discovery | Current-source PYTHONPATH binding is a necessary local environment correction, reflected in plan/details/changes; no significant decision divergence |
| Delivery boundary | P02-T02 authorized commit/push/PR-ready bookkeeping follows this review; no new PR, force-push, main push or merge authorized |

## Validation Considered

* Core: 325 tests passed, 118.749s.
* API: 475 run, OK with 97 optional/environment skips, 199.856s.
* Targeted hazard semantics: 18 passed; targeted synthetic HTTP app: 3 passed.
* Nine interleaved transition subtests plus stale-clear dependency, unsaved
  request cleanup, transaction-local SQL trace and concurrent writer ordering.
* Core/API ruff lint and format checks passed; mypy 71/36 source files passed.
* git diff --check passed. New SQL uses existing placeholders and no banned
  SQLite-specific syntax. Excluded paths and mvp have no correction edits.
* Tests explicitly bind this worktree sources; no changes to shared editable
  installation, dependency manifests or environment files.
* No actual SQL Server/Azure, verified transport, real model, browser/human,
  container build/runtime/scan or policy approval is claimed by this review.
  Current local commands/results, including initial failures, are in changes.

## Findings and Routing

### RV-001 High: corrected in the selected implementation

No active hold can commit before a guarded completion and then be bypassed
by it under the assessed serialized-writer protocol. Persisted state and
audit prove refusal; the opposite valid serialization (completion first,
intake second) is also covered. Actual SQL Server runtime evidence remains
part of RV-003, not claimed from SQLite.

### RV-002 Medium: policy ratification remains open

The documentation request is satisfied, not the underlying owner decision.
Repairs/Safety/Housing must approve operational responsibility, release
authority, response/resident-update timing and escalation. Route to later
rpi-plan with accountable owners. Keep original acceptance boxes unticked.

### RV-003 Medium: verified service and live acceptance remain open

Human-recorded evidence is not verified transport. No actual model/SQL Server/
Azure or human acceptance is supplied. Route to later rpi-research and a distinct
permitted validation task. This is inherited residual work, not a new code defect.

## Handoff

Local correction ready for code review, not accepted for operational rollout.
Proceed only with explicitly authorized same-branch delivery and PR readiness.
No further source changes or review execution in this loop. CI and owner
merge decision remain separate; do not merge or check original issue criteria.
