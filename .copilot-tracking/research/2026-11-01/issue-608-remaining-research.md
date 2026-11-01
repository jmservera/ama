# Research: issue 608 remaining criteria

* Task: issue-608-remaining. Head: 37283f6ce (origin/main).
* Prior merged PRs: #610 (admit_browser_output preflight, code and tests), #626 and #718 (evidence-only RPI records).
* Criterion 1 (long paths fail before expensive checks): proven by #610; `--out` of 58 bytes accepted, 59 rejected with a measured-length diagnostic.
* Criterion 2 (boundary, cleanup, receipt contracts): proven by regression tests in tools/test_rpi_checks.py; re-run this pass: 55 tests OK.
* Criterion 3 (full browser and SQL groups execute without skips on the supported path): unmet. It requires a live full gate with a short external `--out`, which the owner scoped out locally; hosted validation is pending: source CI's pull-request path filter (`.github/workflows/src-ci.yml:4-6`) excludes this tracking-only diff, so no hosted run covers it. A linked run and tested revision are required later and remain distinct from this unmet criterion.
* Disposition: executed (issue, PR bodies and tests re-read). Planning Readiness: Ready.
