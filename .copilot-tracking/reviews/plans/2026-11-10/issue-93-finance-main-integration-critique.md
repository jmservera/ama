---
title: Issue 93 finance main integration plan critique
description: Single prospective critique of the integration plan, executed before implementation
ms.date: 2026-11-10
---

Execution: once, 2026-11-10 by the implementing author through direct adversarial reading, no nested agent. Not repeated for this task.

Verdict: proceed with amendments. All findings are compatible with the brief and are applied directly to the plan and details; none conflicts with a confirmed decision and none needs a user decision.

## Findings and dispositions

| Id | Finding | Disposition |
| --- | --- | --- |
| C1 | Byte guard for `README.md` and `log.md` is vague because main also edited them. | Applied. Guard: `git diff 5318f738 HEAD -- <file>` for each must show only additions that exist in the finance or verification history, with no removed main line. |
| C2 | Test counts could double count overlap among A, B and C, and `-v` output may not identify unique cases. | Applied. Record sorted unique test ids per observation and the union count; the brief's counts are not assumed. |
| C3 | Running tests or tools could write bytecode, mypy or ruff caches into the worktree and dirty the frozen candidate. | Applied. Set `PYTHONDONTWRITEBYTECODE=1`, `MYPY_CACHE_DIR` outside the tree and Ruff `--no-cache`; verify `git status --short --ignored` before the final commit. |
| C4 | The SQL conclusion rests on absence of tests; the parent might change persisted shape. | Applied. Phase 6 adds a diff check that the parent delta touches no `sqlstore`, `mssqlstore`, schema or persisted key names; residual stays stated as unobserved backend, not passed. |
| C5 | API strict mypy and the API test may fail on main-owned code for unrelated reasons, tempting a repair. | Applied. Classify each failure as parent, main or pre-existing; repair only parent-caused defects inside the seven files; otherwise stop and report. |
| C6 | Installing pinned tools needs network. | Accepted and disclosed; package installs only, no model, provider, Azure or private data. |
| C7 | A merge conflict in the log could tempt a semantic rewrite. | Applied. Resolution is textual: keep both blocks in chronological order; never edit earlier log entries. |
| C8 | The parent verification records state a parent-only observation that could be mistaken for main compatibility. | Applied. Changes and Review say explicitly that those observations are parent-only history and are not reused as evidence for this merged tree. |

## Boundary check

Plan stays inside the seven product paths and tracking. No new feature, no shared-hook edit, no gate or publication, no approval inference. Correction-cycle budget: five total, none consumed.
