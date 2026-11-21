# Plan: issue 2061 live single-environment deploy with sqlTier dtu (2026-11-20)

Refs #2061. Task `issue-2061-live-dtu`. Tier FULL (infra and live deployment). Details: `.copilot-tracking/details/2026-11-20-issue-2061-live-dtu-details.md`. Critique: `.copilot-tracking/plans/2026-11-20-issue-2061-live-dtu-critique.md`.

## Phases

1. Source change (separate clean commit): add `sqlTier='dtu'` (Standard S0, 10 DTU, no serverless settings) to `infra/main.bicep`, `infra/modules/sql.bicep` and `infra/modules/guard.bicep`; default stays `serverless`; focused tests in `infra/tests/`; runbook and README notes; runbook delete list gains `evhns-cutover-test-demo` with its id.
2. Local validation: bicep build, infra tests that touch SQL, guard and parameters; ruff on touched Python.
3. Commit the source change cleanly. Live deployment runs from that commit.
4. Live: rebuild the what-if parameter file from the runbook profile and the live app images (not the 2026-10-16 deployment); what-if; stop if a Delete touches SQL data, storage, Key Vault, IoT Hub, `cae-cutover-test-demo` or its public IP.
5. Deploy; run `create-sql-users.py`; move apps and jobs onto `cae-cutover-test-demo`; move the IoT Hub route to the template's `eh-<hub>` namespace and prove telemetry; Playwright employee and resident sign-in; Key Vault 403 test for the internal identity.
6. Delete the runbook delete list by resource id, plus `evhns-cutover-test-demo` only after telemetry and tests pass. Roll back on any failure.
7. Record per-criterion proven/unproven table, review once, commit artifacts, witness.

## Amendments from the critique

* Save live SQL, IoT Hub routing and Event Hub settings to the evidence directory before deploy; read every Modify (not only Delete) in the what-if.
* Two-stage IoT route move: stage 1 `iotHubRoutingReady=false`, verify sender role and private endpoint, stage 2 `true`; then prove telemetry; delete `evhns-cutover-test-demo` last.

## Stop and rollback rules

* No Delete on SQL data, storage, Key Vault, IoT Hub, `cae-cutover-test-demo`, its managed group or public IP, or resource group `ama`.
* No Key Vault rotation, no drills, no secrets printed, cap USD 700.
* Failure after deploy: redeploy with `demoSingleEnvironment=false`; keep old resources until every test passes.
