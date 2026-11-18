---
title: Container hosting live evidence for issue 144 (demo)
description: Recorded run on 2026-11-18 against the live Azure demo showing deployed image identity, deployed container hardening, scale-out under a short load test and revision state
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 144
  - container apps
  - hardening
  - scale rules
  - load test
estimated_reading_time: 6
---

Refs #144. Scope is the synthetic desktop demo in resource group `ama`, authorised by the owner on 2026-11-18 (cap USD 700, no drills, no Key Vault rotation, no production changes). Nothing here is production, pilot or resident evidence, and nothing proves the 60,000-home fixture.

## Method

* Read-only `az containerapp show/list` and `az containerapp job list` against `ca-cutover-test-demo-api`, `ca-resident-demo`, `ca-cutover-test-agents` and the nine `job-*` resources.
* One interactive `az containerapp exec` session into replica `ca-cutover-test-demo-api--0000031-84949d7db9-8v5j4` (container `api`) running `id`, `/proc/self/status`, `touch` and `/proc/mounts` probes. The `touch` probes may have left an empty file in `/tmp` of the replica; it was not removed, and the container file system is ephemeral (a replica restart discards it).
* One load run from this host (the script is not shipped): 150 concurrent clients for 60 s, `GET /healthz` on the demo API, 08:26:28Z to 08:27:28Z. No inference, no SQL write path and no credentials were used. Estimated Azure cost is well under USD 1 (a few vCPU-minutes of Container Apps consumption plus egress), far below the USD 20 cap.
* No Azure resource was created, so there is nothing to delete.

## Per-criterion result

| Criterion in #144 | Result | Evidence |
| --- | --- | --- |
| Worker and job images are real, versioned and deployed through the pipeline | Partly proven; the pipeline clause is unproven | Real: every app and job runs a digest-pinned image from `crcutovertestrzsrg.azurecr.io` (`zava-forward-api`, `-agents`, `-orchestrator`, `-importer`, `-cutover-proof`, `zava-resident-demo`); no resource runs `mcr.microsoft.com/k8se/quickstart`. Versioned: immutable `@sha256` references; the demo API is on revision `--0000031` of 52 recorded. Pipeline: `gh run list --workflow src-deploy.yml` returns no runs, and the workflow needs `ama-private-release` and `ama-private-deploy` self-hosted runners, protected environments and OIDC, so the demo digests were not produced by it. The registry is private (`publicNetworkAccess` Disabled, Premium), so tags could not be listed from this host to match digests to a run-versioned tag. |
| Scale rules, probes, resource limits and revision rollback are defined and tested (ticked) | Re-observed | Demo API: min 0, max 4, HTTP rule at 50 concurrent requests, 0.5 vCPU, 1 Gi, liveness, readiness and startup probes on `/healthz:8088`. Agents: queue rule `agent-task-queue`, queueLength 5, max 5. The load run below scaled the API from 0 to 4 replicas. |
| Container hardening (non-root, read-only file system, dropped capabilities) enforced in the deployed app | Non-root proven; read-only file system and dropped capabilities not enforceable on this platform | See the runtime table below. |
| Load test against the declared scale fixture is recorded without claiming production scale (ticked) | Re-observed at demo scale only | 15,819 requests, 263.6 requests per second, all HTTP 200, p50 0.612 s, p95 1.310 s, p99 2.293 s, max 4.628 s; replicas 0 to 4 (the declared maximum); active revision unchanged. This is a health-endpoint run, not the 60,000-home fixture. |
| Single-replica and restart behaviour verified with audit persistence (ticked) | Not re-run | Restarts and audit-persistence drills are excluded by the owner for this run. |
| Tokenomics: usage and cost drivers per unit of load (ticked) | Partly re-observed | Per-unit drivers from this run: 15,819 requests, 0 assistant calls, 0 SQL writes, up to 4 replicas for about 60 s plus the 300 s cooldown. No price source is set, so cost per unit stays Unknown. |

## Deployed runtime hardening (replica probe)

