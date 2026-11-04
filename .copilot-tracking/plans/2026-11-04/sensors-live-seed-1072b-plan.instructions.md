# Plan: live sensors seed (#1072)

1. Add `infra/scripts/resident_sensor_seed.py` and its image recipe (reuses `sensor_backfill`).
2. Build locally, push inside a short registry window, restore private.
3. Run one-off job executions with per-execution overrides: whoami, seed, map, view, verify.
4. Re-walk signed in at 390 px; file a bug if anything breaks.
5. Document in `infra/README.md`, the UX review note, index and log.

Decision: unique home id plus per-case `home.stock_id` for strict isolation. Details: [details](../../details/2026-11-04/sensors-live-seed-1072b-details.md).
