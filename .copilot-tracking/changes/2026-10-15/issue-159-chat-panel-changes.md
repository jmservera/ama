---
title: "Changes: conversational assistant panel (#159)"
ms.date: 2026-10-15
---

## Changes

* New: `src/core/.../chat_panel.py`, `src/core/tests/test_chat_panel.py`, `src/agents/.../chat.py`, `src/agents/tests/test_chat_model.py`, `src/api/tests/test_chat_panel.py`, `src/api/.../web/chat.js`.
* Edited: `src/api/.../server.py` (panel composition, `ask` and `proposals` routes), `web/{index.html,app.js,style.css}`, `src/api/pyproject.toml` and `src/core/pyproject.toml` (exemptions), `src/api/README.md`, `docs/reference/README.md`, `docs/reference/log.md`.
* No change to `mvp/`, `.env`, `.vscode` or `.copilot-tracking/github-issues`.

## Validation (local, venv with pip only)

| Command | Result |
| --- | --- |
| `src/core`: `python -m unittest discover -s tests -q` | Ran 256, OK |
| `src/core`: `ruff check .`, `ruff format --check .`, `mypy` | clean (62 source files) |
| `src/agents`: `python -m unittest discover -s tests -q` | Ran 47, OK |
| `src/agents`: ruff check, ruff format --check, mypy | clean |
| `src/importer`: unittest, ruff, mypy | Ran 9, OK; clean |
| `src/api`: `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -q` | Ran 457, OK (92 skipped) |
| `src/api`: ruff check, ruff format --check, mypy | clean (33 source files) |
| `src/orchestrator`: `PYTHONPATH=../core/tests python -m unittest discover -s tests -q` (after `pip install -e ../orchestrator`) | Ran 17, OK |
| `python3 tools/rename-zava-tests.py` | Not run to success: `PIL` and `pptx` are not installed locally (environment, unrelated to this change) |
| Local app with synthetic data (`/tmp` script on `dataset.build()` and a stub model), Playwright keyboard-only: open case, open panel with Enter, ask, submit with Enter | Cited answer with label rendered, status "New answer added." |
| `docker ps` | permission denied on the Docker socket; image and `mssql` jobs rely on CI |

## Notes

* An inherited-test duplicate (`Matrix` imported by name) made `test_new_endpoints_for_every_role` fail when run twice in one process; fixed by importing the module (`import test_role_matrix as roles`).
* Not implemented, left unticked: screen-reader test, live model run, real chat data, streaming and resumable panel.
