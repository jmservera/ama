---
title: Details - API discovery bytecode policy move (#1215)
description: Phase details for the focused gate correction
ms.date: 2026-11-05
ms.topic: reference
---

## Phase 1: regression (fails before)

* File: `tools/test_rpi_checks.py`, new test in `GateTests` near the existing Runner install tests (around `test_runner_installs_isolated_chromium_before_project_api_tests`).
* Build a real `gate.Runner` as the neighbouring tests do. Patch only `runner.command` so `python3 -m venv <dir>` really runs (creating the real api venv at `runner.envs / "api"`, `with_pip` default is acceptable) and pip commands are no-ops; run the real `Runner._install("api", ["core", "agents", "api"])` (the real method, including `metadata_cleanup`).
* Revised after critique: the child is the real `design_system_browser_check.main()` server (Playwright import stubbed with a fake module, browser callback a no-op, minimal `{"cases": [], "staff": []}` data, `ROOT` patched to a scratch copy of `src/{core,agents,api}/src`, `sys.executable` patched to the venv python created by the real `_install`). Replaces the generic-child design above.
* Using that venv's python as `sys.executable` of a child, start a real child process with the producer's scrubbed environment: only `PATH`, `HOME`, `LANG` and `PYTHONPATH` to a temporary source package (the allowlist in `src/api/checks/design_system_browser_check.py` `main`). The child imports the temp package.
* Assert exit code 0, that the imported module's `__file__` is under the temp source tree (import-source identity), and that no `__pycache__` exists in that tree.
* Before the change the venv has no policy at this point, so the child writes `__pycache__` and the assertion fails.
* Additionally assert `<out>/browser-bytecode-policy.pth` exists (receipt evidence required when browser executes) and, with a second `_install("namespace", ...)` not needed, no policy is written for other environments.

## Phase 2: move policy

* File: `tools/rpi-checks.py`. Add `Runner.install_bytecode_policy(self)` holding the two existing writes unchanged (same payload and filenames). Call it from `_install` after the final install/metadata cleanup when `name == "api"`, before the closing `pip check` is acceptable; place it right after `metadata_cleanup()`.
* Remove the old block and its comment in `Runner.browser()`, keeping `try:`; keep the "unchanged harness scrubs its server environment" rationale on the new method.

## Phase 3: validation

* `python3 -m unittest tools.test_rpi_checks` equivalent per tooling guide (existing command), the new test before and after, `python3 tools/rpi-checks.py --changed`.
* Maintained real Runner UI smoke: only applicable if the focused tier selects a browser group; otherwise report why not applicable and the exact prerequisite (heavy lock). Do not rerun the failed full gate.
* Heavy lock `/tmp/ama-rpi-heavy.lock` nonblocking for any browser/server run.

## Phase 4: handoff

* Commit with repo-local `8036360+jmservera@users.noreply.github.com`, Copilot trailer, no hook suppression. Add a `docs/reference/log.md` entry and documentation note where gate behaviour is documented.
