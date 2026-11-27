# Issue 1837 changes (run b), 2026-11-27

Refs #1837. Base `a5b36579c2`. Synthetic demo, desktop only. Tier: focused (test-only, no src change); `rpi-checks.py` not run.

## Change

* `src/api/tests/test_nomination_api_routes.py`: in `test_route_form_failures_show_feedback_keep_form_usable_and_write_nothing`, wait for the feedback element to hold text before asserting it equals the server error. The response event fires before the page script writes the text, so the assertion failed once under host load (load average above 10).

## Divergence

* The test edit landed in the same tool batch as the `implement-start` witness call (witness qualification recorded); the changes record was persisted first.
* Not failing-first for the original defect (fixed on main; failing run kept in the 2026-11-18 record). The race fix is shown by the failure it removes: the inherited test failed once under load (`'' != 'Someone else changed...'`) and then passed in a full run.

## Validation

* `tests.test_nomination_api_routes`: 12 tests OK, zero skips ([unit-tests.txt](../../docs/reference/research/issue-1837-live-2026-11-27-b/unit-tests.txt)). One earlier full run had the workbench keyboard test time out at load 10-20; it passed alone and on rerun.
* axe 4.10.3: [standalone forms](../../docs/reference/research/issue-1837-live-2026-11-27-b/axe-nomination_route_forms-result.json) passed (statuses 200, 200, 200; no violations; target size clean); [challenge](../../docs/reference/research/issue-1837-live-2026-11-27-b/axe-challenge-result.json) passed.
* `checks.nomination_browser_check` (read-only nomination view, #1381, not the standalone forms) fails deterministically at its `nomination_review` call with a 5 s client timeout ([stdout](../../docs/reference/research/issue-1837-live-2026-11-27-b/nomination-check-stdout.txt)); cause not diagnosed, routed as a follow-up, not claimed as an 1837 defect.
* `python3 -m mypy` in `src/api`: no issues. `ruff check` and `ruff format --isolated --line-length 100 --check`: clean.
* Live Azure not exercised: a live write adds irreversible records to the shared demo.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Failing-first coverage, three browser submissions, valid challenge target | Proven (earlier record) | [failing run at 9da3fcd](../../docs/reference/research/issue-1837-live-2026-11-18/failing-first-at-9da3fcd.txt); `test_standalone_route_forms_submit_in_browser` passes in this run |
| Valid submissions retain records; JSON callers compatible | Proven locally; live unproven | browser test, stale-version test, axe run with three 200 responses; live writes withheld |
| Negative tests: authorization, isolation, malformed, same-origin/CSRF | Proven locally | refusal tests in the 12-test run |
| Browser journeys with axe, zero unexpected skips | Proven for standalone forms and challenge; workbench read-only check failing | this run's axe JSON; `nomination_browser_check` timeout recorded above |
| Dated RPI evidence; independent exact-head review; hosted CI | Partly proven; owner-gated | dated artifacts here; review and CI need publication, not permitted |
| Full tier receipt | Not applicable | no src change; test-only, impact basis recorded |
