---
title: "Research: issue 466 remaining criteria (r4), 2026-11-01"
ms.date: 2026-11-01
---

* Research disposition: executed (issue comments, merged PR list, fresh test and lint runs on `feat/issue-466-remaining` at `fa6b1c69e`). Planning Readiness: Ready.

## Findings

* Merged delivery: #471 to #474 (gauges, history, advisory assistant, account control), #586, #603 (gauges), #677, #722 (re-verification). Issue comments of 2026-10-27 and the 2026-10-31 closure audit tick criteria 2 to 6 as proven by merged code and tests.
* Only criterion 1 is unmet: "Owner confirms scope and priority". It is a human approval; the closure audit excludes substituting a confirmation. It is not deliverable by an agent.
* No deliverable code gap was found. Source changes are therefore out of scope for this task.

## Fresh evidence (2026-11-01, venv with pip editable installs from this worktree)

* `src/core`: `pytest tests/test_resident_sensors.py tests/test_resident_assistant.py` gave 15 passed, 14 subtests passed.
* `src/api`: `PYTHONPATH=../core/tests:../agents/tests pytest tests/test_resident_assistant_api.py tests/test_resident_assistant_provider.py tests/test_resident_preview_api.py` gave 36 passed.
* `ruff check`, `ruff format --check` and `mypy` passed in `src/core` (193 files) and `src/api` (145 files).
* The system-wide editable installs pointed at another worktree, so the first run failed on import; a clean venv resolved it. This is an environment note, not a defect.

## Not proven here

* Manual assistive-technology acceptance, live resident sign-in checks and live Azure behaviour are owner-run.
