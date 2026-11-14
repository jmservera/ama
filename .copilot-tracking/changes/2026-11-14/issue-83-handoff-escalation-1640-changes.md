---
title: Issue 83 criterion 6 changes
ms.date: 2026-11-14
---

* src/api/src/zava_forward/api/web/app.js: `handoffAttention` gives "State: Action needed" or "State: Escalated: unaccepted handoff", waiting hours, receiver and role, due time with "(overdue)", and the escalation target; used in the pending list and case panel; State column in the waiting table.
* src/api/tests/test_unaccepted_handoff_escalation_ui.py: new.
* No core or API contract change. Validation: fast formula (plus waiting view, read guidance and download UI modules) passed, 98 tests, 13 skipped (opt-in browser); ruff and mypy clean. Hosted CI and human review not run.
