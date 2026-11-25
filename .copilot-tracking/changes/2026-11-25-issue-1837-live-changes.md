# Issue 1837 changes, 2026-11-25

Refs #1837. Base `5bac4d3ff3`. Synthetic demo, desktop only. Tier: focused (test-only, no src change); no `rpi-checks.py` run.

## Change

* `src/api/tests/test_nomination_api_routes.py`: add `test_correction_and_challenge_writes_refuse_unsafe_requests_and_write_nothing`. For `nomination_correct` and `challenge_open` it asserts unauthenticated 401, contractor 403, array body 400, native urlencoded 400, trusted-proxy without CSRF header 403, stale version and stale proposal version refused, unknown case 404, and that the stored case is unchanged afterwards. Previously only `nomination_acknowledge` had these negatives.

## Divergence

* My first draft expected a ZF-1 proposal posted to `/api/cases/ZF-2/resident` to be refused. It returned 200 because the priority suggestion legitimately covers ZF-2 (`_priority_includes_case`); that was a wrong assumption, not a defect. The test uses an unknown case instead.
* The new test passes on current main, so it is not failing-first. It guards existing behaviour; the failing-first evidence for the original defect remains the 9da3fcd run in the earlier records.

## Validation

* `tests.test_nomination_api_routes`: 11 OK (one earlier run showed a Playwright wait timeout in the keyboard test under host load; the rerun passed).
* `test_nomination_api_routes`, `test_nomination_screen`, `test_challenge_no_retaliation_api_220`, `test_resident_api`: 42 tests OK, 1 skipped (in a neighbouring file, not investigated).
* `python3 -m mypy` in `src/api`: no issues. `ruff check` and `ruff format --isolated --line-length 100` clean on the file.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Failing-first coverage, three browser submissions, valid challenge target | Proven (earlier record) | [failing run at 9da3fcd](../../docs/reference/research/issue-1837-live-2026-11-18/failing-first-at-9da3fcd.txt); `test_standalone_route_forms_submit_in_browser` passes this pass |
| Valid submissions retain records; JSON callers compatible | Proven locally; live write unproven | browser test asserts owner, original account, correction and challenge records; live writes would add irreversible records to the shared demo |
| Negative tests: authorization, isolation, malformed, same-origin/CSRF | Proven, extended | new test covers correction and challenge as well as acknowledgement |
| Browser journeys with axe, zero unexpected skips | Not re-run this pass | proven in the [2026-11-23 r2 record](../../docs/reference/research/issue-1837-live-demo-evidence-2026-11-23-r2.md) with a disclosed load-related retry; no web file changed |
| Dated RPI evidence; independent exact-head review; hosted CI | Partly proven; owner-gated | dated artifacts here; independent review and hosted CI need publication, which is not permitted |
| Full tier receipt | Not applicable | no src change; gate not run by instruction |
