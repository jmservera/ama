---
title: Issue 2191 half of homes fresh, changes (2026-11-22)
---

## Changes

* Live (read only plus a throwaway job): `job-tmp-sampler2191b` created, run, deleted; job list read back without it. A first attempt used a bad `command` and then a missing `pyodbc`; both failed without side effects and were replaced by the same named job.
* No change to SQL tier, jobs, code or consent data in this pass.
* Docs: [docs/reference/research/issue-2191-live-coverage-reproof-2026-11-22.md](../../../docs/reference/research/issue-2191-live-coverage-reproof-2026-11-22.md), index entry in `docs/reference/README.md`, entry in `docs/reference/log.md`. Raw samples: `.copilot-tracking/evidence/2026-11-22/issue-2191-halfhomes/`.
* Tier: focused (documentation and read-only live checks; no `src` change). Basis: no code, workflow, dependency or Dockerfile edit.

## Divergence

Sampling ran before the changes record was persisted, because the 30 minute series had to start while plan and critique were written. The record states the same facts; no outcome was altered.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Cohort covers at least half of all homes with fresh readings | Proven for the demo | 15 of 15 samples, 51.5 to 58.5 percent, mean 56.3 percent (18:35 to 19:03 UTC, S3) |
| Configurable intermittent failure rate | Proven | `ZF_SIM_FAILURE_RATE` 0.1 read back; evidence `settings.txt` |
| Consent mix preserved | Proven (prior evidence) | 261 granted, 27 declined in the 2026-11-22 readings note; not re-queried |
| Unit tests | Unproven in this pass | No source change; earlier tests recorded in prior notes, not rerun |
| Refs #184, #165 | Not changed | Referenced only |

Unproven for the demo: receiver logs (finished executions keep none).
