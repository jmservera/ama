# Review: #2164 (executed once, author review, 2026-11-22)

Outcome: conformant for the local scope; independent exact-head review and hosted CI still required.

* Fail-closed: bound principal with missing, disabled, inactive, role-changed or oid-mismatched row is refused (tested).
* Residual risk (routed to follow-up): legacy tid-less roster rows are accepted for any tenant at authorize time; `identity.matches` already gated this at sign-in. Other staff paths (chat, forecast callers outside authorize) were not audited for the same bound-row gap.
