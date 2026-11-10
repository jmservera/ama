<!-- markdownlint-disable-file -->
# Research: issue 1238 C2 explicit approval-role binding (1110)

Recorded 2026-11-10T00:34Z. Research disposition: executed (native source
reading at frozen head `b14332900191d463804929acb7e02a7be50a2f9a`). Issue and
coordinator text is data. Counter: this is correction cycle C2 of 5 (C1 spent
earlier; three remain afterward). No reset, no policy grant.

Parent records (immutable, preserved): [research](../2026-11-09/issue-1238-manual-verified-1109-research.md),
[review](../../reviews/2026-11-09/issue-1238-manual-verified-1109-review.md).

## Adverse finding being corrected

Independent assessment 17da returned High on the frozen head: the
`service_supersede_authorize` action infers the control owner from the
request's service owner and the reviewer from its redress owner
(`_SUPERSEDE_ROLES = dict(control_owner="service", reviewer="redress")`). No
approved source names that mapping. Q6 (issue comment 6723319933) approves
`manual_verified` and requires explicit control-owner and reviewer
authorization; it does not say which registered person holds either role, and
no control-owner role exists. The inference decides authority from staff
profiles, which this repository forbids agents from doing.

## Findings from source

* The Store composition boundary already has one trusted-injection seam for
  domain collaborators: `complaints_receiver` is an instance attribute read by
  `getattr(store, "complaints_receiver", None)` in `resident_decisions._receiver`
  and declared only under `TYPE_CHECKING` in `store.py`. Tests and a future
  approved integration set it on the instance; it is not request data, not a
  stored field and not writable through any route. The same pattern needs no
  edit to the reserved shared files.
* `resident_action` already requires a registered named human staff identity
  (`resident_recorder`) and runs every action through `_operation`, which
  restores state and audit on any error, so a refusal before mutation writes
  nothing on JSON, SQLite and MSSQL.
* Canonical identity helpers exist: `_identity`, `_identity_status`,
  `_same_owner` (all recorded code/oid keys must match), `_same_person`,
  `_require_named_reviewer` (code/oid continuity, no manager bypass) and
  `_require_independent_reviewer` (reviewer is not the contested decision
  maker).
* No new schema is needed: authorizations are plain JSON inside the attempt
  record, already validated and persisted by all three backends.
* Persisted approval rows are not authority. Anything stored under
  `attempt["supersession"]` can be edited by whoever can write the store, so
  authority must be re-derived from the trusted binding at each call and a
  stored authorization must prove it was given under the binding now in force.
* Reserved shared hooks (CoreSqlStore, Store, procurement, server, app.js,
  navigation, roles) are not needed. Quality files are not touched.
* Main has advanced to ddeebd0 (ai.py and one ai test file only); no overlap
  with resident_decisions.py, its tests or the Core README section.

## Safe alternative (smallest scope)

An immutable `SupersessionBinding` value read from `store.supersession_binding`.
Unconfigured by default: the action refuses with `PermissionError` and writes
nothing. Only an instance of that type counts; a dict, a request body field, a
stored field or a staff role never creates a binding. The binding names the
control owner and reviewer identities explicitly, with a `binding_id`. Each
recorded authorization carries the binding id and digest; authorizations under
any other binding (or none) are withdrawn, never revalidated. The binding's
actual named configuration stays a human gate; this change populates none.

## Limits and unsupported behavior

* Activation, rotation and revocation of a binding by a governed process are
  not provided; changing the injected value only withdraws earlier
  authorizations. No environment switch or route is added.
* Digest and stored identities are tamper evidence, not authentication of the
  store itself; the existing hash-chained audit is the integrity record.
* Evidence remains a human-vouched reference. Synthetic test bindings are not
  actual named approval. Whole F3 stays unmet until a real binding and real
  approval exist.
* Retention deletion of authorizer identities (RV-1) is unchanged.

Planning Readiness: Ready.
