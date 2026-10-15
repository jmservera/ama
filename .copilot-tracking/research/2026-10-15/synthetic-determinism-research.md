# Research: determinism, seeds, versioning (#176, parent #165)

* Disposition: executed. Planning readiness: Ready.
* PR #237 delivered MVP builder and pack manifests (seed, as_of, generator_revision) with tests.
* Gap: `zf_stock_fabric.py` and `zf_stock_epc.py` (derived from the stock register) record seed but no generator revision and have no determinism test.
* Not in repository: stock register generator (samples real OpenStreetMap anchors) and any sensor generator (depends on #177 to #183). Cannot be made deterministic without inventing them.
* Refresh policy exists as proposed defaults; owner approval pending.
