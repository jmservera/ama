# Research: wire eligibility_gate to recorded eligibility evidence (#82 F1)

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* `gates.py` defines `ELIGIBILITY_RULE` (effective 2026-11-13) and `eligibility_gate(state, reason, owner, on)`: only `True` passes; `False` fails; `None` is unknown. No production caller exists (grep of `src/`), so the gate is unwired (review F1).
* `grants.py` holds the grant lifecycle (Opportunity, Award, Claimable, Submitted, Accepted, Rejected, Cash received). `_grant_set_pending` records a proposal; `_grant_approve` applies it after independence and authority checks. Nothing records eligibility.
* `finance.py` uses `finance_gate`/`FinanceGateError` for commitments; `store.py` and `workflows.py` use booking and safety gates, none eligibility.
* Tests: `test_gates.py` covers the gate in isolation; `test_grant_lifecycle_controls.py` walks new grants (via `grant_open`, no eligibility field) through Submitted, so a strict gate on absent evidence would break those and stored legacy grants.

## Design findings

* Natural enforcement point: approving the transition to Submitted (the funder-facing step).
* Evidence field: optional `eligibility` (Eligible, Not eligible, Not assessed) plus `eligibility_source` on a grant proposal, carried in `pending` and committed on approval.
* Legacy compatibility: a grant record with no eligibility field (pre-field) is not gated and its history entry says "Not assessed (legacy record)". An explicit `Not assessed`, malformed or missing outcome is unknown and never passes.

## Open item

Legacy exemption is a deliberate, documented compatibility choice; a later migration should require assessed eligibility.
