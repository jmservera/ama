---
title: Issue 184 credential hygiene review
ms.date: 2026-11-01
---

## Review (single pass, self-review of the diff)

Execution: complete. Outcome: Conformant for scope; criteria not newly proven.

* Tests are outside the package, use only constructed markers, open no certificate files and touch no Azure.
* Scan excludes only its own file; patterns verified by a self-test.
* Limitation: scan covers text suffixes in src, infra, docs, .github, not git history or binaries; runtime test uses a fake SDK so SDK-internal logging is not covered.
* Routed follow-ups: owner acceptance of deferrals (criterion 1); actual credential lifecycle and Hub telemetry evidence after owner approval.

Independent and hosted review remain required; CI is the evidence.

## Correction cycle 1 (PR 704, 2026-11-01)

* Research: two unresolved Copilot threads on `src/api/tests/test_iot_credential_hygiene.py`, both valid: dotenv files (`.env`, `.env.local`) skipped by the suffix filter; `run_publisher` swallowed `StreamError` when no failure was injected.
* Plan/Changes: added `is_scanned` and `scan_directory` helpers plus a temp-directory dotenv regression test; re-raise `StreamError` unless a failure was injected.
* Review: ruff check and format clean; mypy shows the same 14 pre-existing `azure.iot.device` stub errors as before the change; 35 `test_iot*` tests pass in a local venv. No Azure access.

## Correction cycle 2 (PR 704, 2026-11-01)

* Research: one unresolved Copilot thread: the scan suffix allowlist omitted `.pem` and `.key`, so the private-key detector never read them. Valid.
* Plan/Changes: added `.pem` and `.key` to `SUFFIXES` and a `test_private_key_files_are_scanned` temp-directory regression test. Merged `origin/main` (log.md kept both sides; `role-screens.js` passes `node --check`).
* Review: ruff check and format clean; `test_iot_credential_hygiene` and `test_iot_stream` (36 tests) pass in a venv with the src projects installed; mypy shows only third-party stub errors (azure, playwright), none new. No Azure access.
