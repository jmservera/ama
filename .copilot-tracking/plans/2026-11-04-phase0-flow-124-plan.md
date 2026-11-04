# Plan: Phase 0 baseline and wait analysis (Refs #124)

Date: 2026-11-04. Stacked slices: 1 (merged, PR 895) register rules; 2 (this PR) `discovery_flow`; 3 (later, blocked) real nomination, validation, extract import.

* [x] Phase 1: add `src/core/src/zava_forward/core/discovery_flow.py` and tests. Details: [details](../details/2026-11-04-phase0-flow-124-details.md)
* [x] Phase 2: README section and log entry.

Critique (single pass, direct): keep pure and synthetic; never infer cause; None not guess; label candidates. Applied. Tier: focused; no security, infrastructure, SQL or deployment change.
