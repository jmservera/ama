---
title: Issue 119 r1 plan
ms.date: 2026-11-03
---

## Plan

* [x] Phase 1: add a polite tile-failure note in `mapPanel()` (see details).
* [x] Phase 2: static test, ruff, mypy, node syntax check, protocol and KB log update.

Critique: executed once, inline. Verdict: proceed. Directly applied finding: do not clear the note on later tile loads, which would flicker during partial failures. No significant or divergent issue.

Validation tier: focused. The slice touches no security, infrastructure, SQL or deployment, so the gate is not needed.
