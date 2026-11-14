<!-- markdownlint-disable-file -->
# Review: C1 manifest SHA fix

* Execution: executed once, self-review. Outcome: conformant; no open findings.
* Tier: Focused (pip venv /tmp/venv-203-c1, no uv; removed afterwards).

## Validation run

| Check | Result |
| --- | --- |
| unittest `src/core/tests/test_scenario_manifest.py` | Ran 8 tests, OK |
| unittest `src/core/tests/test_needs_inventory.py` | Ran 11 tests, OK |
| `python3 tools/check-legacy-references.py --base 3033dc9c21e57c7f86eca3882fffaf7e9a025033` | references: 0 violation(s); links: 0 violation(s) in 21 document(s) |
| `python3 -m unittest tools/test_check_legacy_references.py` | Ran 7 tests, OK |
| `ruff check` (CI scope `src/core`, plus branch-changed .py files) | All checks passed |

## Notes

* A repo-wide `ruff check src/core tools` reports 117 pre-existing errors outside CI scope (CI runs per project directory); unrelated to this change.
* Hosted CI for the new head is not observed; human approval and independent exact-head review remain required.
