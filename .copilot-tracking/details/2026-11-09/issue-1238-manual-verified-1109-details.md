<!-- markdownlint-disable-file -->
# Details: issue 1238 F3 manual_verified supersession (1109)

Written 2026-11-09T23:31Z, before tests and source. Plan:
[plan](../../plans/2026-11-09/issue-1238-manual-verified-1109-plan.md).

## Action contract

Action `service_supersede_authorize`, added to `RESIDENT_ACTIONS` and
`FOLLOWUP_ACTIONS` so it runs inside `_operation` (audit before save, rollback
on failure, committed-acknowledgement handling). Body: `id`, `attempt` (int),
`reservation_id`, `authorize_as` (`control_owner` or `reviewer`),
`evidence_ref` (a reference, at most 100 chars). No free-text note is stored
(critique PC-006).

Handler `_res_service_supersede_authorize`, in order:

1. Find the request and attempt; the attempt must be `Pending` with the
   supplied `reservation_id`; otherwise `ValueError`.
2. Refuse while `in_flight` for this request on this store.
3. Authorize the caller: `control_owner` needs the request's
   `service_owner_email` and `_require_named_reviewer` against
   `service_identity`; `reviewer` needs `redress_owner_email` and
   `_require_named_reviewer` against `redress_identity`, plus
   `_require_independent_reviewer` against `reviewed_identity` on an
   Independent review. No manager bypass; unknown identity fails closed.
4. Validate `evidence_ref` with `_intake_text` (100).
5. Reuse or create `attempt["supersession"]`
   (`evidence_ref`, `authorizations`, `withdrawn`). First move any recorded
   authorization whose person no longer matches the current owner for its role
   (code or oid) into `withdrawn` (critique PC-004). A remaining authorization
   fixes the evidence: a second must repeat it, come from the other role and a
   different person; a repeated role is refused with a reload message
   (PC-005). With none remaining, the new evidence applies.
6. Append `dict(role, identity, at)`. On the second authorization set
   `status="Superseded"`, `superseded_from="Pending"`, `superseded_at`; leave
   `reason`, `reservation_id`, `receipt_ref`, `route_key` untouched.
7. Return a detail string without the evidence text.

## Resend gate

`_res_service_forward` unresolved set includes `Superseded`, so the existing
`retry_unresolved` and owner or named-reviewer rights still apply to a later,
separate send. `_res_service_forward_outcome` already accepts only `Pending`,
so a late outcome cannot overwrite a `Superseded` attempt.
`complaints_route.STATUSES` is unchanged, so `Superseded` cannot be supplied as
a receiver outcome.

## Test construction

Create the `Pending` attempt as the existing outcome-save-failure test does
(patch `_res_service_forward_outcome` to raise, expect
`ResidentCommittedError`). Users: `sam` is service owner, `rae` is redress
owner, `pam` second owner on the Independent review fixture. Atomic failure
patches `store.audit` to raise on the second authorization. Added by the
critique: reassignment of either owner after the first authorization (PC-004),
a late outcome refused for a `Superseded` attempt with the receipt logged
(PC-002), and retention deletion over a superseded attempt (PC-006).
