---
title: Issue 2257 verify details
ms.date: 2026-11-22
---

## Phase 3 detail

Add `test_map_read_recovers_from_a_dropped_connection` to `WorkspaceScripts`. A Node VM script loads the source between `const STARTUP_RETRY_DELAYS` and `const workspaceScriptLoads` (as the existing test) plus the `async function api(` body, stubs `fetch` to reject once with `TypeError("Failed to fetch")` for `/api/map?...` then answer 200 JSON, and asserts `api("/api/map?zoom=5")` resolves with the data after one retry, and that a second consecutive reject sequence of three still rejects. Also assert the map draw source calls `api(` with `/api/map`.
