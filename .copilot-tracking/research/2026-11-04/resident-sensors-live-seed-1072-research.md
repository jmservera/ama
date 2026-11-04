<!-- markdownlint-disable-file -->
# Research: live resident demo has no synthetic sensor data (#1072, Refs #462)

Date: 2026-11-04. Task slug: `resident-sensors-live-seed-1072`. Research disposition: `executed`.
Planning Readiness: `Ready` for a plan that records the live check and an owner decision; `Blocked` for a live apply.

## Observed live (read-only)

* Live app `ca-resident-demo--0000010`, min replicas 0.
* Signed-in 390 px Playwright walk (test user, credentials read from the owner file, never printed) at 2026-11-04 15:4x UTC: `#sec-sensors` shows only "No synthetic sensor readings are available for your home."; `#gauge-temperature_c` count 0, `#gauge-humidity_pct` count 0, no forecast text, no horizontal overflow.
* SQL server `sql-cutover-test-rzsrg`, database `retrofit` (Standard): `publicNetworkAccess` Disabled, zero firewall rules, Entra administrator is the managed identity `id-cutover-test-init`. The current Azure CLI login is a user, not that administrator.
* Existing in-VNet job `job-cutover-test-init` (Manual, args `initialize`, user identity `id-cutover-test-init`, image `zava-forward-cutover-proof`) is the only SQL-capable compute. Its image holds `private-cutover-proof.py` and the API/core packages, not `infra/sql/resident-showcase.sql`, `resident_showcase_sql.py` or any sensor loader.

## Root cause (evidence-ranked)

1. Sensor tables absent in live SQL. Counts-only evidence on 2026-10-29 (`infra/README.md`) and `admitted-sensor-view-init` markers on 2026-10-30/31 (`.copilot-tracking/changes/2026-10-31/demo-sites-redeploy-1031-evidence.json`) show `sensor_register` and `sensor_reading` at zero rows; the evidence records shapes only. No later live creation or load is recorded in the repository.
2. View not re-applied after PR 1071. `infra/sql/resident-showcase.sql` binds the optional sensor tables only when they exist at apply time, and PR 1071 (`8b9553d8b`) added `COALESCE(home.stock_id, synthetic_stock_anchor_id)`. Nothing in the repository records a live apply since, so the live view cannot be assumed to carry either the sensor binding or the new stock link (the app's column allowlist passes with the earlier view, which already returned `sensor_home_id` and `sensors_json`).
3. Stock mapping unverified. The test resident's case body may carry only `synthetic_stock_anchor_id`; whether it matches a generated `home_id` could only be proved inside SQL. Not read: private route unavailable.
4. Hidden second blocker (source-evidenced): the committed backfill ends 2026-09-30 (`sensor_backfill.START` plus 730 days). The app marks readings older than 24 hours stale and suppresses the forecast, so loading the existing backfill unchanged would still not render gauges or a 24-hour forecast on 2026-11-04. A demo window ending within 24 hours of each walk needs a reviewed generator or loader change and an owner choice.

Causes 1 and 2 are each sufficient for the observed message; which of 1 to 3 holds live is not separated, because SQL cannot be read from here.

## Access route assessment

* Documented apply: `python3 infra/scripts/resident_showcase_sql.py <principal> --client-id <id-resident-demo client id> --apply <server> <database>` runs "with the current Azure CLI login, which must be the SQL Entra admin, from a host the private endpoint allows". Not satisfiable: login is not the admin and there is no private-routed host.
* A temporary firewall rule is not allowed: `infra/README.md` states SQL public access is always Disabled with no firewall in every profile and no firewall or policy-exemption workarounds. Not used; nothing changed.
* The prior route (generated external worker run through `job-cutover-test-init` with a temporary job template change, then exact restore) is evidenced only in tracking files for earlier owner-approved sessions; the worker is not in the repository. Reusing it needs a job-definition write, a permission-touching view reapply (GRANT/DENY batches) and a synthetic data load, which `infra/README.md` says need separate exact owner approval.
* `sensor_backfill.load_into(conn, ...)` is a library loader with `STOCK_SQL_DDL`; no command loads it into the live store.

## Decision

Stop before any live write; record the exact owner decision. No Azure resource was changed.
