---
title: Issue 126 changes
ms.date: 2026-10-15
---

* Added `mvp/zavaforward_mvp/governance.py` and `mvp/tests/test_governance.py`.
* Edited `store.py`, `sqlstore.py` (documents `procurement` and `governance`), `server.py` (routes), `mvp/README.md`, `docs/reference/README.md`, `docs/reference/log.md`.
* No divergence from the plan.

## PR 261 review fixes

* `governance.py`: added `guard_case_event` (pause check on every case, capture gate on cases flagged `pilot`); `breach_record` now needs a manager, quality inspector or building safety liaison; Shadow and Live release refused unless Phase 0 capture is released.
* `store.py`, `workflows.py`: `log_call`, `set_decision`, `advance` and `return_case` call the guard. Hazard paths are intentionally not guarded.
* Tests added in `test_governance.py`; `mvp/README.md` and `docs/reference/log.md` updated.
* Divergence: the capture gate applies only to pilot-flagged cases, because enforcing it on all cases broke 30 existing demo tests and the demo cohort is not the pilot.
