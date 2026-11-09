---
title: Issue 1292 startup diagnostic record qualification research
ms.date: 2026-11-09
task_id: 1292-startup-diagnostic-qual-1109
---

## Disposition and readiness

* Research executed (read-only, no reruns). Planning Readiness: Ready.
* Trigger: independent Readiness review of frozen head `59accfa1ca9be77f2e98faf5ef862deba76cf941` (tree `93e1bf9f2bf563e22ed4c34c1eb84c46f2fd1085`, base `ef28d4da42d83b111d48f14df9b70e3c4932a477`), verdict approve_with_comments: three Medium and one Low evidence-interpretation findings (RQ-1..RQ-4) plus provenance limits.
* Scope: qualify wording only in a NEW dated record. The original authored research, plan, details, critique, changes, review and state record, and the raw evidence, stay byte-identical. No source, harness, test, rerun, SQL, browser, stress, model, cloud, credential or cleanup action. Original six attempts and E4 history are immutable; E5 is not spent; one productive source correction remains; nothing is granted or reset.

## Evidence cross-checked (existing artifacts only)

* RQ-1 Six non-reproducing runs (four observed) are retained in `/home/azureuser/source/ama-demo-wt/logs-1292-startup-diagnostic/`. None varied the six-module API workload or I/O pressure, so neither is shown necessary or sufficient. The original failure's thread, statement and traceback are UNKNOWN (`logs-440-sqlwave/core-store-priority.log:424-441`, assertEqual(errors, [])).
* RQ-2 Observer traces (`I2/I3/C2/C3.observer.json`) hold statement-start events only; there is no COMMIT-return event. Holder COMMIT trace to the next waiter event is 1.80-2.03 s; that interval includes commit work, scheduling, and waiter wake-up. In I3, C2 and C3 the waiter's first later event is a COMMIT closing an earlier BEGIN IMMEDIATE trace, before its `_migrate_recommendations` entry; in I2 the first later waiter event is the COMMIT at 8.0005 inside its `_migrate_recommendations`. The waiter can therefore be blocked in an earlier migration. Backfill wrapper intervals (`_backfill_zero_ordinals` enter to exit) are 1.10-1.17 s.
* RQ-3 `sqlstore.py:224,258` set `PRAGMA busy_timeout=5000` (SQLite per-lock wait). `tests/test_priority_order.py:734-735` assert `errors == []` then `elapsed < 20.0` for the opener phase; the original failure stopped at the first, so the duration assertion was not reached.
* RQ-4 Unittest-reported durations 15.161-16.097 s; process wallclocks (`core_end - core_start` in `.meta`) 16.844-18.057 s; both below the 180 s cap.
* Observer limit: `observer_run.py` `trace_open` appends to `RAISED` unguarded in the `_open` exception path, and a failure to install `set_trace_callback` is suppressed. The four records show `ok: true` and empty `raised`; no recorder error was observed, but harmlessness of every possible recorder failure is not guaranteed.
* Provenance: producer transcript shows a sqlstore.py hash and an import-origin command, but complete per-module import output and the three-file hash promised by plan FR1 were not retained; the owned venv was removed. Not reconstructed here.

## Follow-ups

* Coordinator decision on E5 scope and any separately authorized diagnostic remain open. Nothing is concluded about cause (H1 to H4 stay unknown).
