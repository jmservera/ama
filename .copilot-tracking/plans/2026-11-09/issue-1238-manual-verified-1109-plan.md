<!-- markdownlint-disable-file -->
# Plan: issue 1238 F3 manual_verified Pending supersession (1109)

Prospective, written 2026-11-09T23:31Z before any test or source edit.
Research: [research](../../research/2026-11-09/issue-1238-manual-verified-1109-research.md).
Details: [details](../../details/2026-11-09/issue-1238-manual-verified-1109-details.md).

## Objective

Add the owner-approved `manual_verified` transition only: a `Pending`
formal-route attempt becomes `Superseded` after two separate, explicit,
audited authorizations (control owner and reviewer) on one verified-outcome
evidence reference. Receipt, reservation, route idempotency key and audit are
retained. No send, no age rule, no resend authority.

## Phases

* [x] Phase 1: failing focused regressions (tests first), red run recorded.
* [x] Phase 2: `service_supersede_authorize` action and handler in
  `resident_decisions.py`; `Superseded` keeps the resend gate closed.
* [x] Phase 3: `src/core/README.md` boundary text.
* [x] Phase 4: validation (module JSON/SQLite, MSSQL selected supersession and
  forward cases under one nonqueued admission, ruff, format, mypy).
* [x] Phase 5: one Review, changes record, state (done). Local commit and external handoff follow this record.

## Scope and exclusions

Owned: `src/core/src/zava_forward/core/resident_decisions.py`,
`src/core/tests/test_resident_decisions.py`, `src/core/README.md`, RPI records.
Not touched: `CoreSqlStore`, `Store`, procurement, server, `app.js`, shared
navigation, `resident_demo/app.py`, Quality guards or tests, resident web.

## Tests planned first (inherited by JSON, SQLite and MSSQL classes)

1. Valid flow: control owner then reviewer on the same evidence supersede a
   failed-outcome `Pending` attempt; first authorization alone leaves
   `Pending`; reservation, request id, receipt log, `route_key`, audit entries
   and persisted reopen retained; receiver called once and never again; a later
   send still needs `retry_unresolved`.
2. Refusals change nothing: wrong person for the claimed role, manager,
   non-owner, same person claiming both roles, missing or blank evidence,
   unknown attempt or reservation, non-`Pending` attempt, mismatched evidence,
   duplicate role authorization, in-flight send; Independent review decision
   maker as reviewer.
3. Age alone: an aged `Pending` attempt with no authorization stays `Pending`,
   no resend without `retry_unresolved`, no supersession.
4. Atomicity: an audit or save fault on the second authorization leaves the
   first authorization only and the attempt `Pending`; replay then succeeds.

## Risks

* Control-owner mapping to the service owner is an interpretation; recorded for
  confirmation, no new role.
* Evidence is a reference, not machine-verified.
* Synthetic tests demonstrate gate behavior, not human approval.

## Critique and Review

One critique of this final candidate before tests or source; one Review after
implementation. Counter: 1 of 5 spent, four left; not reset.
