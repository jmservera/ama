<!-- markdownlint-disable-file -->
# Plan: region and quota parameters with recorded checks (issue #137)

* [x] Add `aiModelLocation`, `aiModelFallbackLocation`, `modelCapacityBudget` to `infra/main.bicep` and wire Foundry to `aiModelLocation`.
* [x] Add guards `aiFallbackLocationMustDiffer` and `modelCapacityMustFitBudget` (and empty model region to `deploymentLocationsMustBeSelected`).
* [x] Set the parameters explicitly in dev, test and pilot sets (pilot model region stays a PLACEHOLDER).
* [x] Add `infra/scripts/region_quota_preflight.py` (offline, deterministic).
* [x] Add `infra/tests/test_region_quota_137.py` contract and preflight tests.
* [x] Update `infra/README.md`.

Critique: single self-critique; compatible finding applied (guard limited to `chatModelCapacity` because the policy test evaluator cannot evaluate lambdas; overrides are covered by the preflight). No real check reference is fabricated.

## Cycle 1 findings (independent-direct-137-quota-85addb5e1)

* [x] `foundry.bicep` gains `endpointLocation` (default `location`) for the private endpoint; `main.bicep` passes `endpointLocation: location`.
* [x] `aiModelLocation` added to `infra/scripts/pipeline.py` `OVERRIDES` (a set of keys, so the key only; no env-var mapping exists), with region validation and README.
* [x] Preflight parses `chatModelCapacity`/`modelDeployments` from the `.bicepparam` file (positional or `--bicepparam`).

Critique: single self-critique; compatible.
