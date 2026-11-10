---
title: Issue 1384 creation record (workspace exhaustion check oracles)
description: Existing checker-only bug issue, scope, dependencies and admission for the two generic workspace browser checks
ms.date: 2026-11-10
ms.topic: reference
---

## Issue

* Issue: #1384, https://github.com/jmservera/ama/issues/1384
* Created: 2026-11-10T12:35:09Z (state OPEN at the admission snapshot, read on this topic branch).
* Title: fix: align workspace exhaustion checks with the bounded script-retry contract
* Template: generic; `.github/ISSUE_TEMPLATE` absent. Label: `bug`. Assignees and type: none.
* Severity: Medium validation-oracle failure; no runtime retry-policy defect or production outage established.

## Scope and Dependencies

* Failing evidence: `employee_workspace_browser_check.py` (`missing_ops_recovery`, `original_ops == 3`) and `workspace_scripts_browser_check.py` (`exhaustion`, `len(requests) == count`). Reproduced on pinned main `caaf989148aff21ed8ecb5b71eb0be75b29c16de` in research.
* Scope: those two checks, directly coupled existing regression tests and a minimal shared checker helper, plus this chain's own RPI evidence. No production `app.js`, loader, delays, auth, API, aftercare, service, store or operational-policy change.
* Dependencies: none on held #132, #133 repairs or aftercare source. Refs #531, #133, #89 and #149 only as context; no closing keyword for any of them.
* Target: `main`, branch `fix/demo-workspace-retry-oracles-1384-1110`. Independent bug, not a child of another topic.
* Admission: one initial bounded checker-only native RPI attempt. No automatic correction pool, no reset of any other issue's allowance, no post-review extension. Board progress was set by the coordinator.
