# Research: #2164 scope Entra staff by roster case_ids/areas (2026-11-22)

Research disposition: executed. Planning Readiness: Ready.

## Findings (evidence: source reads)

* `Assistants.authorize` (src/core/src/zava_forward/core/assistants.py ~1507) takes `identity.verified(user)` for Entra principals as `current`. That is a copy of the session principal, which never carries `case_ids`/`areas` or roster `disabled`/`active`, so Entra staff are unscoped and a roster revocation does not apply.
* `identity.bind` (identity.py) gives a roster-bound principal `bound={code,email}` and the roster row's code/email. `identity.matches(store, tid, oid)` finds enabled roster rows for the immutable tenant/object keys. view_only principals skip binding.
* Non-Entra principals read the `staff` row by email and use its role, disabled, active, case_ids, areas.
* `listing` and `forecast` read scope from `authorize` results, so fixing `authorize` fixes all callers.
* `auth.py` marks `view_only=True` when no staff role is assigned (admin only); role is then Application Administrator, which is not in any REGISTRY role list, so view_only never reaches an eligible role via the real auth path. A forged or future view_only principal with an eligible role must still be refused; `continuity._refuse_view_only` is the precedent.

## Decision

Roster-bound Entra staff inherit the scope and revocation state of their bound roster row (looked up by bound email, confirmed by matching oid/tid via the row). Unbound Entra staff (no roster row) keep the current unscoped behaviour (decision recorded, no regression). A bound principal whose row is missing, disabled, inactive, role-changed or oid-mismatched is refused. view_only Entra principals are refused.

## Acceptance criteria (issue body)

1. Decide whether roster-bound Entra staff inherit scope: decided above.
2. Tests for view_only with an eligible role and for scope bypass: planned in src/api/tests/test_assistants.py.
