# Changes: issue 233 utilisation versus choice slice

* `src/api/src/zava_forward/api/web/role-screens.js`: new panel stating offered capacity is not a booking or promise, resident choice takes precedence, and packages are listed in reference order, not ranked by utilisation; packages sorted by id.
* `src/api/tests/test_role_screens_conformance.py`: new static test for the panel and sort; trace-status assertion updated.
* `docs/reference/research/ux/atlas-screen-trace.md`: tension status and guardrail text updated.
* `docs/reference/log.md`: entry appended.

Validation run: test_role_screens_conformance (10 tests), atlas_screen_trace checker (complete), node --check, ruff, mypy --strict on the test file. Not run: gate, full suites, benchmarks, rendered or assistive-technology checks. `tests.test_static_assets` errors on a missing module import, identically before this change.
