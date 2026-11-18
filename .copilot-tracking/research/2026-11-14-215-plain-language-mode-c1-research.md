---
title: Issue 215 plain-language mode correction cycle 1 research
---

* Source: independent review `independent-direct-215-plain-e970d14e8.md` found that `role="status"` on `.regulatory-mode-state` adds a second status node inside `#regulatory-alerts`.
* Evidence: `test_case_journey.py` queries the first `[role="status"]` in the chat root and now matches the mode text; `checks/regulatory_ux_check.py` resolves `#regulatory-alerts [role=status]` in Playwright strict mode and fails on two matches.
* The panels already own one status paragraph each (`regulatoryAlertsPanel`, `regulatoryChatPanel`), so announcements can reuse them.
* Original research, plan, changes and review files are preserved unaltered.
* Planning readiness: Ready. Disposition: executed.
