---
title: Issue 2191 live pass 3 changes
ms.date: 2026-11-21
---

Refs #2191. Tier: FULL classification because `src/core` changed (no `rpi-checks.py --all` run; the coordinator owns the gate). Local commit only.

## Changes

* `src/core/src/zava_forward/core/sensor_consumer.py`: `MAX_CONTROLS = 500` replaces the 100 literal in `configure`, `_changed_homes` (TOP/LIMIT and row check). Defect found live: 222 controls gave `INVALID_CONTROL_BATCH`.
* `src/core/tests/test_sensor_consumer.py`: one test (222 and 220 accepted, 501 refused); fails without the change.
* `infra/live-simulator-job.bicep` and `infra/README.md`: `failureRate` parameter (`ZF_SIM_FAILURE_RATE`), secret capacity note. Bicep compiles.
* `docs/reference/research/issue-2191-live-cohort-222-2026-11-21.md`, two screenshots, README index row, log entry.

## Live changes (resource group ama, all within the owner authorisation)

* 222 hub device identities registered (9 stale removed); consent mix 111/111 applied with a runtime shim (image predates the cap fix); `job-live-simulator` redeployed (445 secrets, skip rate 0.1) and `job-live-receiver` redeployed with a wider control. Temporary roles removed (readback 0); throwaway jobs deleted; key material shredded.

## Validation

* `test_sensor_consumer` 39 passed; `infra/tests` four wiring and hosting files 64 passed; ruff check and format clean; mypy in `src/core` shows the same 3 pre-existing errors with and without the change; Bicep compile clean.
* Not run: the full `src/core` and `src/api` suites, `rpi-checks.py --all`.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Cohort covers at least 50% of homes | Proven live | 222 of 443; 222 hub devices; 96 to 104 readings per slot from 111 granted homes |
| Configurable intermittent-failure rate | Proven live | `failureRate` 0.1 deployed; hub 192, 207, 196 of 222 per slot |
| Consent mix preserved | Proven live | 111 granted, 111 declined; staff app `ok` versus `consent-withheld` |
| Unit tests | Proven | Earlier 229 and 5 tests, new core test, 39 consumer tests |
| Refs #184, #165 | Unproven here | Outside this issue's criteria |
| Deployed image carries the cap fix | Unproven | Needs an image rebuild and registry push window; shim used |
| Receiver full-window behaviour at 222 homes | Unproven | Ingestion rows seen; window completion not observed (issue 2201) |
