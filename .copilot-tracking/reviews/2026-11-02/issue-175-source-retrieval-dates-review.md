# Review: issue #175 source retrieval dates (2026-11-02)

* Review execution: one inline self-review of the final diff (not independent; independent exact-head review still required)
* Outcome: partially conformant; criterion 2 of #175 remains unproven

## Evidence

* Dates 2026-10-01 for SRC-CENSUS-TS054, SRC-IMD-2025 and SRC-ONS-BOUNDARIES verified with `git log -S` (068fb08ce).
* `unittest tests.test_synthetic_provenance`: 12 tests OK. `source_issues` now returns exactly `SRC-ONS-BOUNDARIES:provisional_attribution`.
* No "(expected, owner to confirm)" wording remains in licences; the OS copyright year in the ONS boundaries attribution still reads "[year to confirm]".
* Focused gate `tools/rpi-checks.py --changed --base origin/main --lock-timeout 1800`: BLOCKED twice with "Global heavy-resource lock timeout" (other sessions held the lock for 1800 s each). No receipt exists; the gate is not passed.

## Routed follow-ups

1. Owner confirms the OS copyright year against the LSOA 2021 BGC and LAD December 2021 BFC product notices, then removes the provisional wording; the strict audit then passes.
2. Rerun the focused gate when the heavy lock is free.
