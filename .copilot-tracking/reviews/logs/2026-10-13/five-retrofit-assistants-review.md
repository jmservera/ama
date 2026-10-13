<!-- markdownlint-disable-file -->
---
title: Five Retrofit Assistants Delivery Review
ms.date: 2026-10-13
---

## Scope and Evidence

* Task: five-retrofit-assistants-2026-10-13; full task reviewed once.
* Plan: .copilot-tracking/plans/2026-10-13/five-retrofit-assistants-plan.md.
* Details: .copilot-tracking/details/2026-10-13/five-retrofit-assistants-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-13/five-retrofit-assistants-plan-critique.md.
* Research: .copilot-tracking/research/2026-10-13/five-retrofit-assistants-research.md.
* Changes: .copilot-tracking/changes/2026-10-13/five-retrofit-assistants-changes.md.
* Source: c4b28e3168770252fb35a79074dc2202ef375514.
* CI: https://github.com/jmservera/ama/actions/runs/38446725200.
* Current canonical documents and 13 MVP source/UI/test files.

## Opening Review State

Review full requested document/runtime/build outcome against PC-001 to PC-008,
PRD FR-047/AC-058 to AC-061 and mandatory CON-009/AC-057.
P01/P02 complete, P03 remains unchecked for actual accepted Azure delivery.
Exact local image and passing source CI establish local technical progress,
not model calibration/human acceptance or changed-version real-service proof.
First compare completed contracts/durability/source/review behavior; then
reconcile remaining delivery and distinct follow-up gates. Read-only evidence;
only this review record may change during Review. Initial blocker: scoped
live rollout/finite budget approval unavailable. No second critique or Review.

## Execution Status

Complete. One parent full-task comparison and one bounded read-only runtime
lens executed. Local SQL bootstrap failed, CI general SQL Server parity
passed; new-assistant live SQL/provider unexecuted. Review completion is not
full implementation or accepted delivery.

## Validation Evidence

* Parent full suite: 333 discovered, 307 pass, 26 integration skips; targeted 44 pass.
* Worker-reported Chromium: 15 checks pass, no human/mobile acceptance claimed.
* Source CI passes unit/JS, image/hardening/Trivy/SBOM and actual SQL Server
  general parity (26 tests); no new-assistant actual SQL or provider proof.
* Local exact-source image a9314193655f4a206553cd294cd9df0b280c40d497ca3c067f32c18d891a54e3
  as UID10001. This is an image ID, not an ACR manifest/serving digest.
* Documentation: zero new link/fragment/frontmatter failures and preserved
  original/memory/regulatory sources.
* Actual live deployment/model/SQL restart/control acceptance: Blocked.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Accepted changed-version real-platform delivery is blocked

* Related scope: P03/P03-T01, CON-009/AC-057, PC-007.
* Evidence: current source/image and passing CI are local/technical evidence.
  Specific retained-data rollout/finite incremental approval was unavailable;
  the existing --0000009 serving app was not changed. No registered real
  assistant/provider/usage and independent actual SQL before/after/restart.
* Impact: the requested version is implemented/built/published as source, but
  cannot be represented as an accepted delivered AMA application build.
* Destination: later rpi-implement after owner scoped approval.
* Smallest next action: approve specific existing-app rollout and finite
  allowance, preserve private config/data/rollback fingerprints, deploy the
  exact image and run required real provider/SQL/control checks.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: New-assistant real SQL path is not covered by general parity

* Related scope: P02/P03, AC-059/060/061 and PC-001/004/006.
* Evidence: CI ran 26 general SQL Server store tests successfully. The
  disposable local SQL login could not be established, so the separately
  authored five-proposal SQL generation/review/restart probe did not run.
* Impact: SQLite race fixtures/dialect emulation and existing store parity
  do not prove the new assistant tables, reservations and atomic review on
  actual SQL Server/Azure SQL.
* Destination: later rpi-implement, coordinated with RV-001.
* Smallest next action: obtain reproducible SQL test execution and exercise
  new-task migrations/leases/reservations/role-source review and recovery
  against actual SQL, preserving live data and distinct provider evidence.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Shutdown can admit a new provider dispatch after stop returns

* Related scope: P02, PC-005/AC-061. Confidence High; static control-flow
  evidence, not a live observation.
* Evidence: mvp/zavaforward_mvp/assistants.py, execute/_worker/stop.
  Worker passes its stop check, blocks polling/claim, stop sets event and
  finishes bounded joins, then resumed execute claims/reserves and starts
  the provider thread before checking stop_event in its wait loop.
* Impact: a new bounded billable dispatch can begin after shutdown admission
  should close. Reservations/fencing still apply; no unlimited-spend claim.
