# Review: issue 130 identity 403 (2026-11-18)

Execution: one self-review of the diff (no independent reviewer available to this worker). Outcome: conformant for the stated scope, with open items routed below.

* Correctness: the check now compares email, code and oid; `_actor` has already resolved a bound principal to exactly one roster row by tenant and object id. Legacy (non-Entra) users are unaffected, because their actor equals the roster row.
* Security observation: role and display name are no longer compared between the principal and the roster row. For Entra the principal role comes from the sign-in mapping and is checked by `require_role`; the old whole-dict test could never pass for Entra, so no previously-passing control is weakened. Needs independent security review (FULL tier).
* Tests: new tests fail on the unfixed code and on the disabled-check mutation; they run on JSON and SQLite stores.
* Findings routed to later work: (1) independent exact-head review, hosted CI and the full local gate; (2) redeploy and live re-probe of an Entra staff write; (3) the representative-evidence criterion stays unproven for the demo.
