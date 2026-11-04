---
title: Issue 82 round 2 details
ms.date: 2026-11-04
---

* Funding passes only when `funding_ok` is boolean True; any other non-boolean value is unknown.
* Safety passes only when `hazards` is a list and every entry has `released` True; a missing list is unknown, an unreleased or malformed entry fails.
* Resident passes when the existing `resident_gate` returns no reasons; None is unknown.
* Rule records: source BRD RULE-001/RULE-002 and PRD FR-008, effective 2026-11-04, version 1, reviewer marked unreviewed.
* Manual path and AI-unavailable behaviour: no AI involved; advance remains a human action.
