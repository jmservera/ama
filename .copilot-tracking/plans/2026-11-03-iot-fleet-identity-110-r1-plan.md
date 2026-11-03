# Plan: IoT fleet identity evidence slice (issue 110 r1)

Stacked slices: S1 (this PR) offline fleet-identity evidence; S2 live Hub identities, issuance and a live stream after owner decisions on tier, sizing, cost, network exposure and credential owner (#140 provisioning); S3 live Azure SQL application acceptance.

## S1 scope

* [x] Add `FleetIdentityTests` to `src/api/tests/test_iot_stream.py` (two tests, constructed fixtures only).
* [x] Run focused IoT tests, ruff and mypy.
* [x] Record research, plan, details, critique, changes and review under `.copilot-tracking/`.

Details: [2026-11-03-iot-fleet-identity-110-r1-details.md](../details/2026-11-03-iot-fleet-identity-110-r1-details.md)

## Critique (single pass, self-run)

Verdict: proceed. Findings applied directly: the test must not claim a live Hub identity, so names and docstring say offline; no source change is needed. No conflict with confirmed decisions.

## Boundaries

No live Azure, credential, deployment, AI call or human approval widened. Criterion 1 stays unticked.
