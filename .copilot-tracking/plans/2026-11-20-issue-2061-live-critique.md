# Critique (one pass, 2026-11-20)

Execution: executed once, on the final candidate plan. Verdict: proceed with amendments applied directly.

* Risk: dropping `snet-aca` by template would fail while the old environment exists. Applied: keep the subnet, list it as owner-approved cleanup after teardown.
* Risk: a new identity in production changes the production design. Applied: the identity and its roles exist only with `demoSingleEnvironment`; outputs fall back to the API identity.
* Risk: the issue asks for a public identity without SQL access, but the public API container needs SQL to serve employees. Applied: the API keeps SQL; the split removes the jobs from it and the ADR states the residual access honestly.
* Risk: live deployment, Entra redirect reads and a negative role test cannot be proven without deploy or Graph rights. Applied: record as unproven with the exact reason.
