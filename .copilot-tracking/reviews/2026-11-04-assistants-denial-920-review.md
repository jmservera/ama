# Review: assistants denial (Refs #920)

Execution: executed once, self-review of the diff. Outcome: conformant for the slice; independent exact-head review and hosted CI remain pending.

## Acceptance criteria

* 1 Classified with reasons: met (PR #929, research above).
* 2 Expected denials show plain-language UI and no console error: met for photo, law alerts, regulatory chat status and `/api/assistants` (admin-only). UNMET in a wider sense: an admin-only account still gets 403 on `/api/facets` and case data on its landing list, which log console errors.
* 3 Browser test asserts no console errors: met for the staff flow; for the admin-only flow it asserts no `/api/assistants` request or denial only, not a clean console.

Issue stays open (Refs, not Closes).

## Follow-ups (ranked)

1. Admin-only landing: avoid or word the `/api/facets` and case 403s, then assert a clean console.
2. Live re-check after next deploy (pending, no deployment run here).

Limits: no axe, keyboard or screen-reader evidence; Fluent 2 and WCAG acceptance not claimed.
