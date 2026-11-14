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

## Cycle 1 validation

* Hosted `src-namespace` ruff step reported `All checks passed!`; no source change was required.
* From the repository root (`pyproject.toml` applies): `ruff check` and `ruff format --check` on `tools/ci-affected.py` and `tools/test_ci_affected.py` pass (ruff 0.17.3).
* `python3 -m unittest tools/test_ci_affected.py -v`: 25 tests OK.
* `python3 tools/rename-zava-tests.py`: 25 tests OK in a temporary venv with python-pptx, pillow and pyyaml; the system interpreter lacks pptx and PIL (7 environment errors, not code defects).
