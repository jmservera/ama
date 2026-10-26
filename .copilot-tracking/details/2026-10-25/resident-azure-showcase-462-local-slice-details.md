# Phase details: local implementation slice for issue 462

Written 2026-10-25 with `.copilot-tracking/plans/2026-10-25/resident-azure-showcase-462-local-slice-plan.md`, before critique and implementation. Original phase details (`resident-azure-showcase-462-phase-details.md`) are preserved unchanged.

## Phase A: domain (`src/core/src/zava_forward/core/resident_showcase.py`, `src/core/tests/test_resident_showcase.py`)

* Tests first for: `normalise_email` (NFKC, trim, lower), `build_identity_map`, `PasswordVerifier`, `SessionCodec`, CSRF, `LoginLimiter`, `showcase_view`, `ShowcaseConfig.from_env`.
* Exit: tests pass; mypy and ruff clean for core; no import of `resident_preview` functions except read-only constants.

## Phase B: SQL boundary (`infra/sql/resident-showcase.sql`, `infra/scripts/resident_showcase_sql.py`, `src/core/src/zava_forward/core/resident_showcase_sql.py`, `src/core/tests/test_resident_showcase_sql.py`)

* The SQL file creates schema, allowlist table and view and grants SELECT on the view only to the placeholder principal, with explicit DENY of write and DDL on the schema. The script validates the principal name, renders the file, and prints by default; `--apply` needs `ZF_SQL_*` and an operator token and is not run here.
* Local SQL Server tests are skipped unless `ZF_TEST_MSSQL=1` and the server is loopback (same convention as `test_mssqlstore.py`).
* Exit: tests pass against the owned local container; container removed.

## Phase C: HTTP and composition (`src/api/src/zava_forward/api/resident_demo/`, `src/api/tests/test_resident_demo_api.py`, `src/api/Dockerfile.resident-demo`)

* App and `__main__` as in the plan. Tests start the server on `127.0.0.1` port 0 and use `urllib` and raw sockets (Host spoof).
* Exit: tests pass; Docker build, non-root, refusal and health checks pass; the exact test containers and images are removed.

## Phase D: web and browser (`resident_demo/web/`, `src/api/checks/resident_demo_browser_check.py`)

* Guidelines fetched this session are applied while writing. Review changed web files against every fetched rule and record `file:line` findings in the review.
* Exit: browser check passes with real sign-in, forged 401, cross-case deny, logout and a keyboard-only sign-in; screenshots stay outside the repository.

## Phase E: documentation and evidence

* `src/api/README.md` section for the showcase, `src/core/README.md` pointer, `infra/README.md` pointer for the SQL script, a docs knowledge-base log entry. Changes artifact lists the ungated planning push deviation unaltered.
* Exit: Markdown reviewed; `git diff` reviewed.

## Phase F: review and commit

* One independent post-implementation review with original outcome preserved. One local commit with the privacy-safe identity and Copilot trailer. No push.
