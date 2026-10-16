---
title: Task queue filter implementation evidence
ms.date: 2026-10-16
---

## Scope and first boundary

Full plan #327, P01-T01 active. Approved writes: src/core store and external
tests, directly relevant READMEs/index/log and RPI artifacts. No blockers.
Research reused; final candidate critique executed once, Pass, no findings.
Implementation and Review explicitly requested in the user's end-to-end task;
no unattended follow-up loop is authorised.

## Validation intent

60k deterministic fictional cases, cold/repeated wall times plus evaluator
counts, JSON/SQLite semantic parity and invalidation, original-path mutation,
local pip-venv suites/ruff/mypy. No private inputs or live dependencies.

## P01-T01 implementation and baseline

Implemented Store._queue_candidates: process-local inverted ID lists, canonical
work_context evaluated once per open case for all queues, atomically published
under existing Store lock. Key includes version/as_of/current resident day and
canonical policy JSON. Existing guards precede index access; existing filters,
visibility, ordering, global ranks and per-output projection follow it.
SqlStore's queue fallback therefore uses the index without new SQL.

Before-fix scale test failed on all six evaluator-count assertions. A first
trial used Mock call-history recording and exaggerated timings; discarded from
the published comparison. Final before/after use the same lightweight counter.
Fixture: make_cases/queue_cases seed 5, 60,000 fictional homes, 58,224 open,
as_of 2026-10-16. Three repeated second pages, median ms before/after:

| Queue | Matches | Before | After |
| --- | ---: | ---: | ---: |
| new | 19375 | 2167.9 | 215.3 |
| priority | 0 | 1931.9 | <0.1 |
| stale | 14539 | 2102.7 | 158.3 |
| blocked | 58224 | 2567.9 | 611.3 |
| overdue | 18326 | 2157.9 | 198.8 |
| unowned | 11675 | 2134.4 | 129.6 |

Cold first new page before/after: 3217.4/3090.6 ms, not materially improved.
All subsequent queues share the index. Warm per-page evaluator counts changed
58274 -> 50, or 58224 -> 0 for priority. Generation/DB opening excluded.
After scale test passed; includes first-page/next-cursor disjointness and totals.

## P02-T01 current verification

13 queue tests pass: existing definitions plus four new semantic/invalidation/
complexity methods; the fifth added method is the 60k scale test. No removals.
JSON/SQLite uncached parity covers all six queues, six sorts, mine/all, area,
wave, owner, long/consent flags and search. Additional tests cover exported
row counts, guard-before-index ordering, snapshot/policy/current-day expiry,
failed build recovery, shared-only saves and another SQL process's handoff and
closure writes. Initial expiry test fixture lacked first-contact evidence;
fixed the fixture, not the production rule. Existing three HTTP queue tests pass.
Core ruff/format/mypy pass; full suite in progress. API ruff/format pass; mypy
found missing playwright dependency, to install the existing dev extra.

## P02-T01 completed checks and mutation

Core full suite: 468 tests, OK, one existing SQL Server skip. Core ruff,
format and mypy: passed (89 checked files). API three queue HTTP tests, ruff
and format: passed. Installed the existing api[dev] extra after mypy's missing
playwright failure; API mypy then passed (44 checked files).
Agents: 70 tests; orchestrator: 21 tests; importer: 39 tests; all passed,
as did each project's ruff/format/mypy checks.

Mutation executed with unittest and patch.object(Store, "_queue_candidates",
original_scan), running test_warm_pages_exports_and_denials_do_not_rescan_context:
both JSON and SQLite failed with 91 contexts versus 2 output rows. Harness
required exactly two assertion failures and no errors, then reported MUTATION
KILLED. Production source remained unchanged by this check.

Full core repeat run confirmed first queue 2280.5 ms; warm medians
211.6/<0.1/157.3/595.3/194.1/123.3 ms. These secondary results show normal
run-to-run variation; the README retains the original paired before/after run.
Existing unfiltered 60k SQL reads remained 53-150 ms in the full suite.
Full API suite is still running; publication/Review await its result.

Full API suite subsequently passed: 542 tests, 103 existing conditional skips.
All five suites total 1140 tests, 104 skips; all executed tests pass. The API's
expected missing-law-store tests log explicit errors; no swallowed error or new
failure is reported. No Docker or Azure validation attempted.

## P02-T02 handoff and follow-up boundary

Core README records paired timing medians, matches, cold construction, command
and invalidation rules; API README links it. Knowledge index updated and log
appended. No schema, dependency manifest or workflow/check name changed.
Code/validation scope ready for the task's single Review. Commit/push/PR remain
publication actions after review. If writes make cold rebuilds dominant in a
future workload, owner may select incremental maintenance as a separate task;
that speculative optimisation is not a blocker or active scope expansion.

## Single Review result

Review executed once, Complete / Conformant for source/test/docs scope, no
findings or material divergence. Canonical review:
.copilot-tracking/reviews/logs/2026-10-16/task-queue-filters-327-review.md.
Remaining P02-T02 work is commit/push/PR. Resolved GitHub account through
gh api user: id 8036360, login jmservera; required privacy email therefore
8036360+jmservera@users.noreply.github.com.
