---
title: Five assistants live demo re-verification, fifth pass (Refs #107)
description: Per-criterion record for the two unticked acceptance criteria of issue 107, adding regression tests for suspended-release reactivation and expired-release restart by an old image
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only, FOCUSED tier (test-only change, no `src` code change). Owner decisions of 2026-11-18 apply. Supplements the [fourth pass](./issue-107-live-r4-assistants-evidence-2026-11-23.md).

## Result per unticked criterion

| Criterion | Result for the demo | Limit |
| --- | --- | --- |
| Independent SQL connection/worker and race tests cover material mismatches, revocation and restart; old images and restarts cannot restore revoked approval or replenish finite allowances | Proven for the demo. Two new tests close the remaining restart gaps: an old image cannot reactivate a suspended release through the change path, and a release expired in its stored body stays denied after restart even when the old image is configured with a later expiry, with zero provider calls and unchanged domain rows and allowance pool. They pass on SQLite and on actual SQL Server 2022 (34 tests OK, 0 skipped) | Local disposable SQL Server only, never Azure SQL. A real older image cannot be pulled (private ACR), so an old image is a store opened with older settings. Independent exact-head review and hosted CI outstanding |
| A matching approved exercise record permits bounded proposals only; delivered-build acceptance needs version-linked real AI, actual SQL and Azure evidence (CON-009/AC-057) | Unproven for the demo | No approved release exists on the deployed build and creating one needs a named approver (OQ-017); inventing one would fabricate authority |

## Evidence

* `src/api/tests/test_assistant_restart_non_replenishment.py`: `test_old_image_cannot_reactivate_a_suspended_release_through_the_change_path` and `test_expired_release_stays_denied_for_an_old_image_with_a_later_configured_expiry`.
* SQLite run, from `src/api`: `python3 -m unittest tests.test_assistant_restart_non_replenishment` gave 34 tests OK (17 SQL Server cases skipped); ruff and mypy clean.
* Actual SQL Server run (throwaway local container, random password never printed, container removed): 34 tests OK, no skips. Output with the password masked: [mssql-restart-tests-20261123T172611Z.txt](../../../.copilot-tracking/evidence/107-live/mssql-restart-tests-20261123T172611Z.txt).
* No Azure resource was created or changed; the live revision observation of the fourth pass was not repeated.

## Sixth pass: concurrent token-allowance race (run 20261123T210546Z)

Prior passes raced the call allowance only. A new regression test, `test_concurrent_connections_never_reserve_more_than_the_token_allowance`, starts three independent workers behind a barrier on a pool that fits exactly one token reservation (call allowance 1000, so the token pool is the limiter). Result on SQLite and on a throwaway SQL Server 2022 container (removed afterwards): sorted results `[False, False, True]`, one provider call, one used call. The full module ran 36 tests, 0 skipped, on SQL Server. Evidence: [mssql-token-race-20261123T210546Z.txt](../../../.copilot-tracking/evidence/107-live/mssql-token-race-20261123T210546Z.txt) (no credentials). Criterion 8 stays unproven for the demo: no approved exercise record on the deployed build (OQ-017, owner-gated).
