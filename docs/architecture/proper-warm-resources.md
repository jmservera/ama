---
title: Proper Warm PoC Resource and Validation Ledger
description: Actual created artefacts, local runtime resources and safe teardown
ms.date: 2026-10-08
ms.topic: reference
---

## Ownership and Scope

This ledger belongs to the 2026-10-07 Proper Warm architecture/PoC task.
No cloud or tenant creation is necessary for this local synthetic implementation.
Permission to create resources has not been mistaken for a need to create them.

The 2026-10-08 architecture update specifies a concrete Azure PoC deployment
design: Container Apps, Azure SQL, registry, managed identities, Foundry
account/project/model/agents, Cosmos DB, agent Storage/Search and telemetry.
These are planned components, not created resources. No endpoint, role
assignment, model deployment or cloud charge is claimed for this update.
See [the implementation sequence](./proper-warm-poc.md#cloud-poc-implementation-sequence-and-acceptance)
for the work required to turn that design into an observed cloud PoC.

Before creation, the task checked Compose project `proper-warm-poc` containers,
volumes/networks and TCP port 3410: none existed/listened. No existing resources
were adopted, stopped or removed. App and volume labels identify task
`4aaf9ee3-da69-4ebb-812a-edccc5637af7` and purpose `synthetic-demonstrator`.
Other Docker workloads on the workstation are unrelated and untouched.

## Resource Inventory

| Resource | Name/location | Status | Purpose / persistence |
| --- | --- | --- | --- |
| Azure resource groups/resources | none | not created | target architecture only; zero task cloud charges |
| M365 sites/files/folders | none | not created | no tenant content accessed or changed |
| Application source | apps/proper-warm/src, public, tests, package.json, manifest.json | created | executable synthetic PoC and reproducible tests |
| Container definition | apps/proper-warm/Dockerfile, compose.yaml, .dockerignore | created | non-root, local-only single instance |
| Architecture/runbook | this ledger, proper-warm-poc.md, app README | created | boundaries, setup, known gaps and inventory |
| Validation automation | .github/workflows/proper-warm-poc.yml, apps/proper-warm/scripts/verify-runtime.mjs, verify-browser.py | created | scoped CI, API/performance smoke and optional real browser interaction |
| Base image | node:24.18.0-bookworm-slim | downloaded | 325761777 bytes; application sources not uploaded |
| Local image | proper-warm-poc:2026-10-07 | rebuilt locally with RV-001 fix | 326010163 bytes; no code/credentials sent to remote registry |
| Container | proper-warm-poc-app-1 | running, healthy | user `node`; 127.0.0.1:3410 -> 3410; left available |
| Volume | proper-warm-poc_data | created, retained | persistent SQLite at /data/proper-warm.db |
| Network | proper-warm-poc_default | created | task-scoped Compose bridge |
| Native test databases | apps/proper-warm/.test-data | generated/ignored during tests | isolated owned test files, cleaned after closing |
| Native app database | apps/proper-warm/data | only if native start used | ignored, not needed for Docker execution |
| Validation screenshots | session files: proper-warm-desktop.png, proper-warm-mobile.png | generated | browser observations, not company evidence |

Application image ID:
`sha256:3ecff42a8529ebf6c997158e2e6ef92cf5bc7ac15b9ac3bf07d62c46c3967ce8`.
It is a local build, not published to a registry. Runtime was verified after
creation; this is not a cloud deployment.

The Dockerfile pins the verified base digest:
`sha256:6f7b03f7c2c8e2e784dcf9295400527b9b1270fd37b7e9a7285cf83b6951452d`.
No third-party application packages were installed. The base image layers
remain locally cached independently of the application image.

## Validation Evidence

| Check | Observed result | Boundary |
| --- | --- | --- |
| `npm test` | 40 passed, zero failures | domain, store faults/replay/reopen, HTTP and assistant contracts; RV-001 regression included |
| `npm run evaluate` | five fixtures passed; schema/citations 100%; zero prohibited actions/approval mutations/external calls | simulator checks, not model quality |
| Compose build/health | image built, non-root process healthy, writable named volume, loopback only | one local process, no HA |
| Runtime API smoke | all nine cohorts, exact filter, held-home blockers, portfolio/export/metrics pass | nine constructed homes |
| 100 sequential GETs | rebuilt image: p50 27.44ms; p95 61.52ms <=250ms | latest measured localhost sample; not production load |
| Python Playwright | sourced command, blocked hazard advancement, draft/failure, exact lost-response replay, export, drilldown, 390px reflow, no page errors | synthetic UI interaction, not user/accessibility certification |
| Container restart | EX-HOME-900 version12, 12 events and update due 2026-10-10T16:00:00Z preserved | browser-generated history retained, no reseed |
| Documentation hygiene | relative links and Git whitespace reviewed | original/addendum/memory/snapshots untouched |
| Existing synthetic generator | seed 1341953496; 980 candidates, 13 tables, 23,528 rows; zero validation errors | dry-run only; existing pack/private answer key unchanged; not imported into transactional approval state |
| RV-001 container regression | completion count 1 -> 0 -> 1 after independent handover reacceptance | isolated in-memory store in rebuilt image; persistent EX-HOME-900 version12/event12 retained |

The later owner-directed RV-001 implementation replaced the existing app image
and container, retaining the same owned volume, network, port and stored history.
The initial image ID was
`sha256:2aeb2b9b22502e6668728793cbe8f04e31a4a7513f8d28f9545c5af0c89f7fa6`
(326010139 bytes). Initial latency was p50 14.25ms/p95 28.55ms; latest sample
above supersedes it, without claiming comparable production-load performance.

The browser test intentionally created update and deduplicated assistant
fallback events in EX-HOME-900; failed hazard progression created no approval.
Failed intermediate browser checks exposed and corrected mobile grid overflow.
Transport-interception assertions were corrected to read hidden retained JSON
as text content. No lost-response replay or gate failure was hidden.
Cross-site navigation may load the loopback UI; writes still require exact
same-origin checks and Host remains restricted against DNS rebinding.

## Stop and Cleanup

Run from the repository root. Inspect names and task labels first:

```powershell
docker compose -f .\apps\proper-warm\compose.yaml ps
docker volume inspect proper-warm-poc_data --format '{{json .Labels}}'
docker compose -f .\apps\proper-warm\compose.yaml down
```

`down` stops/removes this project's container and network but preserves the
database volume and image. No other Compose project is in scope.

Intentional synthetic reset loses all task-case history. Export records first,
verify ownership and explicitly approve loss before executing:

```powershell
docker volume rm proper-warm-poc_data
```

Remove the exact image only if no longer required:

```powershell
docker image rm proper-warm-poc:2026-10-07
```

These destructive reset commands are documented for the owner, not run by
this task. No wildcard deletion, broad process killing or Docker pruning is used.
No Azure or M365 teardown is necessary because none was created.
