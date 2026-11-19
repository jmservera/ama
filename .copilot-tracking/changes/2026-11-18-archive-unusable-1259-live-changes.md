# Changes: #1259 live lane

Files: docs/reference/research/2026-11-18-ranking-archive-unusable-1259-failing-first.md (new), docs/reference/README.md (index row), docs/reference/log.md (entry). No source change; tier FOCUSED (FULL not triggered).

Validation: core `test_ranking_publication_runner` + `test_ranking_publication` 110 OK (sequential); `UnusableArchivePathTests` 7 failures on `cd687abad^` source, OK on current. Markdown links checked by diff review. ruff/mypy not applicable (no Python change).

| Criterion | Proven? | Evidence |
| --- | --- | --- |
| AC1 creatable absence vs unusable | Proven (ticked) | research note |
| AC2 unknown window, unreadable shape | Proven (ticked) | research note |
| AC3 first run and path-free diagnostics | Proven (ticked) | research note |
| AC4 regressions + failure before fix | Proven here | 7 failures before, OK after |
| AC5 FULL receipt, exact-head assessment, hosted checks | Unproven | no src change so FULL not run; receipt, independent assessment and hosted CI are outside this candidate |
