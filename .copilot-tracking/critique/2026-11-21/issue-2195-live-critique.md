# Issue 2195 critique (one pass)

Date: 2026-11-21. Executed by a rubber-duck agent against the plan and details. Verdict: revise, applied directly.

| ID | Finding | Disposition |
| --- | --- | --- |
| PC-001 | Routing text could imply a distinct subagent answered when only the evidence lens changes and rule or fallback paths answer. | Accepted. Text says "Routed to the X agent" and the existing answer-origin label stays beside it; tests cover consent, refusal and fallback attribution. The demo records this lens model as the limit. |
| PC-002 | Single-word keywords can mis-route or narrow evidence on multi-topic questions. | Accepted. Tie or zero match stays general; tests for ambiguous and multi-topic cases; test that citations remain available. |
| PC-003 | Older responses without `routing` would break the UI. | Accepted. JS reads `answer.routing && answer.routing.text` and shows nothing otherwise. |
| PC-004 | Post-call revalidation must use the effective lens. | Accepted. The effective skill replaces `skill` before sources are built, so revalidation uses it. Test added. |

No finding conflicts with a confirmed owner decision.
