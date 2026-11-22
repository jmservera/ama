---
title: Issue 2191 capacity changes
ms.date: 2026-11-22
---

Refs #2191. Tier: focused; no `src` change, so no full gate and no `rpi-checks.py` run.

## Changes

* Live (az only, no Bicep): `retrofit` database objective Standard S0 to S3 (100 DTU), 13:51:29 to 13:53:49 UTC 2026-11-22. Read back capacity 100, Online.
* Throwaway job `job-tmp-sampler2191` created, run twice, deleted; job list read back without it. Temporary files in `/tmp` removed.
* Docs: [docs/reference/research/issue-2191-live-sql-capacity-2026-11-22.md](../../../docs/reference/research/issue-2191-live-sql-capacity-2026-11-22.md), index entry in `docs/reference/README.md`, entry in `docs/reference/log.md`.

## Divergence

The diagnostic reads, baseline samples and the scale ran during the research phase (the plan is one reversible command), before the plan and critique files were written. The artifacts record the same facts; no outcome was altered afterwards.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Cohort covers at least half of all homes with fresh readings | Proven for the demo | 30 minute series on S3: 51.7 to 58.7 percent per sample, mean 56.4 percent (14:03 to 14:31 UTC); baseline on S0 mean 30.8 percent |
| Configurable intermittent failure rate | Proven | `ZF_SIM_FAILURE_RATE` 0.1 read back on `job-live-simulator` |
| Consent mix preserved | Proven (prior evidence) | 261 granted, 27 declined in the 2026-11-22 readings note; consent data untouched |
| Unit tests | Not rerun | No source change |
| Refs #184, #165 | Not changed | Referenced only |

Unproven for the demo: receiver logs (workspace denies public queries; finished executions keep none). Open: S3 stays in place; the owner may step down.
