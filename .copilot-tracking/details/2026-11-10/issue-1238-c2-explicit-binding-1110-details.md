<!-- markdownlint-disable-file -->
# Details: issue 1238 C2 explicit approval-role binding (1110)

Prospective, written 2026-11-10T00:34Z. Plan:
[plan](../../plans/2026-11-10/issue-1238-c2-explicit-binding-1110-plan.md).

## Design

* `SupersessionBinding` frozen dataclass in `resident_decisions.py`:
  `binding_id` (1 to 60 characters), `control_owner` and `reviewer` each a
  tuple of sorted (key, value) pairs of email, code, oid, normalised in
  `__post_init__`. Validation: each identity has an email and a code or oid
  (Known); the two identities share no email, code or oid. `identity(role)`
  returns a fresh dict; `digest` is a SHA-256 of the canonical JSON of the id
  and both identities.
* `_supersession_binding(store)`: `getattr(store, "supersession_binding",
  None)`; anything but a `SupersessionBinding` raises `PermissionError`
  ("No approval-role binding is configured ..."). Called first in the handler,
  before any read of the request or mutation, so refusal writes nothing.
* Handler: roles are `("control_owner", "reviewer")`; the acting user must
  match the binding identity for the role by email and by `_same_owner`
  (every recorded code/oid), plus `_require_named_reviewer` continuity. The
  request's owner fields are not consulted. The Independent review rule stays:
  the reviewer must not be the contested decision maker.
* Each authorization stores `binding_id` and `binding_digest`. Before use,
  every stored authorization whose digest differs from the current binding, or
  whose identity no longer matches the binding identity for its role, moves to
  `withdrawn`. Withdrawn items never count again.
* Everything else is unchanged: both authorizations on one `evidence_ref`
  (at most 100 characters), different people, second authorization sets
  `Superseded`, receipt/reservation/key/audit kept, in-flight refusal, age
  never an input, no send, resend still needs `retry_unresolved`.

## Critique amendments (PC-001 to PC-004, applied 2026-11-10T00:36Z)

* A prior authorization counts only if the audit holds an entry by the same
  actor, case and detail (`<id> formal-route attempt <n> supersession
  authorized by the <role>`); otherwise it is withdrawn. The digest is
  provenance only, not proof.
* The binding is captured once in the `_operation` validation context; SQL
  replay refuses a different binding (PermissionError).
* Restoring an earlier binding revalidates approvals carrying its digest:
  documented unsupported (new `binding_id` required); no rotation claim.
* Helper is `synthetic_binding`, bound explicitly in each test.

## Tests (red first)

Existing class `test_resident_decisions.py` (inherited by JSON, SQLite, MSSQL):

* `bind(control, reviewer, binding_id)` helper sets a synthetic binding;
  `pending_attempt` binds sam and rae by default, so existing success tests
  keep their meaning.
* Default unconfigured: both old inferred paths (service owner, redress owner)
  and a forged stored two-authorization record are refused with no state or
  audit change; a non-binding object (dict) is refused.
* Binding does not follow staff roles: a binding for other persons refuses the
  former owners.
* Forged stored authorization (no digest) is withdrawn and cannot finish the
  supersession.
* Changing the binding withdraws earlier authorizations.
* Binding validation: same person twice, Unknown identity, and immutability.
* Reassigning a request owner no longer matters (replaces the reassignment
  test).

## Validation

Targeted only: module on JSON and SQLite, selected MSSQL under one nonqueued
heavy-lock admission (actual-holder inspection, no queue, spin or kill),
`mypy` for the exact Core project and the API project if Core signatures reach
it, Ruff check and format on the changed files with pinned declared tools.
