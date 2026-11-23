---
title: Issue 144 worker image to workload mapping contract
description: Offline regression test that ties Bicep workloads, the pipeline image mapping and shipped worker modules together, with per-criterion status for issue 144
ms.date: 2026-11-23
---

Scope: synthetic demo, repository-only. No Azure call, no throwaway resource, no credential read. Refs #144. Retrieved 2026-11-23.

## Finding

`WORKLOAD_IMAGE_PARAMETERS` in `infra/scripts/pipeline.py` had no test referencing it. A drift between it and `infra/modules/containerapps.bicep` would let the pipeline record, or an operator deploy, the digest of the wrong project for a worker. No test showed that each worker command module exists in the project whose image the worker receives.

## Change

`WorkerImageMapping` in `infra/tests/test_container_hosting_completeness.py` (3 tests):

* every Bicep workload symbol is in the mapping table and the table matches the pipeline workload keys exactly;
* each workload's `image:` parameter equals the pipeline mapping;
* each of the six `python -m` workers (agents, orchestrator, token_store, digest_blob, ranking_publish, importer) resolves to a file under the `src/<project>` that owns its image parameter.

Evidence: 21 tests in the file pass; changing `auth-renewal` to `importImage` in `pipeline.py` makes the new test fail (mutation check, reverted). `ruff check` and `ruff format` clean. `test_pipeline.SmokeTests.test_installed_local_api_denies_unauthenticated_requests` errors on this host with and without the change (needs an installed API).

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| Worker and job images real, versioned, deployed through the pipeline | Unproven | The mapping and module contract is now tested, but no `src-deploy.yml` run exists and registry tags are unreadable from this host. |
| Hardening enforced in the deployed app | Proven except read-only root | See [the 2026-11-23 receipt](./issue-144-live-hardening-receipt-2026-11-23.md); read-only root needs an owner exception. |
| Scale, probes, limits, rollback; load test; single replica and restart; tokenomics drivers (ticked) | Not re-proven | Out of scope for this angle. |
