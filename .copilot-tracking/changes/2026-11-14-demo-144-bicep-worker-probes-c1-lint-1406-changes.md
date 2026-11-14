---
title: Changes: C1 ruff correction
ms.date: 2026-11-14
---

* Source changes: none; `infra/tests/test_container_hosting_completeness.py` already conforms.
* Added dated RPI artifacts only; prior artifacts unchanged.
* Validation: ruff check and format check on the file exit 0 (0.17.1 and 0.17.3); `az bicep build --file infra/main.bicep --stdout` exit 0; `unittest discover -s infra/tests -p 'test_*.py' -q` exit 0 (601 tests, 4 skipped) with core, agents and orchestrator installed in a venv.
* Caches in `/tmp`; none in the worktree.
* Not run: `rpi-checks.py --all`, Docker, hosted CI (focused tier).
