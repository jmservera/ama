---
title: Issue 215 regulatory alerts UX research
ms.date: 2026-11-01
---

## Disposition

Research executed. Planning Readiness: Ready.

## Findings

* #215 criteria 1, 2 and 4 are ticked and delivered by merged PR #354 and #506 (alerts panel, plain-language toggle, doubt route, no-source state in `chat.js`; role matrix in `src/api/README.md`).
* Criteria 3 and 5 remain open. Criterion 5 needs real staff and owner authorisation; a protocol exists in the README and is not run.
* Reproduced locally (pinned axe 4.10.3, `checks/regulatory_ux_check.py`): 21 states, zero violations, `color-contrast` incomplete on `#regulatory-question` in 10 states.
* Root cause: axe `Ch()` treats an `overflow:auto` element's extent as `scrollHeight`, which excludes the 1px border, so the textarea is reported as partially obscured. Elements-from-point sampling showed nothing overlaps it; scrolling into view did not help.

## Acceptance criteria mapping

| Criterion | Status | Evidence |
| --- | --- | --- |
| Per-role patterns | Proven (existing) | README audience matrix, #354 |
| Alert fields | Proven (existing) | `regulatoryAlertsPanel` |
| WCAG 2.2 AA | Partial; automated contrast gap addressable now; manual AT assessment unmet | harness run |
| Doubt and no-source states | Proven (existing) | `regulatorySources`, doubt action |
| Staff comprehension | Unmet, human gate | protocol only |

## Decision

Scope: fix the false contrast incomplete, assert it in the harness, update README and log. Do not claim criteria 3 or 5.
