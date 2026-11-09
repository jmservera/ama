---
title: Changes for #185 truthful action report (corrective)
ms.date: 2026-11-06
---

* `src/core/src/zava_forward/core/synthetic/device_provision.py`: `credentials` text now chosen by mode and action (`_CREDENTIALS`); field and type unchanged; docstring clarified for injected adapters. No new catches.
* `src/core/tests/test_device_provision.py`: strengthened dry-run assertion; added applied provision, applied teardown with the original manifest, and dry-run-with-adapters tests.
* RED on 117d with the new tests: `unittest discover -p test_device_provision.py` exit 1, 4 failures of 10 (log `/tmp/red185.log`). An earlier invocation `unittest tests/test_device_provision.py` exited 1 with an import error from the invocation style; it is not RED evidence.
* GREEN and checks from `src/core` using `/tmp/v185`, imports verified to resolve to this worktree: `unittest discover -p "test_device_*.py"` exit 0, 48 tests OK; `ruff check --no-cache .` exit 0; `ruff format --no-cache --check .` exit 0 (215 files); `mypy --cache-dir=/tmp/mypy-185-fix` exit 0 (268 files). Exits captured to `/tmp/*185.log`, not piped.
* Not run: FULL gate, images, SQL, browser. The receipt `/tmp/g185-full-r7-1105/receipt.json` applies only to 117d and is preserved.
* Original chronology failure (implementation created before artifacts, per `/tmp/rpi-185.log` lines 678, 681 and 710) is unchanged and not waived.
