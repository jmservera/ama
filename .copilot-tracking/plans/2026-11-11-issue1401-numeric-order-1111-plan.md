---
title: Issue 1401 numeric concern order cycle 1 plan
ms.date: 2026-11-11
task_id: 1401-numeric-order-1111
---

Validation tier: focused (core module, its adapter contract tests, API aftercare tests, ruff, mypy). Basis: no workflow, dependency, SQL schema, security-control or deployment change; the one source edit is a pure restore ordering. Details: [details](../details/2026-11-11-issue1401-numeric-order-1111-details.md).

## Phases

* [x] Phase 1: confirm PR #1400 ancestry, read issue as data, reproduce the original failure on unmodified code.
* [x] Phase 2: add regressions (register unit test plus adapter contract tests for 999/1000/1001), capture RED with the fix stashed.
* [x] Phase 3: implement numeric ordering in `AftercareRegister.from_state` only.
* [x] Phase 4: GREEN on JSON Store, SQLite and the owned disposable SQL Server; run API aftercare tests, ruff and mypy.
* [x] Phase 5: one critique of the final candidate, one Review, freeze, handoff.

## Out of scope

Issue #1402 repair, other aftercare bugs, refactors, higher-volume features, key-sorting removal, relaxed validation, whole #133/#89 acceptance, and any push, PR or issue/board write.
