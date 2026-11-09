---
title: Plan critique - issue 1288 E3
---

# Plan critique (single final-candidate critique), issue 1288 E3

Executed once, by the RPI agent itself (not independent). Process disclosure: the P4 regression test was drafted and run once (green, no red) before the plan, details and this critique were written; the critique therefore reviews it as a candidate and does not claim it was written test-first. Verdict: Approve with two applied amendments. Independent exact-head review remains required.

## Challenges and dispositions

| Challenge | Finding | Disposition |
| --- | --- | --- |
| Cross-namespace contamination | Simulated and real readings share one application store and receiver; no namespace separation exists | Supports freeze; any route needs a separate store |
| Caller flag or label | Env switches and booleans are not provenance; chat demo switch is chat-only | Freeze; test asserts they do not open the route |
| SYN spoof | `SYN-` and `LIVE-` are naming; a real record could be named so | Freeze; test uses SYN and LIVE readings and still holds |
| Private-case contamination | Payload includes address, postcode, documents and quality records from the working store | Freeze; no case-side marker exists |
| Free-text contamination | Quality checklist `evidence` is user text and can say anything, including "synthetic" | Freeze; allowlist cannot classify text |
| Egress boundary | `Ai` sees only a string; withholding at `Ai` is the only sound current control | Keep E2 fail-closed unchanged |
| Value coincidence and dataset path | Matching fixtures or arbitrary `ZF_DATA` prove nothing | Test patches an arbitrary path |
| Is a freeze "partial"? | Owner asked for a working demo; mock and manual routes still work, real-AI grounding does not | Recorded as an unmet criterion and an owner decision, not hidden |

## Applied amendments

* A1: the test must assert the request really contains the persisted reading (so the zero-egress result is not vacuous). Applied.
* A2: state plainly that the test passed on first run and locks existing behaviour, and that it is not evidence for model, live or AT acceptance. Applied in changes and handoff.

## Not changed

No source, switch, store or token was added. No live call is made.
