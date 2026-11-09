# Details: issue 954 C2 false-refresh proof (2026-11-09)

Plan `.copilot-tracking/plans/2026-11-09-issue-954-c2-refresh-plan.md`.

## Step 1: checker (`src/api/checks/photo_flag_stale_browser_check.py` only)

* `refresh()`: stash `window.__zfServices = me.services` before the visibility event; wait for `me.services !== window.__zfServices` (the handler always replaces it) instead of the status text.
* New `false_refresh_proof()` shared by the real runs and the control:
  1. `page.evaluate("me.services = {...me.services, photo: true}; photoFailed = false")`, assert `me.services.photo` is true and the photo request count is still 1 (no extra load).
  2. `refresh(photo=False)`; assert served `me_flags == [True, False]`, then assert the ACTUAL client `me.services.photo` is false and the status shows the unavailable text, then after a 500 ms settle assert no additional photo request.
* `observe(..., ignore_false=False)`: when set, `me_route` records the served false then drops `services.photo` from the fulfilled body (the client sees no false).
* `main()`: before the real runs, run the control once with status 503 and require an `AssertionError` whose label is the client-flag assertion; record the outcome in the observation output. Then the real 503 and 403 runs (corrected behaviour) pass through the same helper. The control result is not appended to `results` (no count inflation).

## Step 2: validation

Ruff 0.17.1 (existing pinned venv, read only) check and format; holder check then one `flock -n` admission; unit selections. Raw logs outside the repo in an owned mktemp directory copied to session evidence.

## Step 3: record

Changes, review (referencing the original adverse outcomes), state JSON, handoff.
