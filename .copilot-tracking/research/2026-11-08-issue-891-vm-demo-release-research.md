---
title: Issue 891 VM demo release and live verification research
description: Evidence for the owner-authorised VM release of the demo API and guarded live check
ms.date: 2026-11-08
---

## Disposition

Research executed (read-only). Planning Readiness: Ready, with one named gap (live browser sign-in runner).

## Identities (2026-11-08)

* Worktree `issue-891-vm-live`, branch `chore/demo-vm-release-891`, HEAD = fetched `origin/main` = `e2ecee2565e86889c6beb43cb32e7c5b54270e01`. Report commits go only on this branch; deployment source is pinned main.
* Live `ca-cutover-test-demo-api` revision `--0000026`, image `crcutovertestrzsrg.azurecr.io/zava-forward-api:1f465bf5e` (rollback reference; deployed 2026-11-04/05). Source delta since that image: 13 commits under src api/core/agents, including #1245 (disclaimer placement and gate test).
* ACR `crcutovertestrzsrg`: public access Disabled, exports disabled, no IP rules (baseline to restore and read back).
* Hosted Source projects CI: no run exists for main `e2ecee25`; PR runs passed for earlier heads. `src-ci.yml` has `workflow_dispatch`, so the legitimate manual run is needed. `src-deploy.yml` deploy job needs a self-hosted `ama-private-deploy` runner that does not exist (owner decision, issue #891 comment 6723702746), so the VM route replaces only that job.

## Existing route (infra/README.md, entries 2026-11-03, 11-04 and 11-05)

* Local `docker build -f src/api/Dockerfile src`, short registry window (`az acr update` export policy, public access on, one IP rule; trap removes rule by bare IP, disables public access and exports; readback Disabled, Deny, no rules), `docker push`, one `az containerapp update` setting the image (env demo switch already present: `ZF_CHAT_DEMO_ACTIVATION=approved-2026-11-03`, `ZF_DEPLOYMENT_PROFILE=demo`). `az acr build` does not work.
* Release workflow equivalents to run locally: `src/check-container.py api <image>`, Trivy v0.76.0 gate (`src/trivy.yaml`, HIGH/CRITICAL fixable), report scan, SPDX SBOM. Trivy is installed.
* Pipeline `publish` pushes a tar by digest; reusing it needs `AZURE_PUBLISH_*` OIDC and is not required; the README manual recipe is the reviewed VM route.

## Resources

Root 17 GiB free, /mnt 4.2 GiB (no heavy output on /mnt). Heavy lock `/tmp/ama-rpi-heavy.lock` free at check (lsof empty); hold it with `flock -n` for the image build and scan only. Docker 29.9.0.

## Live verification inputs and gap

* Three owner-supplied credential files exist (not read). Maintained identity procedure (src/api/README.md): independently verify expected tid/oid from Entra, never from `/api/me`; strict predicate at navigation boundaries (`checks.employee_acceptance_check.verify_employee`). The maintained operator entry `employee_live_acceptance.py` expects a manual sign-in over loopback CDP; no committed credential-reading runner exists. Earlier two employee attempt slots are consumed and immutable.
* Gap: automated form sign-in needs an uncommitted, in-memory runner reading the files; Entra may require MFA or consent that blocks it. If expected oid cannot be resolved independently, stop and record.

## Decisions

* Deploy the demo API only; do not redeploy the resident app, agents or infrastructure.
* Keep existing env; no new env, no Bicep. Provenance is judged from the response receipt, not from health or flags.
