# Research: non-detriment independent review and complaints route (Refs #86)

Date: 2026-11-14. Base: feat/demo-233-same-home-tensions-0825. Disposition: executed. Planning Readiness: Ready.

* Delivered: `resident_decisions.py` already has Complaint and Independent review routes (`ROUTES`, `FORMAL_ROUTES`), a different redress owner, an independent named reviewer bound to a measure decision version, a formal-route forward boundary (`complaints_route.py`, unconfigured by default) and a test that opening a formal request leaves decisions, reviews, hazards and stage unchanged.
* Gap: no surface states the route or the non-detriment commitment. `store.case_view` exposes `measure_decisions` but nothing tells a resident, representative or frontline staff member how to reach independent human review or the formal complaints route, who may raise it, what is preserved (programme place, repairs, safety duties) or what is not yet sent. The service-issue screen (`role-screens.js` `resident-service-issues`) lists requests only.
* Constraint: no legal outcome is asserted. The receiver is unconfigured, so the route must say nothing is sent unless acknowledged. Representative authority for "Communicate" must not be inferred.
* Plan: add a pure `redress_route_view(case)` in core, expose it as `redress_route` on the case view, render it on the service-issue screen (read-only, text cues), test core and screen.
