---
title: Issue 80 r11 details
description: Exact edits, commands and proof steps for the r11 plan
ms.date: 2026-11-06
---

* Edit 1, `src/api/checks/design_system_browser_check.py`: add `scratch_parent()` returning `Path(ZF_BROWSER_SCRATCH)` (created with mkdir parents, must be absolute and outside ROOT) when set, else `ROOT / ".venv"` as today; add `child_env()` returning the PATH/HOME/LANG subset plus `PYTHONDONTWRITEBYTECODE` and `PYTHONPYCACHEPREFIX` when present in the caller environment; use both in `main`.
* Edit 2, new `src/api/tests/test_browser_harness_scratch.py`: unittest cases with `patch.dict(os.environ, clear=True)` for default parent, external parent, relative or in-repo refusal, and pass-through present or absent. No server, browser or network.
* Checks (new absent logs under `/mnt/ama-gates/e80-r11-r64-1106/logs/`, pipefail, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPYCACHEPREFIX` and tool caches under `/mnt/ama-gates/e80-r11-r64-1106/`): new unit module plus the nine r9 modules, Ruff CI-style on both files, component Ruff, format, mypy, py_compile via ast only.
* Byte identity: tree hashes of `src/api/src`, `src/core/src`, `src/agents/src`, `src/importer/src` equal at 1fa33543 and HEAD.
* Preservation under `/mnt/ama-gates/e80-r11-r64-1106/preservation/`: inventory TSV (type, mode, size, sha256, mtime) of the three caches and `.venv`; `git ls-files -s`/hashes of tracking snapshot; `tar --no-dereference` archive of the whole `.copilot-tracking` plus the exact generated members; readback listing compared to inventory; restore with `tar --no-same-owner` into a new empty directory, compare hashes and modes; protected-byte hashes of tracked source and tracking; pending manifest JSON listing the exact four paths, member counts, status `pending-root-authorisation`.
* Nothing is removed.
