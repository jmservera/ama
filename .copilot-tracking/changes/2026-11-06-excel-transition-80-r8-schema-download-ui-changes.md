# Issue 80 r8 changes: schema catalogue download on the finance funding screen

Chronology: r8 research, plan (with internal critique) and details were written before any test or source edit. Tests were then written and run to fail, then the source changed. r3 to r7 records are unchanged.

## Changed paths

* `src/api/src/zava_forward/api/web/role-screens.js`: `finance-funding` renders a "Form schema catalogue" panel with one `<a class="btn alt" href="/api/form-schemas.csv" download="form-schemas.csv">Download for Excel</a>` and plain-language scope text, only when `readable` (the `form-review` read succeeded). That read goes through the same `forms._actor` check as the catalogue, so the link is never decided from role names. When the read fails or is nonconforming, no link or panel appears and the existing "Unknown. The field review could not be read" text stays. No `onclick`, inline style, new class, API, core, CSS, dependency or other list change.
* `src/api/tests/test_finance_grants_screens.py`: `anchors` helper; two new behaviour tests (present with exact attributes and wording and absent from the invoices screen; absent for `null`, `{}` and a partly unreadable review); the existing no-anchor assertion in the keyboard-reachable test now permits only the `/api/form-schemas.csv` href and still rejects buttons, inputs, selects, textareas, `role=button` and `onclick`.
* README: not changed; the export route is already documented and the screen text carries the scope.

## Evidence (worktree paths; Python 3.12.3, ruff 0.17.3, mypy 2.4.1, node v24.21.0; bytecode off; external RUFF_CACHE_DIR and mypy cache)

* Imported `zava_forward.api.server` is `src/api/src/zava_forward/api/server.py` in this worktree.
* Test before fix: `python3 -B -m unittest tests.test_finance_grants_screens`: rc 1, 19 tests, 1 failure (the new present-link test). The absent-case test passed before the change because no link existed, so it guards the gating, not the missing feature.
* `node --check role-screens.js`: rc 0.
* After fix, nine API modules together (finance grants screens, role screens conformance, content standard, role screens, procurement screens, loading feedback, list export, role endpoint inventory, form staging): rc 0, 120 tests, OK, no skips reported.
* `ruff check --no-cache .`: rc 0. `ruff format --no-cache --check .`: rc 0, 115 files.
* `mypy --cache-dir /tmp/r8-80-mypy`: first run rc 1, one error in my test (`review` needed a type annotation, `var-annotated`, test line 241). Corrected with a typed list; rerun rc 0, 186 files. Finance module rerun rc 0, 19 tests.

## Not performed (stated plainly)

* No browser, keyboard, focus, download, screen reader or responsive run, and no accessibility-conformance claim. Future bounded check, not run: the existing employee-workspace browser check `src/api/checks/employee_workspace_browser_check.py` extended or a targeted check as Retrofit Programme Manager (reason-view enabled) opening `#/screens/finance-funding/<case>`, tabbing to "Download for Excel", asserting the download of `form-schemas.csv` with the expected header, and the same screen as Grants and Evidence Officer showing no link. Selector: `a[href="/api/form-schemas.csv"]`. Exact command to be chosen by the coordinator under heavy admission.
* If rights are revoked after the page loads, the server refuses the click (403); how a browser presents a refused `download` anchor is unverified.
* No FULL receipt, independent exact-head review or hosted CI. Every-list export and owner threshold criteria stay open; governance, resident, chat (RULE-026/AC-096), candidate and other lists are not exported.
