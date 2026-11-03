# Changes: issue #227 design-system and axe evidence

* src/api/tests/test_safety_screens.py: new rendered-class test (defined in CSS, documented, no inline style, expected components present).
* Evidence run (not a file change): `ZF_AXE_JS=<pinned axe 4.10.3> python3 -m checks.safety_screens_browser_check` with PYTHONPATH on this worktree's src trees. Result: no FAIL lines; axe found no violations and no incomplete items for Building Safety Liaison and Resident Liaison Officer, on both the per-home screen and the cross-home table at 1280px (main only); 320px reflow, Tab reach, no writes and no JavaScript errors pass.
* Validation run: test_safety_screens, test_role_screens, test_role_screens_conformance, test_design_system (36 pass); ruff check, ruff format --check, mypy (--cache-dir=/tmp/mypy-227) on the test.
* Not run: gate, benchmarks, full suites, AT, human acceptance. Tier: focused.
