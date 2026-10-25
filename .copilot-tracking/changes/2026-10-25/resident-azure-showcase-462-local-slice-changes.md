# Changes: synthetic resident Azure showcase, local slice (issue 462)

Written 2026-10-25 after implementation, before the independent Review. Refs #462, no closing keyword. Plan: `.copilot-tracking/plans/2026-10-25/resident-azure-showcase-462-local-slice-plan.md` (with critique amendments PC-001 to PC-005 from `.copilot-tracking/reviews/plans/2026-10-25/resident-azure-showcase-462-local-slice-plan-critique.md`).

## Process disclosures (not relabelled)

* Planning commit `5963fa3f` was pushed WITHOUT the required full gate, contrary to the explicit brief. It stays disclosed. The owner's #436/#459 process acceptance does not cover it, and no owner acceptance is invented here.
* No push, PR, heavy `tools/rpi-checks.py --all`, Azure, Graph, M365 or live SQL call, secret read/list/generation, job start or deployment was done in this continuation. No real password was generated.
* `origin/main` (PR #455 merge `c8d16059`) was merged without rewriting (`abd16893`).

## Added

* Core domain: `src/core/src/zava_forward/core/resident_showcase.py` (email canonicalisation, admission, identity map of at most 25, scrypt verifier, session and CSRF codec, limiter, positive-allowlist view, fail-closed config).
* Core SQL adapter: `src/core/src/zava_forward/core/resident_showcase_sql.py` (two fixed SELECTs on the view; no cache).
* SQL boundary: `infra/sql/resident-showcase.sql`; renderer `infra/scripts/resident_showcase_sql.py` (dry run by default).
* HTTP app and composition: `src/api/src/zava_forward/api/resident_demo/{__init__,__main__,app}.py` and `web/{index.html,demo.css,demo.js}`.
* Image: `src/api/Dockerfile.resident-demo` and its `.dockerignore` (non-root uid 10001).
* Tests and checks: `src/core/tests/test_resident_showcase.py`, `src/core/tests/test_resident_showcase_sql.py`, `src/api/tests/test_resident_demo_api.py`, `src/api/checks/resident_demo_browser_check.py`.

## Modified

* `src/api/pyproject.toml` (package-data for the web assets), `src/api/README.md`, `src/core/README.md`, `infra/README.md`, `docs/reference/README.md`, `docs/reference/log.md` (append-only entry).
* Not modified: the #444 `resident_preview` package, its guard and fixture, staff server, auth, store and Entra code.

## Actual validation (local, venv `/home/azureuser/.venvs/ama462`)

* Core `test_resident_showcase` + `test_resident_showcase_sql` with `ZF_TEST_MSSQL=1` against an owned loopback Docker SQL Server: 49 tests OK, 0 skipped (13 SQL tests skip without it).
* Core `test_resident_*`: 253 OK (77 skipped without SQL); `test_dependency_rule` OK.
* API `test_resident_demo_api`: 30 OK; `test_resident_preview_api`, `test_resident_api`, `test_dependency_rule` OK; `test_role_endpoint_inventory` 19 OK via `discover -s tests`.
* ruff check, ruff format --check and mypy clean for core and api; ruff clean on the infra script.
* Docker build OK; uid 10001; refuses to start without config and with a `ZF_STORE*` setting (exit 2); no `/data` or `/state`. The image was NOT run against SQL or Azure.
* Playwright browser check on the real server and real local SQL view: keyboard-only sign-in, `__Host-` cookies accepted on 127.0.0.1, HttpOnly/Secure/SameSite=Strict, generic failure alert focused, forged token 401, another case's handle 401, logout then replay 401, no horizontal scroll at 360 px, no script errors.
* Web files follow the fetched web-interface-guidelines where applicable (labelled inputs, autocomplete, focus on error, skip link, `touch-action`, `text-wrap`). This is an engineering check, not WCAG conformance or accessibility acceptance.
* Owned local Docker container and image were removed. Another worktree's resources were untouched.

## Blocked live criteria (unproven)

* G1: remaining budget headroom under the non-reset cumulative USD 50 cap is unknown.
* G2: live email-to-case equality and synthetic provenance; live cases have no per-case synthetic flag, the allowlist ships empty and needs named approval with provenance.
* G3: the budget-gated private job that creates the view and principal was not run.
* G4: Key Vault `kv-cutovertest-rzsrg` is named but no retrieval role or network route is proven; no secret read.
* Coordinator full gate, hosted checks and independent exact-head assessment are outstanding.
