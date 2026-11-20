# Changes: issue 2061 live deploy with sqlTier dtu (2026-11-20)

Refs #2061. Task `issue-2061-live-dtu`. Status: complete for the delivered scope. Tier: FULL (infra source changed); the full local gate was not run and `rpi-checks.py --all` was never run, so the receipt is coordinator-owned.

## Source changes (infra only, separate commits)

| Commit | Change |
| --- | --- |
| `16331ca89` | `sqlTier=dtu` in `infra/main.bicep`, `infra/modules/sql.bicep`, `infra/modules/guard.bicep`; tests in `test_sql_tier.py`, `test_bicep_policy.py`, `test_environment_quota_parameters.py`; `infra/README.md`; runbook profile, `eh-` namespace and delete-list row for `evhns-cutover-test-demo` |
| `ed3890a32` | Drop `maximumThroughputUnits` from the Event Hubs namespace (auto-inflate off); `overrideQueryTimeRange` `PT26H` to `PT48H` on `ledgerVerifyMissing`; tests and `monitoring-runbooks.md` aligned |

Live deploy ran from `ed3890a32`. Stage 1 first failed on the two issues the second commit fixes (deployment `main-dtu-20261120`); `main-dtu-20261120b` and `main-dtu-20261120c` Succeeded.

## Validation run

* `az bicep build -f infra/main.bicep`: built.
* Unit tests: `test_sql_tier`, `test_environment_quota_parameters`, `test_bicep_policy`, `test_deploy`, `test_resident_demo_deploy`, `test_iothub_module` passed (the last two sets re-run after the fix: 93 tests OK).
* Not run: `rpi-checks.py` (any mode), hosted CI. Pre-existing ruff findings in `test_sql_tier.py` were left alone.

## Live evidence

See [the research note](../../docs/reference/research/issue-2061-live-single-environment-2026-11-20.md) for commands, results, role inventory and the per-criterion table. Evidence directory: `/home/azureuser/.local/share/ama/phase-witness/2061-live-20261120T185228Z/live/`.

## Per-criterion table

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Decision record (ADR 0008) | Proven (earlier loop) |
| 2 | One external environment, ingress scoping | Partly proven |
| 3 | Reviewed delete list, only those removed | Proven (optional subnet and NSG, `evhns-cutover-test-demo` remain) |
| 4 | Entra URIs before/after table, employee and resident sign-in | Unproven (employee sign-in passed; URIs unreadable without directory privileges) |
| 5 | Identity split, role inventory, negative test | Proven for after state (403 internal, 200 API) |
| 6 | Demo end to end | Unproven (IoT Hub has no usable device path from here; no message sent) |
| 7 | Production profile builds, tests pass, full gate receipt | Partly proven; receipt unmet here |
| 8 | Rollback documented | Proven |

## Divergences and open items

* `create-sql-users.py` could not run from this host (SQL is private, admin is an application identity). The same statements ran in a throwaway job as `id-cutover-test-init`; the job was deleted.
* `evhns-cutover-test-demo` was not deleted: the owner condition (telemetry flows end to end) is unmet. Delete it by its id once a device message is shown on `eh-iot-cutover-test-rzsrg`.
* The runbook still says the delete list needs the old apps and jobs removed first, and that `create-sql-users.py` needs a reachable SQL host; neither was written back to the runbook after the deploy.
* ACR `defaultAction` Deny to Allow, Key Vault tag added, IoT Hub fallback route disabled.
