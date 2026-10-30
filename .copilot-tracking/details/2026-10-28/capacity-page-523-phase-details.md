---
title: Capacity page 523 phase details
description: Bounded implementation tasks and evidence boundaries
ms.date: 2026-10-28
---

Task 523. Source research C1-C7; no unresolved source design choice.

<!-- rpi:phase id=P01 -->
## P01: Repair read compatibility

<!-- rpi:task id=P01-T01 -->
### P01-T01: Legacy binding

Change appointments._appointment_binding to read the optional legacy
contract_version consistently with list_packages. Do not normalize storage or
grant authority. Test HTTP package and order reads with the field removed,
null binding, Unknown appointment status and rejected appointment write.
Fixture is already SQLite-backed and inherited by real SQL Server test class.

<!-- rpi:phase id=P02 -->
## P02: Recover capacity loads

<!-- rpi:task id=P02-T01 -->
### P02-T01: Capacity error recovery

Wrap the two capacity GETs with context-specific plain-language errors.
Let route cancellation/session expiry retain existing behavior. Preserve
server-supplied actionable messages, avoid raw transport jargon, and use
the route's Try again control rather than duplicate recovery machinery.
Add explicit no-packages state. Avoid touching appointment mutations/drafts.
Browser harness uses the existing synthetic generator patched with fictional
register rows, temporary SQL store, manager login, seeded orders, empty data,
each endpoint's injected 503 and successful retry, adjacent navigation checks.
Real SQL Server mode must be opt-in and loopback-only; no existing DB wipe.
The stable harness is src/api/checks/capacity_browser_check.py:
`PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests python3
src/api/checks/capacity_browser_check.py`. Default is isolated SQLite. MSSQL
execution uses only a newly created task-owned container with freshly constructed
local settings, never ambient targets. Document the command in src/api/README.md.
Inject unstructured 503 for each endpoint, transport failure, structured
actionable denial, 401 session expiry, cancelled navigation and successful retry.
Use actual returned manager navigation as the inventory, asserting each page's
main heading/legitimate empty state and recording relevant request failures and
console/page errors. Include shared work-order read consumers in source analysis.

<!-- rpi:phase id=P03 -->
## P03: Validate and review

<!-- rpi:task id=P03-T01 -->
### P03-T01: Evidence

Lightweight targeted tests, Ruff and mypy first. Requested full API command,
SQL Server and browser checks require heavy admission and remain blocked
under current intake lock evidence. No retry polling or foreign resource use.
Record exact commands, outcomes, skips and missing evidence separately.
From src/api use the requested `PYTHONPATH=../core/tests:../agents/tests
python3 -m unittest discover -s tests -q`. Focused selectors include procurement
API regressions and appointment/core contracts. Ruff check/format and mypy use
the owning component configurations. Inherited destructive MSSQL tests run only
inside the gate's newly created labelled disposable SQL resource, with fresh
constructed connection settings; loopback or opt-in alone is insufficient.
The new browser harness is a separate required exact-candidate check, not
automatically discovered by tools/rpi-checks.py.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Review and publication

One independent review of source and evidence. Preserve original findings;
route findings to later work, never claim closure in this task.
Blocking findings prevent publication; only nonblocking/out-of-scope work may
be deferred without blocking it. No in-task correction/re-Review loop is allowed.
Resolve gh api user, configure repository-local privacy-safe identity and
commit Conventional Commit with required trailer. Full exact-head gate and
receipt verification precede publication; if blocked, do not push or create PR.
If eligible, PR says Refs #523 unless every criterion is proven. Live check
is pending owner, not inferred from local results.
Immediately before publication fetch main, verify the external full receipt
against current origin/main and require independent exact-head assessment.
Any later correction/commit invalidates the gate. Preserve the original Review.
