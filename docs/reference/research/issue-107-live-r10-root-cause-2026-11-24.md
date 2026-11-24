---
title: Issue 107 root cause of repeated no-new-proof re-verification, and process-level mismatch tests (Refs #107 #1830 #435)
description: Why ten passes of live re-verification of issue 107 added no proof, the missing separate-process model, data and provenance mismatch race tests now added, and a per-criterion proven or unproven record
ms.date: 2026-11-24
---

Scope: synthetic demo, desktop only. Tier FULL for the change (test code under `src/api/tests`); `rpi-checks.py --all` was not run. Owner decisions of 2026-11-18 apply. No sign-in, no Azure write and no Azure resource; a disposable local SQL Server container was created and deleted. Supplements the [ninth pass](./issue-107-live-r9-criteria-2026-11-23.md).

## Why re-verification returns no new proof

* The evidence class is saturated. Passes r2 to r9 re-ran the same unit classes and unauthenticated probes. The tests exist and pass; a rerun repeats a result already recorded and cannot tick a box.
* Live probes cannot reach the property. Unauthenticated `GET /api/assistants/releases` and `/api/health` return 401, which says nothing about revocation or restart. The SQL test fixture refuses any server except localhost, 127.0.0.1 or `sql` (`MssqlFixture.setUp` in `test_assistants.py`), so the independent-connection tests deliberately never run against Azure SQL.
* The 24 to 27 skipped classes are the actual-SQL variants. They run only with `ZF_TEST_MSSQL=1` and a disposable SQL Server, which CI provides and agent sessions did not start. A default run therefore proves the SQLite side only.
* The second criterion needs an appointed approver and residual-risk holder (OQ-017). A live check cannot supply that without fabricating authority.
* #1830 and #435 follow the same pattern: their unticked items need an external statement (mentor, owner, hosted CI on a pushed head) that a local rerun cannot produce.
* A genuine gap did exist: the separate-OS-process harness varied only policy, prompt and permissions. The in-process separate-worker class already covered ten triggers.

## Code added

* `src/api/tests/assistant_process_worker.py`: variations `data`, `provenance` and `model`.
* `src/api/tests/test_assistant_release.py` (`ProcessRaces`): three tests. A changed-data, changed-provenance or changed-serving-model process revokes the release and denies the task with no provider call; a fresh original-binding process with a larger allowance and later expiry stays denied, and stored calls, attempts and the revoked record do not change.
* A mutation check (serving model left unchanged) makes the model test fail, so it can fail.

## Evidence

* Live, read-only: revision `ca-cutover-test-demo-api--0000060` (2026-11-24T08:11:30Z), Healthy; unauthenticated releases and health return 401. See [live-probe-20261124T083552Z.txt](../../../.copilot-tracking/evidence/107-live/live-probe-20261124T083552Z.txt).
* SQLite: `tests.test_assistant_release` and `tests.test_assistant_restart_non_replenishment` gave 105 tests OK (27 skipped, the SQL Server classes).
* SQL Server 2022 in a local container (`ZF_TEST_MSSQL=1`, server 127.0.0.1; note `localhost` resolved to IPv6 and failed to connect): `MssqlUnleasedRevocation` plus the restart module gave 44 tests OK, 0 skipped. The container was removed.
* `ruff check`, `ruff format --check` on the worker and `python3 -m mypy` in `src/api` are clean.

## Per-criterion result

| Criterion | Result for the demo | Limit |
| --- | --- | --- |
| Independent SQL connection/worker and race tests cover material mismatches, revocation and restart; old images and restarts cannot restore revoked approval or replenish finite allowances | Proven for the demo on constructed fixtures and a disposable actual SQL Server, now including separate-process model, data and provenance mismatches | Not run against the live Azure SQL database, by design of the fixture |
| A matching approved exercise record permits bounded proposals only; delivered-build acceptance needs version-linked real AI, actual SQL and Azure evidence (CON-009/AC-057) | Unproven for the demo | No approved release exists on the deployed build; creating one needs a named approver (OQ-017) |
