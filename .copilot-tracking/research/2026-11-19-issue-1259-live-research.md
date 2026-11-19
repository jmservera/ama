# Issue 1259 live research (2026-11-19)

Research disposition: executed. Planning Readiness: Ready.

## Findings

* Criteria 1 to 3 are already ticked in the issue.
* The fix and the regressions landed together in commit cd687abad (#1328): `UnusableArchivePathTests` in `src/core/tests/test_ranking_publication_runner.py` covers regular file, dangling link, dangling ancestor and stat failure for verify, schedule, publish and exercise, a main() exit-code test, and absent-directory first-run tests.
* Criterion 4 gap: "demonstrate failure before fix" has no recorded evidence. It can be proven locally by running the current tests against the source tree of cd687abad^.
* Criterion 5 (FULL receipt, independent exact-head assessment, hosted checks) needs a human and hosted CI; the brief forbids `rpi-checks.py --all`. Unprovable for the demo.
* No source change is needed, so the tier is FOCUSED. Live Azure is not relevant to a local filesystem path guard.
