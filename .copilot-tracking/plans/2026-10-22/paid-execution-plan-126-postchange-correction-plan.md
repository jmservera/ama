<!-- markdownlint-disable-file -->
# RPI Plan: Paid execution plan #126, post-change forecast correction

## Task Metadata

* Task ID: 126-postchange-correction
* Task slug: paid-execution-plan-126-postchange-correction
* Planning status: ready
* Plan date: 2026-10-22
* Phase details: .copilot-tracking/details/2026-10-22/paid-execution-plan-126-postchange-correction-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-22/paid-execution-plan-126-postchange-correction-plan-critique.md

## Executive Summary

An independent review found that the addendum calls a 14:00Z forecast (535.33, "S0 no change") current although owner-authorized deletion of the cutover-test Front Door Premium and WAF policy and a scale-down of the cutover-test demo API app were later completed and verified. This plan corrects the wording only: observed accrued cost stays; 535.33 and the limits derived from it become an explicitly labelled conservative PRE-CHANGE scenario; no saving or zero residual is invented; a refreshed post-change forecast and inventory are required before any tranche activation. Outside-group spend stays unknown and paid execution stays blocked. Documentation only.

### User Decisions and Requirements Highlights

* USD 700 is the total October forecast ceiling (not additional); expiry 2026-10-25T16:02Z unchanged.
* No new spending permission is needed, but headroom evidence is.

### What You May Not Know

* Cost Management data at 14:53Z is identical to 14:00Z (lag), so no post-change cost evidence exists yet.
* 61 resource names still contain "cutover-test"; remaining items may keep charging.

### Unresolved Decisions or Blockers

* Refreshed post-change forecast (needs complete post-change days); subscription-scope read for U; Blob role; other gates from the prior revision.

## User Decisions and Requirements

* Retain observed accrued costs; label 535.33 and derived limits a conservative PRE-CHANGE scenario; account for deletion and scale-down without inventing exact savings or zero residual charges; require a refreshed post-change forecast before tranche activation.
* Outside-RG costs remain unknown; paid execution blocked.
* No Azure or tenant mutation, inference or deployment; read-only queries only; no scope expansion; preserve prior history, append-only logs and old receipts.
* No closing keyword; issue #126 stays open; no merge.

## Goals

* Remove every contradictory "current" claim about the pre-change forecast across addendum, index and log.

## Scope and Non-Goals

### In Scope

* The 2026-10-22 subsection in docs/case_study_48_addendum.md, the index row in docs/reference/README.md, one appended log entry, new dated artifacts.

### Non-Goals

* Estimating savings; changing the 700 ceiling, thresholds or tranche definitions; infrastructure or source changes.

## Functional Requirements

* The text separates observed, pre-change scenario and (absent) post-change forecast.
  * Observable acceptance criteria: 535.33, 164.67 and 89.67/84.67/74.67/66.67 each carry the pre-change label; no sentence calls them current.
* A refresh gate precedes any tranche.
  * Observable acceptance criteria: stated inputs (fresh inventory, complete post-change days, cost read timestamp) are listed.

## Non-Functional Requirements

* Aggregate non-sensitive evidence only.
  * Objective threshold or evaluation condition: identifier search finds none in additions.
  * Observable acceptance criteria: new complete local gate passes with a new external receipt.

## Acceptance Criteria

* Wording corrected; old history preserved; gate receipt verified; PR updated; ready for another independent review.

## Implementation Context Record

| Context item | Current artifact or record |
|--------------|----------------------------|
| Plan | .copilot-tracking/plans/2026-10-22/paid-execution-plan-126-postchange-correction-plan.md |
| Phase details | .copilot-tracking/details/2026-10-22/paid-execution-plan-126-postchange-correction-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-10-22/paid-execution-plan-126-postchange-correction-plan-critique.md |
| Relevant research | .copilot-tracking/research/2026-10-22/paid-execution-plan-126-postchange-correction-research.md |
| Changes-record role | .copilot-tracking/changes/2026-10-22/paid-execution-plan-126-postchange-correction-changes.md |
| Planning execution and readiness | complete; ready |

## Sources

* .copilot-tracking/research/2026-10-22/paid-execution-plan-126-postchange-correction-research.md: evidence.
* docs/case_study_48_addendum.md, docs/reference/README.md, docs/reference/log.md: targets.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct wording

* Intent: pre-change labelling and refresh gate everywhere.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Edit addendum subsection

* Requirement and evidence: research C1, W1 to W3.
* Expected result: no contradictory current claim.
* Detail section: P01-T01 in .copilot-tracking/details/2026-10-22/paid-execution-plan-126-postchange-correction-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Edit index row; append log entry

* Requirement and evidence: research C2.
* Expected result: consistent wording; earlier log entries untouched.
* Detail section: P01-T02 in .copilot-tracking/details/2026-10-22/paid-execution-plan-126-postchange-correction-phase-details.md

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate and publish

* Intent: new receipt, push, PR refresh.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Gate, verify, push

* Requirement and evidence: repository local gate.
* Expected result: new external receipt verified; PR refreshed.
* Detail section: P02-T01 in .copilot-tracking/details/2026-10-22/paid-execution-plan-126-postchange-correction-phase-details.md

## Dependencies

* origin/main 9e55a392b95c90730c6410b9a4db4ad3a5ae70ce at start; branch head a4df6a04.

## Critique Disposition

One critique executed by a worker, verdict Revise: 3 High, 3 Medium, 1 Low, all planner-direct, no user decision. No second critique. All applied in P01 and P02 below:

* PC-001: rewrite the "retirement not authorized" sentence to say that this proposal authorizes no retirement, and that a separate owner-authorized cutover-test deletion was later completed (reported by the coordinator, verified by read-only inventory); no repository record of the authorization is cited.
* PC-002: enumerate and relabel every stale "current", "no change", "S0", 94-resource and Front Door statement; add a dated note to the history S1 row.
* PC-003: state that the first complete post-change day is 23 Oct, so a tranche before 2026-10-25T16:02Z is unlikely, and that the refresh gate is never waived.
* PC-004: add a dated qualifier to the demo API behaviour statement and T1 definition; bounds unchanged.
* PC-005: the new log entry and index row explicitly supersede the earlier 2026-10-22 wording; the old entry is not edited.
* PC-006: describe 535.33 as "pre-change, credits no unmeasured saving, not an upper bound" rather than "conservative".
* PC-007: P02 validation names the identifier search and arithmetic recomputation.

## Follow-Up Items

* After at least one complete post-change day of cost data: measure the run rate, refresh the forecast and inventory, recompute E and admissible U.
* Bound U; verify the Blob role.
