---
title: Issue 135 C5 review
date: 2026-11-10
---

Single self-executed Review after implementation, at the C5 candidate. Not independent.

* Outcome: conformant for the scoped hosted-typing failure. The diff is one `pyproject.toml` override; source, runtime and tests are unchanged from `25946393`.
* The exact hosted failure reproduced in an isolated venv without the driver and is gone; MSSQL stays optional; strict typing of every other import is retained; no stub, broad ignore or workflow change.
* Driver-present and driver-absent both pass mypy, Ruff and 79 tests.
* Limits: hosted CI on the new head is not yet observed; C3 order adverse and the failed PR 1357 hosted run are preserved; whole 135/73 acceptance is not claimed. C5/5 is exhausted.
* Open findings: none.
