# Issue 1259 live r11 research (2026-11-27)

Scope: synthetic demo, desktop only. Core filesystem logic; no Azure resource, credential or model call.

## Findings

* Fix and regressions for criteria 1 to 4 are on main (`02e63b0690`, `d8f1aa5f6d`); the baseline run of `test_ranking_publication_runner` and `test_ranking_publication` gave 112 tests, OK.
* Ten earlier notes cover regular file, dangling link and ancestor, stat failure, ENOTDIR, ELOOP and EACCES. Remaining untested gap named in the r2 note: the check-then-use race in `_names` (path absent at the first `os.stat`, replaced by a regular file or dangling link before `_require_creatable` runs).
* Criterion 5 (FULL receipt, independent exact-head assessment, hosted checks) is a coordinator and human gate, not provable by a worker.
* Live Azure cannot prove this: the apps are image-based and no ranking publication job exists.

## Selected work

Add a deterministic race regression to `UnusableArchivePathTests` and prove it red by mutation. Planning readiness: Ready.
