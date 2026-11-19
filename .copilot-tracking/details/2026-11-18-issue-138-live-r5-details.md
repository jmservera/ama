---
title: Details for issue 138 r5
ms.date: 2026-11-18
---

## Phase 1

Add `test_plan_rejects_unsupported_entry_among_valid_changes` after
`test_plan_rejects_delete_unknown_out_of_scope_and_public_sql`. Use `assertRaisesRegex` on
"unresolved/unsupported". Include the positive control (same plan without the Unsupported entry
returns counts). Success: test passes; temporarily accepting `Unsupported` in the code makes it fail.
