---
title: 149 UX complete parent details
ms.date: 2026-11-13
---

* Run from src/api with `PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest <module>`. The first six modules live in src/api/tests; test_scenario_manifest and test_needs_inventory live in src/core/tests.
* Compare any failures with a pre-merge baseline on 8e786b62d (the #152 review notes four workbench navigation failures); record exact results.
* mypy strict over every src/api python file.
* Remove only /tmp/venv-uxp-1420 before commit.
* Commit tracking evidence on top of the merge; worktree clean and git diff --check empty.
