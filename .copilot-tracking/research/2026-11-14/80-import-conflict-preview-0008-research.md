---
title: Issue 80 import conflict preview regression slice research
date: 2026-11-14
task_slug: 80-import-conflict-preview-0008
---

## Scope

Regression slice for #80 (Excel transition): prove (1) source workbook bytes are
never mutated by preview, staging, approval and comparison, (2) conflict
classification (blocking mapping/duplicate conflicts versus row problems versus
add/remove/change/unchanged comparison), (3) supersession history retention.
Must not touch files changed in PR #1580.

## Evidence

* PR #1580 changes `src/importer/{export,mapping,xlsx}.py`, `src/importer/tests/test_excel_transition.py`
  and `test_xlsx_safe_cell.py` (via `gh pr view 1580`). Slice therefore adds a new test file only.
* `mapping.preview_file` reads once, hashes, rejects if size/mtime changed (`mapping.py:201`).
* `QuarantineStore.stage` refuses `preview.blocking` (`quarantine.py:100`); `approve` supersedes earlier approved batch; `history`/`rows` keep old rows.
* `export.compare` is pure (`export.py:88`).
* Existing tests cover each piece in isolation, but not the staged end-to-end chain, that a refused stage writes nothing, or that comparison against staged rows leaves history intact.

## Disposition

Research executed. Planning Readiness: Ready. No source change needed.
