---
title: Progress dashboard correction round 2 phase details
ms.date: 2026-10-29
---

Task: 533-correction2-2026-10-29. P01/P02/P03-T01 complete; Review pending.
Research C1-C7 answers the scoped questions; no unresolved design decision.

<!-- P01 -->
## P01: Lifecycle validation

<!-- P01-T01 -->
### P01-T01: Reject malformed evidence before replay

At lifecycle entry validate history and both auxiliary lists. Missing auxiliary
keys retain []; explicit null/non-list or any non-dictionary row returns None.
Do not silently skip a row or fabricate a date. Existing history admission remains.
Extend inherited JSON/SQLite tests using persisted malformed values and reopened
stores, known sibling totals, archive null dates/date-filter exclusion, and open
malformed returns. Positive coverage keeps absent/empty/dictionary evidence valid.
Update existing API progress documentation without changing the knowledge base.
Completed: guards and three inherited API test methods pass for JSON/SQLite,
including newly opened stores reading deliberately malformed persisted evidence.
SQLite corruption fixture writes stored bodies directly; normal save's queue
validation is not the API-read boundary under test.

<!-- P02 -->
## P02: Clock-only overdue evaluation

<!-- P02-T01 -->
### P02-T01: Share the existing overdue algorithm

Move deadline evaluation to a typed taskqueues.overdue_tasks helper taking case,
dataset as_of and the existing projected handoff. Preserve ordered hazard response,
hazard resident update, case resident update, handoff acceptance rows including
case_id/source/version/as_of. Context continues computing blockers/hazard clocks,
but delegates overdue rows. Dashboard calls helper plus handoff_view, never context.
Invalid as_of retains its explicit ValueError.

Add core fixed expected rows and clock boundary table coverage. Existing queue
tests already cover strict past dates, naive/invalid dates, future completions,
released hazards and pending states; retain all. API regression links multiple
open cases to a registered synthetic building with hold/context, computes the
old work_context-based count, then patches full context and building.record to
raise during the new dashboard read. Include closed/unmarked exclusions and
multiple overdue tasks on one case so the count remains cases, not tasks.
Completed: helper/context/dashboard reuse, seven frozen expected deadline rows,
snapshot boundaries and registered-building parity/call-avoidance tests pass.

<!-- P03 -->
## P03: Validation and Review

<!-- P03-T01 -->
### P03-T01: Verify within current environment

First add regression tests and observe pre-fix failure. Use absolute current
worktree src/api/src, src/core/src, src/agents/src and their test paths in
PYTHONPATH. /tmp/mv has mypy/Ruff, but no Playwright and its core editable points
elsewhere. Inspect existing browser venv; install needed editable packages only
after the already observed missing-dependency failure if required.

Run mypy, ruff check . and ruff format --check . independently in both owning
projects. Run focused progress/taskqueue suites. Attempt full API/core discovery
under one nonblocking flock -n admission; if busy retain targeted-only fallback.
Owning tests must come first in PYTHONPATH for discovery: duplicate API/core
test module basenames caused the first core discovery import error after API
passed. Core-only retry again acquires nonblocking admission. API mypy uses
--python-executable /tmp/ama-533-venv/bin/python to inspect already-installed
dependencies missing from /tmp/mv; no shared environment mutation or suppression.
Run existing progress_browser_check with pinned axe and external output directory.
Do not invoke the full publication gate (includes az) or publish. Record actual
versions, exact commands, counts, log paths and blockers. No CI-equivalence claim
for differing tool versions or skipped integration prerequisites.
Completed: focused 49 tests; API/core mypy 102/156 files; both projects Ruff
lint/format; API discovery 1239 tests (316 skips); core retry 1456 (190 skips);
progress browser with pinned axe, eleven states/zero violations. Details and
changes retain initial dependency/discovery harness failures and successful
refinements. Existing contrast incompletes and opt-in integrations remain
distinct human/publication follow-ups, not waived or reported as accepted.

<!-- P03-T02 -->
### P03-T02: Preserve independent evidence and local stop

Resolve GitHub identity (8036360/jmservera from this session), set repository-local
noreply email for author/committer, commit implementation and current evidence
with Conventional Commit and Copilot trailer. Reviewer activates rpi-review,
reads exact correction diff plus plan/details/critique/changes, writes only
the new Review artifact. Preserve the single verdict and route findings later;
no fix/re-review loop. Commit original Review and reconciled closeout locally.
Stop automatic session per explicit caller direction. No push or az.
