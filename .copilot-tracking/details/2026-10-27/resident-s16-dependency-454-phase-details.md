---
title: Resident S16 dependency correction phase details
description: Task context and completion evidence for the PR 454 correction
ms.date: 2026-10-27
---

Task: `jmservera/ama#454:discussion_r4390263899`
Plan: `.copilot-tracking/plans/2026-10-27/resident-s16-dependency-454-plan.md`
Research: `.copilot-tracking/research/2026-10-27/resident-s16-dependency-454-research.md`

<!-- P01 -->
## P01: Documentary correction

### P01-T01

In `.copilot-tracking/changes/2026-10-25/resident-prd-backlog-readiness-441-draft-backlog.md`,
split the combined RB-17/RB-18 dependency row. Preserve all existing
prerequisites and conditional comparison freeze. Add RB-17 only to RB-18,
and repeat it in the RB-18 slice gate cell. Explicitly preserve urgent help
independent of model/task release and no OD-53 for both items. RB-19/RB-20
remain untouched.

### P01-T02

The PRD story row already has S13/S15 and independent urgent help; acceptance
also preserves model independence. Do not edit the PRD. In the current
unregistered proposal's grouped R4 reconciliation, explicitly state S16
follows S13/S15 for task-failure verification and preserve the independent
R3/human route. Historical author snapshots/assessment reports remain unchanged.

### P01-T03

Check exact row uniqueness and prerequisites, help/OD-53 wording, table cell
counts, introduced links and whitespace. Review the complete small source diff.
Record actual outcomes in the changes artifact. No runtime tests, new tooling,
full gate receipt or fresh full-PRD assessment is needed/claimed.

<!-- P02 -->
## P02: Independent Review and publication

Current handoff: P01-T01/T02/T03 complete, documentary assertions and both
active table shapes passed, 39 relative link targets verified across seven
Markdown files, `git diff --check` passed. No source blocker/divergence.
PRD, historical assessments and RB-19/RB-20/governance/protocol rows unchanged.
P02-T01 now complete: independent Review Complete / Conformant, no substantive
findings. P02-T02 remains pending; publication, not runtime acceptance.

### P02-T01

Fresh independent worker reviews the final correction against plan, evidence
and owner boundaries, writes only the dated Review. One Review only; findings,
if any, route to later work rather than a hidden second pass. Approval and
unchanged full-PRD FAIL remain separate.

### P02-T02

Resolve authenticated GitHub account and set local privacy-safe author/committer
email. Commit changed documentation and original RPI evidence with the requested
trailer. Fetch/reconcile bot movement before normal push without rewriting
published history. Reply to thread `PRRT_kwDOUU8JX86wvdLp` with commit-linked
dependency and validation evidence; resolve only if the requested fix is
published and the independent review supports it. Do not merge.
