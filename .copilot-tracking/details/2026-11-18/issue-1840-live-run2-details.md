---
title: "Details: issue 1840 completed() classification"
ms.date: 2026-11-18
---

Phase 1: tests in `src/api/tests/test_old_image_sql_probe.py`, extend near `test_unproved_mismatch_completion_does_not_blame_the_row` with a subTest table of malformed `restart_after_mismatch` records.

Phase 2/3: in `src/api/checks/old_image_sql_probe.py`, `execution_gaps` returns the list of gap strings for the `executed` and `reinvoked` blocks; `completed(name, step, tids)` returns `step.get("status") == "ok" and not execution_gaps(name, step, wanted)`. Release identities, adverse precedence and the late-restoration audits are untouched.

Phase 4: commands run from `src/api` with `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`.
