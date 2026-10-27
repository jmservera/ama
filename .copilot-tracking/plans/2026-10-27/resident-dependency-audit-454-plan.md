---
title: Resident dependency graph audit plan
description: One complete documentary correction cycle for PR 454
ms.date: 2026-10-27
---

## Task Metadata

* Task ID: jmservera/ama#454:dependency-audit-2026-10-27
* Task slug: resident-dependency-audit-454
* Planning status: Ready; original critique Revise, PC-001 resolved directly
* Phase details: .copilot-tracking/details/2026-10-27/resident-dependency-audit-454-phase-details.md

## Executive Summary

Correct the complete RB dependency graph from the PRD story matrix, not
just the four comment locations. Distinguish engineering dependencies,
internal multi-story acceptance order and cumulative release evidence.
Retain M1's partial-R2 boundary, conditional protocol freeze, routine OFF
and independent urgent help. Run one critique and one final Review.

### What You May Not Know

RB-13 contains S09/S10 and RB-14 contains S11/S12: their internal ordering
must be explicit without adding self-cycles. R3 evidence includes the
portal-only baseline and completed earlier-stage evidence, not just RB-15.
Existing quality FAIL and acceptance blockers remain unchanged.

## User Decisions and Requirements

* Complete the full RPI loop with dated artifacts on the existing PR 454 branch.
* Audit S01-S16 and R1-R3 against every RB row; split grouped rows where needed.
* Correct RB-09, RB-12, RB-14, RB-16 and RB-17 plus M1 critical-path prose.
* Re-read the final graph once against the stories; this is the last
  correction cycle. Report later findings instead of another correction loop.
* Pull with rebase first, push without force, reply to and resolve four
  threads with evidence; do not merge. No uv or secrets.
* Documentation-only Markdown/link review and git diff. The task-specific
  validation boundary supersedes the general full-local-gate instruction
  for this correction; do not claim that broader gate ran or passed.

## Goals

Every story prerequisite has a documented RB path or an explicit internal
ordering, and release advancement requires its named evidence.

## Scope and Non-Goals

Canonical edit target:
.copilot-tracking/changes/2026-10-25/resident-prd-backlog-readiness-441-draft-backlog.md.
Also reconcile the active R3/R4 table in
.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441/resident-service-unregistered-proposal.md
if needed. No PRD/BRD requirement change, runtime work, quality reassessment,
historical outcome rewriting, issue creation, activation or merge.

## Functional Requirements

* Separate RB-08/RB-09 and RB-11/RB-12 dependency rows.
* RB-09 requires RB-08/RB-05; RB-12 requires RB-11/RB-05/RB-09.
* Separate RB-13 through RB-16. RB-14 requires RB-05/RB-08/RB-11/RB-13;
  RB-15 requires RB-14 (retain RB-05/RB-08); RB-16 additionally requires RB-15.
* Explicitly order S10 after S09 in RB-13 and S12 after S11 in RB-14.
* RB-17 requires RB-13 through RB-16, completed R3 evidence and task release;
  OD-53 is not a prerequisite. RB-18 through RB-20 retain existing edges.
* Document cumulative R1/R2/R3 evidence, including R3 baseline frozen under
  RB-01. Use it for RB-17 and R5 review; do not make full R2 a prerequisite
  to M1. Add explicit RB-01 root and staged RB-23 script dependencies.
* Correct M1 to branch after RB-05 into RB-06, RB-07 and RB-08 then RB-09,
  alongside R0 measurement design and M1 accessibility scripts before RB-10.

## Non-Functional Requirements

Maintain a readable, acyclic, fully specified documentary graph. Preserve
all existing approvals, Not-run evidence and model-independent help.

## Acceptance Criteria

* All S01-S20 rows mapped, with S01-S16 and R1-R3 exhaustively compared.
* Each RB-01 to RB-24 and governance item has explicit prerequisite or root
  treatment; no grouping implies a missing dependency.
* Markdown tables and local links reviewed; `git diff --check` passes.
* One final graph reread and one independent post-implementation Review
  retained; any residual findings reported, not silently fixed in a loop.
* Normal push and evidence-backed replies/resolutions; PR remains open.

## Sources

Research C1-C5 and full mapping:
.copilot-tracking/research/2026-10-27/resident-dependency-audit-454-research.md.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and verify the whole graph

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Apply graph, gate and narrative corrections

Use the research matrix and requirements above. Preserve unrelated content.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Re-read once and review Markdown, links and diff

Compare every source story and R1-R3 gate with the final graph. Retain
exact file hashes and results in the changes record.

<!-- rpi:phase id=P02 -->
### [ ] P02: Independent Review and publication

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run one independent Review

Review final source and original RPI evidence; report residual findings.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Publish and address threads

Configure authenticated privacy-safe author/committer, commit with supplied
trailer, pull/rebase for bot updates, push normally, then reply/resolve only
the four addressed threads. Do not merge. Hosted/human approval is separate.
Compare assessed PRD/backlog/proposal hashes after synchronization and
immediately before push. If any differs, STOP publication and thread
resolution, report the changed paths and invalidated assessment, and do
not start another correction, reread or Review. Bot-only updates with
byte-identical assessed sources may proceed.

## Dependencies and Locked Validation Ownership

P01-T02 depends on P01-T01; P02-T01 on P01-T02; P02-T02 on Review results.
Parent owns Markdown/link and diff checks. No executable tests, test removals,
test additions, generated targets or new tooling. Maximum source targets:
two Markdown files; original RPI artifacts are separate evidence. Semantic
coverage is the full story mapping; regression coverage preserves routine
OFF, no OD-53 for RB-17/18, independent help, M1 scope and existing failures.

## Critique Disposition

One final-candidate independent critique executed: original verdict Revise,
one Medium PC-001. Planning parent resolved it directly by adding the
fail-closed pre-push source-identity condition to P02-T02 in this plan and
phase details. No user decision needed and no repeat critique. Original
critique retained at
.copilot-tracking/reviews/plans/2026-10-27/resident-dependency-audit-454-plan-critique.md.

## Follow-Up Items

* Existing requirements-quality dispositions, engineering sizing and
  architecture registration remain separately owned work, not this cycle.

## Handoff

P01 complete after direct PC-001 disposition and one final graph reread.
Changes evidence:
.copilot-tracking/changes/2026-10-27/resident-dependency-audit-454-changes.md.
P02-T01 independent Review Complete / Conformant with justified divergence,
no findings. Original Review retained at
.copilot-tracking/reviews/logs/2026-10-27/resident-dependency-audit-454-review.md.
P02-T02 publication remains pending with assessed sources frozen.
