# Critique: issue 107 restarted-process allowance clamp plan

Date: 2026-11-08. One execution by an independent reviewer (rubber-duck), before any code. Not repeated.

Verdict: no blocking findings; proceed as planned.

| Point | Disposition |
| --- | --- |
| The second wave reaches the clamp on a successful restarted claim, and assertions on the stored calls, tokens and expiry would fail if configured limits replaced `min(stored, configured)` | Accepted as confirmation |
| No helper change needed | Accepted; implementation stays one method |
| MSSQL behaviour unverified until the gate | Accepted; disclosed in plan and later records |

The reviewer returned no revisions, so none were applied. This is the reviewer's outcome, not an author-invented pass.
