<!-- markdownlint-disable-file -->
# Implementation Plan: Routed AI metering findings

* Task: 432-review-findings; parent 432; date 2026-10-31.
* Direction: reuse the original accepted source-only plan and PC-001..008;
  apply RV-001..005 as ordinary later implementation, not a new Review loop.
* Original Review outcome Defects found remains immutable.
* Details: .copilot-tracking/details/2026-10-31/ai-metering-432-review-findings-phase-details.md.

<!-- rpi:phase id=P01 -->
## [x] P01: Ledger lifecycle and dispatch invariants

<!-- rpi:task id=P01-T01 -->
### [x] P01-T01: Review revisions, budget holds and currencies

Restore append-only latest/as-of review state, enforce shared liability holds
at dispatch, and reject deferred-price currency ambiguity. Add durable legacy
review intents and unresolved-join reporting in the existing event partition.
Write boundary: core ai_consumption.py and test_ai_consumption.py.

<!-- rpi:phase id=P02 -->
## [x] P02: Legacy recovery and composed adapter evidence

<!-- rpi:task id=P02-T01 -->
### [x] P02-T01: Wire intent/recovery and actual adapters

Depends on completed P01 interfaces. Write-disjoint phase boundary:
core ai_tasks.py/store.py and API test_ai_consumption_api.py. Preserve domain
review semantics while recovering interrupted financial joins. Extend actual
metered assistant withdrawal, legacy/priority failure, chat and worker/fence
compositions. Total new test methods across the original two modules <=35.
No additional source/test module, DDL, deployment or approval.

<!-- rpi:phase id=P03 -->
## [x] P03: Evidence, requested checks and publication preparation

<!-- rpi:task id=P03-T01 -->
### [x] P03-T01: Reconcile corrections and final candidate

Depends on P02. Update directly related guidance and append knowledge log;
record exact observed tests/static checks, preserve original adverse outcomes.
Run requested API discovery/Ruff and prepare the final committed candidate
with external clean task-owned isolation. The complete exact-head local gate
is a separate mandatory post-commit publication prerequisite: fetch main and
verify its external receipt before authorised push/Refs #432 PR. Do not repeat
Review, close the issue, approve live economics or merge the PR.
