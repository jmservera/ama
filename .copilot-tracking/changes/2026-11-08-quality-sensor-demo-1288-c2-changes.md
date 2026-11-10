# Changes: #1288 C2 (2026-11-08, written 20:27Z)

Start head `7d2dcc08` (tree `025bf08b`); origin/main `6354b13f` fetched, not merged (c50 ancestry kept, no stack on #184). Research/plan/details committed first (`34409ed8`, `91227ca5`; header-time correction noted in them).

## Findings dispositions

| # | Disposition | Where |
| --- | --- | --- |
| 1 same-bucket reuse | `assistants.digest(snapshot)` (exact clock-free capture) is task id and staleness; coarse `scheduling_signature` only rate-limits scan/forecast | assistants.py |
| 2 uncited/edited leak | withheld consent stubs whole `output` and every event `output`/`edited_output` (list/detail/export/raw) | assistants.py |
| 3 relabel | `claim` records immutable `dispatch.trigger`; `review_flag` uses it; legacy tasks are not proactive | assistants.py |
| 4 unsampled control | `sensor_consumer_control_home(home_id, sensor_id)` index, filled by `configure` and one-time backfill; `consent` reads at most 101 rows per home, decline wins, incomplete is unknown | sensor_consumer.py, sensor_view.py |
| 5 future/horizon | as-of filter (not stored), 366-day window, 30-day context, `future_dated_excluded`, negative age is never fresh; UI states the rule | sensor_view.py, ops.js |
| a11y | account summary name now `<first name>, your account`, containing the visible text | app.js:188-190 |

README `src/core/README.md` updated. Tests: `src/api/tests/test_quality_sensors.py` (ReadModel, Http, AccountSummaryName).

## Raw light evidence (SQLite, venv /tmp/ama-1288-venv, imports resolve to the worktree tree; exits all 0)

* `/tmp/c2-sqlite-qs-3.txt` ReadModel+Http 42 tests OK (AccountSummaryName 1 test OK separately)
* `/tmp/c2-sqlite-test_assistants.txt` 120 OK skipped=58
* `/tmp/c2-sqlite-test_assistant_release.txt` 54 OK skipped=4
* `/tmp/c2-sqlite-test_sensor_consumer.txt` 37 OK; `..._sensor_ingestion.txt` 47 OK; `..._sensor_consistency.txt` 38 OK
* ruff check/format clean on changed Python tests/core sensor files; `node --check` app.js, ops.js OK
* Blob hashes: assistants ced7c460, sensor_view 2cec3087, sensor_consumer b389122a, test 6fb3165f (pre-final test edit), app.js b90ffba7, ops.js c21370fa

## PENDING (not run, not passed; no heavy admission)

Actual SQL Server (`ZF_TEST_MSSQL=1`, Mssql* variants and per-home index query-plan evidence), real Chromium/axe/keyboard/reflow rerun of the account-summary check and sensor states, `tools/rpi-checks.py --changed`, committed-tree import proof on a fresh install. The 62 skipped assistant tests are not SQL evidence.

## Not granted

No release, attestation, model call or activation. Existing proposal source signatures and the rules hash are invalidated again.
