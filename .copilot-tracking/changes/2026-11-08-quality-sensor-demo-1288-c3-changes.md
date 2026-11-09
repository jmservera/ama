---
title: Quality sensor demo 1288 C3 changes
ms.date: 2026-11-08
---

Recorded 2026-11-08T21:00Z (real clock). Start head `8d95ae96` (tree `32a3f744`), plan commits `c9562a90c`, `38a48ad6e`. Refs #1288. Source and light SQLite only.

## Finding dispositions

| # | Finding | Fix | Regression test |
| --- | --- | --- | --- |
| 1 | Context-only capture skipped consent projection | `sensor_view.capture_source` state `ok` when window or before/after exist; `_withhold_sensors` keys on captured citations | `test_context_only_capture_*` (ReadModel and Http) |
| 2 | Notes disclosed values/IDs | `verification.note`, `review.note` and event `note` stubbed while withheld; stored record unchanged | `test_review_notes_are_withheld_with_consent_and_return_when_it_does` |
| 3 | Gap branches ignored the schedule | `_due` shared by `scan` and `forecast`: exact-capture tasks and non-sensor changes still proceed, same coarse capture is throttled | `test_throttle_applies_with_*` (three gap branches, finite count) |
| 4 | 50-event window hid manual requests | `manual_requested` on the task, set by `_enqueue`/`_mark_requested`; `claim` proactive only on explicit `false` | `test_a_manual_request_after_many_events_*`, `test_unknown_dispatch_authority_*` |
| 5 | Control index only built by destructive configure | `ensure_control_home`/`reconcile_control_home`, `migrate_control_index`, `Assistants.migrate`; count guard fails closed | `test_migration_restores_*`, `test_partial_index_*`, `test_orphan_index_*` |
| 6 | Reject wrote the redacted projection | `review()` checks the view, writes the stored `_row`; verify/accept refused while withheld | `test_reject_after_withdrawal_keeps_the_stored_snapshot_and_output` |

One C2 test was adjusted: the key-access spy now allows the new `SELECT COUNT(*)` guard statements.

## Files

* `src/core/src/zava_forward/core/assistants.py` sha256 `595b9dd8...`
* `src/core/src/zava_forward/core/sensor_view.py` sha256 `8abd8786...`
* `src/core/src/zava_forward/core/sensor_consumer.py` sha256 `6ff04295...` (small diff, overlaps #184)
* `src/api/tests/test_quality_sensors.py` sha256 `7634f5f6...`
* `src/core/README.md` C3 paragraph. No web source edited, so no web-design-guidelines review was due.

## Raw evidence (task venv `/tmp/ama-1288-venv`, from `src/api`)

| File | Command | Exit | Result |
| --- | --- | --- | --- |
| `/tmp/c3-red-1.txt` | ReadModel+Http before source | 1 | 11 failures, 1 error (intended) |
| `/tmp/c3-green-1.txt`, `-2.txt`, `-3.txt` | intermediate runs | 1 | test-helper defects, fixed |
| `/tmp/c3-green-4.txt` | `test_quality_sensors` | 0 | 112 run, 56 skipped (Mssql variants) |
| `/tmp/c3-green-test_assistants.txt` | `test_assistants` | 0 | 120, 58 skipped |
| `/tmp/c3-green-test_assistant_release.txt` | `test_assistant_release` | 0 | 54, 4 skipped |
| `/tmp/c3-green-test_sensor_consumer.txt` | `test_sensor_consumer` | 0 | 37 |
| `/tmp/c3-green-test_sensor_ingestion.txt` | `test_sensor_ingestion` | 0 | 47 |
| `/tmp/c3-green-test_sensor_consistency.txt` | `test_sensor_consistency` | 0 | 38 |

Ruff (line length 100) passes on the changed files; `assistants.py` checked with F,E9 only (pre-existing long lines).

## PENDING, not passed

* FULL gate (`tools/rpi-checks.py --all`), receipt, exact-head independent review.
* Actual SQL Server Mssql variants (56 plus 58 skipped here are not SQL evidence) and query plans.
* Browser, axe, keyboard, reflow.
* Release and serving-model attestation; #184 semantic integration; live walkthrough.
