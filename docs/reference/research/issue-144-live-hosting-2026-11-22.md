---
title: Issue 144 live container hosting probe
description: Read-only Azure evidence for the two unticked criteria of issue 144, with proven and unproven status
ms.date: 2026-11-22
---

Scope: synthetic demo, desktop only, resource group `ama`, read-only `az` calls plus `az containerapp exec` running `id`, `touch /usr/x`, `/proc/self/status` and `/proc/mounts` reads. No Azure change, no throwaway resource. No credential value was read. Refs #144.

## Findings

* Five container workloads run in `cae-cutover-test-demo`: apps `ca-cutover-test-demo-api` (revision 0000053), `ca-resident-demo` (0000025), `ca-cutover-test-demo-agents` (0000003), and jobs `job-cutover-test-demo-load`, `-audit`, `-orch`, `job-live-simulator`, `job-live-receiver`. Revision mode is `Single`.
* Every app and job image is a registry reference pinned by `sha256` digest in `crcutovertestrzsrg.azurecr.io` (api, resident-demo, agents, importer, orchestrator repositories). The importer and orchestrator jobs run `python -m zava_forward.importer` and `python -m zava_forward.orchestrator` commands, so they are not placeholder images.
* Runtime inside the API and resident demo replicas: `uid=10001(app)`, `/usr` not writable, effective capability set `0000000000000000`. The agents app has minReplicas 0 and no replica was running, so its user could not be read.
* The root file system is mounted `overlay ... rw`, `NoNewPrivs` is 0 and the capability bounding set is `00000000a80425fb`. The container spec returns `securityContext: null` for all apps and jobs, and `infra/modules/containerapps.bicep` sets none.
* `gh run list --workflow src-deploy.yml` returns no runs. The pipeline file defines build, scan, SBOM, publish and deploy steps, but no run exists that produced the deployed digests.
* Registry tags and manifests could not be listed: the data plane returned `connectivity_forbidden`. Opening the registry firewall is an Azure change and was not made.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Worker and job images are real, versioned and deployed through the pipeline | Unproven | Real digest-pinned images with module commands are deployed, but zero `src-deploy.yml` runs exist and registry tags were not readable, so pipeline origin and version tags are not shown. |
| Container hardening (non-root, read-only file system, dropped capabilities) enforced in the deployed app | Partly proven | Non-root and no effective capabilities proven live for api and resident-demo. Read-only root file system is disproved (`rw`), capabilities are not dropped from the bounding set, and the Container Apps spec exposes no `securityContext`. Needs a platform feature or an accepted exception. |

The three ticked criteria in the issue are not re-proven here.

## Limits

Single read on 2026-11-22. The agents replica user is unread. No source change, so the focused tier applies.
