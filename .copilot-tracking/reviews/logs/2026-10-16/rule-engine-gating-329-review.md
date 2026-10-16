---
title: RPI Review - Rule engine gating regressions
description: Single post-implementation review for issue 329
ms.date: 2026-10-16
---

## Scope and Evidence

* Task ID: 329; task slug: rule-engine-gating-329.
* Review date: 2026-10-16.
* Assessed boundary: completed test/documentation implementation and validation
  in P01-T01 and P01-T02. Remote publication is pending delivery work, not a
  claim of implemented behavior or completed PR.
* Plan: .copilot-tracking/plans/2026-10-16/rule-engine-gating-329-plan.md.
* Details: .copilot-tracking/details/2026-10-16/rule-engine-gating-329-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-16/rule-engine-gating-329-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-16/rule-engine-gating-329-changes.md.
* Evidence: issue 329, regression diff, installed-core unit/mutation/static-check
  outputs, core README and reference routing/log. Research reused.

## Opening Review State

* Goal: compare the exact gating/throttle requirements against implemented tests
  and mutation evidence, without treating synthetic approvals as real approval.
* Evidence readiness: one coherent reconciled artifact set, one passing
  critique, source/test/docs diff and completed local validation.
* Acceptance basis: exact source labels, distinct episodes, persisted checks and
  publication limits, UTC boundary, independent keys and breach bypass.
* First comparison boundary: test inputs and assertions against citation and
  publication code, then validation and documentary claims.
* Authority: read-only implementation/plan/changes; write only this review record.
* Initial blockers: none. Remote publication not yet assessed as completed.

## Execution Status

* Execution status: Complete.
* Exactly one post-implementation comparison completed for the declared
  test/documentation boundary. No review worker or repeat review was needed.

## Plan-to-Change Reconciliation

| Marker | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 | Existing source test tightened; three methods added; fixture card ID and raw-publication helper | Complete, below six-method maximum; no tests removed |
| P01-T02 local validation/docs | Targeted/full tests, Ruff, mypy, nine mutations, README/index/log | Complete for assessed implementation boundary |
| P01-T02 delivery | Commit/push/PR not performed at review time | Explicitly pending; not falsely marked complete |
| Follow-Up Items | None in plan and changes | Consistent; no invented implementation work |

## Completed Work Assessment

* Exact consultation/historical/future labels replace permissive assertions.
  Active card status and citation metadata ensure the test is not passing due
  to an unrelated inactive card. No evaluator invocation and no raw publication
  are asserted; partial/unreviewed/stale/missing remain unknown.
* Distinct cases change the episode case dimension while retaining
  home/card/step/item. Same-case awareness changes alter due time and revision.
  Published episode IDs differ at the boundary. Check IDs and raw persisted
  checks/checkpoint counts prove attempts were evaluated rather than replayed.
* A 100-hour attention window keeps attempts in attention across the boundary.
  One-minute and 24-hour-minus-one-microsecond attempts are in distinct schedule
  buckets; the exact 24-hour attempt publishes. Episode-only deduplication
  cannot satisfy this test, as its mutation confirms.
* Independent-key tests hold the other key dimensions equal and require a new
  raw publication. Cross-case breach test requires immediate breach publication
  plus acknowledgement and outcome obligations.
* Only tests, related documentation and task artifacts change. No SQL syntax,
  package runtime, private data or deployment changes.

## Implementation-Time Update and Critique Assessment

* One final-candidate critique: Pass, no findings to dispose.
* Production-code gate respected: original implementation passes new tests;
  no speculative defect fix introduced.
* Subtest first-case isolation is a fixture correction within approved scope,
  not a product decision or material divergence. Changes evidence records it.
* Plan markers, phase details, changes, validation and remaining delivery work
  agree. No dependent work proceeded through an unresolved decision.

## Findings and Defects

None. Severity counts: Critical 0, High 0, Medium 0, Low 0.
No implementation, planning or research finding requires routing.

## Validation Evidence

| Check | Result |
| --- | --- |
| Original targeted baseline | 17 tests passed |
| New targeted suite | 20 tests passed |
| Full core suite | 466 tests run, OK, one explicit isolated-Azure-SQL opt-in skip |
| Ruff check / format | Passed / 36 files already formatted |
| Mypy | Passed, 89 source files |
| Independent consultation/historical/future guard mutations | Intended assertion failures; no unittest errors |
| Shared-throttle removal with episode deduplication retained | Both distinct-case and due-time scenario assertions fail |
| Exact-boundary comparison mutation | Both scenario assertions fail |
| Four omitted throttle-key dimension mutations | Each intended isolation assertion fails |
| Git diff check | Passed; runtime rule_engine.py unchanged |
| Markdown/link review | Existing relative README/API links and anchor retained; log append-only; no new knowledge page |

Mutation evidence demonstrates regression sensitivity, not real-source or
operational acceptance. Existing sensor-backfill ResourceWarnings are unrelated.
No unexecuted cloud or live SQL Server test is reported as passed.

## Outcome

* Outcome: Conformant.
* Execution: Complete for the declared test/documentation implementation
  boundary, independently of pending publication.
* Rationale: issue 329's specific missed mutation sensitivities are now guarded;
  preserved checks, boundary semantics and non-suppressed breach behavior are
  explicitly covered. No production defect is revealed.

## Closeout Routing Record

| Finding class | Destination | Next action |
| --- | --- | --- |
| Implementation defect | None | None |
| Decision gap | None | None |
| Material evidence gap | None | None |
| Remaining delivery | Parent orchestration | Commit, non-forced push and references-only PR; record actual URL |

Blockers: none. Hosted checks and owner merge decision remain separate from
this local review; no new child implementation work is justified by this task.
