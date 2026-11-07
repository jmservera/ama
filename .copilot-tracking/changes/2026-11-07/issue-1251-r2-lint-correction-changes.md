---
title: Issue 1251 R2 lint correction changes
description: Original change record for the E501 and format correction
ms.date: 2026-11-07
ms.topic: reference
---

## Changes

* `tools/test_backlog_sync.py` only: `ruff format --isolated --line-length 100` plus a manual split of the f-string at the former line 162. No suppression, config or workflow change.
* Source delta: `tools/backlog-sync.py` unchanged from faf6c578e6cb5cd0b5171e51f6eab8b36c130d45. Test delta: formatting only; `ast.dump` SHA-256 identical before and after (a9b04ee36123b9f010257eba143655b5bb8d6a13476a16a128f3bdb7ee24f6f5, Python 3.12.3, pre-correction file from `git show faf6c578:tools/test_backlog_sync.py`).
* Amendment to the original records: the unchecked boxes in the original plan are the creation-state; the original critique, changes and Review are preserved unchanged. The original E9,F-only lint selection omitted the workflow's E,F,I,B,UP and format checks and is superseded by the plan in [R2 plan](../../plans/2026-11-07/issue-1251-r2-lint-correction-plan.md).

## Evidence (external, `/mnt/ama-gates/g1251-ci-r2-1107`)

* Original hosted failure `original-ci-failure.log`, pre-correction `pre-ruff.log` and `pre-format.log` retained; earlier evidence in `/mnt/ama-gates/g1251-focused-1107` untouched.
* Final-HEAD command logs and exits: `final-*.log`, `final-*.exit` (see Review).
