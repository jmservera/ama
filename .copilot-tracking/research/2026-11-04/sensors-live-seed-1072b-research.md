# Research: live sensors seed (#1072), 2026-11-04

* Disposition: executed. Planning Readiness: Ready.
* Finding: the live sensor tables were empty and the resident view lacked the PR 1071 stock binding, so the signed-in resident saw the fail-closed message.
* Evidence read: `sensor_backfill.py`, `sensor_stock.py`, `resident_forecast.py`, `resident_showcase.py`, `infra/sql/resident-showcase.sql`, `infra/scripts/resident_showcase_sql.py`.
* Rules: the view reads the latest 48 readings per case; the forecast needs 6 readings within 24 h of the last and is stale after 24 h.
* Fact: the committed backfill ends 2026-09-30, so the existing deterministic generator is run with a window ending today.
* Fact: the test resident's case shares a stock anchor with 13 flats, so binding the anchor would expose the readings to neighbours.
* Owner approval (2026-11-04 to end of November 2026): one-off in-VNet jobs, SQL private, no firewall rule, restore spec with readback.
