<!-- markdownlint-disable-file -->
# Phase details: resident sensors live seed (#1072)

## Phase 1 commands (read-only)

* `az resource list`, `az containerapp job list/show`, `az containerapp show`, `az sql server list`, `az sql db list`, `az sql server firewall-rule list`, `az containerapp job execution list`.
* Playwright (Python) 390x844 walk of the live resident app; credentials read from `~/.ama-resident-test-user`, never printed or stored.

## Phase 3 (proposed, only after owner approval)

1. Save the exact `az containerapp job show -n job-cutover-test-init` JSON externally.
2. Run a generated external worker as `id-cutover-test-init` (SQL Entra admin) inside the VNet that: creates `dbo.sensor_register` and `dbo.sensor_reading` with `sensor_backfill.STOCK_SQL_DDL`; reads the test resident's stock link (`home.stock_id`, else `synthetic_stock_anchor_id`) inside SQL; loads one synthetic home with a window ending within 24 hours of the walk via `sensor_backfill.load_into`; renders and applies `resident-showcase.sql` with `--client-id` of `id-resident-demo` after `verify_principal`; checks the evaluated `sensors_json` projection for that case (not `TOP (0)`).
3. Restore the job definition exactly and verify the diff is empty.
4. Re-walk at 390 px and record gauges and forecast.
