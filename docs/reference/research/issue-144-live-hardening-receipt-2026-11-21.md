---
title: Issue 144 live Container Apps hardening receipt (2026-11-21)
description: Live replica receipt that the current-tree agents image starts and stays healthy on Azure Container Apps under enforced hardening, with per-criterion status
ms.date: 2026-11-21
ms.topic: reference
---

## Scope

Synthetic demo, desktop only, resource group `ama`, 2026-11-21 06:27 to 06:40 UTC. Refs #144. No source change, no credential read, no change to the demo apps or the shared registry. Two throwaway resources were created and deleted: Basic registry `acr144throwrzsrg` and Container App `ca-144-hardening-probe` in `cae-cutover-test-demo`.

## Method

* The shared registry `crcutovertestrzsrg` is Premium with public access disabled. `az acr build` against it failed at registry login with 403 (run `dbv`), so no image could be published to it from this host. Changing its network posture is out of scope.
* On the throwaway Basic registry `az acr build` failed because the Dockerfile uses `RUN --mount` and ACR Tasks lacked BuildKit (run `db1`). The image was built locally with Docker from this tree (`src/agents/Dockerfile`, HEAD `0c497160e`) and pushed as digest `sha256:d5df701f1cc1648a1a40e72dc036ae1b9063c9b1aeea5b8390566cbe04d4a438`.
* The throwaway app used the Bicep hardening settings from `infra/modules/containerapps.bicep`: `ZF_CONTAINER_HARDENING=enforced`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp`, `ZF_STATE=/state`, EmptyDir volumes on `/tmp` and `/state`, one replica, command `python -m zava_forward.agents serve`.
* Registry credentials stayed in a shell variable and were never printed.

## Observations

| Check | Result |
| --- | --- |
| Without volumes, default command (version), enforced | Container exited 0 after printing `zava-forward-agents 0.1.0`. The guard runs before that output and refusal exits 2, so the guard passed. |
| With EmptyDir volumes, `serve`, enforced | Revision `0000001` `Healthy`, `RunningAtMaxScale`, 1 replica. Console: `serve: standby, queue consumption is off`. |
| Replica PID 1 `/proc/1/status` (via `az containerapp exec`) | `Uid` 10001, `CapInh` 0, `CapPrm` 0, `CapEff` 0, `CapAmb` 0, `CapBnd` `a80425fb`, `NoNewPrivs` 1. |
| Replica scratch directories | `/tmp` and `/state` are `root:root` 0777 EmptyDir mounts; `/tmp/zf` and `/state/zf` are 10001:10001 mode 0700. |
| Cleanup | App and registry deleted; `az acr list -g ama` shows only `crcutovertestrzsrg`; the three demo apps are untouched. |

This is the live receipt that the 2026-11-20 fix (commit `0c497160e`) resolves the Container Apps startup refusal: the pre-fix state was `CapInh` equal to `CapBnd` and a world-writable scratch directory, both refused. `CapBnd` stays non-zero as documented in the earlier note; with `NoNewPrivs` 1 and empty permitted, effective and ambient sets it cannot raise a capability.

## Live demo state (read-only)

* `ca-cutover-test-demo-agents`: `ZF_CONTAINER_HARDENING=enforced`, EmptyDir volumes present, revision `ht85blh` created 2026-11-20 19:09 UTC, but the image is the pre-fix digest `sha256:2217d94d...` and it is ScaledToZero, so it has never shown a replica under enforcement.
* `ca-cutover-test-demo-api` revision `0000038`: `ZF_CONTAINER_HARDENING=off`, 2 replicas, Healthy. `ca-resident-demo` revision `0000015`: variable unset. Both digest-pinned on the shared registry.
* `src-deploy.yml` has no runs.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Worker and job images are real, versioned and deployed through the pipeline | Unproven (real and immutable proven on 2026-11-19) | The release workflow has never run and pushing is forbidden, so pipeline deployment and tag versioning cannot be shown; the shared registry cannot be reached from this host to publish a fixed image |
| Container hardening is enforced in the deployed app, not only in CI | Partly proven | Proven: the current image runs Healthy on a Container Apps replica under the Bicep enforced settings, as uid 10001 with zero permitted, effective, inheritable and ambient sets. Unproven: the three demo apps themselves (agents runs the pre-fix image, api and resident have it off), because redeploying them needs an image on the shared registry |

## Follow-up

* Publish the fixed images to the shared registry through the pipeline (or an owner-run registry network exception), then roll `ca-cutover-test-demo-agents` and record a replica receipt on it.
