# Issue 1259 live changes (2026-11-19)

No source change. Tier FOCUSED (tracking records only). Refs #1259.

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1 Distinguish absent creatable dir from non-dir, dangling link, stat failure | Ticked in issue | Existing; HEAD tests pass |
| 2 Unusable inputs report archive-unreadable and unknown window | Ticked in issue | Existing; HEAD tests pass |
| 3 Absent-directory first run and path-free diagnostics preserved | Ticked in issue | Existing; HEAD tests pass |
| 4 Regular-file and dangling-link regressions for schedule/verify/publish, absent-dir coverage, failure before fix | Proven | `UnusableArchivePathTests`; 53 tests OK at HEAD; against pre-fix src (`a80acadaa`) the unknown-state, CLI exit, store-status and path-free tests fail |
| 5 Full receipt, independent exact-head assessment, hosted checks | Unproven | Needs rpi-checks --all, independent reviewer and hosted CI; not permitted or possible in this worker |
