# Research 1258/1259 (2026-11-23)

Research disposition: executed. Planning Readiness: Ready.

Both fixes are already on main: ancestor fsync in `_confirmed` (ranking_publication.py) and non-directory, dangling-link and stat-failure classification in `_require_creatable`, with `UnusableArchivePathTests` in test_ranking_publication_runner.py. Unticked criteria: #1258 AC5 (process gates); #1259 AC4 (regression tests, failure before fix) and AC5 (process gates). Plan: rerun tests, mutate each fix to show failures, record a research note; no src change.
