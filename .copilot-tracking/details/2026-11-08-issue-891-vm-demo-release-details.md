---
title: Issue 891 VM demo release details
description: Phase details and outcomes for the VM release of main e2ecee25 to the test demo API
ms.date: 2026-11-08
---

## Phase outcomes

* Phase 1 done. Source projects CI run 42497999337 (workflow_dispatch, main, head `e2ecee25`) completed success, all jobs green. No prior failed run for this head.
* Phase 2 done. Clean `git archive` of `e2ecee25` (tree `b8b48536a786dab0b46010b84d0bec6fdd523078`), built under `flock -n /tmp/ama-rpi-heavy.lock`. Image id `sha256:1605ca20f06598e62441c2894e4c34b554c31bdd9b1e1e88103d3bc3bcca0f64`. `check-container.py api` PASS; Trivy 0.76.0 gate (HIGH/CRITICAL fixable) exit 0, clean; SPDX SBOM written.
* Phase 3 done. Pre-mutation revalidation: no drift (main unchanged, app on `--0000026`, 100 percent traffic, ACR Disabled/Deny/no rules/exports disabled). Window opened, one IP rule, pushed tag `e2ecee25c`, digest `sha256:1605ca20f06598e62441c2894e4c34b554c31bdd9b1e1e88103d3bc3bcca0f64`, window closed and read back Disabled, Deny, no rules, exports disabled BEFORE the app update. Rollback digest of `1f465bf5e` is `sha256:bf7d604510f04347d3344c62c4b487211b489284fa6c5db6ec2c7b85142dcb8f`.
* Phase 4 done. One `az containerapp update` by digest. Revision `--0000027` Running, Healthy, 100 percent; `--0000026` deprovisioning. Env variable names identical before and after (39). No values printed.
* Phase 5 partial. `/healthz` 200 after warm; unauthenticated `/api/chat/status` 401 (Easy Auth intact). Independent Entra resolution of the expected object id failed (`az ad user show` insufficient privileges; signed-in identity is not a delegated user), so no sign-in was attempted. Resident app not redeployed and not smoked.
* Phase 6: records, issue comment, commit (no push).

## Evidence

Retained outside the repository in `/home/azureuser/evidence-891-vm-1108` (SBOM, scan and startup output, env names, digests).
