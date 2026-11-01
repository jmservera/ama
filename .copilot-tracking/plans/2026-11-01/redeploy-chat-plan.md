---
title: Redeploy chat changes from main 398e846fd, plan
ms.date: 2026-11-01
---

Critique: one final-candidate critique executed inline by the parent; verdict Proceed; no conflicts with the owner's constraints. Compatible finding applied: the registry window is the only way to publish to the private registry and must use the standing IP-only, exact-restore procedure.

## Phases

1. [x] Back up each app's full configuration (0600, session folder) plus a sanitized copy without secret values.
2. [x] Build resident, employee and agents images from a `git archive` of origin/main under `flock /tmp/ama-rpi-heavy.lock`.
3. [x] Push in one IP-only registry window; restore and compare the full registry configuration.
4. [x] Resident: `resident_demo_deploy.py` what-if then `--apply` (typed confirmation).
5. [x] Demo API, API and agents: `az containerapp update --image <digest>`; API and demo API also set the five `CHAT_*` variables with identical values.
6. [x] Health and configuration diff; roll back a revision only if health fails.
7. [x] Live Playwright checks; bug issues for failures.
8. [x] Remove own images by exact tag; commit evidence; push topic branch; open PR with `Refs` only.

## Constraints kept

Min replicas 0, eight jobs Manual, no RG deletion, no private endpoint, public network or RBAC change (registry restored identical), five `CHAT_*` variables preserved or applied, secrets never printed.
