---
title: Issue 81 demo recovery research
description: Recovery research for the controlled lifecycle parent PR 1240 before main reconciliation and demo-targeted validation
ms.date: 2026-11-09
task_slug: issue-81-demo-recovery
---

Refs #81. Research disposition `executed`. Planning Readiness `Ready` for the bounded scope below. This is an authentic recovery continuation, not a backfill of earlier phases.

## Scope

Existing PR #1240 (parent `feat/controlled-lifecycle-integration-81`) only. Not all lifecycle, legal or production controls. Production compliance, legal acceptance and security hardening are deferred, not satisfied.

## Identities observed (2026-11-09)

| Item | Value |
| --- | --- |
| PR #1240 head (seed) | `6ef6dc368ae3f8739095f740aa1e68634bd52922`, tree `0006f193b0fc459920f1fa3cf319d96c2a050c4a`; mergeable `CONFLICTING`; `statusCheckRollup` empty |
| Fetched `origin/main` | `b46a9ad9a9619db535368d1b2cbbddec8110e122` (#1299); merge base with seed `56eec736906774ef56d8c9a66ed7f3f9c1e520c6`; main is 43 commits ahead |
| Original verified head | `c5edb320a` against main `56eec736` (receipt `g81-r15-1106`); the seed adds only #86 (#1243) and was not covered by that receipt |
| Receipt | Original full receipt and its gate output were removed; it is historical and not current |

## Recovered original evidence (retained, unmodified)

* Original parent records: alignment (2026-11-06) and re-alignment r2 (2026-11-07) research, plans, critiques, changes, reviews and state under `.copilot-tracking/*/2026-11-0[67]/issue-81-*`; main merges (2026-11-07, 2026-11-08 `issue-81-merge-f548`).
* Original reviews are author Reviews, not independent, hosted or human review. Carried adverse findings: Medium (no FULL, SQL Server, browser or independent evidence for the head); #1226 follow-up (replacement route for in-progress quality records) open; #1238 Pending/supersession policy owner-blocked.
* Integrated #86 child records under `.copilot-tracking/*/2026-11-08/issue-86-*` including the SQL fixture baseline and fix reviews.

## Ancestry and boundaries

* Seed contains #1226 (`9055abce3`), #1228 (`e6434dd1d`), #1229 (`81c106998`, #82 explicit capacity gate outcomes) and #1243 (`6ef6dc368`, #86 complaints adapter); all are ancestors of the recovery HEAD. Main also already holds earlier #82 work (#898, #1035, #1097).
* Human and resident boundaries: sources keep roles, resident decision records and consent, manual routes and complaint/independent-review route open under holds. Nothing here approves Legal, resident, accessibility or owner decisions.

## Known blocking defect

#1292 (existing-main recommendation reload ordering after SQL reload; issue open, fix running separately). Not duplicated here and no sibling code imported. Affected SQL tests are expected to reproduce it; the exact result is recorded in the changes and review. Final SQL acceptance of #81 stays blocked on the merged #1292.

## Test selection (owner demo-targeted tier)

Changed source relative to main: `appointments.py`, `complaints_route.py`, `gates.py`, `procurement.py`, `quality.py`, `resident_decisions.py`, `store.py` (core only) and their core tests. Impacted selectors: `test_gates`, `test_resident_decisions`, `test_quality_procurement`, `test_hazard_referral`, `test_handoff_lifecycle`, plus ranking selectors to show the #1292 dependency. SQL: owned disposable loopback SQL Server container for changed persistence (`ZF_RESIDENT_MSSQL=1`), never an existing database. No `rpi-checks --all`.

## Open questions

None blocking planning. Whether #1292 lands before the coordinator integrates is a coordinator decision.
