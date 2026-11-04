---
title: Issue 215 status record details
ms.date: 2026-11-04
---

## Phase 1: record

Add dated RPI artifacts only. Knowledge-base files are unchanged, so no log.md entry.

## Owner actions that unblock the issue

* Criterion 3: authorise and run the per-role keyboard and screen-reader scripts in docs/reference/research/ux/regulatory-ux-acceptance-protocol.md, then run `src/api/checks/regulatory_at_record_check.py` on the records.
* Criterion 5: authorise a staff round (repairs, housing, grants; 3+ per group), then score with `src/api/checks/regulatory_comprehension_score.py`.
