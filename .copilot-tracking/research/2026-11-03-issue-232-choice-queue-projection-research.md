# Research: issue #232 server-side cross-home choice queue

* Task: issue-232-choice-queue-projection (round 2). Disposition: executed (reused closure audit and prior research).
* Merged evidence: #652 (choice and update screen), #715 (page-level summary), #777 (service issue screen), #856 and #933 (keyboard, axe and design-system class evidence). #487 closed unmerged.
* Closure audit 2026-11-03: criteria 2 and 3 ticked; criterion 1 unmet because the queue summary covers only the 20 homes on one page and fetched each home from the browser; criterion 4 (WCAG 2.2, AT, #151/#155) and 5 (Fluent adoption, #150) unmet.
* Smallest coherent slice: a read-only server projection `GET /api/resident/choice-queue` reusing `Store.detail` so existing role redaction applies, restricted to the four resident-choice roles, and the screen reading it. Criteria 4 and 5 need AT/human testing and Fluent adoption, out of scope.
* Planning readiness: Ready. Risks: new authorised read endpoint (role matrix, redaction), so security-sensitive tier boundary applies.
