# Changes: issue 107 restarted-process allowance clamp test

Date: 2026-11-08. Base `eb7e62b6f` (planning commit) on main `2e0c676ad`.

| Path | Change |
| --- | --- |
| `src/api/tests/test_assistant_release.py` | One method `test_restarted_processes_keep_partially_used_allowance_and_stop_at_stored_calls` in the `ProcessRaces` mixin (25 lines); inherited by the SQLite and `MssqlUnleasedRevocation` classes |
| `.copilot-tracking/...` | Changes, review and state records |

No helper, production, runner, store, rubric, schema or doc change.

## Raw LIGHT evidence

Venv `/home/azureuser/.local/share/ama/gates/g107-clamp-light-r1/venv` (pip, editable installs). `zava_forward.core` and `zava_forward.api` resolve inside this worktree. The three generated egg-info folders were moved by explicit path to `.../egg/` afterwards. Env: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests`, run from `src/api`.

| Command | Result |
| --- | --- |
| `python -m unittest -v test_assistant_release.SqliteUnleasedRevocation test_assistant_release.MssqlUnleasedRevocation` | exit 0, 8 tests, `OK (skipped=4)`; the three SQLite process methods `ok` (the new one first time, no earlier failure); all four MSSQL rows skipped (`needs disposable SQL Server (ZF_TEST_MSSQL=1)`) |
| `python -m unittest test_assistant_release test_assistants` | exit 0, 174 tests, `OK (skipped=62)` |
| `ruff check .` | exit 0 |
| `mypy` | exit 0, 190 files |
| formatter on the excluded test file | whole file differs from baseline (pre-existing); the added 25-line block is unchanged by the formatter |
| `git diff --check` | clean |

Mutation check: temporarily replaced the `min()` clamp at `assistants.py:918` with the configured limits. Only the new method failed; the merged process tests still passed, so the gap is closed. The production file was restored (`git checkout`) and the tree showed only the test change.

## Not run

No SQL server, Docker, gate runner, browser, scanner or image. The MSSQL method is unexecuted and actual SQL is unverified.

## Future actual-MSSQL selection

`SQL_SELECTORS` in `tools/rpi-checks.py` includes `test_assistant_release.MssqlUnleasedRevocation`, so the maintained SQL group discovers the new method with no runner change. FULL command shape, later and only after admission: `python3 tools/rpi-checks.py --all --base <current-origin-main> --out <new external dir> --jobs 2 --lock-timeout 0 < /dev/null`; the SQL log must show `test_restarted_processes_keep_partially_used_allowance_and_stop_at_stored_calls (test_assistant_release.MssqlUnleasedRevocation...) ... ok`.
