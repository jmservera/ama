# Changes: #1288 correction 1 (C1)

Recorded 2026-11-08T20:08Z. Start b89520be (tree 441c2f1e), merged origin/main c50e9f0b as ef6c05e9 (no rebase).
Originals untouched. Refs #1288/#107; no closing claim.

## Changes by finding

* F1 provenance: `sensor_view.classify()` gives synthetic-weather-derived, synthetic-modelled-indoor, synthetic-unclassified; all "Not calibrated". Live `live-sim-reading-v1` rows are admitted with accurate labels.
* F2 latest bound to capture: `capture_source` is clock-free (newest 12 incl. latest, 4 before/after anchor); UI latest comes from the same capture. Trigger uses a coarse 6h-bucket signature.
* F3 stability: `assistants.signature` strips `sensor:` citations and `source:sensors`; empty/withheld/unavailable captures stay stable across seals; `eligible(known=)` dedupes.
* F4 `review_flag` statuses: withheld, rejected, reviewed, not-current, manual-proposal, uncited, review-suggested. Only the last is an autonomous review flag; delivery text states no recipient recorded.
* F5 withdrawal: `_withhold_sensors` plus `_scrub_events` apply to detail, list, export and sensors projections; stored records kept.
* F6 retrofit context stated unavailable in model source and UI; quality-record anchor named separately.
* F7 UI `SENSOR_ROLES` = Quality Inspector, Retrofit Programme Manager; PSO keeps ordinary quality panel and manual route.
* F8 per-sensor primary-key consent lookup; index `ix_sensor_reading_home_time (home_id, observed_at)` created idempotently in `sensor_consumer._schema`.
* F9 citation key `sensor:{sensor_id}:{reading_id}`; collision regression.

Files: sensor_view.py, assistants.py, sensor_consumer.py, ops.js, assistants.js, core README, tests/test_sensor_consumer.py (index drop before ALTER in two helpers, found by real SQL), api/tests/test_quality_sensors.py (new suite).

## Evidence (raw exits)

* SQLite final 20:08Z: test_quality_sensors, test_assistants, test_assistant_release, test_sensor_consumer, ingestion, consistency: EXIT 0, Ran 353 OK (skipped=91). Skips are SQL variants, not SQL evidence.
* Real SQL Server 2022 container under `flock -n /tmp/ama-rpi-heavy.lock` (resources at 19:49Z: / 12G, /mnt 7.0G free): MssqlReadModel+MssqlHttp Ran 29 OK 0 skipped; test_assistants, test_assistant_release, test_sensor_analysis_mssql Ran 182 OK skipped=8 (analysis lacked ZF_SENSOR_MSSQL); rerun with ZF_SENSOR_MSSQL=1 analysis/ingestion/consistency/sql_check Ran 97 OK 0 skipped. MssqlStore asserted. Container removed, exit 0.
* Browser: real local Chromium, real local API, scripted mock provider (not real AI), SQLite store. Verified flag grounded, manual, uncited, rejected, stale, withdrawal (no value in page HTML), absent retrofit text, role matrix (PSO denied readings, Contractor not found), reflow at 1280/390/320, first Tab focus, reduced motion. Axe 4.14.0 full states: 0 incompletes, 1 violation per state `label-content-name-mismatch` on pre-existing `summary[aria-label="Your account"]` (not C1). No full WCAG or AT claim.
* ruff clean; `node --check` ops/assistants/app exit 0.
* Not run: `tools/rpi-checks.py --changed`; complete local gate.

## Deviations

* Test-helper index drop; `_scrub_events` and `source:sensors` signature fix discovered during implementation.
* Existing proposals' source signatures are invalidated by the rule hash change; no release or activation granted.
