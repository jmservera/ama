---
title: Resident dependency graph audit changes
description: Whole-graph correction and original validation evidence for PR 454
ms.date: 2026-10-27
---

## Context and Scope

Task ID: jmservera/ama#454:dependency-audit-2026-10-27.
Plan and details: .copilot-tracking/plans/2026-10-27/resident-dependency-audit-454-plan.md
and .copilot-tracking/details/2026-10-27/resident-dependency-audit-454-phase-details.md.
Declared implementation scope: P01. P02 remains parent-owned Review/publication.
Original independent critique Revise retained; PC-001 resolved directly.

## P01-T01: Whole-graph Correction

Complete. Applied all research-matrix edges, internal acceptance order,
cumulative release evidence and M1 prose as one coherent batch in the draft
backlog. Added explicit fixture contracts, root/staged-accessibility rows
and governance inventory treatment. Reconciled the active proposal R3/R4
table without modifying historical assessment outcomes or the canonical
PRD/BRD. No new requirement or runtime authority.

## P01-T02: Final Comparison and Validation

Complete. One final source/story comparison performed after the complete
correction batch, with PRD S01-S20 and R0-R5 gates, final backlog slices,
dependency/gate tables and M1 prose, and active proposal reconciliation
read together. No residual story-edge mismatch found; no second source
correction or repeated final reread commissioned.

| Source dependency | Final path / evidence |
| --- | --- |
| S01 configuration | RB-04 -> RB-02 synthetic identity fixtures |
| S02 -> S01 and grant owner | RB-05 -> RB-04/RB-02 |
| S03 -> S01/S02 | RB-07 -> RB-05 -> RB-04 |
| S04 -> S02 | RB-06 -> RB-05 |
| S05 -> S02 and published projection | RB-08 -> RB-05 -> RB-02 |
| S06 -> S05 and publication authority | RB-09 -> RB-08/RB-05 -> RB-02 |
| S07 -> S02 and safe file configuration | RB-11 -> RB-05/RB-09; file configuration explicit before execution |
| S08 -> S07 | RB-12 -> RB-11; original grant/publication prerequisites retained |
| S09 -> S02 and offered slot | RB-13 -> RB-05/RB-02 |
| S10 -> S09 | Explicit within RB-13 acceptance order, no self-edge |
| S11 -> S05/S07/S09 and event contract | RB-14 -> RB-08/RB-11/RB-13/RB-01 |
| S12 -> S02/S11 | RB-14 -> RB-05; explicit S11-before-S12 internal acceptance order |
| S13 -> S11/S12 | RB-15 -> RB-14, which verifies both in order |
| S14 -> S12/S13 | RB-16 -> RB-14/RB-15 |
| S15 -> R3 and independent task gate | RB-17 -> RB-13 to RB-16 AND completed R3 evidence AND task registry/evaluation/release; no OD-53 |
| S16 -> S13/S15 | RB-18 -> RB-15/RB-17; urgent help independent of task/model/release |
| S17 -> S15/S16 | RB-19 -> RB-17/RB-18; OD-53 only for positive activation |
| S18 -> S17 | RB-20 -> RB-19; negative suspension still needs no OD-53 |
| S19 -> R3 comparator, conditional R4 | RB-21 -> completed R3 evidence; protocol authored in RB-01 before data; blocked R4 not successful evidence |
| S20 -> R1-R3, conditional R4, NFRs | RB-22 -> stage evidence, RB-21/RB-23/RB-24; Not-run entries cannot satisfy acceptance |

Every RB-01 to RB-24 row checked, including root, fixture, measurement,
milestone, accessibility and load rows; G0/RB-G1 through RB-G4 inventory
checked. R3 evidence cumulatively requires R2 then R1, with their named
tests and the frozen portal/workflow-only baseline. No cycles: R1/M1
accessibility deliverables depend only on their tested slices, not later
RB-23 scripts, RB-10 or the R5 manifest. M1 explicitly orders RB-08 before
RB-09 and excludes full-R2 upload evidence.

Markdown review: 12 rectangular tables and 38 local file links checked in
the two changed sources; no missing target. `git diff --check` passed.
Diff reviewed for both source documents; only scoped documentary changes.
No new source links or anchor changes. No uv, runtime suite,
heavy local gate, deployment or new requirements approval is authorised or
claimed. This explicit owner validation boundary is a documented deviation
from the repository's general full-local-gate instruction, not a passed gate.

### Assessed source identity

| Input | SHA-256 |
| --- | --- |
| PRD | 3094a602a5763ae6e25838639e1f7315735d065888c9d5b6caa3dd7ac456645b |
| Draft backlog | 0673b9705c129e3c50cef76c437106710121ddf074c977ed1e0aa13c6c7ef6f9 |
| Active proposal | 45d335fafa4ee346405ac085233ae1e8fb9f092f6b5a61f5da6eb28e7061075a |

## Pre-Review Reconciliation

Declared P01 scope Complete: P01, P01-T01 and P01-T02 checked in plan;
details and handoff synchronized. Research executed/Ready; original
critique Revise with PC-001 directly resolved, no second critique. No
implementation blocker. Quality FAIL, sizing and registration remain
separate follow-ups and no approval is inferred.

## Remaining Work and Handoff

P02-T01 independent Review executed Complete / Conformant with justified
divergence, no substantive findings. Original Review:
.copilot-tracking/reviews/logs/2026-10-27/resident-dependency-audit-454-review.md.
All three source hashes independently matched; Review assessed the working
tree before publication. Later checklist/status bookkeeping does not rewrite
that original Review or its assessed task-artifact hashes.

P02-T02 publication and
four thread replies/resolutions. Any late source change stops publication
under PC-001; later findings are reported, not another correction cycle.
