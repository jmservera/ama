---
title: Archive marker bounded audit follow-up
ms.date: 2026-10-27
---

Task ID: 496-rv001-archive-marker. Parent: 496-r4391306128.
Status: bounded later implementation complete; final-head assessment pending.

## Authority and Original Outcome

The original correction Review is Complete / Not accepted, with one Medium
RV-001 audit finding. Preserve it unchanged and do not repeat it. The user
already requested a comprehensive same-pattern queue audit, and the session is
explicitly non-interactive with end-to-end implementation required. This is a
bounded later follow-up within that request, not a waiver of the finding,
unrequested redesign, backend enrichment or a new human approval.

## Research Disposition

Disposition: reused and verified. Wider: the manager closed-case archive also
receives summary.hazard independently of work. Deeper: Store.page_cases returns
closed summaries with hazard but no work; closedView drops the hazard flag.
Contrarian: a completed retrofit can receive a new safety report without
reopening, proven by test_hazard_referral.py's existing closed-case coverage.
Therefore "no work projection" was not a sufficient marker-specific disposition.
Original research's broad no-additional-pattern claim is qualified by this
later evidence, not silently rewritten.

Planning Readiness: Ready. Existing evidence and exact implementation are
sufficient; no new authority, backend field or timing decision is needed.

## Bounded Plan and Acceptance

* Add only the canonical projected `Safety issue open` danger/text marker to
  closedView, using r.hazard exactly as the open queues do.
* Add the second (already budgeted maximum) executable unit method to the
  existing role-screen test owner, running actual closedView with hazard=true
  and hazard=false closed summaries and no work.
* Observe pre-fix failure, then run all host/queue/projection regressions.
* Do not manufacture archive work/clocks, change the closed status, reopen
  cases, broaden permissions or alter the contractor allow-list.
* P03's one scoped gate and original/final-head review boundaries are unchanged.
  Final-head independent assessment must cover this later delta as well.

This is a later ordinary rpi-implement finding disposition, not another Plan
critique or repeat of the original Review. The source change is fully determined
by the original canonical marker and independently evidenced projection; no
new design choice calls for a new plan-critique cycle.

## Implementation and Validation

Second executable real-renderer unit failed before the fix for missing
"Safety issue open", then all 17 host/navigation/HTTP queue/hazard API tests
passed after adding only the projected canonical marker to closedView.
API-wide Ruff check, configured format (46 files), strict mypy (88 source
files), app/host JS syntax and diff checks pass.

An external owned-loopback browser exercise added two temporary synthetic
closed cases, signed in as the actual manager and read the actual closed-case
API. It confirmed hazard is projected without work, only the true-hazard row
has the visible canonical marker, no task clocks are invented, native focus
and 320/390/1280px reflow pass, and no writes/JavaScript errors occur.
Script and logs are retained at the external session evidence root; no
production fixture or child browser expectation changed.

Original RV-001 and its Not accepted outcome remain unchanged in the original
Review. This later implementation dispositions the evidenced display omission;
independent exact-head assessment must cover both this delta and the specialist
correction before publication. No second original Review or gate was run.
