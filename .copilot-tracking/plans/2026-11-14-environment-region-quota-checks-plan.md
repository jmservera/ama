<!-- markdownlint-disable-file -->
# Plan: region and quota parameters with recorded checks (issue #137)

* [x] Add `aiModelLocation`, `aiModelFallbackLocation`, `modelCapacityBudget` to `infra/main.bicep` and wire Foundry to `aiModelLocation`.
* [x] Add guards `aiFallbackLocationMustDiffer` and `modelCapacityMustFitBudget` (and empty model region to `deploymentLocationsMustBeSelected`).
* [x] Set the parameters explicitly in dev, test and pilot sets (pilot model region stays a PLACEHOLDER).
* [x] Add `infra/scripts/region_quota_preflight.py` (offline, deterministic).
* [x] Add `infra/tests/test_environment_region_quota_checks.py` contract and preflight tests.
* [x] Update `infra/README.md`.

Critique: single self-critique; compatible finding applied (guard limited to `chatModelCapacity` because the policy test evaluator cannot evaluate lambdas; overrides are covered by the preflight). No real check reference is fabricated.
