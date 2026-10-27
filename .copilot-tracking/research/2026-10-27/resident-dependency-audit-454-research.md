---
title: Resident dependency graph audit research
description: Complete story and release-gate dependency derivation for PR 454
ms.date: 2026-10-27
---

<!-- markdownlint-disable-file -->

## Research Brief

Audit every PR442-S01 to S16 dependency and R1 to R3 advancement gate
against every draft RB row, including adjacent S17 to S20 rows. Output mode:
audit preparing planning. Audience: PR 454 author and reviewer. Focused
posture, selected for the owner's bounded documentation correction request.
Evidence root: `.copilot-tracking/`. No application, uv, secrets, live action,
merge or repeated correction cycle. Only Markdown/link review and git diff.

## Extension Registry and Participation

Repository instructions and RPI phase contracts selected. Requirements
rewriting, web skills and specialist research delegation skipped: this is a
single tightly coupled documentary graph trace, not a new product decision.
Owner explicitly requests the full loop and publication on the existing
branch. Existing automatic parent state supports continuation; no new
manual-to-automatic switch is inferred. No clarification is necessary.

## Questions and Prior Knowledge

Q1: Does every story edge have an explicit or transitive RB path?
Q2: Do release evidence gates and conditional authority remain distinct?
Q3: Do all RB rows and M1 prose agree with that graph?
Prior single-finding corrections are historical evidence, not proof of
whole-graph correctness. Initial clean worktree, correct branch, OPEN PR
targeting main, and `git pull --rebase` (already up to date) verified.

## Research Cycle 1

### Wider

Read the complete backlog, all twenty story dependencies and release stages.
Four unresolved Copilot threads identify six missing story edges plus an
incomplete R3 prerequisite. The graph also omits explicit root/accessibility
rows and hides ordering inside the two multi-story slices.
Reflection: audit the complete mapping, not just the four comment locations.

### Deeper

Derived mapping below from C1. A slash in a source dependency means AND, not
an alternative. Internal edges in a bundled slice require explicit acceptance
ordering, not a self-referencing RB edge.

| Story | Backlog mapping | Required story/fixture prerequisite | Initial graph disposition |
| --- | --- | --- | --- |
| S01 | RB-04 | Synthetic identity configuration | RB-02 supplies it |
| S02 | RB-05 | S01; grant-owner fixture | RB-04/RB-02 present |
| S03 | RB-07 | S01/S02 | RB-05 reaches RB-04 |
| S04 | RB-06 | S02 | Present |
| S05 | RB-08 | S02; published projection fixture | RB-05 reaches RB-02 |
| S06 | RB-09 | S05; publication authority fixture | Missing RB-08; retain RB-05 |
| S07 | RB-11 | S02; safe file configuration | RB-05/RB-09 present; specify configuration |
| S08 | RB-12 | S07 | Missing RB-11; retain RB-05/RB-09 |
| S09 | RB-13 | S02; offered-slot fixture | RB-05 reaches RB-02 |
| S10 | RB-13 | S09 | Internal ordering must be explicit |
| S11 | RB-14 | S05/S07/S09; common event contract | Missing RB-11/RB-13; retain RB-08/RB-05 |
| S12 | RB-14 | S02/S11 | Internal ordering must be explicit |
| S13 | RB-15 | S11/S12 | RB-14 supplies both; retain RB-05/RB-08 |
| S14 | RB-16 | S12/S13 | Missing RB-15; retain RB-14/RB-05/RB-08 |
| S15 | RB-17 | Completed R3; independent task registration/evaluation/release | Require RB-13 to RB-16 and R3 evidence, not only RB-15 |
| S16 | RB-18 | S13/S15; independent urgent/help route | RB-15/RB-17 present; retain model-independent help |
| S17 | RB-19 | S15/S16; OD-53 before positive activation only | Present; preserve |
| S18 | RB-20 | S17 | Present; preserve |
| S19 | RB-21 | R3 comparator; conditional R4 evidence | Preserve, clarify R3 evidence |
| S20 | RB-22 | R1 to R3; conditional R4; NFR checks | Preserve, clarify stage evidence |

Reflection: no renumbering or split of story ownership is needed. Split
dependency-table groups, and explicitly order acceptance inside RB-13/RB-14.

### Contrarian

Tested whether RB-05 or existing RB-15 transitively supplies the missing
paths: it does not. Tested whether organisational R3 grouping implies
completed R3 evidence: hierarchy expressly is not a dependency (C2).
Tested whether OD-53 is needed for S15/S16: source says independent task
release, whereas OD-53 governs later positive dispatch (C1). Tested whether
all R2 work must precede M1: M1 explicitly excludes uploads (C3); do not
introduce an RB-10 -> R2 gate. Accessibility is staged so RB-10 can use M1
scripts without waiting for R5 or creating a cycle.
Reflection: add explicit release-evidence nodes separately from engineering
slice ordering; R3 evidence requires R2 evidence, which requires R1 evidence.
This preserves partial-R2 M1 and independent urgent/help service.

## Evidence Log

| ID | Finding | Workspace-relative location |
| --- | --- | --- |
| C1 | Authoritative S01 to S20 dependencies | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1110-1131` |
| C2 | Slice ownership, current edges and M1 prose | `.copilot-tracking/changes/2026-10-25/resident-prd-backlog-readiness-441-draft-backlog.md:55-146` |
| C3 | M1 excludes uploads; R1/R2/R3 evidence before advancement | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1270-1306` |
| C4 | Four unresolved threads | PR 454 discussions r4390547328, r4390547408, r4390547471, r4390646631; retrieved 2026-10-27 using GraphQL |
| C5 | Active architecture R3/R4 reconciliation | `.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/resident-service-unregistered-proposal.md:703-709` |

## Findings, Alternatives and Decisions

Accepted: explicit per-item graph plus R1/R2/R3 evidence prerequisites (C1-C3).
Rejected: grouped-row shorthand or hierarchy as implicit edges; both obscure
missing ordering. Rejected: OD-53 on RB-17/18; it changes task authority.
Deferred: requirements-quality FAIL, sizing and registration; no approval
or acceptance is supplied by this graph correction.

## Planning Readiness and Self-check

Research disposition: executed. Planning Readiness: Ready.
All questions answered by C1-C5. One complete wider/deeper/contrarian cycle
executed inline; further discovery is redundant for this bounded graph.
No external legal/platform research needed. Preserve original adverse review
outcomes. Plan one independent critique and one post-implementation Review;
after the single final graph reread, report residual findings rather than
starting another correction cycle.
