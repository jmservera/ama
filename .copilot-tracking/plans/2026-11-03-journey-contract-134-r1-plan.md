# Plan: same-home journey trace, slice 1 (Refs #134, R1)

Research: [research](../research/2026-11-03-journey-contract-134-r1-research.md). Details: [details](../details/2026-11-03-journey-contract-134-r1-details.md).

* [x] Phase 1: add `journey_trace.py` (pure, read-only, no store writes)
* [x] Phase 2: tests incl. sibling and building negative controls
* [x] Phase 3: core README section
* [x] Phase 4: focused validation (unit, ruff, mypy)

Tier: focused. No security, infrastructure, SQL or deployment change; no gate run.

Critique (single pass, recorded by author): keep the function read-only and storage-agnostic (applied); never derive durations when a timestamp is missing (applied: Unknown); do not claim user validation or approval (applied: notice and fields). Resident consent and human approval boundaries are unchanged; no AI feature is added, so no AI-unavailable path applies. No web screen, so Fluent 2, WCAG and plain-language checks are not triggered in this slice.
