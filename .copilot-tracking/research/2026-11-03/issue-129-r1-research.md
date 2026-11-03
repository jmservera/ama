# Research: issue #129 journey learning-test bundles (r1)

Disposition: executed. Planning Readiness: Ready.

## Prior delivery check

* Merged PR search for #129 returned only unrelated PRs (#336, #504, #411, #371). Commit history shows no #129 delivery. ADR 0003 "Implementation status" does not list the bundles.
* Conclusion: nothing delivered for the bundles; no work to avoid redoing. ADR 0003 itself is owner-accepted with amendment (2026-10-15); the issue's "owner acceptance" dependency text is stale for the ADR but BRD/PRD acceptance and the DPO retention decision remain open.

## Evidence

* PRD "Candidate journey learning tests" (docs/prds/zava-forward-retrofit-programme-demonstrator.md, ~line 2852) lists five bundles, atlas IDs, requirements, comparators and stop rules; NFR-009 net effort; mapping needs atlas-owner confirmation.
* ADR 0003 decisions 1 to 5; open item: atlas-owner confirmation; DPO decision on representative retention.
* Atlas rows O01 to O24 (customer-journey-atlas.md). O10, O18, O19, O20 are marked E (exploratory); others P.
* Observation: O16 is in two bundles (change impact; funding evidence).

## Scope decision

The issue is large (five experiments, atlas-owner and DPO dependencies). Slice 1: a knowledge-base protocol for all five bundles, no code. Executable harness deferred until the mapping is confirmed and the DPO decision allows representative data.

## Follow-ups

1. Atlas-owner confirmation of mapping and O16 overlap.
2. Non-AI comparator harness in src/core on constructed cases.
3. First bundle run with stop rule.
