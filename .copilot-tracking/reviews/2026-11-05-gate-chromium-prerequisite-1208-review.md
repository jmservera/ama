---
title: Gate Chromium prerequisite review (#1208)
description: Single post-implementation review of the Chromium ordering repair
ms.date: 2026-11-05
ms.topic: reference
---

* Execution: one review, delegated to a read-only code-review agent over the working diff, plus the author's reconciliation. Boundary: tools/rpi-checks.py and tools/test_rpi_checks.py at the frozen candidate.
* Outcome: no material code findings. The agent confirmed the install is in the same project-api group in required_checks and Runner.run, runs once before sharding and scheduling, is skipped when project-api is reused on resume, is not recorded for setup-api only, and that verify_commands rejects a receipt lacking it.
* Qualified outcome: acceptance criterion 2 (native execution of the resident-summary regression with the installed browser) is not proven. The heavy lock was held by #96, so no native browser run occurred. Criteria 1, 3 and 4 are met by unit, lint and type evidence only.
* Routed follow-ups: (1) when the heavy lock is free nonqueued, run the small native check (isolated venv, playwright install, test_resident_summary_ai_ui, zero skips) and record it; (2) #188 and others rerun their own full gate on a head containing this fix. Neither is done here.
* Independent exact-head review, hosted CI and human approvals remain required. Issue #1208 should be referenced with Refs, not Closes, until native evidence exists.

## Follow-up 1 execution (appended 2026-11-05; original outcome above unchanged)

* Routed follow-up 1 was executed under a nonqueued heavy lock; criterion 2 is now evidenced natively (1 test, 0 skips) per the changes record. No new review was run. Follow-up 2 remains open.
