<!-- markdownlint-disable-file -->
---
title: Issue 159 validation-refusal receipts changes
description: Implementation record for the initial feature increment
ms.date: 2026-11-09
---

## Changes

* src/core/src/zava_forward/core/chat_panel.py: `ChatPanel.record_validation_refused(user, tid=None)` (14 lines). Rechecks the user, writes nothing for a refused user, otherwise one audit row: stored `chat.turn` with `_receipt(tid)`, unstored `chat.turn.unstored` with `{outcome: rejected, model_calls: 0}`; case target empty.
* src/api/src/zava_forward/api/server.py `_chat`: one helper call before each of the three `ValueError` raises (3 lines). Messages and 400 mapping unchanged.
* src/api/tests/test_chat_panel.py: two tests (receipt shape, canary, spy and count for the three branches; normal-receipt and pre-check-denial controls).
* src/core/tests/test_chat_panel.py: two tests (exact shapes on JSON and SQL-backed stores, restart equality; refused-user no-op).
* Own increment over the merge: 4 files, 113 insertions, 0 deletions. No schema, migration, store, CI or config change.

## Divergences and debugging

* Test-only: first draft asserted `target`; the audit entry key is `case`. Fixed before the final run.
* A module-name invocation of the API tests shadowed by the core test of the same name, and a core run from the wrong directory, were invocation mistakes; both logs are retained and the CI `discover -s tests` form was used for all counted results.
* Plan decision D1 as revised (refused user keeps the 400 and gets no new receipt) was implemented as planned. No amendment to the plan.

## Validation (owner demo-targeted tier; external logs in the coordinator session files directory `159-impl-logs/`, hashes in `SHA256SUMS.txt`)

* Red before source change: core 3 errors (`AttributeError`, helper absent) in 45 tests; API `test_validation_refused_turns_record_one_metadata_only_receipt` failed with 0 != 1 for the unstored branch while the controls passed.
* Core, from src/core: `unittest discover -s tests -p 'test_chat*.py'` 134 OK; `-p test_regulatory_chat.py` 25 OK.
* API, from src/api with `PYTHONPATH=../core/tests:../agents/tests`: `test_chat*.py` 100 OK (1 skipped, opt-in local Chromium test), `test_regulatory_chat_api.py` 9, `test_role_endpoint_inventory.py` 22, `test_resident_chat_api.py` 51, all OK.
* Ruff 0.17.1 `check .` and `format --check .` in both projects: exit 0. Strict mypy 2.4.0 (project config, CI profile): core 276 files, api 202 files, no issues. No Any, casts, ignores or config changes.
* Not run: full gate, Docker, standalone SQL Server, browser, hosted CI, full API and core suites. The SQL-backed (SQLite) audit persistence is covered by the core test.
