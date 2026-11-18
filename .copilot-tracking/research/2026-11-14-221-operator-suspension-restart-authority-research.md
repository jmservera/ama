---
title: Issue 221 restart authority and NFR-014 drill research
ms.date: 2026-11-14
---

* Disposition: executed. Planning Readiness: Ready.
* Existing: `continuity.suspend` records `restart_authority`; `restart_decide` requires a match. `governance.breach_record` required `restart_authority` but `breach_restart` accepted any `authority_ref` and nothing named RULE-024 or blocked automatic restart.
* Existing drill helper `drill()` in `src/api/tests/test_operator_suspension.py` had no explicit NFR-014 test name.
* Environment: the installed `zava_forward` resolves to another checkout, so tests need `PYTHONPATH` set to this worktree `src/*/src`.
