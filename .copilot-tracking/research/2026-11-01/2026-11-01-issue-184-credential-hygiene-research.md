---
title: Issue 184 credential hygiene research
ms.date: 2026-11-01
---

## Disposition

Research executed 2026-11-01. Planning Readiness: Ready.

## Prior delivery (do not redo)

* #508 (merged): finite opt-in X509 publisher and consumer, versioned schema, speed, pause, stop, burst, disconnect, budget and rate controls, sanitized failures.
* #557 (merged): approved Basic B1 hub reconciliation, publisher activation gate. No devices or credentials issued.
* #637 (merged): cost estimate, quota headroom, run controls. #486 backfill (#177 closed). #698 (open): local handover demo (Refs #188).
* Issue comments (coordinator, closure audit batch 2): criterion 1 unmet (owner acceptance of deferrals); criterion 3 has partial safeguards only, lacking log/telemetry/source assurance tests.

## Remaining slice deliverable without Azure

Criterion 3 local evidence: no existing test scans the repository for key or connection-string material, and none captures logs, truth records and wire payloads from a publish run. Source reading of src/api/src/zava_forward/api/iot_stream.py: publisher uses only create_from_x509_certificate, no logging, failures collapse to stable codes.

## Not deliverable here

Real credential issue, storage, rotation, revocation, live exercise, owner acceptance of child deferrals (criterion 1). Azure-live work is not authorised.

## Correction cycle 1 (PR 704, 2026-11-01)

* Research: two unresolved Copilot threads on `src/api/tests/test_iot_credential_hygiene.py`, both valid: dotenv files (`.env`, `.env.local`) skipped by the suffix filter; `run_publisher` swallowed `StreamError` when no failure was injected.
* Plan/Changes: added `is_scanned` and `scan_directory` helpers plus a temp-directory dotenv regression test; re-raise `StreamError` unless a failure was injected.
* Review: ruff check and format clean; mypy shows the same 14 pre-existing `azure.iot.device` stub errors as before the change; 35 `test_iot*` tests pass in a local venv. No Azure access.

## Correction cycle 2 (PR 704, 2026-11-01)

* Research: one unresolved Copilot thread: the scan suffix allowlist omitted `.pem` and `.key`, so the private-key detector never read them. Valid.
* Plan/Changes: added `.pem` and `.key` to `SUFFIXES` and a `test_private_key_files_are_scanned` temp-directory regression test. Merged `origin/main` (log.md kept both sides; `role-screens.js` passes `node --check`).
* Review: ruff check and format clean; `test_iot_credential_hygiene` and `test_iot_stream` (36 tests) pass in a venv with the src projects installed; mypy shows only third-party stub errors (azure, playwright), none new. No Azure access.
