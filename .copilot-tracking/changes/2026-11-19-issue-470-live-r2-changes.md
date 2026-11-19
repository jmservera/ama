# Changes 2026-11-19 issue 470 (r2)

No source change; FOCUSED tier. Files: this tracking set only. Evidence note: docs/reference/research/issue-470-live-2026-11-19.md (earlier run, reused).
Validation: `python3 -m unittest tools.test_rpi_checks -q` gave 113 tests OK. mypy, ruff and web checks not applicable (no src or web change).

| # | Criterion | State |
| --- | --- | --- |
| 1 | --changed selects groups, records scope | proven |
| 2 | --verify-receipt rejects partial receipt | proven |
| 3 | --jobs parallel under single lock | proven |
| 4 | Before/after full-run timing in PR | UNPROVEN (needs a forbidden --all run and a PR) |
| 5 | Tests for selection and receipt scope | proven |
