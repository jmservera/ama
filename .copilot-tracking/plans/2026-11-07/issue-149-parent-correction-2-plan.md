---
title: Issue 149 parent correction 2 plan
ms.date: 2026-11-07
---

## Plan

* Change `says_failure_outcome` to `happened.startswith(f"{lead} {NOT_A_MODEL_RESULT}")` for the two supported leads. Reason suffixes stay accepted.
* Add one case to `test_data_operator_ai_state.py`: both delivered-prefix variants rejected; ordinary quarantine/fallback and extra legitimate rows accepted.
* Red: run the actual current helper before editing; green after. Tier FOCUSED manual, light only: AI-state plus exception-register screen tests, ruff, mypy from a new exact-candidate archive; installed production reused only if all 211 bytes match.
* Source commit, then Review and state in one commit; no later commit. Browser and axe pending admission.

## Critique (single pass)

Prefix semantics match the original b470 suggestion and leave Kind selection and ID uniqueness intact. Whitespace-leading cells would be rejected, which is acceptable because the rendered cell text is trimmed. No product, Core predicate or SQL scope; no escalation needed.
