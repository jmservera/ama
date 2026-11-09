<!-- markdownlint-disable-file -->
---
title: Issue 159 validation-refusal receipts review
description: Authored post-implementation Review of the initial feature increment
ms.date: 2026-11-09
---

## Execution

* Review executed once after implementation, authored by the implementing agent against the diff `cbc54ab20..working tree` (4 files, +113). Not independent; the independent exact-head review stays required before publication. Not repeated in this task.

## Assessment against the brief

* Three branches only: met. The helper is called only at the three raise sites; other 400 branches untouched (verified in the diff).
* Exactly one metadata-only receipt, zero model calls, UNKNOWN tokens: met. Stored receipt reuses `_receipt` (tokens `None`, cost "Unknown"); unstored mirrors the existing `{outcome, model_calls}` payload. API test asserts the row delta, sibling action unchanged, shape, empty case target, and the model-call spy.
* No question, unknown field name or value, raw skill: met by construction (the helper takes no request content) and by canary assertions on the audit row. The rejected request 400 message is unchanged and contains none of them.
* Stored `tid` only after thread and permission checks: met; the calls sit after `chat_resume` and the regulatory handling.
* No duplicate receipts: met; the raises precede `ask`, the only other `chat.turn` writer. Valid asks keep one receipt (control). Existing denial, foreign and missing thread tests pass unchanged.
* No schema, migration, seam, CI or config change: met. No Any, cast or ignore.

## Findings

* R1 (low, accepted limitation): a user refused at the helper recheck after the earlier checks (a race) gets the 400 with no receipt, by design D1. The no-actor and denial policy is out of scope. Routed to the coordinator or a later issue; no source change.
* R2 (low, existing seam property): an audit write failure would surface as a 500 as it does for the existing rejected receipts. Unchanged semantics; not addressed.
* R3 (info, unproven): hosted CI, named assistive-technology acceptance, anonymous 401 receipt policy, other 400 branches and the whole-issue criteria remain unproven or out of scope. Use `Refs #159` and `Refs #189`, never a closing keyword.
* No open blocking or material finding. Outcome: conformant for the bounded slice at the local demo-targeted tier. Any later corrective source pass needs a bounded coordinator history disposition; none is self-authorized.

## Routed follow-ups

1. Independent exact-head review and hosted CI (coordinator).
2. Owner decision on the anonymous or no-actor 401 receipt policy and the other unreceipted 400 branches.
3. Named screen-reader and announcement acceptance (human tester).
