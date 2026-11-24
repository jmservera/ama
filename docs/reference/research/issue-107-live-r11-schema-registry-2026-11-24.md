---
title: Issue 107 separate-process schema and registry mismatch race tests (Refs #107)
description: The last two bound release fields not yet moved in a separate OS process, now covered on SQLite and a disposable SQL Server, with a per-criterion proven or unproven record
ms.date: 2026-11-24
---

Scope: synthetic demo, desktop only. Tier FULL (test code under `src/api/tests`); `rpi-checks.py --all` was not run. No sign-in, no Azure write, no Azure resource; a disposable local SQL Server 2022 container (127.0.0.1) was created and removed. Builds on the [tenth pass](./issue-107-live-r10-root-cause-2026-11-24.md).

## Gap found

The release binds 13 fields. After r10, separate-process tests moved policy, prompt, permission, data, provenance and serving model. `registry_version` and `schema_version` were not moved in a separate process.

## Code added

* `assistant_process_worker.py`: variations `schema` (changes `SCHEMA_VERSION`) and `registry` (changes `VERSION`), confined to the worker process.
* `test_assistant_release.py`: two tests reusing `check_process_wide_binding`. A changed-schema or changed-registry process revokes the release and denies the task with no provider call; a fresh original-binding process with a larger allowance and later expiry stays denied, and stored calls, attempts and the revoked record do not change. Observed triggers: schema gives `data` and `evidence` (the schema also feeds `data_version`); registry gives `evidence`.

## Evidence

* SQLite: `test_assistant_release` plus `test_assistant_restart_non_replenishment`: 109 tests OK (29 skipped, the SQL Server classes).
* SQL Server 2022 container: `MssqlUnleasedRevocation` plus the restart module: 46 tests OK, 0 skipped. Container removed.
* Mutation check: leaving `SCHEMA_VERSION` unchanged makes the schema test fail.
* `ruff check`, `ruff format --check` and `python3 -m mypy` in `src/api` are clean.

## Per-criterion result

| Criterion | Result for the demo | Limit |
| --- | --- | --- |
| Independent SQL connection/worker and race tests cover material mismatches, revocation and restart; no restore or replenishment | Proven for the eight fields moved in separate processes (registry, schema, prompt, policy, data, provenance, permission, model); provider, endpoint, deployment, task contract and evaluation version are covered by in-process tests only | Constructed fixtures; disposable SQL Server only, never Azure SQL |
| Matching approved exercise record permits bounded proposals only; delivered-build acceptance | Unproven | No approved release on the deployed build; needs a named approver (OQ-017) |
