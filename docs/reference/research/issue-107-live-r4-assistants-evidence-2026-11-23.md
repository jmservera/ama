---
title: Five assistants live demo re-verification, fourth pass (Refs #107)
description: Fourth per-criterion proven or unproven record for the two unticked acceptance criteria of issue 107, adding the actual SQL Server 2022 process-race, restart and old-image run and a fresh live revision observation
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only, FOCUSED tier, no source change. Owner decisions of 2026-11-18 apply (live Azure authorised in resource group `ama`, cap USD 700; billing reconciliation, DPO and Legal approval and person-run assistive technology testing waived). Head `ac58e5c45`. This note supplements the [third pass](./issue-107-live-r3-assistants-evidence-2026-11-18.md).

## Result per unticked criterion

| Criterion | Result for the demo | Limit |
| --- | --- | --- |
| Independent SQL connection/worker and race tests cover material mismatches, revocation and restart; old images and restarts cannot restore revoked approval or replenish finite allowances | Proven for the demo on actual SQL Server 2022 (disposable local container, never Azure SQL): 95 tests OK, 0 skipped, including the composite `test_old_image_after_a_material_mismatch_cannot_reactivate_or_refill` and the process-level race, restart and changed-binding tests | An older released image cannot be pulled (ACR private, see the third pass), so "old image" is simulated by a store opened with the older stored-default settings. Independent exact-head review and hosted CI remain outstanding |
| A matching approved exercise record permits bounded proposals only; delivered-build acceptance needs version-linked real AI, actual SQL and Azure evidence (CON-009/AC-057) | Unproven for the demo | No approved release exists on the deployed build, and creating one needs a named approver and residual-risk holder (OQ-017); inventing one would fabricate authority. The denial side stays re-proven by tests; the approved side is shown only against constructed fixtures |

## Evidence

* SQL Server `mcr.microsoft.com/mssql/server:2022-latest` ran as a throwaway local container (port 14331, random password held only in a temporary file and in the environment, never printed). Command, from `src/api`: `ZF_TEST_MSSQL=1 ZF_SQL_SERVER=localhost ZF_SQL_AUTH=password ... python3 -m unittest tests.test_assistant_release tests.test_assistant_restart_non_replenishment -v`. Result: `Ran 95 tests in 121.430s OK`, no skips. Full output with the password masked: [mssql-release-tests.txt](../../../.copilot-tracking/evidence/107-live/mssql-release-tests.txt). The container was stopped (it was started with `--rm`) and the password file deleted.
* The SQLite proxy run of `tests.test_assistant_release` gave 65 tests OK with 7 skipped (the SQL Server classes), so the skipped classes are now covered.
* Live observation, read-only: `az containerapp revision list` shows one active revision `ca-cutover-test-demo-api--0000055` (created 2026-11-23T03:25:45Z) on image digest `sha256:b628e067...30b9f`; an unauthenticated `GET /api/assistants/releases` returns 401. No sign-in, invoke or write was made, no Azure resource was created, so nothing needed deletion.

## Limits

* The SQL run is local SQL Server, not Azure SQL; it is not delivered-build acceptance.
* No claim of approved release admission, serving-version attestation on the deployed build or human effectiveness is made.
