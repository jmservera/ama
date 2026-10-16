---
title: Task queue filter phase details
ms.date: 2026-10-16
---

## P01-T01

Use direct evidence in research/2026-10-16/task-queue-filters-327-research.md.
First record original 60k timings. Build an ordered ID index for all queues in
one canonical evaluation pass, publish only on success. Key it by snapshot
version, as_of, controls.today and ranking definition/approval. Look up current
case objects after restricting IDs; retain original filters and projection.
Closed view and contractor/invalid-queue guards must run before index access.

## P02-T01

Depend on P01. Add at most eight core test methods, no removals. Compare cached
selection to canonical uncached selection for every queue and existing sorts.
Check context-call counts on repeated pages (including negative queues), export,
current-day/snapshot/policy invalidation and SQL cross-process/shared changes.
Use the existing generated 60k stock with deterministic queue field variation;
report cold and repeated-page timings, matches and exported-row counts.
Run core and API unit suites, all project ruff/mypy checks in the pip venv.
Patch selection to the original uncached scan at runtime: new regression must fail.

## P02-T02

Depend on verification. README describes invalidation and remaining cold/export
costs with actual figures, knowledge log appended, index routing updated.
One post-implementation review; fix issues before review rather than looping it.
Resolve GitHub identity, use owner-specified privacy email, include required
Copilot trailer, push existing topic and create main-based PR with Refs #327.

## Current state

All plan tasks complete, including one Review and publication of PR #336.
Five test methods added, zero removed, within budget.
Local suites total 1140 tests, 104 existing skips; all executed tests passed.
All five project ruff/format/mypy checks passed. One critique Pass; mutation
killed in JSON/SQLite. Detailed paired timings and cold caveat are in changes
and the core README. No material decision or code-scope divergence.
