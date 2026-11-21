---
title: Source CI critical path evidence (issue 2189)
description: Hosted CI timings and acceptance-criterion status for sharding src-api, retrieved 2026-11-21
ms.date: 2026-11-21
---

## Scope

Issue 2189 asks for three outcomes: Source CI wall time under 15 minutes on a code PR, no skipped test, and unchanged required check names. Evidence below comes from `gh run view` on recent `Source projects CI` pull request runs of jmservera/ama (retrieved 2026-11-21). No workflow or source file was changed.

## Observed timings

| Run | Created (UTC) | src-api | src-core | mssql | src-namespace | Run wall time |
| --- | --- | --- | --- | --- | --- | --- |
| 44931821304 | 17:45:55 | 28.1 min | 9.6 min | 7.4 min | 7.9 min | 28.9 min |
| 44920805967 | 15:44:46 | 22.4 min | 10.0 min | 7.9 min | 5.8 min | 23.1 min |
| 44902274916 | 12:06:43 | 23.0 min | 12.7 min | 7.5 min | 7.4 min | 23.6 min |

For run 44931821304 the src-api job spent 22.9 min in "Unit tests and dependency-rule test", 2.9 min in the synthetic design-system browser checks, 0.3 min installing and under 1 min on image, scan and SBOM steps. The unit-test step alone exceeds the 15 minute target, so no change outside that step can meet it.

## Findings against the issue's proposals

* Shard api into 3: not implemented. `.github/workflows/src-ci.yml` runs one `src-${{ matrix.project }}` job per project and `python -m unittest discover -s tests -v` without a shard split.
* Cache pip: not implemented. `actions/setup-python` has no `cache` input; install takes about 20 s, so the saving is small.
* Run mssql only when SQL paths change: already in place. `tools/ci-affected.py` sets `mssql` true only when core, agents, api or orchestrator change (`MSSQL_PROJECTS`), and the workflow gates the job on that output. Local run with a 19-file diff returned `mssql=true` because api files changed; `tools/test_ci_affected.py` passes.
* Even with these changes, the mssql job (about 7.5 min) and src-core (up to 12.7 min) are not the critical path; src-api is.

## Acceptance criteria

| Criterion | Status | Evidence or reason |
| --- | --- | --- |
| Source CI wall time under 15 min on a code PR | Unproven (currently not met) | Three recent code PR runs took 23.1 to 28.9 min. Meeting it needs sharding plus a hosted run on a pushed branch; pushing is forbidden here, so a post-change timing cannot be recorded. |
| No skipped test | Unproven | No change was made, so no regression was introduced. Whether CI skips tests was not measured: `src/*/tests` contain 20 or more runtime `skipTest` calls (missing Chromium, SQL-only or SQLite-only contracts) and a hosted skip count was not retrieved. |
| Required check names unchanged | Proven for the current head | No workflow edit; job names `src-changes`, `src-api`, `src-core`, `src-agents`, `src-orchestrator`, `src-importer`, `src-namespace`, `src-no-working-data`, `mssql` match the observed runs. A sharded design must keep `src-api` as a single aggregate check name. |

## Why no implementation

A workflow edit that changes job structure affects gate semantics, so it takes the full validation tier, including a complete local receipt that the coordinator, not this worker, runs. Its main outcome (wall time) can only be measured on a hosted run, which needs a push. Sharding also needs a design decision: the api tests use shared SQLite state and a cross-test PYTHONPATH, and sharding must keep the `src-api` required check name via an aggregating job.

## Recommended follow-up

Add an `api` shard dimension (three jobs from an ordered module list), keep an aggregator job named `src-api`, enable `cache: pip`, then compare timings on the first hosted PR run.
