---
title: Details for #74 home case API and screen slice
ms.date: 2026-11-04
---

* Phase 1: `server.py` GET branch before the generic `/api/cases/` read (exact 4-part path, KeyError 404, PermissionError 403); POST act `home-case-version` calls `Store.home_case_record_version` and returns the view. Existing handlers map ValueError 400, ConflictError 409.
* Phase 2: `app.js` `homeCaseView` and route; sections labelled "This home only" and "Shared at building level"; unknown data labelled; finance restriction notice shown.
* Phase 3: `src/api/tests/test_home_case_api.py`, `src/api/README.md`.
