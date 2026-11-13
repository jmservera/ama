---
title: Issue 432 per-call join across all worker modes details
ms.date: 2026-11-13
---

## Phase 1 to 4 details

* `call_join` gets keyword `configuration`, `prompt`, `root`, `attempt` (exact strings) and `output: str | None`. With `output=None` assert no output row under the root is eligible and the completed row exists by meter id with the same attempt/root.
* Worker modes expected: returned -> eligible output `reference(task id)`; revoked -> ineligible output; stale-fence and provider-failure -> no output row. Tokens: returned/revoked/stale-fence have usage, provider-failure `None`, held True.
* Retry: one task, first claim provider-failure, `expire`, reclaim; second returned. Assert two reserved rows, retry 0/1, attempts differ, `report["retries"] >= 1`, task `attempts == 2`.
* Canary: `assert_content_free` with worker system prompt and input text canaries plus the existing private strings.
