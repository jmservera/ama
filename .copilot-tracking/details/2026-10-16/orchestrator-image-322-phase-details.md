---
title: Orchestrator image resolution phase details
description: Implementation boundaries and evidence for issue 322
ms.date: 2026-10-16
---

Task #322; slug orchestrator-image-322. No blockers.

<!-- rpi:phase id=P01 -->
## P01: Implementation

<!-- rpi:task id=P01-T01 -->
### P01-T01: Bicep and resolver

main.bicep currently defaults directly to quickstart and forwards that value.
Use an empty default and a conditional module argument. The containerapps
module's three image consumers remain unchanged.

No deployment script exists. Add infra/scripts/deploy.py with az subprocesses,
explicit resource-group/registry/environment scope and what-if default.
List jobs within the group, select only exact target job names, and retain
any unique real image. Multiple different real images require explicit input.
Only confirmed registry/repository absence or no tags may fall back; registry
and repository list calls distinguish absence without parsing CLI error text.
Authorization, networking and malformed output fail before deploy.
Always print the source and final image, including an explicit placeholder
warning. Forward normal parameters while protecting lookup identity parameters.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Tests

Fake az is a temporary executable on PATH driven by JSON expectations and
capturing calls; execute the actual deploy CLI, not just mocked Python helpers.
Test read call order and no deployment on failure, plus final image argument.
Reuse compiled Bicep helpers/evaluator for default, empty, tag and digest values,
and keep the existing job command/image assertions.

<!-- rpi:phase id=P02 -->
## P02: Evidence and delivery

<!-- rpi:task id=P02-T01 -->
### P02-T01: Validation and documentation

Run infra unittest suite with local Bicep compilation. Use a disposable pip
venv for Ruff and mypy of changed Python. Mutate temporary copies or in-memory
compiled templates; never change private data or invoke real Azure.
Update README deployment examples to use the resolver and explain raw-Bicep
empty semantics. Append the KB log and add an index routing pointer.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Review and publication

Record one post-implementation RPI Review. Verify authenticated identity and
set repository-local privacy-safe author/committer email, include required
Copilot trailer, push normally and create a main-targeting PR with Refs #322.
Hosted checks and owner merge remain separate from local acceptance.
