# Issue 1420 current-main validation record (2026-11-11)

Additive to the changes file and author Review; those are unchanged. Raw evidence: session folder `files/priv1420/final-main/` (`imports.txt`, `focused124.log`, `intake4.log`, `mypy-project.log`, `ruff.log`, `main-hunk.txt`, `head-hunk.txt`).

## Integration

* Amendment commit, then ordinary no-ff merge of main `1b169fe7d4f9b5a005123c8eb1825028ea431612`; no conflicts. Versus `fa497143c` the only non-tracking changes are `src/api/tests/test_staff_intake_api.py` (+53) and `.github/rubric/scores/latest.json`.
* `git diff --quiet fa497143c HEAD` over `src/api/src/zava_forward/api` (incl. `web/`), `src/api/checks` (incl. fixtures), the three feature test files, `src/api/README.md`, `src/core` and `src/agents`: equal. Feature blobs are identical to fa497.

## Tests (private venv, own-source imports verified in `imports.txt`)

* Existing focused selection: 124 tests, OK.
* Four new inventory/QA tests (two methods on `StaffIntakeApi` and on `JsonStaffIntakeApi`): 4 tests, OK, no skips. `StaffIntakeApi` is the non-JSON (`sql` default) class; MSSQL class not run.

## Static checks

* ADVERSE: project `python3 -m mypy` (from `src/api`, config `[tool.mypy]` strict, files src/tests/checks; tool 2.4.1, repo pin 2.4.0 not installed, no install done) exits 1 with 13 errors, all in files this issue authored: `tests/test_resident_choice_export.py` (8), `tests/test_resident_choice_screen.py` (4), `checks/role_screens_browser_check.py:734` (1 operator error from `str + None`; the log counts 2 for that file). `server.py` is covered only under the project's `ignore_errors` override, so it adds no errors but is not strictly typed. The new serializer module itself has no error. The hosted `src-ci` Type check would fail on this. Not corrected here (no feature file edits authorised); route to Root as a correction decision.
* Ruff 0.17.3 (pin 0.17.1): `ruff check` clean on the six changed Python files. `ruff format --check` reports three files; all three (`server.py`, `test_role_endpoint_inventory.py`, `role_screens_browser_check.py`) are also unformatted on pinned main, and the browser-checker hunk (line 222) is byte-identical on main (`main-hunk.txt` equals `head-hunk.txt`). My own added lines in these files need no reformat.
* `node --check role-screens.js`: exit 0.

## Browser

No fresh run. The earlier story 232 Chromium/axe run (exit 0, zero axe violations) is retained as source-equivalent evidence only: all application, web, checker, fixture, core and agents inputs are blob-equal to the tree that was run.

## Limits

No full gate, private data, cloud, install, push, PR or issue write. Independent review, hosted CI and human acceptance are not claimed.
