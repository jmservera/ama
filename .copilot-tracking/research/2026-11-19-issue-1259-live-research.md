# Issue 1259 live research (2026-11-19)

Planning Readiness: Ready. Research disposition: executed.

Open criteria: (4) regular-file and dangling-link regressions for schedule/verify/publish plus absent-directory coverage, with failure shown before the fix; (5) FULL receipt, independent exact-head assessment and hosted checks.

Findings:
* `UnusableArchivePathTests` in `src/core/tests/test_ranking_publication_runner.py` already covers regular file, dangling link, dangling ancestor and stat failure across verify, schedule, publish and exercise, plus the absent-directory first run tests. Landed with #1328.
* Pre-fix source (`a80acadaa`) with HEAD's tests fails: regular_file/dangling_link/dangling_ancestor/stat_failure report `overdue True` instead of unknown, CLI exits 0, store status has no problems.
* Criterion 5 needs a full receipt, independent assessment and hosted CI; owner decision forbids rpi-checks --all here.
* Azure not needed: the behaviour is local filesystem only.
