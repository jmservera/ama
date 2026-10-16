---
title: Task queue filter research
ms.date: 2026-10-16
---

## Scope and evidence

Task #327, slug task-queue-filters-327. Research disposition: reused supplied
issue evidence plus direct code inspection. Planning Readiness: Ready.

`gh issue view 327 --comments` ran first; issue has no comments. PR #325 merged.
The clean existing branch perf/task-queue-filters-327 continues this work.
ADR 0006 requires src-only executable changes and external tests.

Store._filtered evaluates complete work_context for each visible open case,
before search, on every queue request. SqlStore deliberately delegates queue,
CSV and closed reads to Store. Queue membership is independent of the viewer;
only returned narratives are role-projected. Membership depends on all cases,
building/procurement context, snapshot as_of, ranking policy and the current
resident-authority/retention day (controls.today), not only case row versions.

## Decision

Use a process-local inverted queue membership index for each snapshot, storing
only case IDs, not projected context. Build all six queues once, atomically,
under the existing Store lock. Restrict candidates before ordinary filtering,
authorisation, sorting and paging. Invalidate by store version, as_of, policy
version/hash/approval/owner and controls.today. SQL's existing change-sequence
sync invalidates cross-process writes including shared-building changes.
Keep the closed-view contract (queue ignored after validation) unchanged.

This avoids dialect-specific schema and parameter-count limits. First access
after startup/invalidation still pays a full membership build; measure and
report it separately rather than claiming all requests are fast. CSV still
projects every matching output row, an unavoidable output-size cost.

## Measurement

Use test_sqlreads.make_cases(60000, seed=5), wholly fictional numbered Test Road
homes, with deterministic recent/stale/document/handoff/deadline variations.
No private stock or environment files are inputs. Measure first and repeated
queue pages separately, and count work_context calls to detect the original
scan independently of hardware timing.
