---
title: Proper Warm Exercise Rebuild Review
description: One implementation review with separate execution and acceptance outcome
ms.date: 2026-10-10
---

## Scope and Evidence

* Task ID: exercise-poc-rebuild-2026-10-10.
* Review scope: complete accepted rebuild boundary, with implemented local
  change assessment and explicit unexecuted/blocked requirements.
* Plan: .copilot-tracking/plans/2026-10-10/exercise-poc-rebuild-plan.md.
* Details: .copilot-tracking/details/2026-10-10/exercise-poc-rebuild-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-10/exercise-poc-rebuild-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-10/exercise-poc-rebuild-changes.md.
* Requirement/results: .copilot-tracking/changes/2026-10-10/exercise-poc-rebuild-acceptance.md.
* Baseline: docs/prds/proper-warm-retrofit-programme-demonstrator.md v0.12.0
  and docs/case_study_48_addendum.md exercise assumptions.

## Opening Review State

The goal is to assess the implemented local slice and full-scope remaining
gaps once, not to infer full acceptance from its passing engineering tests.
Plan/details/changes are reconciled: P01-P04 completed, P05/P06 partial.
Current evidence includes 355 regression tests with 26 live SQL skips,
22 finite browser checks, 200 warm HTTP samples per operation, exact clean
restart/backup case/audit-head equality and non-root/read-only image startup.
The first comparison examines source/proposal/version invalidation and exact
financial predecessor bindings; its independent lens is read-only.
Only this review record may be written during review. Source fixes are later
work, not a repeated review/correction pass.
Initial blockers: no Decision 1 deployment/verified billable authorization,
unexecuted required workload/recovery/live/human evaluation and incomplete
handoff/update/full fixture acceptance.

## Execution Status

Partial: the one local independent integrity assessment is complete; actual
platform/human and full runtime acceptance cannot be reviewed as executed
evidence. Four substantive code defects were reproduced, including SQLite
persistence, by the read-only assessment.

## Plan-to-Change Reconciliation

| Plan scope | Evidence | Assessment |
| --- | --- | --- |
| P01-P04 | Domain/provider/fixture tests and merged PRD | Completed local components; live provider success not claimed. |
| P05 | Ten connected tests and seven data-contract tests | Local journey works, but funding-chain defects and handoff/update/fixture omissions prevent full acceptance. |
| P06 | 355 tests, 22 browser checks, sampled HTTP/clean backup and image | Engineering checks pass; exact workloads/recovery/accessibility/live/human gates unavailable or unexecuted. Publication must be draft, not ready to merge. |

## Implementation-Time Updates and Critique

PC-001 through PC-005 were incorporated in the original plan before dependent
implementation: common guard, external authority, generative provenance,
actual text/table extraction and isolated startup. No second critique ran.
Related integration adjustments preserved the owner's fictional exercise,
USD 450 ceiling and human-control intent. The narrower workbook contract,
finite browser probes and sampled HTTP/clean backup are documented as subsets,
not accepted reductions of the complete PRD. No review or human signature
has been manufactured.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Upstream financial staleness does not propagate

* Evidence: mvp/properwarm_mvp/store.py _exercise_reconcile_dependents,
  lines 697-704 at assessment.
* Reproduction: record award and accepted claim on separate forms; correct an
  application field; record cash against that claim. The award becomes stale
  but claim descendants remain current and cash succeeds.
* Impact: financial evidence proceeds against a suspended award.
* Destination: later rpi-implement; traverse exact preceding-event chains and
  stale all and only dependent financial events, with independent snapshot tests.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Historical stale awards override a fresh current award

* Evidence: mvp/properwarm_mvp/store.py _exercise_reconcile_dependents,
  lines 703-707 at assessment.
* Reproduction: invalidate an old award; record a newly reviewed application
  and fresh award. funding_ok becomes true, but exporting the current form
  resets it false because historical stale awards are still processed.
* Impact: otherwise-current readiness cannot recover after correction.
* Destination: later rpi-implement; derive readiness from an explicitly
  current/superseding award, preserving historical records without activating them.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Cash ceiling resets across claim attempts

* Evidence: mvp/properwarm_mvp/store.py _exercise_funding_event,
  lines 820-824 at assessment.
