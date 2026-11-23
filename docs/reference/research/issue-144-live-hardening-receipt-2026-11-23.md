---
title: Issue 144 live hardening receipt on revision 0000055
description: Read-only Azure and replica evidence for the two unticked criteria of issue 144, with proven and unproven status
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only, resource group `ama`. Read-only `az` list calls and `az containerapp exec` into the API replica running `id`, `touch /usr/x`, `ls -ld` and reads of `/proc/1/status` and `/proc/mounts`. No Azure change, no throwaway resource, no credential value read. Refs #144. Retrieved 2026-11-23.

## Change since 2026-11-22

On 2026-11-20 the live API revision ran with `ZF_CONTAINER_HARDENING=off`. On 2026-11-23 every container app and job in `ama` carries `ZF_CONTAINER_HARDENING=enforced`: `ca-cutover-test-demo-api` (revision 0000055), `ca-resident-demo` (0000028), `ca-cutover-test-demo-agents` (0000003) and the five jobs. `securityContext` is still null everywhere.

## Replica receipt (ca-cutover-test-demo-api, replica 8n5x9, PID 1 `python -m zava_forward.api`)

| Field | Value |
| --- | --- |
| Uid | 10001 (user `app`) |
| NoNewPrivs | 1 |
| CapInh, CapPrm, CapEff, CapAmb | all `0000000000000000` |
| CapBnd | `00000000a80425fb` (not droppable on Container Apps; inert with NoNewPrivs and empty permitted set) |
| `/tmp/zf` and `/state/zf` | mode `0700`, owner `app` (created by `prepare_private_scratch`) |
| Root file system | `overlay ... rw` |
| `touch /usr/x` | Permission denied |

A separate `az containerapp exec` shell reports `CapInh` equal to `CapBnd` and `NoNewPrivs` 0; that is the exec session, not the application process. The guard ran in PID 1, which is the process that matters.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Worker and job images real, versioned, deployed through the pipeline | Unproven | Digest-pinned images in `crcutovertestrzsrg.azurecr.io` with module commands are deployed (see `issue-144-live-hosting-2026-11-22.md`), but `src-deploy.yml` has no run and registry tags are unreadable from this host; pipeline origin cannot be shown without an Azure change. |
| Container hardening enforced in the deployed app | Proven except read-only root | Guard enforced on every app and job spec; the live application process is non-root, NoNewPrivs 1, with empty inheritable, permitted, effective and ambient sets. Read-only root file system is not provable: the mount is `rw` and the platform has no setting for it. Needs an accepted exception from the owner. |

The three ticked criteria are not re-proven. `infra/scripts/deployed_hardening.py` and its tests make the receipt check repeatable from saved output.
