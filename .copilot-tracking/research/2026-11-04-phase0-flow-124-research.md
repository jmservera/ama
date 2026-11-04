# Research: Phase 0 retrofit-flow discovery, slice 2 (Refs #124)

Date: 2026-11-04. Disposition: executed (focused). Planning Readiness: Ready.

## Delivered already

* PR 895 (merged) added `discovery_register`: owner and accepted-handover endpoint status, ten-event dictionary gaps, constraint register with supporting and contradicting evidence, "not a company finding" labelling.
* PR 928 (merged) is the epic checkpoint under #123.

## Acceptance criteria status

* Owner nominated and endpoint agreed: rules only; no real nomination. Unmet.
* Lifecycle and event dictionary validated: rules only; no owner validation. Unmet.
* Constraint register supporting and contradicting evidence: rules and empty seed hypotheses; no real evidence. Unmet.
* Not company findings until validated: enforced in rules and labels. Met for the rule layer only.

## Gap in the brief (docs/brds/retrofit-flow-discovery-brief.md)

Outcomes 2 and 3 (baseline population, queue, wait and return-loop analysis; Analysis Population and Time Attribution) have no code. Smallest unblocked slice: pure, synthetic, deterministic arithmetic in `src/core`, with manual path and AI-unavailable behaviour (no model).

## Blocked

Nomination, validation and real data need named company people and a sponsor decision.
