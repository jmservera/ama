# Changes: issue 230 programme screen browser proof

* `src/api/checks/role_screens_browser_check.py`: scenario 230 (`check_programme`, `programme_data`, `load_axe`, `scan_main`).
* `src/api/README.md`: documents the 230 check, `ZF_AXE_PATH` and the evidence boundary.
* No production web, core or API change.

Observed: 64 PASS lines for scenario 230 with axe 4.10.3 (wcag2a/aa, 21, 22aa) reporting zero violations on the programme overview and the connected home view for both roles. Scenario 232 and the parent run still pass. The coordinator projection withholds return reason and sender ("Held for roles with a recorded need"), which the check asserts as the expected boundary.
Not done: web-design-guidelines source was not fetched because no web file changed; assistive-technology testing and Fluent adoption remain open.
