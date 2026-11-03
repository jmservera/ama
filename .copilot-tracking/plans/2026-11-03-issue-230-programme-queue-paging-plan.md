# Plan: issue 230 programme queue paging

Details: [details](../details/2026-11-03-issue-230-programme-queue-paging-details.md)

1. Add paging to `programmeQueue` in `role-screens.js`.
2. Add node-driven unit tests (paging success, failure keeps rows) to `src/api/tests/test_programme_screen.py`.
3. Update the atlas screen trace row and append a `log.md` entry.
4. Validate: focused unit tests, ruff, mypy strict with `--cache-dir=/tmp/mypy-230`. No gate, browser check, benchmarks or full suites.

Critique (executed once, inline): control placement outside the scope form keeps Reset behaviour and tab order intact; failure path keeps rows and gives a next step; no write requests. Accepted. Stacked later slices: portfolio returned-work endpoint; AT validation (#155); Fluent adoption (#150).
