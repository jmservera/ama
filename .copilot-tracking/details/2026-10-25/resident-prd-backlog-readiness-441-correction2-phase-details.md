---
title: Resident PRD and backlog readiness correction cycle 2 phase details
description: Phase details for the paired-protocol freeze dependency correction
ms.date: 2026-10-25
---

## Phase 1: Backlog dependency correction

* RB-01 (R0): add the frozen paired protocol and the rule that comparison data gathered before the freeze is discarded as not evidence.
* RB-21 (R5): result collection and review; dependencies RB-01, RB-13 to RB-16, RB-17 to RB-20 (or blocked status).
* Dependency table: add RB-13 to RB-20 on RB-01 for the frozen protocol; RB-24 effort observations likewise.
* Hierarchy list: RB-21 stays in R5 as collection and review.
* Acceptance: a reader can trace that no comparison run can start before RB-01 is done.

## Phase 2: Evidence and review

* Append dispositions to critique, review, changes, state and log (append-only).
* Independent review of the full dependency graph and the FR-071/AC-132/133/GOAL-005 trace.

## Phase 3: Publication

* Commit with noreply identity and Copilot trailer, new gate output, official verification, normal push to the same draft PR.
