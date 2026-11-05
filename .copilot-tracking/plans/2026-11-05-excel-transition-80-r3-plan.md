---
title: Plan for issue 80 round 3
description: Checklist list CSV export
ms.date: 2026-11-05
---

## Phases

* [x] Phase 1: core `quality.checklist_rows()`, `checklists.csv` staff kind in `projection.STAFF_GET`, route entry in `LIST_EXPORTS` and `list_rows` in `src/api/src/zava_forward/api/server.py`.
* [x] Phase 2: "Download for Excel" link in the quality checklist form (`web/ops.js`), with the existing read-only wording.
* [x] Phase 3: tests (registry, rows equal JSON, denial, no private data, selectors ignored, read-only, core rows, web source), role endpoint inventory, API README.

Details: [phase details](../details/2026-11-05-excel-transition-80-r3-details.md).

## Critique (one pass, direct)

Verdict: proceed. Reuse `list_export.to_csv` and the registry; no new helper beyond the row builder; no new framework or dependency. Staff-only via the existing default-deny projection, so contractors, residents and the administrator role get 403 as for the JSON route. No free text: labels are constants, so no extra sanitisation beyond the existing formula-safe cell. Compatible advice applied directly; nothing conflicts with confirmed decisions. Follow-ups: governance, resident, chat and form lists; owner thresholds (C4).
