---
title: Chat memory review fixes research (PR 285)
ms.date: 2026-10-15
---

* CI validate failure: `test_items_are_inspectable_editable_deletable_and_clearable` flaked because memory ids were random and SQL orders by `created_at, id`; two items in the same millisecond swapped.
* `add_memory(task="")` skipped the per-task switch in `memory_status`.
* `list_memory`, `edit_memory` ignored `expires_at`; only `prompt_memory` filtered.
* `_admin` trusted `user["role"]`; the register is `store.staff` keyed by lower-case email.
* `CREATE TABLE IF NOT EXISTS chat_memory` does not add columns to a #163-era table.
* Planning Readiness: Ready. Open owner items unchanged: administrator role, retention, scoping and user wiring.
