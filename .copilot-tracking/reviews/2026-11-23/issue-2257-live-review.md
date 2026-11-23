---
title: Issue 2257 live review (run 084412Z)
ms.date: 2026-11-23
---

Executed once after implementation. Outcome: conformant with routed follow-ups.

* The change is confined to `mapPanel` and one test; native button, hidden until failure, named in the notice, redraw bounded and cancelled on dispose and new draws.
* Behaviour preserved: JSON 500 still shown, not auto-retried; existing pinned tests pass (67 OK).
* Claim limits: live effect of the button is unproven until deploy; the origin of the live `ProgrammingError` stays unproven.
* Routed follow-ups: (1) deploy and add a Playwright proof that aborts the first `/api/map` calls and clicks the button; (2) log the SQLSTATE class for `ProgrammingError` if a 500 reappears. Human review, hosted CI and the gate remain with the coordinator.
* Reviewed also: research note `docs/reference/research/issue-2257-retry-control-2026-11-23.md`, its index row and log entry (documentation only, claims match the changes record).
