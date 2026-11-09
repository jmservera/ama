---
title: Issue 149 parent correction 3 plan
ms.date: 2026-11-07
---

## Plan

* Add `SOURCE_COLUMN = 6` to `data_operator_ai_state.py`; the browser check collects IDs from that cell of the Kind-selected rows. Kind selection, prefix semantics, exactly-once and all-rows outcome checks stay.
* Test: make the Node render helper return per-row cell lists; add a test that runs the actual selection on the real render and asserts both SYN IDs appear exactly once in the source cell of failed rows (red on current code). Fix the stub rows to the real column layout.
* Validation (CI-first focused): AI-state plus exception-register screen unit tests, ruff, mypy strict, canonical format from a fresh exact-candidate archive; installed production reused only if all 211 bytes match. Then the maintained atlas and data-operator Chromium checks with required axe 4.10.3 under `flock -n`, no queue. Source freezes before final evidence.

## Critique (single pass)

Using the source-reference cell is the narrowest contract-true fix and keeps the check independent of outcome text. Risk: duplicate SYN IDs in other columns are not counted, which is intended. No product, Core, SQL or assertion weakening.
