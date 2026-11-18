---
title: Container hosting proof for issue 144 with retained raw output (demo)
description: Third live demo run for issue 144 that retains redacted raw az, exec and load output, reconciles the job count and records a per-criterion table
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 144
  - container apps
  - hardening
  - load test
estimated_reading_time: 4
---

Refs #144. Synthetic desktop demo only, resource group `ama`, owner authorisation of 2026-11-18 (cap USD 700, no drills, no Key Vault rotation, no production change). This run closes the evidence gap in the [earlier note](./issue-144-container-hosting-live-evidence-2026-11-18.md), whose second-run raw output was not kept. Raw files are in [issue-144-hosting-proof-live-2026-11-18/](./issue-144-hosting-proof-live-2026-11-18/) with subscription, tenant, replica and file-system ids redacted. No credentials were used and no Azure resource was created, so none needed deleting.

## Probes run

* Read-only `az containerapp show`, `revision list`, `job list` on three apps and the jobs ([apps.json](./issue-144-hosting-proof-live-2026-11-18/apps.json), [jobs.json](./issue-144-hosting-proof-live-2026-11-18/jobs.json), [revisions.json](./issue-144-hosting-proof-live-2026-11-18/revisions.json)).
* `gh run list --workflow src-deploy.yml` ([src-deploy-runs.json](./issue-144-hosting-proof-live-2026-11-18/src-deploy-runs.json)): `[]`.
* One interactive `az containerapp exec` into a demo API replica ([exec-probe-raw.txt](./issue-144-hosting-proof-live-2026-11-18/exec-probe-raw.txt)). The probe created `/tmp/zz144` and removed it in the same session.
* One bounded load run, 120 clients for 45 s against `GET /healthz` on the demo API, 13:40:53Z start ([load-test-raw.txt](./issue-144-hosting-proof-live-2026-11-18/load-test-raw.txt)). Cost is a few vCPU-minutes, far below USD 700.

## Observations

* Job count reconciled: `az containerapp job list` returns 8 jobs, all digest-pinned on `crcutovertestrzsrg.azurecr.io`. The earlier count of nine was wrong.
* No resource runs a quickstart placeholder image. Images in use: api (2 digests), agents, resident-demo, orchestrator (2 jobs), importer, cutover-proof (4 jobs).
* Demo API: revision `--0000031` is the only listed revision, single-revision mode, 100% traffic, created 2026-11-17T19:42Z; min 0, max 4, HTTP rule at 50 concurrent requests, 0.5 vCPU, 1 Gi, 2 Gi ephemeral, liveness, readiness and startup probes. Agents app: queue rule (queueLength 5), max 5, no probes declared. Resident demo: max 1, probes declared.
* Load: 1,752 requests, all HTTP 200, 38.9 requests per second, p50 1.067 s, p95 27.819 s, p99 29.16 s. Replicas went 0, 1, 2, 3, 4 in about 50 s. Latency was dominated by cold start and scale-out, which the earlier run (150 clients, p95 1.31 s) did not show; this is an adverse observation, not a failure of the criterion.
* Exec: `uid=10001(app)`, `CapEff` and `CapPrm` zero, `CapBnd` `00000000a80425fb` (runtime default, not dropped), `NoNewPrivs: 0`, `/` is `overlay rw`, `/usr` write denied by permission, `/tmp` writable, `ZF_CONTAINER_HARDENING` unset.
* `securityContext` is null on all three apps; the Container Apps API does not expose a read-only root or capability drop.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Worker and job images real, versioned, deployed through the pipeline | Partly proven. Images real and digest-versioned; pipeline clause unproven | Raw jobs.json and apps.json; `src-deploy.yml` has no runs and needs protected self-hosted runners and OIDC, outside the demo authorisation; the registry is private so tags cannot be matched to digests |
| Scale rules, probes, limits, rollback defined and tested (ticked) | Re-observed | Config in apps.json; scale 0 to 4 in the load log; rollback not exercised (single revision listed, drills excluded) |
| Container hardening enforced in the deployed app | Unproven. Non-root proven only | Exec output above: writable root, bounded but not empty capability set, no-new-privileges off, hardening env unset; closing it needs a redeploy from current main, a deployment change outside this authorisation |
| Load test recorded without claiming production scale (ticked) | Re-observed at demo scale | Health endpoint only; not the 60,000-home fixture |
| Single-replica and restart with audit persistence (ticked) | Not re-run | Restart and audit drills are excluded by the owner |
| Tokenomics drivers per unit of load (ticked) | Re-observed | 1,752 requests, 0 assistant calls, 0 SQL writes, 4 replicas peak; cost per unit stays Unknown without a price source |

No Playwright proof applies; the criteria concern container hosting, not a web page.
