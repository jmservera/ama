---
title: Issue 107 separate-process provider, endpoint and deployment tests and live gate proof (Refs #107)
description: The last three release-bound routing fields now move in a separate OS process, plus read-only live proof that the deployed build denies all five assistants without an approved release
ms.date: 2026-11-25
---

Scope: synthetic demo, desktop only. Tier FULL (test code under `src/api/tests`); `rpi-checks.py --all` was not run. Builds on the [eleventh pass](./issue-107-live-r11-schema-registry-2026-11-24.md). Live Azure use was read-only: no resource, setting or release was created or changed. A disposable local SQL Server 2022 container (127.0.0.1) was created and removed.

## Gap closed

The release binds 13 fields. After r11, separate-process tests moved eight. This pass adds `provider`, `endpoint` and `deployment` variations to `assistant_process_worker.py` and three tests reusing `check_process_wide_binding`: the changed-route process revokes the release (trigger `model`) and is denied with no provider call; a fresh original-binding process with a larger allowance and later expiry stays denied, and stored calls, attempts and the revoked record do not change. Only `task_contract_version` and `evaluation_version` remain covered by in-process tests alone; both derive from source in the same image, so a separate process cannot change them without changing code.

## Evidence

* SQLite: `test_assistant_release` plus `test_assistant_restart_non_replenishment`: 115 tests OK (32 skipped, the SQL Server classes).
* SQL Server 2022 container: `MssqlUnleasedRevocation` plus the restart module: 49 tests OK, 0 skipped (46 before, 3 added). Container removed.
* Mutation check: not applying the constructed route in the worker makes the endpoint test fail.
* `ruff check`, `ruff format --check` (worker) and `python3 -m mypy` in `src/api` are clean.
* Live, read-only, signed in as the test employee (values never printed; see `.copilot-tracking/evidence/107-live/`): revision `ca-cutover-test-demo-api--0000068` was the single active revision at 14:16Z; `GET /api/health` and `/api/assistants/releases` return 401 unauthenticated. Signed in, `GET /api/assistants` lists the five assistants (stock-prioritisation, assessment-preparation, funding-evidence, works-resident-coordination, quality-evidence), `proactive` is false, and every assistant reports `Release admission denied: no approved release matches (approved, unexpired release record)` with the OQ-017 owner and the four authority holders (release, residual-risk acceptance, suspension, restart) as gaps. Twelve repeated reads returned the SQL-backed path with `durable_sql_release_store` passed, `rai_exercise_acceptance` passed and `real_ai_delivery_gate` blocked. The blocking reasons are OQ-017 named live releases, OQ-017 authority holders, OQ-018 and OQ-019. `/api/assistants/proposals` shows every listed proposal `disabled`; `rai-metrics` shows 4 invocations, 4 fallbacks, 0 provider tokens.
* Observation: during the session the app moved to revision 0000069 (two replicas) through a deployment by another worker, and two early reads showed a non-SQL response shape with the SQL store check failing, and `/api/assistants` returned 503 `sql-write-lock-busy` once. These are transient and coincide with that deployment; they are recorded, not diagnosed, and I made no change to the Azure estate.

## Per-criterion result

| Criterion | Result for the demo | Limit |
| --- | --- | --- |
| Independent SQL connection/worker and race tests cover material mismatches, revocation and restart; old images and restarts cannot restore revoked approval or replenish finite allowances | Proven for eleven of the 13 bound fields moved in separate processes, plus racing, restart and non-replenishment tests on SQLite and disposable SQL Server | Constructed fixtures; local disposable SQL only, never Azure SQL; no real older packaged image was run (see issue comment on #1840) |
| A matching approved exercise record permits bounded proposals only; delivered-build acceptance needs version-linked real AI, actual SQL and Azure evidence (CON-009/AC-057) | Partly proven: the approved side is shown against constructed fixtures (`note`: bounded proposals only); the deployed build is shown default-off and denying all five without an approved release. Delivered-build acceptance is unproven | Creating an actual approved release needs a named approver and residual-risk holder (OQ-017) that do not exist; inventing one would fabricate authority. OQ-018 and OQ-019 are owner and DPO items outside the demo scope |
