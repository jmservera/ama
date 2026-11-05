---
title: Issue 80 round 3 details
description: Phase details
ms.date: 2026-11-05
---

* Phase 1: `checklist_rows` in `src/core/src/zava_forward/core/quality.py`; `"checklists.csv"` in `STAFF_GET` of `src/core/src/zava_forward/core/projection.py`; `/api/checklists.csv` in `LIST_EXPORTS` and `list_rows` in `src/api/src/zava_forward/api/server.py`. `get_kind` already maps a registered export to its path name, so no kind table change.
* Phase 2: `web/ops.js` quality form, shown after the checks. A native link with visible text, keyboard focusable, same class and wording as the other export links.
* Phase 3: `src/api/tests/test_list_export_api.py`, `src/api/tests/test_role_endpoint_inventory.py`, `src/api/tests/test_loading_feedback.py`, `src/core/tests/test_list_export.py`, `src/api/README.md`.
