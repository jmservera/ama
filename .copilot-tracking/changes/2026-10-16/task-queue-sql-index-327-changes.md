---
title: SQL queue membership changes
description: Implementation and validation evidence for issue 327
ms.date: 2026-10-16
---

## Approved execution boundary

Full plan P01/P02. Owner comment and current request authorize implementation and
PR delivery on perf/task-queue-sql-index-327, based on origin/main at aedd616.
Worktree was clean. Research reused; plan and phase details prepared. Source
changes limited to src/, with related README/reference and RPI evidence.
First boundary: establish the reproducible post-write benchmark.

## Validation intent

Every queue/sort/view parity; indexed SQL plans; seed/backfill/write/shared/
cross-process/rollback tests; independent mutation checks; generated 60k before/
after measurements; pip-venv unit suites, ruff and mypy. No current blockers.

## P01-T01: Baseline measured

Session files/queue327-before.txt records three rounds per queue against aedd616,
using test_queue_benchmark.py. Initialization 12.145 s; median write/cold/repeat ms:
new 7.9/4973.8/76.8; priority 5.7/4185.6/0.2; stale 2.8/3582.5/49.9;
blocked 2.9/4326.0/169.9; overdue 6.1/4501.9/64.8;
unowned 7.2/4050.5/52.3. Cold context calls 58,274 for nonempty queues,
58,224 for priority. Mock evaluator instrumentation is included in both runs.

## Compatible critique refinements

PC-001/002/003 accepted directly: durable generation, locked refresh/hot validation,
complete evaluator-ready seed/backfill, SQL Server schema and harness checks.
Plan/details reconciled; no new owner decision or repeated critique.

## P01-T02: Durable flags and generation publication

Added queue columns/indexes to both dialect schemas and an additive, serialized
migration. Seed uses complete SQL state and an established snapshot; existing
rows backfill before startup readiness. Every save updates changed flags inside
its checked write transaction. Shared documents/linked cases conservatively
refresh all rows from authoritative SQL, including other-process changes.
Queue definition/day/as_of/policy changes refresh with atomic fingerprint and
generation publication. Hot hits validate under the same writer lock as ID
selection; only IDs are cached. Store filtering/projection remains after lookup.
Ranking now follows candidate synchronisation, preventing a write between initial
sync and lookup from producing old ranks with new context.

## P02-T01: Semantic, portability and mutation coverage

Existing parity now tests positive priority, all/mine/closed, all supported sorts
and fallback sorts, filters/search. Existing export/cursor/denial tests retained.
test_sqlqueues adds 12 tests covering physical flags, bounded writes/cold reads,
seed/backfill/reopen without a seed, rollback, index plans, cross-process context,
refresh-only generation changes and SQL Server DDL/migration/portable statements.
Seven behavior methods are wired into MssqlQueueMembership for opt-in execution.
No tests removed. Added exactly two core test modules, outside the package.

Mutation evidence (session files/queue327-mutations.txt):
* Original full-scan lookup: cold/hot regression fails 85 vs 6 evaluations.
* Incremental maintenance omitted: write regression fails 0 vs 1 evaluation.
* Shared maintenance omitted: physical blocked flag fails 0 vs 1.
* Exact baseline Store/SqlStore source aedd616 additionally fails all six 60k
  cold-path assertions: 58274 vs 50, or 58224 vs zero. No package edits involved.

## P02-T02: Final measurements and validation

The initial MagicMock-instrumented numbers above are superseded for comparison
by adjacent runs with a lightweight counter. Exact original Store/SqlStore source
was loaded in memory from git aedd616; the current benchmark ran unchanged
against both implementations. Baseline structural failures were expected and
required; all six queues still ran. Initialization 14.213 s before / 15.029 s
after. Session raw outputs: files/queue327-before-lightweight.txt and
files/queue327-after-lightweight.txt.

| Queue | Before write/cold/repeat medians ms | After write/cold/repeat medians ms |
| --- | --- | --- |
| new | 16.6 / 2900.0 / 60.8 | 5.1 / 1062.9 / 54.1 |
| priority | 6.1 / 2850.5 / 0.2 | 4.7 / 1140.5 / 0.2 |
| stale | 4.2 / 3487.7 / 59.2 | 4.7 / 1107.9 / 41.0 |
| blocked | 3.4 / 3153.5 / 191.8 | 4.0 / 1241.0 / 145.0 |
| overdue | 2.5 / 3029.8 / 55.3 | 3.6 / 1157.0 / 54.3 |
| unowned | 3.8 / 3032.2 / 43.6 | 4.1 / 1130.5 / 34.2 |

Every nonempty cold read evaluates 50 contexts, priority zero. Repeated same
pages are identical. Initialization and shared/clock/policy full-refresh costs
are explicitly distinguished from ordinary writes. Cold global ranking remains
and timings have load/GC variance; no write-speed or Azure latency guarantee.

Local pip venv, installed src packages:
* Core: 487 tests, one isolated-Azure opt-in skip. Includes both 60k suites.
* API: 549 tests, 110 opt-in skips, including seven new MSSQL behavior methods.
* Agents: 70 passed. Orchestrator: 22 passed. Importer: 39 passed.
* Total: 1167 tests, 111 conditional skips; every executed test passed.
* All five project ruff check, format check and mypy passed. Missing declared
  API Playwright dev dependency was restored with pip after mypy reported it.
* Final targeted queue tests: 12 SQL and 13 semantic/parity methods passed.
* git diff --check passed. README links/anchors reviewed; reference log appended.

No private datasets, prohibited paths, Docker, Azure resources or live SQL Server
were accessed. Azure compatibility is local DDL/shared-statement evidence plus
opt-in harness wiring, not claimed live execution.

## Pre-Review reconciliation

P01/P02 implementation and evidence complete. P03-T01 contains only one Review
and publication; splitting it from validation removes a circular gate without
changing scope or decisions. No implementation blocker or unresolved critique
finding. No evidence-grounded new follow-up task is required for this slice.

## P03-T01: Review complete, publication pending

One post-implementation Review completed: Conformant for the local engineering
boundary, no substantive findings or later corrective routing. Source and tests
are frozen for publication. No live-engine or operational approval is inferred.
