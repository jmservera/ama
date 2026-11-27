# Issue 1837 plan, 2026-11-27

Refs #1837. Tier: focused (test-only; no src change, so the full gate is not run).

## Critique (one pass, executed)

Verdict: proceed. Risks: the new test could pass vacuously. Mitigation: a temporary mutation of `nomination-routes.js` (removing the button re-enable) must fail it, then revert. The test must use the real server rejection (stale `expected_version`), not a stubbed one; only the network-failure branch is aborted in the browser.

## Steps

* Add `test_route_form_failures_show_feedback_keep_form_usable_and_write_nothing` to `src/api/tests/test_nomination_api_routes.py`.
* Run mutation proof, the file's tests, mypy and ruff.
* Record per-criterion table in the changes record; write research note under `docs/reference/research/`.
