---
title: Capacity page 523 changes
description: Implementation evidence and explicit validation boundaries
ms.date: 2026-10-28
---

## Scope and status

Task 523; full planned scope requested. P01 and P02 implemented.
P03 heavy runtime/publication work remains blocked by recorded foreign lock
ownership, not waived. Original critique Revise retained; dispositions in plan.

## P01: Read compatibility

Appointment bindings project absent legacy contract_version as null. No seed
or authority is rewritten. New HTTP regression removes the field and old
resident bindings from a persisted work order, reads both endpoints, asserts
Unknown appointment state and rejects a write for lack of current authority.
Known-empty reads have their own regression. Both tests are inherited by the
existing JSON and opt-in SQL Server fixtures.

Pre-fix regression: exit 1, RemoteDisconnected after handler traceback ending
in appointments.py `_appointment_binding`, KeyError contract_version.
Post-fix four focused JSON/SQLite cases: PASS, 4 tests, 2.854s.

## P02: Capacity recovery

Scoped capacity GET errors identify packages or work orders, retain actionable
server text/error identity and preserve captured navigation abort/session expiry.
Initial errors use existing route Try again; refresh-load errors offer the same
read-only recovery, never replay a mutation. Added explicit no-packages state.
API README documents the separately invoked owned browser/SQL check.

capacity_browser_check.py generates the full seeded demo using the existing
fictional-register test fixture. It checks populated/empty capacity, actual
manager navigation, each 503/retry, transport failure, structured 403, 401 and
navigation abort. Default temporary SQLite and optional newly owned disposable
MSSQL container are separate modes. It takes the heavy lock nonblocking,
sanitizes inherited configuration and cleans only its own resources.
Harness execution remains blocked; source presence is not browser evidence.

## P03: Validation and review

SQL Server, full API suite, browser and full gate
not run because shared-heavy admission was unavailable at intake.
No Azure, secrets, environment files, private dataset or foreign SQL access.

Lightweight executed checks:

* `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests
  /tmp/ama-capacity-523-venv/bin/python -m unittest test_procurement_api -q`:
  PASS, 32 tests, 24.277s.
* Generated-demo SQLite rerun, seed 20260901/as-of 2026-10-13 with fictional
  register: PASS, 980 cases (443 open), 10 staff; one package and 601 work
  orders read, every binding contract version null.
* Node VM exercising actual ops.js: PASS, unstructured package failure,
  transport order failure and retained structured message/error identity.
  This is not a browser check.
* Node syntax check and Ruff check on changed Python: PASS.
* Browser harness strict isolated Ruff (E/F/I/B/UP, 100 columns): PASS after
  import sorting. No new line-length exemption.
* API mypy: initial failure from importing an untyped core generator test
  module; corrected to the existing dynamic test-generator boundary pattern.
  Rerun PASS, 91 source files.
* Final core mypy: PASS, 154 source files. Final added harness/test formatting:
  PASS. Browser/system libraries were not probed or installed because execution
  was blocked, not because they were assumed available.
* `git diff --check`: PASS.

## Other manager pages

Source search finds the failing manager projection only in work-order reads
and mutation response projection. Capacity is the only manager navigation page
loading that endpoint. Contractor order view also reads it, but intentionally
withholds evidence-visible bindings. The shared read fix applies without
expanding contractor disclosure. Resident preview uses appointment_status,
not the crashing summary for a legacy order with no offer.

Actual generated manager inventory and runtime disposition:

| Route | Runtime result |
| --- | --- |
| #/ | Browser blocked, not checked |
| #/all | Browser blocked, not checked |
| #/overview | Browser blocked, not checked |
| #/visits | Browser blocked, not checked |
| #/funding | Browser blocked, not checked |
| #/finance | Browser blocked, not checked |
| #/capacity | SQLite source/API regression passes; browser/SQL Server blocked |
| #/closed | Browser blocked, not checked |
| #/assistants | Browser blocked, not checked |
| #/time | Browser blocked, not checked |
| #/screens | Browser blocked, not checked |

No other confirmed same-class manager-page defect from source inspection;
this is not a runtime all-pages pass.

## Acceptance and residuals

Root-cause evidence and regression: met locally, live causality unverified.
Real SQL demo capacity, browser retry and other-page runtime checks: unmet.
Live verification: pending owner after separately authorized deployment.
Publication: blocked pending real SQL/browser, requested full API suite,
complete exact-head gate, current-base receipt and final independent assessment.
Use Refs #523, not Closes #523, in any later eligible PR.

## Review handoff

Source implementation is stable. P01/P02 complete; P03-T01 is partial
(lightweight checks pass, required heavy checks blocked); P03-T02 remains
pending one independent Review and commit/publication disposition.
This is a blocked partial candidate, not full-plan completion.
No material design divergence; dynamic fixture import and captured abort signal
are ordinary implementation judgments preserving the accepted boundaries.

## Original Review and publication disposition

The one independent Review completed: full-task execution Partial, outcome
Not accepted. Original findings remain unchanged in
.copilot-tracking/reviews/logs/2026-10-28/capacity-page-523-review.md.
RV-002 identifies introduced unsaved-draft loss on repeated refresh retry;
RV-003 identifies insufficient manager-route/read assertions in the new
browser harness. Both route to later implementation, not closure or another
Review in this task. RV-001 routes missing runtime evidence to research.
RV-004 through RV-006 are separately scoped pre-existing UI follow-ups.

Ordered Research, Plan, Implement and Review have executed, but implementation
acceptance is not complete. Automatic session remains running at Follow-up.
P03 markers remain unchecked. Source/evidence are retained as a partial local
candidate commit; no push or PR is eligible. No full receipt exists, no current
SQL/browser lock status is inferred, and no blocked check was retried/polled.
Live verification remains pending owner. The next eligible source action is
later rpi-implement for RV-002/RV-003; heavy work needs explicit coordination.
