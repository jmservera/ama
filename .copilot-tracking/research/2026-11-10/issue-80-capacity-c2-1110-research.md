---
title: Issue 80 capacity browser check aftercare route inventory, research
description: Pre-execution source comparison of manager navigation against the check inventory (correction C2)
ms.date: 2026-11-10
---

## Scope and disposition

* Task `issue-80-capacity-c2-1110`, parent `issue-80-capacity-c1-1110`. Research disposition `executed` (source reading only; no browser run in this chain so far).
* Root admits one checker correction: add `#/aftercare` to `MANAGER_ROUTES`. Any further gap found before execution returns to Root.
* Preserved: C1 chain (`728e320c`, seven-record verify 0 is local phase verification, not strict separate-call conformance because the `implement-start` validation and marker were batched), original `4a0af32f` and its Review, browser-run1 and run2 logs.
* Base: `origin/main` fetched is `6d4cd624`, contained in HEAD `728e320c`; no merge.

## Navigation versus inventory (bounded, source-only)

* `workbench.py navigation()` for a manager (Retrofit Programme Manager; fixture user selected at `capacity_browser_check.py:179`) yields: `#/`, `#/all`, `#/overview`, `#/progress`, `#/visits`, `#/funding`, `#/finance`, `#/capacity`, `#/closed`, `#/assistants`, `#/time`, `#/aftercare`, `#/screens` (`#/simulator` is admin only). `MANAGER_ROUTES` holds all of these except `#/aftercare`. No other stale or missing entry found by this comparison; the guard order means the runtime confirmation is limited to routes reached.
* `#/aftercare` view: `aftercareWorkspaceView` in `aftercare.js`. A manager is in `VIEW_ROLES` but not `RECORD_ROLES` (`controls.py`: record = Resident Liaison Officer, Retrofit Coordinator).

## Second gap found before execution (stop condition)

* The view first calls `read("form")`, mapping a 403 to "no form" (`aftercare.js:316`). The server `form` handler requires `RECORD_ROLES` (`server.py:404`, `_staff(..., "record a concern")`), so for the manager this GET returns 403.
* The check's response listener appends every `/api/` response with status >= 400, not in `expected_failures`, to `failures` (`capacity_browser_check.py:265-283`), and `verify_route` asserts `not failures` after each route. So adding the route as the sole change is predicted to fail at `#/aftercare` with a `403 /api/aftercare/form` failure, by source reading (not executed).
* Also, `verify_route` demands a successful matching GET per listed endpoint; a 403 form endpoint cannot be listed, so the inventory entry would list only `concerns` and `evaluator`.
* Resolving this needs a different check design (for example registering that known 403 as an expected failure for this route) which is outside the admitted "add the route entry" scope and loosens a guard. I did not do it.
* Likely manager heading `Aftercare concerns` with a `role=status` line "Your role can read these concerns but cannot record one. Ask a colleague who can." (source reading).

## Planning Readiness

Blocked on a Root decision: either admit the expected-403 handling for the aftercare form read in the check, or direct another approach. No implementation or browser run was started.