* Destination: later rpi-implement.
* Smallest next action: coordinate stop and provider admission; preserve
  conservative existing reservations. Interleave blocked polling/claim,
  stop and resume in a nonbillable test, asserting zero new dispatches.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Auxiliary assistant requests block ordinary case rendering

* Related scope: P02, PC-005/AC-061. Confidence High; static control-flow
  evidence, not a live observation.
* Evidence: mvp/web/app.js, caseView awaits assistantCasePanel before rendering
  controls; mvp/web/assistants.js uses Promise.all for registry/proposals with
  no deadline. A pending assistant response never reaches the error catch.
* Impact: successful ordinary case retrieval can still leave manual controls
  unavailable indefinitely when an auxiliary request stalls.
* Destination: later rpi-implement.
* Smallest next action: render ordinary controls independently, populate
  assistance asynchronously with bounded timeout/manual fallback and stale-
  render protection. Hold an assistant response pending in a nonbillable
  browser test and assert manual controls remain usable.

## Plan-to-Change Reconciliation

| Scope | Evidence | Assessment |
| --- | --- | --- |
| P01/P01-T01 | PRD v0.14.0, five contracts, FR-047/AC-058 to AC-061, 47/61 traceability, ADRs/index/log | Complete source amendment; fresh formal requirements/owner acceptance still open |
| P02/P02-T01 | 13 MVP files, source c4b28e3, registry/queue/claims/limits/review; tests and source CI | Implemented/local checks pass, but RV-003/004 are open release-relevant defects |
| P03/P03-T01 | Local exact-source image, non-root/hardening and source CI, source pushed to #68 | Partial: actual accepted cloud delivery blocked; marker correctly unchecked |
| Phase split | Same scope split into write-disjoint P01/P02/P03 for independent platform inspection | Ordinary execution ownership change, not new scope/authority |
| Safe failure reporting | Fixed warnings and backoff, private-text regression | Tightly coupled pre-Review correction, not a second critique/review |

## Critique and Material Revision Assessment

PC-001 to PC-008 accepted in plan/details. Source implementation addresses the
durable/source/review/boundary contracts, with tests documented. Actual-dialect
and live delivery proof remains explicitly incomplete (RV-001/002), not a
claim every critique's acceptance evidence passed. No material scope or
unaccepted company-control/spend expansion. Earlier procedural Not ready was
superseded by explicit owner autonomous direction; actual rollout authority
was not inferred from that or from the #58 exception.

## Plan Follow-Up Assessment

Role/accessibility acceptance, semantic calibration and comparative task
benefit remain distinct follow-ups, not runtime approval or fabricated
results. Owner/product and competent reviewers own those exercises.
Separate queue/worker estate remains deferred pending evidence of material
need; no new infrastructure is justified by this review.

## Outcome

Not accepted. Local source/image exist and source CI passes, but RV-003/004
violate bounded shutdown/manual-access contracts and RV-001/002 leave mandatory
new-version platform/dialect evidence incomplete. No conformant full delivery,
formal PRD adoption, human acceptance or measured benefit is claimed.

## Defects and Routed Findings

| Finding | Class | Destination and next owner |
| --- | --- | --- |
| RV-003/004 | Implementation defects | Later rpi-implement; selected runtime-fix task, before live rollout |
| RV-001 | Scoped approval and missing actual delivery | Owner rollout/finite allowance confirmation, then later rpi-implement exact-image provider/SQL/control proof |
| RV-002 | New-assistant actual SQL validation gap | Later rpi-implement; reproducible disposable SQL and changed Azure SQL path, coordinated with RV-001 |

There is no significant new scope/architecture decision or additional research
requirement identified. The existing live approval blocker remains explicit.
Do not loop back to Implement or repeat Review inside this task; later
user-selected work owns the fixes/evidence.

## Residual Work

* Owner/product-led staff, role, source-verification and accessibility exercise:
  direct human acceptance remains outside this technical build.
* Data/performance and competent reviewers: per-task semantic calibration and
  paired rules/manual comparisons including review/correction burden.
* Separate worker/queue estate: defer until evidenced need, not a new default.

## Blockers and Remaining Work

P03/P03-T01 remains unchecked for actual accepted delivery. Specific rollout/
finite allowance approval unavailable. Fix RV-003/004 before exercising the
new version live; do not bypass human/current-source controls or reseed data.
Source/build boundary published on consolidated #68; this review/route record
is the final publication step. No PR merge or draft closure.

## Closeout Routing Record

* Review execution: Complete; outcome: Not accepted.
* Implementation defects: RV-003/004 -> later rpi-implement.
* Scoped permission/delivery and validation: RV-001/002 -> owner approval
  plus later rpi-implement; no new planning choice or research pass required.
* Nonblocking residual: distinct human/accessibility and calibration/value
  follow-ups owned by the exercise owner and appropriate reviewers.
* One Review only; no closure verification or source fixes in this Review.
