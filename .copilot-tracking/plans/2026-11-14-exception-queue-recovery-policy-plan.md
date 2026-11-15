---
title: Issue 135 exception queue plan
ms.date: 2026-11-14
---

* Add `unresolved_eligibility: True` and `recovery_policy` (allowed actions, `automatic_replay: False`, `automatic_release: False`) to every item.
* Add `automatic_replay`/`automatic_release` False to the recorded recovery.
* Tests: core queue test per failure kind; API register assertion.
* Critique (single pass): additive fields keep existing `eligibility` and `recovery is None` contracts; accepted.
* Validation: targeted unittest modules with worktree PYTHONPATH and TMPDIR=/dev/shm/zf-tmp, ruff, mypy. No unittest discover.
