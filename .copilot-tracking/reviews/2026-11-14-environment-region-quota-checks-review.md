<!-- markdownlint-disable-file -->
# Review: region and quota parameters with recorded checks (issue #137)

Execution: executed once, post-implementation. Outcome: conformant with noted limits.

* AC "Region and quota choices are parameters with recorded checks, not assumptions": met in source: explicit parameters in all three sets, named guards, deterministic preflight, contract tests.
* Limit: committed sets carry empty check references by design; no live Azure check was run, and pilot region/quota remain owner decisions.
* Follow-ups: extend the capacity guard to `modelDeployments` overrides; install `src/orchestrator` to clear the pre-existing policy-test error.

## Cycle 1 review

Execution: executed once. Outcome: conformant; all 3 independent findings resolved with tests. Limit: no live Azure what-if was run. Follow-up: the Bicep capacity guard still covers `chatModelCapacity` only.
