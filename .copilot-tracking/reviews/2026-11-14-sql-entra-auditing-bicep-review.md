---
title: SQL Entra auditing Bicep review (issue 143)
ms.date: 2026-11-14
---

## Review

Execution: executed once. Outcome: conformant for the focused slice; independent coordinator review pending.

* Tests are deterministic static source checks; they fail if any control is removed.
* No Bicep, src or web files changed; no cache directories left in the worktree.
* Follow-up: compile-level check with bicep build is covered by existing test_bicep_policy; Refs #143 only, acceptance criteria of the issue body are not claimed.
