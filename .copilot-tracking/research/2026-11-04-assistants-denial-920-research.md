# Research: assistants 403 and browser console (Refs #920)

Disposition: executed. Planning readiness: Ready.

## Already delivered

* PR #929 (merged 2026-11-03) classified all four responses as expected, added `services.photo` and `services.law_alerts` to `/api/me`, and added a Chromium check for photo, law alerts and regulatory chat status.
* Criterion 1 (classification) met. Criteria 2 and 3 were partial: `/api/assistants` 403 was not browser-tested.

## Findings

* `/api/assistants` returns 403 for any role outside `projection.STAFF_ROLES` (`core/assistants.py` registry). Contractors never load `assistants.js`.
* An admin-only account (`ZavaForward.ApplicationAdmin`, no staff role) reaches the case panel and `#/assistants` queue, which call `/api/assistants` and log a console error. This reproduced in Chromium before the fix (check FAIL).
* Expected, not defective: the denial is the intended role boundary; the server is unchanged.
* Separate finding, out of scope: the admin-only landing list also gets 403 on `/api/facets` (and `/api/cases/<id>` if a case route is opened). Recorded as follow-up.

## Slice

Add `services.assistants` to `/api/me`; the client skips the request and shows plain words with the manual route; extend the browser check.
