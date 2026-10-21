<!-- markdownlint-disable-file -->
# RPI Plan: Cut-over soak evidence preparation for #201

## Task Metadata

* Task ID: 201-soak-review
* Task slug: cutover-soak-review-201
* Planning status: ready (critique PC-001 to PC-009 applied; verdict Revise resolved, no second critique)
* Plan date: 2026-10-21
* Phase details: .copilot-tracking/details/2026-10-21/cutover-soak-review-201-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-21/cutover-soak-review-201-plan-critique.md

## Executive Summary

This plan reconciles the existing cut-over evidence pack with today's repository and GitHub state, maps all 11 original #201 acceptance criteria to dated evidence and gaps, and proposes (not runs) a soak evidence specification and the exact owner decisions still pending. It edits the existing pack, ADR 0006 note, index row and log only. Nothing is signed off, ticked, tagged, deleted or deployed, and no Azure, private data or issue/PR write is involved.

### User Decisions and Requirements Highlights

* Preparation only (owner, 2026-10-20): proposal for review, not a completed soak or sign-off.
* Minimum soak duration stays OPEN; no number is invented.
* Missing, stale or unverified evidence stays UNMET.

### What You May Not Know

* The owner decided "no minimum soak" on 2026-10-15, yet the issue body still lists it as open and the owner asked on 2026-10-20 for a proposal. The plan flags the contradiction as decision D1 instead of resolving it.
* The pack's "no valid post-migration rubric comparison" is stale: snapshots now show 47 then 48, though candidate-commit scoring is still missing.
* CI runs on pull requests only, so candidate CI evidence cannot come from a push run.
* The USD500 total cap is already forecast to be exceeded and expires 2026-10-25T16:02Z, so no soak resources can start without a separately approved finite plan.

### Unresolved Decisions or Blockers

* D1 to D16 are pending with @jmservera and must not be recorded as decided (listed in P01-T03). Actual gate blocked by owner, tenant and budget, not by this preparation.

## User Decisions and Requirements

* Authorized preparation only: https://github.com/jmservera/ama/issues/126#issuecomment-6290697705 (propose soak duration and evidence checklist; no sign-off or legacy deletion).
* Map all 11 AC to source, date, revision, what is proven, gaps and human owners.
* Reconcile inside existing docs; no competing gate or unrelated new document.
* Preserve dependency on all other restructure children except deletion verification.
* Soak specification covers revision/environment, start/window, health/parity/CI/rubric, failure/reset/escalation, collector/reviewer.
* No Azure or paid calls, tenant writes, private data, backup attestation, tag, deletion; never delete `ama`; no budget headroom inferred.
* Do not touch other workers' files; shared index/log append-only; no copied tracking; no extra dependency pins.
* Focused local checks only; local author via GitHub privacy email; no amend, push, PR or merge.

## Goals

* A reviewable, evidence-linked AC map and soak proposal in the existing pack.
* Exact pending owner decisions with owner and smallest evidence.

## Scope and Non-Goals

### In Scope

* `docs/architecture/cutover-evidence-pack.md` new dated section and one unchecked checklist item.
* `docs/adrs/0006-src-layout-and-cutover.md` dated reconciliation note.
* `docs/reference/README.md` row for #200/#201, `docs/reference/log.md` append.
* Tracking artifacts and one local commit.

### Non-Goals

* Choosing a soak duration, checking AC boxes, owner sign-off, tag, release, deletion, backups, Azure or budget changes, workflow renames, edits to other workers' files, frontmatter `ms.date` of the pack (open PR #423 edits lines 1-7).

## Functional Requirements

* AC table lists 11 rows with source, date, revision, evidenced component, unmet component, status, owner.
  * Observable acceptance criteria: each row names a file or URL and a date; every row is overall UNMET (closed vocabulary) with its unmet component named.
* Soak specification table has revision/environment, start/window, signals, failure/reset/escalation, collector/reviewer, each labelled proposal with OPEN parameters.
  * Observable acceptance criteria: no numeric duration, cadence or tolerance appears except as `OPEN (owner)`.
* Pending decision list D1 to D16 with owner.
  * Observable acceptance criteria: every decision names an owner and the evidence needed.

## Non-Functional Requirements

* Markdown follows the existing file style, ASCII, no em dashes, relative links valid.
  * Objective threshold: focused link check reports zero broken links in changed files; `git diff --check` clean.
