<!-- markdownlint-disable-file -->
---
title: Issue 350 main acafc6ee integration changes
description: Changes record
ms.date: 2026-10-26
---

Actual order: research, plan and details, critique (Revise, PC-701..703 applied), commit `206415ab`, main pinned at `acafc6ee04e3612cd62349ab9e4a0af3b24e8109`, normal `--no-ff` merge `57e4524464f028793b4ea475c645905f24247798`, verification, one review (Conformant, no findings), this record.

Changes: the merge brought in main's 42 paths only (docs, tracking, rubric, `log.md`, root `requirements.txt`, `tools/cowork-native-recovery/`). No conflict, no source, checker, fixture or shared-runner edit. Root `requirements.txt` (`markitdown==0.1.9`) is intentionally not installed; the checker does not use it.

Verification: topic-bound venv resolves `zava_forward.core` to this worktree; `unittest tools.test_check_demo_feedback` 88 OK; ruff check E,F,I,B,UP py312 line-length 100 passes; ruff format (88) check passes; checker, tests and `rpi-checks.py` unchanged since `7a43bbbe`.

Dependency: no full gate until the issue 349 shared no-cache image gate fix is published and integrated into main; the gate then needs a re-plan on the new base with `--lock-timeout 0`. Old c8d16059 candidate and plan are historical and untouched. No push, PR edit, acceptance tick or live action.
