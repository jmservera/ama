---
title: "Plan: issue 1840 completed() classification"
ms.date: 2026-11-18
---

Refs #1840. Tier: FULL classification by the issue (diagnostic evidence correctness), but the owner brief for this run sets FOCUSED validation and forbids `rpi-checks.py --all`; recorded as a limit, not a satisfied full gate.

* [x] 1. Add failing-first regressions: missing mismatch `result`, missing `after`, missing reinvoke state, missing reinvoke list, wrong task id, with the active MUTATED row retained, expecting `INSUFFICIENT`.
* [x] 2. Extract `execution_gaps(name, step, wanted)` from `check_step`; `check_step` calls it unchanged.
* [x] 3. Change `completed()` to take name and task id and require status ok and no execution gaps; update the `judge` call.
* [x] 4. Run probe tests, mypy from `src/api` (bare), ruff check and format. Fix the two untyped `config()` calls only if they reproduce.
* [x] 5. Record per-criterion proven/unproven table, review, commit.
