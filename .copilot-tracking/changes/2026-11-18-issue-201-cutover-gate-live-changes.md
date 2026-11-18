# Changes: issue 201 live audit (2026-11-18)

Tier: FOCUSED, docs-only. Basis: no src, SQL, infrastructure, workflow, dependency or deployment change; only read commands and one read-only in-container listing. No Azure resource created, so nothing to delete. No credentials read or printed.

## Files

* docs/reference/research/cutover-gate-live-r2-2026-11-18.md (added)
* docs/reference/README.md (index row), docs/reference/log.md (entry)

## Per-criterion table (unticked criteria of #201)

| # | Criterion | Result | Evidence |
| --- | --- | --- | --- |
| 1 | CI, Docker, Bicep image paths and scripts repointed; src build deployed and healthy | Proven for demo; residual gap | 0 tracked mvp/prototype files; workflows and Dockerfile use src context; infra pipeline tests pass; revision 0000032 Healthy, /healthz 200 (curl, Playwright); exec listing: only zava-forward-{agents,api,core}, no /app/mvp. Unproven: build-run record (ACR private, all 10 task runs Failed, no src-deploy runs) |
| 2 | Private mvp/data relocated and backed up outside git | Unproven (owner-only) | Private real data; no agent may read it; host has none |
| 3 | Owner signs off in this issue | Unproven (human) | Soak-period decision open |

Production-only items remain deferred under #1905 to #1908.

## Validation

* Docs only: relative links and diff reviewed (see review). mypy, ruff and unit tests not applicable (no executable change).
* Adverse: tools/check-legacy-references.py reports 45 violations (11 earlier); not fixed, out of scope.
