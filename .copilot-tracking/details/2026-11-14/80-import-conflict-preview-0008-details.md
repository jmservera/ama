---
title: Issue 80 import conflict preview regression details
date: 2026-11-14
task_slug: 80-import-conflict-preview-0008
---

## Phase 1 tests

* Source bytes, SHA-256 and mtime unchanged on a read-only file across preview, stage, approve, compare.
* Conflict classification: duplicate key and ambiguous columns block staging and write no batch or rows; row problems stage but need explicit acceptance.
* Comparison of a staged import against current approved rows classifies added, removed, changed, unchanged without altering history.
* Supersession retains the superseded batch rows and lineage; a rejected batch supersedes nothing.

## Validation (Focused tier)

Venv `/tmp/venv-80-0008` via pip; ruff check/format with isolated flags, mypy, `src/importer/tests`, `src/core/tests/test_scenario_manifest.py`.
