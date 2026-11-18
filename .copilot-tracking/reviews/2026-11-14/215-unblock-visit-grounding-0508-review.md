# Review: #215 unblock and visit grounding (Refs #215)

Execution: executed once after implementation. Outcome: conformant for the bounded objective; one residual gap routed.
Assessed boundary: the new test file against current source at base 40266b643. This is not independent human or hosted review.

## AC verdict

| Criterion | Verdict | Evidence |
| --- | --- | --- |
| Provenance origin distinct (decision model vs generative) in payload and rendered copy | Met | API payload tests (`answer_source`, `model`, label); static `chat.js` attribution tests |
| Actionable grounded unblock or cited reasons, no silent record mutation | Met | cited ZF-4 citations, deterministic reasons, record JSON unchanged across turns |
| Human approval and safety-lead sign-off boundary on visit or safety-stop clearing | Partly met | Human route and "cannot book a visit or approve a safety step" asserted; Safety lead named from the record as owner |
| Resident-consent boundary | Not met in source | No consent wording in `_unblock`; not a deterministic bug, routed as follow-up |
| `Chat cannot approve or change records` invariant | Met | static assertions for both chat.js notices |

## Follow-ups (ranked)

1. Owner and resident-engagement review of a resident-consent sentence in `_unblock` (small copy change in `chat_case_answers.py` with a core test update). Evidence: this review.
2. Observe hosted CI for the exact head before any merge.
