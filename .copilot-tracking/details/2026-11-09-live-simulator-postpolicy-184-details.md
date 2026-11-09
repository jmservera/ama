---
title: "#184 post-policy validation details (prospective)"
ms.date: 2026-11-09
---

Details for [the plan](2026-11-09-live-simulator-postpolicy-184-plan.md). Commands are fixed here before any run. W is the worktree root; V is /home/azureuser/venv-184; logs go to /home/azureuser/logs-184-pp (outside the repository, not committed).

## P2 merge

* `git fetch origin main`, verify `git rev-parse origin/main` equals 76db469b16e7ac0ae862e8c9b19873fc66b04f0e, then `git merge --no-ff 76db469b16e7ac0ae862e8c9b19873fc66b04f0e -m "merge: current origin/main (76db469b1) into recovered 184 parent"` with the repository-local noreply identity and the Co-authored-by trailer. Verify `git merge-base --is-ancestor 14ce745 HEAD` and `... 76db469 HEAD`; `git diff --name-only HEAD^1 HEAD -- src infra tools` must list only src/README.md (policy text) and no source, infra or tool path.

## P3 environment

* `V/bin/python -c` printing `zava_forward.core.__file__`, `zava_forward.api.__file__`, `zava_forward.agents.__file__` (all must be under W) and `python --version`; `V/bin/pip list` for mssql-python, ruff, mypy.

## P4 non-heavy checks (V/bin/python)

* core, from W/src/core: `-m unittest discover -s tests -p "test_sensor*.py" -q`, `-p "test_device*.py"`, `-p "test_live*.py"`, `-p "test_resident_sensors.py"`, plus `test_historical_backfill.py` and `test_retrofit_scenarios_retained_store.py` (critique C3: they exercise changed consumer and analysis-store paths). Every run uses `-v` and the log is parsed for the number of tests, `skipped=` and each skip reason; zero discovered tests fails the check, and skips are listed by name in the changes record as offline opt-in, never as SQL proof.
* api, from W/src/api with `PYTHONPATH=../core/tests:../agents/tests`: patterns `test_live*.py`, `test_iot*.py`, `test_sensor*.py` (includes test_sensor_sql_check, test_sensor_consistency, test_sensor_ingestion).
* tools, from W: `-m unittest tools.test_rpi_checks -q` (or discover with -p test_rpi_checks.py -s tools if module import fails).
* lint, from W: `ruff check` and `ruff format --check` on the modified Python files under src/api, src/core and tools (list from `git diff --name-only 76db469...HEAD -- '*.py'` after the merge). Type: `mypy --strict tools/rpi-checks.py tools/test_rpi_checks.py` (the runner's own TYPE_GROUPS contract) and `mypy` per package config on modified api and core source modules. Tool install only after absence failure: `pip install ruff==0.17.1 mypy==2.4.0` into V.
* bicep, from W: `az bicep build --file F --stdout` and `az bicep lint --file F` for infra/live-receiver-job.bicep, infra/live-simulator-job.bicep, infra/iot-hub-live.bicep, infra/modules/iothub.bicep and infra/modules/iothub-scope-guard.bicep. `REQUIRE_AZ_BICEP=1 V/bin/python -m unittest discover -s infra/tests -p "test_iothub_module.py" -v` and the same for test_bicep_policy.py and test_container_contract.py. If a module needs a missing prerequisite, report it as missing.
* Skips from offline opt-in SQL classes are copied verbatim into the changes record under their own heading.

## P5 owned SQL (heavy; non-queued admission)

* Admission: `flock -n -E 99 /tmp/ama-rpi-heavy.lock` wrapping the command, so lock contention is the distinct status 99 and a test exit 1 is not confused with busy; nothing heavy starts on 99. Run under `set -o pipefail` and capture the command status (`PIPESTATUS[0]`), never the status of `tee`. Retry with bounded spacing while doing other work. Holder identity is read with `fuser -v` before reporting busy.
* Default: the admission wrapper around `V/bin/python src/api/checks/sensor_sql_check.py 2>&1 | tee LOGS/sql-default.log` with `PIPESTATUS[0]` recorded; accept only exit 0 with a verbatim `Ran 70 tests`, `OK` and no `skipped=`; the harness validates exit status only for this selector, so the log parse is the skip check (strictness is applied here, not by editing the harness).
* Analysis: same with `--selector analysis`; accept only `Ran 10 tests`, `OK`, no skips, `Selector analysis: accepted`, exit 0. Test identity (critique C5): run with the harness's verbose output retained when available, and independently compare the ten test names found by `unittest` discovery of test_sensor_analysis_mssql against the ten Mssql names in SENSOR_MSSQL_REQUIRED_TESTS in tools/rpi-checks.py (a read-only listing, not a heavy run). For the default selector compare the 70 executed ids to the six selectors the same way. The earlier rejected exit 1 and corrected exit 0 stay in the original records and are cited, not re-created.
* Each run uses the harness's task-owned loopback container that it removes. Verify afterwards with `docker ps -a` that the task container is gone and that the other lane's container is untouched. No global prune.
* The selectors counted before: six default selectors (verified by reading DEFAULT_TESTS, plus the unit test asserting six), analysis pinned via ANALYSIS_TESTS 10 and the two added names in SENSOR_MSSQL_REQUIRED_TESTS.

## P6 static guard assertions

* Produce a guard table: guard, executing test name, backend (offline mocks, offline fake store or owned SQL), outcome. Guards the tests do not execute are listed as uncovered. Exact-grant main entrypoint and rejected data-quality SQL stay open unless a test proves them. Read tests and source for MAX_COHORT 100, MAX_WINDOW 14 days, admin cohort grant, rejected data-quality, replay, window and dedup tests; list the test names that cover each.
* `git diff 14ce745^2..` style comparison is not needed; instead `git diff origin/main HEAD -- tools/rpi-checks.py` must show exactly two added names in SENSOR_MSSQL_REQUIRED_TESTS and no runner logic.
* `grep -rniE "(SharedAccessKey|AccountKey|BEGIN (RSA|PRIVATE)|password\s*=)" ` limited to the changed non-test source and infra files; test fixtures with fake values are noted as such.
* Read test_live_receiver_sql.py for exact-grant main entrypoint and rejected-data-quality coverage and state the C5 Low gaps' status (open or closed) from what the file contains.

## Re-run and pending evidence

After any correction rerun every affected check and record the final HEAD. Hosted CI and independent exact-head review are recorded as pending; none is claimed.

## Rollback and boundaries

No source edit is planned. Any correction is limited to a tightly coupled failing test or fixture, is preceded by a recorded failing output and its own mini plan entry, and counts against the five total correction cycles per issue only as the owner's repository default requires; spent cycles are not reset.
