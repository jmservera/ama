# Research: tenure route Legal position reference (Refs #131, slice R1)

Date: 2026-11-03. Branch feat/issue-131-r1, target main. Disposition: executed (code and merged-PR review). Planning Readiness: Ready.

## Prior delivery checked

* #509 (merged): unverified `tenure_intake` in `src/core/src/zava_forward/core/resident_decisions.py`. Every report has verification, decision_route, legal_position and cost_position `Unknown`, seven static questions, and a case-wide hold (`TENURE_HOLD`) that blocks scope recording and resident gate.
* #92 (merged, #389): consultation evidence only; distinct from this issue.
* Closure audit comment 2026-10-31: C7 ticked; C1 to C6 unmet.

## Findings

* No Legal role exists in `controls.py` roles; Legal reviewers are not system users. A Legal-reviewed position therefore has to be a human-attested reference to an external Legal document, recorded by resident-workflow staff, naming a separate Legal reviewer.
* Roles without resident-workflow rights already receive no `tenure_reports` (projection by RESIDENT_FIELDS), so a nested reference inherits that hiding.
* `resident_action` already routes intake actions through the transactional `_operation` for JSON and SQL stores, so a new action needs no API change.

## Slice decision (R1)

Smallest coherent slice for C3: attach an append-only Legal position reference to a tenure report. It stores no lease terms, interprets nothing, does not set verification, route or cost, and does not release the hold.

## Stacked follow-up slices (not delivered)

* R2: decision route set per household only from a Legal-reviewed, data-owner-verified record (C1, C2).
* R3: responsibility-question pack drafted from reviewed records for human approval (C4).
* R4: package review stays open on scope change, dispute, defect, charge query (C5); ambiguous lease identity reuse stop and data-owner routing (C6).

Blocked on humans: appointed Legal owner and Home Ownership data owner (issue "Open" item).
