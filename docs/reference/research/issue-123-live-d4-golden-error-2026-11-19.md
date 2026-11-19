---
title: Issue 123 live run, D4 golden-file configuration error (2026-11-19)
description: Re-check of the #440 triage drafts on main and the D4 fix, with a per-criterion proven and unproven table
ms.date: 2026-11-19
ms.topic: reference
---

Scope: synthetic demo, desktop only, focused tier, main `05e94d303`. Refs #123, #440. No issue is created, ticked or closed.

## Re-check of the 2026-11-18 drafts

| Draft | Result on main 05e94d303 |
| --- | --- |
| D1 time status HTTP 500 | Not touched: SQL scope needs the FULL tier and an SQL Server container check |
| D2 legacy-reference allowlist | Already fixed: `python3 tools/check-legacy-references.py` prints `references: 0 violation(s)` |
| D3 `ChatIsolation.turn` unreachable | Still open; needs an owner or design choice (delete or wire) |
| D4 AI golden path | Fixed here (named-error branch) |

## D4 change

`ai_eval.run_eval` now reads the golden file through `load_golden`, which raises `GoldenFileError` (a `FileNotFoundError` subclass) naming the path and `ZF_AI_GOLDEN`. The alternative of packaging the fixture in the wheel is not taken. The `chat_eval` and `review_effectiveness` modules use the same path pattern and are unchanged.

Validation: `python3 -m unittest tests.test_ai_eval` in `src/agents` ran 21 tests, all passing; `python3 -m mypy` reported no issues in 67 files; `ruff check` on both files passed. The full gate was not run (heavy lock rule); the src change takes the FULL tier before publication.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| #123: #440 stabilization checkpoint complete | Unproven | #440 criteria 7 and 8 remain unticked; owner approval and independent review pending |
| #123: all child features closed or deferred | Unproven | #124, #125, #126, #128, #129 and #440 are open |
| #440 criterion 7: triage into filed issues | Partly proven | Drafts exist; D2 now obsolete, D4 delivered here, D1 and D3 remain unfiled and need owner or coordinator filing |
| #440 criterion 8: RPI artifacts and review | Unproven | HVE Builder behaviour change review and merge are not done |
