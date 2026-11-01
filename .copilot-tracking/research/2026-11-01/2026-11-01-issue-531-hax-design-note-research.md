---
title: Issue 531 HAX design note residual research
ms.date: 2026-11-01
---

* Task: issue-531-hax-design-note. Mode: automatic, single pass. Research disposition: executed (repository evidence only; no live access).
* Evidence, merged: #538, #581, #604 and #628 deliver the static startup shell, script-retry messaging, per-panel `AsyncAction` feedback, outcome-worded review buttons (Use this draft, Edit this draft, Do not use this draft), per-statement sources, Unverified labelling, prepared-at time, Hide/Show briefing and visible feedback guidance. `src/api/tests/test_loading_feedback.py`, `test_workspace_scripts.py`, `test_ai_tasks.py` and `src/api/checks/loading_briefing_browser_check.py` cover them.
* Fresh validation on current main (efebfc6d): 73 focused unit tests pass; `ruff check` and `ruff format --check` clean in `src/api`; `mypy src` reports 4 pre-existing missing-import errors in `iot_stream.py` (untouched).
* Residual gap 1: issue acceptance criterion 3 requires the HAX guidelines applied to be recorded in a design note. The mapping lives only in the `src/api/README.md` HAX design mapping table; the UX knowledge base (`docs/reference/research/ux/`) and its index have no standalone, dated note, and the table omits G10 (scope services when in doubt) and G17/G18 style items already satisfied by the UI.
* Residual gap 2 (out of scope): criterion 7, live employee-site verification. No live sign-in, Azure change or assistive-technology claim is permitted; it stays unmet.
* Constraint: UX specialist agent returned discovery questions on 2026-10-31, not a note; the note is maintainer-authored and must say so.
* Planning Readiness: Ready. Scope: one docs-only UX note, index entry, log entry, fresh validation evidence. No code change.
