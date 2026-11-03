<!-- markdownlint-disable-file -->
---
title: Issue 159 role-gate receipt changes
description: Changes and validation for the role-gate denied-turn receipt slice
ms.date: 2026-11-03
---

## Changes

* `src/api/src/zava_forward/api/server.py`: the POST role gate records an `access-rejected` `chat.turn` receipt for refused `messages` and `ask` turns (3 lines).
* `src/api/tests/test_chat_panel.py`: two tests.
* No change to permissions, responses, knowledge base files, `mvp/` or private data.

## Validation (focused tier; venv in /tmp, pip only)

| Command | Result |
| --- | --- |
| `src/api`: `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_chat_panel.py -q` | Ran 45, OK (1 skipped); new test fails without the server change |
| `src/api`: same runner for `test_chat_isolation.py`, `test_chat_fixture_roles.py` | Ran 32 OK; Ran 1 OK |
| `src/core`: `python -m unittest discover -s tests -p test_chat_panel.py -q` | Ran 41, OK |
| `src/api`: `ruff check .`, `ruff format --check .` | clean |
| `src/api`: `mypy --cache-dir=/tmp/mypy-159` | 37 errors, identical before and after the change (missing `playwright` stubs and similar in untouched tests); none new |

## Not run

* Complete local RPI gate, full suites, benchmarks, browser checks, screen-reader or any assistive-technology run, hosted CI, independent review.
* Tier: focused. No SQL, infrastructure, deployment or new permission; the coordinator decides whether a gate is needed.
