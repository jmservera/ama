<!-- markdownlint-disable-file -->
# Issue 189 current-main integration phase details (2026-11-09)

Plan: [plan](../../plans/2026-11-09/current-main-integration-189-plan.md).

## P2 Merge

* `git status --short` empty; `git rev-parse HEAD^` equals `b933c2f606b394469b53f702824b707e6fc3548d`; `git config --local user.email` equals the noreply address (confirm `gh api user`); `git fetch origin`; `git rev-parse origin/main` must equal `3a9767d5cf728c5e3be76813ce0bfdac4c06841e`, else STOP and report.
* `git merge --no-ff origin/main` with a Conventional Commit message and the Copilot trailer. Read-only merge-tree was clean. No file overlap under `src`.

## P3 Differences

* `git diff b933c2f60 HEAD --stat -- src tools` equals main's delta since `8d6f029ca`.
* `git diff b933c2f60 HEAD -- src/api` is empty (no main change under `src/api`); hash `live_simulator.py` and `test_live_simulator.py` and compare with the C4 recorded `5195ff4a...` and `ccf4cd06...`.

## P4 Composition read

* `git diff 8d6f029ca origin/main -- src/core/src/zava_forward/core/store.py`: `audit` unchanged. `grep -rn "azure.iot" src/core` is empty; in the API `iot_stream.py` and `live_receiver.py` import the SDK at top level by design, and the reachable chain from `server` -> `simulator_admin` -> `live_simulator` must not import them (proved by import in the SDK-free interpreter).

## P5 Checks

Scratch `mktemp -d /tmp/i189-curmain-XXXXXX`; producer exit files, no pipes; `unset ZF_RESIDENT_AZURE_TEST ZF_RESIDENT_MSSQL ZF_SQL_SERVER ZF_SQL_TASK_MANIFEST`.

* Reduced SDK-free venv (critique 1, 2; `azure-iot-device` is a declared API dependency, so this is a deliberately reduced install): `python3 -m venv $S/base`, `pip install --no-deps ./src/core ./src/agents ./src/api` plus `aiohttp==3.14.5 azure-identity==1.26.0` and the packages the three SDK-free test modules import; `python -c "import azure.iot.device"` must fail; with that interpreter import `zava_forward.api.server` and `zava_forward.api.simulator_admin` and run `test_live_simulator test_simulator_admin test_live_control` (SDK-free subset); keep the scrubbed-server contract test with that interpreter per the test's own install logic from `tools/` (`python3 -m unittest test_rpi_checks.GateTests.test_api_install_prevents_scrubbed_server_child_writing_source_bytecode`). Record the interpreter and module paths.
* `tools`: `python3 -m unittest test_rpi_checks`.
* API tests from `src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests`: `test_live_simulator test_simulator_admin test_live_control test_iot_stream test_iot_credential_hygiene test_sensor_consistency`.
* Core impacted by the merge and the Store dependency: from `src/core`, `PYTHONPATH=tests` `test_gates test_quality_procurement test_resident_decisions` (SQL cases skip, reported).
* Lint/type: `pip install ruff==0.17.1 mypy==2.4.0` in the owned venv; from `src/api`: `mypy` (pyproject profile) and `ruff check` / `ruff format --check` over `src/zava_forward/api/live_simulator.py tests/test_live_simulator.py checks/simulator_control_browser_check.py` (paths relative to `src/api`) and the other affected 189 files; tools: `ruff` and `mypy --strict tools/rpi-checks.py tools/test_rpi_checks.py` per `src-ci.yml`.
* Browser: from `src/api` with `PYTHONPATH=tests:../core/tests:../agents/tests`, Playwright 1.64.0 and `google-chrome`; `flock -n /tmp/ama-rpi-heavy.lock` held until the browser process exits; if busy, skip and report BLOCKED-BY-HOLDER with independent work done; else one `python -m checks.simulator_control_browser_check --axe <asset>` run. Asset sha256 verified before use.

## P6 Evidence

Changes, review, state, handoff in the coordinator files directory. Raw logs stay out of the commit. Report HEAD, tree, base, C4 source equivalence (hashes), counts, exits, skips.
