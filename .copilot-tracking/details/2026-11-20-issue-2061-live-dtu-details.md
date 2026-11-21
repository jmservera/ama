# Phase details: issue 2061 live deploy with sqlTier dtu (2026-11-20)

## Source edits

* `infra/modules/sql.bicep`: allow `dtu`; database `sku` is `{ name: 'Standard', tier: 'Standard', capacity: 10 }` for `dtu` with no `family`; `autoPauseDelay` and `minCapacity` stay null unless serverless; GP SKUs unchanged.
* `infra/main.bicep`: allow `dtu` in `sqlTier`; description names it.
* `infra/modules/guard.bicep` and the guard call: `dtuTierRequiresDevelopmentProfile` (dtu only for `deploymentProfile=development`), so production cannot take the S0 tier.
* Tests: `test_sql_tier.py` (compiled sku for dtu, null serverless settings, guard cases), `test_environment_quota_parameters.py` allowed values, `test_bicep_policy.py` guard loop if it enumerates tiers.
* Runbook: profile adds `sqlTier=dtu`; delete list adds `evhns-cutover-test-demo` with id; Event Hubs move step.

## Live parameter file

Built under `/tmp` (not committed) from the runbook profile: `workload=cutover`, `environmentName=test`, `deploymentProfile=development`, `demoDirectIngress=true`, `demoSingleEnvironment=true`, `enablePublicEdge=false`, `allowPublicNetworkAccess=false`, `sqlTier=dtu`, `iotHubRoutingReady=true`, live image digests read from running apps, Entra client id read from the live API app configuration (not a secret). SQL admin fields from the live SQL server.

## Verification

Commands and outputs (secrets redacted) are recorded in the changes record and in `docs/reference/research/issue-2061-live-single-environment-2026-11-20.md`.