* Reproduction: receive GBP 7500, invalidate that claim through field
  revalidation, then record another accepted claim on the unchanged award.
  Another GBP 7500 receipt succeeds: total GBP 15000 against GBP 7500.
* Impact: retained real receipt evidence is excluded from cumulative exposure.
  No real money moves, but the demonstrator's financial-control claim is false.
* Destination: later rpi-implement; cap retained receipts across the same award/
  opportunity chain and reconcile corrected claims without erasing historical cash.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Re-export alone permits an unchanged rejected pack retry

* Evidence: mvp/properwarm_mvp/store.py _exercise_funding_event,
  lines 775-782 at assessment.
* Reproduction: reject an application, export the unchanged form again,
  then resubmit export-2 with retry_of. The digest is identical and only the
  original review exists, but the new export ID passes the correction check.
* Impact: fresh external attempts do not require actual correction/re-review.
* Destination: later rpi-implement; require a changed content/version digest
  and independent current re-review before corrected resubmission.

<!-- rpi:review id=RV-005 -->
### RV-005 [High]: Complete accepted local workflow contracts remain unfinished

* Evidence: exercise-poc-rebuild-acceptance.md, FR-011/033 and AC-035/036;
  remaining lifecycle-return, hazard receipt/acceptance and full fixture checks.
* Impact: the working one-home journey does not establish the requested
  complete PRD end-to-end capability or eleven/nine task coverage.
* Destination: later rpi-implement; finish explicit handoff/update/return
  states and independent oracle-based acceptance before full delivery claims.

<!-- rpi:review id=RV-006 -->
### RV-006 [High]: Required actual platform evidence and safe activation are blocked

* Evidence: E02/E04 fake-only/default no-call evidence and Foundry metadata:
  no Decision 1 deployment, unverified response/terms/price/quota/authorization.
* Impact: no actual selection/support/generation, 120-family adjudicated
  evaluation or net-effort benefit is demonstrated. Cross-process/provider
  liability accounting is not established before activating either adapter.
* Destination: focused platform prerequisite research/operator verification,
  then later rpi-implement for shared cost accounting and bounded real evaluations.
  No broad company discovery or relaxed budget/control gate is needed.

<!-- rpi:review id=RV-007 -->
### RV-007 [Medium]: Prescribed runtime/recovery/accessibility shapes are unexecuted

* Evidence: E06/E07 explicitly label subset workloads and missing checks.
* Impact: one-session latencies and clean backup cannot satisfy concurrent
  30-minute core/scale, failure/RPO, screen-reader/contrast/targets/zoom acceptance.
* Destination: later rpi-implement validation work, with exact populations,
  request mix, concurrency, interruption points and independently retained results.

## Routed Findings

| Finding | Destination | Priority |
| --- | --- | --- |
| RV-003 | rpi-implement: award-chain cash cap | First: explicit double-counted receipt exposure. |
| RV-001/002 | rpi-implement: transitive stale/current-award recovery | Second: financial correctness and recovery. |
| RV-004 | rpi-implement: corrected re-reviewed retries | Third: rejection control integrity. |
| RV-005 | rpi-implement: full workflow/fixture contracts | Required before full end-to-end acceptance. |
| RV-006 | Focused platform verification, then rpi-implement | Actual Foundry and cost prerequisite, not fictional company facts. |
| RV-007 | rpi-implement: exact validation workload | Independent full-shape evidence, not proxy timing results. |

No source fixes were made during this review; no second review is proposed.
Later user-directed implementation owns routed corrections.

## Validation Evidence

Engineering evidence E01-E09 is recorded in the acceptance register.
The independent source assessment reproduced RV-001, RV-002 and RV-004 through
SQLite exercise_action/save, and RV-003 against one unchanged award.
Passing regression tests did not include these failure paths and therefore
do not refute the findings.

## Outcome

**Not accepted** for the complete user task. A useful local exercise slice and
reproducible engineering evidence exist, but three High financial defects,
one Medium rejection defect, incomplete local contracts and required external/
runtime/human gates remain. Publish only a clearly labelled draft implementation
PR, keeping real inference disabled. The task is not complete.
