# Issue 1259 live changes (2026-11-19)

No source, test or knowledge-base change. Criterion 4 is already proven by [the failing-first note](../../docs/reference/research/2026-11-18-ranking-archive-unusable-1259-failing-first.md) and [the live second audit](../../docs/reference/research/2026-11-18-ranking-archive-unusable-1259-live-r2.md); a new note would duplicate them. Tier: FOCUSED.

Re-run today: `cd src/core && PYTHONPATH=src:tests python3 -m unittest tests.test_ranking_publication_runner -q` gave 53 tests, OK. The same `UnusableArchivePathTests` class against the `cd687abad^` source (git archive to /tmp, removed afterwards) gave 6 tests, `FAILED (failures=7)`, with the representative mismatch `('problem', None, True)` against `('problem', None, None)`.

| Criterion | Status | Evidence |
| --- | --- | --- |
| Distinguish absent creatable from unusable path | Proven (ticked) | prior notes, current tests |
| Unknown window, archive-unreadable shape | Proven (ticked) | `check_unknown` |
| Preserve first run and path-free diagnostics | Proven (ticked) | absent-directory tests |
| Regressions and failure before fix | Proven (re-observed today) | runs above |
| FULL receipt, independent exact-head assessment, hosted checks | Unproven | human and hosted gates; `rpi-checks.py --all` forbidden; no src change |

Remaining criterion is human or hosted only, so implementation stops here.
