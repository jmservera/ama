<!-- markdownlint-disable-file -->
# RPI Plan: Paid execution plan #126, revised USD 700 demo budget with private Blob options

## Task Metadata

* Task ID: 126-demo-budget-700
* Task slug: paid-execution-plan-126-demo-budget-700
* Planning status: ready
* Plan date: 2026-10-22
* Phase details: .copilot-tracking/details/2026-10-22/paid-execution-plan-126-demo-budget-700-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-22/paid-execution-plan-126-demo-budget-700-plan-critique.md

## Executive Summary

Revise the existing costed Azure demo execution-plan subsection so the owner's 2026-10-22 decision (USD 700 replacement all-in October forecast ceiling) is current, the USD 500 wording survives only as dated history, and the smallest finite private-Blob demo options are offered for separate approval. Fresh read-only evidence shows resource group `ama` at 242.36 observed and 535.33 forecast with no change, which leaves at most 89.67 for outside-group spend U plus approved ceilings plus reserve. Subscription scope is still unreadable, so U stays unknown and every paid tranche stays blocked. Documentation only; nothing is executed or approved.

### User Decisions and Requirements Highlights

* USD 700 is the replacement all-in forecast ceiling, not 700 additional: the envelope must include U, tranche ceilings and reserve.
* Expiry 2026-10-25T16:02Z stays; no extension.

### What You May Not Know

* The spend step from about 15 to about 30 per day on 17 October dominates the forecast; headroom exists only if the run rate holds.
* The Blob route depends on an existing managed-identity role assignment that this loop cannot verify further or grant.

### Unresolved Decisions or Blockers

* Subscription-scope cost read access (precise blocker: Cost Management read above resource-group scope, `RBACAccessDenied`).
* Owner approval of any option; role assignment; private-link data and retention meters; human, legal and privacy gates.

## User Decisions and Requirements

* "spend approved", then "limit to $700 forecast": USD 700 is the replacement all-in October forecast ceiling, not additional spend. Prior expiry kept. Unknown costs are not assumed zero.
* Preferred demo route is private Blob with managed identity; no resource tags carrying results; private backing services remain private.
* No Front Door or resource retirement, resource-group deletion, identity loss, access or role-assignment change is authorized.
* Screen-reader acceptance and independent signed source/image attestation may be documented as unverified production follow-ups, not passed. No real personal data or human pilot capture.
* Proposal-only integration through normal fresh validation, independent review and merge gates; issue #126 criteria stay open; no closing keywords.
* Paid execution is not part of this task.

## Goals

* Make USD 700 the current ceiling in the addendum subsection, index row and log, with USD 500 and earlier figures preserved as dated history.
* Record current aggregate observed and forecast evidence, with scope, source, timestamp and currency, and reconciliation with the 2026-10-20 read.
* Offer the smallest finite private-Blob options with finite incremental ceilings, thresholds and stop rules.

## Scope and Non-Goals

### In Scope

* Edit the existing subsection in docs/case_study_48_addendum.md, its index row in docs/reference/README.md and append to docs/reference/log.md.
* Commit dated research, plan, details, critique, changes and review artifacts.

### Non-Goals

* Any Azure change, job, deployment, retirement or permission change; any approval; issue acceptance.

## Functional Requirements

* The subsection states the current ceiling, observed versus forecast, U, envelope, thresholds and options.
  * Observable acceptance criteria: a reader can compute E and each maximum admissible U from numbers in the text.
* Old figures appear only under a dated history label.
  * Observable acceptance criteria: no unqualified "500" total remains as a current rule.

## Non-Functional Requirements

* Evidence is aggregate and non-sensitive.
  * Objective threshold or evaluation condition: no subscription, tenant, user identifier, account name or raw record appears in committed files.
  * Observable acceptance criteria: a search of the diff for identifiers finds none.
* Markdown follows repository style (ASCII, no em dashes, asterisk lists).
  * Observable acceptance criteria: the full tools/rpi-checks.py gate passes or its gaps are recorded.

