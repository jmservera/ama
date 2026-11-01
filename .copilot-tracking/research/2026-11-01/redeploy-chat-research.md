---
title: Redeploy chat changes from main 398e846fd, research
ms.date: 2026-11-01
---

Task `redeploy-chat`, mode manual-full-loop by owner request, Research disposition `executed`, Planning Readiness `Ready`.

## Scope

Deploy origin/main `398e846fd8ed508c8618c2d72d3479020e3221b1` (includes #741, #743, #744, #745) to `ca-resident-demo`, `ca-cutover-test-demo-api`, `ca-cutover-test-api` and `ca-cutover-test-agents` in RG `ama`, then run live checks.

## Evidence

* Live baseline: min replicas 0 on all four apps, eight jobs Manual, five `CHAT_*` variables present on resident and demo API, absent on `ca-cutover-test-api` (`redeploy-chat-2026-11-01/pre-deploy-config-sanitized.json`).
* Registry `crcutovertestrzsrg` is Premium with public access disabled; the established owner procedure is a short IP-only window with exports enabled and an exact restore (`.copilot-tracking/changes/2026-10-26/resident-release-462-changes.md`, `.copilot-tracking/changes/2026-10-31/demo-sites-redeploy-routing-changes.md`).
* Resident image: `src/api/Dockerfile.resident-demo`; employee image: `src/api/Dockerfile` (shared by demo API and `ca-cutover-test-api`); agents: `src/agents/Dockerfile`; deploy helper `infra/scripts/resident_demo_deploy.py` (what-if gate, typed confirmation, needs a TTY).
* Employee username for the Entra sign-in is recorded in earlier tracking files; the credential files were read only inside automation.
* The "sensors live view" exists only in the resident app ("Your home sensors"); the employee SPA has no sensor page.

## Risks

* `ca-cutover-test-api` is internal to the private environment, so no public health probe is possible; revision health state is the signal.
* #743 grounds only `/api/chat/unstored-ask`; #745 enabled stored chat, which may bypass it (confirmed live, issue #749).
