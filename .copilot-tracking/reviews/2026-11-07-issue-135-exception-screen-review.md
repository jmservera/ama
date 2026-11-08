---
title: Issue 135 employee exception screen review
ms.date: 2026-11-07
---

* Review executed once, after implementation, by the implementing agent (self-review). Independent exact-head assessment remains required and is not claimed.
* Web Interface Guidelines re-fetched 2026-11-07 (HTTP 200) before review; changed web file checked against all rules.
* Outcome: **Conformant for the bounded slice with open items; criteria not all proven by browser evidence.** Not a pass of the focused gate (browser check pending).

## Acceptance criteria

* 1 Explicit access to GET /api/exceptions on the existing screen, returned contract rendered: met in source and renderer tests.
* 2 Fields and failed-AI versus workflow-only distinction: met in renderer tests; no model call.
* 3 Both conflict values with source, date, version, owner, Unknown eligibility, no winner: met in renderer tests.
* 4 Banner, sources, unrouted, access, note preserved; empty not all clear: met in renderer tests.
* 5 Failure, denial and stale handling: met for the renderer (clears via replaced view, abort rethrown). Real DOM replacement and navigation not browser-verified: OPEN.
* 6 No write control: met (one `<a>` only; source test; every recorded call is a GET).
* 7 Reuse of labelled table pattern, text states: met in structure tests. Keyboard and narrow reflow not browser-verified: OPEN. Human and AT acceptance: UNMET by design (#151/#155).
* 8 Regression demonstration: met for renderer; zero write requests asserted.

## Findings (preserved, none resolved in this task)

* F1 (medium, open): focused browser feature check not run; pending heavy admission.
* F2 (medium, open): `test_exception_register` Register and Endpoint classes (SQL and server fixtures) and `rpi-checks --changed` not run. Backend authority is unchanged but not re-exercised.
* F3 (low, accepted): named stewards whose signed-in role is not a manager cannot open this screen; widening roles would infer authority from profile names. Owner decision, route to later work.
* F4 (low, accepted): deep link `exceptions=1` re-requests and re-audits on refresh or back navigation; selecting a home drops the parameter.
* F5 (low): source dates and versions show as recorded strings, not via `Intl`, to avoid altering evidence; identifiers lack `translate="no"`.
* F6 (info): runbook text is placeholder engineering guidance labelled as such; no approved runbook or staff naming exists.

## Routing

* Coordinator admits the browser and SQL/server checks, then independent assessment. Whole #135 stays open (producers, durable recovery, roles, live and AT acceptance). Child PR uses `Refs #135`.
