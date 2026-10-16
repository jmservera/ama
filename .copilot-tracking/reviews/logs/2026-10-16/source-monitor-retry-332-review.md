---
title: Source monitor retry implementation review
description: One evidence-based implementation assessment for issue 332
ms.date: 2026-10-16
---

## Scope and Evidence

Task: #332 / source-monitor-retry-332. Review date: 2026-10-16.
Assessed boundary: full implementation and local validation P01; P02 publication
is subsequent delivery, not source acceptance.

* .copilot-tracking/research/2026-10-16/source-monitor-retry-332-research.md
* .copilot-tracking/plans/2026-10-16/source-monitor-retry-332-plan.md
* .copilot-tracking/details/2026-10-16/source-monitor-retry-332-phase-details.md
* .copilot-tracking/reviews/plans/2026-10-16/source-monitor-retry-332-plan-critique.md
* .copilot-tracking/changes/2026-10-16/source-monitor-retry-332-changes.md
* Git diff from baseline 736a2e84d0e3caba75155b1244da07cbd71a26b9 and local
  validation outputs recorded in the changes evidence.

## Opening Review State

Goal: determine whether failures no longer postpone successful source checks.
Evidence readiness: P01 reconciled and complete; no missing artifacts.
Acceptance basis: plan requirements, regression and mutation evidence,
portable SQL and preserved chronology/approval boundaries.
First comparison: due() behavior and core/job assertions against the issue.
Read-only boundary: implementation evidence only; write only this Review record.
Initial blockers: none. Publication remains P02-T02 after this assessment.

## Execution Status

Execution: Complete. One post-implementation Review; no repeat planned.

## Plan-to-Change Reconciliation

| Plan scope | Changes evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Success-based cadence and regressions | Complete: latest success anchors cadence; latest attempt protects clock; failure evidence unchanged |
| P01-T02 | Final validation evidence | Complete: both suites/static checks and original-method mutation pass |
| P02-T01 | This record | Complete assessment; parent reconciles delivery markers |
| P02-T02 | Publication | Subsequent delivery step, not claimed complete by Review |
| Follow-Up Items | None | No added out-of-scope work |

## Completed Work Assessment

* Core due() keeps parameter-bound source matching, lock and chronological
  ordering. Every stored body carries error; decoding its non-error value
  correctly recognizes unchanged and changed successful observations.
* Failure-only history remains due after checking the latest attempt date.
  Existing successful history is not reset by early, due-day or repeated
  failed observations. Successful recovery restarts the exact interval.
* Core tests exercise 30/366-day failure-only histories, prior success and
  clock rejection after a later failed attempt. Job tests require actual
  next-day checked reports for missing and explicit error observations.
* SQL remains adapter-portable; no schema change, dialect JSON expression,
  approval path, private data path, hosted schedule or network call was added.
* README behavior matches the implementation and the reference log was
  appended, not rewritten. No knowledge-base synthesis or index topic changed.

## Implementation-Time Plan and Detail Update Assessment

PC-001 proposed project-local scratch beyond the user's actual src build
requirement. Local scratch was used for pip/builds and monitor mutation.
The full core suite proved generator tests intentionally prohibit
repository-local output. Details/plan correctly narrow the scratch advice
to preserve those guards, with no test or runtime bypass. Supported local
execution correction, not an unapproved requirements or architecture change.

The transient SQL timing failure and mutation subtest-count correction are
explicitly recorded. The unchanged performance limit passed the isolated
rerun; the corrected mutation harness verifies assertion failures rather
than accepting setup/import errors. No material decision gap remains.

## Critique and Follow-Up Assessment

Exactly one critique executed. PC-001 is disposed with measured evidence;
no repeated critique or unresolved required decision. No plan follow-ups.
No new live-platform acceptance is required for this bounded cadence fix.

## Findings, Defects and Routed Work

No substantive implementation findings. No RV entries or routed defects.
No residual source work; P02-T02 publication remains with the delivery parent.
No claim of human legal review, Azure verification or hosted CI results.

## Validation Evidence

| Scope | Result | Evidence |
| --- | --- | --- |
| Core unittest discovery | Passed | 466 run, one existing opt-in skip |
| Orchestrator unittest discovery | Passed | 22 passed |
| Core Ruff check/format and mypy | Passed | 36 formatted files; 89 type-checked files |
| Orchestrator Ruff check/format and mypy | Passed | 7 formatted files; 10 type-checked files |
| Original due() in-memory mutation | Passed | Four fixed test methods pass; all four reject original, five assertion failures including subtests, zero errors |
| Git whitespace review | Passed | git diff --check |
| Docker, Azure and live source retrieval | Not run | Explicitly outside user-authorized local validation |

## Outcome

Outcome: Conformant with justified divergence. The only divergence is scratch
placement for unrelated generator tests, preserving their existing safety
guards. No source acceptance criteria remain unmet.

## Closeout Routing Record

Execution Complete; implementation outcome Conformant with justified divergence.
No implementation defect, decision gap, material evidence gap or new residual
follow-up. Delivery parent owns P02-T02 commit, push and PR publication. No
blockers; external PR checks and owner merge decision remain separate.
