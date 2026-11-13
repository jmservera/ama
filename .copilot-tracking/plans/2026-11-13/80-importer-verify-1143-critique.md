---
title: Issue 80 importer verification critique
ms.date: 2026-11-13
---

Independent critique (rubber-duck subagent) verdict: REVISE, dispositions below.

* Pip upgrade uses default index: kept, mandated by the owner brief (pip only); if it fails, record as blocker, no workaround.
* Bare python: accepted. Use /tmp/venv-imp-1143/bin/python.
* Egg-info and bytecode: accepted. Set PYTHONDONTWRITEBYTECODE=1; confirm git status is clean of untracked src artefacts (egg-info is gitignored or removed before commit).
* test_exception_register_screen.py also has CSV tests: accepted, added to the run in addition to test_list_export_api.

Post-revision verdict: APPROVE.
