---
title: Issue 144 live hardening re-probe
description: Live replica receipt checked by an offline verifier for the two unticked criteria of issue 144
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only, resource group `ama`. Read-only `az containerapp list`, `az containerapp job list` and `az containerapp exec` running `cat /proc/1/status` and `cat /proc/mounts` (exec needs a pseudo-terminal, supplied with `script`). No Azure change, no throwaway resource, no credential read. Refs #144.

## Method

The new offline verifier `infra/scripts/deployed_hardening.py` (tests in `infra/tests/test_deployed_hardening.py`) reads the saved JSON and process status. `infra/scripts/deployed_images.py` classified image references.

## Findings

* Specs: 8 containers across the apps and jobs in the group all set `ZF_CONTAINER_HARDENING=enforced` (`all_enforced: true`).
* Image references: 8 of 8 are digest-pinned in `crcutovertestrzsrg.azurecr.io` (`all_real_and_immutable: true`).
* Live `ca-cutover-test-demo-api` process 1: uid 10001, `NoNewPrivs: 1`, inheritable, permitted, effective and ambient capability sets all zero (`all_passed: true`). The bounding set is `00000000a80425fb`, so capabilities are not dropped from it. `ca-resident-demo` passes the same status checks.
* Root file system: `overlay / ... rw` (`read_only: false`). Container Apps exposes no `readOnlyRootFilesystem` or `securityContext`.
* `src-deploy.yml` has 0 workflow runs (`gh api .../runs` total_count 0).
* Earlier note [2026-11-22](./issue-144-live-hosting-2026-11-22.md) read `NoNewPrivs` 0; today it is 1, consistent with the guard now running under `enforced`.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Images real, versioned, deployed through the pipeline | Unproven | Real digest-pinned images, but no pipeline run exists and registry tags were not readable. Protected runners and OIDC are outside the demo authorisation. |
| Hardening enforced in the deployed app | Partly proven | Non-root, `NoNewPrivs` and empty effective capabilities proven live; read-only root disproved and bounding set not dropped, a platform limit. |
