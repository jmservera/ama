---
title: Role task queues 76 implementation evidence
ms.date: 2026-10-16
---

## Scope and initial state

Full P01-P03 offline plan, user-directed end-to-end implementation. Clean
existing topic branch; current source includes merged role IA and technical/
resident controls. Write boundary src plus requested docs/RPI. No deployment
or private dataset. First execution boundary P01-T01.

## Planning corrections

Applied PC-001..004 clock, lifecycle, projection, source trace and independent
test oracles in phase details. Rejected PC-005's unsupported temporary-path
prohibition in favor of explicit user /tmp/zf164 direction. Critique is final.
Open operational owner decisions remain follow-ups, not fabricated approvals.

## Validation intent

Absolute worktree PYTHONPATH per project, /tmp/zf164 Python/ruff/mypy; Node
syntax; real loopback synthetic SQLite app and Playwright. Record outcomes
after execution. SQL Server/Azure/real AI and direct human acceptance not run.

## P01 and P02-T01 shared implementation

Added typed core taskqueues derived model, six visible definitions, snapshot
clock, explicit missing evidence/owners, control prerequisites and independent
external deadlines. Store and limited SqlStore share context; dynamic filters
use existing in-memory fallback before paging, keeping deterministic cursors.
Both API list and CSV validate/propagate queue. Authenticated metadata provides
the versioned reset. Contractors receive no new fields or queue authority.

The web uses one shared current-context renderer in queue/case/history/
suggestion, with blocked-step and source-trace disclosure. Existing single
reset consumes the server default, clears the new filter and retains focus.
Existing browser harness now explicitly imports this worktree's packages,
avoiding another editable install accidentally exercising different code.

Targeted evidence: nine core tests and two real SQLite HTTP tests passed.
Core/API ruff and mypy passed after typed fixture annotations were corrected.
The HTTP sentinel exposed an existing derived-status leak to contractors;
fixed the tightly coupled projection alias for status, not a new role policy.
Role-restricted staff status and top-level reason now withhold human text too.
No owner permissions, approvals or SQL schema were changed.

## P02-T02 validation results

All commands use /tmp/zf164 and absolute current-worktree PYTHONPATH for
installed project source plus the executing project's tests first, then
required shared core/agents fixtures. This resolves duplicate test module
names across projects without loading another worktree.

* Core: 401 tests passed, Ruff passed, mypy 83 files passed.
* API: 519 tests passed, 101 skipped, Ruff passed, mypy 43 files passed.
* Agents: 70 tests passed, Ruff passed, mypy 16 files passed.
* Orchestrator: 17 tests passed, Ruff passed, mypy 8 files passed.
* Importer: 39 tests passed, Ruff passed, mypy 10 files passed.
* Node syntax check of app.js passed.
* Real loopback design-system and shared-IA Playwright suites passed under
  Chromium 156.0.8078.4, using synthetic JSON with no model/deployment settings.
  HTTP unit harness separately uses real local SQLite. All eight implemented
  roles, 320/390/768/1024/1280 widths, 200% root text enlargement, exact queue
  IDs, hazard timing/owner, current-context equality, case refresh, all-filter
  reset, alternate server default, focus/announcements and stale-response
  rejection passed. No browser errors.

Initial full-suite failures were corrected before review: safe missing status
in the existing projection helper, and "Task sources" replacing internal word
"trace" to meet the copy audit. Initial browser strict-locator ambiguity was
removed by avoiding a second safety-flag class on the clock paragraph.
No existing tests were removed. Two new test files, existing browser files
extended. The 120-case HTTP/store oracles verify totals, cursor pages without
duplicates, compound filters, nondefault sort and CSV order.

Orchestrator metadata was absent in the pre-existing venv. Pip-only editable
installation of orchestrator/importer restored it after the missing-dependency
failure; no runtime dependency or lock changed. No-build-isolation first
failed because setuptools was absent; ordinary pip build isolation succeeded.
Existing sensor fixture ResourceWarnings were observed; unrelated tests passed.
SQL Server, opt-in human/browser paths and other existing API skip gates were
not silently enabled. Real AI, SQL Server/Azure, direct screen-reader/human
acceptance and hosted checks remain not run/Pending CI.

## P03 documentation and review readiness

Updated component guides, dated parity audit and reference routing; appended
the reference log without rewriting history. Explicitly distinguish record
timestamp age from source validity and snapshot hazard observations from
live service timing. PC-001..004 are reconciled; no remaining implementation
markers or source blockers before the single post-implementation Review.
Operational policy owner decisions remain follow-ups, not offline blockers.

## Single Review handoff

P03-T01 complete. Review execution Complete; outcome Residual work for full
issue acceptance, no source defect identified in the bounded offline slice.
RV-001 routes operational definition/role/redaction decisions to owner/control
owners; RV-002 routes live-platform and direct human acceptance separately.
No repeat Review or source correction loop. Parent continues only requested
delivery P03-T02. Review pointer:
.copilot-tracking/reviews/logs/2026-10-16/role-task-queues-76-review.md.

API skips reconciled without re-running: 98 declared SQL Server cases, two
azure-core-dependent cases and one opt-in stock browser method. The separate
shared-workbench/browser suite passed; the stock browser remains not run.
