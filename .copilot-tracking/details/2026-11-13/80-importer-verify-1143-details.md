---
title: Issue 80 importer verification details
ms.date: 2026-11-13
---

Commands (logs under /tmp/imp-1143-logs, outside worktree; exit codes via `$?` written to files):

* `python3 -m venv --system-site-packages /tmp/venv-imp-1143`
* `/tmp/venv-imp-1143/bin/pip install --upgrade setuptools wheel`
* `/tmp/venv-imp-1143/bin/pip install --no-deps --no-build-isolation -e src/core -e src/agents -e src/importer -e src/api`
* Verify `zava_forward.<pkg>.__path__[0]` under worktree src/.
* `cd src/importer && python -m unittest discover -s tests -v`
* `cd src/api && PYTHONPATH=../core/tests:../agents/tests python -m unittest tests.test_list_export_api -v`

Success: exit 0 or explicit documented skips; failures recorded as-is, not fixed.

Revision after critique: use absolute venv python, PYTHONDONTWRITEBYTECODE=1, also run tests.test_exception_register_screen, check src tree for stray artefacts.
