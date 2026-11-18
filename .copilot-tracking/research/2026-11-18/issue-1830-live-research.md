# Issue 1830 live research (2026-11-18)

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue 1830 body read in full; four unticked criteria (measure critical path, preflight, tests/docs, RPI artifacts and tier).
* `tools/rpi-checks.py` has modes `--all`, `--changed`, `--resume`, `--verify-receipt`; `--base` and `--out` are required for the first three. Extra selectors are validated by `extra_selector` (reviewed `PROJECT:test_module[.Class.method]` pattern) and a tracked-module check in `required_checks`.
* No retained receipt exists on this host: `/tmp/rpi-1297-pyc-full-20261116T1530Z/` is absent and no `/tmp/rpi-*/receipt.json` exists. Multi-receipt critical-path measurement (criterion 1) cannot be proven locally; `--all` is forbidden for this worker.
* The issue's single receipt gives wall 2733 s (~45m33s); longest command core unittest 1307 s. Not reproducible here.
* Owner decisions of 2026-11-18 (demo, no Azure needed): this issue is local tooling only; no live Azure used.

## Design

Add `--preflight PROJECT:selector` (repeatable) to `tools/rpi-checks.py`: validate selectors with the existing grammar, require tracked test module, run `python -m unittest -v` per selector in a read-only manner, fail closed on zero tests, skips or failures, and label output as non-receipt feedback. No receipt, no lock, no `--out`. Browser and SQL recipes are documented in `src/README.md` (prerequisites unchanged).
