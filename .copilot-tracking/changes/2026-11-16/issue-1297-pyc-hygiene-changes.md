---
title: "Issue 1297 gate bytecode hygiene changes"
ms.date: 2026-11-16
---

## Changes

* `tools/test_rpi_checks.py`: added `test_every_venv_install_prevents_scrubbed_child_writing_source_bytecode`. Run before the fix it failed for all five venv names (core, agents, orchestrator, importer, namespace) with a `__pycache__` written into the scratch source directory by a scrubbed-environment child.
* `tools/rpi-checks.py`: `_install` now calls `install_bytecode_policy(name)` for every venv. The policy writes `00-rpi-bytecode.pth` (`sys.dont_write_bytecode = True`) into each venv; the out-dir `browser-bytecode-policy.pth` receipt file is still written only for `api`. `clean_identity`, snapshot and skip/SQL logic are unchanged.

## Validation (local, targeted)

* `python3 -m unittest tools.test_rpi_checks`: 108 tests OK after the fix (run with PYTHONDONTWRITEBYTECODE=1).
* Gate-equivalent `ruff check --isolated --select E,F,I,B,UP` and `ruff format --check` on both files: clean (local ruff 0.17.3; the gate pins 0.17.1 and will rerun).

## Divergences and notes

* The first targeted test run (without the no-bytecode variable) created two ignored files in `tools/__pycache__`; the gate rejects ignored inputs in the source worktree, so exactly those two files and the empty directory were removed. No retained receipt, checkout, log or evidence was touched.
* A reproduction scratch directory recorded in `/tmp/pyc-repro-dir.txt` remains in /tmp.
