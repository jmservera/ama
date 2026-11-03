# Review: issue #227 cross-home hazard referral queue

Execution: executed once, self-review of the diff. Outcome: queue-level slice delivered; independent review and human/AT acceptance pending.

| Criterion | Evidence |
| --- | --- |
| Queue shows time, source, destination, distinct sent, received, accepted | New cross-home table and existing per-home table; unit tested. Not browser-run in this slice. |
| Owned follow-up; release evidence | Follow-up in both views; release evidence stays per home with released-without-evidence flagged. |
| No classify, clock, close, authorise | No controls in either view (tag assertion). |
| SA-007 | Released and unavailable homes are listed; the no-row text does not claim safety. |
| WCAG baseline | Native table markup only; AT and human acceptance not performed (#155, #151). Unproven. |
| Design system (#150), no simulator | Unproven. |

Not every criterion is proven, so the PR uses Refs #227. Routed follow-ups: re-run the safety browser check in an installed environment; validate with people and AT (#155); Fluent adoption check (#150).
