# Issue 220 live review (2026-11-21), executed once

Outcome: Conformant for the code fix and documentation; criterion 5 remains unproven live (not claimed).

* Fix is narrow: oid optional only when the roster row records none; code and email still must match; verified principals tie code and email to oid.
* Regression test fails before, passes after; 491 related tests pass.
* Routed work: owner authorises a demo API rebuild, then re-run `run1.py` to observe a live successful write; do not tick criterion 5 before that and before any human acceptance.
