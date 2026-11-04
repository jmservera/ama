---
title: Issue 126 round 2 details
ms.date: 2026-11-04
---

## Slice 2

* `release_record` requires `economics_report_ref` and `economics_limit_breach` (None or a description).
* When decision is Release and the breach is not None, `economics_breach_decision` is required.
* Existing fixture RELEASE gains the two fields; new test covers missing fields, breach without decision, Withhold with breach, Release with decision and clean Release.
* Docs: `src/core/README.md` governance section, `docs/reference/log.md`.
