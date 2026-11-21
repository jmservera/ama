# Plan: issue 470 gate scan count

* [x] Phase 1: update expected case journey scan count 87 to 91 in `tools/rpi-checks.py` and the fixtures/negative cases in `tools/test_rpi_checks.py` (details file).
* [x] Phase 2: run `python3 tools/test_rpi_checks.py`, ruff check/format and mypy for the tool.
Tier: full (gate semantics). Coordinator gate command: `python3 tools/rpi-checks.py --all --base <origin-main-sha> --out <new-external-dir>`; not run here.
