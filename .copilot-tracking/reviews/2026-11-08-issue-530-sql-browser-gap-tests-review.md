---
title: Issue 530 actual SQL and employee browser gap tests review
ms.date: 2026-11-08
---

* Execution: authored Review once after implementation. Outcome: conformant for the bounded LIGHT scope, with open gaps routed below. No regrading of earlier reviews.

## Assessment

* Scope: only the three test and tool files changed outside `.copilot-tracking`. Production source is byte-identical to Main 0f05e9aa.
* Critique F1, F2 and F3 are applied and covered by regressions.
* The evidence is LIGHT only: 91 runner tests OK, static and type checks pass, 21 new MSSQL tests skip without opt-in, and a SQLite proxy of 21 passes is logic-only.

## Routed follow-ups

* Future FULL admission: all 17 groups, `--jobs 1 --lock-timeout 0`, the canonical lock free, fresh Main, fresh images, an external verified receipt, independent exact-head review and hosted CI. The actual MSSQL group must report the 21 new methods `ok`, and the browser group must run the chat check.
* Separate scope: fix lint and format of `employee_chat_browser_check.py`, then add it to the browser lint list. Separate scope: native CI parity for the chat check.

## Still unmet

* Actual MSSQL and employee Chromium/axe runs, real sign-in, private-runner authority, model price and budget, real-model grounded answer, named agent confirmation, and screen-reader, voice-control, resident, legal and professional approvals. #530 stays open.
