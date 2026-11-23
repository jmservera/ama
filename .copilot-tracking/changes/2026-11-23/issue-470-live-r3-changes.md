# Changes, issue 470 live r3

Files: docs/reference/research/issue-470-live-r3-2026-11-23.md (new), docs/reference/README.md (index row), docs/reference/log.md (entry). No src or tools change; tier FOCUSED. Divergences: none. Check run: 129 gate tests OK.

| # | Criterion | State | Evidence |
| --- | --- | --- | --- |
| 1 | --changed selects groups, records scope | Proven | 129 tests pass |
| 2 | --verify-receipt rejects partial receipt | Proven | 129 tests pass |
| 3 | --jobs parallel within lock rule | Proven | 129 tests pass |
| 4 | Measured full-run before/after in the PR | Unproven, owner-gated | --all forbidden, heavy lock present, retained receipts non-comparable, no PR allowed |
| 5 | Tests for group selection and receipt scope | Proven | 129 tests pass |
