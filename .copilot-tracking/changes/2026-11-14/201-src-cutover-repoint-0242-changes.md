---
title: Changes, src cutover repoint contract (Refs #201)
ms.date: 2026-11-14
---

## Changes

* Added `tools/test_src_cutover_repoint.py`.
* Added dated RPI artifacts under `.copilot-tracking/`.

## Validation

* `ruff check` and `ruff format --check` on the new file: pass.
* `python3 -m unittest tools/test_src_cutover_repoint.py -v`: 16 tests OK.
* `python3 tools/rename-zava-tests.py`: 25 tests, 7 errors from missing `pptx` and `PIL` modules in this environment. The same 7 errors occur on the unchanged baseline, so they are unrelated.

## Divergences

None. Live Azure health (deployed, healthy `src/` build) remains the separate Azure-only half of criterion 5 and is not claimed.
