---
title: Issue 82 funding readers review (follow-up RV01)
ms.date: 2026-11-12
task_id: funding-readers-82-2250
---

## Execution

Review executed once, after implementation, by an independent read-only code-review agent over the working-tree diff against base `dc9fb68e0` plus the changes record and evidence. Outcome: conformant. No second Review is run for this task. This is an author-side agent review, not human review, hosted CI or professional ratification.

## Assessed boundary

Three one-expression readers, one cache revision bump and six regressions in five existing test files. Not assessed: SQL Server suites, complete gate, hosted CI, other `funding_ok` readers outside the write surface.

## Findings

| ID | Severity | Finding | Routing |
| --- | --- | --- | --- |
| RV-01 | Low, informational | The new SQL regression ran on the local SQLite store only; the opt-in SQL Server harness (165 skipped tests) and API mypy were not run. Already declared in the changes record. | Later work: run the SQL Server suite and API mypy in hosted CI for the eventual exact head. No change here. |
| RV-02 | Low, informational | Other `funding_ok` readers and writers (`export_fields.py:51`, `resident_preview_fixture.py`, `ai_eval.py`) pass the value through and are outside the write surface. | None. |

Reviewer checks recorded: all three readers now match `store.py:171` and `gates.booking_gates`; `True` stays confirmed, so no gate, role or consent is weakened and no rule or helper is invented; `app.js:1344` renders a bool safely; the `MEMBERSHIP_REVISION` bump recomputes stale SQL flags and its negative control fails when reverted; scope is limited to the admitted surface.

## Routing of open work

* Eventual exact-head hosted CI and independent human review remain required, together with retargeting onto the UX parent after 1490 and #82 reach it, then any receipt required by that tier.
* No tick, closure or acceptance claim: whole #82 stays open.
