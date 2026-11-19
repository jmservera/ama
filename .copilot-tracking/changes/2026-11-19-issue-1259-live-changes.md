# Changes: issue 1259 live DEMO (2026-11-19)

Plan: [plan](../plans/2026-11-19-issue-1259-live-plan.md). No `src` change; tier FOCUSED.

## Files

* Added `docs/reference/research/2026-11-19-ranking-archive-unusable-1259-live-r3.md`.
* Edited `docs/reference/README.md` (index row) and `docs/reference/log.md` (entry).

## Per-criterion status (issue 1259)

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Distinguish creatable absence from non-directory, dangling link, stat failure | Proven (ticked) | `_names`, `_require_creatable`; tests |
| 2 | Unknown window and archive-unreadable shape, no healthy-empty fallback | Proven (ticked) | `check_unknown` assertions |
| 3 | Preserve absent first run and path-free diagnostics | Proven (ticked) | absent-directory tests, path-free assertions |
| 4 | Regressions for regular file, dangling link, absent; failure before fix | Proven | Red: Ran 6, failures=7 on `cd687abad^`; green: 110 OK on `1dddac2e0` |
| 5 | Original RPI, FULL receipt, independent exact-head assessment, hosted checks | Unproven, not provable for the demo | No src change so FULL not triggered, `--all` not run; independent assessment and hosted CI for a pushed head are outside this local candidate |

## Validation

* `PYTHONPATH=src:tests python3 -m unittest test_ranking_publication_runner test_ranking_publication -q` in `src/core`: 110 tests OK.
* Red overlay: failures=7 (see research note).
* mypy and ruff: not applicable, no Python changed.
* Markdown link review and `git diff --check`: see review record.
