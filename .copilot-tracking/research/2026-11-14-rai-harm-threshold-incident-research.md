---
title: RAI harm threshold incident research (Refs #146)
date: 2026-11-14
---

Research disposition: executed. Planning Readiness: Ready.

## Findings

* `monitoring_coverage.evaluate_indicator` classifies breach/within/insufficient/blocked. Constructed thresholds set `offline_only`; a live threshold without a named `approved_by` is blocked; a breach carries `incident_owner` only when named. There is no suspension authority in core.
* `continuity.suspend` (`POST /api/continuity/suspend`, manager, quality inspector or building safety liaison roles) requires a named incident owner, records the task scope and affected assistant tasks, and rejects a repeat scope. `assistants.suspended` blocks execution; `reason_text` gives manual-route guidance.
* `test_operator_suspension.py` covers the suspension mechanics and one seeded drill; it does not distinguish offline from live thresholds through the API, nor deny dispatch of a post-incident invocation.
* `test_assistants.Base` provides the SQL-backed store/service; the suite is run via discover, so `tests/` is on the path. `pyproject.toml` needs no change: no sharding list names tests and the `test_rai_*` module is picked up by discovery.

## Scope

Add `src/api/tests/test_rai_harm_threshold_incident.py` only. No `src/core` edits. Focused validation tier.
