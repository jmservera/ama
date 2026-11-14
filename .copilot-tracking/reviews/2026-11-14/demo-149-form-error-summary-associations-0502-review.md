---
title: Epic 149 form error summary associations review
ms.date: 2026-11-14
---

## Review (executed once)

Outcome: conformant with disclosed pre-existing failures. Boundary: the new test file only.

* Scope matches: associations, summary anchors and focus targets, plain copy; baseline not altered.
* Static string checks are engineering evidence, not WCAG or assistive-technology acceptance.
* Open items routed to later work, not re-reviewed here.

## Routed follow-ups

1. Fix `test_epic149_role_workbench_heading_hierarchy.py` failures (H1_NOT_FIRST, table names) at HEAD.
2. Fix mypy `App` untyped call in the landmarks test.
3. Add field focus at ops.js:534, progress.js:82, role-screens.js:1416 and remove them from `NO_FIELD_FOCUS`.
