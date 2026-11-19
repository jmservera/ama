# Research: issue 124 live r3 (2026-11-19)

Refs #124. Task slug `issue-124-live-r3`. Disposition: reused (2026-11-18 r1 and r2 evidence, re-verified).
Evidence: `.copilot-tracking/evidence/2026-11-19/issue-124-live/` (59 discovery tests OK; read-only Azure CLI).

* Unticked criteria: owner nominated and endpoint agreed; dictionary validated; constraint register with two-sided evidence.
* Each needs a named human (sponsor, operational owners) or a real twelve-month company extract. None is buildable for the synthetic demo; the contract rules are already coded and tested (`discovery_contract.py`, `discovery_register.py`).
* Live: API revision 0000033, same image digest as the r2 pass; Event Hub holds only `sensor-readings`; no discovery consumer in src/api, orchestrator, agents or importer.
* Planning Readiness: Ready (conclusion: no source change; evidence note only).
