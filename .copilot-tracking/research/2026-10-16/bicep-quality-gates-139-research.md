---
title: Bicep quality gates 139 research
description: Bounded offline infrastructure gate evidence
ms.date: 2026-10-16
---

## Brief and direction

Task #139, slug `bicep-quality-gates-139`. Focused internal convergence research
for an offline implementation. No deployment, pipeline #138, private datasets,
environment files or check renames. Caller explicitly requests implementation,
RPI evidence, local validation, commit, push and PR using Refs #139.
Research disposition: executed. Planning Readiness: Ready.

Repository instructions and RPI research selected; no domain research specialist
needed for this tightly coupled trace. No external sources or Azure access.
Caller inputs suffice; no unresolved intake decision.

## Cycle 1

### Wider

* C1 `infra/bicepconfig.json:1`: an existing error-level linter configuration
  already covers relevant secrets, identifiers and unused declarations.
* C2 `infra/tests/test_bicep_policy.py:1`: compiled-template assertions already
  exist. The issue description predates that work; extend rather than replace it.
* C3 `.github/workflows/mvp-validation.yml:1` and
  `.github/workflows/src-ci.yml:1`: old validation job runs infra tests, while
  source CI does not trigger on infra changes. Keep all job/check names.

### Deeper

* C4 `infra/main.bicep:108`: production/public and purge combinations already
  have a named minLength guard; dependent modules wait directly or transitively.
* C5 `infra/modules/storage.bicep:8`: audit retention lacks the positive lower
  bound already present for digest retention. Small safe decorator fix.
* C6 `infra/tests/test_bicep_policy.py:188`: immutability assertion counts
  policies without proving their target containers or positive retention.
  Endpoint assertion aggregates group names without proving service ownership,
  actual endpoint resources, connection or DNS. No mutation coverage.

### Contrarian

* C7 `infra/modules/storage.bicep:8`: policies deliberately start unlocked;
  offline tests cannot claim locked WORM, legal retention or Azure acceptance.
* C8 `infra/modules/authTokenStore.bicep:1`: optional template must remain
  checked even when disabled by default. IoT and Log Analytics local auth also
  need explicit assertions rather than a generic no-keys claim.
* C9 `infra/README.md:760`: Front Door/private origin remains unverified.
  Compiled JSON cannot replace live network verification or ARM validation.
* Baseline: Bicep 0.48.1 builds successfully. Infra tests fail only because
  installed source distributions are absent; restore using pip in an isolated
  venv, not PYTHONPATH workarounds.

## Synthesis and handoff

Accept reuse of linter configuration and guard design; strengthen exact compiled
control assertions and prove sensitivity with in-memory mutations. Cover each
service rather than global counts. Add source-CI gates inside existing namespace
job and retain the legacy validation gate. Reject a new policy engine,
deployment workflow or Azure calls as unnecessary/out of scope. No further
research cycle is needed: named source evidence covers the bounded questions.
Residual live validation and irreversible policy locking remain owner work.
