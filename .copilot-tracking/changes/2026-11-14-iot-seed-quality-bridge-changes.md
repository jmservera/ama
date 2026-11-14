---
title: IoT seed to Quality UI bridge changes
task_slug: iot-seed-quality-bridge
date: 2026-11-14
---

## Changes

* Added `src/api/tests/test_iot_seed_to_quality_ui_bridge.py` (7 tests, strict-mypy clean, ruff clean). No source changes.
* The module prepends its own directory to `sys.path` because sibling test fixtures import by bare name and the required `tests.<module>` invocation does not otherwise provide it.

## Divergences

* No CO2 channel exists in the generator or read model, so tests assert CO2 is absent (moisture = `humidity_pct`) instead of flowing a CO2 value.
* The shared interpreter's editable `zava_forward` installs point at a stale checkout (`/home/azureuser/source/ama`) without `sensor_view`. Validation ran in a throwaway venv (`/tmp/zfvenv-1003`, `--system-site-packages`, `--no-deps -e` of this worktree's `src/{core,agents,api}`), then removed.

## Validation

* unittest (command as given, venv python): 7 tests OK.
* `ruff check`, `ruff format --check`, `mypy` on the file: clean.
* Local-only focused tier; no hosted CI observed; no push.
