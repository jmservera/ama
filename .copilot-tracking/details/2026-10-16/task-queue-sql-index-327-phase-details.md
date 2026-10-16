---
title: SQL queue membership phase details
description: Write boundaries and validation evidence contract
ms.date: 2026-10-16
---

## P01-T01

Add a generated-fixture benchmark under src/core/tests. For each queue, commit a
case change before timing the first 50-row page, then repeat the same page.
Use three rounds; report write and read timings, result counts and context calls.
Baseline uses the current merged cache; no private stock or external calls.

## P01-T02

Use queue_new/priority/stale/blocked/overdue/unowned integer columns, each with
a membership/id index. Seed and save maintain them transactionally. Existing
databases get defaults and a transactional backfill with a persisted context
fingerprint. Full refreshes cover day/as_of/policy/definition changes; shared
building/procurement or linked-case changes conservatively refresh dependants.
Evaluate against authoritative transactional SQL state, not stale process data.
Keep original rowversion/seq/audit semantics and fail explicitly on evaluator errors.
Cache only membership IDs; query SQL on cache miss, then reuse existing _filtered.
Publish a monotonically increasing membership generation with every refresh,
atomically with its fingerprint. Validate even hot hits under the cross-process
writer lock and sync cases before selecting IDs, preventing mixed generations.
Evaluator inputs must stay unchanged through a refresh or the transaction fails.
Schema addition precedes evaluator-ready backfill: establish effective as_of and
read complete SQL bodies/building/procurement documents before evaluating.

## P02-T01

Extend test_taskqueues.py for full every-view parity, positive priority fixture,
exports and cursors. Focus SQL tests on physical flags, index plans, old-schema
backfill/reopen, ordinary-write bounded evaluation, rollback and cross-process
shared-context correctness. No test removals, at most two added test modules.
Mutation disable SQL lookup and disable write maintenance separately; targeted
regressions must fail. Benchmark both unchanged and final implementation.
Cover two-store refresh-only generation invalidation, input changes without a
policy version bump, failed refresh rollback and startup without the seed file.
Assert fresh/migrated SQL Server integer DDL, translated indexes and portable
lookup/refresh statements locally. Wire relevant behavior into opt-in MSSQL tests;
live server execution remains explicitly unverified.

## P02-T02

Use the session pip venv with editable src packages, never uv/PYTHONPATH=mvp.
Run all core and API unit tests plus relevant dependent workload suites,
ruff and mypy using project configuration. Record skips honestly; no Docker or
live Azure run is implied. Update existing core README, reference routing and
append-only log. Implementation evidence is complete; local suites total 1167
tests, 111 conditional skips. All five projects pass lint/format/type checks.

## P03-T01

Review once after implementation; publish without merging. This delivery-only
task is separated from P02-T02 to avoid a circular pre-Review completion gate.
