<!-- markdownlint-disable-file -->
# Bounded live demo plan revision 2: details (2026-11-11)

Revised planning content, applying the [critique](../../plans/2026-11-11/issue-184-bounded-live-plan-rev2-1111-critique.md) to the [rev2 plan](../../plans/2026-11-11/issue-184-bounded-live-plan-rev2-1111-plan.md). **NO EXECUTION.** Supersedes, for planning only, the matching statements in the [original details](./issue-184-bounded-live-plan-1111-details.md) and original plan; those files are unchanged. Every item here is a prerequisite or a future-request field, not an approval.

## 1. Receiver start, replay, limits and linkage (finding 1)

* Source fact: the receiver starts at the retained-stream beginning (`starting_position='-1'`, non-inclusive); the hub retains 1 day (recorded 2026-11-10). Starting a window before a send does not isolate this run; earlier retained events can be read.
* Source fact: a window ends successfully only when receipts reach `--events` (default 1000). Otherwise the deadline gives `RUN_DEADLINE`, and a control stop or expiry gives `RUN_STOPPED`; both exit 2. A window with fewer events than `--events` therefore ends exit 2 by design. The earlier "four short windows, stop on first failure, never re-run" sequence is inconsistent with this and is withdrawn.
* Prerequisite, not approved: a finite-window receive design that states the explicit event limit per window, replay handling, the exact designated slot and reading IDs, the expected exit of each window and how each completes. If it needs a source change, that is a separately scoped design and source prerequisite. No window is declared passing, and no failure is redefined as success, until such a design is separately reviewed.
* Linkage required (counts alone are insufficient, they are supplementary): run-specific synthetic or redacted IDs through send, receiver receipt, retained SQL row, same-home UI, captured snapshot, privacy-compatible provider-request witness and attributed `review-suggested` flag with model, version and time. No raw readings, secrets or private identifiers are logged to obtain this.

## 2. Transport bounds and stop (finding 2)

* Distinguish: designated logical slots (at most 13), application send attempts (at most 4 per slot, so at most 52), acknowledged sends, and unique retained readings. Retry acknowledgements do not establish unique service-side messages.
* Expiry and a control stop are checked only before each slot is admitted. They do not cancel an in-flight retry loop, and the job has no durable global slot or attempt counter; `--once` bounds one process only. No absolute hard stop or global bound is claimed.
* Assumptions for any future request: exact UTC slot and trigger times (the cron `*/5 * * * *` gives 12 or 13 triggers in a 60-minute span depending on alignment, so 13 is a maximum), no manual or replacement executions, a monitoring threshold on send counts, a deletion deadline for the schedule, and a bounded drain allowance for in-flight retries inside the three-hour envelope.
* Unverified prerequisite: the simulator lists all open cases; that the control cohort restricts it to one home must be verified from source before any request.
* If the owner needs an absolute no-send-after-expiry or a durable global attempt fence, that is a separately scoped owner design prerequisite and not provided by existing control.

## 3. Model calls and tokens (finding 3)

* The reservation uses the serialized ASCII JSON provider body length (with overhead and escapes) plus output tokens, not 12,000 characters. A 50,400 allowance may therefore admit fewer than four calls.
* Cap: four total reservations or physical attempts, including retries, under one authority and aggregate token budget. Never four calls times two attempts.
* USD0.00576 is an illustrative calculation only, not a worst case. The source meter has call, token and money checks, but the money check needs an approved authority and price record, both Unknown; no currency cap is claimed.
* The captured-reading dispatch guards in `assistants.py` and `ai.py` stay in force. No simulation seal, mock, renamed carrier or financial approval clears them. A future source revision would need its own provider token bounds, timeout liability and meter review.

## 4. Pricing, timeouts and cost classes (finding 4)

* Prices: a NEW 2026-11-11T17:03:14Z public retrieval with exact records in [the price records file](../../research/2026-11-11/issue-184-bounded-live-plan-rev2-1111-price-records.json). The original temporary payloads were removed and are not invented. Unretrieved rates are Unknown.
* Receiver replica timeout is window plus 120 s: a 360 s window is a 480 s replica, four are 1,920 s, about USD0.02016. Simulator 13 x 240 s = 3,120 s, about USD0.03276. Illustrative incremental total about USD0.059 at list price with no free grant. The original compute figures are superseded.
* Classes, kept apart: incremental illustration; existing fixed (hub B1 USD10 per month); newly ongoing if activated (Event Hubs, possible Container Apps environment meters), needing a named owner, duration and teardown; unpriced liability (Log Analytics, Private Link, SQL, ACR, Azure Files, post-expiry ticks, failed cleanup). No cap, no affordability claim; budget alerts are not stops. Cost is Unknown and Unknown liability is a HOLD.

## 5. Provenance (finding 5)

Native CLI session `053b0ad3-0c8d-46d8-b30c-e3b1f3fcdb3f`. `d7c3b05b-1d90-41d2-80b2-ee64088929e2` is an artifact and task identifier generated before the original artifacts, not a native session. The original critique was one pre-revision invocation with seven author-applied dispositions, not an independent reconfirmation of `76e21e9a`. Original wrapper `.log.exit` is missing and the shared launcher may have been edited during capture: no exit 0 is inferred and no exit file is recreated. The independent report is a separate exact-head assessment.

## 6. Only the next design question (finding 6)

"The current source cannot meet the live-model criterion. Shall this remain a non-executable plan with that criterion unproved, or shall a separate narrowly scoped source and design proposal be prepared for your review? No execution, spend or proposal implementation is included."

Replaces the original combined question. A later exact execution request is allowed only after the design, current identities, approved prices, finite limits, accountable ongoing-resource ownership and a financial boundary exist. This question does not approve any of those.
