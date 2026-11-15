---
title: Issue 132 changes
date: 2026-11-14
---

* `src/core/src/zava_forward/core/job_pack.py`: new field and claim key.
* `src/core/src/zava_forward/core/staff_intake.py`: field on escalation destination and boundaries.
* `src/core/tests/test_job_pack.py`: field assertion and claim rejection test.

Validation: ruff check and format (line length 100) pass on core and api; test_job_pack (11), test_fieldwork_variation_owner_guard (14) pass with PYTHONPATH on worktree sources.

Note: the installed zava_forward distribution shadows worktree sources, so tests need PYTHONPATH=src/*/src.
