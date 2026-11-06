# Issue 80 r9 research: executable browser regression for the schema catalogue download

Task `excel-transition-80-r9-schema-download-browser-check`, parent task r8. Intake head 1e56f443e9e8a1d1f5ba3be8f101ad7304e4665f, tree 1f06403f3c0ccb92e259cba4334ea9622e418f0b, ignored-inclusive status 0 entries, main bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f, parent `feat/case-workbench-integration-73` ead177ef90d24666557708ea344848a1be43bdf8. Research disposition: executed, read-only. Planning Readiness: Ready, with the browser run itself NOT admitted (#188 is the sole heavy owner).

## Honest qualification of r8 evidence

* r8 ran its second mypy command with output redirected to the same `/tmp/r8-my.log` as the first, overwriting the first raw file. The first failure (`tests/test_finance_grants_screens.py:241 var-annotated`, rc 1) survives only in the original tool event and in the r8 changes record. Original raw bytes were not recovered; this is not a claim of full raw preservation. The r8 Changes and Review are not rewritten. All r9 outputs use new absent paths under `/tmp/80-ui-browser-r9-1106/`.

## Harness inventory (verified in source at the intake head)

* `src/api/checks/finance_screens_browser_check.py` (#225) is the maintained Playwright check for the finance screens. README documents `PYTHONDONTWRITEBYTECODE=1 python -m checks.finance_screens_browser_check` (src/api/README.md line 1279), run from `src/api`. It is not named in `.github/workflows/src-ci.yml` or `tools/rpi-checks.py` by that module name (grep found no match); CI references `design_system_browser_check` and `case_journey_browser_check`. So this check is a documented manual or journey-lane check, not a CI-wired one. r8's prose named `employee_workspace_browser_check.py`; it was not verified as the right home and is not used.
* `checks.design_system_browser_check.main(browser_check, data_factory)` starts a loopback server with `ZF_STORE=json`, `ZF_AUTH=password`, `ZF_PASSWORD=synthetic-check`, scratch `ZF_DATA`, a clean environment and no model endpoints, then calls the check. `check()` raises on failure. Reusable as is.
* `checks.role_screens_fixtures.synthetic_data` builds the shared synthetic home (case ZF-1). Staff come from `workbench-manifest.json` and dataset: `pam@example.test` (Retrofit Programme Manager), `support@example.test` (Programme Support Officer), `grants@example.test` (Grants and Evidence Officer).
* Existing finance check weakness for this requirement: its "grants ... with draft" story routes `**/form-review` to a constructed response with `page.route`. Under the r8 change that story now renders the catalogue link for a Grants and Evidence Officer who the real server would deny. That story is therefore NOT evidence for the download and must not be reused for it. It makes no assertion that conflicts with the link (its no-write-control selector is `button, form, input, select, textarea`; an anchor is not in it).

## Authorization facts for the fixtures

* `forms._actor` needs Finance view AND resident-record view AND `projection.can_see_reason` AND document read. Default reason-view roles: Resident Liaison Officer, Building Safety Liaison, Retrofit Programme Manager. So Retrofit Programme Manager passes; Programme Support Officer and Grants and Evidence Officer are Finance viewers without reason view and are denied by the real intersection (r6 covered the Grants case at the API; the browser harness can show both denials for real).
* `finance-funding` is registered for `financeRoles` (Grants and Evidence Officer plus managers), so all three actors can open the screen; only the form-review read decides the link.
* The catalogue is empty in the synthetic data. Real content needs a schema registered through the real `POST /api/form-schemas` (pam only, 201) with the existing core fixture `schema()` in `src/core/tests/test_form_staging.py`; that module imports `dataset` and unittest, so it must be loaded with `src/core/tests` on `sys.path`. Seeding by direct JSON write would bypass the registration path and is not used.
* Browser login: the page sign-in form (`#email`, `#pw`, `button[type=submit]`) sets the session cookie in the Playwright context, so `page.request` shares it. No CSRF header is required for the password provider (the `X-ZF-CSRF` check applies to `trusted-proxy` only).

## Decision and limits

* New small module `checks/schema_download_browser_check.py` in the existing style (reuses `main`, `check`, `base_data`); no change to the finance check, runner, workflow or matrix. Production UI, API, core and CSS stay byte-identical to 1e56f44.
* It cannot be executed here: browser, server, SQL and install are not admitted. It is statically compiled, linted and type-checked only. Its behaviour is unproven until the coordinator admits one real run.
* Not covered: other screens, assistive technology, responsive redesign, axe (the existing check owns axe), refused-download presentation after a mid-session revocation.
