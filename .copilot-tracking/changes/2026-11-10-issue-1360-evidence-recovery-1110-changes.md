---
title: Issue 1360 evidence recovery changes
ms.date: 2026-11-10
---

Evidence recovery at frozen source head `c7d570c8b89adab76a6402bd29c0cee215ab0233` (base main `6d4cd6247`). Records only; no source, test, config or documentation change. The original handoff `handoff-1360-extension1-1110.md` stays a historical claim.

## Fresh exact-head results (external evidence `phase1360-evidence-recovery-evidence-1110/logs/`)

| Check | Exit | Note |
| --- | --- | --- |
| importer `ruff check .` | 0 | supersedes the retained E501 log, which predated the docstring shortening |
| importer `ruff format --check .` | 0 | |
| importer `mypy` | 0 | |
| importer unittest discover | 0 | 82 tests OK |
| core `ruff check` sqlstore.py, test_priority_order.py | 0 | |
| core `ruff format --check` sqlstore.py, test_priority_order.py | 1 | sqlstore.py would be reformatted (import block at line 21 and others); test_priority_order.py formatted |
| core `mypy` | 0 | |
| core tests test_import_refusals, test_priority_order | 0 | 165 tests, 73 skipped (opt-in MSSQL) |

Module origins (own venv `/tmp/zf-1360-e1`) resolve under this worktree.

## Core format claim

The base (`6d4cd6247`) and current `sqlstore.py`, formatted from scoped temporary copies outside the worktree with the core config, both report "would be reformatted" with identical changed-line sets (`FORMAT_DIFFS_IDENTICAL`). The pre-existing format failure claim is proven; the one-line fix adds no new formatter difference. The retained original log of this claim did not exist, so this is a new comparison, not the original.

## New diagnostic, not the original red

Isolated copy of `src/core/src` with `except RuntimeError` restored, first on PYTHONPATH (origin asserted): the two committed-then-reload importer tests fail with "Nothing was recorded" (exit 1, 8 tests, 2 failures). The original raw red remains unrecoverable.

## Unchanged

Source and tests are unchanged against `c7d570c8`. No E2, no extension reset.
