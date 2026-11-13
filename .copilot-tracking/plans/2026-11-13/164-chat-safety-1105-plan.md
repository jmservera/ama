---
title: Plan 164 chat safety verification
task_slug: 164-chat-safety-1105
---

# Plan

* [ ] P1 Create /tmp/venv-164-1105 (system-site-packages), pip install --no-deps -e src/core src/agents src/api; verify module paths inside worktree.
* [ ] P2 Run candidate modules (see details) per package with env -u ZF_DATA -u ZF_TEST_MSSQL, offline; save exit codes and counts.
* [ ] P3 Write changes file with per-module counts, skips, AC mapping for #164/#157 (scripted L2 offline vs unperformed live/human-labelled gates).
* [ ] P4 Remove venv; independent review; commit; witness.

No edits to src/ or docs/.

## Critique amendments (applied)

* Install: pip install --no-deps --no-build-isolation --no-index -e per package; blocker if unavailable.
* PYTHONDONTWRITEBYTECODE=1; check git status for src writes; remove untracked artifacts (egg-info) before commit.
* Run with unittest -v; confirm named memory-never-evidence test and injection/poisoning/isolation cases ran and passed; list skips.
* test_chat_fixture_roles belongs to api. Each package runs with its own tests dir first on PYTHONPATH.
* Record test_chat_eval.py:181 limitation (integrated memory poisoning not covered).
