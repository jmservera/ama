---
title: Issue 144 main-based slice A port review
description: Authored post-implementation review of the main-based worker permit port (E1)
ms.date: 2026-11-10
task_id: issue-144-main-port-extension1
---

## Review execution

Executed once, by the implementing agent as an authored review (no sub-agents authorized). Boundary assessed: the working-tree diff against origin/main 6d4cd62475ba89a214055f761b8e3276ef063d44 (5 source and test files) plus the RPI records. This is not an independent review; independent exact-head review is required before publication.

## Outcome

Conformant for the declared scope at the DEMO targeted tier, with the limits below. No material finding is open inside this batch.

## Requirement checks

* Fresh database time after the blocking task-row UPDATE is used for the margin, `issued_at` and `lease_remaining`: covered by the ordering test (positive control, jump 5) and a causal RED mutation (log 07, 3 of 3 clock tests fail when the read is moved before the UPDATE).
* Expired or insufficient-margin lock crossing refuses with no reservation, budget charge or provider dispatch: covered for lease margin (jump 100) and authority expiry (jump 19 against 20 s).
* Valid window still grants: positive control and short-authority window tests.
* Consent not granted denies; captured readings fail closed to manual regardless of carrier; fence unavailable refuses with no reservation, a `send-refused` event and allowance refund. Positive controls included.
* Existing main safeguards (provider_body, seal, fence, witness, accounting, manual and denial paths) are preserved: `fence_send` behavior is unchanged through `_fence_in`, and the affected existing selectors pass unchanged (api 385 OK with 93 skipped, core 59 OK, agents 15 OK).
* No B scope was touched (queue_azure, dispatch, server, queue tests, publisher, routes, Date, backoff).

## Findings routed to later work

* Real MSSQL task-row lock-crossing regression was not run (SQL not authorized). Route: a separately authorized disposable-SQL run.
* Consent and captured-readings gates are tested with patched sensor predicates; route: a real sensor-fixture selector run.
* The lineage digest hook, reconcile, settlement-conflict, publisher and routes remain deferred to B.
* A never-sent permit holds its allowance slot until `active_until`; safe, documented, not changed.
* `complete_result` has no production caller yet in this scope; kept as the settlement entry for the deferred worker.

## Limits

* No actual consent, live, provider, spend or deployment decision is made or implied.
* No whole-issue 144, publication, production or human approval is claimed. Original spent history and the unknown minimum are preserved; this is E1 of the new five, four left.
