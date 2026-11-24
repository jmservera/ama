# Issue 470 changes (2026-11-24)

Tier FOCUSED, documentation only, no source edit, no `--all`, no Azure.

* Added docs/reference/research/issue-470-live-r9-2026-11-24.md (before/after timing record).
* Added docs/reference/README.md index row and docs/reference/log.md entry.
* Note: the implement-start witness recorded that docs edits predated it.

## Per-criterion table

| # | Criterion | State | Evidence |
| --- | --- | --- | --- |
| 1 | `--changed` selects groups, records scope | Proven (already ticked) | 129 gate tests (r3) |
| 2 | `--verify-receipt` rejects partial receipts | Proven (already ticked) | same |
| 3 | `--jobs` parallel within lock rule | Proven (already ticked) | same |
| 4 | Measured full-run time before and after recorded in the PR | Partly proven: figures recorded in r9; controlled same-head pair and PR entry unproven | `--all` and PRs forbidden; receipts differ in head, base, load; host load 7.45 |
| 5 | Tests for group selection and receipt scope | Proven (already ticked) | same |
