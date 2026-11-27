# Issue 1259 live r11 changes (2026-11-27)

Tier: FOCUSED (test-only; no `src/core/src` change; `rpi-checks.py --all` not run). Refs #1259.

## Changes

* `src/core/tests/test_ranking_publication_runner.py`: `verify_with_race` helper and `test_path_replaced_after_the_first_stat_is_unknown_not_empty`. The archive is absent at the first `os.stat`; it becomes a regular file or a dangling link before `_require_creatable` classifies it. Expected: `problem`, latest and overdue null, one path-free problem.

## Validation

* `test_ranking_publication_runner` plus `test_ranking_publication`: 113 tests, OK.
* Red-before by mutation (`_names` returns `[]` without `_require_creatable`): 4 failures, both new subtests (regular_file, dangling_link) and two existing dangling cases. Source restored; `git diff` shows tests only.
* ruff check and format pass. `python3 -m mypy` in `src/core` reports 3 pre-existing errors in `telemetry.py` and `device_provision.py`, none in touched files.
* Azure: not applicable; the apps are image-based and have no ranking publication job. No resource created, no credential read.

## Per-criterion status

| Criterion | Status | Evidence |
| --- | --- | --- |
| Distinguish creatable absence from non-directory, dangling link, stat failure | Proven | Existing tests; now also the check-then-use race |
| Unusable inputs report unreadable shape and unknown window | Proven | `check_unknown` scenarios; race test |
| Preserve absent-directory first run and path-free diagnostics | Proven | `test_absent_directory_stays_creatable_for_first_run`; path-free assertions |
| Regular-file and dangling-link regressions for schedule/verify/publish plus absent coverage; failure before fix | Proven | 113 tests OK; mutation red above; original pre-fix red in the 2026-11-18 notes. Ticking stays with the owner |
| Original RPI, FULL receipt, independent exact-head assessment, hosted checks | Unproven | Owner/coordinator gate: no src change so no FULL receipt applies; independent assessment and hosted CI need a push, which is forbidden to this worker |
