# Issue 444 boundary threat model: plan critique

Date: 2026-10-25. One independent critique (rubber-duck agent) of the research, plan and details before any content change. Not repeated for this task.

## Verdict: Proceed with changes

| Id | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| C1 | Blocking | Do not claim tests exist for DNS rebinding, XSS from dataset text, outbound traffic or generalised traversal. | Applied: evidence labelled test-proven or implementation-inspected. |
| C2 | Blocking | Missing residuals: fixture tampering, DoS and no concurrency bound, uneven unexpected-error handling. | Applied to details. |
| C3 | Non-blocking | Research said "other writes 405"; unknown paths are 404, bad Host 403. | Applied as wording rule; research is a prospective record and keeps its original text. |
| C4 | Non-blocking | "No outbound client code" is imprecise; same-origin fetch exists. | Applied. |
| C5 | Non-blocking | "Only two files" conflicts with tracking artifacts. | Applied. |
| C6 | Non-blocking | Correction cap must not leave accuracy defects. | Applied. |
| C7 | Suggestion | Loopback bind is the exposure control; Host check is extra. | Applied. |

No finding conflicts with a confirmed owner decision.
