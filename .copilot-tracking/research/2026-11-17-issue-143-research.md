# Research: issue 143 private networking and public edge

Base: origin/main eb51af5c9ab0b1353ac380fc8960ee8dd96d17c4. Tier: FOCUSED, evidence only, no live change.
Disposition: executed. Planning Readiness: Ready (assessment only).

## Measurements

* `python3 -m unittest infra.tests.test_edge_module -q`: 9 tests, OK (baseline, nothing reproduced as failing).
* `infra/modules/edge.bicep` emits `entraRedirectUri` from `hasDomain ? customDomain : endpoint.properties.hostName`;
  `infra/main.bicep` passes `edgeCustomDomain` through and re-exports it; `test_edge_module.py` lines 122-133 assert this.
* `infra/modules/network.bicep:76` keeps the AzureFrontDoor.Backend NSG rule.

## Criteria

* C1, C2, C4: ticked, anchors unchanged on main.
* C3: the static derivation of the callback from host is covered by existing tests. What remains is owner domain/DNS and edge go/no-go, managed TLS validation and actual Entra app registration URLs, none of which can be proven from the repository.
* C5: needs a production-profile deployment with Private Link to the internal Container Apps environment. This needs live Azure and is outside this brief.

## Decision

A further C3 test would restate the asserted derivation; a real fix touches infrastructure (FULL tier). No reproducible defect found, so no code change. Unmet: C3, C5.
