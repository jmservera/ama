<!-- markdownlint-disable-file -->
# RPI Plan: Non-operative custody preparation correction (#122)

## Task Metadata

* Task ID: continuity-custody-preparation-122-recovery
* Task slug: continuity-custody-preparation-122-recovery
* Planning status: ready
* Plan date: 2026-10-21
* Phase details: .copilot-tracking/details/2026-10-21/continuity-custody-preparation-122-recovery-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-21/continuity-custody-preparation-122-recovery-plan-critique.md

## Executive Summary

The earlier candidate c9f65c48 added a non-operative custody, witness and stop protocol to the issue #122 section of `src/core/README.md`. It was written without running the RPI skills, so this task re-runs the loop for real. Research found that the text is mostly sound but implies role assignments no source makes (drill authoriser, head custodian, competent reviewer) and describes `verify_export` slightly too broadly.

This plan corrects only those two points in the same README subsection, keeps every #122 criterion open and every authority UNASSIGNED or UNAPPROVED, and records the history of the direct-authored attempt honestly.

### User Decisions and Requirements Highlights

* Preparation only: no drill, authority, witness, Azure configuration, push or heavy gate. Consequence: the change is text-only and adds no executable path.
* Preserve the adverse direct-authored history. Consequence: earlier files stay unchanged and are never cited as phase evidence.

### What You May Not Know

* Source documents name who must answer OQ-017 and who owns OD-35 override and restart evidence, not who holds authority, authorises a drill or witnesses one.
* The coordinator still has to run the full exact-head gate and an independent assessment before any push.

### Unresolved Decisions or Blockers

* Actual restart authority holders, drill authoriser, witness and head custodian remain owner decisions (OQ-017, OD-35). Not blockers for this documentation task.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements).

## User Decisions and Requirements

* Run real skill phases in order: rpi-research, rpi-plan with an actual critique, rpi-implement, rpi-review (recovery brief).
* Preserve the c9f65c48 candidate and its direct-authored tracking as adverse history; do not backfill phases; correct the model evidence to claude-sonnet-5.5 from observed session metadata.
* Scope is the core README non-operative protocol and relevant issue #122 tracking only; no other active issue files (agents README, cutover pack, KB index/log, CSS, mapdocs).
* All original #122 criteria stay open; no actual authority, witness, drill or Azure work; no runtime code or tests for documentation constants.
* No push, PR or heavy gate; commit truthful correction artifacts, freeze clean, return head/base and actual invocations.

## Goals

* Make the README subsection state only what sources support, with unassigned roles shown as UNASSIGNED.
* Make the record of how this candidate was produced truthful.

## Scope and Non-Goals

### In Scope

* Edit the "Non-operative custody, recovery and witness preparation" subsection in `src/core/README.md`.
* Tracking artifacts for this task and a correction record.

### Non-Goals

* Runtime code, tests, other READMEs, KB index/log, cutover pack, issue criteria, remote writes.

## Functional Requirements

* The decision-rights table shows a source-backed owner only where OQ-017 or OD-35 names one, and UNASSIGNED otherwise.
  * Observable acceptance criteria: no row implies a person, delegation or approval; each row that cites a source cites OQ-017 or OD-35 correctly.
* The verification text describes `verify_export` as checking digest, ledger chain, recorded head, optional external head and completeness, and treats sealed-year `--by-year` checks as a separate step.
  * Observable acceptance criteria: wording matches continuity.py `verify_export` and the #114 README section.
* The witness requirement and the drill sequence are labelled proposed expectations, not existing controls.
  * Observable acceptance criteria: text says no source defines a witness role.

## Non-Functional Requirements

* Plain ASCII punctuation, existing heading and table style.
  * Objective threshold or evaluation condition: added lines contain no non-ASCII characters.
  * Observable acceptance criteria: anchors from the subsection to #221 and #114 resolve.

## Acceptance Criteria

* `git diff` against base touches only `src/core/README.md` and `.copilot-tracking/` files.
* Every #122 and #221 criterion remains unticked and every actual authority UNASSIGNED/UNAPPROVED.
* The tracking record states that c9f65c48 was directly authored and not a skill run.

## Implementation Context Record

