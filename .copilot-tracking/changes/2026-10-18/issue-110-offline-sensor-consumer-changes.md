---
title: Issue 110 offline sensor consumer changes
description: Actual implementation and validation evidence, including initial failures
ms.date: 2026-10-18
---

Task: issue-110 / issue-110-offline-sensor-consumer. Full plan execution.
Pinned base: 578631ac75cc8c6a7af53922c6aaae4435e7761c.

## P01 implementation

Started after rpi-implement activation and seven direct critique dispositions.
No implementation workers. No shared-store/infra/UI/assistant modifications.
Core processor reuses sensor_reading with task-owned schema checks and additive
legacy MSSQL schema-version width compatibility. Independent transaction-owned
connections read current constructed controls/home and append reading/outcome/DQ.
API callable preflights finite envelopes and reports stopped-batch prefix plus
uncertain outcome reference. Exact historical replay cannot re-admit.
Dedicated restricted metadata inspection does not register an HTTP route.

P01-T01/P01-T02 implemented; focused core 19 and API 25 cases cover the contracts.

## Actual validation and initial failures

* Initial `python3 -m unittest discover -s src/api/tests -p
  test_sensor_ingestion.py -q`: 1 error, distributions absent.
* `python3 -m pip install --quiet --user --no-deps -e src/core -e src/agents
  -e src/api`: PEP-668 externally managed environment refusal. No override used.
* Created session-owned --system-site-packages venv and installed local editable
  distributions with --no-deps. Same test: 1 error specifically missing
  zava_forward.api.sensor_ingestion, establishing requested fail-before.
* Actual core SQLite `PYTHONPATH=src/core/tests <venv>/bin/python -m unittest
  discover -s src/core/tests -p test_sensor_consumer.py -q`: 19 tests passed.
* Initial API SQLite run: 25 tests, 1 assertion failure. The privacy assertion
  wrongly matched SENS inside the bounded code SENSOR_SQL_UNAVAILABLE; corrected
  to assert the actual constructed device identifier is absent. SQL runner had
  not started because the combined command stopped at that failure.
* Tool probes: Ruff/mypy modules absent. Installed repository-pinned versions
  0.17.1/2.4.0 only after those missing-tool failures.
* Initial changed-file Ruff: 7 findings (import sorting, three long lines, three
  loop-variable closure bindings). Formatting/import fix and explicit bound
  test closure parameters applied; no production authority change.
* After the privacy assertion correction, API SQLite: 25 tests passed.
* First SQL container attempt failed before tests: mssql-python rejects the
  Connection Timeout connection-string keyword. Container removed by finally.
  Removed that unsupported keyword, not an engine-test pass.
* Initial core mypy: 2 errors (SQL datetime parameter list inference and
  variable-length count tuple annotation). Corrected explicit object parameter
  boundary and honest variable tuple annotation. Ruff pre-format rerun still
  reported 3 long lines before formatter fixed them; retained as an initial failure.
* Second SQL attempt reached a responsive actual server but child test import
  failed (`No module named zava_forward`); zero acceptance tests executed.
  Container removed. Runner now captures invoking interpreter/environment before
  driver initialization so its subprocess retains the installed distributions.
* Ruff follow-up found one unbreakable f-string >100 columns, manually split.
* Third SQL attempt repeated the child import failure; capturing interpreter and
  environment alone did not solve driver re-execution. No engine acceptance
  claimed; container removed. Putting the invoking venv on PATH before driver
  initialization resolved it. Fourth SQL attempt: responsive loopback SQL
  Server, 25 actual API tests passed in 9.311s, container removed.
* Core mypy follow-up exposed list invariance despite explicit annotation;
  changed construction to typed list.extend/append. Core 3 files then passed.
* API mypy initial 4 errors exposed skipped typed core inheritance and invalid
  runtime receipt fixture. Enabled normal checking only for the typed sensor
  module, added core test lookup, and made receipt-time object validation explicit.
  New lookup exposed 247 pre-existing errors in four migrated core fixture
  modules. Those existing fixture imports now skip transitive API checking
  (core owns them); owned sensor modules/tests remain checked, not exempted.

## P02 current state

Narrow core/API guides, Proposed ADR implementation status, addendum sensor
boundary, KB index and append-only log updated. No memory/original edits.
Remaining: final expanded/focused regression/static checks and hardened image.

## Final implementation evidence (before original Review)

The earlier "Remaining" line is historical. P01/P02 are now complete within the
offline boundary, with the full API static limitation below explicitly retained.
Local judgment added malformed persisted-outcome detection (never a successful
fallback for corrupt witnesses), equal-time and actual JSON refusal checks, and
restricted SQL retention of closed-schema observations for actionable DQ.
Unknown-field/malformed input is not copied into that raw column. Restricted
metadata readers and receipts never return it. No new operational authority.

Final commands used the session venv Python at
`/home/azureuser/.copilot/session-state/350bfa26-8783-4b1f-81b7-0434d2d93881/files/venv/bin/python`.
`PY` below means that exact executable, not a changed source import path.

