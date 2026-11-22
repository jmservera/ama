# Critique: #2164 plan (executed once, author self-critique, 2026-11-22)

Verdict: proceed with direct dispositions.

* Risk: verifying the oid on the roster row could break legacy rows without oid. Disposition: bound principals only arise from `identity.matches`, which requires the row oid; a missing or different oid on the row now means revoked. Accepted.
* Risk: looking up by bound email only. Disposition: also require the row's role to equal the principal role and oid to equal the principal oid. Accepted.
* Risk: refusing unbound Entra staff would regress existing flows. Disposition: rejected; unbound keep unscoped behaviour, recorded as a decision.
* Tier: src change in a security control, so FULL tier candidate; the coordinator runs gates (never rpi-checks --all here).