| Context item                     | Current artifact or record |
|----------------------------------|----------------------------|
| Plan                             | .copilot-tracking/plans/2026-10-21/continuity-custody-preparation-122-recovery-plan.md |
| Phase details                    | .copilot-tracking/details/2026-10-21/continuity-custody-preparation-122-recovery-phase-details.md |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-10-21/continuity-custody-preparation-122-recovery-plan-critique.md with disposition recorded below |
| Relevant research                | .copilot-tracking/research/2026-10-21/continuity-custody-preparation-122-recovery-research.md |
| Changes-record role              | .copilot-tracking/changes/2026-10-21/continuity-custody-preparation-122-recovery-changes.md is created by implementation |
| Planning execution and readiness | executed; ready |
| Continuation context             | confirmed automatic RPI Agent loop requested by the user brief |

## Sources

* .copilot-tracking/research/2026-10-21/continuity-custody-preparation-122-recovery-research.md: findings F1 to F5, C1 to C10, W1, W2.
* src/core/README.md: subsection at the #122 section.
* Caller briefs as supplied, summarised in User Decisions and Requirements; they are non-durable context, not repository evidence.
* src/core/src/zava_forward/core/continuity.py: `verify_export` and the free-text `incident_owner` field on a suspension record.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct the README subsection

* Intent: remove unsupported role implications and over-broad verification wording.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Rework the decision-rights table

* Requirement and evidence: F5; C7, C8, C9.
* Expected result: owners UNASSIGNED except citations of OQ-017 question owners and OD-35 Building Safety and Sponsor as the owners of override/restart evidence; drill authoriser and head custodian explicitly UNASSIGNED.
* Detail section: P01-T01 in .copilot-tracking/details/2026-10-21/continuity-custody-preparation-122-recovery-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Fix verification wording and label proposals

* Requirement and evidence: F2, F5; C2, C5.
* Expected result: accurate verify_export description; witness rule and sequence marked proposed.
* Detail section: P01-T02 in .copilot-tracking/details/2026-10-21/continuity-custody-preparation-122-recovery-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and record

* Intent: show the scope held and record the history honestly.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Local checks

* Requirement and evidence: acceptance criteria.
* Expected result: anchors resolve, ASCII, diff scope, git status.
* Detail section: P02-T01 in .copilot-tracking/details/2026-10-21/continuity-custody-preparation-122-recovery-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Correction record

* Requirement and evidence: recovery brief.
* Expected result: changes record states that c9f65c48 was direct-authored, cites session metadata, and does not treat prior files as phase evidence.
* Detail section: P02-T02 in .copilot-tracking/details/2026-10-21/continuity-custody-preparation-122-recovery-phase-details.md

<!-- rpi:task id=P02-T03 -->
#### [x] P02-T03: Commit and freeze

* Requirement and evidence: user decisions (commit, freeze clean, return head/base and invocations); repository branch and commit rules.
* Expected result: repo-local noreply identity set, one Conventional Commit with the Co-authored-by trailer, empty `git status --short --ignored`, head and base SHAs and actual skill invocations recorded; gate and push left to the coordinator.
* Detail section: P02-T03 in .copilot-tracking/details/2026-10-21/continuity-custody-preparation-122-recovery-phase-details.md

## Dependencies

* Locked before critique: test ownership none (docs only, no tests added or removed); exact removals: the unsupported role rows and over-broad verify wording in the README subsection; maximum additions: about 15 README lines net versus pre-edit HEAD c9f65c48; canonical target src/core/README.md, no generated targets; semantic coverage via source comparison, regression coverage via anchor/ASCII/diff scope checks; validation evidence is the changes record.
* Research artifact: supplies findings.
* Base ca4baf75837de57c99718f7423716d5dc0b0e244 unchanged.

## Critique Disposition

One critique ran once (verdict Revise) via a fresh general-purpose worker that activated rpi-plan-critique. No second critique runs.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| PC-001 no commit/freeze task | resolved | P02-T03 added to plan and details |
| PC-002 row-by-row table | resolved | six-row target table in P01-T01 detail; OD-35 owners supply evidence, not authority |
| PC-003 other bullets unexamined | resolved | per-bullet disposition in P01-T02 detail; bullets marked proposed expectations; C10 qualifier |
| PC-004 validation unspecified | resolved | exact commands in P02-T01 detail; line cap measured against pre-edit HEAD |
| PC-005 history record content | resolved | required content listed in P02-T02 detail |
| PC-006 /tmp sources | resolved | Sources relabelled non-durable |
| Residual: critique did not re-verify continuity.py, OQ-017, OD-35, live issues | accepted with risk | implementer compares against sources in P01; independent review follows |

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-10-21/continuity-custody-preparation-122-recovery-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: none