| Working directory | Actual command | Result |
| --- | --- | --- |
| src/core | `PY -m ruff check .` | Pass |
| src/core | `PY -m ruff format --check .` | Pass, 75 files |
| src/core | `PY -m mypy` | Pass, 128 source files |
| src/api | `PY -m ruff check .` | Pass |
| src/api | `PY -m ruff format --check .` | Pass, 27 files |
| src/api | `PY -m mypy src/zava_forward/api/sensor_ingestion.py tests/test_sensor_ingestion.py checks/sensor_sql_check.py` | Pass, 3 selected files and followed typed boundary |
| src/core | `PY -W ignore::ResourceWarning -m unittest discover -s tests -p 'test_sensor_*.py' -q` | 75 tests, 1 opt-in sensor112 MSSQL skip, no failures |
| src/core | `PY -W ignore::ResourceWarning -m unittest discover -s tests -p test_sqlstore.py -q` | 18 tests pass |
| src/api | `PYTHONPATH=tests:../core/tests:../agents/tests PY -W ignore::ResourceWarning -m unittest test_sensor_ingestion test_auth test_role_matrix test_role_endpoint_inventory test_chat_isolation -q` | 124 tests pass |
| repository | `PATH=<venv>/bin:$PATH PY src/api/checks/sensor_sql_check.py` | Actual responsive loopback SQL Server: 28 API tests pass, container removed |
| repository | `docker build --quiet -f src/api/Dockerfile -t ama-sensor110-api:offline-20261018 src` | Pass, final production image 52d3a038a16ed73e72ce4efa2b915e97f4e3b1eb763ed028d5e68799a5bde990 |

Hardened image command used `docker run --rm --network none --read-only
--cap-drop ALL --security-opt no-new-privileges`, tmpfs /tmp and /state,
read-only mounts of core/API test fixtures, `PYTHONPATH=/tests/core:/tests/api`,
and `ZF_DATA=/tmp/no-default-dataset.json`. Actual UID asserted 10001.
`unittest` loaded test_sensor_consumer, test_sensor_ingestion and test_sensor_privacy:
66 tests, 1 opt-in sensor112 SQL skip, no failures. A separate actual adapter
invocation in the same hardened configuration admitted two constructed rows,
closed/reopened the SQL store and reconciled two replays. No network or live
application/AI acceptance is inferred.

Existing resource warnings were visible in the first 72-test sensor regression;
later runs suppressed only ResourceWarning noise. The API preservation suite
logs the expected deliberately unloaded-law-store ValueError while all 124
assertions pass; it is not a sensor SQL success fallback.

Additional initial validation failures, retained:

* Full API `PY -m mypy`: 738 errors after the new core-fixture lookup exposed
  existing core-test modules plus absent browser types. Preserved existing
  core-test ownership by skipping only those imported legacy modules in API
  checking; full core mypy independently passes. No owned sensor module exemption.
* Full API mypy after that correction: 9 missing `playwright.sync_api` imports
  in 9 existing browser/test files, checked 60 source files. Repeated with the
  pinned baseline pyproject and those exact nine original files: same 9 missing
  dependency errors. No browser dependency install/execution under owner's
  no-Playwright/no-UI scope. Full API type-check is NOT green; owned checks pass.
* Expanded corrupt-witness check initially introduced one 101-column SQL string
  and one local variable inference conflict (`str | None` vs prior `str`).
  Split SQL and renamed historical reason variable before final validation.
  These were pre-Review implementation fixes, not original Review corrections.

The supported legacy/stock test now seeds a reading before compatibility setup
so actual migration preserves a populated table. Its final focused rerun is
recorded in the execution log, not inferred from an earlier empty-table check.
Final populated-legacy SQLite/core+API 2-case rerun passed; full actual SQL Server
API rerun 28 passed in 8.849s; final hardened image suite 66 passed (one existing
opt-in sensor112 SQL skip) in 0.724s. No production source changed after image
52d3a038; only that test's placement of the pre-existing legacy row changed.
Final Git diff whitespace check and test-file Ruff/formatter pass.

## Review handoff and unexecuted gates

Original critique: executed once, Revise, PC-001..007 directly dispositioned.
SHA-256: ad56b59a8df472fff31ed3ae906eca63505ea76fca0f63a457dda4acf540942b.
Original Review not yet executed at this handoff; no post-Review corrections.
No live Hub identity/transport, tier/sizing/cost/provisioning/network/credential
owner approval, Azure SQL application acceptance, real AI, DPO or operational
acceptance. Whole issue 110 cannot be closed. No issue/board changes or AC ticks.
Publication and complete independent exact-published-head review remain P03.

## Amendments and divergences

Single planning refinement PC-001..007 before implementation. No new policy
authority. Original critique Revise retained unchanged.

## Remaining work and handoff

The following line is the contradictory historical pre-Review handoff identified
by original RV-002; it is retained verbatim as adverse evidence, not current state:

P01/P02 pending. Review not executed; correction count 0.

## Current handoff after separately authorized correction ONE

P01/P02/P03 were completed for the original bounded offline delivery. Original
Review executed once, Complete / Defects found; RV-001 Medium, RV-002 Low and
RV-003 Low residual remain the immutable original findings. Later owner authority
resumed this same task in Implement for RV-001/RV-002 only, correction count ONE
of maximum TWO. No Research, critique or original Review was rerun.

Retained reading/witness validation now refuses malformed or inconsistent SQL
with bounded ConsumerError, preserving finite API committed-prefix metadata.
Historical exact replay remains independent of current withdrawn authority.
Actual SQLite and disposable SQL Server tests are green after recorded red runs.
Current correction validation, pinned integration, hashes and publication evidence
are recorded separately in
[the correction ONE receipt](issue-110-offline-sensor-consumer-correction-one.md).
Independent exact-published-head review remains the coordinator's gate; this is
implementation evidence, not a replacement Review or acceptance.

RV-003 full API baseline browser-import tooling remains residual and not green.
All whole-issue/live/human gates above remain unmet. No issue closure or AC tick.
