# Details: #225/#226 static UX verification

* P1: git -C prior show bfc8ab5c5:<path> > <same path>; verify with cmp.
* P2: view role-screens.js asset-board and finance sections and style.css rules; findings table with file:line, rule, severity, disposition (no source edits; defects become follow-ups).
* P4: python3 -m venv /tmp/venv-225-1045; pip install -e src/core -e src/agents -e src/api; python -c print zava_forward.api.__file__; run python -m unittest -v tests.test_asset_board_screen tests.test_role_screens tests.test_role_screens_conformance from src/api with PYTHONPATH unset to mvp (core/agents tests dirs only if needed); record status from the producer via a status file; rm -rf venv.
* Success: tests exit 0 or failures recorded honestly; git status clean after commit; git diff --check exit 0.

## Critique amendments
* Run tests from src/api/tests with bare module names (python -m unittest -v test_asset_board_screen ...), record __file__ and counts; check node -v first.
* Prior paths: .copilot-tracking/research/*225-226-finance-asset-readiness-0630-research.md and .copilot-tracking/rpi-sessions/*225-226-finance-asset-readiness-0630-state.json (historical; no overwrite).
* Static audit is partial evidence; criterion 4 (assistive-technology) and WCAG conformance stay unclaimed; rules without evidence are "not assessed".
