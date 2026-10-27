---
title: Resident PRD and backlog readiness correction cycle 2 plan
description: Prospective plan for the RB-21 paired-protocol freeze dependency correction (issue 441)
ms.date: 2026-10-25
---

## Trigger and research

* Coordinator draft-return comment 6394209248 and blocking review comment on draft-backlog RB-21 (line 123 dependency row).
* Evidence: PRD stage table (R0 includes "test expectations and protocol"; R3 requires a portal/workflow-only effort baseline; R5 requires paired results) and the PRD GOAL-005/FR-071 text: "freeze a paired synthetic protocol before testing". Proposal staging row R5 says collect results only. So the freeze belongs to R0; R5 only collects and reviews.
* Defect: RB-21 was a frozen-protocol item placed in R5 and depending on RB-10 to RB-16, so RB-13 to RB-20 could produce comparison evidence before rules were frozen.
* Bot head 0099fc2a changes only the score JSON; fast-forwarded first. Main 36996d70.

## Planned changes (minimal, documentation and tracking only)

* [ ] Move the paired-protocol freeze into RB-01 (R0): matched packs, disjoint episodes, effort and adverse-outcome definitions, review and recovery effort, unknowns stay unknown.
* [ ] Redefine RB-21 as R5 result collection and review only; depends on RB-01 and on RB-13 to RB-16 baseline and RB-17 to RB-20 evidence or recorded blocked status.
* [ ] Make every comparison-evidence run (RB-13 to RB-20, RB-24 where effort is recorded) depend on RB-01 frozen protocol; no effort or adverse-outcome data counts if gathered before the freeze.
* [ ] Fix hierarchy list and RB-22 dependency; append correction notes to changes, review, critique, state; append log entry. No edit to PRD or proposal expected unless review finds a coupled contradiction.
* [ ] One independent review of the corrected full proposed dependency graph and requirement trace (not a full-PRD quality pass), then commit, gate with new output and lock timeout 14400, official verification, normal push.

## Boundaries

Unsigned PRD, unregistered proposal (id null), G0 owner acceptance pending, inherited findings open, no date, no implementation issues, no runtime. Earlier stale statements of owner readiness are corrected by appended history only.
