<!-- markdownlint-disable-file -->
# Changes: region and quota parameters with recorded checks (issue #137)

* `infra/main.bicep`, `infra/modules/guard.bicep`: new parameters and guards.
* `infra/main.bicepparam`, `main.test.bicepparam`, `main.pilot.example.bicepparam`: explicit region and budget parameters.
* `infra/scripts/region_quota_preflight.py`: new offline preflight.
* `infra/tests/test_region_quota_137.py`: new contract tests.
* `infra/README.md`: parameter contract and helper documented.

Divergence: capacity guard covers `chatModelCapacity` only; `modelDeployments` overrides are checked by the preflight.

Validation: az bicep build and build-params for all three sets pass; ruff check and format clean for new files; infra unit tests pass except `test_ledger_alert_queries_match_the_verifier_markers` (pre-existing: `zava_forward.orchestrator` not installed, fails identically on base). Repository-wide `ruff --isolated` at line length 100 reports pre-existing findings in untouched files.

## Cycle 1 (3 findings fixed)

* `infra/modules/foundry.bicep`, `infra/main.bicep`: `endpointLocation` keeps the private endpoint in the VNet region.
* `infra/scripts/pipeline.py`: `aiModelLocation` override (key only) validated as a region; `infra/tests/test_pipeline.py`, `infra/README.md` updated.
* `infra/scripts/region_quota_preflight.py`: `read_capacity`, `--bicepparam`, checks `parameter-capacity-budget` and `record-covers-parameter-capacity`.
* Test file renamed to `infra/tests/test_region_quota_137.py` with new cases.

Validation: ruff check and format clean; both unittest discover patterns and test_pipeline pass; `az bicep build infra/main.bicep` passes.
