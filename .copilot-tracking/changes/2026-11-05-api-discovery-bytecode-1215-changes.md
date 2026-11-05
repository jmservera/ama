---
title: Changes - API discovery bytecode policy move (#1215)
description: Implementation record, adverse before-state, validation evidence and divergences
ms.date: 2026-11-05
ms.topic: reference
---

## Changes

* `tools/rpi-checks.py`: new `Runner.install_bytecode_policy()` holds the existing two writes unchanged (`<out>/browser-bytecode-policy.pth` and `<api venv>/lib/python3.12/site-packages/00-rpi-bytecode.pth`, payload `import sys; sys.dont_write_bytecode = True`). `Runner._install` calls it for `api` right after `metadata_cleanup()`, covering both `project-api` and `setup-api`. The old copy in `Runner.browser()` is removed. No other group, receipt-verification, scrubbing, dirty-snapshot or cleanup code changed.
* `tools/test_rpi_checks.py`: `test_api_install_prevents_scrubbed_server_child_writing_source_bytecode` runs the real `Runner._install("api")` (only `command` patched; `python3 -m venv --without-pip` really executes), then the real `design_system_browser_check.main()` server launch (Playwright import stubbed, no-op browser callback, minimal data, `ROOT` patched to a scratch copy of `src/{core,agents,api}/src`, `sys.executable` patched to that venv's python). Asserts the loopback server responded, no `__pycache__` or `*.pyc` under the scratch source roots, and the receipt policy file exists.
* `src/README.md` and `docs/reference/log.md`: short documentation and log entry.

## Before and after (real process results)

* Before (unchanged `tools/rpi-checks.py`, new test only): exit FAILED (failures=1). The first assertion run showed the policy file missing; after reordering assertions so the behavioural check runs first, the failure was `Lists differ` with three created directories: `.../src/agents/src/zava_forward/agents/__pycache__`, `.../api/src/zava_forward/api/__pycache__`, `.../core/src/zava_forward/core/__pycache__`. The server responded before that, so the real producer path ran.
* After: `Ran 1 test ... OK`.
* `python3 -m unittest tools.test_rpi_checks` (clean env, `PYTHONDONTWRITEBYTECODE=1`, Python 3.12.3): Ran 86 tests, OK, no skips reported, exit 0. The "Required command interrupted: TimeoutExpired" text in that output is expected fixture output from existing tests.
* `ruff check/format --isolated` (ruff 0.17.3 locally; the gate pins 0.17.1) on both tool files: clean.

## Divergences and limitations

* The test fixture's temporary directory is removed by the existing `setUp` cleanup used by every test in this file; no gate, receipt or snapshot evidence was deleted.
* A direct reproduction outside the test (scratch copy in `/tmp/issue1215-scratch-1105`, system Python, scrubbed env) also created `__pycache__` under core, agents and api; that scratch directory is retained.
* Not done: sealed-receipt or resume test for `setup-api` (non-blocking critique note); the maintained Runner UI smoke and focused gate run are recorded after the candidate commit.
* No complete gate, fresh full receipt, SQL, image, scanner or browser-geometry run. `/tmp/g96-c6-1105a` was read only.
