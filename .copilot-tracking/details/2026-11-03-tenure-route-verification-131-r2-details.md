# Details: tenure verification and decision route (R2)

## Phase 1

* New closed action `tenure_verify`: `case_id`, `report_version`, `expected_version`, `outcome`, `verified_tenure`, `identity_confirmed`, `verifier_name`, `verifier_role`, `evidence_ref`, `verified_on`.
* `Verified` needs known tenure, confirmed identity and an attached Legal position reference; sets route label from a fixed map. `Not verified` needs Unknown and unconfirmed and resets verification and route to Unknown.
* Refused: unknown report, stale version, non data-owner role, verifier equal to recorder, future date, blank evidence, extra fields (such as a supplied route).
* Hold, cost_position and legal_position untouched.

## Phase 2

* Core: route set only after Legal reference; Not verified returns to Unknown; refusals leave state and audit unchanged.
* API: HTTP 400 before Legal reference, 403 for non-workflow roles, no canary leak to restricted roles.

## Phase 3

* `src/core/README.md`, `src/api/README.md`.
