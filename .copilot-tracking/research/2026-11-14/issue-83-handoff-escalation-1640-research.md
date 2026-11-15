---
title: Issue 83 criterion 6 research, unaccepted handoff escalation (BG-010)
ms.date: 2026-11-14
---

* Disposition: executed. Planning Readiness: Ready.
* Existing: `handoff_ageing` and `unaccepted_handoffs` (src/core workflows.py) flag a handoff when its own due time passes; no queue-wide limit is defaulted (OD-09 undecided). `/api/handoffs`, `/api/handoffs/unaccepted` and the CSV already exist; `#/handoff-waiting` showed "Needs escalation." text.
* Gap: the "Handoffs waiting for you" list and the case handoff panel showed only the raw status, with no explicit action-needed or escalated wording, elapsed time, target role or escalation target. The waiting table had no state column.
* Constraint: the unaccepted CSV has a fixed column list tested in test_unaccepted_handoff_csv_api, so no new projection fields were added; the list and panel rows already carry destination, due_at, offered_at and escalation_owner.
* Boundary: escalation stays a named manager's act; no automatic escalation, no approved limit invented.
