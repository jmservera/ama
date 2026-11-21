---
title: Issue 144 live registry import probe (2026-11-21)
description: Live attempt to publish the current-tree agents image to the shared registry by control-plane import, with the denial recorded and per-criterion status
ms.date: 2026-11-21
ms.topic: reference
---

## Scope

Synthetic demo, desktop only, resource group `ama`, 2026-11-21 08:17 to 08:25 UTC. Refs #144. No source change, no credential read, no change to the demo apps or the shared registry. Follows the [06:27 hardening receipt](issue-144-live-hardening-receipt-2026-11-21.md), whose open follow-up was to get the fixed image onto the shared registry.

## Method and observations

| Step | Result |
| --- | --- |
| Live read of demo state | `ca-cutover-test-demo-agents` still on the pre-fix digest `sha256:2217d94d...`, minimum replicas 0, revision `ht85blh`. Shared registry `crcutovertestrzsrg` is Premium, public network access Disabled. `gh run list --workflow src-deploy.yml` returns no runs. |
| Build | `docker build -f src/agents/Dockerfile src` at HEAD `981aa6aaf` succeeded locally (image id `sha256:95c74d41d496...`). |
| Stage | Created throwaway Basic registry `acr144throw2rzsrg` with admin enabled; pushed the image there (digest `sha256:95c74d41d49615ffa100450da0550c78a31ec7c2dc7042cb4504c2be63cc0909`). Credentials stayed in a shell variable. |
| `az acr import` into the shared registry | First attempt: `InvalidHostName` (source name not yet resolvable). Retry after 30 s: `InvalidParameters`, "Access to crcutovertestrzsrg.azurecr.io denied due to network restrictions" (trusted-services bypass does not admit the import). |
| Direct tag listing on the shared registry | Refused with the same network-restriction error. |
| Cleanup | Throwaway registry deleted; `az acr list -g ama` shows only `crcutovertestrzsrg`; local tags removed. |

Conclusion: the shared registry cannot receive an image from this host by push (earlier 403), by ACR Tasks (earlier) or by control-plane import (now). Opening it needs an owner network exception, which is outside this demo's authority, so the three demo apps could not be rolled to the fixed image and no replica receipt exists on them.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Worker and job images are real, versioned and deployed through the pipeline | Unproven | Real and digest-pinned proven earlier (2026-11-19); `src-deploy.yml` has no runs and pushing is forbidden; publishing to the shared registry is blocked by its network posture, now confirmed for import as well |
| Container hardening is enforced in the deployed app, not only in CI | Partly proven | Proven on a throwaway replica of the current image (06:27 receipt). Unproven on the demo apps: agents runs the pre-fix image, api revision `0000038` has `ZF_CONTAINER_HARDENING=off`, resident has it unset |

The three ticked criteria are unchanged and nothing is ticked here.

## Follow-up

* Owner decision needed: either run `src-deploy.yml` from a merged branch, or allow a temporary registry network exception (or a runner inside the private network), then roll `ca-cutover-test-demo-agents` and record a replica receipt.
