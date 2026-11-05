---
title: Gate Chromium prerequisite changes (#1208)
description: Implemented changes, commands and results for the Chromium ordering repair
ms.date: 2026-11-05
ms.topic: reference
---

## Changes

* tools/rpi-checks.py: new Runner.install_chromium; Runner.run calls it right after the api venv install when project-api is selected (before plan_shards and schedule); required_checks adds the identical command to the project-api contract; Runner.browser reuses the helper (same argv and 900 s timeout, so its contract is unchanged).
* tools/test_rpi_checks.py: three regressions: contract order, receipt rejected without the install, runner order and PLAYWRIGHT_BROWSERS_PATH.
* No change to EXPECTED_SKIP_REASONS, check names, SQL, security, human or closure gates.

## Commands and results

* Red reproduction on base ead177e with the new tests: 1 failure and 2 errors (no Chromium install in contract or runner).
* python3 -m unittest tools.test_rpi_checks: 85 tests OK after the change (a printed KeyboardInterrupt line comes from an existing timeout fixture).
* ruff check and ruff format --check (isolated, line length 100, E,F,I,B,UP, py312) on both files: pass.
* mypy --strict on both files: no issues.
* Not run: full gate, SQL, image and browser groups; no full-suite receipt for tooling.

## Native validation status (qualified)

* Nonqueued probe of /tmp/ama-rpi-heavy.lock on 2026-11-05 reported HELD (holder #96, PID 1232396, rpi-checks --all, --lock-timeout 0).
* The small native-browser check was therefore not run. Native execution of test_resident_summary_ai_ui with the installed browser is UNPROVEN. No sleeping or polling; no shared cache mutation.

## Preserved adverse evidence

* /tmp/rpi188-full-20261105T0740/receipt.json (SHA256 72b69ac4d11d7215b3d8c583385c98c6a807d59740cc82a4287000189e399ef8) and 0051-project-api.log are untouched and not used as evidence for this head.
