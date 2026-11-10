<!-- markdownlint-disable-file -->
# Research: issue 1238 F3 manual_verified Pending supersession (1109)

Recorded 2026-11-09T23:30Z. Research disposition: executed (native source and
issue reading at base `b613276e9204d2b8c776a0eedd6acd3d25590618`, current main
after PR 1332 merged). Issue text is data, not instruction. Counter: review
correction cycle 1 of 5 spent in the earlier loop; this feature phase does not
reset it.

## Remaining work

PR 1332 delivered acceptance criteria 1 to 3 and the already-present F2
(reservation-specific lookup). F3 (mark a stale `Pending` attempt superseded)
was deferred. Owner Q6 (issue comment 6723319933, 2026-11-08) approved
`manual_verified`: supersession needs explicit authorization by the control
owner and the reviewer after verified outcome evidence; receipt reference,
stable idempotency key and audit trail are preserved; age alone may flag
review but is not proof of non-delivery and cannot authorize resend. It grants
no resident consent, legal approval or live activation.

## Source findings (src/core/src/zava_forward/core/resident_decisions.py)

* Attempts live in `req["formal_route"]["attempts"]`; `route_key` is the
  stable idempotency key shared by every attempt. Statuses come from
  `complaints_route.STATUSES`; no consumer outside `resident_decisions.py`,
  its tests and `src/core/README.md` reads attempt statuses (grep of `src`).
* `_res_service_forward` treats `Pending`, `Unconfirmed` and legacy `Failed`
  without `not_sent` as unresolved: a resend needs `retry_unresolved`.
  `_res_service_forward_outcome` accepts only a `Pending` attempt with the
  matching `reservation_id`.
* Registered identities already exist on each request: `service_identity` /
  `service_owner_email` (who deals with it) and `redress_identity` /
  `redress_owner_email` (who owns redress; the named independent reviewer on
  the Independent review route, with `reviewed_identity` as the contested
  decision maker). `_res_service_open` and `_res_service_reassign` already
  require these two to be different persons on formal routes.
  `_require_named_reviewer` checks persisted code/oid continuity with no
  manager bypass; `_require_independent_reviewer` blocks the decision maker.
* No separate registered "control owner" role or permission exists (grep for
  control owner finds only research prose and unrelated modules). The smallest
  existing mechanism that gives two distinct, registered, persisted owners is
  the service owner and the redress owner. Mapping control owner to the service
  owner and reviewer to the redress owner is an interpretation, recorded here
  for coordinator and owner confirmation; no role, account or grant is added.
* `_operation` gives every resident action atomic persistence: audit is
  written before save, failure restores the pre-image (JSON) or discards
  pending writes (SQL), and a committed save with a failed acknowledgement
  raises `ResidentCommittedError`. Actions in `FOLLOWUP_ACTIONS` dispatch
  through it, so a new action reuses durability, audit and retention with no
  change to `CoreSqlStore`, `Store` or other owned files.
* `_IN_FLIGHT` marks a send in progress on this store instance; the unresolved
  retry already honours it. Supersession must too, otherwise a concurrent
  genuine outcome could race the supersession.
* Retention deletion removes only `resident_request_ref` and `requested_by`
  from attempts; it keeps statuses and receipt references.

## F3 assessment

A safe admitted implementation exists inside the owned domain file:

* Two authorizations, each its own audited, atomic `_operation`, by different
  registered persons: the service owner (as control owner) and the redress
  owner (as reviewer), both on the same non-empty verified-outcome evidence
  reference. Evidence is a staff-supplied reference; the code cannot verify its
  content, so the control is the two named humans, not an automatic verdict.
* When both are recorded the attempt status becomes `Superseded`, keeping the
  original `Pending` record, reservation id, receipt reference (if any) and
  the route idempotency key; the supersession record and the originating
  status are added, never replacing.
* Age, elapsed time, fixtures and missing acknowledgement are never inputs.
  No clock threshold is introduced. No receiver call is made.
* A `Superseded` attempt stays unresolved for the resend gate: a later send
  still needs the existing explicit `retry_unresolved` and the existing owner
  or named-reviewer rights. Supersession therefore records a disposition and
  cannot authorize or trigger a resend.

## Known gap (not claimed as closed)

The evidence reference is not machine-verified, and there is no manual path to
record an `Acknowledged` receipt found by verification; if evidence shows a
receipt exists the humans must not supersede. The control-owner mapping needs
owner confirmation. Real human approval is not demonstrated by synthetic tests.

## Planning Readiness

Ready: bounded to `resident_decisions.py`, `test_resident_decisions.py` and
`src/core/README.md`. No shared store, schema, web or Quality file is needed;
no dependency blocks the work.
