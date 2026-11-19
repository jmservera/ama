---
title: Issue 470 live audit changes
ms.date: 2026-11-18
---

Tier: FOCUSED, docs-only. No `src/` change; `rpi-checks.py --all` not run. Refs #470.

## Files

* `docs/reference/research/issue-470-live-20261118T1639Z-2026-11-18.md` (new audit note)
* `docs/reference/README.md` (index row), `docs/reference/log.md` (entry)

## Per-criterion result

| # | Criterion | State |
| --- | --- | --- |
| 1 | `--changed` selects groups, records scope | Proven (tests pass) |
| 2 | `--verify-receipt` rejects partial where full required | Proven (tests pass) |
| 3 | `--jobs` parallel within lock and limits | Proven (worker-limit tests pass) |
| 4 | Measured full-run before/after in the PR | Unproven: full gate not run (brief), only prior full attempt failed with exit 124, changed tier not comparable |
| 5 | Tests for selection and receipt scope | Proven (109 of 109 pass) |

## Validation

* `python3 -m unittest tools.test_rpi_checks -q`: 109 tests, OK.
* mypy, ruff and web tests: not applicable (no Python or web file changed).
* Hosted CI for the exact head: not observed (no push by this task).
