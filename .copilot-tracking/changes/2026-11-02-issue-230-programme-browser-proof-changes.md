# Changes: issue 230 programme screen browser proof

* `src/api/checks/role_screens_browser_check.py`: scenario 230 (`check_programme`, `programme_data`, `load_axe`, `scan_main`).
* `src/api/README.md`: documents the 230 check, `ZF_AXE_JS` and the evidence boundary.
* No production web, core or API change.

Observed: 64 PASS lines for scenario 230 with axe 4.10.3 (wcag2a/aa, 21, 22aa) reporting zero violations for `main` only at 1280 px on the programme overview and the connected home view for both roles (4 scans). Without `ZF_AXE_JS` the run now prints PARTIAL instead of reading as a pass. Scenario 232 and the parent run still pass. The coordinator projection withholds return reason and sender ("Held for roles with a recorded need"), which the check asserts as the expected boundary.
Not done: web-design-guidelines source was not fetched because no web file changed; assistive-technology testing and Fluent adoption remain open.

## Correction note (2026-11-02, after independent review FAIL)

Original text above is preserved. Corrections:

* Gate: Gate result (2026-11-02, two attempts): `python3 tools/rpi-checks.py --changed --base origin/main --lock-timeout 600` reported `BLOCKED: Global heavy-resource lock timeout` both times (/tmp/ama-rpi-heavy.lock held by another session). The focused gate has NOT passed; no receipt exists. Publication remains blocked until it is rerun.
* Divergences from the original claim: the original recorded the gate as passed with no blockers; that was unsupported. Browser check re-run locally in a venv (pip, non-editable): scenario 230 passes with and without `ZF_AXE_JS` (PARTIAL without), parent run passes. Editable-install egg-info had to be cleaned because the gate rejects ignored inputs.
* Code: writes detection now flags any method outside GET/HEAD/OPTIONS (sign-in POST excluded by timing, commented); vacuous `check(..., True)` replaced with a real assertion; OR-based readiness assertion tightened to "no 'ready' wording"; axe skip is tracked and summarised as PARTIAL.
