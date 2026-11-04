# Review: role survey browser test (Refs #920)

Execution: executed once, self-review of the diff. Outcome: conformant for the slice; independent exact-head review and hosted CI pending.

## Acceptance criteria

* 1 Classified with reasons: met (#929).
* 2 Plain-language UI and no console error: met locally for all staff roles, Contractor and admin-only accounts on their navigation routes, case route and assistants. UNMET: live evidence after deploy; routes outside navigation not surveyed.
* 3 Browser test asserts no console errors: met locally for admin-only, seven staff roles and Contractor. Not run in hosted CI; the check is a manual Chromium script, not a CI job.

Refs #920, not Closes: live re-check and independent review remain.

## Follow-ups

1. Live re-check after the next deploy.
2. Decide whether to wire the Chromium check into a CI job.
