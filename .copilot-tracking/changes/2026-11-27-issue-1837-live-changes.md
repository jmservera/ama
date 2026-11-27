# Issue 1837 changes, 2026-11-27

Refs #1837. Base `b64c6e95dd`. Synthetic demo, desktop only. Tier: focused (test-only, no src change); `rpi-checks.py` not run.

## Change

* `src/api/tests/test_nomination_api_routes.py`: add `test_route_form_failures_show_feedback_keep_form_usable_and_write_nothing`. In Chromium it submits the acknowledgement form with a stale `expected_version` (a second JSON ack lands first) and asserts a real server rejection (status >= 400) whose `error` text appears in the form feedback, focus moves to the feedback, the button is re-enabled and the stored acknowledgement is the other session's. It then aborts the request and asserts the "Nothing was recorded" message and an enabled button.

## Divergence

* The test edit was written before this record and before the `implement-start` witness (witness qualification recorded). The research and plan records were persisted first.
* The test passes on current main, so it is not failing-first for the original defect (that evidence stays in the 2026-11-18 failing-first record). Its sensitivity was shown by mutation: removing the `button.disabled = false` re-enable line in `nomination-routes.js` made it fail (`False is not true`); the script was reverted.

## Validation

* `tests.test_nomination_api_routes`: 12 tests OK. `python3 -m mypy` in `src/api`: no issues. `ruff check` and `ruff format --isolated --line-length 100 --check`: clean.
* Live Azure not exercised: a live write adds irreversible records to the shared demo.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Failing-first coverage, three browser submissions, valid challenge target | Proven (earlier record) | [failing run at 9da3fcd](../../docs/reference/research/issue-1837-live-2026-11-18/failing-first-at-9da3fcd.txt); `test_standalone_route_forms_submit_in_browser` |
| Valid submissions retain records; JSON callers compatible | Proven locally; live unproven | same browser test and the new stale-version test (original, owner kept); live writes withheld |
| Negative tests: authorization, isolation, malformed, same-origin/CSRF | Proven, extended | existing refusal tests plus browser failure-path test (stale version, network abort, nothing written) |
| Browser journeys with axe, zero unexpected skips | Not re-run | proven in the [2026-11-23 r2 record](../../docs/reference/research/issue-1837-live-demo-evidence-2026-11-23-r2.md); no web file changed |
| Dated RPI evidence; independent exact-head review; hosted CI | Partly proven; owner-gated | dated artifacts here; independent review and CI need publication, not permitted |
| Full tier receipt | Not applicable | no src change |
