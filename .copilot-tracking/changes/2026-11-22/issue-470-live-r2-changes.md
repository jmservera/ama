---
title: Issue 470 live changes r2 (2026-11-22)
ms.date: 2026-11-22
---

Tier FOCUSED (no src change; `rpi-checks.py --all` not run). Refs #470.

## Changes

* Added docs/reference/research/issue-470-live-r2-2026-11-22.md, an index row in docs/reference/README.md and a log entry.

## Validation

* `python3 -m unittest discover -s tools -p 'test_rpi_checks*.py'`: 128 tests, OK.
* Not run: hosted CI (no push), full gate.

## Per-criterion table

| # | Criterion | State | Evidence |
| --- | --- | --- | --- |
| 1 | `--changed` selects groups, records scope | Proven | 128 tests pass |
| 2 | `--verify-receipt` rejects partial receipts | Proven | 128 tests pass |
| 3 | `--jobs` parallel within lock rule | Proven | 128 tests pass |
| 4 | Measured full-run time before and after in the PR | Unproven | No matched full-gate pair; `--all` and PRs forbidden; PR 2272 now merged but no timing recorded |
| 5 | Tests for group selection and receipt scope | Proven | 128 tests pass |
