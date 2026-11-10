---
title: Infrastructure integration 136 recovery correction R1C1 amendment
description: Superseding correction of R1 provenance, acceptance criteria summary and file accounting for current use
ms.date: 2026-11-09
---

## Status

Supersedes, for current use only, the R1 wording named below. The R1 records, the original 16 files, the earlier critiques and reviews, and the immutable native recovery log are preserved and not rewritten. This amendment does not claim any native log changed. Source: the independent readiness report (approve_with_comments; Medium 2, Low 1).

## Correction 1 Provenance (Medium)

* R1 research, plan, details, changes, review and state were created together in one recorded recovery operation, which also committed them. No separately timestamped planning checkpoint or critique preceded implementation inside that operation.
* The "One critique executed" statement in the R1 plan describes an author-inline scope assessment. It is not independent and not a separately evidenced checkpoint. The word "Prospective" in the R1 plan title and description means the plan stated its intended scope, not that an earlier checkpoint was captured.
* This correction cycle (R1C1) differs: its [research](../research/2026-11-09-infrastructure-integration-136-r1c1-research.md), [plan](2026-11-09-infrastructure-integration-136-r1c1-plan.md) and [details](../details/2026-11-09-infrastructure-integration-136-r1c1-details.md) were committed before implementation, as a separate Git commit.
* No retrospective R1 checkpoint is created.

## Correction 2 Five unproven acceptance criteria (Medium)

The original matrix is in the [topic record](2026-11-08-infrastructure-integration-136-topic-record.md), section "136 acceptance criteria status". The R1 summary "four" referred to four original criteria; with the #440 scoped checkpoint the total is five. Current status, all unproven and none ticked:

| # | Criterion | Status | Open evidence |
| --- | --- | --- | --- |
| 1 | Scoped stabilization checkpoint of #440 before closure | Unproven | No scoped checkpoint, bug or refactor disposition |
| 2 | Every resource in Bicep or intentionally manual with owner | Unproven | Static register only; manual owner confirmation, full coverage and live check absent |
| 3 | Child features accepted | Unproven | Children 137, 138, 140, 142, 143, 144, 145, 146, 148 open; none accepted at parent level |
| 4 | From-empty deployment reproducible | Unproven | No new run; 2026-10-12 observation predates the 2026-10-27 cut-over |
| 5 | Delivered versus missing status current in the epic | Unproven | Tracking recommendations only; epic body not refreshed by the owner |

Use `Refs #136`; no closing keyword.

## Correction 3 Six R1 files (Low)

R1 added six files: five Markdown (research, plan, details, changes, review) plus one state JSON. The state is counted once. Inline critique shares the plan path, not a further file. Accounting: 16 original plus 6 R1 equals 22 files in `git diff origin/main...HEAD` at `b816656aa`. The "seven" in the R1 handoff and in the native closeout is superseded and remains as historical adverse evidence.

With R1C1 (research, plan, details, amendment, changes, review, state: seven added files) the candidate diff is 29 files.
