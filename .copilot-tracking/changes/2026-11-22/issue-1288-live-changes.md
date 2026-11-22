# Issue 1288 changes (2026-11-22)

Tier: focused. No src change; docs and evidence only. Classification basis: no source, workflow, dependency or Dockerfile edit.

## Files

* docs/reference/research/issue-1288-live-r8-quality-sensor-evidence-2026-11-22.md (new)
* docs/reference/README.md (index line), docs/reference/log.md (entry)
* .copilot-tracking/evidence/2026-11-22/issue-1288-live8/ (probe, scrubbed JSON, two screenshots, focused test output)
* RPI artifacts under .copilot-tracking/

## Validation

* 92 tests OK (9 skipped): test_quality_sensor_grounding, test_quality_sensors_correlation, test_quality_sensors_c7, from src/api.
* Read-only live probe against ca-cutover-test-demo-api revision 0000053; no Azure resource created or changed. Hosted CI and rpi-checks not run; nothing pushed.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 Read model (ticked) | Proven (live seen) | 7 homes ok, 12 readings, IDs, fresh |
| 2 UI display (ticked) | Proven (live screenshot) | Home sensors panel |
| 3 AI snapshot uses identical IDs | Proven locally only | mock provider tests; no live request |
| 4 Proactive deduplicated flag | Unproven live | release admission denied, OQ-017; allowance 0 |
| 5 Employee sees finding and attribution | Proven locally only | no live model output |
| 6 Explicit missing/stale/unavailable states | Proven locally; seen live (consent-withheld, release blocked) | no zero substitution |
| 7 Focused tests correlate | Proven as local engineering evidence | 92 tests OK |
| 8 Finite live walkthrough | Unproven | model leg blocked by missing human release record |
| 9 Human controls intact (ticked) | Not re-examined; no code changed | unchanged |
