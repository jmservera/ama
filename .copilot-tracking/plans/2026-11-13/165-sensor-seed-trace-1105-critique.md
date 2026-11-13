# Critique: 165 sensor and stock seed trace (independent rubber-duck, single pass)

Verdict: Changes required (no user decision needed).

Blocking
* Probe source unspecified; `/tmp/probe-165.py` did not exist and no hash basis. 
* Sensor selection ambiguous: `sensor_stock.select` sorts all rows by id before taking first N, so filtering to consent granted first changes the subset; fixture has no consent field. Define N, seed, consent assumptions and order; label hypothetical.

Non-blocking
* Fixture findings cannot identify deployed conflicts or readings; keep fixture-only evidence separate; candidate ids are not live evidence.
* Distinguish absent key (generated JSON omits `stock_reconciliation`) from `[]` (store default). Flats can share an anchor, so a sensor match is not unique-dwelling proof.

## Disposition (all applied directly)
* Probe is created at `/tmp/probe-165.py` from the details file spec, sha256 recorded, source embedded in changes file.
* Sensor check: all rows get `monitoring_consent=granted` (hypothetical), `select(rows, homes=len(rows))` over the full fixture register (sorted), sensor seed 20260901; report whether each anchor yields a `sensor_key`; additionally report the default `sensor_backfill --homes` SYN register membership (anchors are TEST-* so no overlap).
* Findings split into fixture-only vs deployed-unknown; absent vs empty recorded; shared-anchor caveat recorded.
