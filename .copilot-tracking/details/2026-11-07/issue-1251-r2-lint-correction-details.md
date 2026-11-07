---
title: Issue 1251 R2 lint correction phase details
description: Phase details for the test-formatting correction
ms.date: 2026-11-07
ms.topic: reference
---

## Phase 2

* Run `ruff format --isolated --line-length 100 tools/test_backlog_sync.py` (existing formatter; no config change).
* Split the f-string at line 162 into two adjacent literals; no change to the asserted text.
* Prove no behaviour change: compare `ast.dump` of the pre-correction and corrected files after normalising adjacent string constants (parser already merges them), expect identical SHA-256 `a9b04ee3...f6f5`, and diff of `tools/backlog-sync.py` empty versus faf6c578.

## Phase 3

* Run all validation commands; capture each command and exit. Record in changes and a single original R2 Review; commit.
* Reconfirm origin/main identity; report drift, do not rebase.
