---
title: Issue 80 import conflict preview regression changes
date: 2026-11-14
task_slug: 80-import-conflict-preview-0008
---

## Added

* `src/importer/tests/test_import_conflict_preview.py`: five tests (source bytes/hash/mtime stability, blocking conflicts write nothing, row problems need acceptance, comparison classification leaves history intact, supersession retention and rejection).

## Not touched

Files changed by PR #1580; no production source changed.

## Validation (Focused tier)

* ruff check on the new file: pass. Whole-package isolated `I001` hits remain in `__main__.py` and `test_import_exceptions.py` (pre-existing, untouched; isolated mode misclassifies `zava_forward.core` as first-party).
* ruff format --check: pass. mypy (importer, strict): pass.
* `src/importer/tests`: 90 tests OK. `src/core/tests/test_scenario_manifest.py`: 8 tests OK.
* Hosted CI not run; nothing pushed.
