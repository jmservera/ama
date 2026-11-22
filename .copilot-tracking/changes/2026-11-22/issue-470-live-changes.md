# Changes: issue 470 closure evidence

Status: implemented. Tier: FOCUSED (documentation only, no `src/` or tool change; no `--all` run).

* Added `docs/reference/research/issue-470-live-2026-11-22.md`; index row in `docs/reference/README.md`; log entry in `docs/reference/log.md`.
* Validation: `python3 -m unittest tools.test_rpi_checks -q` 123 tests OK; links checked by review and diff.

## Acceptance criteria, issue 470

| Criterion | Status | Evidence |
| --- | --- | --- |
| `--changed` selects groups, records scope | Proven (ticked) | 123 tests OK |
| `--verify-receipt` rejects partial receipt | Proven (ticked) | 123 tests OK |
| `--jobs` parallel groups, single lock | Proven (ticked) | 123 tests OK; heavy lock only for heavy groups (#2215) |
| Measured full-run time before and after recorded in the PR | Unproven | Needs two matched full gates and a PR; `--all` and PRs forbidden; speed-up PR #2272 unmerged; retained receipts non-comparable |
| Tests for group selection and receipt scope | Proven (ticked) | 123 tests OK |

Not run: full gate, hosted CI. Demo scope: no live Azure or browser proof applies.
