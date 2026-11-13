# Research: 165 sensor and stock seed trace (seed 20260901)

Refs #165, #188, #1288, #134. Base 3b05143179f83235c5b4e80e70aad99bdc44d83f.
Scope: committed synthetic generators only; no private data.

Docs read at start: case study original and addendum, reference README, memory (scope-relevant sections only for time budget).

## Findings (static, committed code)

* Cases come from `support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/build_mvp_dataset.py` (seed 20260901, as-of 2026-10-13). Each case carries `synthetic_stock_anchor_id` (a stock register home id). `stock_epc` is attached from `zf_stock_epc.epc_record` (surveyed rate 0.35, conflict rate 0.08 of surveyed, so about 2.8% of homes carry a non-empty `conflict_type`).
* The builder never writes sensor keys or `stock_reconciliation` into the case JSON. `stock_reconciliation` is a runtime list created only by the stock-query API path (`core/store.py` ~566-571) and defaulted to `[]` on load (`store.py` 489). A fresh seed export therefore always shows it empty. The seed signal for the stock story is `stock_epc.conflict_type`.
* Sensor backfill (`core/synthetic/sensor_backfill.py`, `sensor_stock.py`, `sensor_identity.py`) is a separate generator keyed by register home id (`SYN-nnnnn` default, or `--register` CSV with consent). Sensor id is `sensor_key(home_id)` (hash), so a case receives readings only when its `synthetic_stock_anchor_id` is in the backfill register with consent `granted`. The register for the demo cases is the private north-east register, not available here; tests use the fictional `TEST-*` register.
* Proposals: no generator seeds them in the case JSON (not found in generator or core by grep).

## Hypothesis to verify

Under the committed fictional test register, the five runbook homes have anchors with no sensor rows unless chosen as the backfill register subset; conflict-bearing case IDs are listable from `stock_epc.conflict_type`.

Planning Readiness: Ready
