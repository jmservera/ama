---
title: Issue 134 demo preflight plan
ms.date: 2026-11-13
---

## Plan

* [ ] Phase 1: Critique this plan before any execution.
* [ ] Phase 2: Create /tmp/venv-preflight-1045 with pip, editable `--no-deps` installs of src/core, agents, api, importer; verify module origins under the worktree.
* [ ] Phase 3: Run unit modules with `env -u ZF_DATA`, capturing producer exit codes to a status file.
* [ ] Phase 4: Run read-only inspection script (stored outside the repo in /tmp, source embedded in changes log) over seed 20260901, as-of 2026-10-13 with the fictional register.
* [ ] Phase 5: Write changes log, remove venv, independent review, commit.

Validation tier: Focused. Write surface: `.copilot-tracking/` only.
