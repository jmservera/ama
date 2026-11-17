---
title: Safety screens WCAG textual state and keyboard changes
ms.date: 2026-11-14
---

* src/api/src/zava_forward/api/web/role-screens.js: text labels for stop-work indicator, service response clock (Overdue or Awaiting) and escalation state; headed sections; keyboard jump nav.
* src/api/tests/test_safety_screen_wcag_keyboard.py: new focused conformance tests.

Validation tier: focused (web UI, no gate tool, workflow, dependency or security change). Hosted CI and full gate not run. Refs #227; #227 stays open (human validation in #155 remains).
