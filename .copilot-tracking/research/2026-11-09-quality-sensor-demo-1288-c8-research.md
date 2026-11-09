---
title: Quality sensor demo 1288 C8 recovery research
ms.date: 2026-11-09
---

Written 2026-11-09T08:00Z, before any C8 edit. Refs #1288, #107, #91, #231. Research disposition: executed (inventory of surviving records plus fresh validation). Planning readiness: Ready for a bounded validation correction only.

## Authority and boundary

* Demo recovery brief (coordinator session `demo-rpi-common.md`, 2026-11-09): owner-selected demo-targeted test tier replaces the full local gate; modified and impacted modules run with existing unit, SQL and browser checks; no `rpi-checks --all`; no push, PR, merge, real model call, cloud write, role grant or spend. Hosted checks and independent exact-head review stay mandatory.
* Seed: unpublished C7 candidate `391e42f0d` (branch `feat/quality-sensor-demo-1288`, tree unchanged). Recovery branch `feat/demo-recovery-quality-1288-1109`. `origin/main` fetched at `b46a9ad9a`; merged locally as `d808e83f1` without conflicts (five commits, none touch the quality modules).
* The 1288 issue comments record the C7 independent review (Revise: 5 High, 1 Medium: consent withdrawal versus physical sends and direct database writes, manual/proactive scheduling, bounded legacy-history adoption, coalescing under continuous readings, unavailable readings misreported as missing). The full finding file is not in this worktree; those findings are retained as open adverse evidence and are not claimed fixed by C8.

## Inventory of genuine surviving evidence

* Original research, plan, details, changes, review and state for the parent loop and corrections C1 to C7 under `.copilot-tracking/{research,plans,details,changes,reviews,rpi-sessions}/2026-11-08-quality-sensor-demo-1288-*`. C7 changes and review record light SQLite and loopback evidence only; SQL Server, browser, axe, #184/#1292 integration and live evidence were all pending. Temp logs and gates from the original runs were removed and are not treated as evidence.
* Existing mature code: `sensor_view.py` (bounded permission-projected read model), `sensor_consumer.py` (retained consumer, control and consent), `assistants.py` (capture, citation, versioning, schedule, dispatch gate, review flag), `ai.py` and `ai_consumption.py` (gated transport), `assistants.js` (employee UI). Nothing is recreated.

## Fresh validation 2026-11-09 (this worktree, merged head `d808e83f1`)

Environment: worktree-local venv `.venv-1288` (editable installs of `src/core`, `src/agents`, `src/api`, hashed `src/api/requirements.txt`); the previous editable installs pointed at the primary checkout, so any earlier run in a shared interpreter would not have tested this source.

* SQLite and loopback, from `src/api` with `PYTHONPATH=../core/tests:../agents/tests`: `test_quality_sensors_c7` 48 tests OK (7 skipped); `test_quality_sensors` 187 OK (92 skipped); `test_assistants` 120 OK (58 skipped); `test_technical_quality_screens` 16 OK; `test_sensor_consistency` 38 OK; `test_sensor_handover_demo` 4 OK; `test_sensor_sql_check` 4 OK.
* The skips are exactly the SQL Server variants. Heavy lock `/tmp/ama-rpi-heavy.lock` was free (`flock -n` succeeded); a foreign container `zf-1292-sql` (the #1292 session) was left untouched. An owned container `zf-1288-sql` (label `ama.rpi.owner=issue-1288-c8`, 3 GiB, 2 CPU, loopback port, generated password not recorded) ran the same three SQL-bearing files with `ZF_TEST_MSSQL=1` under the nonqueued lock, then was removed.
* SQL Server result: `test_assistants` 120 OK, no skips. `test_quality_sensors_c7` FAILED (1 error). `test_quality_sensors` FAILED (1 failure).

## Confirmed remaining blockers from the actual SQL run

* B1 (confirmed): `MssqlPerHome.test_moving_a_sensor_waits_for_the_old_home_and_a_batch_only_for_changed_homes` raised `SENSOR_DISPATCH_IN_FLIGHT` in its setup `configure()`, and `MssqlHttp.test_withdrawal_cannot_commit_between_the_final_check_and_provider_transport` saw one `assistant_dispatch_gate` row left over (`1 != 0`). Reading `test_assistants.MssqlFixture.setUp`: it drops a fixed table list that predates the C5 to C7 tables (`assistant_schedule`, `assistant_dispatch_gate`), and the database `zf_test_assistants` persists. `PerHome` tests insert gate rows with a 600 s expiry; the previous test's row for `ZF-2` was therefore live in the next test. Hypothesis: the failures are fixture isolation, not a product leak. This is to be proven by fixing the fixture and rerunning, not assumed; a residual failure after isolation is a product defect.

## Dependencies

* #1292 (separate ready fix) may change store and `sqlstore` creation and schema paths; not imported. Its overlap with `assistants.py` and `sensor_consumer.py` schema creation must be reconciled by the coordinator after either merges.
* #184 transport parent recovers independently; source consumes the delivered retained interface. Live chain acceptance (AC8) waits for merged transport, release admission and existing finite authorization.

## Out of scope

Rewriting the C7 gate design, the five High review findings, browser/axe execution on the real UI (separate slice, see plan), production hardening, real model calls.
