# Issue 1830 live plan

* [x] P1 Add `--preflight` mode to `tools/rpi-checks.py` (selector validation, zero-test rejection, non-receipt label).
* [x] P2 Add focused tests in `tools/test_rpi_checks.py`.
* [x] P3 Document preflight, browser/SQL recipes and benchmark method in `src/README.md`.
* [x] P4 Demonstrate on real selectors; record per-criterion table.

Tier: FULL (gate-tool edit changes `tools/rpi-checks.py`, a gate tool). Coordinator runs the full gate; this worker does not run `--all`.