* Append-only index/log behaviour.
  * Objective threshold: diff of `docs/reference/log.md` is additions only.

## Acceptance Criteria

* All edits confined to the in-scope files plus tracking; no forbidden path in `git diff --name-only`.
* Checklist boxes remain unchecked; no sign-off wording implies approval.
* Final committed tree is clean including ignored and untracked files.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                            |
|----------------------------------|-------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-10-21/cutover-soak-review-201-plan.md                                    |
| Phase details                    | .copilot-tracking/details/2026-10-21/cutover-soak-review-201-phase-details.md                         |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-10-21/cutover-soak-review-201-plan-critique.md (Revise, all findings applied) |
| Relevant research                | .copilot-tracking/research/2026-10-21/cutover-soak-review-201-research.md                            |
| Changes-record role              | .copilot-tracking/changes/2026-10-21/cutover-soak-review-201-changes.md created by implementation    |
| Planning execution and readiness | candidate ready for the single critique                                                               |
| Continuation context             | confirmed automatic RPI Agent                                                                         |

## Sources

* .copilot-tracking/research/2026-10-21/cutover-soak-review-201-research.md: C1 to C19, W1 to W7, AC map.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Reconcile the evidence pack

* Intent: add the dated AC map, stale-statement reconciliation, soak proposal and pending decisions to the existing pack.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: AC map and reconciliation

* Requirement and evidence: AC table and contradictions (research AC table, C1 to C19).
* Expected result: 11-row table plus dated corrections for rubric, soak, open PRs, CI trigger.
* Detail section: P01-T01 in .copilot-tracking/details/2026-10-21/cutover-soak-review-201-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Soak evidence specification proposal

* Requirement and evidence: owner direction W3; no invented duration.
* Expected result: specification table with OPEN parameters.
* Detail section: P01-T02 in .copilot-tracking/details/2026-10-21/cutover-soak-review-201-phase-details.md

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Pending owner decisions and checklist pointer

* Requirement and evidence: owner decisions D1 to D16; unchecked checklist item.
* Expected result: decision table and one unchecked checklist item.
* Detail section: P01-T03 in .copilot-tracking/details/2026-10-21/cutover-soak-review-201-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Align ADR, index and log

* Intent: flag the soak contradiction at the ADR and update navigation append-only.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: ADR note, index row and log entry

* Requirement and evidence: C10, C16, C17.
* Expected result: dated ADR note, updated row, appended log entry.
* Detail section: P02-T01 in .copilot-tracking/details/2026-10-21/cutover-soak-review-201-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused validation and local commit

* Intent: verify links, whitespace, scope and cleanliness; commit locally.
* Dependencies: P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Checks, changes record and commit

* Requirement and evidence: repository gate rules; coordinator owns the full gate.
* Expected result: focused checks recorded, unperformed checks documented, local commit with trailer, clean tree.
* Detail section: P03-T01 in .copilot-tracking/details/2026-10-21/cutover-soak-review-201-phase-details.md

## Dependencies

* Research artifact: supplies the evidence.
* Open PR #423 overlaps the pack: edit only a distinct section and avoid the frontmatter.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| PC-001 AC1/AC2 MET labels | resolved | Closed vocabulary: all rows overall UNMET; evidenced and unmet components split (P01-T01) |
| PC-002 PARTIAL hides unmet part | resolved | Unmet component column names it per row (P01-T01) |
| PC-003 stale text uncorrected | resolved | Additive superseded blockquote under Other Cut-Over Gates; history intact (P01-T01) |
| PC-004 unsourced rules | resolved | Rows labelled proposals; recovery baseline, workflow set and rubric comparator cited or OPEN (P01-T02) |
| PC-005 missing checklist decisions | resolved | D13 to D16 added plus crosswalk (P01-T03) |
| PC-006 log type | resolved | Type `query`; files and contradictions listed (P02-T01) |
| PC-007 overlap safeguards | resolved | Heading anchors, fetch and base SHA record, re-anchor rule (P03) |
| PC-008 commit/gate boundary | resolved | Two commits, paths listed, branch not publishable, receipt invalidation stated (P03-T01) |
| PC-009 overconfident readiness | resolved | Handoff states D1 to D16 pending, not decided; new owner comments reported (plan Handoff) |

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-10-21/cutover-soak-review-201-changes.md
* Ready phase or task: P01
* Remaining provisional question or blocker: D1 to D16 pending owner decisions (not blockers for preparation); a new owner comment on #201 is reported, not applied
