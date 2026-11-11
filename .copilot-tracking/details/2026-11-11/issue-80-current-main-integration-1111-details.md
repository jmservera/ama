---
title: Issue 80 current-main integration details
description: Commands and boundaries
ms.date: 2026-11-11
---

* cwd `src/api` of this worktree; Python `/tmp/ama-80-audit-venv-1110/bin/python` (editable installs of this worktree; import origins asserted by module `__file__`).
* `PYTHONPATH=../core/tests:../agents/tests:tests` only; `ZF_DATA` an owned temp path; direct exits to evidence files in `phase80-current-main-integration-evidence-1111`, no pipes.
* Browser classes use their built-in nonqueued lock; no outer `flock`. The checker also takes its own lock.
* Missing dependency: restore in the owned venv only after the actual failure.
* Only own tracking records are committed afterwards; no tests on another uncommitted tree.
