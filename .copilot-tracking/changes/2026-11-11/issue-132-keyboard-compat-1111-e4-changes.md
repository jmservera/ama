---
title: Issue 132 keyboard probe compatibility E4 changes and author review
description: Changes, red/green, static and browser evidence, and the single author Review for the staff-job-pack-intake keyboard probe repair (issue 132 E4)
ms.date: 2026-11-11
---

## Changes

Admission: [E4 amendment](../../plans/2026-11-11/issue-132-keyboard-compat-1111-e4-admission.md). Native session `3daf20c8-310c-4926-85ce-96019ffd6646`. Base `35eb0e559c7d0660ab87594732675b71be7bee67`; `origin/main` fetched and unchanged at admission, no rebase or merge.

* `src/api/checks/specialist_keyboard_browser_check.py`: one entry `"staff-job-pack-intake"` in `NO_REGION_GAPS`. Nothing else.
* `src/api/tests/test_specialist_keyboard_check.py`: `test_every_registered_screen_is_declared_and_unknown_screens_still_fail`. It asserts no failure for the screen with no table, rejection of an invented table, rejection of `unlisted-screen`, that every `registerRoleScreen` id in `web/*.js` is declared, and that parsed ids equal `registerRoleScreen(` calls (unsupported syntax fails closed).
* `src/api/README.md:4162`: `five` to `six` only.

## Red then green

* Red on the unchanged probe, system interpreter before the private HOME: `python3 -m unittest tests.test_specialist_keyboard_check -q`: Ran 7, failures=1, `region_failures("staff-job-pack-intake", [])` returned `screen staff-job-pack-intake has no declared region expectation or declared gap`.
* Green after the entry: Ran 7, OK (repeated under the private venv: Ran 7, OK).

## Static

Private HOME `/tmp/zf132-e4/home`, venv `/tmp/zf132-e4/venv`. First private-HOME attempt failed with `No module named ruff` and `No module named mypy` (user-site hidden). Minimal restore: pinned `ruff==0.17.1`, `mypy==2.4.0`, `playwright==1.64.0`, then editable core, agents and api only.

* `ruff check` on the two owned Python files: passed. `ruff format --check`: 2 files already formatted.
* Full API-project `mypy` once on the final source: exit 1. First run 24 errors, all missing optional imports (`mssql_python`, `azure.*`, `zava_forward.agents.*`). After the private installs and `MYPYPATH=../agents/src`: 2 errors, both `unused-ignore` at `tests/test_ai_consumption_api.py:22-23`, a file not changed here. Zero errors in owned files. Without `MYPYPATH` four errors remain in the same file. Not claimed as a clean mypy; the residual is a private-environment effect that was not tested against a base run.

## Browser (one run, no retry)

`flock -n -E99 /tmp/ama-rpi-heavy.lock timeout 900 python -m checks.specialist_keyboard_browser_check`, short scratch `/tmp/zf132-e4/s`, cached Chromium via `PLAYWRIGHT_BROWSERS_PATH`, no download, no axe. Lock was free and not queued. Exit 0 (04:03:50 to 04:04:20 UTC). Log `/tmp/zf132-e4/browser.log`, 863 lines, 805 PASS lines, no FAIL line, no uncaught JavaScript errors, 15 negatives rejected, `GAPS: 22`, 46 OBS lines. The count is a count of checks printed, not of acceptance criteria.

For `staff-job-pack-intake` all seven permitted roles (Retrofit Coordinator, Resident Liaison Officer, Building Safety Liaison, Grants and Evidence Officer, Quality Inspector, Retrofit Programme Manager, Programme Support Officer) produced an OBS with `regions: []`, the declared gap, home, handoff and reset keys present, and passed menu, status, focus, handoff and reset steps. Contractor was not served the screen (one screen, `contractor-job-pack`).

Narrow limit: the existing probe does not record `/api/workorders` HTTP statuses or the empty-order message (`endpoint_text` is false for this screen). The browser run therefore shows only that no evidence table rendered and that the walk steps passed. The absence of work orders remains source-derived and is not proven by this run.

## Author Review (one pass, not independent)

* Scope: three owned files only; no predicate, helper signature, `EXPECTED_REGIONS`, walk, negative-control, product, fixture, workflow or manifest change; #134 files untouched.
* Fail-closed behaviour is retained and tested; no wildcard, prefix or skip.
* Open: mypy residual above; empty-order cause not browser-observed; pinned tooling used in a private venv; no axe, assistive technology, human or acceptance claim. Whole #132, #134 and #233 stay open; no criterion ticked.
* Outcome: no blocking finding from the author. Independent exact-head review belongs to Root before push.

## Extension balance

Original C5 and E1, E2, E3 spent. E4 spent for this correction. One extension cycle (E5) remains. No reset or #134 authority transferred.