| Probe | Observed | Reading |
| --- | --- | --- |
| `id` | `uid=10001(app) gid=10001(app)` | Non-root, matches `USER 10001:10001` in `src/api/Dockerfile`. Proven in the deployed replica. |
| `CapEff` | `0000000000000000` | No effective capabilities for the non-root process. |
| `CapBnd` | `00000000a80425fb` | The bounding set is the runtime default, not empty, so `--cap-drop ALL` is not applied. |
| `NoNewPrivs` | `0` | `no-new-privileges` is not applied. |
| `touch /usr/zz` | `Permission denied` | Blocked by file permissions for a non-root user, not by a read-only mount. |
| `touch /tmp/zz` | succeeded | Writable `/tmp`. |
| `/proc/mounts` for `/` | `overlay / overlay rw,...` | Root file system is mounted read-write. |
| `securityContext` in the deployed template | `None` for all three apps | Nothing in `infra/modules/containerapps.bicep` sets one. The Microsoft.App ContainerApps schema `2025-07-01` (stable) and `2025-02-02-preview` define no `securityContext`, so the read-only root file system and capability drop cannot be declared there. Schemas newer than those two were not found or checked. |

CI enforces `--read-only --cap-drop ALL --security-opt no-new-privileges` for the image (`.github/workflows/mvp-ci.yml`), but that does not carry into the deployed app. The criterion stays unticked: non-root is real in the demo, the other two controls are not enforced in Container Apps.

## What this does not prove

* No run of `src-deploy.yml`, so "deployed through the pipeline" is not shown, and no private-registry tag listing was possible.
* The load run exercised only `/healthz`; it says nothing about authenticated paths, SQL, assistants or the 60,000-home fixture, and no production profile was used.
* The three-job and worker images (`-orchestrator`, `-importer`) were inspected by reference only; no job execution or exec probe was run on them.
* Restart and audit-persistence behaviour were not re-run.
* No Playwright proof applies: the criteria concern container hosting, not a web page.

## Second run, 2026-11-18 (issue-144-live, rpi-144-live)

Repeated read-only probes against resource group `ama`; no Azure resource was created, changed or deleted, no load was generated, and no credentials were used. One interactive `az containerapp exec` session ran in the live demo API replica (`id`, `/proc/self/status`, `/proc/mounts`, and `touch` in `/usr` and `/tmp`). The `/usr` write was denied; a `/tmp/zz` file may remain until the replica is replaced. The exec session is a live action on the demo replica, not a read-only call.

| Probe | Result | Reading |
| --- | --- | --- |
| `az containerapp job list -g ama` | 8 jobs, all on digest-pinned `crcutovertestrzsrg.azurecr.io` images (`-orchestrator`, `-importer`, `-api`, `-cutover-proof`) | Images are real and immutable by digest. |
| `gh run list --workflow src-deploy.yml` | No runs | "Deployed through the pipeline" remains unproven. |
| `az acr repository show-tags` | Refused: registry is private (`publicNetworkAccess` Disabled, Premium) | Digests cannot be matched to versioned tags from this host. The firewall was not changed. |
| `az containerapp exec` into the demo API replica (revision `--0000031`) | `uid=10001(app)`, `CapEff` all zero, `NoNewPrivs: 0`, `/` mounted `overlay rw`, `/usr` write denied by permission, `/tmp` writable | Non-root is real. The root file system is writable, so read-only is not enforced. `NoNewPrivs: 0` is read here as the runtime privilege lock not being active (interpretation). |
| `ZF_CONTAINER_HARDENING` on the API, agents, resident-demo apps and the orchestrator and import jobs | Not set on any of them, and the demo API has no `EmptyDir` volumes | Adverse: the deployed revisions predate or lack the in-process hardening that main's Bicep and `infra/tests/test_container_hosting_144.py` describe, so that control is not live in the demo. |
| `securityContext` in the deployed template | `null` | Platform-level rootfs and capability controls remain undeclarable. |

Per-criterion status after this run: criterion 1 unproven (pipeline clause; images are real and digest-versioned), criterion 3 unproven (non-root only; read-only file system, capability drop and in-process hardening not live). Fixing criterion 3 means redeploying a revision built from current main, which is a deployment change outside the owner's demo authorisation for this task.

## Evidence limits

* The raw output of the exec session (`id`, `CapEff`, `NoNewPrivs`, `/proc/mounts`), the job list and the environment variable checks was not retained. Those second-run rows are "Observed; raw output not retained".
* Job count: the first run counts nine `job-*` resources and the second run lists 8 jobs. The difference was not reconciled and no raw list exists to settle it. Three apps were examined: `ca-cutover-test-demo-api`, `ca-resident-demo` and `ca-cutover-test-agents`.
