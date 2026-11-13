# Changes: 165 sensor and stock seed trace

Refs #165, #188, #1288, #134. Tracking-only; no edits to src/ or docs/. Evidence is fixture-only: the tests' fictional `TEST-*` register (6000 rows), seed 20260901, as-of 2026-10-13. It is not the private register or the deployed store.

## Commands and results

* venv `/tmp/venv-165-1105` (system-site-packages), `pip install --no-deps -e src/core -e src/api` exit 0. `zava_forward.core` and `sensor_backfill.__file__` resolved inside this worktree `src/core/src`.
* From `src/core/tests`: `python -m unittest test_sensor_backfill test_sensor_stock test_stock_fabric test_stock_reconciliation test_generated_dataset -q`: exit 0, 77 tests OK, log sha256 `051e7a66fc9afa85bb4b7e3d21a76cb8d9e2679f1c6489330e59927bb44688da`. Build reported 980 cases (443 open).
* Probe `/tmp/probe-165.py` sha256 `fcf8a9f97dedb9b4d53e056c70c4731e2e9a0af83c81b255302fc488cd2313aa`, exit 0, output sha256 `597d9e54bfb2827bc26548a593ad51e7f5b1a4437b96007fc74a1fa9d0bc2a70`. Method: patch `build_mvp_dataset.load_register` with the test fixture `register()`, run builder `--seed 20260901 --as-of 2026-10-13`, read the JSON; set all fixture rows `monitoring_consent=granted` (hypothetical), `sensor_stock.select(rows, homes=len(rows)).sensors(20260901)`; report per runbook home the anchor, `stock_epc.conflict_type`, `stock_reconciliation` (absent or value), hypothetical sensor key; then list cases with non-empty `stock_epc.conflict_type`. Venv, probe and scratch were removed afterwards.

## Findings

1. Case JSON never carries sensor keys, readings or proposals (no case key containing sensor or proposal), and no case has a `stock_reconciliation` key (0 of 980, absent). `core/store.py` defaults it to `[]` on load and fills it only from the stock-query action (human or API raised), so it is empty on a fresh seed by design. The seed signal for the stock story is `stock_epc.conflict_type`.
2. Sensor backfill is a separate generator keyed by register home id through `sensor_identity.sensor_key`. A case gets readings only when its `synthetic_stock_anchor_id` is in the backfill register selection with `monitoring_consent=granted` (sorted-id subset of `--homes N`). Under the hypothetical all-granted selection every fixture anchor gets a sensor, including the five homes; the default `SYN-nnnnn` backfill has no overlap with `TEST-*` anchors. Whether the five homes receive readings in a real run depends on the consent and subset choices, so it is not proven. Flats can share an anchor; here each anchor maps to one case.
3. Runbook homes (all `conflict_type` empty, `stock_reconciliation` absent): ZF-2025-0355 (TEST-B-terrace-205, not surveyed), ZF-2025-0382 (TEST-C-terrace-353, not surveyed), ZF-2025-0286 (TEST-C-bungalow-137, surveyed, no conflict), ZF-2026-0829 (TEST-A-terrace-242, not surveyed), ZF-2026-0892 (TEST-C-semidetached_house-258, not surveyed). The Wave-1 observation is confirmed for the fixture.
4. 41 fixture cases carry a seeded `conflict_type`, 18 open. Open: ZF-2025-0029 (heating_differs, Contact paused), ZF-2025-0030, 0031, 0032, 0041 (heating_differs, Waiting for block programme), ZF-2025-0111 (heating_differs, Aftercare issue), ZF-2025-0274 (band_differs, Quality check), ZF-2025-0466 (band_differs, Handover to arrange), ZF-2026-0922 and 0548 (construction_differs, Quality check), ZF-2026-0673, 0712, 0751 (band_differs, Quality check), ZF-2026-0753 (age_band_differs, Quality check), ZF-2026-0770 (age_band_differs, Install booked), ZF-2026-0958 (age_band_differs, Contact paused), ZF-2026-0977 (band_differs, Survey write-up), ZF-2026-0954 (age_band_differs, Survey booked). Closed ones (23) are omitted. Quality check candidates for the hook: ZF-2025-0274 and ZF-2026-0548, 0673, 0712, 0751, 0753, 0922.
5. No committed generator seeds proposals; the hook needs a runtime step (raise a stock query, then draft). These IDs are fixture evidence, not live deployed evidence; the private-register store may differ.

## Probe source

```python
import importlib, json, sys, tempfile, os
from pathlib import Path
from unittest.mock import patch

R = Path("/home/azureuser/source/ama-demo-wt/child-165-sensor-seed-trace-1105")
sys.path.insert(0, str(R / "src/core/tests"))
import test_generated_dataset as t
from zava_forward.core.synthetic import sensor_stock, sensor_identity

builder = t.builder
RUNBOOK = ["ZF-2025-0355", "ZF-2025-0382", "ZF-2025-0286", "ZF-2026-0829", "ZF-2026-0892"]
out = Path(tempfile.mkdtemp()) / "seed.json"
reg = t.register()
with patch.object(builder, "load_register", return_value=reg):
    with patch.object(sys, "argv", ["b", "--seed", "20260901", "--as-of", "2026-10-13", "--out", str(out)]):
        builder.main()
data = json.loads(out.read_text())
cases = {c["id"]: c for c in data["cases"]}

rows = [dict(synthetic_home_id=r["synthetic_home_id"], building_form_osm=r["building_form_osm"],
             locality_theme=r["locality_theme"], is_synthetic="true", monitoring_consent="granted") for r in reg]
sel = sensor_stock.select(rows, homes=len(rows))
sensors = {s["home_id"]: s for s in sel.sensors(20260901)}

top_keys = sorted({k for c in cases.values() for k in c})
print("case_keys_with_sensor_or_proposal:", [k for k in top_keys if "sensor" in k or "proposal" in k])
print("cases_with_stock_reconciliation_key:", sum("stock_reconciliation" in c for c in cases.values()))
print("register_rows", len(reg), "sensors_when_all_granted", len(sensors))
print("runbook homes:")
for cid in RUNBOOK:
    c = cases[cid]
    a = c.get("synthetic_stock_anchor_id")
    e = c.get("stock_epc") or {}
    print(" ", cid, "anchor=", a, "conflict_type=", repr(e.get("conflict_type")),
          "survey=", e.get("survey_status"), "stock_reconciliation=", c.get("stock_reconciliation", "ABSENT"),
          "sensor_key=", sensors[a]["sensor_id"] if a in sensors else None,
          "anchor_cases=", sum(1 for x in cases.values() if x.get("synthetic_stock_anchor_id") == a))
conf = [(c["id"], c["stock_epc"]["conflict_type"], c["stage"], c["closed"], c["synthetic_stock_anchor_id"] in sensors)
        for c in data["cases"] if (c.get("stock_epc") or {}).get("conflict_type")]
print("conflict cases:", len(conf), "open:", sum(1 for x in conf if not x[3]))
for x in conf:
    print("  ", *x)
```
