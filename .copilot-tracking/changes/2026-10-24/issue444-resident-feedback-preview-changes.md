# Issue 444 changes: resident synthetic feedback preview

Date: 2026-10-24. Plan: ../../plans/2026-10-24/issue444-resident-feedback-preview-plan.md

## Added

* src/core/src/zava_forward/core/resident_preview.py: grant boundary (default-deny, re-read per request), positive-allowlist projection, safe-start guard.
* src/core/src/zava_forward/core/synthetic/resident_preview_fixture.py: disposable fixture builder (SYN-C1 confirmed, SYN-C2 offer only, SYN-C3 unrelated home with canaries).
* src/api/src/zava_forward/api/resident_preview/ (app, CLI entrypoint, web/index.html, resident.css, resident.js): separate loopback read-only server and page.
* Tests: src/core/tests/test_resident_preview.py (30), src/api/tests/test_resident_preview_api.py (14, real local server), src/api/checks/resident_preview_browser_check.py (35 checks, real Chromium against real server).

## Edited (shared paths)

* src/api/pyproject.toml: one additive package-data line. No other shared runtime file touched; server.py, auth.py, projection.py and store.py unchanged.
* src/api/README.md, src/core/README.md, docs/reference/README.md (index row), docs/reference/log.md (appended entry).

## Validation

* Focused: core 30 and api 14 tests pass; browser check 35 PASS.
* Full suites: core 1273 tests OK (167 skipped); api 973 tests OK (301 skipped).
* ruff and mypy clean for src/api and src/core.
* web-interface-guidelines fetched and applied to changed web files.

## Divergences and not performed

* No divergence from the plan beyond critique items C1-C4, applied directly.
* Accessibility skill harness not run (needs uv/npx); no human screen-reader audit; no live Azure, SQL or AI checks. Fluent 2 adoption is partial; this is not an accessibility acceptance.
* Complete local gate pending after Review and commit.

## Preview

* tmux ama-444-resident: window resA http://127.0.0.1:8444 (SYN-RES-A), window resB http://127.0.0.1:8445 (SYN-RES-B). Data /tmp/ama-444-preview-data.
