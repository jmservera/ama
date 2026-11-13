---
title: Issue 153 app.js notices details
ms.date: 2026-11-13
---

* Briefing: status keeps `Briefing unavailable: ${error.message}.` then `Owner: application support. Next action: choose Try loading briefing again, then contact application support if it continues.`
* Priority: keep prefix; add owner and `request a suggestion again, then contact application support if it continues`.
* Cases unavailable status: append owner and next action; Map: append; Home case view: keep `Use the case and building screens instead.` and add owner; Shared building context: add owner, next action; startup alert: add owner.
* Do not touch `Workspace unavailable: ` status or safetyPanel.

## Critique amendments

* Helper `ownedNotice` keeps messages already containing `Owner:`; all seven notices get both clauses; briefing next action names Try loading briefing again or Refresh briefing; tests cover owner-bearing and generic errors; validation runs test_app_js_notices_content, test_content_standard, test_case_journey, test_ui_support, workbench_browser_check, ruff, mypy.
