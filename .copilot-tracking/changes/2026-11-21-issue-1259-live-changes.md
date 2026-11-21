# Changes: issue 1259 live DEMO (2026-11-21)

Plan: [plan](../plans/2026-11-21-issue-1259-live-plan.md). No `src` change; tier FOCUSED. `rpi-checks.py --all` not run.

## Files

* Added `docs/reference/research/2026-11-21-ranking-archive-unusable-1259-live-r4.md`.
* Edited `docs/reference/README.md` (index row) and `docs/reference/log.md` (entry).

## Per-criterion status (issue 1259)

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Distinguish creatable absence from non-directory, dangling link, stat failure | Proven (ticked) | tests green, 110 OK |
| 2 | Unknown window and archive-unreadable shape, no healthy-empty fallback | Proven (ticked) | `UnusableArchivePathTests` green |
| 3 | Preserve absent first run and path-free diagnostics | Proven (ticked) | absent-directory and path-free tests green |
| 4 | Regressions for regular file, dangling link, absent; failure before fix | Proven | Red on `cd687abad^`: Ran 6, failures=7; green on `d2585a4c9`: 110 OK; stat failure mocked |
| 5 | Original RPI, FULL receipt, independent exact-head assessment, hosted checks | Unproven, not provable for the demo | No src change so FULL not triggered; nothing pushed, so no hosted run or independent assessment of a head exists |

## Validation

* Red overlay and `PYTHONPATH=src:tests python3 -m unittest test_ranking_publication_runner test_ranking_publication -q` in `src/core`: 110 OK.
* mypy and ruff: not applicable, no Python changed.
