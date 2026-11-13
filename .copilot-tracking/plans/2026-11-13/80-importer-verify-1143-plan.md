---
title: Issue 80 importer verification plan
ms.date: 2026-11-13
---

* [ ] Phase 1: critique plan before any venv or test run.
* [ ] Phase 2: create /tmp/venv-imp-1143, editable-install core, agents, importer, api (pip, no-deps, no-build-isolation); verify paths inside worktree.
* [ ] Phase 3: run src/importer unittest discover -v and src/api test_list_export_api (PYTHONPATH core/agents tests dirs only, never mvp); save logs externally, record exit codes, counts, skips, sha256.
* [ ] Phase 4: write changes, remove venv, review, commit (Refs #80, #176, #135).

No edits to src/ or docs/. Focused tier; classification basis: tracking-only write surface.
