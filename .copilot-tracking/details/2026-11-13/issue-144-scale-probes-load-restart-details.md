# Details: Issue #144 scale, probes, load and restart

## Phase 1: infra contract test

* Parse every declared `Microsoft.App/containerApps` and `jobs` resource in `infra/*.bicep` and `infra/modules/*.bicep` as text.
* Assert: bounded cpu/memory (<= 0.5 vCPU, <= 1 GiB); apps have bounded `maxReplicas` and a scale rule where they scale; jobs set `replicaTimeout` and `replicaRetryLimit`; ingress apps have Startup/Readiness/Liveness on one port equal to `targetPort`; Single revision; API limits equal `scale_load.API_LIMITS`; `/healthz` is the store readiness handler (200/503); worker has no probe; rollback prose and pipeline guard; fixture declared 60,000/600,000 with no production claim.

## Phase 2: separate-process test

* `ApiProcess` runs `python -m zava_forward.api.server` with `ZF_STORE=sqlite` over `scale_load.build_store` output.
* Sequence: start, log in, 3 acknowledged `call` writes, closed-loop concurrent load with RSS sampling, record `VmRSS`/`VmHWM`, SIGKILL, restart on the same file, compare `/api/audit-check` entries and chain, write once more, chain still intact.
* Unit tests use 150 homes, 4 clients, 2 s. The CLI uses declared 60,000 homes.

## Phase 3 and 4: record

* `docs/architecture/scale-restart-2026-11-13.json` is the unedited benchmark output.
* `infra/README.md` hosting table rows for C2, C4, C5 and `src/api/README.md` gain dated, bounded wording.
* `docs/reference/log.md` gets an appended entry.
