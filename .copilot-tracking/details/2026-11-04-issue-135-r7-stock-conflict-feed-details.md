# Details: issue 135 round 7

* `raise_conflict(..., ref=None)`: a repeated ref for the same kind returns the existing item, matching `raise_failure`.
* `feed_stock_conflicts(queue, cases, owner)`: cases are case mappings with `stock_reconciliation` and optional `stock_reconciliation_events`; status via `stock.query_status`. Values map `source_id` to `source`; original source keeps the case id, query id, query owner name and both full assertions.
* Not wired to the store; nothing calls it yet. Never resolves, withdraws or selects a source.
