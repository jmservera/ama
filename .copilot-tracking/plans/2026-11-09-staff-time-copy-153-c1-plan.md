---
title: Issue 153 C1 project mypy plan
ms.date: 2026-11-09
task_id: 153-c1-project-mypy-1109
---

## Plan (2026-11-09T23:37Z)

1. Critique once (plan plus details) before any edit.
2. Implement: add `# type: ignore[no-untyped-call]` to the six reported calls in `src/api/tests/test_timecapture_copy.py` only, then read back the activation.
3. Verify: exact `cd src/api && mypy` project command (expect 0 errors, no unused-ignore error); `ruff format --check` and `ruff check`; the 12 new tests with the 5 browser cases under one nonqueued `flock -n /tmp/ama-rpi-heavy.lock` after actual-holder inspection; directly affected `test_timecapture`, `test_content_standard`, `test_workspace_scripts`, `test_static_assets`, `test_role_screens`; `git diff --check`.
4. One Review, clean local commit, handoff. No push, PR, issue or board write, rebase, amend or reset.

## Boundaries

Only the new test file plus C1 tracking records. No config, backend, JS, shared or other worktree edits. Cycle counter: C1 of 5 used; four remain.
