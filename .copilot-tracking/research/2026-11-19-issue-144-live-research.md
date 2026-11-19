# Issue 144 live research (2026-11-19)

Status: opened. Scope: synthetic demo, desktop only, read-only Azure queries in resource group ama.

## Unticked criteria at open

* Worker and job images are real, versioned and deployed through the pipeline (first unmet; chosen)
* Container hardening enforced in the deployed app, not only in CI

## Initial observations

* ACR crcutovertestrzsrg: publicNetworkAccess Disabled, Premium; tag listing from this host is refused.
* `gh run list --workflow src-deploy.yml` returns no runs.

## Live evidence (read-only `az containerapp list|job list|revision list -g ama`, 2026-11-19 00:03 UTC, no secrets)

Apps (registry crcutovertestrzsrg.azurecr.io, all digest-pinned, none a quickstart placeholder):

| Resource | Repository | Digest prefix |
| --- | --- | --- |
| ca-cutover-test-api | zava-forward-api | sha256:161fa1f0ff29 |
| ca-cutover-test-agents | zava-forward-agents | sha256:2217d94d1c23 |
| ca-cutover-test-demo-api | zava-forward-api | sha256:5368f4e4009c (revision 0000033, Single mode, 0..4 replicas) |
| ca-resident-demo | zava-resident-demo | sha256:65481780cb3f |

Jobs (8): init, verify, smoke and mi-http use zava-forward-cutover-proof sha256:ef0058f8f380; ledger-verify and orchestrator use zava-forward-orchestrator sha256:e3b290bfa2af; import uses zava-forward-importer sha256:51b6a480bd7e; public-audit uses zava-forward-api sha256:111b26226cad.

## Per-criterion proof status

| Criterion | Status | Basis |
| --- | --- | --- |
| Worker and job images real, versioned, deployed through the pipeline | Real and immutable: proven live. Versioned tags and pipeline provenance: unproven | Digest-pinned refs above. ACR has public network access disabled so tags cannot be listed from this host; `src-deploy.yml` has zero workflow runs (`gh run list`), and its publish and deploy jobs need the private self-hosted runners and protected environments. Live images were therefore published outside that pipeline. |
| Container hardening enforced in the deployed app | Unproven live, adverse evidence | No deployed app or job carries `ZF_CONTAINER_HARDENING`, `PYTHONDONTWRITEBYTECODE` or scratch volumes; deployed images predate the hardened Bicep. ARM `securityContext` is also unsupported on Container Apps 2025-07-01 (infra/README.md). A redeploy is out of scope for this read-only task (no production changes). |

## Planning readiness

Ready. Gap chosen: no executable check classifies deployed image references; the first criterion rests on prose. Plan a read-only offline-testable audit script that classifies `az containerapp|job list` JSON (placeholder, tag-only, `:latest`, foreign registry, digest-pinned) so the live evidence is reproducible.
