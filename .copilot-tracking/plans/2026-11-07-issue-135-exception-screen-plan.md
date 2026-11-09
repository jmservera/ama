---
title: Issue 135 employee exception screen plan
ms.date: 2026-11-07
---

* Research: `.copilot-tracking/research/2026-11-07-issue-135-exception-screen-research.md`. Details: `.copilot-tracking/details/2026-11-07-issue-135-exception-screen-details.md`.
* Tier: focused. Scope: `role-screens.js`, `test_data_operator_screen.py`, new `test_exception_register_screen.py` only.

## Phases

* [x] Phase 1: host passes `(signal, rows, c)` to `overview`; data-operator `overview` keeps summary and adds register panel.
* [x] Phase 2: pure functions `exceptionRegisterView(signal)`, `exceptionRegisterPanel(data)`, `validRegister`, unavailable/denied panels.
* [x] Phase 3: regression test file with synthetic constructed responses (failed-AI, quarantined, conflict, workflow-only note, empty/unrouted/roles-not-named, denied, malformed, network, stale/aborted, zero writes).
* [x] Phase 4: run focused unit, ruff, format, mypy, node syntax; record pending browser check.
* [x] Phase 5: web-guidelines refresh, changes record, single Review. Browser feature check is NOT done (pending heavy admission).

## Critique (one pass, final candidate)

Executed 2026-11-07 against this plan. Verdict: proceed with direct amendments.

* Finding 1 (applied): an auto-load would write an audit entry for every page view; the plan uses an explicit link.
* Finding 2 (applied): `screenTable` falls back to "No records supplied. This does not establish readiness." which is wrong wording for an empty queue; the register panel must use its own empty text that says empty or unrouted is not all-clear.
* Finding 3 (applied): `screenValue` on an object prints "[object Object]"; render only named scalar fields and guard non-string values.
* Finding 4 (applied): stale protection relies on `routeController.signal`; the plan must re-check `signal.aborted` after the await and rethrow so a superseded load never renders.
* Finding 5 (recorded, not applied): widening `roles` for named non-manager staff conflicts with the no-inferred-authority rule; routed to follow-up.
