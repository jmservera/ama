# Research: issue 954 C2 false-refresh proof is vacuous (2026-11-09)

Task `issue-954-c2-refresh`, parent `issue-954-c1-detector`. Local only: no push, PR, issue, board, live provider, credential, model or spend.

## Disposition

Research executed 2026-11-09 against frozen commit `3a1629c08` (clean, branch `test/demo-photo-validation-954-1109`). `origin/main` fetched: `1464b4d850a89aaaf835ba8a9ad98d38aeb1fdd6` (tool, selector, tracking and score only; no merge or rebase needed). Planning Readiness: Ready.

## Correction budget

Standing limit five total scoped correction cycles per issue. C1 is spent. C2 is authorized by the coordinator within the five total; three remain after C2. This is not an extra grant or a budget reset.

## Evidence

* Independent C1 Functional finding 1 (session files `independent-954-c1-final/functional-findings.json`, Medium, `photo_flag_stale_browser_check.py` lines 257-260): the startup denial already sets client `me.services.photo` to false, so the false refresh never exercises a client true-to-false transition. `me_flags` is appended inside the `/api/me` route fixture before the application consumes the response, so `me_flags == [True, False]` proves only what was served.
* App contract (`src/api/src/zava_forward/api/web/app.js:244-266`, `recheckPhotoService`): the handler replaces `session.services` with `{...session.services, ...fresh.services}` and, when the result is false, sets the unavailable status. If a regression ignored `fresh.services.photo=false` while a client flag of true remained and `photoFailed` was true, the handler would reload the photo and heal itself, so a text sentinel alone could pass.
* The status-text sentinel in `refresh()` proves that some handler branch ran, not that the flag was applied.

## Design conclusion

* Before the false refresh, set and assert client `me.services.photo === true` (and `photoFailed = false`) without another photo load, asserting the photo request count is unchanged.
* Make the refresh sentinel the replaced `me.services` object identity (the handler always replaces it), so an ignored false still completes deterministically, with no self-heal reload.
* After the refresh assert the actual client flag is false and the unavailable status shown, retaining served-sequence, no-additional-request and time-origin checks.
* Add a deterministic negative control: the same page flow where the route omits `services.photo` from the fulfilled body only after recording the served false (a stand-in for a client that ignores the false response). The shared proof helper must raise at the client-flag assertion; the corrected path (the real 503 and 403 runs) passes through the same helper.

## Historical qualification (review wording only)

The original review F2 said 403 receipt rows were not produced. Original raw observation `evidence-954/obs/photo-flag-stale-console.json` actually holds both a 503 row and a 403 row (neither has a `failure`; the empty `#account-error` hit is recorded in both). Classification happened after both observations and failed on the 503 assertion first, so the 403 classification assertion never ran. A dated qualification is appended to the original review; the original text is not rewritten.

## Boundaries

Checker only. No `app.js`, `index.html` or API change. Preserve actual 503/403 quiet receipts, pending states, manual paths and detector positives; no blanket ignore of empty dialogs. The published owner definition of quiet is unchanged.
