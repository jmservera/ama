# Details: issue 233 resident-choice summary withheld panel

* Phase 1: in `src/api/src/zava_forward/api/web/role-screens.js` the `resident-choice` `summary(entries)` returns a div with the existing panel plus `screenWithheld([...])` (contact history, detailed access and household history, contractor capacity and offered slots).
* Phase 2: `src/api/tests/test_role_screens_conformance.py` asserts the summary contains `screenWithheld(`; the trace states the panel is on the summary; log entry appended.
* Phase 3: validation listed in the changes file.
