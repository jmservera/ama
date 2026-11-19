---
title: Issue 107 sixth live pass, unticked criteria (2026-11-19)
description: Fresh test run and proven/unproven table for the two unticked issue 107 criteria in the synthetic demo
ms.date: 2026-11-19
---

Scope: synthetic demo, desktop only. No Azure resource was created or changed.

## Evidence

* Command, from `src/api`: `python3 -m unittest tests.test_assistant_restart_non_replenishment tests.test_assistant_release -q`.
* Result on SQLite: 95 tests, OK, 22 skipped (actual-SQL classes need `ZF_TEST_MSSQL=1`).
* Actual SQL: see [r4 note](issue-107-live-r4-criteria-2026-11-19.md), 30 tests with 0 skipped on a local SQL Server 2022 container.

## Per-criterion result

| Criterion | Result | Basis |
| --- | --- | --- |
| Independent SQL connection/worker and race tests for material mismatches, revocation, restart; old images and restarts cannot restore revoked approval or replenish allowances | Proven for the demo (SQLite and local actual SQL) | Tests above; Azure SQL and a pulled registry image remain untested and are not needed for the demo |
| Matching approved exercise record permits bounded proposals only; delivered-build real AI, SQL and Azure evidence | Unproven | Needs an approved release record from unappointed OQ-017 holders and real-AI authority; human step |

No source change was warranted; a further test would duplicate existing coverage.
