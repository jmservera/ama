<!-- markdownlint-disable-file -->
---
title: Issue 159 role-gate receipt phase details
description: Step-level details for the role-gate denied-turn receipt slice
ms.date: 2026-11-03
---

## Phase 1: gate receipt

* File: `src/api/src/zava_forward/api/server.py`, POST dispatch, inside `if not projection.allowed(u, "post", "POST")`.
* Split the path; when it is `api/chat/threads/<tid>/(messages|ask)` call `app.panel.record_rejected(u, tid)` before the existing 403.
* `record_rejected` writes the audit row only; it does not read the body, so the question is never logged.

## Phase 2: tests

* File: `src/api/tests/test_chat_panel.py` (outside the package).
* `test_role_gate_denials_record_one_receipt_per_turn_route`: contractor on `ask` and `messages` gets 403 and one receipt each.
* `test_role_gate_denial_of_other_chat_routes_records_no_turn_receipt`: contractor `archive` gets 403 and no turn receipt.
* Verified the first test fails when the server change is stashed.

## Phase 3: checks

* `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_chat_panel.py -q` from `src/api`.
* `ruff check .`, `ruff format --check .`, `mypy --cache-dir=/tmp/mypy-159`.
