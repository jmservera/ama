---
title: Issue 1384 workspace exhaustion oracles plan critique
description: Single final-candidate critique of the plan and details with direct dispositions
ms.date: 2026-11-10
ms.topic: reference
---

## Execution

* Critique executed once on the final candidate (plan, details and research), by a read-only rubber-duck subagent on 2026-11-10. It will not be repeated for this task.
* Verdict: approve-with-changes (four significant findings, no blocker).

## Findings and Direct Dispositions

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Significant | Fulfilling a transformed `app.js` may keep a stale `Content-Length`, ETag or immutable caching | Applied. `serve_mutated_app` sets the JavaScript content type, recomputed `content-length`, no `etag` and `no-store` (details, Phase 1). |
| 2 | Significant | A control that matches only the assertion message passes for any wrong count | Applied. `assert_requests` puts expected and observed counts in the text and `expect_detected` requires the exact observed count derived from contract plus transformation, never from a run (details, Phases 1 to 3). |
| 3 | Significant | An appended delay could push the sequence past the 5 s `expect` timeout before the intended assertion | Applied. The extra delay is a fixed 250 ms and the transformation refuses a schedule with less than one second of margin; no timeout is relaxed. |
| 4 | Significant | The early control rejected a valid single-delay contract | Applied. A one-delay declaration becomes an empty schedule (zero retries). The `continue` control refuses fewer than two delays because it would be indistinguishable from the contract. |

No finding conflicts with a confirmed decision, and none needs a user decision. No change of scope: still the two checks, the helper and the coupled tests.
