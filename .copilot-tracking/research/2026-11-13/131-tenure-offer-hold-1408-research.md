# Research 131 tenure before offer
Disposition: executed. Planning Readiness: Ready.
* Legacy exemption: `resident_decisions._inventory_managed(c)` is False for cases with no tenure fields, so `resident_gate` skips the tenure hold (AC2).
* Managed cases are always held: `resident_gate` returns refusal reasons plus TENURE_HOLD whatever the inventory says, so a verified route can never proceed.
* Open triggers, stale links, ambiguous identity already appear as inventory reasons (AC5, AC6 covered by `tenure_inventory_view`).
* Owner decision Batch-2 Q3: hold unknown tenure before offer.
