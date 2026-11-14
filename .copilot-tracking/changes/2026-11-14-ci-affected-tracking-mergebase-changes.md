---
title: ci-affected tracking paths and merge-base diff changes
ms.date: 2026-11-14
---

## Changes

* `tools/ci-affected.py`: added `is_inert_path` (`.copilot-tracking/` and unwatched docs Markdown skipped in `select`); `changed_files` now diffs `base...head`; docstring updated; file mode set executable (shebang present, ruff EXE001 required by the validation command).
* `tools/test_ci_affected.py`: tests for tracking/docs skipping, watched/non-Markdown docs widening, and `changed_files` (three-dot args, non-zero exit gives `None`, empty or zero base skips git).

## Validation

* `python3 -m unittest tools/test_ci_affected.py -v`: 25 tests OK.
* `ruff check` and `ruff format --check`: pass.
* Plan phases 1 to 4 complete. No divergences.
