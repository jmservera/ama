<!-- markdownlint-disable-file -->
# RPI Plan: PR420 gate-evidence correction

## Task Metadata

* Task ID: 420-gate-evidence
* Task slug: coordinator-gate-evidence-420
* Planning status: ready
* Plan date: 2026-10-21
* Phase details: .copilot-tracking/details/2026-10-21/coordinator-gate-evidence-420-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-21/coordinator-gate-evidence-420-plan-critique.md

## Executive Summary

PR420 pins launched RPI sessions to Sonnet 5.5. Its original HVE mechanical validation report says application gates were "Not run (none exist or required)", which wrongly suggests the mandatory complete local RPI gate is waived. This plan corrects that wording truthfully: the gate was not run in the mechanical stage and stays separately mandatory on the final exact head before publication. The Pass verdict is scoped to mechanical validation. A new dated correction record preserves the original wording and today's evidence. No source file changes.

### User Decisions and Requirements Highlights

* Correct the false waiver implication only; preserve the original static-only and adverse history and never claim the gate ran earlier.
* The coordinator, not this worker, runs the full gate after the frozen candidate.

### What You May Not Know

* The correction is a new commit, so any earlier receipt would be invalid; none exists for this candidate, and the coordinator must run the complete gate on the final head.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements).

## User Decisions and Requirements

* Scope is the false evidence-waiver implication and coupled records only (brief /tmp/brief-420-gate-correction-2113.md).
* Preserve original HVE author/review/validation history; do not pretend the full gate ran previously.
* Launch clarification: run focused checks and HVE validation, commit all evidence, freeze a clean head, exit without running the full gate or waiting for the heavy lock. No push, PR, merge, paid or cloud work.
* Pinned to Sonnet 5.5; do not rebase or rewrite; fast-forward only genuine clean upstream commits (none exist).

## Goals

* Make the validation record truthful about gate status and verdict scope.
* Leave a dated, reviewable correction trail.

## Scope and Non-Goals

### In Scope

* `.copilot-tracking/hve-builder/2026-10-20/coordinator-sonnet-55-validation-01.md` line 29 and verdict scope.
* New correction record and RPI evidence for this task.

### Non-Goals

* Coordinator agent source change, authority or gate redesign, running the full gate, publication.

## Functional Requirements

* The line 29 row states the gate was not run in this stage and remains separately mandatory.
  * Observable acceptance criteria: no "none exist or required" text applies to the complete RPI gate.
* The verdict is scoped to mechanical validation.
  * Observable acceptance criteria: verdict line says it is not a gate pass or publication approval.
* A correction record quotes the original wording and records dated checks.

## Non-Functional Requirements

* Truthfulness: no statement that a check ran unless it did.
  * Objective threshold or evaluation condition: every executed check in the record has a command and result from this session.
  * Observable acceptance criteria: `git diff --check` clean; tracked source diff versus f3e8a8f1 excludes `.github/`.

## Acceptance Criteria

* Original wording is preserved in the correction record and Git history.
* Only tracking evidence changes versus f3e8a8f1.
* Clean committed head frozen; full gate explicitly not run, handed to the coordinator.

## Implementation Context Record

| Context item                     | Current artifact or record |
|----------------------------------|----------------------------|
| Plan                             | .copilot-tracking/plans/2026-10-21/coordinator-gate-evidence-420-plan.md |
| Phase details                    | .copilot-tracking/details/2026-10-21/coordinator-gate-evidence-420-phase-details.md |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-10-21/coordinator-gate-evidence-420-plan-critique.md |
| Relevant research                | .copilot-tracking/research/2026-10-21/coordinator-gate-evidence-420-research.md |
| Changes-record role              | .copilot-tracking/changes/2026-10-21/coordinator-gate-evidence-420-changes.md |
| Planning execution and readiness | complete; ready (critique Revise, all findings applied) |
| Continuation context             | parent RPI Agent continues to Implement |

## Sources

* Research artifact: evidence C1 to C9 and selected alternative A.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct evidence wording

* Intent: truthful validation record and correction trail.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Edit line 29 and verdict scope in validation-01

* Requirement and evidence: C1, C2, C9
* Expected result: truthful row and scoped verdict with correction pointer.
* Detail section: P01-T01 in .copilot-tracking/details/2026-10-21/coordinator-gate-evidence-420-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add dated validation-02 correction record

* Requirement and evidence: C3, C4, C5, C6
* Expected result: drafted with original quote, gate boundary and unchanged-source statement; the focused-check results are appended only after P02-T01 runs them, before the single commit.
* Detail section: P01-T02 in .copilot-tracking/details/2026-10-21/coordinator-gate-evidence-420-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Validate, review and freeze

* Intent: focused checks, one Review, commit and freeze.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run focused checks and HVE validation; one Review; commit evidence

* Requirement and evidence: launch clarification; C8
* Expected result: focused checks (git diff --check, tracked-source diff, grep confirming the gate appears only as not run and separately mandatory), fetch of origin/main with base SHA recorded, noreply email from gh api user set locally, one Conventional Commit with Copilot trailer, no amend, clean frozen head, no gate run.
* Detail section: P02-T01 in .copilot-tracking/details/2026-10-21/coordinator-gate-evidence-420-phase-details.md

## Dependencies

* P02 depends on P01: checks apply to the final wording.

## Critique Disposition

| PC-001 premature "checks run today" before checks | resolved | P01-T02 drafts first; results appended after P02-T01 checks; grep check added |
| PC-002 missing fetch/base SHA/commit identity/handoff | resolved | P02-T01 expected result extended; final handoff reports HEAD, base, evidence paths, gate not run |
| PC-003 no minimal-diff guardrail for validation-01 | resolved | P01-T01 limited to line 29, verdict line and one correction note; verified by diff |

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-10-21/coordinator-gate-evidence-420-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: none
