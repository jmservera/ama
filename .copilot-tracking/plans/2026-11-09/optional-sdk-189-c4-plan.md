<!-- markdownlint-disable-file -->
# Issue 189 C4 optional streaming SDK import plan (2026-11-09)

Research: [research](../../research/2026-11-09/optional-sdk-189-c4-research.md). Details: [details](../../details/2026-11-09/optional-sdk-189-c4-details.md). Critique: [critique](optional-sdk-189-c4-critique.md). Refs #189 only. Cycle: C1, C2, C3 spent; C4 authorised; one remains after.

## Objective

Let the base employee API boot and expose planning, manual and unavailable simulator controls without the Azure streaming SDK, while the real streamer and CLI still require the declared SDK and report its absence explicitly when selected.

## Phases

* [ ] P1 Commit research, plan, details, critique (one) and initial state before any source edit (frozen).
* [ ] P2 Edit `live_simulator.py`: `TYPE_CHECKING` annotation, lazy `iot_stream` import on the `iothub` sink branch, `StreamError("IOT_SDK_MISSING")` on a missing module.
* [ ] P3 Validate: the failing contract test and relevant tools contracts, simulator and live-control tests, API-profile mypy 2.4.0, ruff 0.17.1 lint and format on affected files; one controlled browser run only if the control boot needs reconfirmation.
* [ ] P4 Changes record, one Review, final state, evidence commit, hashes, handoff.

## Owner-selected demo-targeted tier

Focused tier per the demo brief: no full gate, no global install, no SQL, cloud, private data or model calls. Hosted checks and independent exact-head review remain required.

## Stop rule

A change needing a blanket except, a fallback success, an installed SDK, a weakened fixture or check, `Any`, a cast, an ignore, or broad extraction is recorded and stops. A further failed hosted src API finding is retained and only fixed in C4 if directly coupled.
