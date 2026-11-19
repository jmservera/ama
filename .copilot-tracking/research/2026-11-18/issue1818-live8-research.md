<!-- markdownlint-disable-file -->
# Issue 1818 held receiver fix: research (Refs #1818)

Disposition: executed (round 6 evidence reused). Planning Readiness: Ready.

## Finding

* On main (`2cd131da5`) `SensorConsumer.process` inserts `sensor_reading` and `sensor_delivery` only; `sensor_register` is never written on the live path, so live-only sensors are invisible to the resident view and map join (round 5 gap).
* Held commit `7bde5f149` (retained r-series branch) holds the fix: insert-if-absent register row in the accepted-reading transaction, `sensor_register` in the consumer DDL set (SQLite and SQL Server), receiver grant `SELECT, INSERT ON dbo.sensor_register` in `infra/README.md` and the grant test, plus a regression test.
* Scope touches SQL (receiver grants and DDL) so the tier is FULL. `/tmp/ama-rpi-heavy.lock` is held, so the full gate is not run; focused tests only, and the gate is reported as outstanding.
* Remaining unticked criterion: the live walkthrough. Round 6 evidence exists in the held commit's walkthrough note; it is carried forward with caveats, not re-run.
