# Plan critique: Registry observation parent transition

One self-executed pass by the author; not independent. Proceed; amendments applied directly.

* T1: do not claim the `6cc59776` tests ran on `eff05737`; the evidence stays carry-forward and src identity is proven only by equal subtree ids. Applied.
* T2: do not rewrite the pin or trigger rows; `6cc59776` stays historical. Applied.
* T3: conflict resolution must keep main's squash text byte-for-byte and not reorder it. Applied (main side first).
* T4: stop if any non-docs conflict appears; none predicted.
* T5: the "child, not retargeted" statement becomes stale; only that wording changes.
