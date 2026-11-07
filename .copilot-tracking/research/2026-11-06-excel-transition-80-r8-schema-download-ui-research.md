# Issue 80 r8 research: form-screen download for the schema catalogue CSV

Task: `excel-transition-80-r8-schema-download-ui`, parent task r6 (same combined candidate, same branch). Intake head de931ff296ef842ca3bfa77a70717273b28340ca, tree 125e3a67e2e03eb3dd575b3bc106bc47cff9d910, ignored-inclusive status 0 entries, main bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f, parent `feat/case-workbench-integration-73` ead177ef90d24666557708ea344848a1be43bdf8. Research disposition: executed (read-only). Planning Readiness: Ready.

## Evidence

* Route: `GET /api/form-schemas.csv` (server.py LIST_EXPORTS and `list_rows`). It takes no case, reason or context parameter; the catalogue is portfolio-wide and the server authorises it with `forms.list_schemas` -> `forms._actor` (Finance view AND resident-record view AND reason-view AND document read). No URL parameters are needed or invented.
* The only web screen that already reads form data is `finance-funding` in `src/api/src/zava_forward/api/web/role-screens.js` (roles `financeRoles` = Grants and Evidence Officer plus Retrofit Programme Manager and Programme Support Officer). Its `load()` reads `/api/cases/{id}/form-review` and stores `null` on failure.
* `form_review.view` (core/form_review.py, line 389) calls the same `forms._actor(store, user)` first. A successful form-review read therefore proves, at that moment, the exact rights the catalogue needs. The screen already computes `readable` (drafts and decision_holds both arrays). No extra preload is required and no schema data is fetched by the browser.
* Role alone is not a safe signal: Grants and Evidence Officer and Programme Support Officer are on the screen but are denied by default (r6 test), and reason-view roles are configurable. So the link is shown only when the form-review read succeeded, never from role.
* Download patterns: semantic `<a class="btn alt" href=... download=...>Download for Excel</a>` plus "The file is a read-only copy; changes in it are not imported back." at role-screens.js (stock queue, gated by `extra?.queue`), ops.js:114, app.js:736, 2180, 2190. Reuse exactly. `btn alt` is a documented class.
* Existing tests: `src/api/tests/test_finance_grants_screens.py` runs `role-screens.js` in a node vm with a stubbed `api` and `h`. Two existing tests forbid any `a` tag on both finance screens (`test_roles_exclude_other_staff_and_no_controls` line 215 and `test_tables_are_keyboard_reachable_and_labelled` line 414). Their intent is "no action controls". A same-origin read-only download link is navigation, so those assertions must allow exactly this one link and nothing else.
* Conformance tests (`test_role_screens_conformance.py`) check classes exist in CSS, no inline style or handlers, native controls.
* Server stays authority: the click is re-checked by the route. Limitation: if rights change between page load and click, a `download` anchor to a 403 JSON response may save an error body or fail in the browser; same as existing download links. Not verified in a browser here.

## Decisions

* Placement: a new panel "Form schema catalogue" on `finance-funding`, rendered only when the form-review read succeeded. Text states it covers all forms, not only this home, lists every retained version with reviewer, evidence, recorder and time, shows unapproved status as recorded, is a read-only copy, and is not an approval or reviewed pack.
* No API, core, CSS, dependency or other list change. No new JS helper.

## Not verified / deferred

* No browser, keyboard, download or screen reader run (heavy lane is #79's). No accessibility conformance claim.
* Governance, resident, chat (RULE-026/AC-096), candidate and other lists, and owner thresholds remain open.
