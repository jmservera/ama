# Research: tenure verification and decision route (Refs #131, slice R2)

Date: 2026-11-03. Branch feat/issue-131-r1, target main. Disposition: reused (R1 research) plus code re-check. Planning Readiness: Ready.

## Prior delivery checked

* #509 (merged): unverified tenure intake with case-wide hold; route and verification always Unknown.
* #858 (merged, R1): Legal position reference attachable per tenure report.
* #92: consultation check only. No other merged PR sets a decision route.

## Findings

* `decision_route` and `verification` have no writer, so C1 and C2 cannot advance without a data-owner action.
* No data-owner role exists in `controls.py`; as for Legal, the verification must be a human-attested record naming a separate data owner.
* BRD FR-015 / AC-021: route statuses are tenant, shared owner, right to buy or preserved right to buy leaseholder, mixed block or unverified; no capability interprets a lease.

## Slice decision (R2)

Add `tenure_verify`: append-only data-owner outcome per report. Route label only, needs a prior Legal position reference, keeps the case-wide hold. Remaining slices: R3 question pack (C4), R4 review-open triggers and ambiguous identity routing (C5, C6), household enumeration (C1 remainder).
