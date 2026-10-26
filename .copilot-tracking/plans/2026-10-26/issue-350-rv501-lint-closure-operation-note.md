<!-- markdownlint-disable-file -->
---
title: Issue 350 RV-501 lint closure operation note
description: Prospective external operation note for non-behavioural lint closure
ms.date: 2026-10-26
---

Written 2026-10-26 before any edit, at local head `a93bcf8e9d53547210032441bd1e7599bbb0f763`. The coordinator named this closure: a targeted static check found 9 violations introduced by the fixture edits. No new research, critique or re-review is required for this non-behavioural format closure; the earlier Non-conformant reviews (including RV-601/602) are unchanged and not relabelled Conformant.

Violations: F401 unused `ledger` import (line 22, `ledger_report` was removed); UP033 `lru_cache(maxsize=None)` to `functools.cache` (lines 109, 117); E501 long lines 96, 132, 1020, 1028, 1037, 1058.

Check command: `/mnt/ama-rpi-gates/issue462-helper-correction1/venv/bin/ruff check --isolated --no-cache --select E,F,I,B,UP --target-version py312 --line-length 100 tools/test_check_demo_feedback.py`. Plan: `--fix` for F401 and UP033, then `ruff format --isolated --line-length 100`, shorten docstrings by hand only as needed; rerun the check, the format check and the 88 focused tests. No behaviour change, no pinned environment mutation, no gate.
