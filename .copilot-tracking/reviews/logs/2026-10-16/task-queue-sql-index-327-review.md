---
title: SQL queue membership implementation review
description: One post-implementation review of issue 327 delivery
ms.date: 2026-10-16
---

Task: #327 / task-queue-sql-index-327.
Execution: Complete. Outcome: Conformant.

## Assessed Boundary

Owner-directed SQL membership, hot IDs, authorisation after lookup, portable
schema and statements, existing-row backfill, every queue/sort/view parity,
generated-stock write-cold/repeat measurements, mutation evidence and delivery.
No live Azure, Docker, private stock or operational acceptance claim.

## Inputs

* .copilot-tracking/research/2026-10-16/task-queue-sql-index-327-research.md
* .copilot-tracking/plans/2026-10-16/task-queue-sql-index-327-plan.md
* .copilot-tracking/details/2026-10-16/task-queue-sql-index-327-phase-details.md
* .copilot-tracking/reviews/2026-10-16/task-queue-sql-index-327-critique.md
* .copilot-tracking/changes/2026-10-16/task-queue-sql-index-327-changes.md
* Current source/test/documentation patch and session validation outputs.

## Reconciliation

P01/P02 source and validation evidence complete. P03-T01 is intentionally pending
Review and publication, not an unimplemented source requirement. PC-001/002/003
were compatible planner-owned refinements applied once; no owner decision gap.
No active blocker, source work or unrouted plan follow-up is declared.

## Assessment

* Six integer flags exist in both schemas. Additive migration uses portable
  ALTER TABLE ADD, invalidates readiness atomically, and backfills after effective
  as_of and complete SQL shared state exist. Existing body/rowversion/sequence/
  audit evidence is preserved by the backfill regression.
* Seed/save maintain membership in their writer transaction; errors roll back
  body and derived state together. Shared context comes from persisted SQL,
  not stale process data. Linked-home/package/hold changes conservatively
  recompute all memberships. This is a deliberate cost, documented rather than
  hidden as constant-time behavior.
* Fingerprint/generation publication is atomic and every hot/cold lookup checks
  it under the writer lock. The case copy synchronises before ID lookup; ranking
  follows that synchronisation. Review traced the controlled interleaving test
  and the ordinary-write, shared-write and refresh-only two-store cases.
* The existing canonical evaluator is reused through _work_context. Candidate
  IDs carry no authority or viewer context. Existing ownership, filters,
  contractor denial and request-time projection remain in Store._filtered and
  page output. The extended uncached parity oracle covers every queue/sort/view
  with a nonempty approved-priority fixture; existing draft/denial/cursor/export
  tests remain.
* Local SQL Server DDL/index/migration and shared statement checks are sound
  bounded evidence. Seven inherited behavior tests are discoverable but opt-in.
  No real SQL Server/Azure execution is claimed.
* The final benchmark uses identical generated stock and lightweight counting,
  exact merged baseline sources, three committed-write/cold/repeat rounds per
  queue, and separately measured initialization. Earlier heavier-instrumented
  results are explicitly superseded, not mixed with final comparison. Outliers,
  remaining global ranking and full-refresh costs are disclosed.
* P03 delivery separation is an immediately relevant planning clarification,
  not a divergent architecture or acceptance change. No test removals, new
  dependencies, private-data access or prohibited path modifications were found.

## Validation Evidence

Core 487 tests / one skip, API 549 / 110 skips, agents 70, orchestrator 22,
importer 39: all executed tests passed. All five projects passed Ruff lint,
format and mypy. The final lightweight 60k benchmark passed all six assertions;
exact baseline code failed all six. Three focused source-path mutations were
killed by intended assertion failures, not import/runtime errors. Subsequent
targeted SQL and parity suites passed 12 and 13 methods. git diff --check passed.
Source, test and documentation review used the complete supplied patch.

## Findings and Routing

No substantive in-scope findings. No RV items or later corrective stage is
required. Live-engine acceptance remains an explicit evidence boundary rather
than a claimed test result or an invented follow-up task.

## Outcome and Next Action

Complete / Conformant for the local engineering boundary. Publish P03-T01 through
the requested topic PR and leave merge/hosted-check disposition to the owner.
This is the single post-implementation Review; no repeat Review is planned.
