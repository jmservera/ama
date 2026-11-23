---
title: Issue 2191 live pass 4 changes
ms.date: 2026-11-23
---

Refs #2191 (closed). Tier: focused (infra test only; no `src` change). `rpi-checks.py --all` not run; hosted CI not observed. No live Azure change; the owner-authorised live estate was not touched this pass because the live proofs already exist in earlier notes.

## Changes

* `infra/tests/test_bicep_containerapp_demo_wiring.py`: new `SimulatorFailureRateWiring` test pins the `failureRate` default within `MAX_FAILURE_RATE` and its `ZF_SIM_FAILURE_RATE` wiring. Fails when the default is set to 0.95 (checked), passes otherwise.

## Validation

23 tests OK in the file; ruff check clean. The file's existing format differences were left alone.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Cohort covers at least 50% of homes | Proven live earlier, not re-proven now | 222 of 443 (live3 note); SQL S3 re-proof 51.5 to 58.5 percent in PR 2268 |
| Configurable intermittent-failure rate | Proven live earlier; template contract now tested | new test; live3 hub counts |
| Consent mix preserved | Proven live earlier | 111 granted, 111 declined (live3) |
| Unit tests | Proven; one added | counts above |
| Refs #184, #165 | Unproven here | outside this issue's criteria |
| Deployed image carries the cap fix | Unproven | needs image rebuild and push |
| Receiver full-window at 222 homes | Unproven | tracked in issue 2201 |
