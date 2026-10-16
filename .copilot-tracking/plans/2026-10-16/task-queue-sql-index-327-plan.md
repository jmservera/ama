---
title: SQL queue membership implementation plan
description: Indexed durable membership with the existing hot ID layer
ms.date: 2026-10-16
---

Task: #327. Slug: task-queue-sql-index-327. Scope: full plan.
Parent: completed task-queue-filters-327 / PR #336.

## Executive Summary

Persist six indexed integer membership flags. Compute them from the existing
work-context evaluator in the case-write transaction; refresh shared dependants
and rebuild on evaluator-clock/policy changes. Query IDs on a cache miss, leaving
authorisation and output projection after lookup. Measure rather than assume
the remaining filtering, sorting and ranking cost.

## User Decisions and Requirements

* Implement the owner's 2026-10-16 issue #327 comment, not a cache-only alternative.
* SQLite and Azure SQL portability, backfill, every queue/sort/view parity,
  write-cold and repeat 60,000-case timings, failing mutation checks.
* Only src/ application changes; external-package tests; pip venv, unit suites,
  ruff and mypy. Do not read private data or touch prohibited paths.
* Update README and append knowledge log, commit with the specified identity
  and trailer, push current clean topic, open a PR using Refs #327 only.

## Goals

Remove full-stock context evaluation from ordinary post-write queue reads.

## Scope and Non-Goals

Core SQL/schema/write/cache paths and directly related tests/documentation.
No queue semantic changes, Azure deployment, Docker or private corpus access.

## Functional Requirements

Six integer flags and portable indexes; atomic write maintenance and rollback;
restart/backfill; shared/cross-process invalidation; policy/snapshot/day refresh;
authorisation after ID lookup and request-time context projection.

## Non-Functional Requirements

No new SQLite-specific shared syntax. Ordinary writes must not evaluate all
cases. Retain hot ID cache. Timings disclose full rebuild/startup and write costs.

## Acceptance Criteria

Full response parity with uncached selection across all queues, sorts and views;
seed/write/backfill/shared/concurrent/rollback tests; indexed lookup plans;
60,000-case cold-after-write and repeat measurements with evaluator counters.
New regressions must fail with the changed path disabled.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Baseline and implementation

<!-- rpi:task id=P01-T01 -->
* [x] P01-T01: Add reproducible post-write benchmark and record baseline.
<!-- rpi:task id=P01-T02 -->
* [x] P01-T02: Persist and backfill flags; transactionally maintain dependencies;
  retain SQL-backed hot candidates and downstream permissions.

<!-- rpi:phase id=P02 -->
### P02: Evidence and delivery

<!-- rpi:task id=P02-T01 -->
* [x] P02-T01: Extend existing parity/scale owners; add at most one focused SQL
  queue test module and one benchmark module under core/tests. No removals.
  Existing semantic taskqueues tests remain the oracle; add mutation checks.
<!-- rpi:task id=P02-T02 -->
* [x] P02-T02: Run unit suites, ruff/mypy, measurements; update README/index/log.

<!-- rpi:phase id=P03 -->
### P03: Review and publication

<!-- rpi:task id=P03-T01 -->
* [ ] P03-T01: Perform one post-implementation review, commit/push/open PR.

## Critique Disposition

One final-candidate critique executed: Revise, three compatible planner-owned
refinements, all accepted directly. PC-001: atomically publish fingerprint and
generation, validate hot hits and obtain IDs under the writer lock; refresh-only
changes invalidate hot IDs. PC-002: evaluate seed/backfill only after effective
snapshot and complete authoritative shared state exist. PC-003: assert SQL Server
DDL/migration/index/statement portability locally and wire queue behavior into the
existing opt-in server harness. No owner decision or repeat critique required.

## Follow-Up Items

None identified. Live Azure performance and owner operational ratification are
outside this local engineering change, not claimed complete.
