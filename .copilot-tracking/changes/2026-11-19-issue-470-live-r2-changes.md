---
title: Issue 470 live r2 changes (2026-11-19)
ms.date: 2026-11-19
---

Tier FOCUSED; documentation-only, no `src/` or `tools/` change. No test run (nothing changed; the 113-test gate suite result is recorded in [the earlier note](../../docs/reference/research/issue-470-live-2026-11-19.md)).

| # | Criterion | State | Reason |
| --- | --- | --- | --- |
| 1 | `--changed` selects groups, records scope | Proven (ticked) | prior evidence |
| 2 | `--verify-receipt` rejects partial receipts | Proven (ticked) | prior evidence |
| 3 | `--jobs` parallel groups, single lock | Proven (ticked) | prior evidence |
| 4 | Measured full-run time before and after in the PR | Unproven | needs two `--all` runs and a PR; both forbidden |
| 5 | Tests for selection and receipt scope | Proven (ticked) | prior evidence |
