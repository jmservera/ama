---
title: Issue 233 two-screen tension coverage review
description: Single post-implementation review of the technical and quality coverage increment
ms.date: 2026-11-10
---

## Execution

One review of the final implementation diff (two code files, four documentation files) by the primary agent; no nested agent was authorised. Not repeated. Boundary: working tree after implement-done (witness seq 5), base 736561ba0cccb9beb69eea3ae0d3a997bd0dd9bd.

## Outcome

Conformant to the brief with qualifications. No blocking finding. No product defect reproduced. No post-review repair is granted or made; any code change from independent review needs Root to reconcile finite correction authority first (balance UNKNOWN).

## Checks against the brief

* Existing checker extended, three-screen code unchanged: pass. All 194 baseline check names reproduce in the final run (comparison empty), plus 168 new ones (362 PASS, 0 FAIL).
* Same retained home: pass. `open_screen` keeps `case=ZF-1` in the URL and each screen asserts `Selected home ZF-1`.
* Visible withheld-items explanation, labelled regions, keyboard reach, 1280 px and 320 px: pass (4 of 4 technical and 2 of 2 quality regions reached by Tab at both widths; no horizontal scroll).
* Reuses the identity-aware helper `check_regions_and_keys` and the existing fixture port; `role_screens_fixtures.py` not modified.
* Unknown never becomes success: readiness success texts asserted absent; "No evidence", "Not supplied", "Not yet fixed" asserted.
* Original negative controls retained: eight original unit tests unchanged and passing; three new withheld-panel controls added.
* No forbidden file touched (panels.js, app.js, style.css, Core, schema, role-policy, backend). Recipe: N/A, neither changed file is registered in the scenario manifest.

## Qualifications

* Programme Manager is the only signed-in role in the checker. The Quality Inspector's role-specific omission of the technical change note was observed only in external inspection and is not asserted.
* The fixture overlay changed the shared home (technical and quality evidence at design version 1). The first attempt used version 2 and made the paused choice read "Not recorded"; that adverse log is retained and the fix preceded review.
* Browser negative controls (mutating the page to prove an assertion bites) were not run; unit controls cover the withheld helper only.
* The funding-amount absence check is a substring check on the fixture amount.
* Engineering evidence only: not WCAG, assistive-technology, usability, human disclosure, real data, Azure, model, live or production acceptance. Hosted CI and independent exact-head review have not occurred.
