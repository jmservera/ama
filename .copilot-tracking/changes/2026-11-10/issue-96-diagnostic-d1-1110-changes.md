---
title: Issue 96 diagnostic D1 changes
description: Changes and additive validation qualification for the Held download test harness
ms.date: 2026-11-10
---

## Changes

* `src/api/tests/test_form_staging_api.py`: setUp, shutdown, call and working_review moved verbatim into a new `FormApiFixture(unittest.TestCase)`; `FormApi` inherits it. Still 14 tests.
* `src/api/tests/test_form_held_download_api.py`: plain sibling import `import test_form_staging_api as staging` (repository convention), subclasses `staging.FormApiFixture`, and the two direct calls to the unannotated `server.held_download_enabled` are replaced by `test_trusted_proxy_provider_never_serves_even_with_both_switches`, which drives the real route with the provider name patched to `trusted-proxy` and checks a normal request still serves. Now 6 tests (5 + 1).
* No production, core, guard, rights, browser-checker or role-screens change. Default-OFF flags, demo profile and trusted-proxy exclusion are unchanged.

## Qualification of the earlier validation claim (additive)

The parent record (02db2362) and handoff reported mypy as passed. That command used file selectors (`mypy src checks/held_form_download_browser_check.py`), so it did not load `tests/` and is not proof that the configured whole-API check passed. The default configured `mypy` (no selectors, from `src/api`) exited 2 on the parent candidate: unpinned mypy 2.4.1 in Root's log and pinned 2.4.0 in `mypy-pinned-before.log`. Parent ruff checks also ran as 0.17.3 instead of the declared 0.17.1. The parent artifacts are unchanged.

## Validation (pinned mypy 2.4.0, ruff 0.17.1, playwright 1.64.0; raw logs external under phase96-diagnostic-d1-evidence-1110/run/)

* Default configured `mypy --no-incremental` with no selectors: exit 0, 215 source files.
* `ruff check src tests checks`: exit 0. `ruff format --check` on the new test and checker files and the changed staging test: exit 0.
* Unit modules: held download 6, form staging API 14, finance grants screens 20, endpoint inventory 24, role screens conformance 11; core export 9, dependencies 10, review 23, staging 17: all exit 0.
* Served Held-download browser checker under non-queued `flock -n /tmp/ama-rpi-heavy.lock`: exit 0, 31 PASS, no axe scan, no AT or WCAG acceptance.
* Not run: SQL Server, hosted CI, blanket full or `--changed` gate, other browser checkers.
