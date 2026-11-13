# Details: #521 API cutoff test proof

* Phase 1 (venv + install): pass `--no-build-isolation` if offline build fails.
* Phase 2 (origin check): python one-liner prints `__file__` for the two modules; must start with the worktree `src/` path.
* Phase 3 (tests): unittest run; capture exit via `$?` into a file. Expected MSSQL-only skips are recorded, not failures.
* Phase 4 (evidence): changes file `.copilot-tracking/changes/2026-11-13/521-api-cutoff-1105-changes.md`, sha256 of test output log; log stored in /tmp then summarised, removed.
* Success: exit 0, zero failures/errors, boundary tests (`test_sql_fixture_window_ends_at_the_shared_authority_end`, `test_extended_authority_allows_january_and_stops_at_exact_february_boundary`) executed and passing.
