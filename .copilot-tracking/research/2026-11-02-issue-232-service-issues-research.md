# Research: issue 232 service issue screen (2026-11-02)

* Disposition: executed (reuse of merged `resident-choice`, #652, as evidence).
* Finding: `resident-choice` covers criteria on choice, pause/withdrawal and the commitment. It only lists service requests in a minimal table. The "accessible service issue" is not designed. Data exists in `service_requests` (route, owners, accessibility, representative_ref, next_update, remedy, history) and `resident_update`.
* Constraint: other open slice PRs touch `role-screens.js` (#771); append at file end to minimise conflict. No new files other than a test.
* Planning Readiness: Ready.
