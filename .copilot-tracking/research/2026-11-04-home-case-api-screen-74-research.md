---
title: Research for #74 home case API and screen slice
ms.date: 2026-11-04
---

* Task: feat/issue-74-r5, Refs #74. Research disposition: executed (code and issue read).
* Prior delivery: merged PR #907 delivered the core module only (`home_case.py`, `Store.home_case_view`, `home_case_record_version`; test_home_case). The 2026-11-04 closure audit ticked criteria 1, 3, 4 at core level and left criterion 2 open: no API or screen shows the building/home separation to staff. No open PR for #74.
* Gap: `view()` is not routed in `src/api/.../server.py`, and no screen renders it.
* Smallest slice: GET `/api/cases/{id}/home-case`, POST `/api/cases/{id}/home-case-version`, and a read-only `#/case-home/{id}` screen with separate sections (links, this home only, shared building, retained versions). The core already enforces staff-only access and finance-restricted allocation.
* Boundaries: version recording is not an approval; contractors get 403; AI is not involved; manual path is the existing case and building screens.
* Not in this slice: browser/hosted evidence, a UI form to record versions, building record versioning, work-package and provider detail beyond the explicit links.
* Not security, infrastructure, SQL or deployment work: focused tier.
* Planning Readiness: Ready.
