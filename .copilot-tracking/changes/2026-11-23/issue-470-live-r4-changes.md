# Changes, issue 470 live r4

Files: tools/rpi-gate-timing.py (`compare --markdown`, `render_markdown`), tools/test_rpi_gate_timing.py (one test), docs/reference/research/issue-470-live-r4-2026-11-23.md (new), docs/reference/README.md (index row), docs/reference/log.md (entry). Tier FOCUSED (tools only, no src; `--all` not run). Divergences: none.

Checks: `tools.test_rpi_gate_timing` 18 OK; `tools.test_rpi_checks` 129 OK; ruff check and format clean on both changed tool files.

| # | Criterion | State | Evidence |
| --- | --- | --- | --- |
| 1 | --changed selects groups, records scope | Proven | 129 tests pass |
| 2 | --verify-receipt rejects partial receipt | Proven | 129 tests pass |
| 3 | --jobs parallel within lock rule | Proven | 129 tests pass |
| 4 | Measured full-run before/after in the PR | Unproven | `--all` and PR forbidden; `--markdown` only formats a future result |
| 5 | Tests for group selection and receipt scope | Proven | 129 tests pass |
