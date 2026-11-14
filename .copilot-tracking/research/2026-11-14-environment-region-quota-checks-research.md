<!-- markdownlint-disable-file -->
# Research: region and quota parameters with recorded checks (issue #137, last AC)

Date: 2026-11-14. Base: origin/main 61e1917dd075a8307f0fd436c42cc41f47906846.

## Findings

* `location`, `sqlLocation`, `regionCheckReference`, `quotaCheckReference` and model SKU/capacity were already parameters; guards reject empty references and locations.
* No separate model region (`aiModelLocation`) or fallback region existed: the Foundry account used `location`.
* No capacity budget parameter or offline preflight existed; README held dated read-only evidence (2026-10-18) that proves nothing for current deployments.
* Parameter sets live at `infra/main.bicepparam`, `main.test.bicepparam`, `main.pilot.example.bicepparam` (no `infra/parameters/` directory).
* The test evaluator in `test_bicep_policy.py` cannot evaluate lambdas or capacity expression defaults, so guards stay simple parameter comparisons.

## Planning Readiness

Ready. Research disposition: executed.
