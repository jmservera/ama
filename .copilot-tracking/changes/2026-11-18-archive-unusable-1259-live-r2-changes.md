# Changes: #1259 live audit run 2

Date: 2026-11-18. Tier: FOCUSED (documentation only; no `src` change, so FULL is not triggered and `rpi-checks.py --all` was not run).

Files: docs/reference/research/2026-11-18-ranking-archive-unusable-1259-live-r2.md (new), docs/reference/README.md (index row), docs/reference/log.md (entry), and the dated `.copilot-tracking` artifacts.

Validation: the pre-fix overlay ran `UnusableArchivePathTests`, 6 tests, `FAILED (failures=7)`; current main ran `UnusableArchivePathTests`, `test_ranking_publication_runner` and `test_ranking_publication`, 116 tests, `OK`; the real-filesystem repro matches the research note. mypy, ruff and the web checks do not apply (no Python or web file changed). Throwaway worktree and temp folders removed.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| 1 Distinguish creatable absence from unusable input | Proven (ticked) |
| 2 Unknown window and unreadable shape, no healthy-empty fallback | Proven (ticked) |
| 3 Absent-directory first run and path-free diagnostics preserved | Proven (ticked) |
| 4 Regressions for schedule/verify/publish plus absent coverage; failure before fix | Proven here with raw output |
| 5 FULL receipt, independent exact-head assessment, hosted checks | Unproven; not provable for the demo (human and hosted gates; no src change) |

Production-only items: none. Blob variant not exercised. Stat failure covered by a mocked test only.
