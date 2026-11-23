---
title: Five assistants live demo re-verification, ninth pass (Refs #107)
description: Per-criterion proven or unproven record for the two unticked acceptance criteria of issue 107 on live revision 0000058, with no source change
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only, FOCUSED tier, no `src` change. Owner decisions of 2026-11-18 apply. Supplements the [fifth pass](./issue-107-live-r5-assistants-evidence-2026-11-23.md) and the [fourth pass](./issue-107-live-r4-assistants-evidence-2026-11-23.md).

## Result per unticked criterion

| Criterion | Result for the demo | Limit |
| --- | --- | --- |
| Independent SQL connection/worker and race tests cover material mismatches, revocation and restart; old images and restarts cannot restore revoked approval or replenish finite allowances | Proven for the demo. `tests.test_assistant_release` and `tests.test_assistant_restart_non_replenishment` pass again at the current head (99 tests OK). The same classes passed on actual SQL Server 2022 in the fourth and fifth passes (95 and 34 tests, 0 skipped) | The SQLite run skips 24 SQL Server cases, so this pass adds no new actual-SQL run. Local disposable SQL only, never Azure SQL. A real older image cannot be pulled (private ACR); an old image is a store opened with older settings |
| A matching approved exercise record permits bounded proposals only; delivered-build acceptance needs version-linked real AI, actual SQL and Azure evidence (CON-009/AC-057) | Unproven for the demo | No approved release exists on the deployed build, and creating one needs a named approver and residual-risk holder (OQ-017). Inventing one would fabricate authority. The approved side is shown only against constructed fixtures |

## Evidence

* Live, read-only: `az containerapp revision list` shows one active, Healthy revision `ca-cutover-test-demo-api--0000058` (created 2026-11-23T19:20:29Z) on image digest `sha256:4121f3b9...dcdea8`. Unauthenticated `GET /api/assistants/releases` and `GET /api/health` return 401. See [live-probe-20261123T202647Z.txt](../../../.copilot-tracking/evidence/107-live/live-probe-20261123T202647Z.txt).
* Tests, from `src/api`: `python3 -m unittest tests.test_assistant_release tests.test_assistant_restart_non_replenishment` gave `Ran 99 tests ... OK (skipped=24)`. See [sqlite-tests-20261123T202647Z.txt](../../../.copilot-tracking/evidence/107-live/sqlite-tests-20261123T202647Z.txt).
* No defect was found, no sign-in or write was made, and no Azure resource was created, so nothing needed deletion.
