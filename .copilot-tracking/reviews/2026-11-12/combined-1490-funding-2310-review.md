---
title: Issue 82 combined 1490 candidate review
ms.date: 2026-11-12
task_id: combined-1490-funding-2310
---

## Execution

Review executed once, after implementation and validation, by an independent read-only code-review agent over `git diff 8f8be74e1 HEAD` at `1c2c3eea2` (4 commits, 62 files) plus the changes record and evidence. Outcome: conformant. No second Review runs for this task. This is an author-side agent review, not human review, hosted CI or professional ratification.

## Assessed boundary

Source: `store.gate_reasons`, three reader expressions, `MEMBERSHIP_REVISION` 3, tests, and the dated RPI evidence. Not assessed: real SQL Server suites, complete gate, hosted CI, API mypy, readers outside the write surface.

## Findings

| ID | Severity | Finding | Routing |
| --- | --- | --- | --- |
| F1 | Info | Scope is as claimed; `True` stays confirmed, everything else is denied; no helper, grant or policy; no gate weakened. | None |
| F2 | Info | `Store.advance` keeps the stage check before `gate_reasons`. | None |
| F3 | Info | `test_mvp.py` keeps both complete independent methods with separate fixtures and no conflict remnants. | None |
| F4 | Info | Changes record matches the evidence; skips classified as not run; no real SQL, tick or approval claim. | None |
| F5 | Info | Pre-existing `ruff format --check` failure of `tests/test_mvp.py` is preserved as adverse evidence; API mypy not run. | Later work |
| F6 | Low | The 165 core skips were not backed by a core skip-class file. | Resolved after Review by adding `core-skip-classes.out` (evidence only; 146 opt-in owned loopback SQL Server, 15 task-owned SQL Server, 4 other SQL-specific skips). |
| F7 | Info | Commit order, identity and trailers intact; original 82-1112 and RV01 evidence present. | None |

## Routing of open work

* Exact-head hosted CI, independent human review, real SQL Server suites and API mypy remain required later work. No tick, closure or acceptance claim: whole #82 stays open.
