# Independent plan critique: issue 1288 E6

Execution: one independent critique by a separate read-only rubber-duck subagent on the drafted research, plan and details at `5271d62fa`. Not the RPI agent and not the E5 reviewer. Verdict: rework. No second critique round for this task.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | High | A post-check freeze or a late timer can still break the physical cap; "microsecond" overstated | Accepted in part. Residual restated without the word microsecond, as a named limit needing an owner decision for a provider-side fence; live provider stays unavailable. Slot is held for the whole restamped window. |
| 2 | High | Ordinary `claim`/`execute` calls share the cap but not the fence | Accepted. Fence wired into `execute` (A2). |
| 3 | High | Transport path underspecified (proxy CONNECT, multi-send, redirects, timer) | Accepted (A3): private opener, no proxy or redirect, once per connection, socket shutdown timer, tests. |
| 4 | Medium | `disabled` rejects an already reserved call through the capacity clause | Accepted (A4): split the authority hold from the capacity check. |
| 5 | Medium | Plan values violate lease bounds; accepts cannot be zero after connect; token count nonzero | Accepted (A5): valid bounds, assert bytes, fence at request start for zero socket, meter and token. |
| 6 | Medium | A refusal inside `_request` poisons the financial ledger | Accepted (A6): request-start fence precedes the meter; pre-send refusal keeps the existing conservative semantics, documented. |
| 7 | Medium | Store identity and clock not enforced | Accepted (A7): identity by construction, one database clock domain documented, restamp-versus-reclaim tested. |
| 8 | Low | Inventory and typing acceptance too loose | Accepted (A8). |

No finding conflicts with a confirmed owner decision. Significant divergence from the draft: the fence is now two-point, applies to the ordinary path and states its residual honestly. No owner decision is requested; real-provider activation is not part of E6.
