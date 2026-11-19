---
title: Deployed image audit for issue 144 container hosting
description: Live read-only evidence that deployed Container Apps and Jobs use real digest-pinned images, plus a new offline audit script; pipeline provenance and deployed hardening stay unproven
author: AMA RPI agent
ms.date: 2026-11-19
ms.topic: reference
keywords:
  - issue 144
  - container images
  - digest
---

Scope: synthetic demo, desktop only, resource group `ama`, read-only Azure queries on 2026-11-19 00:03 UTC. No secret was read and no Azure resource was created, changed or deleted.

## Method

* `az containerapp list -g ama -o json` and `az containerapp job list -g ama -o json`, piped to the new `infra/scripts/deployed_images.py --registry crcutovertestrzsrg.azurecr.io`.
* `az acr show` for the registry network posture; `gh run list --workflow src-deploy.yml` for pipeline runs.
* Unit tests: `python3 -m unittest infra/tests/test_deployed_images.py` (3 tests, OK); `ruff check` and `ruff format --isolated --line-length 100 --check` clean.

## Observations

* The tool classified 12 containers (4 apps, 8 jobs) as `digest-pinned` on the expected registry; none is a quickstart placeholder, tag-only or `:latest` reference. Repositories: `zava-forward-api`, `zava-forward-agents`, `zava-forward-orchestrator`, `zava-forward-importer`, `zava-forward-cutover-proof`, `zava-resident-demo`.
* `ca-cutover-test-demo-api` runs revision `0000033` in Single revision mode with 0 to 4 replicas.
* The registry is Premium with public network access disabled, so tag listing is refused from this host.
* `src-deploy.yml` has no workflow runs.
* No deployed app or job carries `ZF_CONTAINER_HARDENING`, `PYTHONDONTWRITEBYTECODE` or EmptyDir scratch volumes.

## Per-criterion proof status

| Criterion | Status | Basis |
| --- | --- | --- |
| Worker and job images are real, versioned and deployed through the pipeline | Partly proven: real and immutable live. Tag versioning and pipeline deployment unproven | Digests above. Tags cannot be listed (private registry) and the release workflow has never run, so the live images were not published by it. Proving it needs the self-hosted runners and protected environments, which the demo does not use. |
| Container hardening is enforced in the deployed app, not only in CI | Unproven, adverse live evidence | Deployed specs lack the hardening settings, so the running images predate the hardened Bicep. Redeploying is a production change outside this task. Container Apps ARM also lacks `securityContext`. |

The ticked criteria are untouched by this note. Original evidence in `infra/README.md` and the earlier scale records is preserved.
