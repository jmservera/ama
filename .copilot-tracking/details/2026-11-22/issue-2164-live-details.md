# Details: #2164

Phase 1: in authorize, for `identity.is_entra(user)`: `p = identity.verified(user)`; if None or `p.get("view_only")` refuse. If `p.get("bound")`, load staff row by `bound["email"]`; require `row.get("oid") == p["oid"]` and tid match (row tid empty or equal); `current = row` (row role must equal principal role, checked by the existing common check). Else `current = p` (unbound, unscoped, as before). The existing email check compares current email to user email, which holds for bound rows.
Phase 2: tests build an Entra principal via `identity.principal`, then a staff row with oid/tid/code/email/role and `bound`.
