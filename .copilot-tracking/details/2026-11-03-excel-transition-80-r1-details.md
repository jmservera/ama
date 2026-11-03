---
title: Details for issue 80 round 1
description: Phase details for per-list CSV export wiring
ms.date: 2026-11-03
---

## Phase 1

`list_export.safe_cell` prefixes `'` for `= + - @ TAB CR`, renders bool as Yes/No, nested values as compact JSON. `to_csv` uses first-seen key union.

## Phase 2

`LIST_EXPORTS` and `list_rows` in `server.py` call `list_packages`, `list_work_orders`, `pending_handoffs`, `visits`, `funding_list`. Kinds `<list>.csv` are staff-only.

## Phase 3

Anchors with `download` attribute (native semantics, keyboard reachable); funding link states the file is a read-only copy.

## Phase 4

`core/tests/test_list_export.py`, `api/tests/test_list_export_api.py`, inventory update.