## Acceptance Criteria

* Addendum, index and log updated; history preserved; all approvals and acceptances stay open.
* Local gate run with receipt; independent-review readiness stated, not claimed as review.

## Implementation Context Record

| Context item | Current artifact or record |
|--------------|----------------------------|
| Plan | .copilot-tracking/plans/2026-10-22/paid-execution-plan-126-demo-budget-700-plan.md |
| Phase details | .copilot-tracking/details/2026-10-22/paid-execution-plan-126-demo-budget-700-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-10-22/paid-execution-plan-126-demo-budget-700-plan-critique.md |
| Relevant research | .copilot-tracking/research/2026-10-22/paid-execution-plan-126-demo-budget-700-research.md |
| Changes-record role | .copilot-tracking/changes/2026-10-22/paid-execution-plan-126-demo-budget-700-changes.md |
| Planning execution and readiness | complete; ready for documentation-only implementation |
| Continuation context | active RPI Agent parent continues |

## Sources

* .copilot-tracking/research/2026-10-22/paid-execution-plan-126-demo-budget-700-research.md: evidence and arithmetic.
* docs/case_study_48_addendum.md, docs/reference/README.md, docs/reference/log.md: edit targets.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Revise costed plan synthesis

* Intent: current ceiling, evidence, options and gates in the addendum, index and log.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Update addendum subsection

* Requirement and evidence: owner decisions; research W1 to W4.
* Expected result: revised subsection with dated history.
* Detail section: P01-T01 in .copilot-tracking/details/2026-10-22/paid-execution-plan-126-demo-budget-700-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Update index row and append log entry

* Requirement and evidence: knowledge-base conventions; append-only log.
* Expected result: index row mentions the revised ceiling; one new dated log entry.
* Detail section: P01-T02 in .copilot-tracking/details/2026-10-22/paid-execution-plan-126-demo-budget-700-phase-details.md

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate and publish

* Intent: full local gate, receipt, push, PR update.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Run gate and update PR

* Requirement and evidence: repository instructions (local RPI gate).
* Expected result: external receipt verified; PR #422 body updated; draft kept; issue open.
* Detail section: P02-T01 in .copilot-tracking/details/2026-10-22/paid-execution-plan-126-demo-budget-700-phase-details.md

## Dependencies

* Current origin/main: 9e55a392b95c90730c6410b9a4db4ad3a5ae70ce; branch already contains it.

## Critique Disposition

One critique executed by a worker, verdict Revise: 1 High, 4 Medium, 2 Low, all planner-direct, no user decision needed. No second critique. Dispositions (applied in P01-T01 and P02-T01):

* PC-001 accepted: each option states that T1 and B1 stay blocked until their separate approvals and prerequisites exist (tenant, role and ingress changes; Blob role); this document authorizes none.
* PC-002 accepted: state E includes R and that 560/630/665 apply to the live projection L; derive 655 as 665 less a 10 margin that keeps L at most 625 below the pause line.
* PC-003 accepted: B1 gets bounds (1 GB, 100,000 writes, 1,000,000 other operations, one container, no tags), retention treatment, cleanup of its own container only, and the role gate.
* PC-004 accepted: S0 is the only current baseline; S1 and S2 are history and not authorized.
* PC-005 accepted: sweep for stale 500, 475, 450, 400 and 535.41; add a run-rate sensitivity note.
* PC-006 accepted: identifier search patterns defined (GUID, email, subscription path, tenant domain) over the diff.
* PC-007 accepted: P02 starts with a base fetch, commits in order and recomputes the figures before the gate.

## Follow-Up Items

* Owner or tenant operator: grant Cost Management read at a scope covering U, or supply a bounded U with scope, source, timestamp and currency.
* Verify the managed-identity Blob data role exists (no change authorized here).
* Production follow-ups: screen-reader acceptance; independent signed source/image attestation.
