# Issue 1830 live changes (2026-11-18)

Tier: FULL. Basis: `tools/rpi-checks.py` is a gate tool and gains a new mode; the coordinator must run the complete gate (not run here). No `src/` product code changed. No live Azure used.

## Files

* `tools/rpi-checks.py`: `--preflight PROJECT:SELECTOR` (repeatable, no `--base`/`--out`, no lock, no receipt); `preflight_unit`, `preflight`. `--base` still required for every other mode. Runner, groups, receipts and verification untouched.
* `tools/test_rpi_checks.py`: `PreflightTests` (malformed selector, untracked module, zero-test/skip/failure rejection, non-receipt label, no base/out needed).
* `src/README.md`: "Targeted preflight and gate timing" subsection with browser/SQL recipes and benchmark method.

## Validation

* `python3 -m unittest discover -s tools -p test_rpi_checks.py -q`: 114 tests OK.
* `python3 -m ruff format --isolated --line-length 100 --check` on both tool files: clean.
* Demo: `python3 tools/rpi-checks.py --preflight api:test_production_config_a11y_check` ran 3 tests OK (includes the 320px reflow overflow test); invalid `core:test_x` and `api:test_nonexistent_zz` rejected with BLOCKED, rc 1.
* Not run: `rpi-checks.py --all` (coordinator), mypy (no `src/` project modified), browser/SQL checks.

## Per-criterion table

| Criterion | Status | Evidence or reason |
| --- | --- | --- |
| 1 Measure wall time, queue wait, critical path across multiple receipts | Unproven | No retained receipt on this host (`/tmp/rpi-1297-pyc-full-20261116T1530Z` absent); `--all` forbidden for this worker. Method documented in `src/README.md`; issue's single receipt figures not reproduced. |
| 2 Preflight entry point rejecting zero-test/invalid selectors, non-receipt label | Proven (unit selectors) | Commands above and `PreflightTests`. |
| 2b Demonstrate #1297 320px regression caught pre-gate | Partly proven | Unit-level reflow test runs via preflight; the full browser regression needs Playwright server prerequisites not run here. |
| 2c #1828 map check rerun directly | Unproven | Documented as direct script recipe; not executed (no #1828 check in this branch scope). |
| 3 Focused tests/docs; benchmark with before/after | Tests and docs proven; before/after unproven | No optimization implemented, so no before/after claimed. |
| 4 RPI artifacts, tier, independent exact-head review, hosted CI | Artifacts and tier proven; review and CI pending | Independent review and hosted CI belong to the coordinator. |
