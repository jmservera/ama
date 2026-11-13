# Plan 131
1. RED tests in test_resident_decisions: legacy case (no tenure) held with owner and next action; complete verified inventory (known route, identity resolved, no triggers, all current) proceeds to the normal resident gate; open trigger / ambiguous identity / Unknown inventory still held.
2. resident_gate: unmanaged -> TENURE_HOLD reason; managed -> hold unless inventory view is Declared with no reasons and every household has a known route.
3. Fixtures: add a helper that records a verified tenure inventory for cases advanced past offer; run core + api suites, ruff, mypy.

## Critique disposition (rubber-duck, once, verdict Revise)
* Rejected: release of managed cases. Identity resolution is unreachable and no owner-approved completeness rule exists; the owner decision covers only holding unknown tenure before offer. Managed-case hold stays unchanged; verified-route proceed (AC2 part b) and scope-after-clearance stay blocked for an owner release rule.
* Applied: scope reduced to universal hold for cases with no tenure record; downstream callers (store, quality, projection) covered by existing suites with fixture updates.
